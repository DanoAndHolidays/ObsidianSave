# any、unknown 和 never 💡
> Last Format Time：10/8/2026 23:35:46

在 TypeScript 中，`any`、`unknown` 和 `never` 都是比较特殊的类型。

- `any`：任意类型，不进行类型检查。
- `unknown`：任意类型，但使用前必须确认类型。
- `never`：不可能存在的值，表示永远不会出现的类型。

---
## any：放弃类型检查
`any` 相当于告诉 TypeScript：这个变量是什么类型都无所谓，不需要检查

```ts
let value: any = 10;

value = "hello";
value = true;
value = { name: "Tom" };

// TS 不会报错
value.toUpperCase();
value.foo.bar();
value();
```

TypeScript 不会阻止这些操作，但运行时可能报错。

需要注意：`any` 不仅可以接收任意类型的值，也可以赋值给几乎所有其他类型。

```ts
let a: any = "hello";

let b: number = a; // ✅ 编译通过
let c: boolean = a; // ✅ 编译通过
```

这也是 `any` 危险的原因：它会绕过类型系统的保护。


---
## unknown：类型安全的 any
`unknown` 同样可以接收任意类型的值，但区别在于：

在没有确定具体类型之前，不能直接对它执行依赖具体类型的操作

```ts
let value: unknown = "hello";

value = 100;
value = true;

// ❌ 编译报错
value.toUpperCase();
```

必须先进行类型收窄：
```ts
let value: unknown = "hello";

if (typeof value === "string") {
  console.log(value.toUpperCase()); // ✅
}
```

赋值方向上也有区别：
```ts
let a: unknown = "hello";

let b: unknown = a; // ✅
let c: any = a;     // ✅
let d: string = a;  // ❌
```

因为 TypeScript 无法保证 `a` 一定是字符串。

### 处理不可信数据
比如你从外部获取一份数据：
```ts
function handleData(data: unknown) {
  if (
    typeof data === "object" &&
    data !== null &&
    "name" in data &&
    typeof data.name === "string"
  ) {
    console.log(data.name.toUpperCase());
  }
}
```

这里使用 `unknown`，可以强制开发者在操作数据前进行必要的类型检查。

---
## never：永远不可能出现的类型
`never` 表示一个值永远不可能存在,比较常见的场景有两个

### 函数不可能正常返回
```text
function throwError(): never {
  throw new Error("出错了");
}
```

这个函数不会正常返回任何值，因为它一定会抛出异常。

注意 `never` 和 `void` 的区别：
```ts
function foo(): void {
  console.log("hello");
}

function bar(): never {
  throw new Error("error");
}
```

- `void`：函数可以正常执行结束，只是不提供有意义的返回值。
- `never`：函数不可能正常执行结束。

### 穷尽性检查
这是 `never` 在实际项目中很有价值的用途

```ts
type Status = "success" | "error";

function handleStatus(status: Status) {
  switch (status) {
    case "success":
      return "成功";

    case "error":
      return "失败";

    default:
      const check: never = status;
      return check;
  }
}
```

因为 `success` 和 `error` 已经被处理完了，所以 `default` 中的 `status` 会被收窄成 `never`。

如果以后增加一种状态：
```ts
type Status = "success" | "error" | "loading";
```

那么：
```ts
const check: never = status; // ❌ 报错
```

TypeScript 会提醒你：还有 `loading` 没有处理。

这可以防止添加新业务状态后忘记修改对应逻辑。

---
## 三个类型的区别
|对比|`any`|`unknown`|`never`|
|---|---|---|---|
|核心含义|不检查类型|类型未知|不可能有值|
|能接收任意类型|✅|✅|❌|
|能直接调用方法|✅|❌|不适用|
|能赋值给 `string`|✅|❌|✅|
|类型安全性|低|高|高|
|常见用途|兼容旧代码|外部未知数据|穷尽检查、不可达代码|

有一个需要特别注意的地方：

`never` 可以赋值给任何类型，但普通类型不能赋值给 `never`

```ts
declare const n: never;

const a: string = n;  // ✅
const b: number = n;  // ✅

const c: never = "hi"; // ❌
```

这是因为 `never` 表示空的值集合。

---
## 从类型集合的角度理解
可以把 TypeScript 的类型看作一个集合：
![[Pasted image 20261008233334.png]]

概念示意：unknown 是安全的顶层类型，never 是底层类型；any 的赋值规则特殊，不完全遵循普通集合关系。

- `unknown`：顶层类型，包含所有可能的值。
- `never`：底层类型，不包含任何值。
- `any`：特殊的逃生类型，会绕过正常的类型检查规则。

因此：
```ts
type A = string | never;   // string
type B = string | unknown; // unknown
type C = string | any;     // any
```

在联合类型中，`never` 可以被消去，`unknown` 会吸收其他类型，而 `any` 则具有特殊的吸收行为。
