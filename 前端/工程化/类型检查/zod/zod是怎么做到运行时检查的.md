# zod是怎么做到运行时检查的
> Last Format Time：8/13/2026 15:14:03

关键点是：

> **Zod 并不是把 TypeScript 的 `type` 保留到运行时，而是先创建一个真实存在的 JavaScript Schema，再从 Schema 推导出 TypeScript 类型。**

---
## 普通 TypeScript 类型为什么不能运行时校验
```ts
type User = {
  name: string;
  age: number;
};
```

这里的 `User` 只提供给 TypeScript 编译器检查。编译成 JavaScript 后，`type User` 会被完全删除，所以运行时根本找不到它。([TypeScript][1])

例如：

```ts
type User = {
  name: string;
};

const data = JSON.parse(responseText) as User;
```

编译后大致只剩：

```js
const data = JSON.parse(responseText);
```

`as User` 也会被删除，它只是告诉编译器“相信我，这是 User”，并没有真正检查数据。

即使接口返回：

```json
{
  "name": 123
}
```

TypeScript 在运行时也不会报错。

---
## Zod Schema 是一个真实的 JavaScript 值
```ts
import { z } from "zod";

const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
});
```

这里的 `UserSchema` 不是 TypeScript 类型，而是一个真实的 JavaScript 对象。

可以粗略地把它理解成：

```ts
const UserSchema = {
  fields: {
    name: {
      check(value) {
        return typeof value === "string";
      },
    },
    age: {
      check(value) {
        return typeof value === "number";
      },
    },
  },

  parse(input) {
    // 遍历字段并进行检查
  },
};
```

真实的 Zod 实现当然复杂得多，但原理类似：Schema 中保存了字段结构、校验规则、错误信息以及解析方法，因此编译后它仍然存在。

```ts
UserSchema.parse({
  name: "Dano",
  age: 20,
});
```

运行时，Zod 会按照 Schema 检查输入。验证成功时返回解析后的数据，失败时 `.parse()` 会抛出 `ZodError`。([Zod][2])

---
## Zod 的关键方向：从 Schema 推导 type
Zod 推荐这样写：

```ts
const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
});

type User = z.infer<typeof UserSchema>;
```

推导出来相当于：

```ts
type User = {
  name: string;
  age: number;
};
```

这里存在两个不同的东西：

```ts
UserSchema // 运行时存在的值
User       // 仅编译期间存在的类型
```

也就是：

```text
Zod Schema
    │
    ├── 运行时：用于 parse 和校验数据
    │
    └── 编译时：通过 z.infer 推导 TypeScript 类型
```

Zod 官方将其描述为“TypeScript-first schema validation with static type inference”。([Zod][3])

---
## 完整例子
假设接口数据是不可信的：

```ts
const result: unknown = await fetch("/api/user").then((res) =>
  res.json(),
);
```

为什么应该先写成 `unknown`？

因为在校验之前，你不知道接口实际返回了什么。

定义 Schema：

```ts
import { z } from "zod";

const UserSchema = z.object({
  name: z.string(),
  age: z.number().int().nonnegative(),
});

type User = z.infer<typeof UserSchema>;
```

进行校验：

```ts
const user: User = UserSchema.parse(result);

console.log(user.name);
```

如果数据是：

```ts
{
  name: "Dano",
  age: 22,
}
```

校验成功。

如果数据是：

```ts
{
  name: "Dano",
  age: "22",
}
```

校验失败，因为 `"22"` 是字符串，不是数字。

---
## `safeParse` 不会抛异常
如果你不想使用 `try...catch`，可以使用：

```ts
const result = UserSchema.safeParse(data);

if (result.success) {
  console.log(result.data);
} else {
  console.log(result.error);
}
```

此时 `result` 是一个可辨识联合类型：

```ts
if (result.success) {
  // result.data 已经被推导为 User
  result.data.name;
} else {
  // result.error 是 ZodError
  console.log(result.error);
}
```

Zod 官方文档说明，`safeParse()` 会返回成功结果或包含 `ZodError` 的失败结果，而不是直接抛出异常。([Zod][2])

---
## 与手写类型守卫的关系
实际上你也可以不使用 Zod，自己写运行时检查：

```ts
type User = {
  name: string;
  age: number;
};

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const user = value as Record<string, unknown>;

  return (
    typeof user.name === "string" &&
    typeof user.age === "number"
  );
}
```

使用：

```ts
if (isUser(data)) {
  // 此处 data 被 TypeScript 推导成 User
  console.log(data.name);
}
```

Zod本质上帮助你系统化地完成这些事情：

```ts
const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
});
```

它同时提供嵌套对象、数组、联合类型、可选字段、自定义校验、错误信息和类型推导，避免手写大量类型守卫。

---
## 最核心的区别
```ts
// 只有编译时类型，运行时被删除
type User = {
  name: string;
};
```

```ts
// 真实的运行时 JavaScript 值
const UserSchema = z.object({
  name: z.string(),
});

// 根据运行时 Schema 推导编译时类型
type User = z.infer<typeof UserSchema>;
```

所以准确地说，**Zod 不是在运行时检查 TypeScript 类型，而是在运行时检查 Zod Schema，并让 TypeScript 类型与 Schema 自动保持一致。**

[1]: https://www.typescriptlang.org/docs/handbook/2/basic-types.html?utm_source=chatgpt.com "TypeScript: Documentation - The Basics"
[2]: https://zod.dev/basics?utm_source=chatgpt.com "Basic usage | Zod"
[3]: https://zod.dev/?utm_source=chatgpt.com "Intro | Zod"
