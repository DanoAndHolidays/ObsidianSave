# 07 函数、闭包、作用域与this 🍂
> Last Format Time：9/16/2026 19:24:51

[[JavaScript 作用域]]

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
## 函数/函数进阶
### new function
它实际上是通过运行时通过参数传递过来的字符串创建的。
`new Function` 允许我们将任意字符串变为函数。例如，我们可以从服务器接收一个新的函数并执行它

### setTimeOut()
`setTimeout` 允许我们将函数推迟到一段时间间隔之后再执行。

参数说明：

- `func|code` 想要执行的函数或代码字符串。一般传入的都是函数。由于某些历史原因，支持传入代码字符串，但是不建议这样做。
- `delay` 执行前的延时，以毫秒为单位（1000 毫秒 = 1 秒），默认值是 0；
- `arg1`，`arg2`… 要传入被执行函数（或代码字符串）的参数列表（IE9 以下不支持）

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

### setaInterval()
`setInterval` 允许我们重复运行一个函数，从一段时间间隔之后开始运行，之后以该时间间隔连续重复运行该函数。`setInterval` 方法和 `setTimeout` 的语法相同

在大多数浏览器中，包括 Chrome 和 Firefox，在显示 `alert/confirm/prompt` 弹窗时，内部的定时器仍旧会继续“嘀嗒”。

所以，在运行上面的代码时，如果在一定时间内没有关掉 `alert` 弹窗，那么在你关闭弹窗后，下一个 `alert` 会立即显示。两次 `alert` 之间的时间间隔将小于 2 秒。

使用嵌套的setTimeout，其效果和setInterval一样，但更加灵活

```javascript
let timerId = setTimeout(function tick () {
    console.log("tick");
    timerId = setTimeout(tick,1000)
},1000)
```

这**两个方法并不在 JavaScript 的规范**中。但是大多数运行环境都有内建的调度程序，并且提供了这些方法。目前来讲，所有浏览器以及 Node.js 都支持这两个方法。

### 函数绑定
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

##### 使用函数包装器
在要回调的函数外套一层函数，在外部的函数中调用。这里的user成为了箭头函数的闭包，闭包保留的是词法环境中的绑定，不是某一刻值的副本

```javascript
setTimeout(function () { user.eat() }, 1000);//dano is eating!
setTimeout(() => user.eat(), 1000);//dano is eating!
```

看起来不错，但是我们的代码结构中出现了一个小漏洞。如果在 `setTimeout` 触发之前（有一秒的延迟！）`user` 的值改变了怎么办？那么，突然间，它将调用错误的对象！详见[[闭包是绑定]]

##### 使用bind
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
创建一个包装器（wrapper）函数，该函数增加了缓存功能。

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

### 手动实现call、apply与bind
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

### 函数参数Params和arguments对象
在 JavaScript 中，`arguments` 和**函数参数（params）** 都与函数接收的输入有关，但它们的本质、用法和特性有显著区别：

- **函数参数（params）** 是在函数定义时显式声明的变量，用于接收函数调用时传递的参数。
  例如：`function fn(a, b) { ... }` 中的 `a` 和 `b` 就是参数（params）。
- **`arguments` 对象** 是函数内部的一个**类数组对象**，自动包含函数调用时传递的所有实际参数，无论函数定义时是否声明了对应参数。仅在非箭头函数中存在（箭头函数没有 `arguments` 对象）。

| 特性               | 函数参数（params）                          | `arguments` 对象                          |
|--------------------|--------------------------------------------|------------------------------------------|
| **声明方式**       | 函数定义时显式声明（如 `a, b`）             | 函数内部自动生成，无需声明                |
| **数据类型**       | 普通变量（按声明的类型接收值）              | 类数组对象（有 `length`，可通过索引访问）  |
| **与实参的关系**   | 数量固定（由声明决定），多余实参无法直接访问 | 包含所有实参（数量由调用时传递的参数决定） |
| **箭头函数支持**   | 支持                                        | 不支持（箭头函数中无 `arguments`）        |
| **修改影响**       | 修改参数不会影响 `arguments`（非严格模式下有例外） | 修改 `arguments` 可能影响参数（非严格模式） |
| **用途**           | 清晰接收指定参数，便于代码可读性            | 处理不确定数量的参数（如动态传参场景）    |

参数数量不匹配时：
- 实参数量 > 参数数量：参数只能接收前 N 个，剩余实参需通过 `arguments` 访问。
- 实参数量 < 参数数量：未被赋值的参数为 `undefined`，`arguments` 长度等于实参数量。

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

```javascript
function fn(a, b) {
  console.log(a, b); // 1, undefined（实参不足）
  console.log(arguments.length); // 1（仅1个实参）
}

fn(1); // 只传递1个实参
```

严格模式与非严格模式的差异
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

由于 `arguments` 在箭头函数中不支持，ES6 引入了**剩余参数（`...rest`）**，它是更优的替代方案：
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

### rest和spread
在 JavaScript 中，很多内建函数都支持传入任意数量的参数。
例如：
- `Math.max(arg1, arg2, ..., argN)` —— 返回参数中的最大值。
- `Object.assign(dest, src1, ..., srcN)` —— 依次将属性从 `src1..N` 复制到 `dest`。
- ……等。

在 JavaScript 中，无论函数是如何定义的，你都可以在调用它时传入==任意数量的参数==

我们可以在函数定义中声明一个数组来收集参数：`...变量名`，这将会声明一个数组并指定其名称，其中存有剩余的参数。必须放到**参数列表的末尾**

这三个点的语义就是“收集剩余的参数并存进指定数组中”

有一个名为 `arguments` 的特殊类数组对象可以在函数中被访问，该对象以参数在参数列表中的索引作为键，存储所有参数。尽管 `arguments` 是一个==类数组==，也是可迭代对象，但它终究不是数组。它不支持数组方法，因此我们不能调用 `arguments.map(...)` 等方法。如果我们在箭头函数中访问 `arguments`，访问到的 `arguments` 并不属于箭头函数，而是属于箭头函数外部的“普通”函数

**Spread 语法**它看起来和 rest 参数很像，也使用 `...`，但是二者的用途完全相反。
当在函数调用中使用 `...arr` 时，它会把可迭代的 `arr` “展开”到参数列表中 [[06 集合与迭代 🍂]]

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

使用 `...` 来进行拷贝数组和对象：
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

这种方式比使用 `let arrCopy = Object.assign([], arr)` 复制数组，或使用 `let objCopy = Object.assign({}, obj)` 复制对象来说更为简便。只要情况允许，我们倾向于使用它。

注意事项：

1. **仅适用于可迭代对象**：扩展运算符只能作用于可迭代对象（如数组、字符串、`Set`），不能直接用于普通对象（但对象属性展开是特殊语法，见示例 2）。
2. **浅拷贝限制**：对于嵌套的引用类型（对象、数组），扩展运算符仅复制引用，修改会影响原数据。
3. **不能单独用于函数参数之外的场景**：例如 `const a = ...[1,2,3];` 是错误的，必须在数组、对象或函数参数中使用。

当我们在代码中看到 `"..."` 时，它要么是 rest 参数，要么是 spread 语法。
有一个简单的方法可以区分它们：
- 若 `...` 出现在函数参数列表的最后，那么它就是 rest 参数，它会把参数列表中剩余的参数收集到一个数组中。
- 若 `...` 出现在函数调用或类似的表达式中，那它就是 spread 语法，它会把一个数组展开为列表。

使用场景：
- Rest 参数用于创建可接受任意数量参数的函数。
- Spread 语法用于将数组传递给通常需要含有许多参数的函数。

我们可以使用这两种语法轻松地互相转换列表与参数数组。
旧式的 `arguments`（类数组且可迭代的对象）也依然能够帮助我们获取函数调用中的所有参数。

---
## 其他
### 全局对象
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

##### polyfills（垫片）
如果浏览器版本过旧，存在代码的缺失，可以自行添加代码

### 函数对象
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

还有另一个内建属性 “length”，它返回函数入参的个数，rest 参数不参与计数（这个内建属性length在函数柯里化的时候有用到）

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

### 命名函数表达式（NFE，Named Function Expression）
指带有名字的函数表达式的术语。
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

### 箭头函数
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

 箭头函数的这种特性可以将其==视为外层函数的一部分==，箭头函数“的”this，就是外层函数的this：

- 没有 `this`
- 没有 `arguments`
- 不能使用 `new` 调用，因为它没有`this`，无法将创建的空对象绑定到this上[[构造函数与New]]
- 它们也没有 `super`，但目前我们还没有学到它。我们将在 [类继承](https://zh.javascript.info/class-inheritance) 一章中学习它。

### 解构赋值
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
对象的解构与数组有一个重要的不同。==数组==的元素是==按次序排==列的，变量的取值由它的位置决定；而对象的属性==没有次序==，==变量==必须与==属性==同名，才能取到正确的值。

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

下面第二个 `p` ==是模式，不是变量==，因此不会被赋值。如果 `p` 也要作为变量赋值，可以写成下面这样。

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

### 变量作用域
[[JavaScript 作用域]]

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

### 闭包
是指一个函数可以记住其外部变量并可以访问这些变量。

函数调用完成后，会将词法环境和其中的所有变量从内存中删除。因为现在没有任何对它们的引用了。与 JavaScript 中的任何其他对象一样，词法环境仅在==可达==时才会被保留在内存中。

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
处于非严格模式下，要绑定的`this`指定为`null`或`undefined`时会自动替换为全局对象，原始值则会被包装

```javascript
function foo() {
  console.log(this);
}
foo.call(null); // 浏览器中输出：Window 对象
foo.call(undefined); // 浏览器中输出：Window 对象
```

在非严格模式中，若 `call` 的 `thisArg` 是**原始值**（如数字、字符串、布尔值），JavaScript 会自动将其**包装为对应的对象类型**（`Number`、`String`、`Boolean`），再绑定为 `this`。

在严格模式（通过 `"use strict"` 声明）中，`call` 的 `thisArg` 会**直接绑定**，即使是原始值，也不会被包装为对象。

严格模式：
```javascript
"use strict"; function test() {  console.log(this);} test.call(2);// 2
```

非严格模式：
```javascript
function test() {  console.log(this);} test.call(2);// Number {2}
```

这种差异是 JavaScript 为了兼容历史行为（非严格模式）和更严格的语法规范（严格模式）而设计的

```ts
import { getData } from "./index.js";

// 在严格模式下，确实裸函数调用的this为undefined

// 非严格模式为 <ref *1> Object [global] {
//   global: [Circular *1],
//   clearImmediate: [Function: clearImmediate],
//   setImmediate: [Function: setImmediate] {
//     [Symbol(nodejs.util.promisify.custom)]: [Getter]
//   },
//   clearInterval: [Function: clearInterval],
//   clearTimeout: [Function: clearTimeout],
//   setInterval: [Function: setInterval],
//   setTimeout: [Function: setTimeout] {
//     [Symbol(nodejs.util.promisify.custom)]: [Getter]
//   },
//   queueMicrotask: [Function: queueMicrotask],
//   structuredClone: [Function: structuredClone],
//   atob: [Function: atob],
//   btoa: [Function: btoa],
//   performance: [Getter/Setter],
//   fetch: [Function: fetch],
//   navigator: [Getter],
//   crypto: [Getter]
// }
function test(string = "test") {
    console.log(string, this)
}

test()
```

### 定义函数
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

函数体内部的语句在执行时，一旦执行到`return`时，函数就执行完毕，并将结果返回。因此，函数内部通过条件判断和循环可以实现非常复杂的逻辑。

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

上述两种定义==完全等价==，注意第二种方式按照完整语法需要在函数体末尾加一个`;`，表示赋值语句结束。

### 调用函数
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

### 小心你的return语句
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

要小心了，由于JavaScript引擎在行末自动添加分号的机制，上面的代码实际上变成了：
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

### 变量作用域
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

### 变量提升
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

### 全局作用域
不在任何函数内定义的变量就具有全局作用域。实际上，JavaScript默认有一个全局对象`window`，全局作用域的变量实际上被绑定到`window`的一个属性：
```javascript
var course = 'Learn JavaScript';
console.log(course); // 'Learn JavaScript'
console.log(window.course); // 'Learn JavaScript'
```

因此，直接访问全局变量`course`和访问`window.course`是完全一样的。

这说明JavaScript实际上只有一个全局作用域。任何变量（函数也视为变量），如果没有在当前函数作用域中找到，就会继续往上查找，最后如果在全局作用域中也没有找到，则报`ReferenceError`错误。

### 名字空间
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

### 局部作用域
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

### 标签函数
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
