# 07 函数、作用域与this
> Last Format Time：8/11/2026 21:45:38

本笔记由两个 JavaScript 教程目录中的同主题内容合并而成；全部旧知识保留在“旧笔记知识全集（按来源保留）”中，并由导航逐项索引。

---
## 当前前端开发关键要点

> [!important] 学习优先级：P0
> - 理解词法作用域、闭包和调用位置如何决定 `this`，能解释常见回调与事件处理问题。
> - 箭头函数没有自己的 `this`、`arguments` 和构造能力；不要机械地替代所有普通函数。
> - 掌握参数默认值、rest、spread、解构、高阶函数以及 `call/apply/bind` 的实际用途。
> - 闭包会延长变量生命周期；在订阅、定时器和 React Effect 中要关注清理与过期值问题。

---
## 知识点导航
### [[07 函数、作用域与this#现代JS教程与阮一峰ES6 · 2函数/作用域、闭包和this|现代JS教程与阮一峰ES6 · 2函数/作用域、闭包和this]]
- 变量作用域
- 闭包
- this

### [[07 函数、作用域与this#现代JS教程与阮一峰ES6 · 2函数/函数进阶|现代JS教程与阮一峰ES6 · 2函数/函数进阶]]
- new function
- setTimeOut setaInterval
- 函数绑定
- 透明缓存
- 手动实现call、apply与bind
- 实现 call
- 实现 apply
- 实现 bind
- softBind
- 函数参数Params和arguments对象
- rest和spread
- 全局对象
- 函数对象

### [[07 函数、作用域与this#现代JS教程与阮一峰ES6 · 2函数/扩展运算符|现代JS教程与阮一峰ES6 · 2函数/扩展运算符]]
- 展开可迭代对象（拆分为单个元素）
- 收集剩余元素（合并为数组）
- 浅拷贝对象或数组
- **二、扩展运算符与 `apply` 的对比**
- **三、注意事项**
- **总结**

### [[07 函数、作用域与this#现代JS教程与阮一峰ES6 · 2函数/箭头函数|现代JS教程与阮一峰ES6 · 2函数/箭头函数]]
- 箭头函数

### [[07 函数、作用域与this#现代JS教程与阮一峰ES6 · 2函数/解构赋值与剩余模式（ES6）|现代JS教程与阮一峰ES6 · 2函数/解构赋值与剩余模式（ES6）]]
- 数组的解构赋值
- 嵌套数组解构
- 对象的解构
- 剩余模式：...

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.1 函数的定义与调用|廖雪峰教程 · 4函数/4.1 函数的定义与调用]]
- 函数的定义与调用
- 定义函数
- 调用函数
- arguments
- rest参数
- 小心你的return语句

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.2 变量作用域与解构赋值|廖雪峰教程 · 4函数/4.2 变量作用域与解构赋值]]
- 变量作用域与解构赋值
- 变量提升
- 全局作用域
- 名字空间
- 局部作用域
- 常量
- 解构赋值
- 使用场景

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.3 方法|廖雪峰教程 · 4函数/4.3 方法]]
- 方法
- apply
- 装饰器

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.4 高阶函数|廖雪峰教程 · 4函数/4.4 高阶函数]]
- 正文主题：4.4 高阶函数

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.5 闭包|廖雪峰教程 · 4函数/4.5 闭包]]
- 闭包
- 函数作为返回值
- 闭包

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.6 箭头函数|廖雪峰教程 · 4函数/4.6 箭头函数]]
- 箭头函数
- this

### [[07 函数、作用域与this#廖雪峰教程 · 4函数/4.7 标签函数|廖雪峰教程 · 4函数/4.7 标签函数]]
- 标签函数

---
## 现代前端补充与纠错

> [!info] 修改标记
> - *【修正】*：旧教程中错误、过时或容易误导的内容。
> - *【补充】*：旧教程未覆盖、但当前前端开发需要掌握的内容。
> - *【修正代码】*：替换或校正了旧代码示例。

> [!warning] 下方手写 `call/apply/bind` 仅作历史练习；参数展开、返回值和目标函数捕获已修正，但仍是不能完整模拟构造调用的教学版本。

### `this` 的判断顺序
- *【修正】* 箭头函数没有自己的 `this`、`arguments`、`super` 和 `new.target`；它捕获词法环境，不适合作为依赖动态接收者的方法。
- *【修正】* 普通函数的 `this` 由调用方式决定：构造调用、显式绑定、方法调用、普通调用分别判断。把函数赋给变量后再调用会丢失原接收者。
- *【修正】* ES Module/严格模式中的裸函数调用 `this` 为 `undefined`，不能假设存在浏览器 `window`。

### `call/apply/bind` 的可靠语义
- *【修正】* `apply` 的参数需要以数组类对象展开，不能写成 `context.fn(args)`。
- *【修正】* `call`/`apply` 必须返回原函数结果；模拟实现还要避免临时属性碰撞、处理 `null`/`undefined` 与原始值装箱。
- *【修正】* `bind` 除了绑定参数和返回值，还必须支持 `new`、原型关系以及构造器显式返回对象等规则。学习时可用 `Reflect.apply`/`Reflect.construct` 验证语义，生产代码直接用原生实现。

*【修正代码】*

```javascript
function invoke(fn, thisArg, args) {
  return Reflect.apply(fn, thisArg, args);
}
```

### 作用域与闭包
- *【补充】* 闭包保留的是词法环境中的绑定，不是某一刻值的副本。
- *【补充】* 事件监听器、定时器和缓存中的闭包可能让对象持续可达；组件卸载或任务取消时应清理外部资源。
---
## 旧笔记知识全集（按来源保留）
### 现代JS教程与阮一峰ES6 · 2函数/函数进阶
##### new function
它实际上是通过运行时通过参数传递过来的字符串创建的。
`new Function` 允许我们将任意字符串变为函数。例如，我们可以从服务器接收一个新的函数并执行它

##### setTimeOut setaInterval
目前有两种方式可以实现：
- `setTimeout` 允许我们将函数推迟到一段时间间隔之后再执行。
- `setInterval` 允许我们重复运行一个函数，从一段时间间隔之后开始运行，之后以该时间间隔连续重复运行该函数。
这**两个方法并不在 JavaScript 的规范**中。但是大多数运行环境都有内建的调度程序，并且提供了这些方法。目前来讲，所有浏览器以及 Node.js 都支持这两个方法。参数说明：

`func|code`
想要执行的函数或代码字符串。一般传入的都是函数。由于某些历史原因，支持传入代码字符串，但是不建议这样做。

`delay`
执行前的延时，以毫秒为单位（1000 毫秒 = 1 秒），默认值是 0；

`arg1`，`arg2`…
要传入被执行函数（或代码字符串）的参数列表（IE9 以下不支持）

```javascript
function eat(name, food) {
    console.log(name+" eat "+food);
}

setTimeout(eat, 1000, "dano", "apple");//dano eat apple

setTimeout(eat("dano", "apple"), 1000);//The "callback" argument must be of type function.
```

`setTimeout` 在调用时会返回一个“定时器标识符（timer identifier）”，在我们的例子中是 `timerId`，我们可以使用它来取消执行。

```javascript
function eat(name, food) {
    console.log(name+" eat "+food);
}

let timerId= setTimeout(eat, 1000, "dano", "apple");
clearTimeout(timerId);//没有输出
```

在浏览器中，定时器标识符是一个数字。在其他环境中，可能是其他的东西。例如 Node.js 返回的是一个定时器对象，这个对象包含一系列方法。这些方法没有统一的规范定义，所以这没什么问题。

`setInterval` 方法和 `setTimeout` 的语法相同

在大多数浏览器中，包括 Chrome 和 Firefox，在显示 `alert/confirm/prompt` 弹窗时，内部的定时器仍旧会继续“嘀嗒”。

所以，在运行上面的代码时，如果在一定时间内没有关掉 `alert` 弹窗，那么在你关闭弹窗后，下一个 `alert` 会立即显示。两次 `alert` 之间的时间间隔将小于 2 秒。

使用嵌套的setTimeout，其效果和setInterval一样，但更加灵活

```javascript
let timerId = setTimeout(function tick () {
    console.log("tick");
    timerId = setTimeout(tick,1000)
},1000)
```

##### 函数绑定
```javascript
let user = {
    name: 'dano',
    eat() {
        console.log(this.name + ' is eating!');
    }
}

user.eat();//dano is eating!
setTimeout(user.eat, 1000);//undefined is eating! 发生了this丢失。
```

一旦==方法被传递到与对象分开的某个地方== —— `this` 就丢失。

**1.使用函数包装器**
在要回调的函数外套一层函数，在外部的函数中调用。

```javascript
setTimeout(function () { user.eat() }, 1000);//dano is eating!
setTimeout(() => user.eat(), 1000);//dano is eating!
```

看起来不错，但是我们的代码结构中出现了一个小漏洞。如果在 `setTimeout` 触发之前（有一秒的延迟！）`user` 的值改变了怎么办？那么，突然间，它将调用错误的对象！

### 2.使用bind
```javascript
let boundEat = user.eat.bind(user);
let timerId = setTimeout(boundEat, 1000);//dano is eating!
boundEat()//dano is eating!
```

`func.bind(context)` 的结果是一个特殊的类似于函数的“外来对象（exotic object）”，它可以像函数一样被调用，并且透明地（transparently）将调用传递给 `func` 并设定 `this=context`。
绑定后可以不使用对象调用。

bind还可以绑定参数：
```javascript
function add(a,b) {
    return a + b;
}

let boundAdd = add.bind(null, 2,2);
console.log(boundAdd(1),boundAdd(22,33));
```

一但参数绑定了，再传入参数就无效了。


##### 透明缓存
有一个 CPU 重负载的函数 `slow(x)`，但它的结果是稳定的。换句话说，对于相同的 `x`，它总是返回相同的结果。
如果经常调用该函数，我们可能希望将结果缓存（记住）下来，以避免在重新计算上花费额外的时间。
创建一个包装器（wrapper）函数，该函数增加了缓存功能。正如我们将要看到的，这样做有很多好处。

```javascript
function add(a) {
    console.log('func is running!!');
    return a;
}

//装饰器函数
function cachingDecorator(func) {
    let cache = new Map();
    return function (x) {
        if (cache.has(x)) {
            return cache.get(x);
        }
        let result = func(x);

        cache.set(x, result);
        return result;
    }
}

add = cachingDecorator(add);

console.log(add(1,2));//func is running!!  1
console.log(add(1,2));//1
```

`cachingDecorator` 是一个 **装饰器（decorator）**：一个特殊的函数，它接受另一个函数并改变它的行为。
其思想是，我们可以为任何函数调用 `cachingDecorator`，它将返回缓存包装器。
从外部代码来看，包装的 `slow` 函数执行的仍然是与之前相同的操作。它只是在其行为上添加了缓存功能。

总而言之，使用分离的 `cachingDecorator` 而不是改变 `slow` 本身的代码有几个好处：
- `cachingDecorator` 是可重用的。我们可以将它应用于另一个函数。
- 缓存逻辑是独立的，它没有增加 `slow` 本身的复杂性（如果有的话）。
- 如果需要，我们可以组合多个装饰器（其他装饰器将遵循同样的逻辑）。

在对象的函数中，这样使用会丢失上下文this

```javascript
let worker = {
    someMethod() {
        return 1;
    },

    slow(x) {
        // 可怕的 CPU 过载任务
        console.log("Called with " + x);
        return x * this.someMethod();
    }
};
// 和之前例子中的代码相同
function cachingDecorator(func) {
    let cache = new Map();
    return function (x) {

        if (cache.has(x)) {
            return cache.get(x);
        }

        let func1 = func.bind(this);
        let result = func1(x);
        cache.set(x, result);

        return result;
    };
}

console.log(worker.slow(1)); // 原始方法有效

worker.slow = cachingDecorator(worker.slow); // 现在对其进行缓存

console.log(worker.slow(2)); //Called with 2   2
console.log(worker.slow(2)); //2
```

使用内建函数方法func.call(context,...args)来提供上下文和参数，和bind很像，但是仅仅提供一次，并不是绑定。

```javascript
// 我们将对 worker.slow 的结果进行缓存
let worker = {
    someMethod() {
        return 1;
    },

    slow(x) {
        // 可怕的 CPU 过载任务
        console.log("Called with " + x);
        return x * this.someMethod();
    }
};

// 和之前例子中的代码相同
function cachingDecorator(func) {

    let cache = new Map();

    return function (x) {

        if (cache.has(x)) {
            return cache.get(x);
        }

        let result = func.call(this, x);
        cache.set(x, result);

        return result;
    };
}

console.log(worker.slow(1)); // 原始方法有效

worker.slow = cachingDecorator(worker.slow); // 现在对其进行缓存

console.log(worker.slow(2)); //Called with 2   2
console.log(worker.slow(2)); //2
```

```javascript
let user = {
    name:'dano'
}

let worker = {
    name:'daozhu'
}

function getName() {
    console.log(this.name);
}

getName();//undefined
getName.call(user);//dano
getName();//undefined
getName.call(worker);//worker

let getName1 = getName.bind(user);
getName1();//dano
getName1();//dano

getName1.call(worker)//dano 绑定后传对象无效
```

修改包装器：现在可以对任意参数数量的函数进行包装。
将所有参数连同上下文一起传递给另一个函数被称为“呼叫转移（call forwarding）”。

```javascript
let worker = {
    slow(min, max) {
        console.log('function is running!');
        return min + max; // scary CPU-hogger is assumed
    }
};

function hash(args) {
    return args[0] + ',' + args[1];
}

function cachingDecorator(func,hash) {
    let cache = new Map();
    return function () {
        let key = hash(arguments);
        if (cache.has(key)) {
            return cache.get(key);
        }

        let result = func.call(this, ...arguments);

        cache.set(key, result);
        return result;
    };
}

// 应该记住相同参数的调用
worker.slow = cachingDecorator(worker.slow,hash);

console.log(worker.slow(2, 4), worker.slow(2, 4));
//function is running! 6 6
```

##### 手动实现call、apply与bind
*8/11/26 【修正代码】原内容：`myCall` 使用 `context || window` 且可能发生临时属性冲突，`apply` 未展开参数，`bind` 丢失返回值，复习版 `myBind` 错把调用时的 `this` 当成目标函数；修改点：`call/apply` 改用 `Reflect.apply` 保留调用语义，其余示例改为展开参数、返回结果并捕获原函数。两个 `bind` 仍是教学简化版，不完整模拟构造调用。*
call、apply的实现很像，返回调用的值，就是参数不一样。bind可以基于call来实现，返回一个函数
##### 实现 call
```javascript
Function.prototype.myCall = function(context, ...args) {
    return Reflect.apply(this, context, args);
};
```

说是call，其实是将函数转移到了call的参数的对象上面，在利用完对象执行完函数得到结果后，移除函数，再return结果。
##### 实现 apply
```javascript
Function.prototype.fakeApply = function (context, args) {
  return Reflect.apply(this, context, args ?? []);
};
```

和call很像，就是参数变了
##### 实现 bind
```javascript
Function.prototype.fakeBind = function (obj, ...bargs) {
  return (...rest) => {
    return this.call(obj, ...bargs, ...rest);
  };
};


// function add(a, b, c) { return a + b + c }
// const bound = add.fakeBind(obj, 1, 2)
//           ↑ 阶段1: bargs = [1, 2]，返回新函数
// bound(3)
// ↑ 阶段2: rest = [3]，此时才执行箭头函数体
//   最终调用: add.call(obj, 1, 2, 3)
```

基于call实现


4/8/26 我又实现了一遍，面试复习

```js
Function.prototype.myCall = function (obj, ...args) {
    return Reflect.apply(this, obj, args)
}

Function.prototype.myApply = function (obj, args) {
    obj.fn = this
    const res = obj.fn(...args)
    delete obj.fn
    return res
}

Function.prototype.myBind = function (obj, ...args) {
    const target = this
    // 这里的args是bind方法的要用的参数
    return function (...args2) {
        // 这里的args2是被绑定的函数的参数
        return target.call(obj, ...args, ...args2)
    }
}


```

##### softBind
是一种函数绑定技巧，目的是为函数设置一个“软绑定”的默认 this。当函数被调用时，如果没有显式指定 this（比如直接调用或作为回调），就会使用 softBind 绑定的默认对象；但如果调用时有明确的 this（如 obj.method() 或 call/apply/bind），则优先使用显式的 this。

```javascript
Function.prototype.softBind = function(obj, ...bargs) {
  const fn = this;
  function bound(...args) {
    // 如果 this 是 undefined 或全局对象，则用 obj，否则用当前 this
    const context = (!this || this === globalThis) ? obj : this;
    return fn.apply(context, [...bargs, ...args]);
  }
  bound.prototype = Object.create(fn.prototype);
  return bound;
};
```

使用场景：比如你希望某个回调函数在没有绑定上下文时，自动使用你指定的默认对象，但又不影响显式绑定的情况。

简而言之，softBind 是 bind 的“弱化版”，只在没有显式 this 时才生效。

**注意**：
以上手动实现是简化版，没有考虑一些边界情况，例如如果 context 是原始值，在非严格模式下应该被包装为对象；以及使用 `new` 操作符调用绑定函数时的行为。但是，它们覆盖了大部分常见的使用场景。
- `call`和`apply`都是立即调用函数，区别在于传参方式。
- `bind`是返回一个绑定了`this`和部分参数的新函数，不会立即调用。

##### 函数参数Params和arguments对象
在 JavaScript 中，`arguments` 和**函数参数（params）** 都与函数接收的输入有关，但它们的本质、用法和特性有显著区别：

**1. 定义与本质**
- **函数参数（params）**
  是在函数定义时显式声明的变量，用于接收函数调用时传递的参数。
  例如：`function fn(a, b) { ... }` 中的 `a` 和 `b` 就是参数（params）。

- **`arguments` 对象**
  是函数内部的一个**类数组对象**，自动包含函数调用时传递的所有实际参数，无论函数定义时是否声明了对应参数。
  仅在非箭头函数中存在（箭头函数没有 `arguments` 对象）。


**2. 核心区别**

| 特性               | 函数参数（params）                          | `arguments` 对象                          |
|--------------------|--------------------------------------------|------------------------------------------|
| **声明方式**       | 函数定义时显式声明（如 `a, b`）             | 函数内部自动生成，无需声明                |
| **数据类型**       | 普通变量（按声明的类型接收值）              | 类数组对象（有 `length`，可通过索引访问）  |
| **与实参的关系**   | 数量固定（由声明决定），多余实参无法直接访问 | 包含所有实参（数量由调用时传递的参数决定） |
| **箭头函数支持**   | 支持                                        | 不支持（箭头函数中无 `arguments`）        |
| **修改影响**       | 修改参数不会影响 `arguments`（非严格模式下有例外） | 修改 `arguments` 可能影响参数（非严格模式） |
| **用途**           | 清晰接收指定参数，便于代码可读性            | 处理不确定数量的参数（如动态传参场景）    |


**3. 示例对比**

（1）基本用法

```javascript
function fn(a, b) {
  // 函数参数（params）
  console.log(a, b); // 1, 2（接收前两个实参）

  // arguments 对象（类数组）
  console.log(arguments); // [1, 2, 3]（包含所有实参）
  console.log(arguments.length); // 3（实参数量）
  console.log(arguments[2]); // 3（访问第三个实参）
}

fn(1, 2, 3); // 调用时传递3个实参
```


2）参数数量不匹配时
- 实参数量 > 参数数量：参数只能接收前 N 个，剩余实参需通过 `arguments` 访问。
- 实参数量 < 参数数量：未被赋值的参数为 `undefined`，`arguments` 长度等于实参数量。

```javascript
function fn(a, b) {
  console.log(a, b); // 1, undefined（实参不足）
  console.log(arguments.length); // 1（仅1个实参）
}

fn(1); // 只传递1个实参
```


（3）严格模式与非严格模式的差异
- **非严格模式**：`arguments` 与参数存在“联动”，修改一方会影响另一方。
- **严格模式**（`"use strict"`）：`arguments` 与参数完全独立，修改互不影响。

```javascript
// 非严格模式
function nonStrict(a) {
  a = 100;
  console.log(arguments[0]); // 100（arguments 随参数变化）
}
nonStrict(1);

// 严格模式
function strictMode(a) {
  "use strict";
  a = 100;
  console.log(arguments[0]); // 1（arguments 不受参数影响）
}
strictMode(1);
```


（4）箭头函数中的表现
箭头函数没有 `arguments` 对象，若需获取所有实参，需使用**剩余参数（`...rest`）**：

```javascript
const arrowFn = (...rest) => {
  // 剩余参数（数组）替代 arguments
  console.log(rest); // [1, 2, 3]（接收所有实参）
  // console.log(arguments); // 报错：arguments is not defined
};
arrowFn(1, 2, 3);
```


**4. 现代替代方案：剩余参数（`...rest`）**
由于 `arguments` 是类数组且在箭头函数中不支持，ES6 引入了**剩余参数（`...rest`）**，它是更优的替代方案：
- 本质是数组（可直接使用 `map`、`forEach` 等方法）；
- 支持箭头函数；
- 语法更清晰，明确表示“接收剩余所有参数”。

```javascript
function fn(a, ...rest) {
  console.log(a); // 1（第一个参数）
  console.log(rest); // [2, 3, 4]（剩余参数，数组类型）
  rest.forEach(item => console.log(item)); // 可直接使用数组方法
}

fn(1, 2, 3, 4);
```


**总结**
- **函数参数（params）**：显式声明的变量，用于接收指定位置的实参，提升代码可读性。
- **`arguments`**：非箭头函数中自动生成的类数组对象，包含所有实参，适合处理动态数量的参数，但在现代开发中逐渐被剩余参数替代。
- 推荐优先使用**显式参数 + 剩余参数（`...rest`）**，避免依赖 `arguments`（尤其是在严格模式和箭头函数中）。
##### rest和spread
在 JavaScript 中，很多内建函数都支持传入任意数量的参数。
例如：
- `Math.max(arg1, arg2, ..., argN)` —— 返回参数中的最大值。
- `Object.assign(dest, src1, ..., srcN)` —— 依次将属性从 `src1..N` 复制到 `dest`。
- ……等。

在 JavaScript 中，无论函数是如何定义的，你都可以在调用它时传入任意数量的参数。
我们可以在函数定义中声明一个数组来收集参数。语法是这样的：`...变量名`，这将会声明一个数组并指定其名称，其中存有剩余的参数。这三个点的语义就是“收集剩余的参数并存进指定数组中”。Rest 参数必须放到**参数列表的末尾**。

有一个名为 `arguments` 的特殊类数组对象可以在函数中被访问，该对象以参数在参数列表中的索引作为键，存储所有参数。尽管 `arguments` 是一个==类数组==，也是可迭代对象，但它终究不是数组。它不支持数组方法，因此我们不能调用 `arguments.map(...)` 等方法。如果我们在箭头函数中访问 `arguments`，访问到的 `arguments` 并不属于箭头函数，而是属于箭头函数外部的“普通”函数。

**Spread 语法**它看起来和 rest 参数很像，也使用 `...`，但是二者的用途完全相反。
当在函数调用中使用 `...arr` 时，它会把**可迭代对象** `arr` “展开”到参数列表中。

```javascript
let arr = [1, 3, 4, 5, 6];
console.log(Math.max(1, ...arr, 9));//9
```


```javascript
let { log } = console;
alert = log;
let str = "Hello";

alert([...str]); // [ 'H', 'e', 'l', 'l', 'o' ]
alert(Array.from(str));//[ 'H', 'e', 'l', 'l', 'o' ]
```

`Array.from(obj)` 和 `[...obj]` 存在一个细微的差别：
- `Array.from` 适用于类数组对象也适用于可迭代对象。
- Spread 语法只适用于可迭代对象。

使用... 来进行拷贝数组和对象：
```javascript
let { log } = console;
alert = log;

let arr = [1, 2, 3];

let arrCopy = [...arr]; // 将数组 spread 到参数列表中
// 然后将结果放到一个新数组

// 两个数组中的内容相同吗？
alert(JSON.stringify(arr) === JSON.stringify(arrCopy)); // true

// 两个数组相等吗？
alert(arr === arrCopy); // false（它们的引用是不同的）

// 修改我们初始的数组不会修改副本：
arr.push(4);
alert(arr); // 1, 2, 3, 4
alert(arrCopy); // 1, 2, 3

let obj = { a: 1, b: 2, c: 3 };

let objCopy = { ...obj }; // 将对象 spread 到参数列表中
// 然后将结果返回到一个新对象

// 两个对象中的内容相同吗？
alert(JSON.stringify(obj) === JSON.stringify(objCopy)); // true

// 两个对象相等吗？
alert(obj === objCopy); // false (not same reference)

// 修改我们初始的对象不会修改副本：
obj.d = 4;
alert(JSON.stringify(obj)); // {"a":1,"b":2,"c":3,"d":4}
alert(JSON.stringify(objCopy)); // {"a":1,"b":2,"c":3}
```

这种方式比使用 `let arrCopy = Object.assign([], arr)` 复制数组，或使用 `let objCopy = Object.assign({}, obj)` 复制对象来说更为简便。因此，只要情况允许，我们倾向于使用它。

当我们在代码中看到 `"..."` 时，它要么是 rest 参数，要么是 spread 语法。
有一个简单的方法可以区分它们：
- 若 `...` 出现在函数参数列表的最后，那么它就是 rest 参数，它会把参数列表中剩余的参数收集到一个数组中。
- 若 `...` 出现在函数调用或类似的表达式中，那它就是 spread 语法，它会把一个数组展开为列表。

使用场景：
- Rest 参数用于创建可接受任意数量参数的函数。
- Spread 语法用于将数组传递给通常需要含有许多参数的函数。

我们可以使用这两种语法轻松地互相转换列表与参数数组。
旧式的 `arguments`（类数组且可迭代的对象）也依然能够帮助我们获取函数调用中的所有参数。



##### 全局对象
全局对象提供可在任何地方使用的变量和函数。默认情况下，这些全局变量内建于语言或环境中。

在浏览器中，它的名字是 “window”，对 Node.js 而言，它的名字是 “global”，其它环境可能用的是别的名字。

最近，`globalThis` 被作为全局对象的标准名称加入到了 JavaScript 中，所有环境都应该支持该名称。所有主流浏览器都支持它。

全局对象的所有属性都可以被**直接访问**
如果一个值非常重要，以至于你想使它在全局范围内可用，那么可以直接将其作为属性写入

```javascript
globalThis.userData = {
    name: 'dano',
    age:21,
}

console.log(userData.name);//dano
console.log(globalThis.userData.age);//21
```

一般不建议使用全局变量。全局变量应尽可能的少。与使用外部变量或全局变量相比，函数获取“输入”变量并产生特定“输出”的代码设计更加清晰，不易出错且更易于测试。

polyfills（垫片）:
如果浏览器版本过旧，存在代码的缺失，可以自行添加代码

##### 函数对象
![[Pasted image 20260412174320.png]]

我已经知道在js中函数也是一个值。函数的值的类型是对象。

```javascript
function f(){
    console.log("dano");
}

console.log(typeof f);
// function
```

函数的名字可以通过name属性来访问

```javascript
function f(){
    console.log("dano");
}

let ff = function () {
    console.log("ff");
}

console.log(f.name);
console.log(ff.name);
```

如果函数自己没有提供，那么在赋值中，会根据上下文来推测一个。

还有另一个内建属性 “length”，它返回函数入参的个数,rest 参数不参与计数.

也可以添加我们自己的属性。
这里我们添加了 `counter` 属性，用来跟踪总的调用次数

```javascript
function sayHi() {
    console.log("Hi");

    // 计算调用次数
    sayHi.counter++;
}
sayHi.counter = 0; // 初始值

sayHi(); // Hi
sayHi(); // Hi

console.log(`Called ${sayHi.counter} times`); // Called 2 times
```

命名函数表达式（NFE，Named Function Expression），指带有名字的函数表达式的术语。
关于名字 `func` 有两个特殊的地方，这就是添加它的原因：
1. 它允许函数在内部引用自己。
2. 它在函数外是不可见的。
```javascript
let sayHi = function func(who) {
    if (who) {
        console.log(`Hello, ${who}`);
    } else {
        func("Guest"); // 使用 func 再次调用函数自身
    }
};

sayHi(); // Hello, Guest

// 但这不工作：
func(); // Error, func is not defined（在函数外不可见）
```

我们为什么使用 `func` 呢？为什么不直接使用 `sayHi` 进行嵌套调用？
问题在于 `sayHi` 的值可能会被函数外部的代码改变。如果该函数被赋值给另外一个变量（译注：也就是原变量被修改），那么函数就会开始报错

### 现代JS教程与阮一峰ES6 · 2函数/箭头函数
##### 箭头函数
JavaScript 充满了我们需要编写在其他地方执行的小函数的情况。
- `arr.forEach(func)` —— `forEach` 对每个数组元素都执行 `func`。
- `setTimeout(func)` —— `func` 由内建调度器执行。

箭头函数没有this，如果访问 `this`，则会从外部获取。

```javascript
let user = {
    name: 'dano',
    eat: ["apple", "peal"],
    showEat() {
        this.eat.forEach((value,index,array) => {
            console.log(this.name + " eat "+value);
        })
    }
}

user.showEat();
```

 箭头函数的这种特性可以将其==视为外层函数的一部分==，箭头函数“的”this，就是外层函数的this。

- 没有 `this`
- 没有 `arguments`
- 不能使用 `new` 调用，因为它没有`this`，无法将创建的空对象绑定到this上[[构造函数与New]]
- 它们也没有 `super`，但目前我们还没有学到它。我们将在 [类继承](https://zh.javascript.info/class-inheritance) 一章中学习它。

### 现代JS教程与阮一峰ES6 · 2函数/解构赋值与剩余模式（ES6）
##### 数组的解构赋值
```javascript
let [a, b, c] = [1, 2, 3];
```

上面代码表示，可以从数组中提取值，按照对应位置，对变量赋值。
本质上，这种写法属于“==模式匹配==”，只要等号两边的模式相同，左边的变量就会被赋予对应的值。
##### 嵌套数组解构
如果解构不成功，变量的值就等于`undefined`。
可以使用三个点 `"..."` 来再加一个参数以获取其余数组项
如果我们想要一个“默认”值给未赋值的变量，我们可以使用 `=` 来提供

```javascript
let [foo, [[bar], baz]] = [1, [[2], 3]];
foo // 1
bar // 2
baz // 3

let [ , , third] = ["foo", "bar", "baz"];
third // "baz"

let [x = 2, , y] = [1, 2, 3];
x // 1
y // 3

let [head, ...tail] = [1, 2, 3, 4];
head // 1
tail // [2, 3, 4]

let [x, y, ...z] = ['a'];
x // "a"
y // undefined
z // []
```

##### 对象的解构
对象的解构与数组有一个重要的不同。数组的元素是按次序排列的，变量的取值由它的位置决定；而对象的属性没有次序，==变量==必须与==属性==同名，才能取到正确的值。

```javascript
let { bar, foo } = { foo: 'aaa', bar: 'bbb' };
foo // "aaa"
bar // "bbb"

let { baz } = { foo: 'aaa', bar: 'bbb' };
baz // undefined
```

使用结构赋值，能够将现有对象的方法赋值到某个变量。

```javascript
const { log }=console;
log('Hello!!');
```

这时`p`==是模式，不是变量==，因此不会被赋值。如果`p`也要作为变量赋值，可以写成下面这样。

```javascript
let obj = {
  p: ['Hello',{ y: 'World' }]
};

let { p, p: [x, { y }] } = obj;
x // "Hello"
y // "World"
p // ["Hello", {y: "World"}]

let { p: [x, { y }] } = obj;
p // error
```

解构赋值的规则是，只要等号右边的值不是对象或数组，就先将其转为对象。由于`undefined`和`null`无法转为对象，所以对它们进行解构赋值，都会报错。

在加载模块时，使用的是模块导入的具名导入，我一直以为是Vue的语法。

```javascript
import { ref } = 'vue';
//如果我这样写呢
import { ref:shit } = 'vue';
//按理来说，const x = shit(9);  应该是没有问题的
```

 经过我的验证，不行，import不能这样写；

交换两个变量值的技巧：
```javascript
[a, b] = [b, a];
```

##### 剩余模式：...
- 解构赋值可以简洁地将一个对象或数组拆开赋值到多个变量上。
- 解构对象的完整语法：
```text
    这表示属性 `prop` 会被赋值给变量 `varName`，如果没有这个属性的话，就会使用默认值 `default`。
    没有对应映射的对象属性会被复制到 `rest` 对象。
- 解构数组的完整语法：
```

    数组的第一个元素被赋值给 `item1`，第二个元素被赋值给 `item2`，剩下的所有元素被复制到另一个数组 `rest`。
- 从嵌套数组/对象中提取数据也是可以的，此时等号左侧必须和等号右侧有相同的结构。

在 JavaScript 中，**剩余模式（Rest Pattern）** 与扩展运算符（`...`）共用相同的语法（三个点 `...`），但功能相反：它用于**将多个元素“收集”为一个数组**，而不是将数组“展开”为元素。剩余模式主要应用于**函数参数**和**解构赋值**场景，用于处理不确定数量的元素。


**一、函数参数中的剩余模式（剩余参数）**
在函数定义时，剩余模式用于将**多余的参数收集为一个数组**，语法为 `...变量名`，该变量会成为一个包含所有剩余参数的数组。
- 剩余参数必须是函数的**最后一个参数**（否则会报错）。
- 剩余参数是**真正的数组**，可直接使用 `map`、`forEach` 等数组方法。

```javascript
// 收集所有参数为数组
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}

console.log(sum(1, 2, 3)); // 6（numbers 为 [1,2,3]）
console.log(sum(10, 20, 30, 40)); // 100（numbers 为 [10,20,30,40]）

// 结合固定参数使用（剩余参数必须在最后）
function greet(greeting, ...names) {
  return `${greeting}, ${names.join(' and ')}!`;
}

console.log(greet('Hello', 'Alice', 'Bob')); // "Hello, Alice and Bob!"
console.log(greet('Hi', 'Charlie')); // "Hi, Charlie!"
```

**二、解构赋值中的剩余模式**
在数组或对象解构时，剩余模式用于**将剩余的元素或属性收集为一个新的数组或对象**。

1. 数组解构中的剩余模式
```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
console.log(first); // 1
console.log(second); // 2
console.log(rest); // [3, 4, 5]（剩余元素组成的数组）

// 只取第一个元素，剩余全部收集
const [head, ...tail] = ['a', 'b', 'c', 'd'];
console.log(head); // 'a'
console.log(tail); // ['b', 'c', 'd']
```

2. 对象解构中的剩余模式
```javascript
const obj = { a: 1, b: 2, c: 3, d: 4 };

// 提取 a 和 b，剩余属性收集到 restObj
const { a, b, ...restObj } = obj;
console.log(a); // 1
console.log(b); // 2
console.log(restObj); // { c: 3, d: 4 }（剩余属性组成的对象）
```

**三、剩余模式与 arguments 的区别**
在函数中，剩余参数与 `arguments` 都能获取所有参数，但有明显区别：

| 特性               | 剩余参数（剩余模式）              | `arguments` 对象                  |
|--------------------|-----------------------------------|-----------------------------------|
| 数据类型           | 真正的数组（可直接用数组方法）    | 类数组对象（需转换为数组才能使用方法） |
| 范围               | 仅包含剩余参数（不包含前面的固定参数） | 包含所有参数（包括固定参数）      |
| 箭头函数支持       | 支持                              | 不支持（箭头函数无 `arguments`）  |
| 可读性             | 明确指定收集的参数，更易理解      | 需手动处理索引，可读性较差        |

```javascript
// 剩余参数（推荐）
function fn1(a, ...rest) {
  console.log(rest.map(x => x * 2)); // 直接使用数组方法
}

// arguments（传统方式）
function fn2(a) {
  const rest = Array.from(arguments).slice(1); // 需转换为数组
  console.log(rest.map(x => x * 2));
}

fn1(1, 2, 3); // [4, 6]
fn2(1, 2, 3); // [4, 6]
```

**四、注意事项**
1. **剩余模式必须是最后一个元素**：无论是函数参数还是解构赋值，剩余模式都必须放在最后，否则会报错。
```javascript
   // 错误示例：剩余参数不在最后
   function wrong(...rest, last) {} // SyntaxError

   // 错误示例：数组解构中剩余模式不在最后
   const [...rest, last] = [1, 2, 3]; // SyntaxError
```

2. **对象剩余模式的顺序无关**：对象解构中，剩余属性的收集与顺序无关，只会包含未显式提取的属性。
3. **不能重复使用**：一个解构或函数参数中只能有一个剩余模式。

### 现代JS教程与阮一峰ES6 · 2函数/扩展运算符
在 JavaScript 中，**扩展运算符（`...`）** 是 ES6 引入的语法，用于将**可迭代对象**（如数组、字符串、`Set`、`Map` 等）“展开”为独立的元素，或用于收集多个元素为一个数组。它的灵活性使其在多种场景中非常实用。

##### 展开可迭代对象（拆分为单个元素）
将数组、字符串等可迭代对象拆分为独立元素，常用于合并、传递参数等场景。

**示例 1：数组合并**

```javascript
const arr1 = [1, 2];
const arr2 = [3, 4];

// 合并数组（替代 concat()）
const merged = [...arr1, ...arr2];
console.log(merged); // [1, 2, 3, 4]

// 在中间插入元素
const withExtra = [0, ...arr1, 2.5, ...arr2, 5];
console.log(withExtra); // [0, 1, 2, 2.5, 3, 4, 5]
```

**示例 2：字符串拆分为字符**

```javascript
const str = "hello";
const chars = [...str];
console.log(chars); // ["h", "e", "l", "l", "o"]
```

**示例 3：传递函数参数**

```javascript
const numbers = [1, 2, 3];

// 传统方式：apply() 传递数组参数
Math.max.apply(null, numbers); // 3

// 扩展运算符：更简洁
Math.max(...numbers); // 3（等价于 Math.max(1, 2, 3)）
```

**示例 4：处理 `Set` 等可迭代对象**

```javascript
const set = new Set([1, 2, 2, 3]); // Set 自动去重
const arrFromSet = [...set]; // 转为数组 [1, 2, 3]
```


##### 收集剩余元素（合并为数组）
在函数参数、数组解构中，用于将多个元素“收集”为一个数组，称为**剩余参数**。

**示例 1：函数剩余参数**

```javascript
// 收集除前两个参数外的所有参数为数组
function sum(first, second, ...rest) {
  console.log(rest); // 剩余参数组成的数组
  return first + second + rest.reduce((a, b) => a + b, 0);
}

sum(1, 2, 3, 4, 5); // 1+2+3+4+5=15，rest 为 [3,4,5]
```

**示例 2：数组解构中的剩余元素**

```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
console.log(first); // 1
console.log(second); // 2
console.log(rest); // [3, 4, 5]（收集剩余元素）
```


##### 浅拷贝对象或数组
扩展运算符可用于快速创建数组或对象的浅拷贝（类似 `Object.assign()`）。

**示例 1：浅拷贝数组**

```javascript
const original = [1, 2, [3, 4]];
const copy = [...original]; // 浅拷贝

// 修改表层元素不影响原数组
copy[0] = 100;
console.log(original[0]); // 1（原数组不变）

// 修改嵌套数组会影响原数组（浅拷贝特性）
copy[2][0] = 300;
console.log(original[2][0]); // 300（原数组的嵌套元素被修改）
```

**示例 2：浅拷贝对象**

```javascript
const obj = { a: 1, b: { c: 2 } };
const objCopy = { ...obj }; // 浅拷贝对象

objCopy.a = 100;
console.log(obj.a); // 1（原对象不变）

objCopy.b.c = 200;
console.log(obj.b.c); // 200（嵌套对象共享引用）
```


##### **二、扩展运算符与 `apply` 的对比**
在 ES6 之前，传递数组作为函数参数需要用 `Function.prototype.apply()`，扩展运算符使其更简洁：
```javascript
const arr = [10, 20, 30];

// 传统方式
Math.min.apply(null, arr); // 10

// 扩展运算符
Math.min(...arr); // 10（更直观）
```


##### **三、注意事项**
1. **仅适用于可迭代对象**：扩展运算符只能作用于可迭代对象（如数组、字符串、`Set`），不能直接用于普通对象（但对象属性展开是特殊语法，见示例 2）。
2. **浅拷贝限制**：对于嵌套的引用类型（对象、数组），扩展运算符仅复制引用，修改会影响原数据。
3. **不能单独用于函数参数之外的场景**：例如 `const a = ...[1,2,3];` 是错误的，必须在数组、对象或函数参数中使用。


##### **总结**
扩展运算符（`...`）是 JavaScript 中非常灵活的语法，主要用途包括：
- 展开可迭代对象（合并数组、拆分字符串、传递参数）；
- 收集剩余元素（函数剩余参数、数组解构）；
- 快速浅拷贝数组或对象。

它简化了许多常见操作的语法，使代码更简洁易懂，是现代 JavaScript 开发中的常用特性。

### 现代JS教程与阮一峰ES6 · 2函数/作用域、闭包和this
##### 变量作用域
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

一个“变量”只是 **环境记录** 这个特殊的内部对象的一个属性。“获取或修改变量”意味着“获取或修改词法环境（环境记录与外部引用）的一个属性”。

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

##### 闭包
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

##### this
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

### 廖雪峰教程 · 4函数/4.1 函数的定义与调用
##### 函数的定义与调用
##### 定义函数
在JavaScript中，定义函数的方式如下：
```javascript
function abs(x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}
```

上述`abs()`函数的定义如下：
- `function`指出这是一个函数定义；
- `abs`是函数的名称；
- `(x)`括号内列出函数的参数，多个参数以`,`分隔；
- `{ ... }`之间的代码是函数体，可以包含若干语句，甚至可以没有任何语句。

请注意，函数体内部的语句在执行时，一旦执行到`return`时，函数就执行完毕，并将结果返回。因此，函数内部通过条件判断和循环可以实现非常复杂的逻辑。

如果没有`return`语句，函数执行完毕后也会返回结果，只是结果为`undefined`。

由于JavaScript的函数也是一个对象，上述定义的`abs()`函数实际上是一个函数对象，而函数名`abs`可以视为指向该函数的变量。

因此，第二种定义函数的方式如下：
```javascript
let abs = function (x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
};
```

在这种方式下，`function (x) { ... }`是一个匿名函数，它没有函数名。但是，这个匿名函数赋值给了变量`abs`，所以，通过变量`abs`就可以调用该函数。

上述两种定义_完全等价_，注意第二种方式按照完整语法需要在函数体末尾加一个`;`，表示赋值语句结束。
##### 调用函数
调用函数时，按顺序传入参数即可：
```javascript
abs(10); // 返回10
abs(-9); // 返回9
```

由于JavaScript允许传入任意个参数而不影响调用，因此传入的参数比定义的参数多也没有问题，虽然函数内部并不需要这些参数：
```javascript
abs(10, 'blablabla'); // 返回10
abs(-9, 'haha', 'hehe', null); // 返回9
```

传入的参数比定义的少也没有问题：
```javascript
abs(); // 返回NaN
```

此时`abs(x)`函数的参数`x`将收到`undefined`，计算结果为`NaN`。

要避免收到`undefined`，可以对参数进行检查：
```javascript
function abs(x) {
    if (typeof x !== 'number') {
        throw 'Not a number';
    }
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}
```

##### arguments
JavaScript还有一个免费赠送的关键字`arguments`，它只在函数内部起作用，并且永远指向当前函数的调用者传入的所有参数。`arguments`类似`Array`但它不是一个`Array`

利用`arguments`，你可以获得调用者传入的所有参数。也就是说，即使函数不定义任何参数，还是可以拿到参数的值：
```javascript
function abs() {
    if (arguments.length === 0) {
        return 0;
    }
    let x = arguments[0];
    return x >= 0 ? x : -x;
}

abs(); // 0
abs(10); // 10
abs(-9); // 9
```

实际上`arguments`最常用于判断传入参数的个数。你可能会看到这样的写法：
```javascript
// foo(a[, b], c)
// 接收2~3个参数，b是可选参数，如果只传2个参数，b默认为null：
function foo(a, b, c) {
    if (arguments.length === 2) {
        // 实际拿到的参数是a和b，c为undefined
        c = b; // 把b赋给c
        b = null; // b变为默认值
    }
    // ...
}
```

要把中间的参数`b`变为“可选”参数，就只能通过`arguments`判断，然后重新调整参数并赋值。
##### rest参数
由于JavaScript函数允许接收任意个参数，于是我们就不得不用`arguments`来获取所有参数：
```javascript
function foo(a, b) {
    let i, rest = [];
    if (arguments.length > 2) {
        for (i = 2; i<arguments.length; i++) {
            rest.push(arguments[i]);
        }
    }
    console.log('a = ' + a);
    console.log('b = ' + b);
    console.log(rest);
}
```

为了获取除了已定义参数`a`、`b`之外的参数，我们不得不用`arguments`，并且循环要从索引`2`开始以便排除前两个参数，这种写法很别扭，只是为了获得额外的`rest`参数，有没有更好的方法？

ES6标准引入了rest参数，上面的函数可以改写为：
```javascript
function foo(a, b, ...rest) {
    console.log('a = ' + a);
    console.log('b = ' + b);
    console.log(rest);
}

foo(1, 2, 3, 4, 5);
// 结果:
// a = 1
// b = 2
// Array [ 3, 4, 5 ]

foo(1);
// 结果:
// a = 1
// b = undefined
// Array []
```

rest参数只能写在最后，前面用`...`标识，从运行结果可知，传入的参数先绑定`a`、`b`，多余的参数以数组形式交给变量`rest`，所以，不再需要`arguments`我们就获取了全部参数。

如果传入的参数连正常定义的参数都没填满，也不要紧，rest参数会接收一个空数组（注意不是`undefined`）。
##### 小心你的return语句
前面我们讲到了JavaScript引擎有一个在行末自动添加分号的机制，这可能让你栽到return语句的一个大坑：
```javascript
function foo() {
    return { name: 'foo' };
}

foo(); // { name: 'foo' }
```

如果把return语句拆成两行：
```javascript
function foo() {
    return
        { name: 'foo' };
}

foo(); // undefined
```

_要小心了_，由于JavaScript引擎在行末自动添加分号的机制，上面的代码实际上变成了：
```javascript
function foo() {
    return; // 自动添加了分号，相当于return undefined;
        { name: 'foo' }; // 这行语句已经没法执行到了
}
```

所以正确的多行写法是：
```javascript
function foo() {
    return { // 这里不会自动加分号，因为{表示语句尚未结束
        name: 'foo'
    };
}
```

### 廖雪峰教程 · 4函数/4.2 变量作用域与解构赋值
##### 变量作用域与解构赋值
在JavaScript中，用`var`申明的变量实际上是有作用域的。

如果一个变量在函数体内部申明，则该变量的作用域为整个函数体，在函数体外不可引用该变量：
```javascript
function foo() {
    var x = 1;
    x = x + 1;
}

x = x + 2; // ReferenceError! 无法在函数体外引用变量x
```

如果两个不同的函数各自申明了同一个变量，那么该变量只在各自的函数体内起作用。换句话说，不同函数内部的同名变量互相独立，互不影响：
```javascript
function foo() {
    var x = 1;
    x = x + 1;
}

function bar() {
    var x = 'A';
    x = x + 'B';
}
```

由于JavaScript的函数可以嵌套，此时，内部函数可以访问外部函数定义的变量，反过来则不行：
```javascript
function foo() {
    var x = 1;
    function bar() {
        var y = x + 1; // bar可以访问foo的变量x!
    }
    var z = y + 1; // ReferenceError! foo不可以访问bar的变量y!
}
```

JavaScript的函数在查找变量时从自身函数定义开始，从“内”向“外”查找。如果内部函数定义了与外部函数重名的变量，则内部函数的变量将“屏蔽”外部函数的变量。
##### 变量提升
JavaScript的函数定义有个特点，它会先扫描整个函数体的语句，把所有用`var`申明的变量“提升”到函数顶部：
```javascript
function foo() {
    var x = 'Hello, ' + y;
    console.log(x);
    var y = 'Bob';
}

foo();
```

虽然是strict模式，但语句`var x = 'Hello, ' + y;`并不报错，原因是变量`y`在稍后申明了。但是`console.log`显示`Hello, undefined`，说明变量`y`的值为`undefined`。这正是因为JavaScript引擎自动提升了变量`y`的声明，但不会提升变量`y`的赋值。

对于上述`foo()`函数，JavaScript引擎看到的代码相当于：
```javascript
function foo() {
    var y; // 提升变量y的申明，此时y为undefined
    var x = 'Hello, ' + y;
    console.log(x);
    y = 'Bob';
}
```

由于JavaScript的这一怪异的“特性”，我们在函数内部定义变量时，请严格遵守“在函数内部首先申明所有变量”这一规则。最常见的做法是用一个`var`申明函数内部用到的所有变量：
```javascript
function foo() {
    var
        x = 1, // x初始化为1
        y = x + 1, // y初始化为2
        z, i; // z和i为undefined
    // 其他语句:
    for (i=0; i<100; i++) {
        ...
    }
}
```

建议使用let申明变量，避免var申明变量时带来的隐患。
##### 全局作用域
不在任何函数内定义的变量就具有全局作用域。实际上，JavaScript默认有一个全局对象`window`，全局作用域的变量实际上被绑定到`window`的一个属性：
```javascript
var course = 'Learn JavaScript';
console.log(course); // 'Learn JavaScript'
console.log(window.course); // 'Learn JavaScript'
```

因此，直接访问全局变量`course`和访问`window.course`是完全一样的。

你可能猜到了，由于函数定义有两种方式，以变量方式`var foo = function () {}`定义的函数实际上也是一个全局变量，因此，顶层函数的定义也被视为一个全局变量，并绑定到`window`对象：
```javascript
function foo() {
    alert('foo');
}

foo(); // 直接调用foo()
window.foo(); // 通过window.foo()调用
```

进一步大胆地猜测，我们每次直接调用的`alert()`函数其实也是`window`的一个变量：

这说明JavaScript实际上只有一个全局作用域。任何变量（函数也视为变量），如果没有在当前函数作用域中找到，就会继续往上查找，最后如果在全局作用域中也没有找到，则报`ReferenceError`错误。
##### 名字空间
全局变量会绑定到`window`上，不同的JavaScript文件如果使用了相同的全局变量，或者定义了相同名字的顶层函数，都会造成命名冲突，并且很难被发现。

减少冲突的一个方法是把自己的所有变量和函数全部绑定到一个全局变量中。例如：
```javascript
// 唯一的全局变量MYAPP:
let MYAPP = {};

// 其他变量:
MYAPP.name = 'myapp';
MYAPP.version = 1.0;

// 其他函数:
MYAPP.foo = function () {
    return 'foo';
};
```

把自己的代码全部放入唯一的名字空间`MYAPP`中，会大大减少全局变量冲突的可能。

许多著名的JavaScript库都是这么干的：jQuery，YUI，underscore等等。

##### 局部作用域
由于JavaScript的变量作用域实际上是函数内部，我们在`for`循环等语句块中是无法定义具有局部作用域的变量的：
```javascript
function foo() {
    for (var i=0; i<100; i++) {
        //
    }
    i += 100; // 仍然可以引用变量i
}
```

为了解决块级作用域，ES6引入了新的关键字`let`，用`let`替代`var`可以申明一个块级作用域的变量：
```javascript
function foo() {
    let sum = 0;
    for (let i=0; i<100; i++) {
        sum += i;
    }
    // SyntaxError:
    i += 1;
}
```

##### 常量
由于`var`和`let`申明的是变量，如果要申明一个常量，在ES6之前是不行的，我们通常用全部大写的变量来表示“这是一个常量，不要修改它的值”：
```javascript
let PI = 3.14;
```

ES6标准引入了新的关键字`const`来定义常量，`const`与`let`都具有块级作用域：
```javascript
const PI = 3.14;
PI = 3; // 某些浏览器不报错，但是无效果！
PI; // 3.14
```

##### 解构赋值
从ES6开始，JavaScript引入了解构赋值，可以同时对一组变量进行赋值。

什么是解构赋值？我们先看看传统的做法，如何把一个数组的元素分别赋值给几个变量：
```javascript
let array = ['hello', 'JavaScript', 'ES6'];
let x = array[0];
let y = array[1];
let z = array[2];
```

如果数组本身还有嵌套，也可以通过下面的形式进行解构赋值，注意嵌套层次和位置要保持一致：

```javascript
let [x, [y, z]] = ['hello', ['JavaScript', 'ES6']];
x; // 'hello'
y; // 'JavaScript'
z; // 'ES6'
```

解构赋值还可以忽略某些元素：

```javascript
let [, , z] = ['hello', 'JavaScript', 'ES6']; // 忽略前两个元素，只对z赋值第三个元素
z; // 'ES6'
```

如果需要从一个对象中取出若干属性，也可以使用解构赋值，便于快速获取对象的指定属性。
对一个对象进行解构赋值时，同样可以直接对嵌套的对象属性进行赋值，只要保证对应的层次是一致的：
```javascript
let person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678',
    school: 'No.4 middle school',
    address: {
        city: 'Beijing',
        street: 'No.1 Road',
        zipcode: '100001'
    }
};
let {name, address: {city, zip}} = person;
name; // '小明'
city; // 'Beijing'
zip; // undefined, 因为属性名是zipcode而不是zip
// 注意: address不是变量，而是为了让city和zip获得嵌套的address对象的属性:
address; // Uncaught ReferenceError: address is not defined
```

使用解构赋值对对象属性进行赋值时，如果对应的属性不存在，变量将被赋值为`undefined`，这和引用一个不存在的属性获得`undefined`是一致的。如果要使用的变量名和属性名不一致，可以用下面的语法获取：
```javascript
let person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678',
    school: 'No.4 middle school'
};

// 把passport属性赋值给变量id:
let {name, passport:id} = person;
name; // '小明'
id; // 'G-12345678'
// 注意: passport不是变量，而是为了让变量id获得passport属性:
passport; // Uncaught ReferenceError: passport is not defined
```

解构赋值还可以使用默认值，这样就避免了不存在的属性返回`undefined`的问题：
```javascript
let person = {
    name: '小明',
    age: 20,
    gender: 'male',
    passport: 'G-12345678'
};

// 如果person对象没有single属性，默认赋值为true:
let {name, single=true} = person;
name; // '小明'
single; // true
```

有些时候，如果变量已经被声明了，再次赋值的时候，正确的写法也会报语法错误：
```javascript
// 声明变量:
let x, y;
// 解构赋值:
{x, y} = { name: '小明', x: 100, y: 200};
// 语法错误: Uncaught SyntaxError: Unexpected token =
```

这是因为JavaScript引擎把`{`开头的语句当作了块处理，于是`=`不再合法。解决方法是用小括号括起来：
```javascript
({x, y} = { name: '小明', x: 100, y: 200});
```

##### 使用场景
解构赋值在很多时候可以大大简化代码。例如，交换两个变量`x`和`y`的值，可以这么写，不再需要临时变量：
```javascript
let x=1, y=2;
[x, y] = [y, x]
```

快速获取当前页面的域名和路径：
```javascript
let {hostname:domain, pathname:path} = location;
```

如果一个函数接收一个对象作为参数，那么，可以使用解构直接把对象的属性绑定到变量中。例如，下面的函数可以快速创建一个`Date`对象：
```javascript
function buildDate({year, month, day, hour=0, minute=0, second=0}) {
    return new Date(`${year}-${month}-${day} ${hour}:${minute}:${second}`);
}
```

它的方便之处在于传入的对象只需要`year`、`month`和`day`这三个属性：
```javascript
buildDate({ year: 2017, month: 1, day: 1 });
// Sun Jan 01 2017 00:00:00 GMT+0800 (CST)
```

也可以传入`hour`、`minute`和`second`属性：
```javascript
buildDate({ year: 2017, month: 1, day: 1, hour: 20, minute: 15 });
// Sun Jan 01 2017 20:15:00 GMT+0800 (CST)
```

使用解构赋值可以减少代码量，但是，需要在支持ES6解构赋值特性的现代浏览器中才能正常运行。目前支持解构赋值的浏览器包括Chrome，Firefox，Edge等。

### 廖雪峰教程 · 4函数/4.3 方法
##### 方法
在一个对象中绑定函数，称为这个对象的方法

在JavaScript中，对象的定义是这样的：
```javascript
let xiaoming = {
    name: '小明',
    birth: 1990
};
```

但是，如果我们给`xiaoming`绑定一个函数，就可以做更多的事情。比如，写个`age()`方法，返回`xiaoming`的年龄：
```javascript
let xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        let y = new Date().getFullYear();
        return y - this.birth;
    }
};

xiaoming.age; // function xiaoming.age()
xiaoming.age(); // 今年调用是25,明年调用就变成26了
```

绑定到对象上的函数称为方法，和普通函数也没啥区别，但是它在内部使用了一个`this`关键字，这个东东是什么？

在一个方法内部，`this`是一个特殊变量，它始终指向当前对象，也就是`xiaoming`这个变量。所以，`this.birth`可以拿到`xiaoming`的`birth`属性。

让我们拆开写：
```javascript
function getAge() {
    let y = new Date().getFullYear();
    return y - this.birth;
}

let xiaoming = {
    name: '小明',
    birth: 1990,
    age: getAge
};

xiaoming.age(); // 25, 正常结果
getAge(); // NaN
```

单独调用函数`getAge()`怎么返回了`NaN`？_请注意_，我们已经进入到了JavaScript的一个大坑里。

JavaScript的函数内部如果调用了`this`，那么这个`this`到底指向谁？

答案是，视情况而定！

如果以对象的方法形式调用，比如`xiaoming.age()`，该函数的`this`指向被调用的对象，也就是`xiaoming`，这是符合我们预期的。

如果单独调用函数，比如`getAge()`，此时，该函数的`this`指向全局对象，也就是`window`坑爹啊！

更坑爹的是，如果这么写：
```javascript
let fn = xiaoming.age; // 先拿到xiaoming的age函数
fn(); // NaN
```

也是不行的！要保证`this`指向正确，必须用`obj.xxx()`的形式调用！

由于这是一个巨大的设计错误，要想纠正可没那么简单。ECMA决定，在strict模式下让函数的`this`指向`undefined`，因此，在strict模式下，你会得到一个错误：
```javascript
'use strict';

let xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        let y = new Date().getFullYear();
        return y - this.birth;
    }
};

let fn = xiaoming.age;
fn(); // Uncaught TypeError: Cannot read property 'birth' of undefined
```

这个决定只是让错误及时暴露出来，并没有解决`this`应该指向的正确位置。

有些时候，喜欢重构的你把方法重构了一下：
```javascript
'use strict';

let xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        function getAgeFromBirth() {
            let y = new Date().getFullYear();
            return y - this.birth;
        }
        return getAgeFromBirth();
    }
};

xiaoming.age(); // Uncaught TypeError: Cannot read property 'birth' of undefined
```

结果又报错了！原因是`this`指针只在`age`方法的函数内指向`xiaoming`，在函数内部定义的函数，`this`又指向`undefined`了！（在非strict模式下，它重新指向全局对象`window`！）

修复的办法也不是没有，我们用一个`that`变量首先捕获`this`：
```javascript
'use strict';

let xiaoming = {
    name: '小明',
    birth: 1990,
    age: function () {
        let that = this; // 在方法内部一开始就捕获this
        function getAgeFromBirth() {
            let y = new Date().getFullYear();
            return y - that.birth; // 用that而不是this
        }
        return getAgeFromBirth();
    }
};

xiaoming.age(); // 25
```

用`let that = this;`，你就可以放心地在方法内部定义其他函数，而不是把所有语句都堆到一个方法中。
##### apply
虽然在一个独立的函数调用中，根据是否是strict模式，`this`指向`undefined`或`window`，不过，我们还是可以控制`this`的指向的！

要指定函数的`this`指向哪个对象，可以用函数本身的`apply`方法，它接收两个参数，第一个参数就是需要绑定的`this`变量，第二个参数是`Array`，表示函数本身的参数。

用`apply`修复`getAge()`调用：
```javascript
function getAge() {
    let y = new Date().getFullYear();
    return y - this.birth;
}

let xiaoming = {
    name: '小明',
    birth: 1990,
    age: getAge
};

xiaoming.age(); // 25
getAge.apply(xiaoming, []); // 25, this指向xiaoming, 参数为空
```

另一个与`apply()`类似的方法是`call()`，唯一区别是：
- `apply()`把参数打包成`Array`再传入；
- `call()`把参数按顺序传入。

比如调用`Math.max(3, 5, 4)`，分别用`apply()`和`call()`实现如下：
```javascript
Math.max.apply(null, [3, 5, 4]); // 5
Math.max.call(null, 3, 5, 4); // 5
```

对普通函数调用，我们通常把`this`绑定为`null`。
##### 装饰器
利用`apply()`，我们还可以动态改变函数的行为。

JavaScript的所有对象都是动态的，即使内置的函数，我们也可以重新指向新的函数。

现在假定我们想统计一下代码一共调用了多少次`parseInt()`，可以把所有的调用都找出来，然后手动加上`count += 1`，不过这样做太傻了。最佳方案是用我们自己的函数替换掉默认的`parseInt()`

### 廖雪峰教程 · 4函数/4.4 高阶函数
高阶函数英文叫Higher-order function。那么什么是高阶函数？

JavaScript的函数其实都指向某个变量。既然变量可以指向函数，函数的参数能接收变量，那么一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数。

一个最简单的高阶函数：
```javascript
function add(x, y, f) {
    return f(x) + f(y);
}
```

当我们调用`add(-5, 6, Math.abs)`时，参数`x`，`y`和`f`分别接收`-5`，`6`和函数`Math.abs`，根据函数定义，我们可以推导计算过程为：
```text
x = -5;
y = 6;
f = Math.abs;
f(x) + f(y) ==> Math.abs(-5) + Math.abs(6) ==> 11;
return 11;
```

### 廖雪峰教程 · 4函数/4.5 闭包
##### 闭包
##### 函数作为返回值
高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。

我们来实现一个对`Array`的求和。通常情况下，求和的函数是这样定义的：
```javascript
function sum(arr) {
    return arr.reduce(function (x, y) {
        return x + y;
    });
}

sum([1, 2, 3, 4, 5]); // 15
```

但是，如果不需要立刻求和，而是在后面的代码中，根据需要再计算怎么办？可以不返回求和的结果，而是返回求和的函数！

```javascript
function lazy_sum(arr) {
    let sum = function () {
        return arr.reduce(function (x, y) {
            return x + y;
        });
    }
    return sum;
}
```

当我们调用`lazy_sum()`时，返回的并不是求和结果，而是求和函数：
```javascript
let f = lazy_sum([1, 2, 3, 4, 5]); // function sum()
```

调用函数`f`时，才真正计算求和的结果：
```javascript
f(); // 15
```

在这个例子中，我们在函数`lazy_sum`中又定义了函数`sum`，并且，内部函数`sum`可以引用外部函数`lazy_sum`的参数和局部变量，当`lazy_sum`返回函数`sum`时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力。

请再注意一点，当我们调用`lazy_sum()`时，每次调用都会返回一个新的函数，即使传入相同的参数：
```javascript
let f1 = lazy_sum([1, 2, 3, 4, 5]);
let f2 = lazy_sum([1, 2, 3, 4, 5]);
f1 === f2; // false
```

`f1()`和`f2()`的调用结果互不影响。
##### 闭包
注意到返回的函数在其定义内部引用了局部变量`arr`，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。

另一个需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了`f()`才执行。我们来看一个例子：
```javascript
function count() {
    let arr = [];
    for (var i=1; i<=3; i++) {
        arr.push(function () {
            return i * i;
        });
    }
    return arr;
}

let results = count();
let [f1, f2, f3] = results;
```

在上面的例子中，每次循环，都创建了一个新的函数，然后，把创建的3个函数都添加到一个`Array`中返回了。

你可能认为调用`f1()`，`f2()`和`f3()`结果应该是`1`，`4`，`9`，但实际结果是：
```javascript
f1(); // 16
f2(); // 16
f3(); // 16
```

全部都是`16`！原因就在于返回的函数引用了用`var`定义的变量`i`，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量`i`已经变成了`4`，因此最终结果为`16`。

返回闭包时牢记的一点就是：返回函数不要引用任何循环变量，或者后续会发生变化的变量。

如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变：
```javascript
function count() {
    let arr = [];
    for (var i=1; i<=3; i++) {
        arr.push((function (n) {
            return function () {
                return n * n;
            }
        })(i));
    }
    return arr;
}

let [f1, f2, f3] = count();

f1(); // 1
f2(); // 4
f3(); // 9
```

注意这里用了一个“创建一个匿名函数并立刻执行”的语法：
```javascript
(function (x) {
    return x * x;
})(3); // 9
```

理论上讲，创建一个匿名函数并立刻执行可以这么写：
```javascript
function (x) { return x * x } (3);
```

但是由于JavaScript语法解析的问题，会报SyntaxError错误，因此需要用括号把整个函数定义括起来：
```javascript
(function (x) { return x * x }) (3);
```

通常，一个立即执行的匿名函数可以把函数体拆开，一般这么写：
```javascript
(function (x) {
    return x * x;
})(3);
```

另一个方法是把循环变量`i`用`let`定义在`for`循环体中，`let`作用域决定了在每次循环时都会绑定新的`i`：
```javascript
function count() {
    let arr = [];
    for (let i=1; i<=3; i++) {
        arr.push(function () {
            return i * i;
        });
    }
    return arr;
}
```

但如果`i`定义在`for`循环外面，则仍然是错误的：
```javascript
function count() {
    let arr = [];
    let i;
    for (i=1; i<=3; i++) {
        arr.push(function () {
            return i * i;
        });
    }
    return arr;
}
```

因此，最好的办法还是返回函数不要引用任何循环变量。

说了这么多，难道闭包就是为了返回一个函数然后延迟执行吗？

当然不是！闭包有非常强大的功能。在面向对象的程序设计语言里，比如Java和C++，要在对象内部封装一个私有变量，可以用`private`修饰一个成员变量。

在没有`class`机制，只有函数的语言里，借助闭包，同样可以封装一个私有变量。我们用JavaScript创建一个计数器：
```javascript
function create_counter(initial) {
    let x = initial || 0;
    return {
        inc: function () {
            x += 1;
            return x;
        }
    }
}
```

它用起来像这样：
```javascript
let c1 = create_counter();
c1.inc(); // 1
c1.inc(); // 2
c1.inc(); // 3

let c2 = create_counter(10);
c2.inc(); // 11
c2.inc(); // 12
c2.inc(); // 13
```

在返回的对象中，实现了一个闭包，该闭包携带了局部变量`x`，并且，从外部代码根本无法访问到变量`x`。换句话说，闭包就是携带状态的函数，并且它的状态可以完全对外隐藏起来。

也就是说，闭包实现了一种类似于“类”的私有变量的效果，在包装函数为节流防抖函数时，对原函数的处理用的变量就会存在于返回的这个函数的闭包中。

### 廖雪峰教程 · 4函数/4.6 箭头函数
##### 箭头函数
ES6标准新增了一种新的函数：箭头函数（Arrow Function）。

为什么叫箭头函数？因为它的定义用的就是一个箭头：
```javascript
x => x * x
```

上面的箭头函数相当于：
```javascript
function (x) {
    return x * x;
}
```

箭头函数相当于匿名函数，并且简化了函数定义。箭头函数有两种格式，一种像上面的，只包含一个表达式，连`{ ... }`和`return`都省略掉了。还有一种可以包含多条语句，这时候就不能省略`{ ... }`和`return`：
```javascript
x => {
    if (x > 0) {
        return x * x;
    }
    else {
        return - x * x;
    }
}
```

如果参数不是一个，就需要用括号`()`括起来：
```javascript
// 两个参数:
(x, y) => x * x + y * y

// 无参数:
() => 3.14

// 可变参数:
(x, y, ...rest) => {
    let i, sum = x + y;
    for (i=0; i<rest.length; i++) {
        sum += rest[i];
    }
    return sum;
}
```

如果要返回一个对象，就要注意，如果是单表达式，这么写的话会报错：
```javascript
// SyntaxError:
x => { foo: x }
```

因为和函数体的`{ ... }`有语法冲突，所以要改为：
```javascript
// ok:
x => ({ foo: x })
```

##### this
箭头函数看上去是匿名函数的一种简写，但实际上，箭头函数和匿名函数有个明显的区别：箭头函数内部的`this`是词法作用域，由上下文确定。

回顾前面的例子，由于JavaScript函数对`this`绑定的错误处理，下面的例子无法得到预期结果：
```javascript
let obj = {
    birth: 1990,
    getAge: function () {
        let b = this.birth // 1990
        let fn = function () {
            console.log(this)

            return new Date().getFullYear() - this.birth
            // this指向window或undefined
        }
        return fn()
    },
}

function test() {
    let b = this.birth // 1990
    let fn = function () {
        console.log(this)

        return new Date().getFullYear() - this.birth
        // this指向window或undefined
    }
    return fn()
}

console.log(obj.getAge())
// NaN

// 这里的obj.getAge()本质是一个在全局对象的window下的，this的指向也是window
// 这和直接直接调用test()本质是一样的，只不过使用了对象的写法，感觉很迷惑
console.log(test())
// NaN
```

现在，箭头函数完全修复了`this`的指向，`this`总是指向词法作用域，也就是外层调用者`obj`：
```javascript
let obj = {
    birth: 1990,
    getAge: function () {
        let b = this.birth; // 1990
        let fn = () => new Date().getFullYear() - this.birth;
        // this指向obj对象
        return fn();
    }
};
obj.getAge(); // 25
```

如果使用箭头函数，以前的那种hack写法：
```javascript
let that = this;
```

就不再需要了。

由于`this`在箭头函数中已经按照词法作用域绑定了，所以，用`call()`或者`apply()`调用箭头函数时，无法对`this`进行绑定，即传入的第一个参数被忽略：
```javascript
let obj = {
    birth: 1990,
    getAge: function (year) {
        let b = this.birth; // 1990
        let fn = (y) => y - this.birth; // this.birth仍是1990
        return fn.call({birth:2000}, year);
    }
};
obj.getAge(2015); // 25
```

### 廖雪峰教程 · 4函数/4.7 标签函数
##### 标签函数
前面我们介绍了[模板字符串](https://liaoxuefeng.com/books/javascript/quick-start/string/index.html)，它可以非常方便地引用变量，并合并出最终的字符串：

对于模板字符串，除了方便引用变量构造字符串外，还有一种更强大的功能，即可以使用标签函数（Tag Function）。

什么是标签函数？让我们看一个例子：
```javascript
sql`SELECT * FROM users WHERE email=${email} AND password=${password}`
```

模板字符串前面以`sql`开头，实际上这是一个标签函数，上述语法会自动转换为对`sql()`函数的调用。我们关注的是，传入`sql()`函数的参数是什么。

`sql()`函数实际上接收两个参数：

第一个参数`strings`是一个字符串数组，它是`["SELECT * FROM users WHERE email=", " AND password=", ""]`，即除去`${xxx}`剩下的字符组成的数组；

第二个参数`...exps`是一个可变参数，它接收的也是一个数组，但数组的内容是由模板字符串里所有的`${xxx}`的实际值组成，即`["test@example.com", "hello123"]`，因为解析`${email}`得到`"test@example.com"`，解析`${password}`得到`"hello123"`。

标签函数`sql()`实际上是一个普通函数，我们在内部把`strings`拼接成一个SQL字符串，把`...exps`作为参数，就可以实现一个安全的SQL查询，并返回查询结果。此处并没有真正的数据库连接，因此返回一个固定的Object。

标签函数和普通函数的定义区别仅仅在于参数，如果我们想对数据库进行修改，完全可以定义一个标签函数如下：

```javascript
function update(strings, ...exps) {
    let sql = strings.join('?');
    // 执行数据库更新
    // TODO:
}
```

函数调用可以简化为带标签的模板字符串：
```javascript
let id = 123;
let age = 21;
let score = 'A';

update`UPDATE users SET age=${age}, score=${score} WHERE id=${id}`;
```
