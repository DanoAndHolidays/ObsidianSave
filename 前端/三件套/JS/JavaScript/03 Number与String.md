# 03 Number与String
> Last Format Time：8/11/2026 21:45:36

本笔记由两个 JavaScript 教程目录中的同主题内容合并而成；全部旧知识保留在“旧笔记知识全集（按来源保留）”中，并由导航逐项索引。

---
## 当前前端开发关键要点

> [!important] 学习优先级：P0
> - 理解 IEEE 754 浮点误差；金额与高精度计算不要直接依赖普通浮点运算。
> - 优先使用模板字符串、标准字符串 API 与明确的编码处理，避免隐式拼接造成类型问题。
> - 掌握 `Number.isNaN`、`Number.isFinite`、安全整数范围以及字符串不可变性。

---
## 知识点导航
### [[03 Number与String#现代JS教程与阮一峰ES6 · 1数据类型与变量/Number|现代JS教程与阮一峰ES6 · 1数据类型与变量/Number]]
- Number API
- 数字类型
- 浮点数的底层实现
- 总结

### [[03 Number与String#现代JS教程与阮一峰ES6 · 1数据类型与变量/String|现代JS教程与阮一峰ES6 · 1数据类型与变量/String]]
- String
- 字符串

### [[03 Number与String#廖雪峰教程 · 3快速入门/3.3 字符串|廖雪峰教程 · 3快速入门/3.3 字符串]]
- 字符串
- 多行字符串
- 模板字符串
- 操作字符串
- toUpperCase
- toLowerCase
- indexOf
- substring

---
## 现代前端补充与纠错

> [!info] 修改标记
> - *【修正】*：旧教程中错误、过时或容易误导的内容。
> - *【补充】*：旧教程未覆盖、但当前前端开发需要掌握的内容。
> - *【修正代码】*：替换或校正了旧代码示例。

> [!warning] 下方保留旧教程上下文；已知语法错误已直接修正并标成 *【修正代码】*，API 差异标成 *【修正】*。

### 数值修正
*【修正】* 旧笔记中的科学计数法示例缺少赋值符号，正确写法是：

*【修正代码】*

```javascript
const billion = 1e9;
```

- *【修正】* `Number("12px")` 得到 `NaN`，`parseInt("12px", 10)` 得到 `12`；解析整数时显式传入基数。
- *【补充】* 浮点运算不能用十进制直觉直接比较，金额应使用最小货币单位整数、十进制定点库或明确的舍入规则。
- *【修正】* 用 `Number.isNaN` 判断真正的 `NaN`；全局 `isNaN` 会先强制转换。
- *【补充】* 国际化数字、货币、百分比、日期与相对时间优先使用 `Intl`，不要手拼区域格式。

### 字符串与 Unicode
- *【补充】* `length` 和索引按 UTF-16 码元计数，不等同于用户看到的字符数；遍历码点可用 `for...of`，字素簇需使用 `Intl.Segmenter` 等方案。
- *【补充】* 用户输入搜索、排序、大小写转换要考虑 locale；展示层可使用 `localeCompare`/`Intl.Collator`。
---
## 旧笔记知识全集（按来源保留）
### 现代JS教程与阮一峰ES6 · 1数据类型与变量/Number
##### Number API
在JavaScript中，`Number`类型提供了许多静态方法和实例方法，用于处理数字相关的操作。以下是常用的`Number` API及实例：


**一、静态方法（`Number.xxx()`）**

1. **`Number.isFinite()`**
   判断一个值是否为有限数（非`Infinity`、`-Infinity`或`NaN`）。

```javascript
   console.log(Number.isFinite(123));      // true
   console.log(Number.isFinite(Infinity)); // false
   console.log(Number.isFinite(NaN));      // false
```

2. **`Number.isInteger()`**
   判断一个值是否为整数（不含小数部分）。

```javascript
   console.log(Number.isInteger(5));    // true
   console.log(Number.isInteger(5.0));  // true（5.0本质是整数）
   console.log(Number.isInteger(5.5));  // false
```

3. **`Number.isNaN()`**
   判断一个值是否为`NaN`（比全局`isNaN()`更严格，不会强制类型转换）。

```javascript
   console.log(Number.isNaN(NaN));       // true
   console.log(Number.isNaN('123'));     // false（全局isNaN会返回true）
   console.log(Number.isNaN(123));       // false
```

4. **`Number.parseInt()`**
   解析字符串并返回整数（与全局`parseInt()`功能相同，推荐优先使用）。

```javascript
   console.log(Number.parseInt('123.45'));  // 123（只取整数部分）
   console.log(Number.parseInt('123abc'));  // 123（忽略非数字部分）
   console.log(Number.parseInt('abc123'));  // NaN（无法解析开头非数字）
```

5. **`Number.parseFloat()`**
   解析字符串并返回浮点数（与全局`parseFloat()`功能相同）。

```javascript
   console.log(Number.parseFloat('123.45')); // 123.45
   console.log(Number.parseFloat('123abc')); // 123
```

6. **`Number.MAX_SAFE_INTEGER` / `Number.MIN_SAFE_INTEGER`**
   表示JavaScript中安全的最大/最小整数（安全指能精确表示且不与其他数值混淆）。

```javascript
   console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991
   console.log(Number.MIN_SAFE_INTEGER); // -9007199254740991
```


**二、实例方法（`num.xxx()`）**

1. **`toFixed()`**
   将数字转换为指定小数位数的字符串（四舍五入）。

```javascript
   const num = 123.456;
   console.log(num.toFixed(2)); // "123.46"（保留2位小数）
   console.log(num.toFixed(0)); // "123"（保留0位小数）
```

2. **`toString()`**
   将数字转换为字符串，可指定基数（如2进制、16进制）。

```javascript
   const num = 255;
   console.log(num.toString());   // "255"（默认10进制）
   console.log(num.toString(2));  // "11111111"（2进制）
   console.log(num.toString(16)); // "ff"（16进制，小写）
```

3. **`toPrecision()`**
   将数字转换为指定长度的字符串（包含整数和小数部分，四舍五入）。

```javascript
   const num = 123.456;
   console.log(num.toPrecision(4)); // "123.5"（总长度4位）
   console.log(num.toPrecision(2)); // "1.2e+2"（科学计数法，总长度2位）
```

4. **`valueOf()`**
   返回数字的原始值（通常用于隐式类型转换）。

```javascript
   const numObj = new Number(123);
   console.log(numObj.valueOf()); // 123（从包装对象中获取原始值）
```

5. **`toLocaleString()`**
   根据本地环境格式化数字（如千分位分隔符）。

```javascript
   const num = 1234567.89;
   console.log(num.toLocaleString()); // "1,234,567.89"（默认本地格式）
   console.log(num.toLocaleString('de-DE')); // "1.234.567,89"（德语环境格式）
```

##### 数字类型
JavaScript 中的常规数字以 64 位的格式 [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754) 存储，就是“双精度浮点数”
常规整数不能安全地超过 `2^53-1` 或小于 `-2^53-1`。由于仅在少数特殊领域才会用到 BigInt，因此我们在特殊的章节 [BigInt](https://zh.javascript.info/bigint) 中对其进行了介绍。

使用下划线更具可读性。

```javascript
log(1_000_000);//1000000
```

使用**e**：
*8/11/26 【修正代码】原内容：`let billion 1e9`；修改点：补上赋值号。*

```javascript
let billion = 1e9;//10亿
let mcs = 1e-6;
```

进制：
[十六进制](https://en.wikipedia.org/wiki/Hexadecimal) 数字在 JavaScript 中被广泛用于表示颜色，编码字符以及其他许多东西。所以自然地，有一种较短的写方法：`0x`，然后是数字。
二进制和八进制数字系统很少使用，但也支持使用 `0b` 和 `0o` 前缀

```javascript
let a = 0xff;   //16进制
let b = 0b11111; //2进制
let c = 0o377;   //8进制

let num = 255;
log(num.toString(16));//ff
```

请注意 `123456..toString(36)` 中的两个点不是打错了。如果我们想直接在一个数字上调用一个方法，比如上面例子中的 `toString`，那么我们需要在它后面放置两个点 `..`。

如果我们放置一个点：`123456.toString(36)`，那么就会出现一个 error，因为 JavaScript 语法隐含了第一个点之后的部分为小数部分。如果我们再放一个点，那么 JavaScript 就知道小数部分为空，现在使用该方法。

也可以写成 `(123456).toString(36)`。

舍入：
`Math.floor`
向下舍入：`3.1` 变成 `3`，`-1.1` 变成 `-2`。

`Math.ceil`
向上舍入：`3.1` 变成 `4`，`-1.1` 变成 `-1`。

`Math.round`
向最近的整数舍入：`3.1` 变成 `3`，`3.6` 变成 `4`，中间值 `3.5` 变成 `4`。

`Math.trunc`（IE 浏览器不支持这个方法）
移除小数点后的所有内容而没有舍入：`3.1` 变成 `3`，`-1.1` 变成 `-1`。

|`   Math.floor`|`Math.ceil`|`Math.round`|`Math.trunc`|
|---|---|---|---|
|`3.1`|`3`|`4`|`3`|`3`|
|`3.6`|`3`|`4`|`4`|`3`|
|`-1.1`|`-2`|`-1`|`-1`|`-1`|
|`-1.6`|`-2`|`-1`|`-2`|`-1`|


我们有 `1.2345`，并且想把它舍入到小数点后两位，仅得到 `1.23`。
有两种方式可以实现这个需求：
1. 乘除法
    例如，要将数字舍入到小数点后两位，我们可以将数字乘以 `100`，调用舍入函数，然后再将其除回。
2. 函数 [toFixed(n)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed) 将数字舍入到小数点后 `n` 位，并以字符串形式返回结果。类似于 `Math.round`
```javascript
let num = 12.345;

log(Math.floor(num * 100));//1234
log(num.toFixed(9));//12.345000000
```

 不精确的计算：
 如果一个数字真的很大，则可能会溢出 64 位存储，变成一个特殊的数值 `Infinity`
 如果我们检查 `0.1` 和 `0.2` 的总和是否为 `0.3`，我们会得到 `false`。

```javascript
log(0.1 + 0.2 == 0.3);//false
log(0.1 + 0.2); //0.30000000000000004
log(0.3);//0.3
```

十进制转二进制计算后再转十进制输出导致的误差，二进制无法准确的存储0.1与0.2

```javascript
function equal (a, b) {
	return Math.abs(a - b) < Number.EPSILON
}
```

##### 浮点数的底层实现
1. 最大数（`Number.MAX_VALUE`）
- **值**：`1.7976931348623157e+308`
- **原理**：
  IEEE 754 双精度浮点数的结构为：1位符号位 + 11位指数位 + 52位尾数位。
  - 指数位最大值为 `2^11 - 1 = 2047`，但标准规定指数 `2047` 用于表示特殊值（如 `Infinity`），因此有效最大指数为 `2046`。
  - 尾数位最大值为 `2^52 - 1`（全为1），尾数值为 `1 + (2^52 - 1)/2^52 ≈ 2`（接近2但小于2）。
  - 计算公式：`(2 - 2^-52) × 2^2046 ≈ 1.7976931348623157e+308`。

- **含义**：大于此值的数会被表示为 `Infinity`（无穷大）。
```javascript
  console.log(Number.MAX_VALUE); // 1.7976931348623157e+308
  console.log(Number.MAX_VALUE * 2); // Infinity
```


2. 最大安全整数（`Number.MAX_SAFE_INTEGER`）
- **值**：`9007199254740991`（即 `2^53 - 1`）
- **原理**：
  双精度浮点数的尾数位只有52位（加上隐含的1位，共53位有效数字）。这意味着：
  - 对于整数，只有在 `-2^53` 到 `2^53` 范围内的数，才能被**精确表示**。
  - 超过 `2^53` 的整数可能无法与相邻整数区分（例如 `2^53 + 1` 会被舍入为 `2^53`）。

- **含义**：“安全”指该整数及以内的所有整数都能被精确表示，且不会与其他整数混淆。
```javascript
  console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991
  console.log(2 **53 === 2** 53 + 1); // true（两者无法区分，均为 9007199254740992）
```

3. 最小精度值（`Number.EPSILON`）
- **值**：`2.220446049250313e-16`（即 `2^-52`）
- **原理**：
  尾数位的最小精度单位是 `2^-52`。对于 `1` 这个数，它与下一个可表示的浮点数（`1 + 2^-52`）之间的差值就是 `EPSILON`。

- **含义**：表示 JavaScript 中能区分的两个相邻浮点数的最小差值，常用于判断浮点数运算的精度误差。
```javascript
  console.log(Number.EPSILON); // 2.220446049250313e-16

  // 示例：判断两个浮点数是否近似相等
  function isEqual(a, b) {
    return Math.abs(a - b) < Number.EPSILON;
  }
  console.log(0.1 + 0.2 === 0.3); // false（浮点数误差）
  console.log(isEqual(0.1 + 0.2, 0.3)); // true（通过 EPSILON 判断）
```

##### 总结
| 常量                  | 值                     | 本质原因                          | 用途场景                     |
|-----------------------|------------------------|-----------------------------------|------------------------------|
| `MAX_VALUE`           | ~1.797e+308            | 64位浮点数的指数位和尾数位限制    | 判断数值是否溢出为无穷大     |
| `MAX_SAFE_INTEGER`    | 2^53 - 1               | 53位有效数字的精度限制            | 确保整数运算精确性           |
| `EPSILON`             | 2^-52                  | 浮点数的最小精度单位              | 处理浮点数运算的精度误差     |

这些限制源于 JavaScript 对浮点数的底层实现，了解它们有助于避免数值计算中的常见陷阱（如精度丢失、整数溢出）。

使用二进制数字系统无法 **精确** 存储 **_0.1_ 或 _0.2_**
最可靠的方法是借助方法 [toFixed(n)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed) 对结果进行舍入

```javascript
let money = 0.1 + 0.2;
let fixedMoney = +money.toFixed(2);

log(fixedMoney);//0.3
log(typeof fixedMoney);//number
```

特殊的数值：
- `Infinity`（和 `-Infinity`）是一个特殊的数值，比任何数值都大（小）。
- `NaN` 代表一个 error。

它们属于 `number` 类型，但不是“普通”数字，有用于检查它们的特殊函数：
- `isNaN(value)` 将其参数转换为数字，然后测试它是否为 `NaN`
- 我们不能只使用 `=== NaN` 比较吗？很不幸，这不行。值 “NaN” 是独一无二的，它不等于任何东西，包括它自身
```javascript
log(NaN == NaN);//false
log(NaN === NaN);//false
log(isNaN(Infinity), isNaN(-Infinity));//Infinity和-Infinity都是数字
```

- `isFinite(value)` 将其参数转换为数字，如果是常规数字而不是 `NaN/Infinity/-Infinity`，则返回 `true`
- 在所有数字函数中，包括 `isFinite`，空字符串或仅有空格的字符串均被视为 `0`

**parseInt parseFloat**:
使用加号 `+` 或 `Number()` 的数字转换是严格的。如果一个值不完全是一个数字，就会失败.
唯一的例外是字符串开头或结尾的空格，因为它们会被忽略。

`parseInt` 和 `parseFloat` 可以从字符串中“读取”数字，直到无法读取为止。如果发生 error，则返回收集到的数字。函数 `parseInt` 返回一个整数，而 `parseFloat` 返回一个浮点数
如 CSS 中的 `"100px"` 或 `"12pt"`。并且，在很多国家，货币符号是紧随金额之后的，所以我们有 `"19€"`，并希望从中提取出一个数值

`parseInt()` 函数具有可选的第二个参数。它指定了数字系统的基数，因此 `parseInt` 还可以解析十六进制数字、二进制数字等的字符串

```javascript
log(parseInt('20px', 10));//20
log(typeof parseInt('20px', 10));//number
```

JavaScript 有一个内建的 [Math](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Math) 对象，它包含了一个小型的数学函数和常量库。
`Math.random()`
返回一个从 0 到 1 的随机数（不包括 1）。

```javascript
function random(min,max){
	return min + Math.random() * (max - min)
}
```

`Math.max(a, b, c...)` 和 `Math.min(a, b, c...)`
从任意数量的参数中返回最大值和最小值。

`Math.pow(n, power)`
返回 `n` 的给定（power）次幂。

### 现代JS教程与阮一峰ES6 · 1数据类型与变量/String
##### String
**一、获取与查找**

1. **`charAt(index)`**
   返回指定索引位置的字符（索引从0开始）。

```javascript
   const str = "hello";
   console.log(str.charAt(1)); // "e"（索引1的字符）
   console.log(str.charAt(10)); // ""（索引超出范围返回空字符串）
```

2. **`indexOf(searchValue, fromIndex)`**
   查找子串首次出现的索引，未找到返回`-1`，`fromIndex`指定起始位置。

```javascript
   const str = "hello world";
   console.log(str.indexOf("o")); // 4（首次出现"o"的位置）
   console.log(str.indexOf("o", 5)); // 7（从索引5开始查找）
```

3. **`lastIndexOf(searchValue)`**
   查找子串最后一次出现的索引，未找到返回`-1`。

```javascript
   const str = "hello world";
   console.log(str.lastIndexOf("o")); // 7（最后出现"o"的位置）
```

4. **`includes(searchValue, fromIndex)`**
   判断字符串是否包含指定子串，返回布尔值。

```javascript
   const str = "hello";
   console.log(str.includes("ll")); // true
   console.log(str.includes("xyz")); // false
```

5. **`startsWith(searchValue, fromIndex)` / `endsWith(searchValue, length)`**
   判断字符串是否以指定子串开头/结尾。

```javascript
   const str = "hello world";
   console.log(str.startsWith("he")); // true
   console.log(str.endsWith("ld")); // true
   console.log(str.endsWith("lo", 5)); // true（只看前5个字符"hello"）
```


**二、截取与分割**

1. **`slice(startIndex, endIndex)`**
   截取从`startIndex`到`endIndex`（不包含）的子串，支持负数索引（从末尾计算）。

```javascript
   const str = "abcdef";
   console.log(str.slice(1, 4)); // "bcd"（索引1到3）
   console.log(str.slice(-3)); // "def"（从倒数第3位到结尾）
```

2. **`substring(startIndex, endIndex)`**
   类似`slice`，但不支持负数索引，且自动调整参数顺序（如`start > end`则交换）。

```javascript
   const str = "abcdef";
   console.log(str.substring(4, 1)); // "bcd"（自动交换为1到4）
```

3. **`split(separator, limit)`**
   按分隔符分割字符串为数组，`limit`限制返回的数组长度。

```javascript
   const str = "apple,banana,orange";
   console.log(str.split(",")); // ["apple", "banana", "orange"]
   console.log(str.split(",", 2)); // ["apple", "banana"]（只取前2个）
```


**三、转换与修改**

1. **`toUpperCase()` / `toLowerCase()`**
   转换字符串为全大写/全小写。

```javascript
   const str = "Hello World";
   console.log(str.toUpperCase()); // "HELLO WORLD"
   console.log(str.toLowerCase()); // "hello world"
```

2. **`trim()` / `trimStart()` / `trimEnd()`**
   去除字符串两端/开头/结尾的空白字符（空格、换行等）。

```javascript
   const str = "  hello  ";
   console.log(str.trim()); // "hello"（去除两端空白）
   console.log(str.trimStart()); // "hello  "（仅去除开头空白）
```

3. **`replace(searchValue, replacement)`**
   替换匹配的子串（默认只替换第一个匹配项，可用正则`/g`全局替换）。

```javascript
   const str = "cat dog cat";
   console.log(str.replace("cat", "bird")); // "bird dog cat"（替换第一个）
   console.log(str.replace(/cat/g, "bird")); // "bird dog bird"（全局替换）
```

4. **`repeat(count)`**
   将字符串重复`count`次并返回新字符串。

```javascript
   const str = "ab";
   console.log(str.repeat(3)); // "ababab"
```


**四、其他常用方法**

1. **`length`（属性）**
   返回字符串的长度（字符数量）。

```javascript
   const str = "hello";
   console.log(str.length); // 5
```

2. **`padStart(targetLength, padString)` / `padEnd(targetLength, padString)`**
   在字符串开头/结尾填充指定字符，直到达到目标长度。

```javascript
   const str = "123";
   console.log(str.padStart(5, "0")); // "00123"（开头补0至长度5）
   console.log(str.padEnd(5, "-")); // "123--"（结尾补-至长度5）
```

3. **`concat(str1, str2, ...)`**
   拼接多个字符串（推荐直接使用`+`或模板字符串更简洁）。

```javascript
   const str1 = "hello";
   const str2 = "world";
   console.log(str1.concat(" ", str2)); // "hello world"
```


**总结**
`String`的API覆盖了字符串的查找、截取、转换、修改等常见操作，实际开发中可根据场景选择：
- 查找子串用`includes`、`indexOf`；
- 截取用`slice`（推荐，支持负数索引）；
- 格式化用`trim`、`toUpperCase`、`padStart`等；
- 替换用`replace`（结合正则更强大）。

以下是 `str.toUpperCase()` 中实际发生的情况：
1. 字符串 `str` 是一个原始值。因此，在访问其属性时，会创建一个包含字符串字面值的特殊对象，并且具有可用的方法，例如 `toUpperCase()`。
2. 该方法运行并返回一个新的字符串（由 `alert` 显示）。
3. 特殊对象被销毁，只留下原始值 `str`。

所以原始类型可以提供方法，但它们依然是轻量级的。
JavaScript 引擎高度优化了这个过程。它甚至可能跳过创建额外的对象。但是它仍然必须遵守规范，并且表现得好像它创建了一样。

特殊的原始类型 `null` 和 `undefined` 是例外。它们没有对应的“对象包装器”，也没有提供任何方法。从某种意义上说，它们是“最原始的”。

##### 字符串
在 JavaScript 中，文本数据被以字符串形式存储，单个字符没有单独的类型。
字符串的内部格式始终是 [UTF-16](https://en.wikipedia.org/wiki/UTF-16)，它不依赖于页面编码。

字符串可以包含在单引号、双引号或反引号中
反引号允许我们通过 `${…}` 将任何表达式嵌入到字符串中。反引号的另一个优点是它们允许字符串跨行

```javascript
log(`shit
    shjit
    shit
    `);
/**
 * shit
    shjit
    shit
 */
```

反引号还允许我们在第一个反引号之前指定一个“模版函数”。语法是：`` func`string` ``。函数 `func` 被自动调用，接收字符串和嵌入式表达式，并处理它们。你可以在 [docs](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Template_literals#Tagged_template_literals) 中阅读更多关于它们的信息。这叫做 “tagged templates”。此功能可以更轻松地将字符串包装到自定义模版或其他函数中，但这很少使用。

|字符|描述|
|---|---|
|`\n`|换行|
|`\r`|在 Windows 文本文件中，两个字符 `\r\n` 的组合代表一个换行。而在非 Windows 操作系统上，它就是 `\n`。这是历史原因造成的，大多数的 Windows 软件也理解 `\n`。|
|`\'`, `\"`|引号|
|`\\`|反斜线|
|`\t`|制表符|
|`\b`, `\f`, `\v`|退格，换页，垂直标签 —— 为了兼容性，现在已经不使用了。|
|`\xXX`|具有给定十六进制 Unicode `XX` 的 Unicode 字符，例如：`'\x7A'` 和 `'z'` 相同。|
|`\uXXXX`|以 UTF-16 编码的十六进制代码 `XXXX` 的 Unicode 字符，例如 `\u00A9` —— 是版权符号 `©` 的 Unicode。它必须正好是 4 个十六进制数字。|
|`\u{X…XXXXXX}`（1 到 6 个十六进制字符）|具有给定 UTF-32 编码的 Unicode 符号。一些罕见的字符用两个 Unicode 符号编码，占用 4 个字节。这样我们就可以插入长代码了。|

```javascript
log("\u00A9");//©
log("\u{20331}");//𠌱
log("\u{1f60d}");//😍
log("\u{1F60D}");//😍 大小写一样
```

字符串长度：
`length` 属性表示字符串长度。这是一个属性**不是函数**。

```javascript
const str = 'shit';
log(str.length);//4
```

要获取在 `pos` 位置的一个字符，可以使用方括号 `[pos]` 或者调用 [str.charAt(pos)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/charAt) 方法。第一个字符从零位置开始
方括号是获取字符的一种现代化方法，而 `charAt` 是历史原因才存在的。
它们之间的唯一区别是，如果没有找到字符，`[]` 返回 `undefined`，而 `charAt` 返回一个空字符串

```javascript
log(str[5]);//undefined
log(str.charAt(5));// "" 空的字符串
```

在 JavaScript 中，字符串不可更改。**改变字符是不可能的**。

[toLowerCase()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/toLowerCase) 和 [toUpperCase()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/toUpperCase) 方法可以改变大小写

查找子字符串：
第一个方法是 [str.indexOf(substr, pos)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/indexOf)。
它从给定位置 `pos` 开始，在 `str` 中查找 `substr`，如果没有找到，则返回 `-1`，否则返回匹配成功的位置。可选的第二个参数允许我们从一个给定的位置开始检索。

还有一个类似的方法 [str.lastIndexOf(substr, position)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/lastIndexOf)，它从字符串的末尾开始搜索到开头。
它会以相反的顺序列出这些事件。

在 `if` 测试中 `indexOf` 有一点不方便。我们不能像这样把它放在 `if` 中
![[Pasted image 20250624185221.png]]
这里使用的一个老技巧是 [bitwise NOT](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_NOT) `~` 运算符。它将数字转换为 32-bit 整数（如果存在小数部分，则删除小数部分），然后对其二进制表示形式中的所有位均取反。

实际上，这意味着一件很简单的事儿：对于 32-bit 整数，`~n` 等于 `-(n+1)`。不推荐使用。

更现代的方法 [str.includes(substr, pos)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/includes) 根据 `str` 中是否包含 `substr` 来返回 `true/false`。
如果我们需要检测匹配，但不需要它的位置，那么这是正确的选择：
```javascript
log(str.includes("s"));//true

```

方法 [str.startsWith](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/startsWith) 和 [str.endsWith](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith) 的功能与其名称所表示的意思相同


JavaScript 中有三种获取字符串的方法：`substring`、`substr` 和 `slice`。
`str.slice(start [, end])`
返回字符串从 `start` 到（但不包括）`end` 的部分。如果没有第二个参数，`slice` 会一直运行到字符串末尾。`start/end` 也有可能是负值。它们的意思是起始位置从字符串结尾计算。

`str.substring(start [, end])`
返回字符串从 `start` 到（但不包括）`end` 的部分。
这与 `slice` 几乎相同，但它允许 `start` 大于 `end`。

`str.substr(start [, length])`
返回字符串从 `start` 开始的给定 `length` 的部分。
与以前的方法相比，这个允许我们指定 `length` 而不是结束位置
第一个参数可能是负数，从结尾算起

|方法|选择方式……|负值参数|
|---|---|---|
|`slice(start, end)`|从 `start` 到 `end`（不含 `end`）|允许|
|`substring(start, end)`|从 `start` 到 `end`（不含 `end`）|负值被视为 `0`|
|`substr(start, length)`|从 `start` 开始获取长为 `length` 的字符串|允许 `start` 为负数|
仅仅记住这三种方法中的 `slice` 就足够了。

JavaScript 共有 6 种方法可以表示一个字符。

```javascript
'\z' === 'z'  // true
'\172' === 'z' // true
'\x7A' === 'z' // true
'\u007A' === 'z' // true
'\u{7A}' === 'z' // true
```

为字符串添加了遍历器接口（详见《Iterator》一章），使得字符串可以被`for...of`循环遍历。

```javascript
for (let codePoint of 'foo') {
  console.log(codePoint)
}
// "f"
// "o"
// "o"
```

除了遍历字符串，这个遍历器最大的优点是可以识别大于`0xFFFF`的码点，传统的`for`循环无法识别这样的码点。

```javascript
let text = String.fromCodePoint(0x20BB7);

for (let i = 0; i < text.length; i++) {
  console.log(text[i]);
}
// " "
// " "

for (let i of text) {
  console.log(i);
}
// "𠮷"
```

上面代码中，字符串`text`只有一个字符，但是`for`循环会认为它包含两个字符（都不可打印），而`for...of`循环会正确识别出这一个字符。

模板字符串（template string）是增强版的字符串，用反引号（`）标识。它可以当作普通字符串使用，也可以用来定义多行字符串，或者在字符串中嵌入变量。

```javascript
// 普通字符串
`In JavaScript '\n' is a line-feed.`

// 多行字符串
`In JavaScript this is
 not legal.`

console.log(`string text line 1
string text line 2`);

// 字符串中嵌入变量
let name = "Bob", time = "today";
`Hello ${name}, how are you ${time}?`
```

上面代码中的模板字符串，都是用反引号表示。如果在模板字符串中需要使用反引号，则前面要用反斜杠转义。在${}中可以放入任意的表达式，还能调用函数。如果大括号中的值不是字符串，将按照一般的规则转为字符串。比如，大括号中是一个对象，将默认调用对象的`toString`方法。甚至还能嵌套使用

如果使用模板字符串表示多行字符串，所有的空格和缩进都会被保留在输出之中。

```javascript
$('#list').html(`
<ul>
  <li>first</li>
  <li>second</li>
</ul>
`);
```

上面代码中，所有模板字符串的空格和换行，都是被保留的，比如`<ul>`标签前面会有一个换行。如果你不想要这个换行，可以使用`trim`方法消除它。

```javascript
$('#list').html(`
<ul>
  <li>first</li>
  <li>second</li>
</ul>
`.trim());
```

ES6 提供了`String.fromCodePoint()`方法，可以识别大于`0xFFFF`的字符，弥补了`String.fromCharCode()`方法的不足。在作用上，正好与下面的`codePointAt()`方法相反。

```javascript
String.fromCodePoint(0x20BB7)
// "𠮷"
String.fromCodePoint(0x78, 0x1f680, 0x79) === 'x\uD83D\uDE80y'
// true
```

JavaScript 内部，字符以 UTF-16 的格式储存，每个字符固定为`2`个字节。对于那些需要`4`个字节储存的字符（Unicode 码点大于`0xFFFF`的字符），JavaScript 会认为它们是两个字符。

```javascript
var s = "𠮷";

s.length // 2
s.charAt(0) // ''
s.charAt(1) // ''
s.charCodeAt(0) // 55362
s.charCodeAt(1) // 57271
```

字符可以通过charCodeAt方法获取其==Unicode==编码

基本上，ES6 的`class`可以看作只是一个语法糖，它的绝大部分功能，ES5 都可以做到，新的`class`写法只是让对象原型的写法更加清晰、更像面向对象编程的语法而已。上面的代码用 ES6 的`class`改写，就是下面这样。

```javascript
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  toString() {
    return '(' + this.x + ', ' + this.y + ')';
  }
}
```

由于类的方法都定义在`prototype`对象上面，所以类的新方法可以添加在`prototype`对象上面。`Object.assign()`方法可以很方便地一次向类添加多个方法。

```javascript
class Point {
  constructor(){
    // ...
  }
}

Object.assign(Point.prototype, {
  toString(){},
  toValue(){}
});
```

`constructor()`方法是类的默认方法，通过`new`命令生成对象实例时，自动调用该方法。一个类必须有`constructor()`方法，如果没有显式定义，一个空的`constructor()`方法会被默认添加。

```javascript
class Point {
}

// 等同于
class Point {
  constructor() {}
}
```

### 廖雪峰教程 · 3快速入门/3.3 字符串
##### 字符串
JavaScript的字符串就是用`''`或`""`括起来的字符表示。

如果`'`本身也是一个字符，那就可以用`""`括起来，比如`"I'm OK"`包含的字符是`I`，`'`，`m`，空格，`O`，`K`这6个字符。

如果字符串内部既包含`'`又包含`"`怎么办？可以用转义字符`\`来标识，比如：
```javascript
'I\'m \"OK\"!'; // I'm "OK"!
```

表示的字符串内容是：`I'm "OK"!`

转义字符`\`可以转义很多字符，比如`\n`表示换行，`\t`表示制表符，字符`\`本身也要转义，所以`\\`表示的字符就是`\`。

ASCII字符可以以`\x##`形式的十六进制表示，例如：
```javascript
'\x41'; // 完全等同于 'A'
```

还可以用`\u####`表示一个Unicode字符：
```javascript
'\u4e2d\u6587'; // 完全等同于 '中文'
```

##### 多行字符串
由于多行字符串用`\n`写起来比较费事，所以最新的ES6标准新增了一种多行字符串的表示方法，用反引号`...`表示：
```javascript
`这是一个
多行
字符串`;
```

_注意_：反引号在键盘的`ESC`下方，数字键`1`的左边：
```text
┌─────┐ ┌─────┬─────┬─────┬─────┐
│ ESC │ │ F1  │ F2  │ F3  │ F4  │
└─────┘ └─────┴─────┴─────┴─────┘
┌─────┬─────┬─────┬─────┬─────┐
│  ~  │  !  │  @  │  #  │  $  │
│  `  │  1  │  2  │  3  │  4  │
├─────┴──┬──┴──┬──┴──┬──┴──┬──┘
│        │     │     │     │
│  tab   │  Q  │  W  │  E  │
├────────┴──┬──┴──┬──┴──┬──┘
│           │     │     │
│ caps lock │  A  │  S  │
└───────────┴─────┴─────┘
```

##### 模板字符串
要把多个字符串连接起来，可以用`+`号连接：
```javascript
let name = '小明';
let age = 20;
let message = '你好, ' + name + ', 你今年' + age + '岁了!';
alert(message);
```

如果有很多变量需要连接，用`+`号就比较麻烦。ES6新增了一种模板字符串，表示方法和上面的多行字符串一样，但是它会自动替换字符串中的变量：
```javascript
let name = '小明';
let age = 20;
let message = `你好, ${name}, 你今年${age}岁了!`;
alert(message);
```

##### 操作字符串
获取字符串长度：
```javascript
let s = 'Hello, world!';
s.length; // 13
```

要获取字符串某个指定位置的字符，使用类似Array的下标操作，索引号从0开始：
```javascript
let s = 'Hello, world!';

s[0]; // 'H'
s[6]; // ' '
s[7]; // 'w'
s[12]; // '!'
s[13]; // undefined 超出范围的索引不会报错，但一律返回undefined
```

_需要特别注意的是_，字符串是不可变的，如果对字符串的某个索引赋值，不会有任何错误，但是，也没有任何效果：
```javascript
let s = 'Test';
s[0] = 'X';
console.log(s); // s仍然为'Test'
```

JavaScript为字符串提供了一些常用方法，注意，调用这些方法本身不会改变原有字符串的内容，而是返回一个新字符串：
##### toUpperCase
`toUpperCase()`把一个字符串全部变为大写：
```javascript
let s = 'Hello';
s.toUpperCase(); // 返回'HELLO'
```

##### toLowerCase
`toLowerCase()`把一个字符串全部变为小写：
```javascript
let s = 'Hello';
let lower = s.toLowerCase(); // 返回'hello'并赋值给变量lower
lower; // 'hello'
```

##### indexOf
`indexOf()`会搜索指定字符串出现的位置：
```javascript
let s = 'hello, world';
s.indexOf('world'); // 返回7
s.indexOf('World'); // 没有找到指定的子串，返回-1
```

##### substring
`substring()`返回指定索引区间的子串：
```javascript
let s = 'hello, world'
s.substring(0, 5); // 从索引0开始到5（不包括5），返回'hello'
s.substring(7); // 从索引7开始到结束，返回'world'
```
