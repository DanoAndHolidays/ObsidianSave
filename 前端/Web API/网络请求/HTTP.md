# 版本
---
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
| 版本       | 发布时间 | 核心特点                          | 解决的主要问题               |
|------------|----------|-----------------------------------|------------------------------|
| HTTP/0.9   | 1991     | 仅支持GET，纯文本传输             | 无（基础版本）               |
| HTTP/1.0   | 1996     | 多方法、多类型、状态码            | 扩展传输内容类型             |
| HTTP/1.1   | 1999     | 持久连接、管道化、虚拟主机        | 减少连接开销                 |
| HTTP/2     | 2015     | 二进制分帧、多路复用、服务器推送  | 应用层队头阻塞               |
| HTTP/3     | 2022     | 基于QUIC、UDP传输                 | TCP层队头阻塞、弱网性能      |

目前，HTTP/1.1仍被广泛使用，HTTP/2在主流浏览器和服务器中已普及，HTTP/3则是未来的发展方向，逐步被各大厂商（如Google、Cloudflare）支持。

HTTP是一个TCP/IP通信协议的最上层的协议之一（HTML文件，图片文件，查询结果等）。后面的s是数字证书加密

![[Pasted image 20250831225347.png]]
![[Pasted image 20250831230800.png]]

---
# URL
---
![[Pasted image 20250831231201.png]]


![[Pasted image 20250831231836.png]]

---
# GET与POST的不同点
---
 **幂等性不同**。幂等性是针对于理想情况下的设计结果。GET 对访问的数据没有副作用，具有幂等性，多次请求相同的资源不会导致服务器状态的改变。而当POST 用于**更新**操作时往往是有副作用的，不幂等，多次请求可能导致不同的服务器状态。
- GET 产生的 URL 地址可以保存为书签，而 POST 不可以。
- GET 请求会被浏览器主动 cache，而 POST 不会，除非手动设置；
- GET请求参数会被完整保留在浏览器历史记录里，而POST中的参数不会被保留。
- GET在浏览器回退时是无害的，而POST会再次提交请求。
**携带数据的方式不同**。
- GET 一般将数据以参数的形式放到 URL 中，虽然 HTTP 标准并未对 URL 长度做限制，但是浏览器在实现时，一般会对 URL 的长度做限制，所以携带的数据有限；
- POST 将数据放到 Body 中，无长度限制。
- 对参数的数据类型，GET只接受ASCII字符，而POST没有限制。
- GET请求只能进行url编码，而POST支持多种编码方式。
**安全性不同**。
- GET 比 POST 更不安全，因为参数直接暴露在 URL 上，所以不能用来传递敏感信息。
- GET产生一个TCP数据包；POST有时产生两个TCP数据包，有浏览器会将post请求的header和data分为两次发送。【补充说明：这是某些浏览器的旧版本行为，现代浏览器通常会优化为单个数据包】
-  get：数据通过 URL 传递，容易被缓存、记录、拦截或篡改，不适合传输敏感数据 post: 数据通过请求主体传递，相对不容易被缓存或直接记录
- get： 请求的所有数据都显示在 URL 中，适合用于书签、URL 共享等场景 post: 数据隐藏在请求主体中，用户无法直接看到或修改，不适合用于书签或直接分享

用途不同
- get: 用于请求从服务器获取资源或数据
- post: 用于向服务器提交数据，通常是表单数据 

【补充：其他重要区别】
编码类型 
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
##### 消息头
- 请求头
- 响应头
【补充：常见HTTP头部分类与示例】
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
---
# 模拟报文
---
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
---
# HTTP 状态码详解
---
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
- **204 No Content**：服务器成功处理，但无返回内容（[原笔记误写为202，修正为204]）  
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
---
# HTTP 缓存机制
---
##### 缓存控制机制
HTTP缓存主要分为**强缓存**和**协商缓存**两种机制

强缓存流程，当浏览器请求资源时，会==先检查强缓存==是否有效：
1. 检查Cache-Control的max-age或s-maxage
2. 如果不存在，检查Expires字段
3. 如果缓存有效，直接使用缓存资源，不发送请求到服务器

协商缓存流程，当==强缓存失效==时，进入==协商缓存==阶段：
1. 浏览器携带If-None-Match(ETag值)和If-Modified-Since(Last-Modified值)向服务器发起请求
2. 服务器验证资源是否修改：
   - 如果ETag匹配，返回304 Not Modified
   - 如果资源已修改，返回200和新资源

HTTP缓存相关头部：
`Expires`：绝对过期时间（HTTP/1.0）【补充：已逐渐被Cache-Control取代】
`Cache-Control`：缓存控制指令（HTTP/1.1）【补充：现代浏览器首选】
- `max-age`：资源最大存活时间（秒）`max-age`优先级高于`expires`
- `public`：允许所有缓存节点缓存（包括代理服务器）【修正：public和private对于浏览器缓存效果相同，但影响中间代理缓存】
- `private`：仅允许客户端缓存，不允许代理服务器缓存
![[Pasted image 20250910172246.png]]
- `no-cache`：需向服务器验证新鲜度（使用协商缓存）【补充：不是"不缓存"，而是每次都要验证】
- `no-store`：禁止任何缓存（内存、磁盘都不缓存）
- `s-maxage`：对代理服务器的有效时长，用于共享缓存（如CDN），优先级高于`max-age`

这四个很少使用【补充说明：这些是Cache-Control扩展指令，使用场景较特殊】
- `max-stale`：客户端可以接受过期的缓存（请求头中使用）
- `min-fresh`：要求缓存至少还能保持指定秒数的新鲜度（请求头中使用）
- `must-revalidate`：一旦缓存过期，必须向服务器验证【补充：常见于重要资源】
- `no-transform`：禁止代理服务器对资源进行转换（如压缩图片）
##### 推荐缓存策略
```http
# 静态资源（可长期缓存）
Cache-Control: public, max-age=31536000, immutable

# 经常变动的资源
Cache-Control: no-cache

# 敏感数据
Cache-Control: private, no-store, max-age=0
```

```http
# 带hash值的资源（长期缓存，设置为一年）
Cache-Control: public, max-age=31536000

# 不带hash值的资源（需要验证）
Cache-Control: no-cache
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2023 07:28:00 GMT
```

![[Pasted image 20250910170334.png]]
##### 请求详解
一般server返回的头中的cache-control为no-cache（协商缓存）

当browser向服务器请求资源时，在响应头会添加etag，一个根据文件算出的hash值，同时也会返回last-modified，是一个时间。
【补充：ETag类型】
- 强ETag：文件内容完全相同时才匹配（如"686897696a7c876b7e"）
- 弱ETag：文件语义相同即匹配（如W/"686897696a7c876b7e"）

如果浏览器再次请求同样的文件，会在请求头添加if-none-match，其值为etag的值，同时也会添加值为last-modified的if-modified-since

server会将if-none-match的值与最新的文件的hash值对比，如果一样则返回304，避免了带宽流量的浪费。

（图中的是强缓存）
![[Pasted image 20250910173300.png]]

![[Pasted image 20250910171405.png]]
##### gzip 压缩原理
[补充说明]：  
- 使用LZ77算法和Huffman编码消除冗余数据  
- 文本文件（HTML/CSS/JS）压缩效果显著（60-80%）  
- 已压缩文件（如图片）再次压缩可能变大  
##### TLS 安全协议
由于http是明文的，在其基础上加入ssl与tls协议，增加安全性。
ssl是tls的前身 【补充：SSL 3.0之后被TLS 1.0取代，现在广泛使用TLS 1.2/1.3】

加密方式：
- 对称加密：加密和解密使用相同密钥，速度快 【补充：如AES、DES、3DES】
- 非对称加密：使用公钥和私钥配对，公钥加密只能私钥解密，反之亦然 【补充说明：非对称加密使用数学上的单向函数，公钥可公开，私钥保密。常见算法：RSA、ECC、DH】
tls加密使用混合方式：握手阶段使用非对称加密交换对称密钥，后续通信使用对称加密

向ca申请ssl证书，其中有公钥和私钥，端口改为443，存在服务器中，SSL证书包含域名、公司信息、公钥、CA数字签名等

通过以下方式保证证书可信：
1. 证书颁发机构（CA）：证书由一个被广泛信任的第三方组织签发，这些组织被称为证书颁发机构（Certificate Authority, CA）。
2. 证书链（信任链）：服务器向客户端提供的证书通常并非直接由根证书签发，而是由中间证书签发。根证书—中间证书—服务器证书共同构成了证书链；验证过程中，浏览器会检查服务器证书的签发者是谁，并递归地验证直到找到预先安装的根证书。如果整个证书链都有效并且可以追溯到一个可信的根证书，证书就是可信的
3. 浏览器内置的根证书：主流的操作系统和浏览器都预装了一组可信任的根证书，这些根证书代表了被信任的 CA
4. 证书的数字签名：CA 使用自己的私钥对证书进行数字签名。浏览器使用相应的 CA 公钥来验证证书的签名是否有效
【补充：SSL证书验证过程】
1. 客户端验证证书是否由可信CA签发
2. 检查证书是否在有效期内
3. 验证证书中的域名与访问域名匹配
4. 检查证书是否被吊销

握手过程：
![[Pasted image 20250910175512.png]]
在 TLS 1.2 中，握手协议过程需要耗费两个 RTT，过程如下
- [OUT] Client Hello，客户端选出自身支持的 TLS 版本号、cipher suites、Client Random、SessionId 传送给服务器端 (有可能可复用 Session)
- [IN] Server Hello，服务器端选出双方都支持的 TLS 版本，cipher suite 、Server Random、SeesionId 给客户端
- [IN] Certificate，服务器端给客户端发送证书，用以身份验证及提供公钥
- [IN] Server Key Exchange，服务器端给客户端发送密钥交换算法的一些参数
- [IN] Server Finished
- [OUT] Client Key Exchange，客户端给服务器端发送密钥交换算法的一些参数，计算出预主密钥 (`pre master secret`)，使用密钥交换算法（一般是 ECDHE）传递给服务器端。双方根据（Client Random、Server Random、Pre Master Secret）三个随机数生成对称加密中的密钥（`master secret`）。（再根据 `master secret` 生成 `Session Keys`，包括 `Client MAC Key`、`Client Write Key`、`Server MAC Key`、`Server Write Key`。用以以后对的通信加密。）
- [OUT] Change Cipher Spec，告知以后的消息开始对称加密通信
- [OUT] Finished，加密消息并完整性验证，标志着握手阶段成功并结束（对握手消息使用 `Client Write Key` 加解密，并使用 `Client MAC Key` 进行完整性校验）
- [IN] Change Cipher Spec，告知以后的消息开始对称加密通信。此时服务器端通过密钥交换算法拿到 `pre master secret`，并根据三个随机数生成 `master secret`。
- [IN] Finished，加密消息并完整性验证，标志着握手阶段成功并结束

> 注，对于（）内容在面试中可以忽略不答

【补充：TLS 1.3 改进】
TLS 1.3 简化握手过程，只需1-RTT：
- Client Hello：支持算法+Client Random+密钥共享参数
- Server Hello：选择算法+Server Random+证书+密钥共享参数
- 双方可直接计算预主密钥，大大加快握手速度

[补充说明]：TLS 1.2/1.3 提供HTTPS加密通信，包括：  
- 密钥交换（ECDHE/RSA）  
- 身份认证  
- 对称加密（AES-GCM）  
- 消息完整性验证

【补充：前向安全性】
使用ECDHE等密钥交换算法可提供前向安全性，即使服务器私钥泄露，过去的通信记录也无法解密

【补充：SSL/TLS协议分层】
- 握手协议（Handshake Protocol）：协商加密参数和密钥
- 记录协议（Record Protocol）：数据传输加密和完整性保护
- 警报协议（Alert Protocol）：错误通知和连接关闭
- 变更密码规范协议（Change Cipher Spec Protocol）：加密策略切换

性能优化
1. 启用 TLS 1.3：（1）TLS 1.2 通常需要两个 RTT 来完成握手；TLS 1.3 只需要一个 RTT，降低了延迟（在发送第一个“Hello”消息时，不仅提供加密套件等信息，还包括生成的密钥交换参数（使用椭圆曲线 Diffie-Hellman，ECDHE）和其他需要的信息，服务器响应，选择加密套件并发送密钥交换参数。双方立即可以计算出共享的会话密钥） （2）0-RTT 握手：TLS 1.3 支持“0-RTT”握手，这允许客户端和服务器在之前的会话基础上立即恢复连接
2. HTTP/2 和 TLS 的结合：多路复用、头部压缩、服务器推送
3. 启用 OCSP Stapling：允许服务器在握手过程中将最新的证书状态直接发送给客户端，避免了客户端向 CA 服务器进行额外查询，从而减少延迟

---
# HTTP 请求与压缩技术
---

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

---
