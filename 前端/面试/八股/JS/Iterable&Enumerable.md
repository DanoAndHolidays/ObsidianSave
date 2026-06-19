# Iterable&Enumerable
在 JavaScript 中，**可迭代（Iterable）** 和 **可枚举（Enumerable）** 是两个完全不同维度的概念。

---
## 可迭代 (Iterable)
**核心机制：** 对象是否实现了 **Iterable 协议**。 **判断标准：** 对象（或其原型链上）是否有 `[Symbol.iterator]` 方法。 **使用场景：** `for...of` 循环、展开运算符 `...`、`Array.from()`、解构赋值等。

**内置可迭代对象：** `Array`, `Map`, `Set`, `String`, `TypedArray`, `arguments` 等。 **注意：** **普通的 Object `{}` 默认是不可迭代的！**
```javascript
const arr = [1, 2, 3];
console.log(typeof arr[Symbol.iterator]); // "function" -> 可迭代

for (const item of arr) { console.log(item); } // 正常输出 1, 2, 3

const obj = { a: 1, b: 2 };
// console.log(typeof obj[Symbol.iterator]); // undefined -> 不可迭代
// for (const item of obj) {} // ❌ TypeError: obj is not iterable
```

---
## 可枚举 (Enumerable)
**核心机制：** 对象属性描述符（Property Descriptor）中的 `enumerable` 标志位是 `true` 还是 `false`。 **判断标准：** `Object.getOwnPropertyDescriptor()` 或 `propertyIsEnumerable()`。 **使用场景：** `for...in` 循环、`Object.keys()`、`JSON.stringify()`、对象展开 `{...obj}`。

**特点：**
- 通过普通赋值（`obj.a = 1`）创建的属性，`enumerable` 默认为 `true`。
- 通过 `Object.defineProperty` 创建的属性，`enumerable` 默认为 `false`。
- 内置对象的原型方法（如 `Array.prototype.push`）通常是**不可枚举**的。

```javascript
const obj = {};

// 1. 普通赋值，默认可枚举
obj.a = 1; 
console.log(Object.getOwnPropertyDescriptor(obj, 'a').enumerable); // true

// 2. defineProperty，默认不可枚举
Object.defineProperty(obj, 'b', { value: 2 }); 
console.log(Object.getOwnPropertyDescriptor(obj, 'b').enumerable); // false

console.log(Object.keys(obj));    // ["a"]  -> 只能看到可枚举的属性
console.log(JSON.stringify(obj)); // '{"a":1}' -> 只能序列化可枚举的属性
```

---
## 核心区别对比

|对比维度|可迭代 (Iterable)|可枚举 (Enumerable)|
|:--|:--|:--|
|**底层协议**|`[Symbol.iterator]()` 方法|属性描述符 `enumerable: true/false`|
|**针对目标**|针对**整个对象/数据结构**|针对对象上的**单个属性**|
|**遍历语法**|`for...of`|`for...in`, `Object.keys()`|
|**普通对象 `{}`**|❌ 默认不可迭代|✅ 属性默认可枚举|
|**数组 `[]`**|✅ 可迭代（按值遍历）|✅ 索引属性可枚举（但 `length` 不可枚举）|
|**内置原型方法**|不适用|❌ 不可枚举（如 `toString`, `push`）|

这是面试和实战中最容易踩坑的地方：
```javascript
const arr = [10, 20, 30];
// 给数组加一个自定义属性
arr.customProp = "hello";

// 1. for...in (基于可枚举)
// 遍历的是【可枚举的属性名（键）】，包括原型链上的
for (const key in arr) {
  console.log(key); 
}
// 输出: "0", "1", "2", "customProp" 
// ⚠️ 不推荐用 for...in 遍历数组，因为可能遍历出非预期的属性

// 2. for...of (基于可迭代)
// 遍历的是【迭代器返回的值】
for (const value of arr) {
  console.log(value); 
}
// 输出: 10, 20, 30
// ✅ 只关心数据本身，完美避开 customProp
```