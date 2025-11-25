###  变量作用域
---
如果在代码块 `{...}` 内声明了一个变量，那么这个变量只在该代码块内可见。对于 `if`，`for` 和 `while` 等，在 `{...}` 中声明的变量也仅在内部可见，如果一个函数是在另一个函数中创建的，该函数就被称为“嵌套”函数。
```javascript
{
    let name = 'dano';
    console.log(name);//dano
}

{
    let age = 21;
    console.log(age);//age
    console.log(name);//name is not defined
}
```

在 JavaScript 中，每个运行的==函数==，==代码块 `{...}`== 以及==整个脚本==，都有一个被称为 **词法环境（Lexical Environment）** 的==内部（隐藏）的关联对象==。词法环境对象由两部分组成：
	1. **环境记录（Environment Record）** —— 一个存储所有局部变量作为其属性（包括一些其他信息，例如 `this` 的值）的对象。
	2. 对 **外部词法环境** 的引用，与外部代码相关联。

一个“变量”只是 **环境记录** 这个特殊的内部对象的一个属性。“获取或修改变量”意味着“获取或修改词法环境的一个属性”。

**全局** 词法环境没有外部引用

现在看起来都挺简单的，是吧？
- 变量是特殊内部对象的属性，与当前正在执行的（代码）块/函数/脚本有关。
- 操作变量实际上是操作该对象的属性。

![[Pasted image 20250625122559.png]]
在这个函数调用期间，我们有两个词法环境：内部一个（用于函数调用）和外部一个（全局）：
- 内部词法环境与 `say` 的当前执行相对应。它具有一个单独的属性：`name`，函数的参数。我们调用的是 `say("John")`，所以 `name` 的值为 `"John"`。
- 外部词法环境是全局词法环境。它具有 `phrase` 变量和函数本身。

当代码要访问一个变量时 —— 首先会搜索==内部词法==环境，然后搜索==外部环境==，然后搜索==更外部的环境==，以此类推，==直到全局==词法环境。
```javascript
var scope = "global scope";

function checkScope() {
	var scope = "local scope"; 
	
	function f() {
		return scope; 
	} 
	return f;
} 

checkScope()();
```
输出`local scope`

### 闭包
---
是指一个函数可以记住其外部变量并可以访问这些变量。

函数调用完成后，会将词法环境和其中的所有变量从内存中删除。因为现在没有任何对它们的引用了。与 JavaScript 中的任何其他对象一样，词法环境仅在可达时才会被保留在内存中。

![[Pasted image 20250625124329.png]]
右侧的矩形演示了执行过程中全局词法环境的变化：
1. 当脚本开始运行，词法环境预先填充了所有声明的变量。
    - 最初，它们处于“未初始化（Uninitialized）”状态。这是一种特殊的内部状态，这意味着引擎知道变量，但是在用 `let` 声明前，不能引用它。几乎就像变量不存在一样。
2. 然后 `let phrase` 定义出现了。它尚未被赋值，因此它的值为 `undefined`。从这一刻起，我们就可以使用变量了。
3. `phrase` 被赋予了一个值。
4. `phrase` 的值被修改。
```javascript
let x = 2;
function f() {
    console.log(x);
    let x = 3;
}

f();//Cannot access 'x' before initialization
```
从程序执行进入代码块（或函数）的那一刻起，变量就开始进入“未初始化”状态。它一直保持未初始化状态，直至程序执行到相应的 `let` 语句。也就是说，函数中的x存在于内部的词法环境，但是它的状态是特殊的内部uninitialized。也就是说，内部的x在其上方的代码中是存在的（内部词法环境），所以就不会去寻找外部的词法环境中的x，就error

### this
---
```javascript
function foo() { console.log(this);} foo.call(3);
```

如果处于非严格模式下，要绑定的`this`指定为`null`或`undefined`时会自动替换为全局对象，原始值则会被包装

严格模式：
```javascript
"use strict"; function test() {  console.log(this);} test.call(2);// 2
```

非严格模式
```javascript
function test() {  console.log(this);}test.call(2);// Number {2}
```

1. `Function.prototype.call()` 方法
`call` 是函数的原型方法，用于**显式指定函数执行时的 `this` 指向**，并立即调用函数。

- 语法：`function.call(thisArg, arg1, arg2, ...)`
    - `thisArg`：要绑定给函数的 `this` 值。
    - 后续参数：传递给函数的参数。

2. 非严格模式下的 `this` 绑定（原始值会被 “包装”）
在非严格模式中，若 `call` 的 `thisArg` 是**原始值**（如数字、字符串、布尔值），JavaScript 会自动将其**包装为对应的对象类型**（`Number`、`String`、`Boolean`），再绑定为 `this`。

3. 严格模式下的 `this` 绑定（原始值直接绑定）
在严格模式（通过 `"use strict"` 声明）中，`call` 的 `thisArg` 会**直接绑定**，即使是原始值，也不会被包装为对象。

- 解释：严格模式下，`thisArg` 为 `2`（原始值），直接绑定为 `this`，因此输出原始值 `2`。

3. 特殊情况：`thisArg` 为 `null` 或 `undefined`（非严格模式）
在非严格模式下，若 `call` 的 `thisArg` 是 `null` 或 `undefined`，`this` 会**自动替换为全局对象**（浏览器中是 `window`，Node.js 中是 `global`）。

示例：
```javascript
function foo() {
  console.log(this);
}
foo.call(null); // 浏览器中输出：Window 对象
foo.call(undefined); // 浏览器中输出：Window 对象
```

5. 严格模式与非严格模式的核心区别

|场景|非严格模式|严格模式|
|---|---|---|
|原始值作为 `thisArg`|包装为对应对象（如 `2` → `Number {2}`）|直接绑定原始值（如 `2` → `2`）|
|`thisArg` 为 `null/undefined`|`this` 指向全局对象|`this` 为 `null/undefined`|

- `call` 用于显式绑定函数的 `this` 指向。
- 非严格模式下，原始值会被包装为对象后再绑定为 `this`；`null/undefined` 会被替换为全局对象。
- 严格模式下，`this` 会严格按照 `call` 的 `thisArg` 绑定（原始值直接绑定，`null/undefined` 保持不变）。


这种差异是 JavaScript 为了兼容历史行为（非严格模式）和更严格的语法规范（严格模式）而设计的。