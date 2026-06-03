# TypeScript 中 `is` 与 `as` 的区别

  

这两个关键字虽然都和类型相关，但用途完全不同。一句话概括：

  

> **`as`** **是"类型断言"——你告诉编译器"我知道它是什么类型"；****`is`** **是"类型谓词"——你告诉编译器"经过这个函数检查后，它是什么类型"。**

  

---

  

## 1. `as` — 类型断言（Type Assertion）

  

**作用**：手动告诉编译器"把这个值当作某个类型来处理"。编译器不会做任何运行时检查，纯粹是编译期的类型覆盖。

  

```TypeScript
const input: unknown = "hello world";

// 你断言 input 是 string，编译器就信你
const len = (input as string).length;
```

  

**典型场景**：

- 从 `unknown`、`any` 中取值时
    
- DOM 操作，如 `document.getElementById("app") as HTMLDivElement`
    
- 你比编译器更清楚实际类型时
    

**风险**：断言是"你说了算"，如果断言错误，运行时该崩还是会崩：

  

```TypeScript
const input: unknown = 42;
const len = (input as string).length; // 编译通过，运行时 undefined
```

  

---

  

## 2. `is` — 类型谓词（Type Predicate）

  

**作用**：用在函数返回值类型的位置，声明"如果这个函数返回 `true`，那么参数就是某个类型"。它是**类型守卫（Type Guard）** 的一种写法。

  

```TypeScript
function isString(value: unknown): value is string {
  return typeof value === "string";
}

const input: unknown = "hello world";

if (isString(input)) {
  // 进入这个分支后，TypeScript 自动把 input 收窄为 string
  console.log(input.toUpperCase()); // ✅ 安全，无需 as
}
```

  

**典型场景**：

- 封装自定义类型守卫函数
    
- 联合类型的分支判断
    
- 复杂对象的类型区分
    

```TypeScript
interface Cat { meow(): void }
interface Dog { bark(): void }

function isCat(animal: Cat | Dog): animal is Cat {
  return (animal as Cat).meow !== undefined;
}

function handleAnimal(animal: Cat | Dog) {
  if (isCat(animal)) {
    animal.meow();   // ✅ 编译器知道这里是 Cat
  } else {
    animal.bark();   // ✅ 编译器知道这里是 Dog
  }
}
```

 
## 3. 核心对比

|   |   |   |
|---|---|---|
|维度|`as`（类型断言）|`is`（类型谓词）|
|**本质**|你**强制告诉**编译器类型|你通过函数**证明**给编译器看|
|**位置**|表达式中：`value as Type`|函数返回类型处：`param is Type`|
|**运行时检查**|**无**，纯编译期|**有**，函数体内包含实际判断逻辑|
|**安全性**|低——断言错了运行时出错|高——有真实的检查逻辑兜底|
|**类型收窄**|不收窄，仅当前表达式生效|收窄——`if` 分支内自动缩小类型|
|**典型用法**|快速转型、DOM 操作|封装类型守卫、联合类型判断|
