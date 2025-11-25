#### String
---
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



---

### 
### 字符串
---
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

