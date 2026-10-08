# 日期时间格式化（DateTimeFormatter）💡
> Last Format Time：10/8/2026 23:35:46

---
## 日期时间格式化（DateTimeFormatter）
日期格式化通过特定的字符表示年、月、日、时、分、秒。

注意大小写：不同大小写可能代表不同含义。

以 Java 的 `DateTimeFormatter` 和 `SimpleDateFormat` 为例：

|格式|含义|示例|
|---|---|---|
|`yyyy`|年份（4 位）|2026|
|`MM`|月份（补零）|01～12|
|`M`|月份（不补零）|1～12|
|`dd`|日期（补零）|01～31|
|`HH`|小时（24 小时制）|00～23|
|`hh`|小时（12 小时制）|01～12|
|`mm`|分钟|00～59|
|`ss`|秒钟|00～59|
|`SSS`|毫秒（3 位）|000～999|
|`a`|上午 / 下午标记|AM / PM|

- `MM`：月份（Month），`mm`：分钟（minute）。
- `HH`：24 小时制，`hh`：12 小时制。
- `M` 和 `MM`：区别在于是否补零，例如 `3` 和 `03`。
- `H` 和 `HH`：区别在于是否补零，例如 `9` 和 `09`。

```java
LocalDateTime now = LocalDateTime.of(2026, 10, 8, 15, 5, 9);

DateTimeFormatter formatter =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

String result = now.format(formatter);

// 2026-10-08 15:05:09
```

12 小时制：
```java
DateTimeFormatter formatter =
    DateTimeFormatter.ofPattern("yyyy-MM-dd hh:mm:ss a");

// 2026-10-08 03:05:09 PM
```

1. 日期格式化规则不是 YAML 语法，而是由具体的日期格式化工具定义。
2. 不同语言、工具的格式化规则可能不同，例如 Java 使用 `yyyy`，Day.js 使用 `YYYY` 表示四位年份。
3. Java 中 `YYYY` 和 `yyyy` 含义不同：`YYYY` 是基于周的年份，跨年时可能出现意外结果，普通日期应使用 `yyyy`。

常用格式：`yyyy-MM-dd HH:mm:ss` 记住：`MM` 是月，`mm` 是分；`HH` 是 24 小时制，`hh` 是 12 小时制。