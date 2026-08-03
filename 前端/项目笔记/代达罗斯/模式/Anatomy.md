# Anatomy



针对这个需求，最合适的方案不是直接保存一个递归 JSON，而是：

> **数据库和业务层使用扁平的邻接表结构 `parentId + sortOrder`，接口展示时转换为树，前端编辑时使用标准化数据。**

这样既能表达多层目录，也方便拖拽排序、移动、删除和校验父子关系。

---

## 一、核心领域模型

建议拆成三个实体关系：

```text
Crate
  └── anatomyId

Anatomy
  └── AnatomyNode[]
         └── parentId
```

关系为：

```text
一个 Anatomy
├── 包含多个 AnatomyNode
└── 可以被多个 Crate 引用
```

Anatomy 本身可以视为代码包的“虚拟根目录”，不需要额外保存一个根节点。

---

## 二、Anatomy 基础定义

```ts
type AnatomyStatus = "active" | "archived"

interface Anatomy {
  id: string

  name: string
  description?: string

  status: AnatomyStatus

  createdAt: string
  updatedAt: string
}
```

归档不等于删除：

* `active`：可以继续选择和编辑。
* `archived`：不能被新的 Crate 选择，但已经关联的 Crate 仍然可以查看。
* 被 Crate 引用的 Anatomy 不建议允许硬删除。

---

## 三、目录节点的数据结构

### 名称规则

不要同时设计成：

```ts
name?: string
pattern?: string
```

因为可能出现两个字段同时存在或者都不存在。

更推荐使用可辨识联合类型：

```ts
type NodeNameRule =
  | {
      type: "exact"
      value: string
    }
  | {
      type: "glob"
      value: string
    }
```

例如：

```ts
const exactName: NodeNameRule = {
  type: "exact",
  value: "src",
}

const patternName: NodeNameRule = {
  type: "glob",
  value: "*.test.ts",
}
```

第一阶段建议只支持：

* `exact`：精确名称。
* `glob`：通配符模式。

例如：

```text
src
components
*.test.ts
*.stories.tsx
use*.ts
```

不建议第一阶段直接使用正则表达式，因为正则的校验、转义和跨语言执行都更复杂。

---

## 四、推荐的持久化节点结构

```ts
type AnatomyNodeType = "directory" | "file"

interface AnatomyNode {
  id: string

  anatomyId: string
  parentId: string | null

  nodeType: AnatomyNodeType
  nameRule: NodeNameRule

  required: boolean
  description?: string

  sortOrder: number

  createdAt: string
  updatedAt: string
}
```

其中：

* `anatomyId`：节点属于哪个 Anatomy。
* `parentId`：父目录节点 ID。
* `parentId === null`：表示 Anatomy 根层级节点。
* `nodeType`：文件或目录。
* `nameRule`：精确名称或命名模式。
* `required`：必需或可选。
* `sortOrder`：同一父节点下的显示顺序。

---

## 五、完整数据示例

下面的数据描述了这样的结构：

```text
src/                         必需
├── components/              必需
│   └── *.tsx                可选
├── hooks/                   可选
│   └── use*.ts              可选
└── index.ts                 必需
README.md                    可选
```

扁平数据可以保存为：

```ts
const anatomy = {
  id: "anatomy-react-library",
  name: "React Component Library",
  description: "React 组件库标准目录结构",
  status: "active",
} satisfies Anatomy

const nodes: AnatomyNode[] = [
  {
    id: "node-src",
    anatomyId: anatomy.id,
    parentId: null,
    nodeType: "directory",
    nameRule: {
      type: "exact",
      value: "src",
    },
    required: true,
    description: "源代码目录",
    sortOrder: 0,
    createdAt: "",
    updatedAt: "",
  },
  {
    id: "node-components",
    anatomyId: anatomy.id,
    parentId: "node-src",
    nodeType: "directory",
    nameRule: {
      type: "exact",
      value: "components",
    },
    required: true,
    description: "组件目录",
    sortOrder: 0,
    createdAt: "",
    updatedAt: "",
  },
  {
    id: "node-component-file",
    anatomyId: anatomy.id,
    parentId: "node-components",
    nodeType: "file",
    nameRule: {
      type: "glob",
      value: "*.tsx",
    },
    required: false,
    description: "React 组件文件",
    sortOrder: 0,
    createdAt: "",
    updatedAt: "",
  },
  {
    id: "node-hooks",
    anatomyId: anatomy.id,
    parentId: "node-src",
    nodeType: "directory",
    nameRule: {
      type: "exact",
      value: "hooks",
    },
    required: false,
    description: "自定义 Hooks",
    sortOrder: 1,
    createdAt: "",
    updatedAt: "",
  },
  {
    id: "node-hook-file",
    anatomyId: anatomy.id,
    parentId: "node-hooks",
    nodeType: "file",
    nameRule: {
      type: "glob",
      value: "use*.ts",
    },
    required: false,
    description: "Hook 文件",
    sortOrder: 0,
    createdAt: "",
    updatedAt: "",
  },
  {
    id: "node-index",
    anatomyId: anatomy.id,
    parentId: "node-src",
    nodeType: "file",
    nameRule: {
      type: "exact",
      value: "index.ts",
    },
    required: true,
    description: "代码包导出入口",
    sortOrder: 2,
    createdAt: "",
    updatedAt: "",
  },
  {
    id: "node-readme",
    anatomyId: anatomy.id,
    parentId: null,
    nodeType: "file",
    nameRule: {
      type: "exact",
      value: "README.md",
    },
    required: false,
    description: "代码包说明文档",
    sortOrder: 1,
    createdAt: "",
    updatedAt: "",
  },
]
```

---

## 六、为什么持久化使用扁平结构

不建议直接将整个目录保存成嵌套 JSON：

```ts
{
  name: "src",
  children: [
    {
      name: "components",
      children: [],
    },
  ],
}
```

因为编辑时会遇到很多问题：

* 移动节点需要修改两棵子树。
* 查找节点需要递归。
* 删除节点需要递归查找。
* 很难单独更新一个节点。
* 数据库难以给单个节点建立约束。
* 多人编辑或增量保存困难。
* 排序和拖拽更新不方便。

使用 `parentId` 后，移动一个节点只需要改变：

```ts
{
  parentId: "new-parent-id",
  sortOrder: 2,
}
```

因此，**邻接表结构是这个需求当前阶段最合适的持久化模型**。

---

## 七、接口展示时转换成树

接口可以返回扁平节点，也可以由后端转换为树。

树节点 DTO 可以定义为：

```ts
interface AnatomyTreeNode {
  id: string
  nodeType: "directory" | "file"
  nameRule: NodeNameRule
  required: boolean
  description?: string
  sortOrder: number
  children: AnatomyTreeNode[]
}
```

转换方法：

```ts
function buildAnatomyTree(nodes: AnatomyNode[]): AnatomyTreeNode[] {
  const nodeMap = new Map<string, AnatomyTreeNode>()
  const roots: AnatomyTreeNode[] = []

  for (const node of nodes) {
    nodeMap.set(node.id, {
      id: node.id,
      nodeType: node.nodeType,
      nameRule: node.nameRule,
      required: node.required,
      description: node.description,
      sortOrder: node.sortOrder,
      children: [],
    })
  }

  for (const node of nodes) {
    const treeNode = nodeMap.get(node.id)

    if (!treeNode) {
      continue
    }

    if (node.parentId === null) {
      roots.push(treeNode)
      continue
    }

    const parent = nodeMap.get(node.parentId)

    if (parent) {
      parent.children.push(treeNode)
    }
  }

  const sortNodes = (treeNodes: AnatomyTreeNode[]): void => {
    treeNodes.sort((a, b) => a.sortOrder - b.sortOrder)

    for (const node of treeNodes) {
      sortNodes(node.children)
    }
  }

  sortNodes(roots)

  return roots
}
```

时间复杂度约为：

```text
O(n)
```

适合当前业务。

---

## 八、前端编辑器状态

前端做层级编辑、拖拽排序时，不建议直接频繁修改递归数组。

可以保存成标准化状态：

```ts
interface AnatomyEditorNode {
  id: string
  parentId: string | null

  nodeType: "directory" | "file"
  nameRule: NodeNameRule

  required: boolean
  description: string

  sortOrder: number
}

interface AnatomyEditorState {
  anatomy: {
    name: string
    description: string
  }

  nodesById: Record<string, AnatomyEditorNode>
}
```

例如：

```ts
const editorState: AnatomyEditorState = {
  anatomy: {
    name: "React Component Library",
    description: "React 组件库结构",
  },
  nodesById: {
    "node-src": {
      id: "node-src",
      parentId: null,
      nodeType: "directory",
      nameRule: {
        type: "exact",
        value: "src",
      },
      required: true,
      description: "源代码目录",
      sortOrder: 0,
    },
    "node-index": {
      id: "node-index",
      parentId: "node-src",
      nodeType: "file",
      nameRule: {
        type: "exact",
        value: "index.ts",
      },
      required: true,
      description: "导出入口",
      sortOrder: 0,
    },
  },
}
```

渲染时根据 `parentId` 分组：

```ts
function getChildren(
  nodesById: Record<string, AnatomyEditorNode>,
  parentId: string | null,
): AnatomyEditorNode[] {
  return Object.values(nodesById)
    .filter((node) => node.parentId === parentId)
    .sort((a, b) => a.sortOrder - b.sortOrder)
}
```

这里需要注意：

> `parentId + sortOrder` 应该是唯一的数据来源，不要同时让 `parentId` 和 `childrenIds` 都可以被修改。

否则容易出现：

```text
父节点说自己有某个子节点
但是子节点的 parentId 指向另一个目录
```

---

## 九、必须实现的业务校验

### 1. 文件节点不能有子节点

```ts
function canContainChildren(node: AnatomyNode): boolean {
  return node.nodeType === "directory"
}
```

添加或移动节点时：

```ts
if (parent.nodeType !== "directory") {
  throw new Error("Only directory nodes can contain child nodes")
}
```

---

### 2. 父节点必须属于同一个 Anatomy

必须保证：

```ts
parent.anatomyId === node.anatomyId
```

不允许把一个 Anatomy 的节点挂到另一个 Anatomy 下。

---

### 3. 禁止循环引用

例如禁止：

```text
A/
└── B/
    └── A/
```

移动目录前，需要判断目标父节点是否是当前目录的后代。

```ts
function isDescendant(
  nodes: AnatomyNode[],
  candidateParentId: string,
  nodeId: string,
): boolean {
  const nodeMap = new Map(nodes.map((node) => [node.id, node]))

  let currentId: string | null = candidateParentId

  while (currentId !== null) {
    if (currentId === nodeId) {
      return true
    }

    currentId = nodeMap.get(currentId)?.parentId ?? null
  }

  return false
}
```

---

### 4. 删除目录时检查子节点

```ts
function hasChildren(nodes: AnatomyNode[], nodeId: string): boolean {
  return nodes.some((node) => node.parentId === nodeId)
}
```

推荐交互：

```text
删除目录 “components”？

该目录包含 8 个子节点，删除后这些节点也会被删除。
```

用户必须明确确认。

后端仍然需要再次校验，不能只依赖前端确认框。

---

### 5. 名称不能为空

```ts
function validateNameRule(rule: NodeNameRule): boolean {
  return rule.value.trim().length > 0
}
```

---

### 6. 精确名称不能在同级重复

例如不能出现：

```text
src/
├── index.ts
└── index.ts
```

建议校验同一个 `parentId` 下：

```ts
node.nameRule.type === "exact"
```

的名称唯一。

对于 Glob 规则，第一阶段至少禁止完全相同的模式重复。模式之间是否重叠，可以先提示警告而不是强制阻止。

---

### 7. 顺序只在兄弟节点之间有效

`sortOrder` 的作用域是：

```text
anatomyId + parentId
```

推荐保存后重新整理为：

```text
0, 1, 2, 3...
```

如果预计拖拽操作特别频繁，也可以后续改成字符串排名字段，例如 LexoRank。但当前阶段普通整数已经足够。

---

## 十、Crate 与 Anatomy 的关系

目前需求看起来是：

> 一个 Crate 最多选择一个 Anatomy，一个 Anatomy 可以被多个 Crate 使用。

因此直接在 Crate 上保存外键即可：

```ts
interface Crate {
  id: string
  name: string

  anatomyId: string | null
}
```

不建议保存：

```ts
interface Crate {
  metadata: {
    anatomyTree: unknown
  }
}
```

也不建议把整棵 Anatomy 复制到 Crate 中。

接口数据可以是：

```ts
interface CrateDetail {
  id: string
  name: string

  anatomy: {
    id: string
    name: string
    description?: string
    status: AnatomyStatus
    tree: AnatomyTreeNode[]
  } | null
}
```

---

## 十一、归档和删除策略

为了满足：

> 删除或归档 Anatomy 时不得静默破坏现有 Crate 的阅读体验。

建议规则如下。

### 归档

归档后：

* 已关联的 Crate 仍然可以读取 Anatomy。
* Crate 详情正常显示目录结构。
* Anatomy 选择器默认不再展示该 Anatomy。
* 已经选择该 Anatomy 的 Crate 编辑页面需要继续显示它，并标注“已归档”。
* 用户可以将 Crate 改选为其他 Anatomy。

例如：

```text
React Component Library
已归档
```

### 删除

建议本阶段不提供普通硬删除。

如果 Anatomy 被 Crate 引用：

```text
无法删除该 Anatomy，因为它仍被 12 个 Crate 使用。
请先修改这些 Crate 的 Anatomy，或者归档该 Anatomy。
```

如果确实需要删除能力，只允许删除：

```text
没有任何 Crate 引用的 Anatomy
```

---

## 十二、Anatomy 修改后的语义

这里需要在产品层明确一个重要语义：

### 当前推荐：实时引用

Crate 引用 Anatomy：

```ts
crate.anatomyId = anatomy.id
```

Anatomy 修改后，所有引用它的 Crate 都显示最新结构。

这符合“可复用结构规范”的定位，也最适合当前阶段。

### 暂不推荐：结构快照

如果未来要求：

> Crate 必须保留选择 Anatomy 当时的历史版本。

那就需要引入：

```text
Anatomy
└── AnatomyVersion
    └── AnatomyNode
```

Crate 保存：

```ts
anatomyVersionId: string
```

而不是 `anatomyId`。

但当前 Issue 没有明确提出版本冻结，因此现在直接引用 Anatomy 更简单，不需要提前引入版本模型。

---

## 十三、推荐的接口形式

### 创建 Anatomy

```http
POST /anatomies
```

```json
{
  "name": "React Component Library",
  "description": "React 组件库标准结构"
}
```

### 批量保存结构节点

```http
PUT /anatomies/:anatomyId/nodes
```

```json
{
  "nodes": [
    {
      "id": "node-src",
      "parentId": null,
      "nodeType": "directory",
      "nameRule": {
        "type": "exact",
        "value": "src"
      },
      "required": true,
      "description": "源代码目录",
      "sortOrder": 0
    }
  ]
}
```

层级编辑器通常会发生移动、删除、排序等多个操作，第一阶段采用一次性批量保存，比为每个拖拽操作设计独立接口简单。

后端应在一个事务中：

1. 校验全部节点。
2. 校验父子关系。
3. 校验循环引用。
4. 校验排序。
5. 写入节点。
6. 删除本次提交中已不存在的旧节点。

---

## 十四、最终推荐模型

核心模型可以确定为：

```ts
interface Anatomy {
  id: string
  name: string
  description?: string
  status: "active" | "archived"
}

type NodeNameRule =
  | {
      type: "exact"
      value: string
    }
  | {
      type: "glob"
      value: string
    }

interface AnatomyNode {
  id: string
  anatomyId: string
  parentId: string | null

  nodeType: "directory" | "file"
  nameRule: NodeNameRule

  required: boolean
  description?: string

  sortOrder: number
}

interface Crate {
  id: string
  anatomyId: string | null
}
```

整体数据流是：

```text
数据库保存扁平节点
        ↓
接口读取 AnatomyNode[]
        ↓
转换为目录树
        ↓
前端递归展示

前端编辑标准化节点
        ↓
拖拽修改 parentId 和 sortOrder
        ↓
批量提交
        ↓
后端校验并保存
```

这套设计能够完整覆盖 T1～T4，并为以后增加扫描、匹配、版本管理保留扩展空间。
