# 05 Object对象
> Last Format Time：8/11/2026 21:45:37

本笔记由两个 JavaScript 教程目录中的同主题内容合并而成；全部旧知识保留在“旧笔记知识全集（按来源保留）”中，并由导航逐项索引。

---
## 当前前端开发关键要点

> [!important] 学习优先级：P0
> - 掌握属性访问、枚举、描述符和 `Object.keys/values/entries`，明确自有属性与继承属性。
> - 对象展开与 `Object.assign` 都是浅拷贝；深拷贝优先评估 `structuredClone` 的适用范围。
> - 状态管理与 React 更新中避免直接突变对象；同时注意循环引用、序列化限制和原型污染风险。

---
## 知识点导航
### [[05 Object对象#现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象|现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象]]
- Object API
- 对象的keys，values，entries

### [[05 Object对象#现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象的属性配置|现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象的属性配置]]
- 对象属性标志（数据描述符
- 属性的访问器属性（存取描述符）

### [[05 Object对象#现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象的循环引用与深克隆 ⌚️|现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象的循环引用与深克隆 ⌚️]]
- 对象的循环引用
- 深拷贝与浅拷贝

### [[05 Object对象#廖雪峰教程 · 3快速入门/3.5 对象|廖雪峰教程 · 3快速入门/3.5 对象]]
- 对象

---
## 现代前端补充与纠错

> [!info] 修改标记
> - *【修正】*：旧教程中错误、过时或容易误导的内容。
> - *【补充】*：旧教程未覆盖、但当前前端开发需要掌握的内容。
> - *【修正代码】*：替换或校正了旧代码示例。

> [!warning] 下方保留历史上下文；深克隆、垃圾回收、属性判断和错误代码已直接修正或就地标成 *【修正】*。

### 自有属性与复制
- *【修正】* 判断自有属性优先 `Object.hasOwn(obj, key)`；它可用于无原型对象，也不受对象自身覆盖 `hasOwnProperty` 的影响。
- *【补充】* 展开语法与 `Object.assign` 只复制可枚举自有属性，属于浅复制；访问器可能在复制时被求值，属性描述符和原型不会被完整保留。
- *【补充】* 合并不可信对象时需防范 `__proto__`、`constructor`、`prototype` 等原型污染入口。

### `structuredClone` 的真实边界
- *【修正】* `structuredClone` 属于 Web/宿主环境的结构化克隆 API，不应简单归为“ES2022 语法”。
- *【补充】* 它支持循环引用、`Map`、`Set`、`ArrayBuffer` 等结构，但函数、DOM 节点等不可克隆值会抛出 `DataCloneError`，不是静默忽略。
- *【补充】* 它不会完整保留自定义原型、属性描述符、getter/setter 等对象语义；使用前应确认数据模型。
- *【修正】* 现代追踪式垃圾回收器能回收整体不可达的循环引用。循环引用本身不等于内存泄漏；持续可达的监听器、定时器、缓存和闭包才更常见。

### 深克隆选择
- *【修正】* JSON 往返会丢失 `undefined`、函数、Symbol，并改变日期、非有限数值等，不是通用深克隆。
- *【修正】* 手写递归示例通常无法完整处理原型、描述符、Symbol 键、Map/Set、TypedArray 与循环引用。生产代码应先确认是否真的需要深克隆，再按数据类型选择 `structuredClone`、领域映射或成熟库。
---
## 旧笔记知识全集（按来源保留）
### 现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象
##### Object API
**一、对象创建方法**

1. **`Object.create(proto, [propertiesObject])`**
   创建一个新对象，指定其原型对象和属性。

```javascript
   // 以 obj 为原型创建新对象
   const obj = { a: 1 };
   const newObj = Object.create(obj);
   console.log(newObj.a); // 1（继承自原型）
   console.log(Object.getPrototypeOf(newObj) === obj); // true

   // 同时定义属性
   const customObj = Object.create(null, {
     b: { value: 2, writable: true } // 可写属性
   });
```

2. **`Object.assign(target, ...sources)`**
   将源对象的可枚举属性复制到目标对象，返回目标对象（==浅拷贝==）。

```javascript
   const target = { a: 1 };
   const source1 = { b: 2 };
   const source2 = { c: 3 };

   Object.assign(target, source1, source2);
   console.log(target); // { a: 1, b: 2, c: 3 }

   // 浅拷贝示例（嵌套对象仅复制引用）
   const obj = { info: { name: "Alice" } };
   const copy = Object.assign({}, obj);
   copy.info.name = "Bob";
   console.log(obj.info.name); // "Bob"（原对象被修改）
```

	通过这种方式也可以实现添加一个方法的目的：
```js
// 方式2：后期通过点语法/方括号添加（动态添加）
obj2.say = function() { console.log("说话"); };
obj2["run"] = () => console.log("跑步"); // 方括号支持动态键名

// 方式3：通过 Object.assign 批量添加
Object.assign(obj3, {
  jump() { console.log("跳跃"); }
});
```

3. 使用对象字面量创建，这和new出来的是一样的，就是个语法糖：
```javascript
// 基础字面量创建
const person = {
  name: "张三", // 属性键值对
  age: 20,
  sayHi: function() { // 方法
    console.log(`Hi, ${this.name}`);
  }
};
```

4. 使用关键字`new`，调用构造函数：
```js
const obj = new Object();//（构造函数方式）
```

**二、属性描述与操作**

5. **`Object.defineProperty(obj, prop, descriptor)`**
   为对象定义或修改属性，并设置属性描述符（如是否可写、可枚举等）。与直接为一个对象的属性赋值(o.a = 3)不同，Object.defineProperty 可更为精确，拥有更多选项地为对象属性赋值

属性描述符拥有两种: 数据描述符与存取描述符[[对象的属性配置]]

```javascript
   const obj = {};
   Object.defineProperty(obj, "name", {
     value: "John",
     writable: false,       // 不可修改
     enumerable: true,      // 可枚举（可被 for...in 遍历）
     configurable: false    // 不可删除或修改描述符
   });

   obj.name = "Alice"; // 无效（严格模式下报错）
   console.log(obj.name); // "John"
```

2. **`Object.getOwnPropertyDescriptor(obj, prop)`**
   获取对象指定属性的描述符。

```javascript
   const obj = { age: 20 };
   const desc = Object.getOwnPropertyDescriptor(obj, "age");
   console.log(desc);
   // {
   //   value: 20,
   //   writable: true,
   //   enumerable: true,
   //   configurable: true
   // }
```

3. **`Object.keys(obj)` / `Object.values(obj)` / `Object.entries(obj)`**
   - `keys`：返回对象自身==可枚举==属性的键名数组。  `Object.getOwnPropertyNames()`：列出==所有属性值(包括可枚举与不可枚举)==。在 `Object.defineProperty` 中的选项 `enumerable` 可定义属性是否可枚举
   - `values`：返回对象自身可枚举属性的键值数组。
   - `entries`：返回对象自身可枚举属性的 `[键, 值]` 数组。
```javascript
   const user = { name: "Bob", age: 30 };
   console.log(Object.keys(user)); // ["name", "age"]
   console.log(Object.values(user)); // ["Bob", 30]
   console.log(Object.entries(user)); // [["name", "Bob"], ["age", 30]]
```


**三、原型与继承**

1. **`Object.getPrototypeOf(obj)`**
   获取对象的原型（`__proto__` 的标准替代方法）。

```javascript
   const arr = [];
   console.log(Object.getPrototypeOf(arr) === Array.prototype); // true
```

2. **`Object.setPrototypeOf(obj, proto)`**
   设置对象的原型（谨慎使用，可能影响性能）。

```javascript
   const obj = {};
   const proto = { greet: () => "Hello" };
   Object.setPrototypeOf(obj, proto);
   console.log(obj.greet()); // "Hello"
```

3. **`Object.prototype.isPrototypeOf(obj)`**
   判断当前对象是否为目标对象的原型。

```javascript
const proto = {}
const obj = Object.create(proto)
console.log(proto.isPrototypeOf(obj)) // true

// console.log(obj instanceof proto) 会报错

class Preson {
    constructor(name) {
        this.name = name
    }
}

const p = new Preson('张三')
console.log(p instanceof Preson) // true
console.log(Preson.prototype.isPrototypeOf(p)) // true

```

![[Pasted image 20260412172138.png]]

**四、对象检查与比较**

1. **`Object.prototype.hasOwnProperty(prop)`**
   判断对象自身是否包含指定属性（==不包括继承的属性==）。

```javascript
   const obj = { a: 1 };
   console.log(obj.hasOwnProperty("a")); // true
   console.log(obj.hasOwnProperty("toString")); // false（继承自 Object）
```

2. **`Object.is(value1, value2)`**
   判断两个值是否严格相等（类似 `===`，但处理特殊值更准确）。

```javascript
   console.log(Object.is(1, 1)); // true
   console.log(Object.is(NaN, NaN)); // true（=== 会返回 false）
   console.log(Object.is(0, -0)); // false（=== 会返回 true）
```


**五、其他常用方法**

1. **`Object.freeze(obj)`**
   冻结对象：使其属性不可修改、删除，也不能添加新属性。

```javascript
   const obj = { a: 1 };
   Object.freeze(obj);
   obj.a = 2; // 无效
   delete obj.a; // 无效
   console.log(obj.a); // 1
```

2. **`Object.seal(obj)`**
   密封对象：属性不可删除，也不能添加新属性，但可修改现有属性的值。

```javascript
   const obj = { a: 1 };
   Object.seal(obj);
   obj.a = 2; // 有效
   delete obj.a; // 无效
   console.log(obj.a); // 2
```

3. **`Object.prototype.toString()`**
   返回对象的字符串表示（可用于准确判断数据类型）。

```javascript
   console.log(Object.prototype.toString.call(123)); // "[object Number]"
   console.log(Object.prototype.toString.call([])); // "[object Array]"
   console.log(Object.prototype.toString.call(null)); // "[object Null]"

   console.log(Object.prototype.toString(123)) // "[object Object]"
   console.log(Object.prototype.toString([])) // "[object Object]"
   console.log(Object.prototype.toString(null)) // "[object Object]"
```

直接调用 Object.prototype.toString(123) 时， 123 实际上和函数内部完全没有关系。在非严格模式下， 123 会被当作 this 传入，但实际上在函数内部并没有使用 this ，而是使用 Object.prototype 自己的方法。

```text
Object.prototype.toString(123)
```

这行代码中：

- 123 作为参数传入，但 函数体里根本没用这个参数
- 函数内部用的是 this ，也就是 Object.prototype 自己
- 123 只是被"白传"了

```text
const fn = Object.prototype.toString
fn(123)  // 同样是 123 被传进去当 this，但没用到
```

这其实是一个常见误区：以为传了参数就会用到，其实函数体里根本不理它。

**总结**
- 对象创建与复制：`Object.create()`、`Object.assign()`
- 属性操作：`defineProperty()`、`getOwnPropertyDescriptor()`、`keys()`/`values()`/`entries()`
- 原型管理：`getPrototypeOf()`、`setPrototypeOf()`、`isPrototypeOf()`
- 对象保护：`freeze()`（冻结）、`seal()`（密封）
- 类型判断：`toString()`（比 `typeof` 更准确）

这些方法是操作对象的基础，尤其在处理复杂对象结构或需要精确控制属性行为时非常有用。

##### 对象的keys，values，entries
对于普通对象，下列这些方法是可用的：
- [Object.keys(obj)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) —— 返回一个包含该对象所有的键的数组。
- [Object.values(obj)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Object/values) —— 返回一个包含该对象所有的值的数组。
- [Object.entries(obj)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Object/entries) —— 返回一个包含该对象所有 [key, value] 键值对的数组。

……但是请注意区别（比如说跟 map 的区别）：
|Map|Object|
|---|---|
|调用语法|`map.keys()`|`Object.keys(obj)`，而不是 `obj.keys()`|
|返回值|可迭代对象|“真正的”数组|

第二个区别是 `Object.*` 方法返回的是“真正的”数组对象，而不只是一个可迭代对象。
在 JavaScript 中，对象是所有复杂结构的基础。因此，我们可能有一个自己创建的对象，比如 `data`，并实现了它自己的 `data.values()` 方法。同时，我们依然可以对它调用 `Object.values(data)` 方法。

### 现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象的属性配置
##### 对象属性标志（数据描述符
对象属性（properties），除 **`value`** 外，还有三个特殊的特性（attributes），也就是所谓的“标志”：
- **`writable`** — 如果为 `true`，则值可以被修改，否则它是只可读的。
- **`enumerable`** — 如果为 `true`，则会被在循环中列出，否则不会被列出。
- **`configurable`** — 如果为 `true`，则此属性可以被删除，这些特性也可以被修改，否则不可以。

查看属性标志：
```javascript
const obj = {
    name: 'dano',
    age: 21,
    food:'orange',
}

let descriptor = Object.getOwnPropertyDescriptors(obj);
console.log(descriptor);

// {
//   name: {
//     value: 'dano',
//     writable: true,
//     enumerable: true,
//     configurable: true
//   },

//   age: {
//     value: 21,
//     writable: true,
//     enumerable: true,
//     configurable: true
//   },

//   food: {
//     value: 'orange',
//     writable: true,
//     enumerable: true,
//     configurable: true
//   }
// }
```

修改属性标志：使用修改属性标志的方法来创建的属性的标志均为false

```javascript
const obj = {
    name: 'dano',
    age: 21,
    food:'orange',
}

Object.defineProperty(obj, 'name', { value: 'daozhu' });
let descriptor = Object.getOwnPropertyDescriptors(obj);
console.log(obj.name);//daozhu

Object.defineProperty(obj, 'time', { value: 34 });
// time: { value: 34, writable: false, enumerable: false, configurable: false }
```

*8/11/26 【修正代码】原内容：属性描述符注释缺少右花括号且多出一个可执行的 `}`；修改点：补全注释并删除多余花括号。*

只读、枚举和可配置：只在严格模式下会出现 Errors

```javascript
const obj = {
    name: 'dano',
    age: 21,
    food:'orange',
}

Object.defineProperty(obj, 'name', { writable: false });
obj.name = 'daozhu';//不会报错
console.log(obj.name);//dano
```

通常，对象中内建的 `toString` 是不可枚举的，它不会显示在 `for..in` 中。但是如果我们添加我们自己的 `toString`，那么默认情况下它将显示在 `for..in` 中，如下所示.可以设置 `enumerable:false`。之后它就不会出现在 `for..in` 循环中了，就像内建的 `toString` 一样

```javascript
let user = {
    name: "John",
    toString() {
        return this.name;
    }
};

// 默认情况下，我们的两个属性都会被列出：
for (let key in user) console.log(key); // name, toString
Object.defineProperty(user, 'toString', { enumerable: false });
for (let key in user) console.log(key); // name
```

不可配置标志（`configurable:false`）有时会预设在内建对象和属性中。
不可配置的属性**不能被删除**，它的**标志（attribute）不能被修改**。

```javascript
let descriptor = Object.getOwnPropertyDescriptor(Math, 'PI');
alert(JSON.stringify(descriptor, null, 2));
/*
{
  "value": 3.141592653589793,
  "writable": false,
  "enumerable": false,
  "configurable": false
}
*/
```

属性变成不可配置是一条单行道。我们无法通过 `defineProperty` 再把它改回来。
**请注意：`configurable: false` 防止更改和删除属性标志，但是允许更改对象的值。**
这里的 `user.name` 是不可配置的，但是我们仍然可以更改它，因为它是可写的：
```javascript
let user = {
    name: "John"
};

Object.defineProperty(user, "name", {
    configurable: false
});

user.name = "Pete"; // 正常工作
delete user.name; // 不能删除

console.log(JSON.stringify(user,null,2));//{"name": "Pete"}
```

对于更改标志，有一个**小例外**：
对于不可配置的属性，我们可以将 `writable: true` 更改为 `false`，从而防止其值被修改（以添加另一层保护）。但无法反向行之。

属性描述符在单个属性的级别上工作。
还有一些限制访问 **整个** 对象的方法：
[Object.preventExtensions(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/preventExtensions)
禁止向对象添加新属性。
[Object.seal(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal)
禁止添加/删除属性。为所有现有的属性设置 `configurable: false`。
[Object.freeze(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze)
禁止添加/删除/更改属性。为所有现有的属性设置 `configurable: false, writable: false`。
还有针对它们的测试：
[Object.isExtensible(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isExtensible)
如果添加属性被禁止，则返回 `false`，否则返回 `true`。
[Object.isSealed(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isSealed)
如果添加/删除属性被禁止，并且所有现有的属性都具有 `configurable: false`则返回 `true`。
[Object.isFrozen(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isFrozen)
如果添加/删除/更改属性被禁止，并且所有当前属性都是 `configurable: false, writable: false`，则返回 `true`。
这些方法在实际中**很少使用**。

##### 属性的访问器属性（存取描述符）
对象属性有两种：
- 数据属性：是上面的最常见的
- 访问器属性：本质上是用于获取和设置值的函数，但从外部代码来看就像常规属性。
```javascript
let user = {
    name: 'Dano',
    surname: 'Day',
    get fullName() {
        return `${this.name} ${this.surname}`;
    },
    set fullName(fullname) {
        [this.name, this.surname] = fullname.split(" ")
    },
}

console.log(user.fullName);//Dano Day
user.fullName = "Jungle Dog";
console.log(user.fullName);//Jungle Dog
```

现在，我们就有一个“虚拟”属性。它是可读且可写的。

对于访问器属性，没有 `value` 和 `writable`，但是有 `get` 和 `set` 函数。
所以访问器描述符可能有：
- **`get`** —— 一个没有参数的函数，在读取属性时工作，
- **`set`** —— 带有一个参数的函数，当属性被设置时调用，
- **`enumerable`** —— 与数据属性的相同，
- **`configurable`** —— 与数据属性的相同。
```javascript
let user = {
    name: "Dano",
    surname: "Day"
};

Object.defineProperty(user, 'fullName', {
    get() {
        return `${this.name} ${this.surname}`;
    },

    set(value) {
        [this.name, this.surname] = value.split(" ");
    }
});

console.log(user.fullName); // Dano Day
console.log(Object.getOwnPropertyDescriptors(user));
/**
 * {
  name: {
    value: 'Dano',
    writable: true,
    enumerable: true,
    configurable: true
  },

  surname: {
    value: 'Day',
    writable: true,
    enumerable: true,
    configurable: true
  },
  fullName: {
    get: [Function: get],
    set: [Function: set],
    enumerable: false,
    configurable: false
  }
}
 */
for (let key in user) console.log(key); // name, surname
```

一个属性要么是访问器（具有 `get/set` 方法），要么是数据属性（具有 `value`），但**不能两者都是**。

使用getter和setter来构建一个看似真实，但是可以具有更多控制的属性：
```javascript
let user = {
    get name() {
        return this._name;
    },
    set name (value) {
        if (value.length < 4) {
            console.log("too short");
            return
        }
        this._name = value;
    },
};

user.name = "dano";
console.log(user.name);//dano
console.log(user._name);
```

所以，name 被存储在 `_name` 属性中，并通过 getter 和 setter 进行访问。

从技术上讲，外部代码可以使用 `user._name` 直接访问 name。但是，这儿有一个众所周知的约定，即以下划线 `"_"` 开头的属性是内部属性，不应该从对象外部进行访问。

### 现代JS教程与阮一峰ES6 · 1数据类型与变量/Object/对象的循环引用与深克隆 ⌚️
##### 对象的循环引用
在 JavaScript 中，检测对象是否存在循环引用（即对象直接或间接引用自身）可以通过**追踪已访问对象**的方式实现。核心思路是：遍历对象时记录已访问过的对象，若再次遇到同一对象则说明存在循环引用。

方法及原理：递归遍历 + 已访问对象集合

```javascript
/**
 * 检测对象是否存在循环引用
 * @param {Object} obj - 要检测的对象
 * @param {Set} [visited] - 用于记录已访问对象的集合（内部递归使用）
 * @returns {boolean} 是否存在循环引用
 */
function hasCycle(obj, visited = new Set()) {
  // 若不是对象或为 null，直接返回 false（非对象不会有循环引用）
  if (obj === null || typeof obj !== 'object') {
    return false;
  }

  // 若当前对象已被访问过，说明存在循环引用
  if (visited.has(obj)) {
    return true;
  }

  // 将当前对象加入已访问集合
  visited.add(obj);

  // 递归遍历对象的所有属性
  for (const key in obj) {
    // 只遍历对象自身的可枚举属性
    if (obj.hasOwnProperty(key)) {
      // 递归检测属性值
      if (hasCycle(obj[key], visited)) {
        return true;
      }
    }
  }

  // 遍历完成后移除当前对象（不影响其他分支的检测）
  visited.delete(obj);
  return false;
}
```

 原理说明
1. **核心逻辑**：
   使用 `Set` 存储已访问过的对象（`Set` 可以直接存储对象引用并判断是否存在）。遍历对象时，若当前对象已在 `Set` 中，则说明存在循环引用。

2. **递归遍历**：
   对对象的每个属性值递归执行检测，确保所有嵌套对象都被检查。

3. **边界处理**：
   - 非对象类型（如基本类型、`null`）不会产生循环引用，直接返回 `false`。
   - 使用 `hasOwnProperty` 只遍历对象自身属性，避免遍历原型链上的属性。

 示例验证

```javascript
// 无循环引用的对象
const obj1 = { a: 1, b: { c: 2 } };
console.log(hasCycle(obj1)); // false

// 有循环引用的对象（直接引用自身）
const obj2 = { x: 1 };
obj2.y = obj2;
console.log(hasCycle(obj2)); // true

// 有循环引用的对象（间接引用自身）
const obj3 = { a: {} };
obj3.b = { c: obj3 };
console.log(hasCycle(obj3)); // true
```

 注意事项
- **性能**：对于深层嵌套的大型对象，递归可能存在性能问题，可考虑改用迭代方式实现。
- **特殊对象**：该方法对 `Map`、`Set` 等内置对象可能需要额外处理（需遍历其元素）。
*8/11/26 【修正】原内容：循环引用可能导致内存泄漏并需手动解除；修改点：不可达的循环可被现代追踪式 GC 回收，真正风险是对象仍被监听器、缓存等持续引用。*
- **循环引用的影响**：循环对象无法直接被 `JSON.stringify` 序列化；是否泄漏取决于它是否仍然可达。

通过这种方式，可以有效检测大多数常见场景下的循环引用问题。
##### 深拷贝与浅拷贝
在 JavaScript 中，深拷贝和浅拷贝是针对引用类型数据（如对象、数组）的复制操作，核心区别在于是否复制对象的 “深层结构”：
- 浅拷贝：只复制对象的表层结构，对于嵌套的引用类型（如对象中的对象），仅复制其引用（内存地址），修改拷贝后的嵌套对象会==影响原对象==。
- 深拷贝：完全复制对象的所有层级结构，包括嵌套的引用类型，拷贝后的数据与原对象完全独立，修改==互不影响==。

```javascript
const obj1 = {
  a: 2,
  b: 3,
  c: {
    name: "dano",
  },
};

let obj2 = {}

obj2 = obj1;

console.log(obj2);
//{ a: 2, b: 3, c: { name: 'dano' } }
obj2.c.name = 'shit';

console.log(obj1,obj2,obj1===obj2)
//{ a: 2, b: 3, c: { name: 'shit' } } { a: 2, b: 3, c: { name: 'shit' } } true

// 这就是一个相同的地址
```

**浅拷贝**只处理对象的第一层属性，嵌套对象仍共享引用。
1. 手动遍历赋值
```javascript
const obj = {
  a: 2,
  b: 3,
  c: {
    name: "2",
  },
};

const obj2 = {};

for (key in obj) {
  if (obj.hasOwnProperty(key)) {
    obj2[key] = obj[key];
  }
}

console.log(obj, obj2, obj === obj2);
// { a: 2, b: 3, c: { name: '2' } } { a: 2, b: 3, c: { name: '2' } } false

obj.a = "test"
console.log(obj, obj2, obj === obj2);
// { a: 'test', b: 3, c: { name: '2' } } { a: 2, b: 3, c: { name: '2' } } false

obj.c.name = "test2"
console.log(obj, obj2, obj === obj2);
// { a: 'test', b: 3, c: { name: 'test2' } } { a: 2, b: 3, c: { name: 'test2' } } false
```

 2. `Object.assign()`
```javascript
const obj = { a: 1, b: { c: 2 } };
const shallowCopy = Object.assign({}, obj);

shallowCopy.b.c = 3;
console.log(obj.b.c); // 3（原对象受影响）
```

3. 数组的 `slice()`、`concat()` 或扩展运算符
```javascript
const arr = [1, [2, 3]];
const shallowCopy = [...arr]; // 或 arr.slice()、[].concat(arr)

shallowCopy[1][0] = 4;
console.log(arr[1][0]); // 4（原数组受影响）
```


**深拷贝**会递归复制所有层级，确保拷贝后的数据完全独立。

```js
const obj = {
    a: 1,
    b: {
        c: 2,
        d: {
            name: '张三',
        },
    },
}

// 浅拷贝
const deepCopyB = { ...obj }

// 深拷贝
const deepCopy = JSON.parse(JSON.stringify(obj))

// { a: 1, b: { c: 2 } } { a: 1, b: { c: 2 } }
console.log(deepCopy, deepCopyB)
```
1. `JSON.parse(JSON.stringify())`与原生 structuredClone()（简单场景）
利用 JSON 序列化与反序列化实现深拷贝，缺点是无法处理函数、`Symbol`、循环引用等。

```javascript
const obj = { a: 1, b: { c: 2 } };
const deepCopy = JSON.parse(JSON.stringify(obj));

deepCopy.b.c = 3;
console.log(obj.b.c); // 2（原对象不受影响）
```

*8/11/26 【修正】原内容：`structuredClone` 是 ES2022 新增且普遍最推荐的深拷贝 API；修改点：它是宿主环境的结构化克隆 API，是否适合取决于数据类型与兼容目标。*
`structuredClone` 适合其支持的数据结构，使用前必须确认不可克隆值、原型和属性描述符等边界。

优点:
原生支持：无需第三方库，一行代码搞定。
功能强大：支持 Date, RegExp, Map, Set, ArrayBuffer 等多种内置类型，并能正确处理循环引用。

局限性:
*8/11/26 【修正】原内容：函数会被忽略；修改点：包含函数等不可克隆值时通常抛出 `DataCloneError`。*
无法拷贝函数：包含函数时会抛出 `DataCloneError`。
*8/11/26 【修正】原内容：Symbol 类型属性统一被忽略；修改点：Symbol 值不可克隆并会抛出 `DataCloneError`，Symbol 键也不会被结构化克隆保留。*
无法拷贝 Symbol 值，也不能依赖结构化克隆保留 Symbol 键。
兼容性：需要较新的浏览器环境 (Chrome 98+, Firefox 97+, Safari 15.4+)。

```js
const originalObj = {
  name: 'Alice',
  hobbies: ['reading', 'coding'],
  details: {
    age: 30,
    city: 'New York'
  },
  createdAt: new Date(),
  pattern: /test/g
};

// 一行代码实现深拷贝
const clonedObj = structuredClone(originalObj);

// 验证：修改克隆对象不会影响原对象
clonedObj.details.city = 'London';
clonedObj.hobbies.push('gaming');

console.log(originalObj.details.city); // 输出: 'New York' (未受影响)
console.log(originalObj.hobbies);      // 输出: ['reading', 'coding'] (未受影响)
```

2. 递归实现深拷贝（完整版）
*8/11/26 【修正】原内容：包含函数时手写递归深拷贝是最佳选择；修改点：示例会共享函数引用，且不能完整保留原型、描述符、Symbol 键及多种内建对象。*
兼容旧环境时应按数据模型选择领域映射、受验证的库或受限的递归实现。这个方案的核心是递归遍历对象的所有属性，并使用 WeakMap 来解决循环引用的问题。

```js
function deepClone(obj, hash = new WeakMap()) {
  // 1. 处理 null 和基础数据类型
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  // 2. 处理日期对象
  if (obj instanceof Date) {
    return new Date(obj.getTime());
  }

  // 3. 处理正则表达式
  if (obj instanceof RegExp) {
    return new RegExp(obj.source, obj.flags);
  }

  // 4. 处理循环引用
  // 如果这个对象之前已经被克隆过，则直接返回克隆后的对象
  if (hash.has(obj)) {
    return hash.get(obj);
  }

  // 5. 处理数组
  if (Array.isArray(obj)) {
    const arrCopy = [];
    hash.set(obj, arrCopy); // 在递归前先记录，防止循环引用
    obj.forEach((item, index) => {
      arrCopy[index] = deepClone(item, hash);
    });
    return arrCopy;
  }

  // 6. 处理普通对象
  const objCopy = {};
  hash.set(obj, objCopy); // 在递归前先记录，防止循环引用
  Object.keys(obj).forEach(key => {
    objCopy[key] = deepClone(obj[key], hash);
  });
  return objCopy;
}

// --- 使用示例 ---
const original = {
  name: 'Bob',
  info: { age: 25 },
  hobbies: ['swimming'],
  createdAt: new Date()
};
// 处理循环引用
original.self = original;

const cloned = deepClone(original);

// 验证
cloned.info.age = 99;
cloned.hobbies.push('running');
cloned.self.name = 'Tom'; // 修改克隆对象的循环引用

console.log(original.info.age);      // 输出: 25 (未受影响)
console.log(original.hobbies);       // 输出: ['swimming'] (未受影响)
console.log(original.self.name);     // 输出: 'Bob' (未受影响，循环引用也被正确克隆)
```

优点:
兼容性好：不依赖新API，可在所有 JavaScript 环境中运行。
高度可控：可以根据需求定制，例如增加对 Map、Set 等类型的支持。

局限性:
代码量较大：需要自己实现和维护。
性能开销：对于极深的嵌套结构，递归可能会带来一定的性能开销。
在递归深拷贝中，使用 `WeakMap` 来防止循环引用，其核心原理可以概括为 **“缓存已访问对象，打破递归闭环”**。

当一个对象内部引用了自身（或形成了相互引用的闭环）时，普通的递归深拷贝就会陷入死循环。

```javascript
const obj = { name: 'Alice' };
obj.self = obj; // obj 对象引用了自己，形成循环引用

// 一个普通的递归深拷贝函数
function simpleDeepClone(obj) {
  const clone = {};
  for (let key in obj) {
    clone[key] = simpleDeepClone(obj[key]); // 递归拷贝属性
  }
  return clone;
}

simpleDeepClone(obj); // 这会触发 "Maximum call stack size exceeded" 错误
```

### 执行过程分析
1. `simpleDeepClone(obj)` 开始执行，尝试拷贝 `obj`。
2. 遇到属性 `self`，其值是 `obj` 本身。
3. 函数再次调用 `simpleDeepClone(obj)`。
4. 回到第2步，无限循环，直到调用栈溢出。

`WeakMap` 在这里充当了一个“备忘录”或“缓存”的角色，用来记录“**原始对象 -> 克隆对象**”的映射关系。

在递归函数中，我们增加两个关键步骤：

1. **检查备忘录**：在开始拷贝一个对象前，先检查它是否已经被拷贝过。如果拷贝过，就直接返回之前创建好的克隆对象，不再继续递归。
2. **更新备忘录**：在创建了一个新的克隆对象后，立即将“原始对象”和“新克隆对象”的对应关系存入 `WeakMap`。

让我们看看修正后的代码：

```javascript
function deepClone(obj, hash = new WeakMap()) {
  // 1. 处理基础类型
  if (obj === null || typeof obj !== 'object') return obj;

  // 2. 【关键步骤一】检查备忘录
  // 如果当前对象已经被克隆过，直接从备忘录中取出克隆体返回
  if (hash.has(obj)) {
    return hash.get(obj);
  }

  // 3. 创建新的克隆容器 (数组或对象)
  const clone = Array.isArray(obj) ? [] : {};

  // 4. 【关键步骤二】更新备忘录
  // 在递归之前，立即将“原对象 -> 克隆对象”的关系记录下来
  hash.set(obj, clone);

  // 5. 递归拷贝所有属性
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key], hash); // 将备忘录传递给下一层递归
    }
  }

  return clone;
}
```

### 执行过程分析（使用 WeakMap）
1. `deepClone(obj)` 开始执行。
2. `hash` 是空的，`hash.has(obj)` 为 `false`。
3. 创建空的克隆对象 `clone`。
4. **立即执行 `hash.set(obj, clone)`**，将映射关系 `{obj -> clone}` 存入备忘录。
5. 开始遍历属性，遇到 `self`，其值是 `obj`。
6. 再次调用 `deepClone(obj, hash)`。
7. 此时，`hash.has(obj)` 检查发现 `obj` 已经存在于备忘录中！
8. 函数不再递归，直接返回 `hash.get(obj)`，也就是之前创建的那个 `clone` 对象。
9. 递归被成功打断，函数正常结束。


*8/11/26 【修正】原内容：深克隆使用 `WeakMap` 就能防止内存泄漏；修改点：局部 `Map` 随克隆函数结束后也可整体回收，只有备忘录被长期持有时，强引用才可能造成滞留。*
`WeakMap` 能记录循环引用且不会强持有键，但是否泄漏仍取决于备忘录和相关对象是否持续可达。

|数据结构|对键的引用类型|后果|
|:--|:--|:--|
|**普通对象 `{}`** 或 **`Map`**|**强引用**|只要备忘录自身仍可达，它就会强持有键；若备忘录只是函数内局部值并随调用结束变得不可达，整体仍可被回收。|
|**`WeakMap`**|**弱引用**|`WeakMap` 对其键的引用是“弱”的。如果一个对象在你的程序中没有其他强引用了，即使它还在 `WeakMap` 中，JavaScript 的垃圾回收机制也会**自动回收**它。这保证了 `WeakMap` 不会意外地阻止内存释放。|

**总结来说：** `WeakMap` 在深拷贝中扮演了一个**临时的、不会造成内存泄漏的缓存角色**。它通过记录已访问对象来打破递归的循环链，同时其“弱引用”的特性确保了它不会干扰 JavaScript 引擎正常的垃圾回收机制，是一种既安全又高效的解决方案。

自己实现的版本

```js
const obj = {
    a: 1,
    b: {
        c: 2,
        d: {
            name: '张三',
        },
    },
}

obj.self = obj

const deepClone = (obj, hash = new WeakMap()) => {
    // 函数 + 所有的原始值类型
    if (obj === null || typeof obj !== 'object') {
        return obj
    }

    // 剩下的全部是引用类型的

    // if (obj instanceof Date) {
    //     return new Date(obj.getTime())
    // }

    // if (obj instanceof RegExp) {
    //     return new RegExp(obj.source, obj.flags)
    // }

    if (hash.has(obj)) {
        return hash.get(obj)
    }

    if (Array.isArray(obj)) {
        const arrCopy = []

        // 在递归前先记录，防止循环引用
        hash.set(obj, arrCopy)

        obj.forEach((item) => {
            arrCopy.push(deepClone(item, hash))
        })

        return arrCopy
    }

    // 深拷贝对象
    const objCopy = {}

    // 在递归前先记录，防止循环引用
    hash.set(obj, objCopy)

    Object.keys(obj).forEach((key) => {
        objCopy[key] = deepClone(obj[key], hash)
    })

    return objCopy
}

const deepCopyB = deepClone(obj)

deepCopyB.b.d.name = '李四'

console.log(deepCopyB, deepCopyB.self, obj)
// <
// ref * 1 >
// { a: 1, b: { c: 2, d: { name: '李四' } }, self: [Circular * 1] } <
// ref * 1 >
// { a: 1, b: { c: 2, d: { name: '李四' } }, self: [Circular * 1] } <
// ref * 1 >
// { a: 1, b: { c: 2, d: { name: '张三' } }, self: [Circular * 1] }

```

| 特性               | 浅拷贝                          | 深拷贝                          |
|--------------------|---------------------------------|---------------------------------|
| 复制层级           | 仅复制第一层属性                | 递归复制所有层级（包括嵌套对象）|
| 引用类型处理       | 嵌套对象共享引用                | 嵌套对象完全独立                |
| 对原对象的影响     | 修改嵌套对象会影响原对象        | 修改拷贝后的数据不影响原对象    |
| 适用场景           | 简单结构、无需独立嵌套对象      | 复杂结构、需要完全独立的数据    |
| 性能               | 效率高（复制层级少）            | 效率较低（递归处理所有层级）    |

- 浅拷贝适合简单对象，实现简单但无法隔离嵌套引用类型的修改。
- 深拷贝适合复杂对象（含嵌套结构、循环引用等），确保数据完全独立，但实现较复杂且性能开销更大。
- 实际开发中，可根据数据复杂度选择合适的拷贝方式：简单场景用 `Object.assign()` 或扩展运算符，复杂场景用递归深拷贝函数。

### 廖雪峰教程 · 3快速入门/3.5 对象
##### 对象
JavaScript的对象是一种无序的集合数据类型，它由若干键值对组成。

JavaScript的对象用于描述现实世界中的某个对象。例如，为了描述“小明”这个淘气的小朋友，我们可以用若干键值对来描述他：
```javascript
let xiaoming = {
    name: '小明',
    birth: 1990,
    school: 'No.1 Middle School',
    height: 1.70,
    weight: 65,
    score: null
};
```

JavaScript用一个`{...}`表示一个对象，键值对以`xxx: xxx`形式申明，用`,`隔开。注意，最后一个键值对不需要在末尾加`,`，如果加了，有的浏览器（如低版本的IE）将报错。

上述对象申明了一个`name`属性，值是`'小明'`，`birth`属性，值是`1990`，以及其他一些属性。最后，把这个对象赋值给变量`xiaoming`后，就可以通过变量`xiaoming`来获取小明的属性了：
```javascript
xiaoming.name; // '小明'
xiaoming.birth; // 1990
```

访问属性是通过`.`操作符完成的，但这要求属性名必须是一个有效的变量名。如果属性名包含特殊字符，就必须用`''`括起来：
```javascript
let xiaohong = {
    name: '小红',
    'middle-school': 'No.1 Middle School'
};
```

`xiaohong`的属性名`middle-school`不是一个有效的变量，就需要用`''`括起来。访问这个属性也无法使用`.`操作符，必须用`['xxx']`来访问：
```javascript
xiaohong['middle-school']; // 'No.1 Middle School'
xiaohong['name']; // '小红'
xiaohong.name; // '小红'
```

也可以用`xiaohong['name']`来访问`xiaohong`的`name`属性，不过`xiaohong.name`的写法更简洁。我们在编写JavaScript代码的时候，属性名尽量使用标准的变量名，这样就可以直接通过`object.prop`的形式访问一个属性了。

实际上JavaScript对象的所有属性都是字符串，不过属性对应的值可以是任意数据类型。

如果访问一个不存在的属性会返回什么呢？JavaScript规定，访问不存在的属性不报错，而是返回`undefined`

由于JavaScript的对象是动态类型，你可以自由地给一个对象添加或删除属性：
```javascript
let xiaoming = {
    name: '小明'
};
xiaoming.age; // undefined
xiaoming.age = 18; // 新增一个age属性
xiaoming.age; // 18
delete xiaoming.age; // 删除age属性
xiaoming.age; // undefined
delete xiaoming['name']; // 删除name属性
xiaoming.name; // undefined
delete xiaoming.school; // 删除一个不存在的school属性也不会报错
```

如果我们要检测`xiaoming`是否拥有某一属性，可以用`in`操作符：
```javascript
let xiaoming = {
    name: '小明',
    birth: 1990,
    school: 'No.1 Middle School',
    height: 1.70,
    weight: 65,
    score: null
};
'name' in xiaoming; // true
'grade' in xiaoming; // false
```

不过要小心，如果`in`判断一个属性存在，这个属性不一定是`xiaoming`的，它可能是`xiaoming`继承得到的：
```javascript
'toString' in xiaoming; // true
```

因为`toString`定义在`object`对象中，而所有对象最终都会在原型链上指向`object`，所以`xiaoming`也拥有`toString`属性。

要判断一个属性是否是`xiaoming`自身拥有的，而不是继承得到的，可以用`hasOwnProperty()`方法：
```javascript
let xiaoming = {
    name: '小明'
};
xiaoming.hasOwnProperty('name'); // true
xiaoming.hasOwnProperty('toString'); // false
```
