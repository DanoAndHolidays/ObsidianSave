# 空字符串与filter
> Last Format Time：7/14/2026 20:25:30

最后这句：

```ts
.filter(Boolean);
```

是为了**去掉空字符串**。

你的代码整体逻辑是：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

举几个例子就很容易理解。

### 正常情况
```ts
parseCommaList("a,b,c")
```

执行过程：

```ts
split(",")
// ["a", "b", "c"]

trim()
// ["a", "b", "c"]

filter(Boolean)
// ["a", "b", "c"]
```

没有变化。


### 有空格
```ts
parseCommaList("a, b, c ")
```

执行：

```ts
split(",")
// ["a", " b", " c "]

trim()
// ["a", "b", "c"]

filter(Boolean)
// ["a", "b", "c"]
```


### 连续两个逗号
```ts
parseCommaList("a,,c")
```

执行：

```ts
split(",")
// ["a", "", "c"]

trim()
// ["a", "", "c"]

filter(Boolean)
// ["a", "c"]
```

如果没有 `filter(Boolean)`，结果就是：

```ts
["a", "", "c"]
```

中间会多一个空字符串。


### 首尾有逗号
```ts
parseCommaList(",a,b,")
```

执行：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```


### 全都是空
```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

执行：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

---
## 为什么 `filter(Boolean)` 能过滤空字符串？
`Array.prototype.filter` 需要一个返回 `true/false` 的函数：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

实际上就是下面的简写：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

而 JavaScript 中：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

由于前面已经执行了 `trim()`，所以 `" "` 会变成 `""`，于是：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```


所以这段代码可以理解成：

```ts
const parseCommaList = (s: string): string[] =>
    s
        .split(",")          // 按逗号分割
        .map(item => item.trim()) // 去掉每项首尾空格
        .filter(Boolean);    // 去掉空字符串
```

两种写法效果一样，只是 `filter(Boolean)` 更简洁，也是 JavaScript/TypeScript 中非常常见的一种惯用写法。