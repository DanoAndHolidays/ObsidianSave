# HTTP
### 特点
- HTTP是无连接：无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即断开连接。采用这种式可以节省传输时间。
- HTTP是媒体独立的：这意味着，只要客户端和服务器知道如何处理的数据内容，任何类型的数据都可以通过HTTP发送。客户端以及服务器指定使用适合的MIME-type内容类型。
- HTTP是状态：HTTP协议是无状态协议。无状态是指协议对于事务处理没有记忆能。缺少状态意味着如果后续处理需要前面的信息，则它必须重传，这样可能导致每次连接传送的数据量增大。另一方面，在服务器不需要先前信息时它的应答就较快。

### 版本
HTTP协议是HyperTextTransferProtocol（超文本传输协议）的缩写，主要用于网页的传输，现在也常应用网络API的开发(RestfulAPI)。
##### HTTP/0.9（1991年）
- **特点**：首个版本，极其简单，仅支持`GET`方法，且只能传输纯文本（HTML），不支持请求头、响应头或状态码。
- **局限性**：功能单一，无法处理图片、视频等多媒体内容，也没有错误处理机制。
##### HTTP/1.0（1996年）
- **核心改进**：
  - 引入了更多请求方法（如`POST`、`HEAD`），支持传输多种数据类型（通过`Content-Type`头指定，如图片、音频等）。
  - 增加了HTTP头（请求头和响应头），可传递元数据（如`User-Agent`、`Content-Length`）。
  - 引入状态码（如200表示成功，404表示未找到），便于错误处理。
- **局限性**：每次请求都需要建立新的TCP连接，连接无法复用，效率较低（“无连接”特性）。
##### HTTP/1.1（1999年）
- **核心改进**：
  - **持久连接（Keep-Alive）**：默认允许TCP连接复用，多个请求可通过同一连接传输，减少连接建立/关闭的开销。
  - **管道化（Pipelining）**：客户端可发送多个请求（Chrome最多6个），提高传输效率（但因“队头阻塞”问题，实际应用有限）。
  - **分块传输编码（Chunked Transfer Encoding）**：支持动态生成的内容（无需预先知道总长度）。
  - 增加了更多方法（如`PUT`、`DELETE`、`OPTIONS`）和状态码，支持虚拟主机（通过`Host`头）。
- **局限性**：管道化仍受“队头阻塞”影响（一个请求阻塞会导致后续请求排队），且同一连接中请求需按顺序响应。
#####  HTTP/2（2015年）
- **核心改进**：
  - **二进制分帧**：将请求/响应拆分为二进制帧（Frame），进行压缩，而非文本格式，解析效率更高。
  - **多路复用（Multiplexing）**：同一TCP连接中可并行传输多个请求/响应（帧通过流ID区分），彻底解决“队头阻塞”问题。
  - **头部压缩（HPACK）**：对重复的HTTP头进行压缩，减少数据传输量。
  - **服务器推送（Server Push）**：服务器可主动向客户端推送关联资源（如HTML引用的CSS/JS），提前加载资源。
- **优势**：大幅提升并发性能，尤其适合加载包含大量资源的网页。
![[Pasted image 20250901170355.png]]
##### HTTP/3（2022年标准化）
- **核心改进**：
  - **基于QUIC协议**：取代TCP，使用UDP作为传输层协议，减少连接建立时间（支持0-RTT或1-RTT握手），并自带流量控制和重传机制。
  - **解决TCP层队头阻塞**：QUIC协议在单个连接中支持多个独立流，某一流的丢包不会影响其他流，进一步优化性能。
  - 兼容HTTP/2的多路复用、头部压缩等特性。
- **优势**：在弱网环境（如移动网络）下表现更优，连接建立更快，抗丢包能力更强。
##### 版本对比总结
| 版本       | 发布时间 | 核心特点             | 解决的主要问题       |
| -------- | ---- | ---------------- | ------------- |
| HTTP/0.9 | 1991 | 仅支持GET，纯文本传输     | 无（基础版本）       |
| HTTP/1.0 | 1996 | 多方法、多类型、状态码      | 扩展传输内容类型      |
| HTTP/1.1 | 1999 | 持久连接、管道化、虚拟主机    | 减少连接开销        |
| HTTP/2   | 2015 | 二进制分帧、多路复用、服务器推送 | 应用层队头阻塞       |
| HTTP/3   | 2022 | 基于QUIC、UDP传输     | TCP层队头阻塞、弱网性能 |

目前，HTTP/1.1仍被广泛使用，HTTP/2在主流浏览器和服务器中已普及，HTTP/3则是未来的发展方向，逐步被各大厂商（如Google、Cloudflare）支持。

HTTP是一个TCP/IP通信协议的最上层的协议之一（HTML文件，图片文件，查询结果等）。后面的s是数字证书加密
### URL
![[Pasted image 20250831231201.png]]


![[Pasted image 20250831231836.png]]
### GET与POST的不同点
 **幂等性不同**
 幂等性是针对于理想情况下的设计结果。GET 对访问的数据没有副作用，具有幂等性，多次请求相同的资源不会导致服务器状态的改变。而当POST 用于**更新**操作时往往是有副作用的，不幂等，多次请求可能导致不同的服务器状态。
- GET 产生的 URL 地址可以保存为书签，而 POST 不可以。
- GET 请求会被浏览器主动 cache，而 POST 不会，除非手动设置；
- GET请求参数会被完整保留在浏览器历史记录里，而POST中的参数不会被保留。
- GET在浏览器回退时是无害的，而POST会再次提交请求。
**携带数据的方式不同**
- GET 一般将数据以参数的形式放到 URL 中，虽然 HTTP 标准并未对 URL 长度做限制，但是浏览器在实现时，一般会对 URL 的长度做限制，所以携带的数据有限；
- POST 将数据放到 Body 中，无长度限制。
- 对参数的数据类型，GET只接受ASCII字符，而POST没有限制。
- GET请求只能进行url编码，而POST支持多种编码方式。
**安全性不同**
- GET 比 POST 更不安全，因为参数直接暴露在 URL 上，所以不能用来传递敏感信息。
- GET产生一个TCP数据包；POST有时产生两个TCP数据包，有浏览器会将post请求的header和data分为两次发送。【补充说明：这是某些浏览器的旧版本行为，现代浏览器通常会优化为单个数据包】
-  get：数据通过 URL 传递，容易被缓存、记录、拦截或篡改，不适合传输敏感数据 post: 数据通过请求主体传递，相对不容易被缓存或直接记录
- get： 请求的所有数据都显示在 URL 中，适合用于书签、URL 共享等场景 post: 数据隐藏在请求主体中，用户无法直接看到或修改，不适合用于书签或直接分享
**用途不同**
- get: 用于请求从服务器获取资源或数据
- post: 用于向服务器提交数据，通常是表单数据 

【补充：其他重要区别】
**编码类型不同**
- get: application/x-www-form-urlencoded 
- post: 支持多种编码类型，如multipart/form-data、application/json等
##### GET
![[Pasted image 20250831232320.png]]
![[Pasted image 20250831232832.png]]
##### POST
请求报文：
1. 请求行：<方法><请求目标><http协议版本>
2. 请求头：<头部字段名>: <值>
3. 空行
4. 请求体

响应报文：
1. 状态行：<HTTP版本> <状态码> <原因短语>
2. 响应头部：<头部字段名>: <值>
3. 空行
4. 响应体

【补充：POST请求示例】
```
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json
Content-Length: 45

{"name":"John Doe","email":"john@example.com"}
```

【补充：POST响应示例】
```
HTTP/1.1 201 Created
Content-Type: application/json
Date: Wed, 21 Oct 2024 07:28:00 GMT
Content-Length: 60

{"id":123,"name":"John Doe","email":"john@example.com"}
```

### 消息头
- 请求头
- 响应头
##### 请求头常见字段
- **通用头**：Cache-Control、Connection、Date、Pragma、Trailer、Transfer-Encoding、Upgrade、Via、Warning
- **请求头**：Accept、Accept-Charset、Accept-Encoding、Accept-Language、Authorization、Expect、From、Host、If-Match、If-Modified-Since、If-None-Match、If-Range、If-Unmodified-Since、Max-Forwards、Proxy-Authorization、Range、Referer、TE、User-Agent
- **实体头**：Allow、Content-Encoding、Content-Language、Content-Length、Content-Location、Content-MD5、Content-Range、Content-Type、Expires、Last-Modified

##### 响应头常见字段
- **通用头**：同上
- **响应头**：Accept-Ranges、Age、ETag、Location、Proxy-Authenticate、Retry-After、Server、Vary、WWW-Authenticate
- **实体头**：同上

【补充：重要头字段说明】
- `Content-Type`: 指定请求/响应体的媒体类型（如application/json、text/html）
- `Authorization`: 包含用于HTTP认证的凭证信息
- `Cache-Control`: 指定缓存机制（如no-cache、max-age=3600）
- `User-Agent`: 标识客户端软件信息
- `Set-Cookie`: 服务器向客户端设置cookie
##### 模拟报文
```http
$ nc www.baidu.com 80
GET / HTTP/1.1
Host: www.baidu.com
 
HTTP/1.1 200 OK
Accept-Ranges: bytes
Cache-Control: no-cache
Connection: Keep-Alive
Content-Length: 14615
Content-Type: text/html
Date: Tue, 10 Dec 2019 02:48:44 GMT
P3p: CP=" OTI DSP COR IVA OUR IND COM "
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Pragma: no-cache
Server: BWS/1.1
Set-Cookie: BAIDUID=F0FC6B3A056DEA285F51A1F2F8A170BB:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BIDUPSID=F0FC6B3A056DEA285F51A1F2F8A170BB; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: PSTM=1575946124; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BAIDUID=F0FC6B3A056DEA287CB2B9422E09E30E:FG=1; max-age=31536000; expires=Wed, 09-Dec-20 02:48:44 GMT; domain=.baidu.com; path=/; version=1; comment=bd
Traceid: 1575946124058431156210725656341129791126
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1
 
<!DOCTYPE html><!--STATUS OK-->
........内容省略
```
### HTTP 状态码详解
##### 1xx 信息响应
[补充说明]：  
- **100 Continue**：客户端应继续请求  
- **101 Switching Protocols**：服务器同意升级协议（如切换到WebSocket）  
- **102 Processing**：服务器已接收请求，正在处理（WebDAV）  
- **103 Early Hints**：预加载链接信息  
##### 2xx 成功响应
[修正说明]：  
- **200 OK**：请求成功  
- **201 Created**：POST请求成功，资源已创建  
- **202 Accepted**：请求已接受，但处理未完成  
- **204 No Content**：服务器成功处理，但无返回内容
- **206 Partial Content**：范围请求成功（用于大文件分块传输）  我在请求.mp4的时候就会返回206，支持 Range Request
##### 3xx 重定向
[修正说明]：  
- **301 Moved Permanently**：永久重定向（资源已永久迁移）  
- **302 Found**：临时重定向（请求方法可能改变）  
- **304 Not Modified**：资源未修改，使用缓存  
- **307 Temporary Redirect**：临时重定向（请求方法和主体不变）  
- **308 Permanent Redirect**：永久重定向（请求方法和主体不变）  
##### 4xx 客户端错误
[修正说明]：  
- **400 Bad Request**：请求语法错误  
- **401 Unauthorized**：需要身份认证  
- **403 Forbidden**：服务器拒绝请求  
- **404 Not Found**：资源不存在  
- **405 Method Not Allowed**：请求方法不被允许  
- **413 Payload Too Large**：请求体过大  
- **418 I'm a Teapot**：彩蛋状态码  
- **429 Too Many Requests**：请求过于频繁  
##### 5xx 服务器错误
[修正说明]：  
- **500 Internal Server Error**：服务器内部错误  
- **502 Bad Gateway**：网关错误  
- **503 Service Unavailable**：服务不可用  
- **504 Gateway Timeout**：网关超时  

### gzip 压缩原理
[补充说明]：  
- 使用LZ77算法和Huffman编码消除冗余数据  
- 文本文件（HTML/CSS/JS）压缩效果显著（60-80%）  
- 已压缩文件（如图片）再次压缩==可能变大==  
##### 压缩技术比较
```markdown
| 算法        | 标识      | 压缩效率 | 压缩速度 | 适用场景          |
|-------------|-----------|----------|----------|-------------------|
| Gzip        | gzip      | 高       | 中等     | 通用文本压缩      |
| Brotli      | br        | 非常高   | 慢       | 静态资源压缩      |
| Zstandard   | zstd      | 很高     | 非常快   | 实时通信          |
| Deflate     | deflate   | 中等     | 快       | 传统系统          |
```

[补充说明]：  
- **Gzip**：基于LZ77算法和Huffman编码，适合文本压缩  
- **Brotli**：Google开发，比Gzip压缩率更高但更耗时  
- **图片压缩**：已压缩格式（JPEG、PNG）再次压缩可能增大文件大小  
- **性能考量**：压缩消耗CPU资源，需权衡压缩率与计算成本  

### HTTP 请求分类
##### 简单请求与非简单请求
[修正术语]：  
- **简单请求**：使用特定方法（GET、POST、HEAD）和有限头部的HTTP请求  
- **非简单请求**：需要预检请求（OPTIONS）的复杂请求  

简单请求条件：  
1. 方法为 GET、POST 或 HEAD  
2. 头部仅包含：  
   - Accept  
   - Accept-Language  
   - Content-Language  
   - Content-Type（仅限于 application/x-www-form-urlencoded、multipart/form-data、text/plain）

##### 常见请求头
[补充说明]：  
- **Content-Type**：请求体类型  
  - `application/json`：JSON数据格式  
  - `application/x-www-form-urlencoded`：表单编码数据  
  - `multipart/form-data`：多部分表单数据  
- **Authorization**：身份验证令牌（Bearer token）  
- **Accept-Encoding**：客户端支持的压缩算法  
