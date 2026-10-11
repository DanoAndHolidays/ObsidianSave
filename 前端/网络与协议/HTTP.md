# HTTP
> Last Format Time：9/12/2026 17:40:49

HTTP（Hypertext Transfer Protocol，超文本传输协议）是应用层协议，采用==请求—响应模型==，用于传输网页、图片、音视频和 API 数据等

- 普通 HTTP API 主要按照请求—响应模式组织通信，但不代表：
	
	- HTTP 每次请求都必须重新建立 TCP 连接
	- HTTP 完全不能实现服务端推送
	- HTTP 无法进行长连接


- 特点：
	
	- **无状态**：HTTP 本身不自动保存前后请求之间的业务会话状态。应用可以通过 Cookie、Session、Token 等机制识别用户和维护登录状态。
	
	- **媒体无关**：正文可以是文本或二进制数据，通常通过 `Content-Type` 描述媒体类型，例如 `application/json`、`image/png`
	
	- **支持连接复用（八股是无连接）**：不能笼统地说“HTTP 是无连接协议”。HTTP/1.0 默认使用短连接，HTTP/1.1 默认使用==持久连接==，HTTP/2 和 HTTP/3 支持==多路复用（并发传输多个请求响应流，提高连接利用率）==


---
## 特点与版本
### HTTP/0.9
早期单行协议（1991 年）

- 请求只有一行，使用 `GET` 获取 HTML。
- 没有请求头、响应头和状态码，响应直接返回内容。
- 缺少媒体类型和标准化错误状态表达能力。

### HTTP/1.0
丰富消息语义（1996 年）

- 引入状态码和头字段，支持 `GET`、`HEAD`、`POST` 等方法
- 通过 `Content-Type` 描述不同类型的内容
- **默认一个 TCP 连接处理一次请求—响应**；部分实现通过 `Keep-Alive` 扩展支持复用

### HTTP/1.1
默认==持久连接==

- **持久连接**：Keep-Alive，默认==复用 TCP 连接==，减少建连开销；需要关闭时可使用 `Connection: close`

- **管道化**：允许不等待前一个响应就发送后续请求，但同一连接必须按请求顺序返回响应，仍存在==应用层队头阻塞==，浏览器实际很少使用

- **分块传输编码**：`Transfer-Encoding: chunked` 允许在不知道正文总长度时逐块发送

- **虚拟主机**：请求必须带 `Host`，使服务器能够区分同一地址上的不同站点

“浏览器并发约 6 个请求”通常指 HTTP/1.x 下对同一主机的并行连接策略，不是管道化最多允许 6 个请求，也不是 HTTP 标准规定的固定上限

### HTTP/2
==二进制==分帧与==多路复用==

- **二进制分帧**：将消息编码为帧，以流 ID 区分不同请求与响应；分帧本身不是压缩

- **多路复用**：同一个 TCP 连接内，不同流的帧可以交错传输，无需按请求发起顺序完成所有响应![[Pasted image 20261011210510.png]]

- **HPACK 头部压缩**：减少头字段的传输开销，与正文的 gzip 压缩是两回事。

- **服务器推送**：协议定义了主动推送关联资源的机制，但不能当作浏览器中普遍可用的优化手段；Chrome 从 106 起默认禁用。[Chrome 官方说明](https://developer.chrome.com/blog/removing-push)

![[Pasted image 20250901170355.png]]

### HTTP/3
基于 QUIC（2022 年标准化）

- **QUIC 基于 UDP**，自身实现可靠传输、拥塞控制、流量控制等能力；不是直接用不可靠的 UDP 传输 HTTP 正文。

- **独立的流**：一个流丢包，不会仅因为传输层要求有序交付而阻塞其他流；同一流内部仍可能等待重传，各流仍共享连接的拥塞控制与带宽。

- **QPACK 头部压缩**：保留头部压缩能力，但不是直接沿用 HPACK。

- **连接建立**：通常可在 1-RTT 完成握手；有可用的会话恢复信息等条件时，可以发送 0-RTT 早期数据。0-RTT 不等于请求瞬间完成，也存在重放风险。

---
## URL 与 URI
https://www.zhihu.com/question/21950864

### URL
[Uniform Resource Locator](https://zhida.zhihu.com/search?content_id=58814154&content_type=Answer&match_order=1&q=Uniform+Resource+Locator&zhida_source=entity) 统一资源**定位符**
```text
https://example.com:8443/articles?id=123#comments
  └协议   └主机       └端口 └路径    └查询参数 └片段
```

| 部分 | 示例 | 说明 |
| --- | --- | --- |
| 协议（scheme） | `https` | 指定访问方式 |
| 主机（host） | `example.com` | 域名或 IP 地址 |
| 端口（port） | `8443` | 省略时，HTTP 默认 80，HTTPS 默认 443 |
| 路径（path） | `/articles` | 标识资源路径，HTTP(S) URL 的空路径访问时通常按 `/` 处理 |
| 查询参数（query） | `id=123` | 放在 `?` 后，多个参数通常使用 `&` 分隔 |
| 片段（fragment） | `comments` | 放在 `#` 后，由客户端处理，不随 HTTP 请求目标发给服务器 |

浏览器可显示中文 URL，但实际传输会进行相应编码。前端构造查询参数时可使用 `URL`、`URLSearchParams`，避免直接拼接导致编码错误。

### URI
[Uniform Resource Identifier](https://zhida.zhihu.com/search?content_id=58814154&content_type=Answer&match_order=1&q=Uniform+Resource+Identifier&zhida_source=entity) 统一资源**标志符**
统一资源标志符URI就是在某一规则下能把一个资源独一无二地标识出来

**大白话，就是**URI是抽象的定义，不管用什么方法表示，只要能定位一个资源，就叫URI，本来设想的的使用两种方法定位：URL，用地址定位



---
## 方法
| 方法      | 主要用途       | 是否安全 | 是否幂等 | 常见是否有 body |
| ------- | ---------- | ---- | ---- | ---------- |
| GET     | 获取资源       | 是    | 是    | 通常不带       |
| POST    | 提交/创建/触发动作 | 否    | 否    | 是          |
| PUT     | 整体替换       | 否    | 是    | 是          |
| PATCH   | 局部修改       | 否    | 通常否  | 是          |
| DELETE  | 删除资源       | 否    | 是    | 通常不需要      |
| HEAD    | 获取响应头      | 是    | 是    | 通常不带       |
| OPTIONS | 询问支持能力     | 是    | 是    | 通常不带       |
| CONNECT | 代理隧道       | 否    | 否    | 视实现而定      |
| TRACE   | 调试回显       | 是    | 是    | 通常不带       |
*这个主要是看业务，都用 POST 都可以呢，但是会失去很多真多 GET 的优化*

### 安全性与幂等性

- **安全（safe）**：方法的预期语义是读取，不要求修改服务器业务状态；不排除服务器记录访问日志等附带行为

- **幂等（idempotent）**：相同请求执行一次与执行多次，对服务器的**预期作用相同**，不要求每次响应内容或状态码相同

例如，连续两次 `DELETE /users/123`，可以分别返回 `204` 和 `404`，但预期结果都是该资源被删除，所以仍可符合幂等语义。[方法语义](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2)

| 常见方法      | 用途                  | 安全  | 幂等          |
| --------- | ------------------- | --- | ----------- |
| `GET`     | 获取资源的表示             | 是   | 是           |
| `HEAD`    | 获取类似 GET 的响应头，不返回正文 | 是   | 是           |
| `POST`    | 提交数据，由目标资源处理        | 否   | 不保证         |
| `PUT`     | 创建或整体替换目标资源的状态      | 否   | 是           |
| `PATCH`   | 对资源进行部分修改           | 否   | 不保证，取决于修改操作 |
| `DELETE`  | 删除目标资源              | 否   | 是           |
| `OPTIONS` | 查询通信选项，也用于 CORS 预检  | 是   | 是           |

### GET 与 POST 的区别
| 维度 | GET | POST |
| --- | --- | --- |
| 主要用途 | 获取数据 | 提交数据供处理，不限于创建资源或提交表单 |
| 安全与幂等 | 安全、幂等 | 不保证安全或幂等；业务可通过去重机制实现幂等 |
| 数据位置 | 常用 URL 查询参数 | 常用请求体，也可以同时带 URL 查询参数 |
| 请求体 | 没有通用语义；浏览器 Fetch API 不允许 GET 带 body | 可通过 `Content-Type` 描述 JSON、表单、二进制等内容 |
| 缓存 | 响应通常可缓存，是否存储和复用还取决于缓存规则 | 规范在特定条件下允许缓存，但常见缓存实现通常只支持 GET、HEAD |
| 书签与分享 | URL 可表达查询条件，适合分享 | 收藏 URL 不会保存和重放 POST 的请求体 |
| 数据大小 | 受浏览器、代理和服务器等对 URL 的限制 | 请求体也受服务器、网关、框架等配置限制，并非无限大 |
| 隐私暴露面 | URL 可能进入历史记录、日志等位置 | body 不直接显示在地址栏，但仍可被开发者工具查看、被程序构造或修改 |

---
## HTTP/1.1 报文结构
### 请求报文

1. 请求行：`方法 请求目标 HTTP版本`

2. 请求头：每行一个 `字段名: 值`

3. 空行：分隔头部与正文

4. 请求体：可选，取决于具体请求

```http
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json
Content-Length: 46

{"name":"John Doe","email":"john@example.com"}
```

### 响应报文

1. 状态行：`HTTP版本 状态码 原因短语`

2. 响应头

3. 空行

4. 响应体：是否存在取决于请求方法和响应状态等

```http
HTTP/1.1 201 Created
Location: /api/users/123
Content-Type: application/json
Content-Length: 55

{"id":123,"name":"John Doe","email":"john@example.com"}
```

`Content-Length` 按**字节数**计算，不是字符数

下面依次是 GET 请求结构、实际请求头和响应头。图中的“请求行、请求头、请求正文”是概念分组，读取 HTTP/1.1 原始报文时还要注意分隔正文的空行。

![[Pasted image 20250831231836.png]]

![[Pasted image 20250831232320.png]]

![[Pasted image 20250831232832.png]]

最后一张图中，`Content-Encoding: gzip` 表示正文压缩，`Transfer-Encoding: chunked` 表示分块传输，两者可以同时存在

---
## 常见头字段
### 请求中常见
| 字段 | 作用或示例 |
| --- | --- |
| `Host` | 目标主机与可选端口；HTTP/1.1 必需 |
| `Accept` | 客户端可接受的媒体类型，如 `application/json` |
| `Accept-Encoding` | 客户端可接受的正文编码，如 `gzip, br, zstd` |
| `Accept-Language` | 偏好的语言，如 `zh-CN,zh;q=0.9` |
| `Authorization` | 认证凭证，如 `Bearer <token>` |
| `Cookie` | 向服务器发送符合条件的 Cookie |
| `User-Agent` | 客户端软件标识信息 |
| `Origin` | 请求来源的源，常用于 CORS 判断 |
| `Referer` | 来源页面信息，具体内容受 Referrer-Policy 等规则影响 |
| `If-None-Match` | 携带 ETag 验证资源；GET/HEAD 验证未修改时可返回 304 |
| `If-Modified-Since` | 携带修改时间进行条件请求 |
| `Range` | 请求资源的一部分，例如 `bytes=0-1023` |

### 响应中常见
| 字段 | 作用或示例 |
| --- | --- |
| `Set-Cookie` | 设置 Cookie，多个 Cookie 通常使用多条该字段 |
| `ETag` | 资源表示的验证标识，不保证一定是内容哈希 |
| `Last-Modified` | 资源最后修改时间 |
| `Location` | 重定向目标，或新建资源的位置 |
| `Vary` | 指示选择缓存响应时要比较哪些请求头，如 `Accept-Encoding` |
| `WWW-Authenticate` | 说明认证方案，401 响应必须包含 |
| `Allow` | 目标资源支持的方法，405 响应必须包含 |
| `Accept-Ranges` | 声明范围请求支持情况，如 `bytes` |
| `Content-Range` | 部分内容在完整资源中的范围 |
| `Retry-After` | 建议客户端何时重试 |
| `Access-Control-Allow-Origin` | 允许读取响应的源，详见 CORS 部分 |

### 请求与响应均可能使用
| 字段 | 作用 |
| --- | --- |
| `Content-Type` | 正文的媒体类型 |
| `Content-Length` | 内容长度，单位为字节 |
| `Content-Encoding` | 正文采用的编码，如 `gzip` |
| `Cache-Control` | 请求或响应的缓存指令；具体语义依方向和指令而定 |
| `Connection` | HTTP/1.x 的连接控制；HTTP/2、HTTP/3 不允许该字段 |
##### Cache-Control
[[强缓存&协商缓存⌚️]]

##### Content-Type

- text/event-stream：[[SSE💡]]

- application/json：JSON 数据

- application/x-www-form-urlencoded：表单键值对，如 name=Tom&age=18

- multipart/form-data：多部分表单，常用于文件上传；浏览器发送 FormData 时通常让浏览器自动设置带 boundary 的头字段

- text/plain：纯文本

### 缓存指令辨析
| 响应指令           | 含义                                |
| -------------- | --------------------------------- |
| `max-age=3600` | 响应的新鲜度寿命为 3600 秒，复用时还需考虑已存在的年龄等因素 |
| `no-cache`     | 可以存储，但复用前必须向服务器验证（禁止强缓存，走协商）      |
| `no-store`     | 不存储本次请求或响应的相关信息（缓存彻底关闭）           |
| `private`      | 只允许私有缓存存储，例如浏览器缓存                 |
| `public`       | 允许共享缓存存储，仍须遵守其他适用规则               |

**`no-cache` 不等于“不缓存”**。例如截图中的 `Cache-Control: no-cache, private`，表示允许私有缓存存储，但复用前需要验证。[HTTP 缓存规范](https://www.rfc-editor.org/rfc/rfc9111.html)

---
## HTTP 状态码
### 1xx：信息响应
| 状态码 | 含义 |
| --- | --- |
| `100 Continue` | 已收到请求的初始部分，客户端可以继续发送正文；常与 `Expect: 100-continue` 配合 |
| `101 Switching Protocols` | 同意切换协议，典型场景是 HTTP/1.1 升级到 WebSocket |
| `103 Early Hints` | 最终响应之前提供提示，例如通过 `Link` 提前发现资源 |

原笔记中的 `102 Processing` 是历史 WebDAV 扩展，不作为常用前端状态码重点记忆。

### 2xx：成功
| 状态码 | 含义 |
| --- | --- |
| `200 OK` | 请求成功 |
| `201 Created` | 请求成功并创建了资源，不仅适用于 POST，也可能用于 PUT |
| `202 Accepted` | 已接受处理，但处理尚未完成，也不保证最终成功 |
| `204 No Content` | 处理成功，不包含响应正文 |
| `206 Partial Content` | 成功返回所请求的部分内容，常见于视频播放、断点续传 |

请求 `.mp4` 不一定返回 206。通常是客户端发送 `Range`，且服务器满足范围请求后返回 206；服务器也可以忽略范围请求并返回完整内容 200。范围不可满足时可能返回 `416 Range Not Satisfiable`。

### 3xx：重定向与缓存验证
| 状态码 | 含义及方法变化 |
| --- | --- |
| `301 Moved Permanently` | 永久重定向；历史兼容行为允许把 POST 改为 GET |
| `302 Found` | 临时重定向；历史兼容行为允许把 POST 改为 GET |
| `303 See Other` | 引导客户端到另一地址获取结果，通常使用 GET；常用于表单提交后的跳转 |
| `304 Not Modified` | 条件 GET/HEAD 验证未修改，不包含正文，客户端复用已有内容 |
| `307 Temporary Redirect` | 临时重定向，自动跳转时保留方法和请求体 |
| `308 Permanent Redirect` | 永久重定向，自动跳转时保留方法和请求体 |

304 不表示“跳转到另一个 URL”，也不是所有缓存命中都会产生 304：缓存仍新鲜时，浏览器可能直接使用本地响应。

### 4xx：客户端错误
| 状态码 | 含义 |
| --- | --- |
| `400 Bad Request` | 服务器认为请求存在错误，如语法或消息格式无效 |
| `401 Unauthorized` | 缺少有效认证凭证，通常需要登录或更新凭证 |
| `403 Forbidden` | 服务器理解请求但拒绝执行，常见于权限不足 |
| `404 Not Found` | 未找到资源，或服务器不愿透露资源是否存在 |
| `405 Method Not Allowed` | 目标资源不支持该方法，响应带 `Allow` |
| `413 Content Too Large` | 请求内容过大；旧资料也称 Payload Too Large |
| `414 URI Too Long` | 请求 URI 过长 |
| `415 Unsupported Media Type` | 请求内容的媒体类型或编码不受支持 |
| `429 Too Many Requests` | 请求过于频繁，可能带 `Retry-After` |

`418 I'm a teapot` 来自愚人节协议；HTTP 核心规范将 418 标为保留的 Unused，了解背景即可。

### 5xx：服务器错误
| 状态码 | 含义 |
| --- | --- |
| `500 Internal Server Error` | 服务器遇到意外情况，无法完成请求 |
| `502 Bad Gateway` | 作为网关或代理时，从上游收到无效响应 |
| `503 Service Unavailable` | 暂时无法处理请求，例如过载或维护 |
| `504 Gateway Timeout` | 作为网关或代理时，未及时收到所需的上游响应 |

状态码语义以 [HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-15) 为准。

---
## 正文压缩
### gzip 原理
gzip 常用 DEFLATE 压缩数据，DEFLATE 结合 **LZ77** 与 **Huffman 编码**：前者利用重复片段，后者利用符号频率，减少冗余。[DEFLATE 规范](https://www.rfc-editor.org/info/rfc1951/)
- HTML、CSS、JavaScript、JSON 等文本通常有较好的压缩收益，但压缩率取决于内容，不能固定记成 60%～80%。
- JPEG、PNG、压缩视频等已经压缩过的内容，再压缩通常收益有限，甚至可能因额外开销而变大。
- 实时压缩消耗 CPU，需要权衡传输体积与计算开销；静态资源可预压缩。[HTTP 压缩说明](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Compression)

### 压缩协商
客户端声明支持的编码：
```http
Accept-Encoding: gzip, br, zstd
```

服务器若选择 gzip，相关响应头可以是：
```http
Content-Type: application/json
Content-Encoding: gzip
Vary: Accept-Encoding
```

`Content-Type` 仍然描述解码后内容的类型。若发送 `Content-Length`，对应的是压缩后的内容字节数；浏览器通常自动解压，不需要前端手动 gunzip。[Content-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Encoding)

### 常见编码
| 编码 | 标识 | 复习要点 |
| --- | --- | --- |
| gzip | `gzip` | 常见的通用正文压缩方式 |
| Brotli | `br` | 文本压缩通常有较好收益，高压缩等级的计算成本较高 |
| Zstandard | `zstd` | 可在速度与压缩率之间调整，是否使用取决于双方支持情况 |
| deflate | `deflate` | HTTP 中指 zlib 格式封装的 DEFLATE 数据，不是 gzip 的别名 |

压缩率和速度受数据、压缩等级与实现影响，不宜脱离条件给算法排固定名次。

> [!tip] 区分三种机制
> - HPACK / QPACK：压缩 HTTP 头字段。
> - `Content-Encoding: gzip`：压缩正文。
> - `Transfer-Encoding: chunked`：HTTP/1.1 的正文分块传输机制，本身不压缩；HTTP/2、HTTP/3 使用帧承载数据，不使用 chunked。

---
## CORS：简单请求与预检请求
这是**浏览器跨源访问控制**中的分类，不是所有 HTTP 请求的通用分类。“简单请求”是常用教学术语，Fetch 标准通过安全列表等规则定义是否触发预检。[MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)

源由**协议、主机、端口**共同确定。路径不同本身不构成跨源。

### 不触发 CORS 预检的典型条件
对于通常的跨源 Fetch/XHR 请求，需要同时满足：
1. 方法为 `GET`、`HEAD` 或 `POST`。
2. 开发者设置的头字段满足 CORS 安全列表，包括 `Accept`、`Accept-Language`、`Content-Language`、`Content-Type`、`Range`，且字段值也符合限制。
3. 若设置 `Content-Type`，媒体类型只能是 `application/x-www-form-urlencoded`、`multipart/form-data` 或 `text/plain`。
4. `Range` 只使用符合规则的单一字节范围，例如 `bytes=0-1023`。
5. XHR 未注册上传进度监听器，请求体也未使用 `ReadableStream` 等会触发预检的形式。

安全列表还有值长度、字符等限制，例如单个安全列表头字段值不能超过 128 字节。浏览器自动添加的 `Cookie`、`User-Agent` 等字段，不应机械套用“请求头只能有上述几个”的说法。[Fetch 安全列表规则](https://fetch.spec.whatwg.org/#cors-safelisted-request-header)

### 常见触发预检的情况
- 使用 `PUT`、`PATCH`、`DELETE` 等方法。
- 设置 `Content-Type: application/json`。
- 添加 `Authorization` 或 `X-Token` 等不在安全列表内的请求头。

例如，跨源发送带认证信息的 JSON POST，浏览器可能先发送：
```http
OPTIONS /api/users HTTP/1.1
Host: api.example.com
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: authorization, content-type
```

服务器允许时可返回：
```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 600
Vary: Origin
```

预检通过后，浏览器再发送实际请求；**实际响应也必须包含适用的 CORS 响应头**。预检结果可缓存，因此不能说“非简单请求每次都会先发送 OPTIONS”。[CORS 交互流程](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)

### 前端易错点
- **简单请求也受 CORS 约束**：可以直接发出，不代表 JavaScript 一定能读取响应。
- **CORS 不是防 CSRF 的完整方案**：即使浏览器不让脚本读取响应，请求仍可能已产生服务器端作用。
- **带凭证的跨源请求**：例如 `credentials: 'include'`，服务端需要返回具体的允许源和 `Access-Control-Allow-Credentials: true`，不能用 `Access-Control-Allow-Origin: *`；Cookie 是否实际发送还受其他浏览器规则限制。
- **`mode: 'no-cors'` 不能解决接口读取问题**：跨源响应通常变成 opaque，脚本无法读取正文和正常状态码。
- **浏览器的 Fetch API 不会因为 404、500 自动 reject**：这类响应需要检查 `response.ok` 或 `response.status`；网络错误和 CORS 失败等才可能导致请求 Promise reject。[Fetch 使用说明](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
