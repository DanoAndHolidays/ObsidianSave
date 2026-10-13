# as const
> Last Format Time：10/13/2026 19:28:09

*学舒服了，好清爽*

`as const` 是 TypeScript 的==常量断言==：它让字面量保留最精确的类型，同时把对象属性和数组元素标记为编译期只读

配合 `typeof`、`keyof` 和索引访问类型，可以从一个运行时常量对象自动推导出联合类型。

在前端项目中，我们经常需要同时拥有：

- 一个运行时可以使用的常量对象，例如 `ServiceErrorType.notFound`；
- 一组精确的类型约束，例如 `"not_found" | "invalid_input"`；
- 自动补全、禁止拼写错误，以及新增常量后类型自动同步。

`as const` + `typeof` + `keyof` 正好可以把这几件事组合起来。

因此，它经常被用来替代一部分字符串 `enum`。

---
## 类型拓宽
Java 更偏向于描述「这个对象属于什么类型」，而 TypeScript 更擅长描述「这个值满足什么约束」

| 对比    | Java                    | TypeScript                 |     |
| ----- | ----------------------- | -------------------------- | --- |
| 类型兼容  | 主要是名义类型（Nominal Typing） | 主要是结构类型（Structural Typing） |     |
| 类型粒度  | 通常是类、接口、基本类型            | 可以精确到某个具体值                 |     |
| 字面量类型 | 不支持 TS 式字面量类型           | `"SUCCESS"`、`200`、`true`   |     |
| 联合类型  | 不直接支持通用联合类型             | 支持                         |     |
| 类型运算  | 相对有限                    | 联合、交叉、条件、映射类型              |     |
| 泛型    | 主要约束类型参数                | 还能进行复杂的类型计算                |     |
| 运行时   | Java 类型信息部分保留           | TS 类型主要在编译后擦除              |     |

ts 可以精确到某个具体值，然后这个值就是一种类型了
![[Pasted image 20261013211623.png]]

用集合的角度理解：

- `A`：所有可能的字符串
- `B`：只有 `"SUCCESS"` 这一个值，那么他其实就是一种类型了
- `C`：只有 `"SUCCESS"` 和 `"FAILED"` 两个值

### 基本类型的推断
TypeScript 会根据变量是否允许重新赋值，决定是否保留字面量类型（字面量是代码中直接写出的固定值，例如 `"hello"`、`123`、`true`）
```ts
const a = "SUCCESS"; // "SUCCESS"
let b = "SUCCESS";   // string

const c = 100;       // 100
let d = 100;         // number

const e = true;      // true
let f = true;        // boolean

const g = 100n;      // 100n
let h = 100n;        // bigint
```

原因是：

- `const` 变量不能重新绑定到另一个值，所以 TypeScript 可以保留==更精确==的字面量类型
- `let` 变量可以重新赋值，因此 TypeScript 通常会把==类型拓宽==为 `string`

类型拓宽并不是单纯由 `const` 或 `let` 决定的，还受上下文、显式类型注解等因素影响

例如，即便使用 `let`，也可以显式指定字面量类型：
```ts
let status: "SUCCESS" = "SUCCESS";

status = "FAILED"; // ❌
```

字面量类型是普通类型的子类型：
```ts
let status: "SUCCESS" = "SUCCESS";

status = "FAILED";
// ❌ 类型错误："FAILED" 不能赋值给 "SUCCESS"
```

即使变量使用 `const`，显式类型也可以让它变宽：
```ts
const c: string = "SUCCESS";
// 推断类型：string
```

### `const` 对象的属性会被拓宽
```ts
const obj = {
  status: "SUCCESS",
};
```

此时 `obj` 的类型通常是：
```ts
{
  status: string;
}
```

因为 `const` 只限制变量绑定本身，不能阻止对象内部属性修改：
```ts
obj.status = "FAILED"; // ✅ 允许
// obj = {};           // ❌ 不允许重新绑定 obj
```

---
## `as const` 的三个核心作用
### 保留字面量类型
```ts
const Status = {
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;
```

不加 `as const` 时，属性值通常是 `string`；加上之后，属性值会保留为精确的字面量：
```ts
{
  readonly Success: "SUCCESS";
  readonly Failed: "FAILED";
}
```

这里发生了两个变化：

- 属性值从 `string` 收窄为 `"SUCCESS"` 和 `"FAILED"`；
- 对象属性变成了 `readonly`。

### 对象属性变成编译期只读
```ts
Status.Success = "OTHER";
// ❌ 无法分配给只读属性
```

这里的“只读”只存在于 TypeScript 类型检查阶段。`as const` 不会在运行时冻结对象；如果确实需要运行时不可修改，应考虑 `Object.freeze()`。

### 数组变成只读元组
```ts
const frameworks = ["React", "Vue"] as const;
// 推断类型：readonly ["React", "Vue"]

frameworks.push("Angular");
// ❌ 不存在 push 方法

frameworks[0] = "Angular";
// ❌ 无法修改只读元素
```

普通数组通常会被推断为 `string[]`，而 `as const` 会保留每个位置上的具体字面量和元组长度。

---
## 使用 `as const` 替代字符串 `enum`
### 传统 `enum`
```ts
enum Status {
  Pending = "PENDING",
  Success = "SUCCESS",
  Failed = "FAILED",
}
```

调用时可以使用：
```ts
Status.Pending;
Status.Success;
Status.Failed;
```

### 改写为常量对象
```ts
const Status = {
  Pending: "PENDING",
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;
```

调用方式几乎不变：
```ts
Status.Pending; // "PENDING"
Status.Success; // "SUCCESS"
Status.Failed;  // "FAILED"
```

但普通对象与 `enum` 有一个重要差异：

- `enum` 的名字既可以作为运行时值使用，也可以直接作为类型使用
- 普通对象默认只能作为运行时值使用，需要额外推导

---
## `typeof` + `keyof` + 索引访问类型
这是 `as const` 替代 `enum` 时最需要掌握的部分。

### 用 `typeof` 获取对象类型
```ts
const Status = {
  Pending: "PENDING",
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;

type StatusMap = typeof Status;
```

得到：
```ts
type StatusMap = {
  readonly Pending: "PENDING";
  readonly Success: "SUCCESS";
  readonly Failed: "FAILED";
};
```

这里的 `typeof` 是 TypeScript 的**类型查询操作符**，不是运行时 JavaScript 中的 `typeof` 表达式。

### 用 `keyof` 获取所有键
```ts
type StatusKey = keyof typeof Status;
```

等价于：
```ts
type StatusKey = "Pending" | "Success" | "Failed";
```

### 用索引访问类型获取所有值
```ts
type StatusValue = (typeof Status)[keyof typeof Status];
```

可以拆成更容易理解的写法：
```ts
type StatusMap = typeof Status;
type StatusKey = keyof StatusMap;
type StatusValue = StatusMap[StatusKey];
```

最终得到：
```ts
type StatusValue = "PENDING" | "SUCCESS" | "FAILED";
```

也就是说：

- `typeof Status`：拿到对象的类型；
- `keyof typeof Status`：拿到对象所有键的联合类型；
- `StatusMap[StatusKey]`：拿到这些键对应的值的联合类型。

---
## 推荐模板
```ts
export const Status = {
  Pending: "PENDING",
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;

export type Status = (typeof Status)[keyof typeof Status];
```

TypeScript 允许同名的 `const` 和类型别名共存，因为它们属于不同的声明空间
```ts
function updateStatus(status: Status) {
  console.log(status);
}

updateStatus(Status.Success); // ✅ 使用常量值
updateStatus("SUCCESS");     // ✅ 使用合法字面量
updateStatus("UNKNOWN");     // ❌ 不合法
```

这个模板同时提供了：

- `Status.Success` 这样的运行时常量访问能力；
- `"PENDING" | "SUCCESS" | "FAILED"` 的联合类型约束；
- 编译期只读检查；
- 类型与常量的单点维护。

---
## 为什么它常被用来替代 `enum`
### 更贴近原生 JavaScript
普通 `enum` 不是原生 JavaScript 的对象声明语法，TypeScript 通常需要生成额外的初始化代码
```ts
enum Status {
  Success = "SUCCESS",
  Failed = "FAILED",
}
```

而下面的代码本质上就是普通 JavaScript 对象：
```ts
const Status = {
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;
```

去掉类型断言后，运行时仍然是：
```ts
const Status = {
  Success: "SUCCESS",
  Failed: "FAILED",
};
```

因此，`as const` 不会让运行时对象消失，但通常不会像 `enum` 一样额外生成枚举初始化包装

### 避免数字枚举的反向映射
数字枚举：
```ts
enum Direction {
  Up,
  Down,
}
```

运行时对象通常同时包含正向和反向映射：
```ts
{
  "0": "Up",
  "1": "Down",
  Up: 0,
  Down: 1,
}
```

如果只需要“名称 → 数值”，普通对象更直接：
```ts
const Direction = {
  Up: 0,
  Down: 1,
} as const;
```

运行时只需要：
```ts
{
  Up: 0,
  Down: 1,
}
```

### 更容易遍历
数字枚举的反向映射会影响遍历结果：
```ts
enum Direction {
  Up,
  Down,
}

console.log(Object.values(Direction));
// ["Up", "Down", 0, 1]
```

使用 `as const` 对象时，遍历结果更符合直觉：
```ts
const Direction = {
  Up: 0,
  Down: 1,
} as const;

console.log(Object.values(Direction));
// [0, 1]
```

在 React 中生成选项也很方便：
```tsx
const Status = {
  Pending: "PENDING",
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;

return (
  <select>
    {Object.values(Status).map((status) => (
      <option key={status} value={status}>
        {status}
      </option>
    ))}
  </select>
);
```

### 更容易组合和扩展
普通对象可以直接使用展开语法：
```ts
const BaseStatus = {
  Pending: "PENDING",
  Success: "SUCCESS",
} as const;

const ExtendedStatus = {
  ...BaseStatus,
  Failed: "FAILED",
  Cancelled: "CANCELLED",
} as const;
```

也可以组合多组常量：
```ts
const HttpCode = {
  OK: 200,
  NOT_FOUND: 404,
} as const;

const BusinessCode = {
  USER_NOT_FOUND: 1001,
  TOKEN_EXPIRED: 1002,
} as const;

const Code = {
  ...HttpCode,
  ...BusinessCode,
} as const;
```

---
## `as const` 与 `enum` 的差异
| 对比项 | `enum` | `as const` 对象 |
| --- | --- | --- |
| 字符串值映射 | 支持 | 支持 |
| 自动递增数字值 | 支持 | 不支持，需要手动填写 |
| 数字反向映射 | 自动生成 | 不会自动生成 |
| 类型声明 | 可以直接使用枚举名 | 需要用 `typeof` 等方式推导 |
| 运行时形式 | 枚举对象及初始化逻辑 | 普通 JavaScript 对象 |
| 遍历 | 数字枚举需要过滤反向映射 | 通常更直观 |
| 组合与扩展 | 不适合对象展开式组合 | 支持对象展开和组合 |
| 运行时值 | 有 | 有 |

这并不意味着 `as const` 在所有场景都优于 `enum`。如果确实需要数字自动递增、已有枚举契约或特定枚举行为，`enum` 仍然有价值。

## 实际项目示例：`ServiceErrorType`
最初的问题来自项目文件：
```text
packages/services/src/archetypes-service.ts
```

在文件靠前的位置看到了类似代码：
```ts
const ServiceErrorType = {
  notFound: "not_found",
  invalidInput: "invalid_input",
} as const;
```

后面又出现了：
```ts
type ServiceErrorTypeValue =
  (typeof ServiceErrorType)[keyof typeof ServiceErrorType];
```

因此，问题不只是“`as const` 是什么”，还包括：

1. 为什么这里不能只写普通 `const`？
2. 为什么要再写 `typeof` 和 `keyof`？
3. 这个对象如何同时服务于运行时判断和类型检查？

### 先去掉 `as const` 对比
如果写成：
```ts
const ServiceErrorType = {
  notFound: "not_found",
  invalidInput: "invalid_input",
};
```

TypeScript 通常会推断为：
```ts
{
  notFound: string;
  invalidInput: string;
}
```

此时值类型已经丢失了具体信息，后续无法稳定地推导出：
```ts
"not_found" | "invalid_input"
```

### 加回 `as const`
```ts
const ServiceErrorType = {
  notFound: "not_found",
  invalidInput: "invalid_input",
} as const;
```

此时类型变为：
```ts
{
  readonly notFound: "not_found";
  readonly invalidInput: "invalid_input";
}
```

于是：
```ts
type ServiceErrorTypeValue =
  (typeof ServiceErrorType)[keyof typeof ServiceErrorType];

// "not_found" | "invalid_input"
```

### 继续追踪运行时用法
这个对象不只是用来产生类型，也可以直接参与业务逻辑：
```ts
function isNotFoundError(type: ServiceErrorTypeValue) {
  return type === ServiceErrorType.notFound;
}

if (error.type === ServiceErrorType.notFound) {
  // 运行时判断错误类型
}

throw {
  type: ServiceErrorType.invalidInput,
  message: "请求参数不合法",
};
```

这就是项目采用该模式的原因：同一份对象同时承担了“运行时常量”和“类型来源”两种职责。

### 直接写联合类型当然也可以
如果完全不需要运行时访问 `ServiceErrorType.notFound`，可以直接写：
```ts
type ServiceErrorType = "not_found" | "invalid_input";
```

但一旦需要运行时值，就还要额外定义对象：
```ts
type ServiceErrorType = "not_found" | "invalid_input";

const ServiceErrorType = {
  notFound: "not_found",
  invalidInput: "invalid_input",
};
```

这会造成值和类型的==重复维护==

`as const` 模式只定义一次对象，再从对象自动推导类型

### 这个项目写法的收益

- **同时拥有运行时值和类型**：可以进行错误类型比较，也可以约束函数参数；
- **避免重复定义**：新增属性后，联合类型自动同步；
- **类型安全与自动补全**：使用 `ServiceErrorType.notFound` 比手写字符串更不容易出错；
- **便于扩展**：新增 `databaseError` 后，推导出来的值联合类型会自动包含它。

```ts
const ServiceErrorType = {
  notFound: "not_found",
  invalidInput: "invalid_input",
  databaseError: "database_error",
} as const;

// 自动包含 "database_error"
type ServiceErrorTypeValue =
  (typeof ServiceErrorType)[keyof typeof ServiceErrorType];
```

---
## 使用哪一种

| 场景 | 推荐写法 |
| --- | --- |
| 只需要类型，不需要运行时值 | 直接使用联合类型 |
| 需要运行时常量和类型约束 | `as const` + `typeof` + `keyof` |
| 需要数字自动递增 | `enum` |
| 需要数字枚举反向映射 | `enum`，并注意遍历结果 |
| 需要对象展开、组合、遍历 | `as const` 对象 |
| 需要公共库跨工具链发布 | 优先评估联合类型或 `as const`，谨慎暴露 `const enum` |

示例：只需要类型时，直接写联合类型就足够：
```ts
type Status = "PENDING" | "SUCCESS" | "FAILED";
```

需要同时访问 `Status.Success` 时，再使用对象模式：
```ts
const Status = {
  Pending: "PENDING",
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;

type Status = (typeof Status)[keyof typeof Status];
```

---
## 最后总结

- `const`：限制变量绑定不能重新赋值；
- 字面量类型：比 `string`、`number` 更精确的类型；
- 类型拓宽：把 `"SUCCESS"` 等精确类型推断为 `string` 等宽泛类型；
- `as const`：保留字面量类型，并提供编译期只读约束；
- `typeof`：从值获取类型；
- `keyof`：从对象类型获取键的联合类型；
- `T[K]`：从对象类型中获取指定键对应的值类型。

### 模板
```ts
const Status = {
  Pending: "PENDING",
  Success: "SUCCESS",
  Failed: "FAILED",
} as const;

// "Pending" | "Success" | "Failed"
type StatusKey = keyof typeof Status;

// "PENDING" | "SUCCESS" | "FAILED"
type StatusValue = (typeof Status)[keyof typeof Status];
```

最终可以这样判断：

> 需要运行时常量和类型约束时，优先考虑 `as const` 对象；只需要类型时直接使用联合类型；需要数字自动递增或特定枚举行为时，再考虑 `enum`。

官方参考： [TypeScript Handbook — Enums](https://www.typescriptlang.org/docs/handbook/enums.html)

