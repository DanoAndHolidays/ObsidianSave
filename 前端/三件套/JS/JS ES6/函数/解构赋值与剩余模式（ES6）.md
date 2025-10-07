---

---
### 数组的解构赋值
---

```javascript
let [a, b, c] = [1, 2, 3];
```
上面代码表示，可以从数组中提取值，按照对应位置，对变量赋值。
本质上，这种写法属于“==模式匹配==”，只要等号两边的模式相同，左边的变量就会被赋予对应的值。
### 嵌套数组解构
---
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
### 对象的解构
---
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
### 剩余模式：...
---
- 解构赋值可以简洁地将一个对象或数组拆开赋值到多个变量上。
- 解构对象的完整语法：
    ``` `let` `{``prop` `:` varName `=` `default``,` `...`rest`}` `=` object ```
    这表示属性 `prop` 会被赋值给变量 `varName`，如果没有这个属性的话，就会使用默认值 `default`。
    没有对应映射的对象属性会被复制到 `rest` 对象。
- 解构数组的完整语法：
    ``` `let` `[`item1 `=` `default``,` item2`,` `...`rest`]` `=` array ```
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