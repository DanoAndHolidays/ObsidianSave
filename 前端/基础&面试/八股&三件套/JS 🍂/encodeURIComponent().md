# encodeURIComponent()
> Last Format Time：10/8/2026 23:35:46

它是 JavaScript 内置的 URI 组件编码函数。

主要解决的问题是：某个字符串中的特殊字符可能被 URL 解析器误认为是 URL 结构的一部分。

例如搜索词：
```text
const keyword = "React & Vue";

const url = `/search?q=${encodeURIComponent(keyword)}`;

// /search?q=React%20%26%20Vue
```

`&` 被编码为 `%26`，避免被当作查询参数分隔符。

|API|用途|
|---|---|
|`encodeURI()`|编码完整 URI，保留许多 URI 结构字符|
|`encodeURIComponent()`|编码 URI 的单个组成部分，对特殊字符编码更严格|
|`decodeURIComponent()`|解码被编码的 URI 组成部分|

工程里处理查询参数，更推荐：
```text
const params = new URLSearchParams({
  q: "React & Vue",
  page: "1"
});

const url = `/search?${params}`;
```

`URLSearchParams` 会负责查询参数的编码和序列化。