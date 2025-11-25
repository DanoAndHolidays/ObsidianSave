# Number API
---
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

### 数字类型
---
JavaScript 中的常规数字以 64 位的格式 [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754) 存储，就是“双精度浮点数”
常规整数不能安全地超过 `2^53-1` 或小于 `-2^53-1`。由于仅在少数特殊领域才会用到 BigInt，因此我们在特殊的章节 [BigInt](https://zh.javascript.info/bigint) 中对其进行了介绍。

使用下划线更具可读性。
```javascript
log(1_000_000);//1000000
```

使用**e**：
```JavaScript
let billion 1e9;//10亿
let mcs 1e-6;
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

### 浮点数的底层实现
---
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