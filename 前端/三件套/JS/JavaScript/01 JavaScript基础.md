# 01 JavaScript基础
> Last Format Time：8/11/2026 21:45:35

本笔记由两个 JavaScript 教程目录中的同主题内容合并而成；全部旧知识保留在“旧笔记知识全集（按来源保留）”中，并由导航逐项索引。

---
## 当前前端开发关键要点

> [!important] 学习优先级：P0
> - 默认使用 `const`，需要重新赋值时使用 `let`；避免在现代业务代码中新增 `var`。
> - 熟练掌握严格模式、相等比较、短路运算、可选链 `?.`、空值合并 `??` 与控制流。
> - 理解 JavaScript 单线程执行、动态类型和垃圾回收的基本模型，能据此判断代码行为。
> - 浏览器交互示例中的 `alert`、`prompt`、`confirm` 主要用于学习与调试，不是现代产品交互方案。

---
## 知识点导航
### [[01 JavaScript基础#现代JS教程与阮一峰ES6 · 0基础简介/JS基础知识|现代JS教程与阮一峰ES6 · 0基础简介/JS基础知识]]
- JS基础
- 严格模式
- 在浏览器与用户交互的函数
- alert
- prompt
- confirm
- 数学运算
- 严格相等
- 条件分支
- 逻辑运算符
- 空值合并？？
- 循环
- 函数
- 箭头函数
- 对象
- 垃圾回收
- 对象属性函数：方法
- 可选链 ?.
- symbol类型
- 对象原始值转换

### [[01 JavaScript基础#现代JS教程与阮一峰ES6 · 1数据类型与变量/var let const|现代JS教程与阮一峰ES6 · 1数据类型与变量/var let const]]
- const
- 顶层对象
- 暂时性死域

### [[01 JavaScript基础#廖雪峰教程 · 2历史背景/2.1 JS历史|廖雪峰教程 · 2历史背景/2.1 JS历史]]
- JS历史
- ECMAScript
- JavaScript版本

### [[01 JavaScript基础#廖雪峰教程 · 3快速入门/3.1基本语法|廖雪峰教程 · 3快速入门/3.1基本语法]]
- 基本语法
- 注释
- 大小写

### [[01 JavaScript基础#廖雪峰教程 · 3快速入门/3.6 条件判断|廖雪峰教程 · 3快速入门/3.6 条件判断]]
- 条件判断
- 多行条件判断

### [[01 JavaScript基础#廖雪峰教程 · 3快速入门/3.7 循环|廖雪峰教程 · 3快速入门/3.7 循环]]
- 循环
- for ... in
- while
- do ... while

---
## 现代前端补充与纠错

> [!info] 修改标记
> - *【修正】*：旧教程中错误、过时或容易误导的内容。
> - *【补充】*：旧教程未覆盖、但当前前端开发需要掌握的内容。
> - *【修正代码】*：替换或校正了旧代码示例。

> [!warning] 历史内容与当前结论
> 下方保留旧教程上下文；已知错误已直接修正或就地标注。若历史结论与本节冲突，以带 *【修正】* 的内容和当前运行环境为准。

### 语法与运行模型
- *【修正】* 对象字面量 `{}` 是对象初始化器语法，不应简单描述成 `new Object()` 的语法糖；二者在原型被改写、`__proto__` 字面量等边界上不能画等号。
- *【修正】* 自动分号插入不是“可以不写分号”的保证。`return`、`throw`、`break`、`continue` 后换行，以及以 `(`、`[`、模板字符串开头的下一行，必须特别检查。
- *【补充】* 现代业务代码默认使用 `const`，需要重新赋值时使用 `let`；`var` 主要用于阅读遗留代码和理解提升、函数作用域。
- *【补充】* 严格模式会改变静默失败、裸函数 `this`、重复参数等行为；ES Module 和 class 主体天然处于严格模式。

### 当前工程判断
- *【补充】* 语法是否可用要同时看目标浏览器、构建目标和运行时，不只看 ECMAScript 年份。
- *【补充】* 可选链 `?.` 只处理左侧为 `null`/`undefined` 的情况；空字符串、`0`、`false` 不是“空值”。默认值优先根据语义选择 `??`，不要机械替换成 `||`。
---
## 旧笔记知识全集（按来源保留）
### 现代JS教程与阮一峰ES6 · 0基础简介/JS基础知识
##### JS基础
##### 严格模式
`use strict`严格模式现代模式。使用类和模块会自动的进入严格模式。
##### 在浏览器与用户交互的函数
##### alert
```javascript
alert("Hello");
```

弹出的这个带有信息的小窗口被称为 **模态窗**。“modal” 意味着用户不能与页面的其他部分进行交互，直到他们处理完窗口。
![[Pasted image 20260412160610.png]]

##### prompt
```javascript
result = prompt(title, [default]);
```

浏览器会显示一个带有文本消息的模态窗口，还有 input 框和确定/取消按钮。

`title`
显示给用户的文本

`default`
可选的第二个参数，指定 input 框的初始值。
他的返回值是用户输入的值，不输入返回null，返回的值为字符串
##### confirm
会选择确定返回true，取消返回false，参数为问题

```javascript
let isBoss = confirm('Are you the boss?')
```

![[Pasted image 20260412160952.png]]

这些方法都是模态的，在完成前不能做其他事，会暂停脚本的运行，不允许用户进行其他的交互。
上述所有方法共有两个限制：
1. 模态窗口的确切位置由浏览器决定。通常在页面中心。
2. 窗口确切外观也取决于浏览器。我们不能修改它。
##### 数学运算
支持加法，减法，乘法，除法，取余，求幂

使用+来连接字符串，非字符串的将转换为字符串。
而其他的运算符总是转换为数字再进行运算，这里涉及了原始值的转换

使用+后跟字符串形式的数字，会转化为数字，这和使用Number（）是一样的，不过更加的简短

```javascript
let name = '2323';
console.log(typeof (+name));
// 打印number
```

##### 严格相等
在比较不同类型的值时，处于相等判断符号 `==` 两侧的值会先被转化为数字。空字符串和 `false` 也是如此，转化后它们都为数字 0。

**严格相等运算符 `===` 在进行比较时不会做任何的类型转换。**
换句话说，如果 `a` 和 `b` 属于不同的数据类型，那么 `a === b` 不会做任何的类型转换而立刻返回 `false`

JavaScript 存在一个特殊的规则，null与undefined会判定它们相等。它们俩就像“一对恋人”，仅仅等于对方而不等于其他任何的值（只在非严格相等下成立）。

```javascript
//打印true
console.log(null==undefined);
```

我们为何要研究上述示例？我们需要时刻记得这些古怪的规则吗？不，其实不需要。虽然随着代码写得越来越多，我们对这些规则也都会烂熟于胸，但是我们需要更为可靠的方法来避免潜在的问题：
- 除了严格相等 `===` 外，其他但凡是有 `undefined/null` 参与的比较，我们都需要格外小心。
- 除非你非常清楚自己在做什么，否则永远不要使用 `>= > < <=` 去比较一个可能为 `null/undefined` 的变量。对于取值可能是 `null/undefined` 的变量，请按需要分别检查它的取值情况。
##### 条件分支
if和？
##### 逻辑运算符
|| 或运算：
 或运算符 `||` 做了如下的事情：
- 从左到右依次计算操作数。
- 处理每一个操作数时，都将其转化为布尔值。如果结果是 `true`，就停止计算，返回这个操作数的==初始值==。
- 如果所有的操作数都被计算过（也就是，转换结果都是 `false`），则返回最后一个操作数。
```javascript
let a = 0;
let b = 2;
let c = 3;

let result = a || b || c;

console.log(result);//2
```

与“纯粹的、传统的、仅仅处理布尔值的或运算”相比，这个规则就引起了一些很有趣的用法。
1. **获取变量列表或者表达式中的第一个真值。**
    例如，我们有变量 `firstName`、`lastName` 和 `nickName`，都是可选的（即可以是 undefined，也可以是假值）。
    我们用或运算 `||` 来选择有数据的那一个，并显示出来（如果没有设置，则用 `"Anonymous"`）：
```javascript
let firstName = '';
let lastName = '';
let nickName = 'Dano';

console.log(firstName||lastName||nickName||"shit");//Dano
```
2. **短路求值（Short-circuit evaluation）。**
	或运算符 `||` 的另一个用途是所谓的“短路求值”。
	这指的是，`||` 对其参数进行处理，直到达到第一个真值，然后立即返回该值，而无需处理其他参数。
	如果是假的，就会执行后面的语句

```javascript
let isGay = true;
!isGay || console.log('is gay');
isGay || console.log('not gay');

isGay = false;
isGay || console.log('is gay');
isGay || console.log('not gay');
```

**&&与逻辑**：
 与||很相似，它寻找第一个假值并且返回其值，都是真值就返回第一个。

**！逻辑非运算符**接受一个参数，并按如下运作：
1. 将操作数转化为布尔类型：`true/false`。
2. 返回相反的值。
使用两个！！能够将其转化为布尔值。使用Boolean（）也能完成转化。
##### 空值合并？？
如果第一个参数不是 `null/undefined`，则 `??` 返回第一个参数。否则，返回第二个参数。

```javascript
let user;
console.log(user ?? "shit");//shit

user = "Dano";
console.log(user ?? "shit");//Dano
```

注意：
- `??` 运算符的优先级非常低，仅略高于 `?` 和 `=`，因此在表达式中使用它时请考虑添加括号。
- 如果没有明确添加括号，不能将其与 `||` 或 `&&` 一起使用。
##### 循环
普通 `break` 只会打破内部循环。这还不够 —— 标签可以实现这一功能！
**标签** 是在循环之前带有冒号的标识符：
```javascript
outer: for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 4; j++) {
        console.log(i, j);//2,3后退出
        if (i == 2 && j == 3) break outer;
    }
}
```

`break` 指令必须在代码块内。从技术上讲，任何被标记的代码块都有效

**switch**：
Switch（）括号中的值和case后紧跟的值为严格相等时才会进入case。

```javascript
case 2:
case 3:
	log()
	break;
```

分组2和3执行相同的代码
##### 函数
函数声明：
`function` 关键字首先出现，然后是 **函数名**，然后是括号之间的 **参数** 列表（用逗号分隔，在上述示例中为空，我们将在接下来的示例中看到），最后是花括号之间的代码（即“函数体”）。
新函数可以通过名称调用：`showMessage()`。

```javascript
function f(){
	console.log('shit');
	return true;
}
```

在函数中声明的变量只在该函数内部可见。函数对外部变量拥有全部的访问权限。函数也可以修改外部变量。
如果在函数内部声明了同名变量，那么函数会 **遮蔽** 外部变量。
使用 `=` 为函数声明中的参数指定所谓的“默认”值

函数以 XX 开始……
- `"get…"` —— 返回一个值，
- `"calc…"` —— 计算某些内容，
- `"create…"` —— 创建某些内容，
- `"check…"` —— 检查某些内容并返回 boolean 值，等。

函数表达式：允许省略函数名

```javascript
let f = function(){
	console.log('shit');
	return true;
}
```

上面的两个代码示例的含义是一样的：“创建一个函数并将其放入变量f中”。
**无论函数是如何创建的，函数都是一个值。上面的两个示例都在f 变量中存储了一个函数。**

函数是一个值，所以我们可以把它当成存储着函数的值对待。上面代码显示了一段字符串值，即函数的源码。

```javascript
let f = function () {
    console.log('shit');
    return true;
}

console.log(f);//函数源码[Function: f]
console.log(f());//调用函数
```

回调函数：
将函数作为值来传递

```javascript
function yes() {
    console.log("'yes i'm gay");
}
function no() {
    console.log("not a gay");
}

let shit = function (isGay, yes, no) {
    isGay ? yes() : no();
}

shit(true, yes, no);

```

更加简洁的写法：
```javascript
shit(true,function () {console.log(1)},function () {console.log(0)});
```

这里直接在 `ask(...)` 调用内进行函数声明。这两个函数没有名字，所以叫 **匿名函数**。这样的函数在 `ask` 外无法访问（因为没有对它们分配变量），不过这正是我们想要的。

**函数表达式是在代码执行到达时被创建，并且仅从那一刻起可用。**
**在函数声明被定义之前，它就可以被调用。**
##### 箭头函数
```javascript
let shit = function (isGay, yes, no) {
    isGay ? yes() : no();
};

let shit2 = (isGay, yes, no) => {
    isGay ? yes() : no();
};
```

如果我们只有一个参数，还可以省略掉参数外的圆括号,如果没有参数，括号则是空的（但括号必须保留）。

如果表达式只有一行，则可以省略{ }，箭头函数将自动返回表达式的值，如果使用了{ }想要有返回值则必须return
##### 对象
*8/11/26 【修正】原内容：对象字面量本质上也是 `new` 出来的语法糖；修改点：对象字面量是对象初始化器语法，不能与 `new Object()` 完全等同。*
创建对象常见写法如下，但两者不应视为完全等价：
```javascript
let user = new Object(); // “构造函数” 的语法
let user = {};  // “字面量” 的语法`
let user2 = {
    name: 'dano',
    age: 32,
    "likes birds":true,
}
```

使用`delete`操作符来删除属性。添加多词语的属性时要加上引号。列表中的最后一个属性应以逗号结尾。使得我们的添加，删除操作是相似的行为。

```js
Function.prototype.myCall = function (thisArg, ...args) {
    thisArg = thisArg || window
    // 将被call的函数（this）绑定到thisArg上，这样在调用fn时，this指向thisArg
    thisArg.fn = this

    let res = thisArg.fn(args)

    // 在这里使用了delete
    delete thisArg.fn
    return res
}
```

方括号中的字符串要放在引号中，单引号或双引号都可以。

```javascript
let user = new Object();
let user2 = {
    name: 'dano',
    age: 32,
    "hi world": 'njkjk',
}

console.log(user2["hi world"]);//njkjk
console.log(user2["name"]);
user2["age"] = 21;
console.log(user2["age"]);
```

 完全可以使用[]来代替.但是写着更加的麻烦。

计算属性：
```javascript
let fruit = 'apple';

let bag = {
    [fruit]: 34,
}

console.log(bag.apple);
```

大部分时间里，当属性名是已知且简单的时候，就使用点符号。如果我们需要一些更复杂的内容，那么就用方括号。

属性简写：
```javascript
let user = {
    name: name,
    age,//age: age,
}
```

检查属性是否存在的操作符 `"in"`。

```javascript
'name' in user;
```

对象的引用和复制：
**赋值了对象的变量存储的不是对象本身，而是该对象“在内存中的地址” —— 换句话说就是对该对象的“引用”。**
他们共享内部的属性

我们可以创建一个新对象，通过遍历已有对象的属性，并在原始类型值的层面复制它们，以实现对已有对象结构的复制。也可以使用 [Object.assign](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign) 方法来达成同样的效果。
- 第一个参数 `dest` 是指目标对象。
- 更后面的参数 `src1, ..., srcN`（可按需传递多个参数）是源对象。
- 该方法将所有源对象的属性拷贝到目标对象 `dest` 中。换句话说，从第二个开始的所有参数的属性都被拷贝到第一个参数的对象中。
- 调用结果返回 `dest`。
```javascript
let user = {
    name: 'dano',
    age:21,//age: age,
}

let clone = {};
let clone2 = new Object();

for (value in user) {
    clone[value] = user[value];
}

Object.assign(clone2, user);
clone2.name = 'jungle';
console.log(clone.name);
console.log(clone2.name);
```

也可以使用assign来修改对象中的值

但是上述所使用的方法均为浅拷贝，如果对象的值为对象，那么他们还是会共享一个对象。使用深拷贝来解决这个问题，可以使用lodash库的cloneDeep(obj)

使用const来声明的对象的值也是可以修改的，只要不是整体对对象进行修改就可以。
##### 垃圾回收
JavaScript 中主要的内存管理概念是 **可达性**。
简而言之，“可达”值是那些以某种方式可访问或可用的值。它们被存储在内存中。
1. 这里列出固有的可达值的基本集合，这些值明显不能被释放。
    比方说：
    - 当前执行的函数，它的局部变量和参数。
    - 当前嵌套调用链上的其他函数、它们的局部变量和参数。
    - 全局变量。
    - （还有一些其他的，内部实现）
    这些值被称作 **根（roots）**。
2. 如果一个值可以从根通过引用或者引用链进行访问，则认为该值是可达的。

也就是能够被访问到的值（根），是可达的。

垃圾回收的基本算法被称为 “mark-and-sweep”。
定期执行以下“垃圾回收”步骤：
- 垃圾收集器找到所有的根，并“标记”（记住）它们。
- 然后它遍历并“标记”来自它们的所有引用。
- 然后它遍历标记的对象并标记 **它们的** 引用。所有被遍历到的对象都会被记住，以免将来再次遍历到同一个对象。
- ……如此操作，直到所有可达的（从根部）引用都被访问到。
- 没有被标记的对象都会被删除。

主要需要掌握的内容：
- 垃圾回收是自动完成的，我们不能强制执行或是阻止执行。
- 当对象是可达状态时，它一定是存在于内存中的。
- 被引用与可访问（从一个根）不同：一组相互连接的对象可能整体都不可达，正如我们在上面的例子中看到的那样。
##### 对象属性函数：方法
```javascript
let user = {
    name: 'dano',
    age: 21,
    eat: function () {
        console.log('eat!!!');
    },
    sleep: () => {
        console.log('sleep!!!');
    },
    jump() {//简写
      console.log('jump!!!');
    },
}

user.walk = () => {
    console.log('walk!!!');
}

user.eat();
user.sleep();
user.walk();
user.jump();
```

在对象字面量中，有一种更短的（声明）方法的语法，这种表示法还是有些不同。在对象继承方面有一些细微的差别（稍后将会介绍），但目前它们并不重要。在几乎所有的情况下，更短的语法是首选的。

 **方法中的this**：
 通常，对象方法需要访问对象中存储的信息才能完成其工作。**为了访问该对象，方法中可以使用 `this` 关键字。**

`this` 的值就是在点之前的这个对象，即调用该方法的对象。

在 JavaScript 中，`this` 关键字与其他大多数编程语言中的不同。JavaScript 中的 `this` 可以用于任何函数，即使它不是对象的方法。`this` 的值是在代码运行时计算出来的，它取决于代码上下文。在没有对象的情况下调用this == undefined

在非严格模式的情况下，`this` 将会是 **全局对象**（浏览器中的 `window`，我们稍后会在 [全局对象](https://zh.javascript.info/global-object) 一章中学习它）。这是一个历史行为，`"use strict"` 已经将其修复了。

箭头函数有些特别：它们没有自己的 `this`。如果我们在这样的函数中引用 `this`，`this` 值取决于外部“正常的”函数。
##### 可选链 ?.
假设我们有很多个 `user` 对象，其中存储了我们的用户数据。我们大多数用户的地址都存储在 `user.address` 中，街道地址存储在 `user.address.street` 中，但有些用户没有提供这些信息。在这种情况下，当我们尝试获取 `user.address.street`，而该用户恰好没提供地址信息，我们则会收到一个错误.

==如果该元素不存在，则访问 `null` 的 `.innerHTML` 属性时会报错==。在某些情况下，当元素的缺失是没问题的时候，我们希望避免出现这种错误，而是==接受 `html = null` 作为结果==。

如果可选链 `?.` 前面的值为 ==`undefined` 或者 `null`==，它会停止运算并==返回 `undefined`==。

**为了简明起见，在本文接下来的内容中，我们会说如果一个属性既不是 `null` 也不是 `undefined`，那么它就“存在”。**

换句话说，例如 `value?.prop`：
- 如果 `value` 存在，则结果与 `value.prop` 相同，
- 否则（当 `value` 为 `undefined/null` 时）则返回 `undefined`。

```javascript
let student = {};

console.log(student?.name?.firstName);//undefined
console.log(student.name.firstName);
//Cannot read properties of undefined (reading 'firstName')
```

```javascript
let html =document.findById('header')?.innerHTML;
```

使用这种的写法就不会因为获取不到HTML元素而报错了，在写小游戏的时候（粘钩504），每次都要用if来判断元素是否存在，不然就报错，烦死了。

这种方法具有==短路效应==，在左侧发现错误就不会继续向右执行了，直接返回undefined。

`?.()` 用于调用一个可能不存在的函数。语法 `?.[]` 跟前面的例子类似，它允许从一个可能不存在的对象上安全地读取属性。我们可以使用 `?.` 来安全地读取或删除，但不能写入

可选链 `?.` 语法有三种形式：
1. `obj?.prop` —— 如果 `obj` 存在则返回 `obj.prop`，否则返回 `undefined`。
2. `obj?.[prop]` —— 如果 `obj` 存在则返回 `obj[prop]`，否则返回 `undefined`。
3. `obj.method?.()` —— 如果 `obj.method` 存在则调用 `obj.method()`，否则返回 `undefined`。
##### symbol类型
根据规范，只有两种原始类型可以用作对象属性键：
- 字符串类型
- symbol 类型

symbol 保证是唯一的。即使我们创建了许多具有相同描述的 symbol，它们的值也是不同。描述只是一个标签，不影响任何东西。

id2为symbol名，id为symblo描述

```javascript
let id = Symbol('id');
let id2 = Symbol('id');

console.log(id == id2);//false
```

JavaScript 中的大多数值都支持字符串的隐式转换。例如，我们可以 `alert` 任何值，都可以生效。symbol 比较特殊，它不会被自动转换。如果我们真的想显示一个 symbol，我们需要在它上面调用 `.toString()`

```javascript
let { log } = console;

let id = Symbol('id');
let id2 = Symbol('id');

console.log(id == id2);//false

log(id.toString(), String(id));//Symbol(id) Symbol(id)
log(id.description)//id 获取id的描述（description）
```

symbol 允许我们创建对象的“隐藏”属性，代码的任何其他部分都不能意外访问或重写这些属性。
例如，如果我们使用的是属于第三方代码的 `user` 对象，我们想要给它们添加一些标识符。
我们可以给它们使用 symbol 键：
```javascript
let id = Symbol('id');
let id2 = Symbol('id');

let user = {};
user.id = 3;
user[id2]='dano'

log(user.id);
log(user[id2])
```

除了使用symbol来访问其他的值都无法访问

在字面量中使用要用[ ]括起来

```javascript
let id=Symbol('id')
let user = {
	name:'shit',
	[id]:123,
}
```

symbol 属性不参与 `for..in` 循环。
[Object.keys(user)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) 也会忽略它们。这是一般“隐藏符号属性”原则的一部分。如果另一个脚本或库遍历我们的对象，它不会意外地访问到符号属性。
[Object.assign](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Object/assign) 会同时复制字符串和 symbol 属性

通常所有的 symbol 都是不同的，即使它们有相同的名字。但有时我们想要名字相同的 symbol 具有相同的实体。
该调用会检查全局注册表，如果有一个描述为 `key` 的 symbol，则返回该 symbol，否则将创建一个新 symbol（`Symbol(key)`），并通过给定的 `key` 将其存储在注册表中。注册表内的 symbol 被称为 **全局 symbol**。

对于全局 symbol，`Symbol.for(key)` 按名字返回一个 symbol。相反，通过全局 symbol 返回一个名字，我们可以使用 `Symbol.keyFor(sym)`。它不适用于非全局 symbol。如果 symbol 不是全局的，它将无法找到它并返回 `undefined`。
##### 对象原始值转换
JavaScript 不允许自定义运算符去处理对象。与其他一些编程语言（Ruby，C++）不同，我们无法实现特殊的对象处理方法来处理加法（或其他运算）。

在此类运算的情况下，对象会被自动转换为原始值，然后对这些原始值进行运算，并得到运算结果（也是一个原始值）。

这是一个重要的限制：因为 `obj1 + obj2`（或者其他数学运算）的结果不能是另一个对象！

还是没看懂。。。4/12/26

### 现代JS教程与阮一峰ES6 · 1数据类型与变量/var let const
##### const
由其所声明的==变量的指针==所指向的==内存地址是固定的==，所以对于数值，布尔值，和字符串来说，就是其本身。但是对于复合的数据类型（引用类型的值），其只能保证指针是不变的，指针所指向的内容不能保证不变，所以可以修改由const声明的数组和对象的值

```javascript
//使用Object.freeze方法来声明，对象和对象的属性将同时不能被修改。
const object =Object.freeeze({});
```

##### 顶层对象
window或者global

`var`命令和`function`命令声明的全局变量，依旧是顶层对象的属性；

另一方面规定，`let`命令、`const`命令、`class`命令声明的全局变量，不属于顶层对象的属性。

```javascript
var a = 1;
// 如果在 Node 的 REPL 环境，可以写成 global.a
// 或者采用通用方法，写成 this.a
window.a // 1

let b = 1;
window.b // undefined
```

`globalThis` 是**ES2020** 引入的==统一顶层对象==，解决了不同 JavaScript 运行环境（浏览器、Node.js、Web Worker）顶层对象名称不统一的问题：
- 浏览器：`window` / `self`
- Node.js：`global`
- Web Worker：`self`

`globalThis` 在**所有环境**下都能直接使用，统一指向全局的 `this`。

```javascript
// 1. 全局定义一个变量（挂载到顶层对象）
var globalVar = "我是全局变量";

// 2. 使用 globalThis 统一访问顶层对象
console.log(globalThis.globalVar);
// 输出：我是全局变量（浏览器、Node.js、Worker 环境都生效）

// 3. 给全局对象添加属性（所有环境通用）
globalThis.myGlobalFunc = function () {
  return "Hello globalThis!";
};

// 4. 调用全局方法
console.log(globalThis.myGlobalFunc());
// 输出：Hello globalThis!

// 5. 验证：globalThis 就是当前环境的顶层对象
// 浏览器：globalThis === window
// Node.js：globalThis === global
// Worker：globalThis === self
console.log(globalThis === (typeof window !== 'undefined' ? window : global));
```

1. **浏览器环境**
   `globalThis` 等价于 `window`

```javascript
   globalThis === window; // true
```

2. **Node.js 环境**
   `globalThis` 等价于 `global`

```javascript
   globalThis === global; // true
```

3. **Web Worker 环境**
   `globalThis` 等价于 `self`

```javascript
   globalThis === self; // true
```

##### 暂时性死域
在 JavaScript 中，**暂时性死域（Temporal Dead Zone，简称 TDZ）** 是 ES6 引入 `let` 和 `const` 后出现的概念，指的是变量在**声明之前无法被访问**的这段“死区”范围。

使用 `let` 或 `const` 声明的变量，在**声明语句执行之前**，该变量所处的作用域范围就是“暂时性死域”。在这个范围内访问变量会直接抛出 `ReferenceError`，即使通过全局对象（如 `window`）也无法访问。

```javascript
console.log(a); // 报错：ReferenceError: Cannot access 'a' before initialization
let a = 10;
```
- 变量 `a` 用 `let` 声明，在 `let a = 10` 执行前，访问 `a` 就处于 TDZ 中，直接报错。

==暂时性死域的范围从**当前作用域开始**，直到**变量声明语句执行完毕**为止。==

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
   `var` 声明的变量会“提升”到==作用域顶部==，且默认值为 `undefined`，可能导致意外错误（如变量未赋值就被使用）。TDZ 强制要求变量必须先声明后使用，减少逻辑错误。

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

这个暂时性死域可以简单的理解为先定义再使用，这在c/c++、java中是很正常的。

### 廖雪峰教程 · 2历史背景/2.1 JS历史
##### JS历史
在上个世纪的1995年，当时的网景公司正凭借其Navigator浏览器成为Web时代开启时最著名的第一代互联网公司。

由于网景公司希望能在静态HTML页面上添加一些动态效果，于是叫Brendan Eich这哥们在两周之内设计出了JavaScript语言。你没看错，这哥们只用了10天时间。

为什么起名叫JavaScript？原因是当时Java语言非常红火，所以网景公司希望借Java的名气来推广，但事实上JavaScript除了语法上有点像Java，其他部分基本上没啥关系。
##### ECMAScript
因为网景开发了JavaScript，一年后微软又模仿JavaScript开发了JScript，为了让JavaScript成为全球标准，几个公司联合ECMA（European Computer Manufacturers Association）组织定制了JavaScript语言的标准，被称为ECMAScript标准。

所以简单说来就是，ECMAScript是一种语言标准，而JavaScript是网景公司对ECMAScript标准的一种实现。

那为什么不直接把JavaScript定为标准呢？因为JavaScript是网景的注册商标。

不过大多数时候，我们还是用JavaScript这个词。如果你遇到ECMAScript这个词，简单把它替换为JavaScript就行了。
##### JavaScript版本
JavaScript的标准——ECMAScript在不断发展，最新版ECMAScript 6标准（简称ES6）已经在==2015年6月==正式发布了，所以，讲到JavaScript的版本，实际上就是说它实现了ECMAScript标准的哪个版本。

### 廖雪峰教程 · 3快速入门/3.1基本语法
##### 基本语法
JavaScript的语法和Java语言类似，每个语句以`;`结束，语句块用`{...}`。但是，JavaScript并不强制要求在每个语句的结尾加`;`，浏览器中负责执行JavaScript代码的引擎会自动在每个语句的结尾补上`;`。

让JavaScript引擎自动加分号在某些情况下可能会改变程序的语义，导致运行结果与期望不一致。

例如，下面的一行代码就是一个完整的赋值语句：
```javascript
var x = 1;
```

下面的一行代码是一个字符串，但仍然可以视为一个完整的语句：
```javascript
'Hello, world';
```

下面的一行代码包含两个语句，每个语句用`;`表示语句结束：
```javascript
var x = 1; var y = 2; // 不建议一行写多个语句!
```

语句块是一组语句的集合，例如，下面的代码先做了一个判断，如果判断成立，将执行`{...}`中的所有语句：
```javascript
if (2 > 1) {
    x = 1;
    y = 2;
    z = 3;
}
```

注意花括号`{...}`内的语句具有缩进，通常是4个空格。缩进不是JavaScript语法要求必须的，但缩进有助于我们理解代码的层次，所以编写代码时要遵守缩进规则。很多文本编辑器具有“自动缩进”的功能，可以帮助整理代码。

`{...}`还可以嵌套，形成层级结构：
```javascript
if (2 > 1) {
    x = 1;
    y = 2;
    z = 3;
    if (x < y) {
        z = 4;
    }
    if (x > y) {
        z = 5;
    }
}
```

JavaScript本身对嵌套的层级没有限制，但是过多的嵌套无疑会大大增加看懂代码的难度。遇到这种情况，需要把部分代码抽出来，作为函数来调用，这样可以减少代码的复杂度。
##### 注释
以`//`开头直到行末的字符被视为行注释，注释是给开发人员看到，JavaScript引擎会自动忽略：
```javascript
// 这是一行注释
alert('hello'); // 这也是注释
```

另一种块注释是用`/*...*/`把多行字符包裹起来，把一大“块”视为一个注释：
```javascript
/* 从这里开始是块注释
仍然是注释
仍然是注释
注释结束 */
```

##### 大小写
请注意，JavaScript严格区分大小写，如果弄错了大小写，程序将报错或者运行不正常。

### 廖雪峰教程 · 3快速入门/3.6 条件判断
##### 条件判断
JavaScript使用`if () { ... } else { ... }`来进行条件判断。例如，根据年龄显示不同内容，可以用`if`语句实现如下：
```javascript
let age = 20;
if (age >= 18) { // 如果age >= 18为true，则执行if语句块
    console.log('adult');
} else { // 否则执行else语句块
    console.log('teenager');
}
```

其中`else`语句是可选的。如果语句块只包含一条语句，那么可以省略`{}`：
```javascript
let age = 20;
if (age >= 18)
    console.log('adult');
else
    console.log('teenager');
```

##### 多行条件判断
如果还要更细致地判断条件，可以使用多个`if...else...`的组合：
```javascript
let age = 3;
if (age >= 18) {
    console.log('adult');
} else if (age >= 6) {
    console.log('teenager');
} else {
    console.log('kid');
}
```

上述多个`if...else...`的组合实际上相当于两层`if...else...`：
```javascript
let age = 3;
if (age >= 18) {
    console.log('adult');
} else {
    if (age >= 6) {
        console.log('teenager');
    } else {
        console.log('kid');
    }
}
```

_请注意_，`if...else...`语句的执行特点是二选一，在多个`if...else...`语句中，如果某个条件成立，则后续就不再继续判断了。

如果`if`的条件判断语句结果不是`true`或`false`怎么办？例如：
```javascript
let s = '123';
if (s.length) { // 条件计算结果为3
    //
}
```

JavaScript把`null`、`undefined`、`0`、`NaN`和空字符串`''`视为`false`，其他值一概视为`true`，因此上述代码条件判断的结果是`true`。

### 廖雪峰教程 · 3快速入门/3.7 循环
##### 循环
JavaScript的循环有两种，一种是`for`循环，通过初始条件、结束条件和递增条件来循环执行语句块：
```javascript
let x = 0;
let i;
for (i=1; i<=10000; i++) {
    x = x + i;
}
x; // 50005000
```

`for`循环最常用的地方是利用索引来遍历数组：
```javascript
let arr = ['Apple', 'Google', 'Microsoft'];
let i, x;
for (i=0; i<arr.length; i++) {
    x = arr[i];
    console.log(x);
}
```

`for`循环的3个条件都是可以省略的，如果没有退出循环的判断条件，就必须使用`break`语句退出循环，否则就是死循环：
```javascript
let x = 0;
for (;;) { // 将无限循环下去
    if (x > 100) {
        break; // 通过if判断来退出循环
    }
    x ++;
}
```

##### for ... in
`for`循环的一个变体是`for ... in`循环，它可以把一个对象的所有属性依次循环出来：
```javascript
let o = {
    name: 'Jack',
    age: 20,
    city: 'Beijing'
};
for (let key in o) {
    console.log(key); // 'name', 'age', 'city'
}
```

要过滤掉对象继承的属性，用`hasOwnProperty()`来实现：
```javascript
let o = {
    name: 'Jack',
    age: 20,
    city: 'Beijing'
};
for (let key in o) {
    if (o.hasOwnProperty(key)) {
        console.log(key); // 'name', 'age', 'city'
    }
}
```

由于`Array`也是对象，而它的每个元素的索引被视为对象的属性，因此，`for ... in`循环可以直接循环出`Array`的索引：
```javascript
let a = ['A', 'B', 'C'];
for (let i in a) {
    console.log(i); // '0', '1', '2'
    console.log(a[i]); // 'A', 'B', 'C'
}
```

_请注意_，`for ... in`对`Array`的循环得到的是`String`而不是`Number`。
##### while
`for`循环在已知循环的初始和结束条件时非常有用。而上述忽略了条件的`for`循环容易让人看不清循环的逻辑，此时用`while`循环更佳。

`while`循环只有一个判断条件，条件满足，就不断循环，条件不满足时则退出循环。比如我们要计算100以内所有奇数之和，可以用while循环实现：
```javascript
let x = 0;
let n = 99;
while (n > 0) {
    x = x + n;
    n = n - 2;
}
x; // 2500
```

在循环内部变量`n`不断自减，直到变为`-1`时，不再满足`while`条件，循环退出。
##### do ... while
最后一种循环是`do { ... } while()`循环，它和`while`循环的唯一区别在于，不是在每次循环开始的时候判断条件，而是在每次循环完成的时候判断条件：
```javascript
let n = 0;
do {
    n = n + 1;
} while (n < 100);
n; // 100
```

用`do { ... } while()`循环要小心，循环体会至少执行1次，而`for`和`while`循环则可能一次都不执行。
