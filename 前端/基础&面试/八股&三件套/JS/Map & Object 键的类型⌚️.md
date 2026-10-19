# Map & Object 键的类型
在 JavaScript 中，`Map` 的键（Key）可以是任意 JavaScript 类型，包括基本数据类型和引用数据类型

|类型|是否支持|示例|
|---|---|---|
|`string`|✅|`"name"`|
|`number`|✅|`123`|
|`boolean`|✅|`true`|
|`undefined`|✅|`undefined`|
|`null`|✅|`null`|
|`bigint`|✅|`123n`|
|`symbol`|✅|`Symbol("id")`|
|`object`|✅|`{ id: 1 }`|
|`array`|✅|`[1, 2, 3]`|
|`function`|✅|`() => {}`|

例如：
```
const map = new Map();

map.set("name", "Dano");
map.set(123, "数字键");
map.set(true, "布尔键");
map.set(null, "null 键");
map.set(undefined, "undefined 键");

const obj = { id: 1 };
map.set(obj, "对象键");

const arr = [1, 2, 3];
map.set(arr, "数组键");

const fn = () => {};
map.set(fn, "函数键");
```

---
## 两个键相等
`Map` 使用 SameValueZero 算法判断键是否相等。

对于基本类型，通常比较值；对于对象类型，比较引用身份。

基本类型：
```
const map = new Map();

map.set(1, "hello");
map.set(1, "world");

console.log(map.size); // 1
console.log(map.get(1)); // world

map.set(NaN, "abc");
console.log(map.get(NaN)); // abc

map.set(0, "zero");
console.log(map.get(-0)); // zero
```

需要注意：`NaN` 和 `NaN` 在 `Map` 中被认为是同一个键，`+0` 和 `-0` 也是同一个键。

---
## Map 和 Object 的区别
*我他妈面试答错了，考，我说成 Object 的键值限制了*

|对比项|Map|Object|
|---|---|---|
|键类型|任意类型|`string` 或 `symbol`|
|键顺序|保持插入顺序|有特定的属性枚举顺序规则|
|获取数量|`map.size`|`Object.keys(obj).length`|
|遍历|可以直接 `for...of`|需要借助 `Object.keys/entries` 等|
|适用场景|动态键值映射、频繁增删|结构化数据、普通对象|

例如普通对象：
```
const obj = {};

obj[123] = "hello";

console.log(Object.keys(obj)); // ["123"]
```

这里数字 `123` 会转换为字符串 `"123"`。

而 `Map` 不会：
```
const map = new Map();

map.set(123, "hello");
map.set("123", "world");

console.log(map.size); // 2
```

总结：

- `Object` 的属性键只能是 `string` 或 `symbol`，其他类型作为属性键时通常会转换为字符串

- `Map` 的键可以是任意 JavaScript 类型

- `Map` 的对象键按照引用身份比较，而不是按照对象内容比较

- `Map` 使用 `SameValueZero` 判断键是否相等


这也是为什么在算法题中，如果需要使用对象作为键，通常优先考虑 `Map`