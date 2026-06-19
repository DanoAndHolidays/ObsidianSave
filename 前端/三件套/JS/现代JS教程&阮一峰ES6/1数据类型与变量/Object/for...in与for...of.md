# JS中 for...in 和 for...of 的核心区别（超清晰版）
这是 JavaScript 面试和日常开发**高频考点**，我用最简单、最实用的方式给你讲清楚，一看就懂。

## 一句话总结
- **`for...in`**：遍历**键名（key/index）**，适合遍历**对象**，**不适合遍历数组**
- **`for...of`**：遍历**值（value）**，适合遍历**数组/类数组/可迭代对象**，**ES6 新增**

---

## 1. 遍历的内容不同（最核心区别）
### for...in
遍历**键名**（对象的 key、数组的 index）
```js
const arr = ['a', 'b', 'c'];
for (let index in arr) {
  console.log(index); // 输出 0, 1, 2 （字符串类型）
}
```

### for...of
遍历**值**（数组的元素、迭代器返回的值）
```js
const arr = ['a', 'b', 'c'];
for (let value of arr) {
  console.log(value); // 输出 a, b, c
}
```

---

## 2. 适用数据类型不同
### for...in
**可以遍历对象**（普通对象、数组都能用）
```js
const obj = { name: '小明', age: 18 };
for (let key in obj) {
  console.log(key, obj[key]); // name 小明，age 18
}
```
⚠️ **缺点**：会遍历出**原型链上的属性**，容易出问题。

### for...of
**不能直接遍历普通对象**，只能遍历**可迭代对象**：
- 数组
- 字符串
- Map / Set
- arguments、DOM 集合
- Generator 等

```js
// 遍历字符串
for (let char of 'hello') {
  console.log(char); // h e l l o
}
```

---

## 3. 遍历数组时的表现差异（重点）
| 特性 | for...in | for...of |
|------|----------|----------|
| 遍历内容 | 数组下标（字符串类型） | 数组元素 |
| 顺序 | 不保证顺序 | 严格按数组顺序 |
| 原型属性 | 会遍历出来 | 不会 |
| 数组新增方法 | 会遍历到 | 不会 |

**例子：for...in 会踩坑**
```js
Array.prototype.test = '123';
const arr = [10, 20];

for (let index in arr) {
  console.log(index); 
  // 输出 0、1、test ❌ 把原型上的属性也遍历了
}

for (let value of arr) {
  console.log(value); 
  // 输出 10、20 ✅ 安全、干净
}
```

---

## 4. 支持的语法特性
- `for...in`：**不支持** `await`（异步遍历）
- `for...of`：**支持** `await`（非常实用）

```js
// 异步遍历（for...of 独有）
async function test() {
  const arr = [1, 2, 3];
  for (let item of arr) {
    await new Promise(r => setTimeout(r, 1000));
    console.log(item);
  }
}
```

---

## 5. 最佳使用场景（背会就不会用错）
### ✅ 用 for...in 的场景
- 遍历**普通对象**（`{}`）获取键值对

### ✅ 用 for...of 的场景
- 遍历**数组**
- 遍历**字符串**
- 遍历 **Map / Set**
- 异步遍历
- 需要直接拿元素值的时候

---

## 极简记忆口诀
> **看键用 in，看值用 of；对象用 in，数组用 of。**

---

### 总结
1. **for...in** 遍历**键/下标**，适合**对象**，会遍历原型属性，**不推荐遍历数组**
2. **for...of** 遍历**值/元素**，适合**数组/字符串/可迭代对象**，**安全、现代、推荐**
3. 遍历数组**优先用 for...of**，遍历普通对象用 for...in