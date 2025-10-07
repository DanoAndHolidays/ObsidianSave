### Date
---
调用 `new Date()` 来创建一个新的 `Date` 对象。在调用时可以带有一些参数，如下所示：
不带参数 —— 创建一个表示当前日期和时间的 `Date` 对象

`new Date(milliseconds)`
创建一个 `Date` 对象，其时间等于 1970 年 1 月 1 日 UTC+0 之后经过的毫秒数milliseconds（1/1000 秒）。

`new Date(datestring)`
如果只有一个参数，并且是字符串，那么它会被自动解析。该算法与 `Date.parse` 所使用的算法相同

`new Date(year, month, date, hours, minutes, seconds, ms)`
使用当前时区中的给定组件创建日期。只有前两个参数是必须的。
- `year` 应该是四位数。为了兼容性，也接受 2 位数，并将其视为 `19xx`，例如 `98` 与 `1998` 相同，但强烈建议始终使用 4 位数。
- `month` 计数从 `0`（一月）开始，到 `11`（十二月）结束。
- `date` 是当月的具体某一天，如果缺失，则为默认值 `1`。
- 如果 `hours/minutes/seconds/ms` 缺失，则均为默认值 `0`。

从 `Date` 对象中访问年、月等信息有多种方式：
[getFullYear()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getFullYear)
获取年份（4 位数）很多 JavaScript 引擎都实现了一个非标准化的方法 `getYear()`。不推荐使用这个方法。它有时候可能会返回 2 位的年份信息。**永远不要使用它**。要获取年份就使用 `getFullYear()`。
[getMonth()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getMonth)
获取月份，**从 0 到 11**。
[getDate()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getDate)
获取当月的具体日期，从 1 到 31，这个方法名称可能看起来有些令人疑惑。
[getHours()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getHours)，[getMinutes()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getMinutes)，[getSeconds()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getSeconds)，[getMilliseconds()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getMilliseconds)
获取相应的时间组件。

另外，我们还可以获取一周中的第几天：
[getDay()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getDay)
获取一周中的第几天，从 `0`（星期日）到 `6`（星期六）。第一天始终是星期日，在某些国家可能不是这样的习惯，但是这不能被改变。

[getTime()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getTime)
返回日期的时间戳 —— 从 1970-1-1 00:00:00 UTC+0 开始到现在所经过的毫秒数。

[getTimezoneOffset()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset)
返回 UTC 与本地时区之间的时差，以分钟为单位

下列方法可以设置日期/时间组件：
- [`setFullYear(year, [month], [date])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setFullYear)
- [`setMonth(month, [date])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setMonth)
- [`setDate(date)`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setDate)
- [`setHours(hour, [min], [sec], [ms])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setHours)
- [`setMinutes(min, [sec], [ms])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setMinutes)
- [`setSeconds(sec, [ms])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setSeconds)
- [`setMilliseconds(ms)`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setMilliseconds)
- [`setTime(milliseconds)`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setTime)（使用自 1970-01-01 00:00:00 UTC+0 以来的毫秒数来设置整个日期）
以上方法除了 `setTime()` 都有 UTC 变体，例如：`setUTCHours()`。

**自动校准** 是 `Date` 对象的一个非常方便的特性。
假设我们要在日期 “28 Feb 2016” 上加 2 天。结果可能是 “2 Mar” 或 “1 Mar”，因为存在闰年。但是我们不需要考虑这些，只需要直接加 2 天，剩下的 `Date` 对象会帮我们处理

```javascript
let date = new Date();
date.setDate(date.getDate() + 100);

console.log(date);
//2025-10-02T14:40:25.361Z
```

当 `Date` 对象被转化为数字时，得到的是对应的时间戳，与使用 `date.getTime()` 的结果相同
日期可以相减，相减的结果是以毫秒为单位时间差。
```javascript
let start = new Date(); // 开始测量时间

// do the job
for (let i = 0; i < 100000000; i++) {
    let doSomething = i * i * i;
}

let end = new Date(); // 结束测量时间

console.log(`The loop took ${end - start} ms`);
//The loop took 41 ms
```

如果我们仅仅想要测量时间间隔，我们不需要 `Date` 对象
```javascript
let start = Date.now(); // 开始测量时间

// do the job
for (let i = 0; i < 100000000; i++) {
    let doSomething = i * i * i;
}

let end = Date.now(); // 结束测量时间

console.log(`The loop took ${end - start} ms`);
//The loop took 43 ms
```

它相当于 `new Date().getTime()`，但它不会创建中间的 `Date` 对象。因此它更快，而且不会对垃圾回收造成额外的压力。
这种方法很多时候因为方便，又或是因性能方面的考虑而被采用，例如使用 JavaScript 编写游戏或其他的特殊应用场景。

**Date.prese()**:
字符串的格式应该为：`YYYY-MM-DDTHH:mm:ss.sssZ`，其中：
- `YYYY-MM-DD` —— 日期：年-月-日。
- 字符 `"T"` 是一个分隔符。
- `HH:mm:ss.sss` —— 时间：小时，分钟，秒，毫秒。
- 可选字符 `'Z'` 为 `+-hh:mm` 格式的时区。单个字符 `Z` 代表 UTC+0 时区。

简短形式也是可以的，比如 `YYYY-MM-DD` 或 `YYYY-MM`，甚至可以是 `YYYY`。

`Date.parse(str)` 调用会解析给定格式的字符串，并返回时间戳（自 1970-01-01 00:00:00 起所经过的毫秒数）。如果给定字符串的格式不正确，则返回 `NaN`。