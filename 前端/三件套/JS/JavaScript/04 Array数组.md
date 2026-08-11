# 04 Array数组
> Last Format Time：8/11/2026 21:45:37

本笔记由两个 JavaScript 教程目录中的同主题内容合并而成；全部旧知识保留在“旧笔记知识全集（按来源保留）”中，并由导航逐项索引。

---
## 当前前端开发关键要点

> [!important] 学习优先级：P0
> - 熟练掌握 `map`、`filter`、`reduce`、`find`、`some`、`every`、`flatMap` 等声明式数组操作。
> - 区分会修改原数组与返回新数组的 API；React 状态更新中优先保持不可变数据。
> - 理解浅拷贝、稀疏数组、排序比较函数与迭代回调的行为和性能成本。

---
## 知识点导航
### [[04 Array数组#现代JS教程与阮一峰ES6 · 1数据类型与变量/Arrray|现代JS教程与阮一峰ES6 · 1数据类型与变量/Arrray]]
- Array API
- 数组

### [[04 Array数组#廖雪峰教程 · 3快速入门/3.4 数组|廖雪峰教程 · 3快速入门/3.4 数组]]
- 数组
- indexOf
- slice
- push和pop
- unshift和shift
- sort
- reverse
- splice
- concat
- join
- 多维数组

---
## 现代前端补充与纠错

> [!info] 修改标记
> - *【修正】*：旧教程中错误、过时或容易误导的内容。
> - *【补充】*：旧教程未覆盖、但当前前端开发需要掌握的内容。
> - *【修正代码】*：替换或校正了旧代码示例。

> [!warning] 下方保留旧教程原文；现代数组 API 与不可变更新建议以本节为准。

### 变更型与复制型 API
- *【补充】* `sort`、`reverse`、`splice` 会原地修改数组；状态管理中优先使用 `toSorted`、`toReversed`、`toSpliced` 和 `with`，或在兼容目标不支持时先复制。
- *【补充】* `map` 用于一一映射，`filter` 用于筛选，`reduce` 适合真正的累积过程；不要为了“函数式”把简单循环写成难读的 `reduce`。
- *【补充】* 稀疏数组在不同方法中的跳过/保留规则不一致，业务数据应尽量使用密集数组。

### 常见边界
- *【修正】* `Array(n)` 创建的是含空槽的稀疏数组，不是填充了 `undefined` 的数组；需要初始化时用 `Array.from` 或 `fill`。
- *【修正】* `includes` 可以匹配 `NaN`，`indexOf` 不可以。
- *【补充】* 大数据量去重、关联查询优先使用 `Set`/`Map`，避免循环中反复 `includes` 造成不必要的平方级扫描。
---
## 旧笔记知识全集（按来源保留）
### 现代JS教程与阮一峰ES6 · 1数据类型与变量/Arrray
##### Array API
**一、创建与转换数组**

1. **`Array.from(iterable, mapFn)`**
   将==类数组==对象（如 `arguments`、DOM 集合）或==可迭代对象==（如字符串、`Set`）转换为数组，可选的 `mapFn` 用于加工元素。

```javascript
   // 转换字符串为数组
   console.log(Array.from("hello")); // ["h", "e", "l", "l", "o"]

   // 转换类数组并加工
   const arrLike = { length: 3, 0: 1, 1: 2, 2: 3 };
   console.log(Array.from(arrLike, x => x * 2)); // [2, 4, 6]
```

2. **`Array.of(element1, ...)`**
   创建一个包含所有参数的数组（解决 `new Array(n)` 当 `n` 为数字时创建空数组的问题）。

```javascript
   console.log(Array.of(1, 2, 3)); // [1, 2, 3]
   console.log(Array.of(5)); // [5]（区别于 new Array(5) 返回长度为5的空数组）
```


**二、添加/删除元素**

1. **`push(...elements)`**
   向数组末尾添加元素，返回新的长度。

```javascript
   const arr = [1, 2];
   arr.push(3, 4);
   console.log(arr); // [1, 2, 3, 4]
```

2. **`pop()`**
   删除数组最后一个元素，返回被删除的元素。

```javascript
   const arr = [1, 2, 3];
   console.log(arr.pop()); // 3
   console.log(arr); // [1, 2]
```

3. **`unshift(...elements)`**
   向数组开头添加元素，返回新的长度。

```javascript
   const arr = [3, 4];
   arr.unshift(1, 2);
   console.log(arr); // [1, 2, 3, 4]
```

4. **`shift()`**
   删除数组第一个元素，返回被删除的元素。

```javascript
   const arr = [1, 2, 3];
   console.log(arr.shift()); // 1
   console.log(arr); // [2, 3]
```

5. **`splice(startIndex, deleteCount, ...addElements)`**
   从 `startIndex` 开始（包括）删除 `deleteCount` 个元素，并插入新元素，返回被删除的元素组成的数组。

```javascript
   const arr = [1, 2, 3, 4];
   // 从索引1开始，删除2个元素，插入5、6
   const deleted = arr.splice(1, 2, 5, 6);
   console.log(arr); // [1, 5, 6, 4]
   console.log(deleted); // [2, 3]
```


**三、查询与过滤**

1. **`indexOf(searchElement, fromIndex)` / `lastIndexOf(searchElement)`**
   查找元素首次/最后一次出现的索引，未找到返回 `-1`。

```javascript
   const arr = [1, 2, 3, 2, 1];
   console.log(arr.indexOf(2)); // 1
   console.log(arr.lastIndexOf(2)); // 3
```

2. **`includes(searchElement)`**
   判断数组是否包含指定元素，返回布尔值。

```javascript
   console.log([1, 2, 3].includes(2)); // true
   console.log([1, 2, 3].includes(4)); // false
```

3. **`find(callback)` / `findIndex(callback)`**
   - `find`：返回第一个满足 `callback` 条件的元素（无则返回 `undefined`）。
   - `findIndex`：返回第一个满足条件的元素的索引（无则返回 `-1`）。
```javascript
   const users = [
     { id: 1, name: "Alice" },
     { id: 2, name: "Bob" }
   ];
   console.log(users.find(u => u.id === 2)); // { id: 2, name: "Bob" }
   console.log(users.findIndex(u => u.name === "Alice")); // 0
```

4. **`filter(callback)`**
   返回所有满足 `callback` 条件的元素组成的新数组。  ==过滤==

```javascript
   const numbers = [1, 2, 3, 4, 5];
   const evens = numbers.filter(n => n % 2 === 0);
   console.log(evens); // [2, 4]
```


**四、遍历与转换**

1. **`forEach(callback)`**
   遍历数组，对每个元素执行 `callback`（==无返回值==）。

```javascript
   [1, 2, 3].forEach((item, index) => {
     console.log(`索引${index}的值：${item}`);
   });
   // 输出：
   // 索引0的值：1
   // 索引1的值：2
   // 索引2的值：3
```

2. **`map(callback)`**
   对每个元素执行 `callback`，返回加工后的新数组。  ==加工==

```javascript
   const numbers = [1, 2, 3];
   const squared = numbers.map(n => n * n);
   console.log(squared); // [1, 4, 9]
```

3. **`reduce(callback, initialValue)`**
   从左到右累计处理数组元素，返回最终结果（可用于求和、扁平化等）。就是对每个元素做些操作，将操作最后的结果累加起来，返回最后的值

```javascript
   arr.reduce((pre, cur, index, array) => {
    // pre   - 累积值
    // cur   - 当前元素
    // index - 当前索引
    // array - 原始数组
}, initialValue)

	// 求和
   const sum = [1, 2, 3, 4].reduce((acc, curr) => acc + curr, 0);
   console.log(sum); // 10

   // 扁平化数组
   const nested = [1, [2, 3], [4, 5]];
   const flat = nested.reduce((acc, curr) => acc.concat(curr), []);
   console.log(flat); // [1, 2, 3, 4, 5]
```

5. **`flat(depth)`**
   扁平化数组，`depth` 指定层级（默认1，`Infinity` 表示完全扁平化）。

```javascript
   const deep = [1, [2, [3, [4]]]];
   console.log(deep.flat(1)); // [1, 2, [3, [4]]]
   console.log(deep.flat(Infinity)); // [1, 2, 3, 4]
```


**五、排序与反转**

1. **`sort(compareFunction)`**
   对数组排序（默认按字符串 Unicode 码排序，需自定义比较函数）。

```javascript
   const numbers = [3, 1, 4, 1, 5];
   // 数字升序
   numbers.sort((a, b) => a - b);
   console.log(numbers); // [1, 1, 3, 4, 5]

   // 数字降序
   numbers.sort((a, b) => b - a);
   console.log(numbers); // [5, 4, 3, 1, 1]
```

2. **`reverse()`**
   反转数组元素顺序（修改原数组）。

```javascript
   const arr = [1, 2, 3];
   arr.reverse();
   console.log(arr); // [3, 2, 1]
```


**六、其他常用方法**

1. **`slice(startIndex, endIndex)`**
   截取从 `startIndex`（包括） 到 `endIndex`（不包含）的元素，返回新数组（不修改原数组）。

```javascript
   const arr = [1, 2, 3, 4];
   console.log(arr.slice(1, 3)); // [2, 3]
   console.log(arr.slice(-2)); // [3, 4]（从倒数第2位开始）
```

2. **`join(separator)`**
   用 `separator` 连接数组元素为字符串（默认用逗号连接）。

```javascript
   const arr = ["hello", "world"];
   console.log(arr.join(" ")); // "hello world"
```

3. **`every(callback)` / `some(callback)`**
   - `every`：判断所有元素是否满足 `callback` 条件（全满足返回 `true`）。
   - `some`：判断是否有至少一个元素满足条件（有则返回 `true`）。
```javascript
   const ages = [18, 20, 22];
   console.log(ages.every(age => age >= 18)); // true（所有都成年）
   console.log(ages.some(age => age > 21)); // true（有一个超过21）
```

3. 将数组转化为逗号分隔的字符串
```js
// 法1
arr = [1, 13, 4, 5]
console.log(arr.toString())// 1,13,4,5

// 法2
const arr = ["苹果", "香蕉", "橙子"];
const str = arr.join(','); // 结果："苹果,香蕉,橙子"

```

**总结**
- 增删元素用 `push`/`pop`/`unshift`/`shift`/`splice`（注意是否修改原数组）。
- 查询过滤用 `find`/`filter`/`includes`/`indexOf`。
- 遍历转换用 `forEach`/`map`/`reduce`/`flat`。
- 排序反转用 `sort`/`reverse`。

这些方法覆盖了数组操作的大部分场景，合理使用能大幅简化代码。

##### 数组
使用new Array（）声明一个新的数组。

```javascript
let arr = new Array();
let arr1 = [];
```

判断一个值是不是数组：
```javascript
const isArray =
  Array.isArray || ((list) => ({}.toString.call(list) === "[object Array]"));

console.log(isArray);//[Function: isArray]
```

数组的填充

```javascript
// 方法一:
const shit = Array(100).fill(0);
console.log(shit);

// 方法二:
// 注: 如果直接使用 map，会出现稀疏数组
console.log(Array.from(Array(100), (x) => (x = 0)));

// 方法二变体:
console.log(Array.from({ length: 100 }, (x) => (x = 0)));

//那我就用map呢
console.log(Array(100).map((x) => (x = 0)));
//[ <100 empty items> ]

```

可以替换元素，或者向数组新加一个元素，`length` 属性的值是数组中元素的总个数，也可以用 `alert` 来显示整个数组。数组可以存储任何类型的元素。

```javascript
let arr = new Array();
let arr1 = [
    2,
    'shit',
    function () {
        log("eat");
    },
];

arr1[2]();//eat
log(arr1.length);//3
```

我们可以显式地计算最后一个元素的索引，然后访问它：`fruits[fruits.length - 1]`
幸运的是，这里有一个更简短的语法 `fruits.at(-1)`

`pop`
取出并返回数组的最后一个元素

`push`
在数组末端添加元素

`shift`
取出数组的第一个元素并返回它

`unshift`
在数组的首端添加元素

`push` 和 `unshift` 方法都可以一次添加多个元素
`push/pop` 方法运行的比较快，而 `shift/unshift` 比较慢

当我们修改数组的时候，`length` 属性会自动更新。准确来说，它实际上不是数组里元素的个数，而是最大的数字索引值加一。`length` 属性的另一个有意思的点是它是可写的。清空数组最简单的方法就是：`arr.length = 0;`

数组没有 `Symbol.toPrimitive`，也没有 `valueOf`，它们只能执行 `toString` 进行转换

不应该使用 `==` 运算符比较 JavaScript 中的数组

另外拷贝数组和拷贝对象很像，同样的他们会指向同一个引用，共享里面的数据。

splice函数：
它从索引 `start` 开始修改 `arr`：删除 `deleteCount` 个元素并在当前位置插入 `elem1, ..., elemN`。最后返回被删除的元素所组成的数组。

```javascript
let arr1 = [
    2,
    'shit',
    function () {
        log("eat");
    },
];

arr1.splice(0, 3, '1', '2', 3);
console.log(arr1);//[ '1', '2', 3 ]
```

slice：
它从索引 `start` 开始修改 `arr`：删除 `deleteCount` 个元素并在当前位置插入 `elem1, ..., elemN`。最后返回被删除的元素所组成的数组。

concat：
结果是一个包含来自于 `arr`，然后是 `arg1`，`arg2` 的元素的新数组。

```javascript
let array = [1, 2];
let array1 = [3, 4];
let array2 = [5];

let array3=array.concat(array1, array2);

log(array3);//[ 1, 2, 3, 4, 5 ]
```

forEach:
```javascript
let arr = [1, 2, 3, 4, 5, 6];

arr.forEach((item,index,array) => {
    log(item);// 1 2 3 4 5 6
});
```

- `arr.indexOf(item, from)` —— 从索引 `from` 开始搜索 `item`，如果找到则返回索引，否则返回 `-1`。
- `arr.includes(item, from)` —— 从索引 `from` 开始搜索 `item`，如果找到则返回 `true`（译注：如果没找到，则返回 `false`）。
- 通常使用这些方法时只会传入一个参数：传入 `item` 开始搜索。默认情况下，搜索是从头开始的
- 方法 [arr.lastIndexOf](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Array/lastIndexOf) 与 `indexOf` 相同，但从右向左查找

reduce：累加方法
every：检测每一个值的

数组方法备忘单：

- 添加/删除元素：
	- with：没有使用过
    - `push(...items)` —— 向尾端添加元素，
    - `pop()` —— 从尾端提取一个元素，
    - `shift()` —— 从首端提取一个元素，
    - `unshift(...items)` —— 向首端添加元素，
    - `splice(pos, deleteCount, ...items)` —— 从 `pos` 开始删除（包括） `deleteCount` 个元素，并插入 `items`。
    - `slice(start, end)` —— 创建一个新数组，将从索引 `start` 到索引 `end`（但不包括 `end`）的元素复制进去。
    - `concat(...items)` —— 返回一个新数组：复制当前数组的所有元素，并向其中添加 `items`。如果 `items` 中的任意一项是一个数组，那么就取其元素。
- 搜索元素：
    - `indexOf/lastIndexOf(item, pos)` —— 从索引 `pos` 开始搜索 `item`，搜索到则返回该项的索引，否则返回 `-1`。
    - `includes(value)` —— 如果数组有 `value`，则返回 `true`，否则返回 `false`。
    - `find/filter(func)` —— 通过 `func` 过滤元素，返回使 `func` 返回 `true` 的第一个值/所有值。
    - `findIndex` 和 `find` 类似，但返回索引而不是值。
- 遍历元素：
    - `forEach(func)` —— 对每个元素都调用 `func`，不返回任何内容。
- 转换数组：
    - `map(func)` —— 根据对每个元素调用 `func` 的结果创建一个新数组。
    - `sort(func)` —— 对数组进行原位（in-place）排序，然后返回它。
    - `reverse()` —— 原位（in-place）反转数组，然后返回它。
    - `split/join` —— 将字符串拆分为数组并返回/将数组项组合成字符串并返回。
    - `reduce/reduceRight(func, initial)` —— 通过对每个元素调用 `func` 计算数组上的单个值，并在调用之间传递中间结果。
- 其他：

    - `Array.isArray(value)` 检查 `value` 是否是一个数组，如果是则返回 `true`，否则返回 `false`。

### 廖雪峰教程 · 3快速入门/3.4 数组
##### 数组
JavaScript的`Array`可以包含任意数据类型，并通过索引来访问每个元素。
要取得`Array`的长度，直接访问`length`属性：

_请注意_，直接给`Array`的`length`赋一个新的值会导致`Array`大小的变化：

`Array`可以通过索引把对应的元素修改为新的值，因此，对`Array`的索引进行赋值会直接修改这个`Array`

_请注意_，如果通过索引赋值时，索引超过了范围，同样会引起`Array`大小的变化：

大多数其他编程语言不允许直接改变数组的大小，越界访问索引会报错。然而，JavaScript的`Array`却不会有任何错误。在编写代码时，不建议直接修改`Array`的大小，访问索引时要确保索引不会越界。
##### indexOf
与String类似，`Array`也可以通过`indexOf()`来搜索一个指定的元素的位置：
```javascript
let arr = [10, 20, '30', 'xyz'];
arr.indexOf(10); // 元素10的索引为0
arr.indexOf(20); // 元素20的索引为1
arr.indexOf(30); // 元素30没有找到，返回-1
arr.indexOf('30'); // 元素'30'的索引为2
```

注意了，数字`30`和字符串`'30'`是不同的元素。
##### slice
`slice()`就是对应String的`substring()`版本，它截取`Array`的部分元素，然后返回一个新的`Array`：
```javascript
let arr = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
arr.slice(0, 3); // 从索引0开始，到索引3结束，但不包括索引3: ['A', 'B', 'C']
arr.slice(3); // 从索引3开始到结束: ['D', 'E', 'F', 'G']
```

注意到`slice()`的起止参数包括开始索引，不包括结束索引。

如果不给`slice()`传递任何参数，它就会从头到尾截取所有元素。利用这一点，我们可以很容易地复制一个`Array`：
```javascript
let arr = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
let aCopy = arr.slice();
aCopy; // ['A', 'B', 'C', 'D', 'E', 'F', 'G']
aCopy === arr; // false
```

##### push和pop
`push()`向`Array`的末尾添加若干元素，`pop()`则把`Array`的最后一个元素删除掉：
```javascript
let arr = [1, 2];
arr.push('A', 'B'); // 返回Array新的长度: 4
arr; // [1, 2, 'A', 'B']
arr.pop(); // pop()返回'B'
arr; // [1, 2, 'A']
arr.pop(); arr.pop(); arr.pop(); // 连续pop 3次
arr; // []
arr.pop(); // 空数组继续pop不会报错，而是返回undefined
arr; // []
```

##### unshift和shift
如果要往`Array`的头部添加若干元素，使用`unshift()`方法，`shift()`方法则把`Array`的第一个元素删掉：
```javascript
let arr = [1, 2];
arr.unshift('A', 'B'); // 返回Array新的长度: 4
arr; // ['A', 'B', 1, 2]
arr.shift(); // 'A'
arr; // ['B', 1, 2]
arr.shift(); arr.shift(); arr.shift(); // 连续shift 3次
arr; // []
arr.shift(); // 空数组继续shift不会报错，而是返回undefined
arr; // []
```

##### sort
`sort()`可以对当前`Array`进行排序，它会直接修改当前`Array`的元素位置，直接调用时，按照默认顺序排序：
```javascript
let arr = ['B', 'C', 'A'];
arr.sort();
arr; // ['A', 'B', 'C']
```

##### reverse
`reverse()`把整个`Array`的元素给调个个，也就是反转：
```javascript
let arr = ['one', 'two', 'three'];
arr.reverse();
arr; // ['three', 'two', 'one']
```

##### splice
`splice()`方法是修改`Array`的“万能方法”，它可以从指定的索引开始删除若干元素，然后再从该位置添加若干元素：
```javascript
let arr = ['Microsoft', 'Apple', 'Yahoo', 'AOL', 'Excite', 'Oracle'];
// 从索引2开始删除3个元素,然后再添加两个元素:
arr.splice(2, 3, 'Google', 'Facebook'); // 返回删除的元素 ['Yahoo', 'AOL', 'Excite']
arr; // ['Microsoft', 'Apple', 'Google', 'Facebook', 'Oracle']
// 只删除,不添加:
arr.splice(2, 2); // ['Google', 'Facebook']
arr; // ['Microsoft', 'Apple', 'Oracle']
// 只添加,不删除:
arr.splice(2, 0, 'Google', 'Facebook'); // 返回[],因为没有删除任何元素
arr; // ['Microsoft', 'Apple', 'Google', 'Facebook', 'Oracle']
```

##### concat
`concat()`方法把当前的`Array`和另一个`Array`连接起来，并返回一个新的`Array`：
```javascript
let arr = ['A', 'B', 'C'];
let added = arr.concat([1, 2, 3]);
added; // ['A', 'B', 'C', 1, 2, 3]
arr; // ['A', 'B', 'C']
```

_请注意_，`concat()`方法并没有修改当前`Array`，而是返回了一个新的`Array`。

`concat()`方法可以接收任意个元素和`Array`，并且自动把`Array`拆开，然后全部添加到新的`Array`里：

```javascript
let arr = ['A', 'B', 'C'];
arr.concat(1, 2, [3, 4]); // ['A', 'B', 'C', 1, 2, 3, 4]
```

##### join
`join()`方法是一个非常实用的方法，它把当前`Array`的每个元素都用指定的字符串连接起来，然后返回连接后的字符串：
```javascript
let arr = ['A', 'B', 'C', 1, 2, 3];
arr.join('-'); // 'A-B-C-1-2-3'
```

##### 多维数组
如果数组的某个元素又是一个`Array`，则可以形成多维数组，例如：
```javascript
let arr = [[1, 2, 3], [400, 500, 600], '-'];
```

上述`Array`包含3个元素，其中头两个元素本身也是`Array`。
