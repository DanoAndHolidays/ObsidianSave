### const
---
所声明的变量的==指针==所指向的==内存地址是固定的==，所以对于数值，布尔值，和字符串来说，就是其本身。但是对于复合的数据类型，其只能保证指针是不变的，指针所指向的内容不能保证不变，所以可以修改由const声明的数组和对象的值
```javascript
//使用Object.freeze方法来声明，对象和对象的属性将同时不能被修改。
const object =Object.freeeze({});
```

### 顶层对象
---
window或者global
`var`命令和`function`命令声明的全局变量，依旧是顶层对象的属性；另一方面规定，`let`命令、`const`命令、`class`命令声明的全局变量，不属于顶层对象的属性。
```javascript 
var a = 1;
// 如果在 Node 的 REPL 环境，可以写成 global.a
// 或者采用通用方法，写成 this.a
window.a // 1

let b = 1;
window.b // undefined
```
引入`globalThis`作为顶层对象。也就是说，任何环境下，`globalThis`都是存在的，都可以从它拿到顶层对象，指向全局环境下的`this`

### 暂时性死域
---
在 JavaScript 中，**暂时性死域（Temporal Dead Zone，简称 TDZ）** 是 ES6 引入 `let` 和 `const` 后出现的概念，指的是变量在**声明之前无法被访问**的这段“死区”范围。

使用 `let` 或 `const` 声明的变量，在**声明语句执行之前**，该变量所处的作用域范围就是“暂时性死域”。在这个范围内访问变量会直接抛出 `ReferenceError`，即使通过全局对象（如 `window`）也无法访问。
```javascript
console.log(a); // 报错：ReferenceError: Cannot access 'a' before initialization
let a = 10;
```
- 变量 `a` 用 `let` 声明，在 `let a = 10` 执行前，访问 `a` 就处于 TDZ 中，直接报错。

暂时性死域的范围从**当前作用域开始**，直到**变量声明语句执行完毕**为止。

1. 全局/函数作用域中的 TDZ
```javascript
// 全局作用域的 TDZ：从文件开始到 let 声明处
function fn() {
  // 函数作用域的 TDZ：从函数开始到 const 声明处
  console.log(b); // 报错：ReferenceError
  const b = 20;
}
fn();
```

2. 块级作用域中的 TDZ
```javascript
if (true) {
  // 块级作用域的 TDZ：从 { 开始到 let 声明处
  console.log(c); // 报错：ReferenceError
  let c = 30;
}
```

3. 解构赋值中的 TDZ
```javascript
// 变量 d 在解构赋值中声明，TDZ 覆盖整个解构表达式
const [d = console.log(d)] = [1]; 
// 报错：ReferenceError: Cannot access 'd' before initialization
```
- 这里 `d` 的默认值 `console.log(d)` 试图在 `d` 声明完成前访问它，处于 TDZ 中。

TDZ 的设计主要是为了：
1. **避免变量提升导致的不合理行为**：  
   `var` 声明的变量会“提升”到作用域顶部，且默认值为 `undefined`，可能导致意外错误（如变量未赋值就被使用）。TDZ 强制要求变量必须先声明后使用，减少逻辑错误。
   
   ```javascript
   // var 没有 TDZ，可能出现不合理行为
   console.log(x); // undefined（不报错，但逻辑上可能有问题）
   var x = 10;
   ```

2. **与 ES6 其他特性保持一致**：  
   如 `class` 声明、模块导入（`import`）等也存在类似的“必须先声明后使用”的规则，TDZ 使 `let`/`const` 与这些特性的行为统一。

| 特性    | `let`/`const`（有 TDZ） | `var`（无 TDZ）               |
| ----- | -------------------- | -------------------------- |
| 声明前访问 | 抛出 `ReferenceError`  | 返回 `undefined`（变量提升）       |
| 提升行为  | 存在“创建阶段”的提升，但未初始化    | 提升到作用域顶部，且初始化为 `undefined` |
| 块级作用域 | ==支持==（变量仅在块内有效）     | 不支持（变量在函数/==全局作用域有效==）     |

- **暂时性死域（TDZ）** 是 `let`/`const` 变量在声明前不可访问的范围，访问会报错。
- 目的是强制“先声明后使用”，避免 `var` 变量提升带来的潜在问题。
- 理解 TDZ 有助于写出更规范的代码，避免因变量未声明就使用导致的错误。