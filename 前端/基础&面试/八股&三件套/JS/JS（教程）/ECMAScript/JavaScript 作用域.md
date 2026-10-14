# JavaScript 作用域
> Last Format Time：8/13/2026 15:14:02

---
## 什么是作用域
**作用域（Scope）决定一个变量在哪些位置可以被访问。**

```js
const a = 10;

function test() {
  const b = 20;

  console.log(a); // ✅
  console.log(b); // ✅
}

console.log(a); // ✅
console.log(b); // ❌ ReferenceError
```

这里：

```text
全局作用域
├── a
└── test 函数作用域
    └── b
```

核心规则：

> **内层作用域可以访问外层变量，但外层作用域不能访问内层变量。**


# 2. JavaScript 中的主要作用域

主要有三种：

```text
全局作用域 Global Scope
函数作用域 Function Scope
块级作用域 Block Scope
```

---
## 全局作用域
定义在最外层的变量属于全局作用域。

```js
const name = "Dano";

function hello() {
  console.log(name); // ✅
}
```

`hello` 位于更内层，因此可以访问外层的 `name`。

---
## 函数作用域
函数内部声明的变量，只能在该函数及其内部作用域中访问。

```js
function outer() {
  const a = 10;

  function inner() {
    const b = 20;

    console.log(a); // ✅
    console.log(b); // ✅
  }

  console.log(a); // ✅
  console.log(b); // ❌
}
```

结构：

```text
Global
└── outer
    ├── a
    └── inner
        └── b
```

---
## 块级作用域
`{}` 可以形成块级作用域，例如：

```js
if (true) {
  const a = 10;
  let b = 20;
}

console.log(a); // ❌
console.log(b); // ❌
```

常见块包括：

```js
if (...) {
}

for (...) {
}

while (...) {
}

{
}
```

`let` 和 `const` 都具有块级作用域。

例如：

```js
for (let i = 0; i < 3; i++) {
  console.log(i);
}

console.log(i); // ❌
```


# 3. `var`、`let`、`const` 与作用域

这是作用域中非常重要的一部分。

| 声明方式    | 函数作用域 | 块级作用域 |
| ------- | ----: | ----: |
| `var`   |     ✅ |     ❌ |
| `let`   |     ✅ |     ✅ |
| `const` |     ✅ |     ✅ |

例如：

```js
if (true) {
  var a = 10;
}

console.log(a); // ✅ 10
```

`var` 不受普通 `{}` 限制。

但它受函数限制：

```js
function test() {
  if (true) {
    var a = 10;
  }

  console.log(a); // ✅
}

console.log(a); // ❌
```

所以可以理解为：

```text
var
→ 函数级作用域

let / const
→ 块级作用域
```

现代 JavaScript 中通常优先使用 `const` 和 `let`。


# 4. 作用域链 Scope Chain

当 JavaScript 使用一个变量时，会从**当前作用域开始向外查找**。

```js
const a = 1;

function foo() {
  const b = 2;

  function bar() {
    const c = 3;

    console.log(a);
    console.log(b);
    console.log(c);
  }

  bar();
}
```

作用域结构：

```text
Global
└── foo
    └── bar
```

查找 `b`：

```text
bar
↓
没有 b

foo
↓
找到 b
```

查找 `a`：

```text
bar
↓
foo
↓
Global
↓
找到 a
```

这条查找路径就是：

> **作用域链**

规则可以概括为：

```text
当前作用域
↓
父作用域
↓
父作用域
↓
...
↓
全局作用域
```

如果最终都没有找到：

```js
console.log(x);
```

就会产生：

```text
ReferenceError
```


# 5. 变量遮蔽 Variable Shadowing

如果内层和外层存在同名变量，JavaScript 会优先使用离当前作用域最近的变量。

```js
const a = 10;

function test() {
  const a = 20;

  console.log(a);
}

test();
```

输出：

```text
20
```

因为查找过程是：

```text
test
├── a = 20 ← 找到，停止查找
│
└── Global
    └── a = 10
```

这种现象叫：

> **变量遮蔽（Variable Shadowing）**

例如：

```js
const a = 1;

function foo() {
  const a = 2;

  function bar() {
    const a = 3;

    console.log(a);
  }

  bar();
}
```

结果：

```text
3
```

因为变量查找遵循：

> **就近原则。**


# 6. 词法作用域 Lexical Scope

JavaScript 使用的是：

> **词法作用域。**

它的核心含义是：

> 一个函数能够访问哪些变量，由这个函数**定义在哪里**决定，而不是由它**在哪里调用**决定。

例如：

```js
const name = "global";

function foo() {
  console.log(name);
}

function bar() {
  const name = "bar";

  foo();
}

bar();
```

结果是：

```text
global
```

而不是：

```text
bar
```

原因是 `foo` 定义在全局作用域：

```text
Global
├── name = "global"
├── foo
└── bar
    └── name = "bar"
```

所以 `foo` 中查找 `name` 时：

```text
foo
↓
Global
↓
name = "global"
```

它不会因为：

```js
foo();
```

是在 `bar` 中调用，就去访问 `bar` 的变量。

所以判断函数作用域时，要看：

```text
函数写在哪里
```

而不是：

```text
函数在哪里被调用
```


# 7. 词法作用域与闭包

词法作用域也是闭包产生的基础。

```js
function outer() {
  const count = 10;

  function inner() {
    console.log(count);
  }

  return inner;
}

const fn = outer();

fn(); // 10
```

看起来：

```js
outer();
```

已经执行结束了，但 `fn()` 仍然可以访问：

```js
count
```

原因是 `inner` 定义在 `outer` 中：

```text
Global
└── outer
    ├── count
    └── inner
```

根据词法作用域：

```text
inner
↓
outer
↓
Global
```

所以 `inner` 天然可以访问 `outer` 中的 `count`。

即使：

```js
inner
```

被返回到了外面，它仍然保留对这个外层作用域的访问能力。

这就是：

> **闭包 Closure**

所以可以先把闭包理解为：

> **函数记住了自己定义时所在的外层作用域。**


# 8. 推荐的作用域心智模型

例如：

```js
const a = 1;

function foo() {
  const b = 2;

  if (true) {
    const c = 3;

    console.log(a, b, c);
  }
}
```

可以想象成一层层房间：

```text
┌──────── Global ────────┐
│ a = 1                  │
│                        │
│  ┌──── foo ─────────┐  │
│  │ b = 2            │  │
│  │                  │  │
│  │ ┌── if ────────┐ │  │
│  │ │ c = 3        │ │  │
│  │ └──────────────┘ │  │
│  └──────────────────┘  │
└────────────────────────┘
```

在最里面：

```text
if
```

可以向外访问：

```text
c
b
a
```

查找方向：

```text
if
↓
foo
↓
Global
```

但在 `foo` 中不能访问 `c`，因为变量查找不会进入子作用域。

因此可以记成一句话：

> **作用域只能往外找，不能往里找。**


# 9. 整体关系

这些概念实际上是一条知识链：

```text
作用域 Scope
    │
    ├── 全局作用域
    ├── 函数作用域
    └── 块级作用域
            │
            ↓
       let / const / var

变量访问
    │
    ↓
作用域链 Scope Chain
    │
    ↓
从当前作用域向外查找
    │
    ↓
变量遮蔽 Shadowing

函数作用域关系
    │
    ↓
词法作用域 Lexical Scope
    │
    ↓
由“定义位置”决定
    │
    ↓
闭包 Closure
```

---
## 最终记住 6 条
1. **作用域决定变量在哪里可以访问。**
2. **内层可以访问外层，外层不能访问内层。**
3. **变量查找从当前作用域逐层向外进行，这叫作用域链。**
4. **同名变量优先使用最近的那个，这叫变量遮蔽。**
5. **`let`、`const` 有块级作用域，`var` 没有块级作用域。**
6. **JavaScript 是词法作用域：函数能访问谁，由定义位置决定，而不是调用位置决定。**

把这 6 条掌握之后，后面理解 **闭包、回调函数、React Hooks 中的闭包问题**都会容易很多。
