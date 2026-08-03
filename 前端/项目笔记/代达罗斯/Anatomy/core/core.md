这三个核心文件构成了一条完整链路：

```text
编辑结构
anatomy-tree.ts
    ↓ AnatomyDraftInput
发布前校验
validate-anatomy-for-publish.ts
    ↓ 合法定义
检查真实文件树
check-anatomy.ts
    ↓ Result<检查结果, 定义错误>
```

`index.ts` 只是桶导出，不包含业务逻辑。

## 一、共同的数据结构

核心类型定义在 [anatomy-schema.ts](G:/Save/Grogramming/CodeForge/daedalus/packages/schemas/src/anatomy-schema.ts:25)。

```text
AnatomyStructure
└── root
    └── children: AnatomyNode[]
        ├── FileEntry
        ├── DirectoryEntry
        │   └── children: AnatomyNode[]
        └── OneOfGroup
            └── alternatives: AnatomyEntry[]
                ├── FileEntry
                └── DirectoryEntry
```

关键类型可以简化为：

```ts
type AnatomyNode =
  | AnatomyEntry
  | {
      id: string;
      kind: "one_of";
      minimumMatches: number;
      maximumMatches: number;
      alternatives: AnatomyEntry[];
    };

type AnatomyEntry =
  | {
      kind: "file";
      id: string;
      name: AnatomyName;
      quantity: AnatomyQuantity;
      policyOverrides: AnatomyPolicyOverrides;
    }
  | {
      kind: "directory";
      id: string;
      name: AnatomyName;
      quantity: AnatomyQuantity;
      policyOverrides: AnatomyPolicyOverrides;
      children: AnatomyNode[];
    };
```

这里最重要的是：

- `AnatomyNode` 可以是文件、目录或 `one_of`。
- `directory.children` 是 `AnatomyNode[]`，所以目录中可以放 `one_of`。
- `one_of.alternatives` 是 `AnatomyEntry[]`，不能直接嵌套另一个 `one_of`。
- 根节点不是普通目录，没有 `id`、`kind`、`name`，只有 `children`。
- `kind` 是判别字段。写出 `node.kind === "directory"` 后，TypeScript 就知道它一定存在 `children`。

名称也采用判别联合：

```ts
type AnatomyName =
  | { type: "literal"; value: "index.ts" }
  | { type: "placeholder"; value: "<Name>.tsx" };
```

数量规则：

```ts
"optional"      // 0..1
"exactly_one"   // 1..1
"one_or_more"   // 1..Infinity
"zero_or_more"  // 0..Infinity
```

---

# 二、`anatomy-tree.ts`：树的构造、查询和修改

文件：[anatomy-tree.ts](G:/Save/Grogramming/CodeForge/daedalus/packages/anatomies/src/core/anatomy-tree.ts:1)

它只关心“如何编辑定义树”，不判断真实文件是否符合定义。

## 1. `uid`：IIFE + 闭包

```ts
const uid = (() => {
  const state = { counter: 0 };

  return (): string => {
    state.counter += 1;
    return crypto.randomUUID?.() ?? `node-${state.counter}-${Date.now()}`;
  };
})();
```

这是立即执行函数 IIFE。

执行过程：

1. 模块加载时执行外层 `() => {...}`。
2. 创建私有的 `state`。
3. 返回真正的 `uid` 函数。
4. 后续每次调用 `uid()`，都能访问同一个 `state`。

需要注意：

- `state` 对模块外部不可见。
- 主路径 `crypto.randomUUID()` 会生成合法 UUID。
- fallback 的 `node-1-...` 不是 UUID，而 Zod Schema 要求 `z.string().uuid()`。现代浏览器和 Node 通常都有 `randomUUID`，但 fallback 与 Schema 约束并不完全一致。

## 2. `cloneEntry`：保留具体泛型类型

```ts
const cloneEntry = function <T extends AnatomyEntry>(entry: T): T {
  return JSON.parse(JSON.stringify(entry)) as T;
};
```

`T extends AnatomyEntry` 表示：

- 参数必须属于 `AnatomyEntry`。
- 返回值保留传入时的具体类型。

例如：

```ts
const directory = createDirectoryEntry("src");
const cloned = cloneEntry(directory);
// cloned 仍然知道自己是 directory，而不是宽泛的 AnatomyEntry
```

需要注意：

- `JSON.parse()` 返回 `any`，所以这里必须用 `as T` 告诉 TS 返回类型。
- 这个断言由开发者承担正确性，TS 无法验证。
- 当前 Anatomy 数据只有普通对象、数组、字符串和数字，JSON 深拷贝基本可用。
- 如果以后加入 `Date`、`Map`、`undefined` 或自定义类，JSON 深拷贝会丢失信息。

## 3. 创建文件和目录

```ts
export const createFileEntry = function (
  name: string,
  quantity?: (typeof AnatomyQuantityValues)[number],
): AnatomyEntry & { kind: "file" }
```

`(typeof AnatomyQuantityValues)[number]` 是一个重要写法。

假设：

```ts
const AnatomyQuantityValues = [
  "optional",
  "exactly_one",
  "one_or_more",
  "zero_or_more",
] as const;
```

那么：

```ts
typeof AnatomyQuantityValues
// readonly ["optional", "exactly_one", ...]

(typeof AnatomyQuantityValues)[number]
// "optional" | "exactly_one" | "one_or_more" | "zero_or_more"
```

它避免手写重复的联合类型。

返回类型：

```ts
AnatomyEntry & { kind: "file" }
```

意思是返回值既是 AnatomyEntry，又确定为文件分支。因此调用方不会误访问目录的 `children`。

两个 Factory 默认：

- 数量是 `"optional"`。
- 策略覆盖是空对象。
- 名称类型是 `"literal"`。
- 目录可以通过默认参数 `children = []` 创建空目录。

## 4. `locateNodeInTree`：递归查找

```ts
type LocatedNode =
  | {
      found: true;
      node: AnatomyNode;
      parent: TreeNodeParent;
      index: number;
    }
  | { found: false };
```

这是典型的可辨别联合：

```ts
const result = locateNodeInTree(...);

if (result.found) {
  result.node;   // 安全
  result.parent; // 安全
  result.index;  // 安全
}
```

查找逻辑：

1. 遍历当前 `children`。
2. 当前节点 ID 相等，立即返回。
3. 当前节点是目录，递归检查 `child.children`。
4. 当前节点是 `one_of`，先检查 alternatives 本身。
5. alternative 是目录时，再检查它的 children。
6. 全部找不到返回 `{ found: false }`。

`parent` 有三种可能：

```ts
type TreeNodeParent =
  | DirectoryEntry
  | OneOfGroup
  | null;
```

`index` 的含义取决于 `parent`：

- `parent === null`：在 `root.children` 中的位置。
- `parent.kind === "directory"`：在 `parent.children` 中的位置。
- `parent.kind === "one_of"`：在 `parent.alternatives` 中的位置。

这里的 `Extract`：

```ts
Extract<AnatomyNode, { kind: "one_of" }>
```

表示从 `AnatomyNode` 联合类型中提取 `kind: "one_of"` 的那个成员。

## 5. 不可变修改

### 插入 `insertAnatomyNode`

```ts
insertAnatomyNode(structure, parentId, node)
```

- `parentId === null`：插入根节点。
- 找不到 parent：原样返回 `root`。
- parent 不是目录：原样返回。
- parent 是目录：复制目录、追加 child，再替换回树中。

核心不可变写法：

root与root不是一个东西

```ts
return {
  ...root,
  root: {
    ...root.root,
    children: [...root.root.children, node],
  },
};
```

它不会对原来的 `children.push()`。

### 删除 `removeAnatomyNode`

根据 parent 类型分别处理：

- 根节点：过滤 `root.children`。
- `one_of` alternative：过滤 `alternatives`。
- 普通目录子节点：过滤 `children`。

```ts
children.filter((child) => child.id !== nodeId)
```

注意：从二选一分组中删除一个 alternative 后，可能只剩一个选项。TypeScript 的 `AnatomyEntry[]` 无法表达“至少两个元素”，所以树编辑函数允许暂时产生不满足 Zod `.min(2)` 的草稿。

### 更新 `updateAnatomyNode`

```ts
updateAnatomyNode(root, nodeId, updater)
```

`updater` 使用高阶函数：

```ts
(node: AnatomyNode) => AnatomyNode
```

调用示例：

```ts
updateAnatomyNode(structure, nodeId, (node) => ({
  ...node,
  name: { type: "literal", value: "new-name.ts" },
}));
```

递归中通过 `map` 生成新数组：

```ts
children.map((child) => {
  if (child.id === nodeId) return updater(child);

  if (child.kind === "directory") {
    return { ...child, children: recurse(child.children) };
  }

  return child;
});
```

对 `one_of.alternatives` 有额外限制：

```ts
const updated = updater(alt as AnatomyNode);

return updated.kind === "one_of"
  ? alt
  : (updated as AnatomyEntry);
```

原因是 `alternatives` 只能包含文件或目录，不能把 alternative 更新为 `one_of`。

这里两个 `as` 都是类型逃生口。运行时通过 `kind` 检查保障数据约束，但 TS 本身没有从 updater 返回类型中得到这个保证。

另外，`updater` 应当写成纯函数。类型系统没有阻止下面这种原地修改：

```ts
(node) => {
  node.id = "changed";
  return node;
}
```

这种写法会破坏“不修改旧树”的假设，应坚持使用展开运算符创建新对象。

## 6. `groupSiblingEntries`

它把同一父节点下至少两个文件/目录组合为：

```ts
{
  id: uid(),
  kind: "one_of",
  minimumMatches: 1,
  maximumMatches: 1,
  alternatives: [...]
}
```

算法使用两个数组：

```ts
const entriesToGroup: AnatomyEntry[] = [];
const remaining: AnatomyNode[] = [];
```

遍历一次 children：

- ID 被选中且是 file/directory → `entriesToGroup`
- 其他节点 → `remaining`

最终：

```ts
const newChildren = [...remaining, group];
```

因此需要注意：被分组的元素会从原位置移除，新的 `one_of` 会放在当前 children 的末尾。

---

# 三、`validate-anatomy-for-publish.ts`：验证定义是否合法

文件：[validate-anatomy-for-publish.ts](G:/Save/Grogramming/CodeForge/daedalus/packages/anatomies/src/core/validate-anatomy-for-publish.ts:1)

它验证的是 Anatomy 定义本身，不读取真实文件。

返回值：

```ts
Result<AnatomyDraftInput, AnatomyValidationIssue[]>
```

也就是：

```ts
Ok<AnatomyDraftInput>
// 定义可以继续发布/检查

Err<AnatomyValidationIssue[]>
// 定义存在问题，而且一次返回所有问题
```

## 1. 错误码类型写法

```ts
export const AnatomyValidationCode = {
  duplicateId: "duplicate_id",
  // ...
} as const;

type Code =
  (typeof AnatomyValidationCode)[keyof typeof AnatomyValidationCode];
```

拆开理解：

```ts
keyof typeof AnatomyValidationCode
// "duplicateId" | "duplicateLiteralName" | ...

(typeof AnatomyValidationCode)[...]
// "duplicate_id" | "duplicate_literal_name" | ...
```

最终 Issue 的 `code` 只能是对象中的值，不会退化为普通 `string`。

## 2. 路径和 placeholder 校验

placeholder 正则：

```ts
/^<[^<>/\\]+>[^/\\]*$/
```

允许：

```text
<Name>
<Name>.tsx
<Component>.test.tsx
```

不允许：

```text
prefix-<Name>.tsx
<A/B>.tsx
<<Name>>.tsx
<Name>/index.ts
```

真实路径检测会拒绝：

- `/usr/src`
- `C:\src`
- `\\server\share`
- `../src`
- `src/../file`

它主要阻止绝对路径和目录穿越。不过普通的 `foo/bar` literal 不会被这个函数直接拒绝。

## 3. 全局重复 ID

```ts
const seenIds = new Set<string>();
```

每访问一个节点：

```ts
if (seenIds.has(node.id)) {
  issues.push(...);
}
seenIds.add(node.id);
```

这个 Set 在整个递归过程中共享，所以检查的是全树唯一性，而不是只检查兄弟节点。

## 4. 同级 literal 重名

```ts
const literalNames = new Map<string, string>();
```

Map 的结构是：

```ts
Map<名称, 第一次出现该名称的节点ID>
```

只检查同一 `nodes` 数组中的普通文件/目录：

```ts
if (node.kind === "one_of" || node.name.type !== "literal") {
  continue;
}
```

进入 `one_of` 后，会递归对 alternatives 进行单独的同级检查。

因此“目录直属 children”和“某个 one_of 内部 alternatives”属于不同作用域。

## 5. one-of 范围

检查两类错误：

```ts
minimumMatches < 1
maximumMatches < 1
minimumMatches > maximumMatches
```

以及：

```ts
minimumMatches > alternatives.length
maximumMatches > alternatives.length
```

例如有两个 alternatives，却配置：

```ts
minimumMatches: 2,
maximumMatches: 3
```

最大匹配数 3 永远无法满足，所以是 `impossible_one_of`。

## 6. 递归访问方式

```ts
if (node.kind === "one_of") {
  visitNodes(node.alternatives, node.id);
  continue;
}

validateName(node, parentId);

if (node.kind === "directory") {
  visitNodes(node.children, node.id);
}
```

`continue` 很重要：它保证 `one_of` 不会继续进入普通 Entry 的名称和目录分支。

需要注意：这个函数做的是发布语义校验，并没有调用 `anatomyDraftInputSchema.safeParse()`。因此它假设调用方已经完成 Zod 解析。TypeScript 类型只在编译期有效，不能阻止外部 JSON 在运行时传入错误结构。

---

# 四、`check-anatomy.ts`：将定义与真实文件树对比

文件：[check-anatomy.ts](G:/Save/Grogramming/CodeForge/daedalus/packages/anatomies/src/core/check-anatomy.ts:1)

输入分成两类：

```ts
checkAnatomy(definition, entries)
```

- `definition`：用户设计的 Anatomy 定义。
- `entries`：CLI 从真实文件系统收集出来的树。

真实文件树刻意很简单：

```ts
type AnatomyFileTreeEntry =
  | { kind: "file"; name: string }
  | {
      kind: "directory";
      name: string;
      children: AnatomyFileTreeEntry[];
    };
```

真实节点不需要：

- ID
- quantity
- policyOverrides
- placeholder

因为这些都是“预期约束”，不是真实文件属性。

## 1. 首先验证定义

```ts
const validated = validateAnatomyForPublish(definition);
if (validated.isErr()) return err(validated.error);
```

所以结果有两个层次：

```ts
Err<AnatomyValidationIssue[]>
// 规则定义本身不合法，无法检查

Ok<AnatomyCheckResult>
// 检查完成，可能符合，也可能不符合
```

不要把 `Err` 和 `conforms: false` 混在一起：

- `Err`：定义坏了。
- `Ok({ conforms: false })`：定义没问题，但真实项目违反了定义。

## 2. 名称匹配

literal 会被转换为完整匹配正则：

```ts
index.ts → /^index\.ts$/
```

特殊字符先通过：

```ts
value.replaceAll(/[.*+?^${}()|[\]\\]/g, "\\$&")
```

转义，防止文件名中的 `.`、`+` 等被当作正则语法。

placeholder：

```ts
<Name>.tsx → /^.+\.tsx$/
```

这里真正参与匹配的是 `>` 后面的 suffix。`<Name>` 只是给人看的变量名，并不限制实际文本内容。

## 3. 数量转换

```ts
getQuantityRange(entry.quantity)
```

将枚举转换成统一结构：

```ts
{ minimum: number; maximum: number }
```

这样后续算法只需要比较：

```ts
correctIndexes.length < minimum
position >= maximum
```

不必到处写 quantity 的 switch。

参数类型：

```ts
AnatomyEntry["quantity"]
```

这是索引访问类型，表示直接复用 `AnatomyEntry` 中 `quantity` 字段的类型。

## 4. `checkNodes` 与 `consumed`

每一层目录都会创建一个：

```ts
const consumed = new Set<number>();
```

Set 中存的是已经被某条约束匹配/处理的真实文件下标。

这样一个真实文件不会在正常情况下被重复用于多个预期 Entry，同时最后可以把未消费节点报告为 `unexpected_entry`。

单个 Entry 的匹配顺序是：

1. 名称相同但 kind 不同 → `nesting_mismatch`
2. kind 相同、名称只存在大小写差异 → `name_mismatch`
3. 名称和 kind 都正确 → 数量检查
4. 正确目录 → 递归检查 children
5. 没有关联匹配且不足最小数量 → `missing_required`
6. 所有约束处理后仍未消费 → `unexpected_entry`

例如预期：

```text
file index.ts
```

实际：

```text
directory index.ts/
```

它会报告 `nesting_mismatch`，不会再同时报告一条 `missing_required`，因为代码专门避免了重复报错：

```ts
nestingMismatchIndexes.length === 0 &&
nameMismatchIndexes.length === 0
```

## 5. 策略继承

策略优先级在 [resolveAnatomyPolicies](G:/Save/Grogramming/CodeForge/daedalus/packages/schemas/src/anatomy-schema.ts:256) 中实现：

```text
当前 Entry 的 policyOverrides
            ↓ 没配置
最近的父目录 policyOverrides
            ↓ 没配置
Anatomy defaultPolicies
```

`ancestors` 是从根到当前目录的数组，解析时反转后寻找，因此最近的父目录优先。

需要注意：

- `one_of` 本身没有 `policyOverrides`，它的匹配错误使用父目录或全局策略。
- `quantityExceeded` 使用 `unexpectedEntry` 策略，因为策略模型中没有单独的 quantity 策略。

## 6. one-of 检查

对于：

```ts
{
  minimumMatches: 1,
  maximumMatches: 1,
  alternatives: [index.ts, index.tsx],
}
```

实际情况：

```text
只有 index.ts       → 匹配数 1，通过
两个都没有          → 匹配数 0，one_of_mismatch
两个文件都存在      → 匹配数 2，one_of_mismatch
```

匹配数表示“有多少个 alternative 得到匹配”，不是文件总数。

这里采用按定义顺序、贪心消费的算法。若多个 placeholder 可以匹配同一个真实文件，定义顺序可能影响最终结果；设计 Anatomy 时应尽量避免重叠模式，例如同时存在：

```text
<Name>.tsx
<Component>.tsx
```

因为两者实际正则完全相同。

## 7. 汇总和 conforms

```ts
const summary = issues.reduce(
  (counts, issue) => ({
    ...counts,
    [issue.severity]: counts[issue.severity] + 1,
  }),
  { block: 0, warn: 0, allow: 0 },
);
```

即使 severity 是 `"allow"`，Issue 仍会保留，只是不阻止通过。

```ts
conforms: summary.block === 0
```

因此：

- 有 warn：仍然 `conforms: true`
- 有 allow：仍然 `conforms: true`
- 至少一个 block：`conforms: false`

---

# 五、贯穿三个文件的例子

先用树操作创建两个文件：

```ts
let structure = createEmptyStructure();

structure = insertAnatomyNode(
  structure,
  null,
  createFileEntry("index.ts", "exactly_one"),
);

structure = insertAnatomyNode(
  structure,
  null,
  createFileEntry("index.tsx", "exactly_one"),
);
```

然后把它们组合为 one-of：

```ts
structure = groupSiblingEntries(
  structure,
  null,
  [indexTsId, indexTsxId],
);
```

结果类似：

```ts
{
  schemaVersion: 1,
  root: {
    children: [
      {
        id: "...",
        kind: "one_of",
        minimumMatches: 1,
        maximumMatches: 1,
        alternatives: [
          { kind: "file", name: { type: "literal", value: "index.ts" } },
          { kind: "file", name: { type: "literal", value: "index.tsx" } },
        ],
      },
    ],
  },
}
```

发布时 `validateAnatomyForPublish` 检查：

- 所有 ID 是否唯一。
- alternative 名称是否重复。
- `1..1` 是否是合法范围。
- 范围是否没有超过两个 alternatives。

CLI 检查真实目录：

```ts
[
  { kind: "file", name: "index.ts" },
  { kind: "file", name: "index.tsx" },
]
```

两个 alternatives 都匹配，匹配数量为 2，但最大允许 1，最终产生：

```ts
{
  code: "one_of_mismatch",
  severity: "warn" | "block" | "allow",
  constraintId: oneOfGroupId,
  path: ".",
}
```

---

## 最需要记住的 TypeScript 点

- `kind` / `type` 是判别字段，优先通过判断它们缩窄联合类型。
- `(typeof Values)[number]` 从常量数组生成值联合类型。
- `(typeof Codes)[keyof typeof Codes]` 从常量对象生成值联合类型。
- `AnatomyEntry["quantity"]` 复用对象字段类型。
- `Extract<Union, Condition>` 从联合类型中提取某个分支。
- `Result<T, E>` 明确区分成功值和错误值。
- `as T`、`as AnatomyEntry` 不提供运行时安全，只是开发者向 TS 作保证。
- Zod 的 `.uuid()`、`.min(2)` 等运行时约束不会完整体现在普通 TS 类型中。
- 不可变更新函数要求 updater 保持纯函数习惯，类型本身没有强制 `readonly`。

当前核心测试共 20 项全部通过，`tsc --noEmit` 也通过；本次仅做了代码分析，没有修改文件。