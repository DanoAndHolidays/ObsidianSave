# HTTP&网络

### 【Q035】http 常见的状态码有哪些 ⌚️
废了，全忘了
- **1xx 信息**：100 Continue（继续发送）、101 Switching Protocols（协议切换）
- **2xx 成功**：200 OK、201 Created、204 No Content（无响应体，一般是options）
- **3xx 重定向**：301 永久重定向、302 临时重定向、304 Not Modified（协商缓存）
- **4xx 客户端错误**：400 Bad Request、401 Unauthorized（未认证）、403 Forbidden（无权限）、404 Not Found、405 Method Not Allowed
- **5xx 服务端错误**：500 Internal Server Error、502 Bad Gateway、503 Service Unavailable、504 Gateway Timeout

### 【Q036】http 状态码中 301，302和307有什么区别
- **301 Moved Permanently**：永久重定向，浏览器会缓存，下次直接跳转，搜索引擎会更新索引。POST 请求可能被改为 GET。
- **302 Found**：临时重定向，浏览器不会缓存，搜索引擎保留原 URL。POST 请求可能被改为 GET。
- **307 Temporary Redirect**：临时重定向，严格保持原请求方法（POST 仍是 POST），不允许修改请求体。

### 【Q050】http 状态码 502 和 504 有什么区别
- **502 Bad Gateway**：网关/代理服务器从上游服务器收到了无效响应。如 Nginx 请求后端时后端挂了或返回了畸形数据。
- **504 Gateway Timeout**：网关/代理服务器请求上游服务器超时，上游服务器处理太慢，没有在规定时间内返回数据。

### 【Q079】简述 http 的缓存机制 ⌚️
分为**强缓存**和**协商缓存**：
- **强缓存**：通过 `Cache-Control: max-age=3600` 或 `Expires` 控制，在有效期内部直接使用缓存，不发请求。Cache-Control 优先级高于 Expires。
- **协商缓存**：浏览器发送请求到服务器验证资源是否过期。通过 `If-None-Match`（配合 ETag）和 `If-Modified-Since`（配合 Last-Modified）实现。返回 304 （Not Modified）表示资源未变，继续用缓存。ETag 优先于 Last-Modified。

### 【Q081】http proxy 的原理是什么
HTTP 代理服务器位于客户端和服务器之间。正向代理：客户端→代理→服务器，代理代表客户端请求资源，可用来翻墙、缓存、过滤内容。反向代理：客户端→代理→后端服务器，代理代表服务器接收请求并转发，用于负载均衡、缓存、SSL 终止。代理服务器会解析 HTTP 报文，重新发起请求并转发响应。

### 【Q084】随着 http2 的发展，前端性能优化中的哪些传统方案可以被替代
- **雪碧图/文件合并**：HTTP2 多路复用减少了请求开销，不需要合并文件来减少请求数
- **域名分片**：HTTP2 单连接即可并发，不需要分散到多域名
- **内联 CSS/JS**：HTTP2 Server Push 可以主动推送资源，不需要内联
- **CSS 雪碧图**：可被独立小图片替代
但代码压缩、懒加载、CDN 等优化手段仍然有效。

### 【Q085】http2 与 http1.1 有什么改进
1. **多路复用**：一个连接并发处理多个请求，解决队首阻塞
2. **首部压缩**：HPACK 算法压缩请求头，减少冗余
3. **服务器推送**：Server Push 主动推送资源
4. **二进制分帧**：将报文拆成帧传输，解析更高效
5. **流优先级**：可设置请求优先级，优化加载顺序

### 【Q107】什么是 Basic Auth 和 Digest Auth
- **Basic Auth**：用户名密码用 Base64 编码放在 Authorization 头中（格式 `Basic base64(user:password)`），本质是明文，必须配合 HTTPS 使用。
- **Digest Auth**：挑战-应答模式，服务器返回 nonce，客户端用用户名、密码、nonce 等做 MD5 哈希后返回。密码不直接传，但不能防中间人攻击。

### 【Q108】gzip 的原理是什么，如何配置
- **原理**：基于 DEFLATE 算法，结合 LZ77 压缩和哈夫曼编码。LZ77 用滑动窗口找重复字符串替换为（距离，长度）指针；哈夫曼编码用更短码字表示高频字符。
- **Nginx 配置**：`gzip on; gzip_types text/plain application/javascript text/css; gzip_min_length 1000;`
- 浏览器发送 `Accept-Encoding: gzip`，服务器返回 `Content-Encoding: gzip`。

### 【Q109】可以对图片开启 gzip 压缩吗，为什么
一般**不需要**也不建议对图片开启 gzip 压缩。图片本身已经是压缩格式（JPEG、PNG、WebP），gzip 对其几乎无压缩效果甚至可能变大。而且浪费 CPU。gzip 主要针对文本类资源（HTML、CSS、JS、JSON、SVG）。

### 【Q110】http 的请求报文与响应报文的格式是什么
- **请求报文**：
  ```
  GET /index.html HTTP/1.1       ← 请求行（方法 路径 版本）
  Host: example.com               ← 请求头
  User-Agent: Chrome/...
  Accept: text/html
                                   ← 空行（CRLF）
  body data                        ← 请求体（可选）
  ```
- **响应报文**：
  ```
  HTTP/1.1 200 OK                  ← 状态行（版本 状态码 原因短语）
  Content-Type: text/html          ← 响应头
  Content-Length: 1234
                                   ← 空行
  <html>...</html>                  ← 响应体
  ```

### 【Q111】http 响应头中的 ETag 值是如何生成的
ETag 是服务器生成的资源标识符，常见生成方式：
- 对文件内容做 **Hash**（MD5、SHA-1）
- 文件内容的 **CRC32 校验和**
- 使用**文件最后修改时间 + 文件大小**的组合 Hash
- Nginx 默认使用 `文件mtime + 文件大小` 来生成，格式如 `"5d8c72a5-264"`

### 【Q112】如果 http 响应头中 ETag 值改变了，是否意味着文件内容一定已经更改
**不一定**。ETag 值取决于服务器生成算法。如果 ETag 是用文件修改时间 + 大小生成的，修改时间变了但内容没变（如 touch 命令），ETag 也会变。即使用内容哈希，不同的哈希算法、编码方式也可能导致 ETag 变化而内容不变。反过来，ETag 不变则内容几乎一定没变。

### 【Q116】http 服务中静态文件的 Last-Modified 是根据什么生成的
根据文件系统的最后修改时间（mtime）自动生成。服务器读取文件的 mtime 并设置到 Last-Modified 响应头中。例如 Nginx 默认就是这样做的。

### 【Q117】既然 http 是无状态协议，那它是如何保持登录状态
通过以下机制实现：
1. **Cookie + Session**：登录后在服务端创建 Session，把 Session ID 通过 Set-Cookie 返回给浏览器。后续请求自动带上 Cookie，服务器根据 Session ID 找到对应用户信息。
2. **Token（JWT）**：登录后服务器返回签名的 JWT Token，客户端存储（Cookie/localStorage），每次请求带上 Token（Authorization 头），服务器验证签名即可识别用户。是无状态方案。
3. **OAuth/OIDC**：第三方登录授权。

### 【Q119】https 是如何保证报文安全的
通过 TLS/SSL 协议提供三重保障：
1. **加密**：对称加密（AES 等）保证数据传输机密性，内容不会被窃听
2. **完整性校验**：MAC 消息认证码防止数据被篡改
3. **身份认证**：PKI 公钥体系 + 数字证书验证服务器身份（可能也验证客户端）
建立连接时通过 TLS 握手交换对称密钥，后续用对称密钥加密通信。

### 【Q121】我们如何从 http 的报文中得知该服务使用的技术栈
- **Server 响应头**：`Server: nginx/1.18.0`、`Server: Apache/2.4`
- **X-Powered-By 头**：`X-Powered-By: Express`、`X-Powered-By: PHP/7.4`
- **Set-Cookie 头**：`JSESSIONID`（Java/Spring）、`PHPSESSID`（PHP）、`_session_id`（Rails）
- **Content-Type / 响应特征**：特定格式或默认页面（如 Tomcat 404 页面）
- **X-AspNet-Version** 等特定头
- **Wappalyzer** 等工具自动化检测

### 【Q122】在发送 http 请求报文时，Host 是必要的吗
**在 HTTP/1.1 中是必须的**（RFC 规定）。因为 HTTP/1.1 支持基于域名的虚拟主机，同一个 IP 可能托管多个网站，服务器靠 Host 头来区分请求哪个站点。
HTTP/1.0 不强制但不传 Host 可能导致虚拟主机问题。
HTTP/2 也要求 Host（或 :authority 伪头）。

### 【Q133】http 响应头中如果 content-type 为 application/octet-stream，则代表什么意思
表示**二进制流数据**，是通用的、未知的二进制文件类型。浏览器不会尝试解析或显示，通常会提示用户下载保存到本地。常用于文件下载场景。

### 【Q136】http 向 https 做重定向应该使用哪个状态码
应该使用 **301 Moved Permanently**（永久重定向）或 **302 Found**（临时重定向）。实践中常用 301 来告诉浏览器和搜索引擎该站点应该始终走 HTTPS。Nginx 配置示例：`return 301 https://$host$request_uri;`

### 【Q141】http 响应头中的 Date 与 Last-Modified 有什么不同
- **Date**：服务器生成响应报文的时间（当前时间），每个响应都有。
- **Last-Modified**：请求的资源（文件）最后一次被修改的时间，只对静态资源有意义。
- **部署注意**：集群部署时各服务器时间需 NTP 同步，否则 Date 不一致可能导致缓存问题。CDN 边缘节点时间也需要校准。

### 【Q144】http 1.1 中的 keep-alive 有什么作用
HTTP/1.1 ==默认开启==长连接（HTTP/1.0 需要 `Connection: keep-alive`）。作用是：**一次 TCP 连接可以发送多个 HTTP 请求和响应**，避免了每次请求都要三次握手的开销，减少了 TCP 慢启动的影响，提升页面加载性能。

### 【Q147】当在浏览器中看到某资源使用了 http2 后，使用curl看到的为什么仍是 http 1.1
常见原因：
1. curl 版本太老不支持 HTTP/2（需要 7.33.0+）
2. 没有加 `--http2` 参数（某些旧版本默认关闭）
3. curl 编译时没有启用 HTTP/2 支持（需 nghttp2 库）
4. 服务端只在 TLS ALPN 协商 HTTP/2，curl 没有用 HTTPS 连接
解决：`curl --http2 -v https://example.com`

### 【Q149】什么是队首阻塞，如何解决，原理如何
**队首阻塞（Head-of-Line Blocking）**：HTTP/1.1 中，同一连接上的请求必须==按顺序处理==，如果第一个请求响应很慢，后续所有请求都会被阻塞。

**解决方案：**
- **HTTP/1.1**：并发 TCP 连接（浏览器限制同域名 6-8 个），域名分片
- **HTTP/2**：多路复用，在一个 TCP 连接上分帧传输，不同 Stream 的帧可交错发送，应用层不再有队首阻塞。但 TCP 层仍有队首阻塞（丢包会阻塞所有流）
- **HTTP/3**：基于 QUIC（UDP），彻底解决 TCP 层队首阻塞，每个流独立传输

### 【Q192】简述你们前端项目中资源的缓存配置策略
- **HTML 文件**：`Cache-Control: no-cache`，每次都==协商缓存==，确保入口文件最新
- **JS/CSS 文件**：文件名带 hash（如 `app.abc123.js`），设置 `Cache-Control: max-age=31536000` ==永久缓存==，因为内容==变了 hash 就变==，实际是新 URL
- **图片等静态资源**：同样使用 hash + 强缓存，大图也可 CDN 缓存
- **API 数据**：默认 `no-cache` 或 `max-age=0`，按需设置短时间缓存
- **CDN**：配合 301 + 刷新 CDN 缓存实现资源更新

### 【Q206】no-cache 与 no-store 的区别是什么
- **no-cache**：可以缓存，但每次使用前必须向服务器验证（协商缓存），发请求带 If-None-Match/If-Modified-Since，返回 304 才用缓存。
- **no-store**：**完全不缓存**，不存储到任何缓存（浏览器缓存、CDN 等），每次都重新请求获取最新内容。适用于敏感数据（如银行页面）。

### 【Q252】https 中如何保证证书是可信任的
通过**证书链**验证：
1. 浏览器收到服务器证书，检查其颁发者（CA）
2. 查找颁发者的中间 CA 证书（可能服务器也会发送中间证书）
3. 向上追溯直到**根 CA 证书**（操作系统/浏览器内置的信任锚点）
4. 验证证书签名是否匹配、证书是否在有效期内、是否被吊销（CRL/OCSP）
5. 验证证书中的域名与访问域名是否一致（SAN/CN 字段）

### 【Q267】CSP 是干什么用的了
**CSP（Content Security Policy）** 是浏览器安全策略，通过 HTTP 响应头 `Content-Security-Policy` 或 `<meta>` 标签定义，限制页面可以加载/执行的资源来源。用于防御 XSS、数据注入等攻击。常用指令：
- `script-src 'self'`：只加载同源脚本
- `default-src 'self'`：默认只加载同源资源
- `style-src 'self' 'unsafe-inline'`：样式资源策略
- `img-src *`：图片可以从任何地方加载

### 【Q273】http2 中的首部压缩的实现原理是什么
使用 **HPACK 算法**：
1. **静态表**：预定义的 61 个常用头部字段（如 `:method: GET`、`:status: 200`），直接引用索引
2. **动态表**：连接期间维护的可更新字典，把已出现过的头部键值对缓存起来
3. **哈夫曼编码**：对字符串进行哈夫曼压缩
4. 客户端和服务器各维护一份相同的动态表，请求/响应中的头部字段只需发送索引引用或哈夫曼编码后的差值

### 【Q283】http 请求头中的 X-Forwarded-For 代表什么意思
指示**客户端的原始 IP 地址**。请求经过多级代理时，每级代理会将上游 IP 追加到该头部：
```
X-Forwarded-For: client, proxy1, proxy2
```
让最终服务器能够追溯到真实客户端 IP。类似头部还有 X-Forwarded-Proto（原始协议）、X-Forwarded-Host。现代标准化版本是 Forwarded 头。

### 【Q301】base64 由哪64个字符构成
**A-Z**（26 个大写字母）、**a-z**（26 个小写字母）、**0-9**（10 个数字）、**`+`** 和 **`/`**，共 64 个。外加填充字符 **`=`**（用于补位，当原数据字节数不是 3 的倍数时）。

### 【Q325】关于 cors 的响应头有哪些
- **Access-Control-Allow-Origin**：允许的源，`*` 或具体域名
- **Access-Control-Allow-Methods**：允许的 HTTP 方法
- **Access-Control-Allow-Headers**：允许的请求头
- **Access-Control-Allow-Credentials**：是否允许携带 Cookie
- **Access-Control-Expose-Headers**：允许 JS 读取的响应头
- **Access-Control-Max-Age**：预检请求缓存时间

### 【Q327】如何避免 CDN 为 PC 端缓存移动端页面
1. **使用 Vary 响应头**：`Vary: User-Agent`，让 CDN 按 UA 缓存不同版本
2. **不同域名/路径**：PC 用 `www.example.com`，移动端用 `m.example.com`
3. **响应式设计**：同一套 HTML/CSS，通过媒体查询适配，不需要区分缓存
4. **前端判断后跳转**：首页不发缓存，检测设备后跳转对应版本

### 【Q356】在 node 端如何向服务器上传文件
```javascript
// 使用 fs 读取文件 + http/axios 上传
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

const form = new FormData();
form.append('file', fs.createReadStream('/path/to/file.jpg'));

axios.post('https://example.com/upload', form, {
  headers: { ...form.getHeaders() }
});

// 或用 http 模块
const http = require('http');
const stream = fs.createReadStream('/path/to/file');
const req = http.request({ method: 'POST', host: '...', path: '/upload' });
stream.pipe(req);
```

### 【Q358】什么情况下会发送 OPTIONS 请求
**预检请求（Preflight）**：当跨域请求满足以下条件时会先发送 OPTIONS 询问服务器：
1. 使用了非简单方法（PUT、DELETE、PATCH 等，GET/POST/HEAD 以外）
2. Content-Type 不是 `application/x-www-form-urlencoded`、`multipart/form-data`、`text/plain`
3. 包含自定义请求头（如 Authorization 以外的头）
4. XMLHttpRequest 或 fetch 的跨域请求
5. ReadableStream 请求体

### 【Q359】CORS 如果需要指定多个域名怎么办
Access-Control-Allow-Origin **不支持多个值**。解决方案：
1. **白名单动态判断**：服务器读取请求的 Origin 头，如果匹配白名单，设置 `Access-Control-Allow-Origin: <匹配的Origin>`
2. **通配符限制**：`*` 但不能与 credentials 同时使用
3. **反向代理**：将多个域名反代到同一域下

```javascript
// 服务端动态判断
const allowedOrigins = ['https://a.com', 'https://b.com'];
const origin = req.headers.origin;
if (allowedOrigins.includes(origin)) {
  res.setHeader('Access-Control-Allow-Origin', origin);
}
```

### 【Q361】既然 cors 配置可以做跨域控制，那可以防止 CSRF 攻击吗
**CORS 不能完全防止 CSRF 攻击**。CORS 是限制跨域请求的响应能否被 JS 读取，但 CSRF 攻击主要利用的是浏览器**自动携带 Cookie** 发送请求的特性。CSRF 攻击用 form 表单提交或简单的 GET/POST（属于"非预检"请求）仍可跨域发送。防 CSRF 应该用：
- SameSite Cookie（Strict/Lax）
- CSRF Token
- 验证 Referer/Origin 头
- 敏感操作做二次验证

### 【Q387】http2 中 server push 与 websocket 有什么区别
- **HTTP/2 Server Push**：服务器主动推送静态资源（CSS/JS），用于加速页面加载。是单向的，只在请求响应周期内使用，不能交互通信。
- **WebSocket**：全双工通信协议，客户端和服务器可以随时互发消息。用于实时应用（聊天、游戏、实时数据推送）。需要协议升级（HTTP→WS）。

### 【Q388】简述下 TLS 握手过程
TLS 1.2 握手（简化版）：
1. **Client Hello**：客户端发送支持的加密套件列表、TLS 版本、随机数
2. **Server Hello**：服务器选定加密套件、TLS 版本、随机数，发送数字证书
3. **客户端验证证书**：用内置 CA 公钥验证证书合法性
4. **密钥交换**：客户端生成 Pre-Master Secret，用服务器公钥加密发送（RSA）或用 ECDHE 协商
5. **双方生成会话密钥**：用 Client Random + Server Random + Pre-Master Secret 通过 PRF 生成对称密钥
6. **加密通信验证**：双方发送 Finished 消息（加密），验证加解密正确
总耗时约 2-RTT（ECDHE）或 1.5-RTT（RSA）。TLS 1.3 缩短为 1-RTT。

### 【Q390】简单介绍一下 RSA 算法
RSA 是非对称加密算法，基于大整数因子分解的数学难题：
1. **密钥生成**：选两个大素数 p、q，计算 n = p×q，φ(n) = (p-1)(q-1)。选 e 与 φ(n) 互质。计算 d 使得 e×d ≡ 1 (mod φ(n))。公钥 (n, e)，私钥 (n, d)
2. **加密**：c = m^e mod n（用公钥）
3. **解密**：m = c^d mod n（用私钥）
4. **签名**：s = m^d mod n，验证 m = s^e mod n
在 HTTPS 中用于密钥交换和数字签名（证书签名）。

### 【Q391】https 层可以做哪些性能优化
1. **会话复用**：Session ID / Session Ticket 复用之前的 TLS 会话，减少握手
2. **OCSP Stapling**：服务器预先获取 OCSP 响应，减少客户端在线验证证书时间
3. **TLS 1.3**：握手从 2-RTT 降到 1-RTT，0-RTT 重连
4. **HSTS**：强制浏览器使用 HTTPS，节省 301 重定向时间
5. **ECDHE**：相比 RSA 密钥交换更快
6. **证书链优化**：减少中间证书，缩小证书大小
7. **False Start**：客户端不等 Finished 就发数据

### 【Q392】ECDHE 与 RSA 有何区别
- **RSA 密钥交换**：客户端生成 Pre-Master Secret，用服务器公钥加密传输。**不支持前向保密**（服务器私钥泄露后所有历史会话可解密）。
- **ECDHE 密钥交换**：基于椭圆曲线 DH，每次会话生成临时密钥对，不依赖服务器私钥传输。**支持前向保密**（PFS），即使私钥泄露也无法解密历史数据。速度更快，密钥更短安全性更高。
- 现代 HTTPS 基本都使用 ECDHE。

### 【Q394】https 中证书的格式化信息有哪些
X.509 证书包含：
- **颁发者（Issuer）**：CA 机构名称
- **主题（Subject）**：域名/公司信息
- **有效期**：Not Before / Not After
- **公钥**：算法 + 公钥数据
- **扩展字段**：SAN（Subject Alternative Name，支持多域名）、基本约束、密钥用法
- **签名算法 + 签名值**：CA 对证书的数字签名
- **序列号**：证书唯一标识
- **指纹**：SHA-256/SHA-1 指纹

### 【Q395】https 连接时如何保证证书没被废弃掉
1. **CRL（证书吊销列表）**：CA 定期发布吊销证书列表，浏览器下载检查。缺点是列表大、延迟高
2. **OCSP（在线证书状态协议）**：客户端实时查询 CA 服务器证书是否有效。缺点是隐私泄漏（CA 知道你访问了哪个网站）
3. **OCSP Stapling**：服务器预先从 CA 获取带签名的 OCSP 响应，TLS 握手时附带传给客户端。既保证实时性又保护隐私

### 【Q396】TLS1.3 相比 TLS1.2 有何不同
1. **握手更快**：1-RTT 握手（TLS 1.2 需 2-RTT），支持 0-RTT 重连
2. **移除不安全算法**：去掉 RSA 密钥交换、CBC 模式、RC4 流密码、SHA-1 哈希
3. **只保留安全套件**：仅支持 AEAD 加密（如 AES-GCM、ChaCha20-Poly1305）
4. **密钥交换强制前向保密**：只保留 ECDHE/DHE，不再有 RSA 密钥交换
5. **简化握手消息**：合并了多个步骤，减少交互
6. **加密更多握手消息**：证书等敏感信息更早进入加密通道

### 【Q398】在 wireshark 中如何抓包 https/http2
需要配置环境变量让浏览器/TLS 库导出对称密钥：
```bash
# 设置 SSLKEYLOGFILE 环境变量
export SSLKEYLOGFILE=/path/to/sslkeylog.log
# 启动浏览器
chrome
```
在 Wireshark 中：`Edit → Preferences → Protocols → TLS → (Pre)-Master-Secret log filename` 指定该文件。Wireshark 即可解密 HTTPS 流量。

HTTP/2 解密同上，因为 HTTP/2 在 TLS 之上。

### 【Q401】在 TLS 层如何优化网站性能
1. **升级 TLS 1.3**：握手 1-RTT，减少延迟
2. **启用 OCSP Stapling**：避免客户端额外请求验证证书
3. **使用 ECDSA 证书**：比 RSA 证书小，验证更快
4. **会话复用**：Session Tickets/IDs 避免重复握手
5. **证书链精简**：只发送必需中间证书
6. **启用 0-RTT**：重连时可以立即发送数据（有重放风险）
7. **选择合适的加密套件**：AES-GCM（有硬件加速）优先
8. **CDN/边缘节点**：缩短 TLS 握手 RTT

### 【Q419】DV、OV、EV 类的证书有何区别
- **DV（Domain Validation）**：只验证域名所有权，通过邮箱/DNS/CNAME 验证。最快，几分钟签发。浏览器显示挂锁图标。适合个人/小网站。
- **OV（Organization Validation）**：验证域名所有权 + 组织真实性（营业执照等）。浏览器显示挂锁图标，证书信息中有组织名。适合企业网站。
- **EV（Extended Validation）**：最严格验证（法律实体、运营地址等）。浏览器曾显示绿色地址栏/公司名（现在 Chrome 已弱化）。适合金融、电商等。

### 【Q420】https 中是如何进行身份认证的
1. 服务器将**数字证书**（包含公钥、域名、颁发者等信息）发送给客户端
2. 客户端用**内置的 CA 公钥**验证证书签名合法性
3. 通过**证书链**向上追溯到根 CA
4. 验证**域名匹配**（证书 SAN/CN 与访问域名对比）
5. 验证**有效期**和**吊销状态**（CRL/OCSP）
6. 通过后建立安全连接。这一过程确保了一端是真实的服务端（而非冒充者）——这也是中间人攻击被防御的关键。

### 【Q431】http 状态码 401 和 403 有什么区别
- **401 Unauthorized**：**未认证**（你是谁？），客户端没有提供身份凭证或凭证无效。响应应包含 WWW-Authenticate 头说明认证方式。常用于：未登录状态访问需要登录的页面。
- **403 Forbidden**：**无权限**（我知道你是谁但你没权限），服务器理解请求但拒绝执行。常用于：无访问权限、IP 黑名单、请求限制等。

### 【Q434】当服务器资源返回 304 时与那些 HTTP 响应头有关
304 Not Modified 与以下请求/响应头有关：
- 响应头：**ETag**（资源标识符）、**Last-Modified**（最后修改时间）、**Cache-Control**（缓存策略）
- 请求头：**If-None-Match**（对应 ETag）、**If-Modified-Since**（对应 Last-Modified）
- 当服务器验证 If-None-Match 值匹配当前 ETag，或 If-Modified-Since 时间没有更早的修改，返回 304 不带响应体。

### 【Q442】http3 解决了什么问题
主要解决 TCP 层的**队首阻塞**问题。HTTP/2 虽然应用层可以多路复用，但 TCP 丢包时整个连接所有流都会等待重传。

HTTP/3 基于 **QUIC（UDP）**：
- 每个流独立传输，丢包只影响自己的流
- 连接迁移：切换网络（WiFi→4G）不需要重建连接
- 0-RTT 握手：重连时直接发送数据
- 内置 TLS 1.3 加密

### 【Q554】SameSite Cookie 有哪些值，是如何预防 CSRF 攻击的
- **Strict**：完全禁止跨站发送 Cookie，最严格。点击外部链接也不会带 Cookie，需要重新登录。
- **Lax**（Chrome 默认值）：跨站时不发送 Cookie，但"安全"的导航（如点击链接、GET 请求重定向）会发送。基本不影响用户体验。
- **None**：所有跨站请求都发送 Cookie，但必须配合 `Secure` 属性（仅 HTTPS）。

防 CSRF 原理：SameSite 限制了第三方网站发起请求时 Cookie 的携带，使 CSRF 攻击无法携带用户的认证信息，服务器会视其为未登录请求。

### 【Q560】Data URL 的应用场景及如何生成
**格式**：`data:[<mediatype>][;base64],<data>`

**应用场景**：
- 小图标/小图片内嵌，减少 HTTP 请求
- 邮件中嵌入图片
- HTML 中直接嵌入字体/图片

**生成方式**：
```javascript
// 浏览器端 - FileReader
const reader = new FileReader();
reader.onload = e => console.log(e.target.result); // data:image/png;base64,...
reader.readAsDataURL(file);

// Node 端
const b64 = fs.readFileSync('img.png').toString('base64');
const dataUrl = `data:image/png;base64,${b64}`;

// Canvas
canvas.toDataURL('image/png');
```

### 【Q578】HTTP 响应头 cache-control: s-maxage=0 是什么意思
`s-maxage` 是给**共享缓存（CDN/代理）**看的指令。s-maxage=0 表示：**共享缓存必须立即向源服务器验证**（即每次都做协商缓存）。但是对浏览器私有缓存没有影响，私有缓存仍然遵循 max-age 或其他指令。

### 【Q579】http 缓存控制中 Cache-Control 为 public 与 private 有何区别
- **public**：允许所有缓存（浏览器私有缓存、CDN、代理缓存）存储。即使响应需要认证。
- **private**：只允许浏览器私有缓存存储，CDN/代理等中间缓存不能存储（如用户个人信息）。
- 默认值取决于情况，通常有 Authorization 头时为 private。

### 【Q580】http 方法 get 与 post 有何区别
| 维度 | GET | POST |
|------|-----|------|
| 语义 | 获取资源 | 提交/创建资源 |
| 参数位置 | URL 查询字符串 | 请求体 |
| 长度限制 | URL 长度受限（~2KB） | 无限制 |
| 安全性 | 参数暴露在 URL/历史日志 | 参数在请求体 |
| 幂等性 | 幂等 | 非幂等 |
| 缓存 | 可缓存 | 默认不缓存（必须协商） |
| 书签/分享 | 可收藏 | 不可收藏 |

### 【Q583】http 状态码 204 使用在什么场景
- 预检请求 OPTIONS 返回（常见场景）
- 删除/更新操作成功但不需返回内容
- 表单提交后不希望页面跳转/刷新
- Ping/Health Check 请求
- **关键特性**：204 响应没有响应体，浏览器接收到后不会改变页面内容。

### 【Q584】现代前端应用应如何配置 HTTP 缓存机制
1. **HTML 入口文件**：`Cache-Control: no-cache` 或 `max-age=0`，每次协商验证
2. **JS/CSS 构建产物**：文件名带内容 hash，`Cache-Control: public, max-age=31536000, immutable`，永久强缓存
3. **图片/字体**：带 hash版本用强缓存，不常变的用 max-age 较长时间
4. **API 数据**：按数据特性设置，动态数据 `no-cache`，静态数据可设短时间缓存
5. **Service Worker**：对 SPA 做更精细的离线缓存控制
6. **CDN**：配合构建工具的 hash 化文件名实现灰度发布

### 【Q585】如何确保你们的项目开启了 gzip
1. **Nginx 配置**：检查 `gzip on;` 和相关配置（gzip_types、gzip_min_length）
2. **浏览器 DevTools**：Network 面板查看响应头 `Content-Encoding: gzip`
3. **curl**：`curl -H "Accept-Encoding: gzip" -I https://example.com` 查看是否有 `Content-Encoding: gzip`
4. **响应体大小**：实际传输大小（Transfer Size）< 源大小（Content Size），说明被压缩了
5. **Lighthouse/WebPageTest** 检测

### 【Q586】HTTP 有哪些常见的请求头和响应头
**通用头**：Cache-Control, Connection, Date, Transfer-Encoding

**常用请求头**：
- Accept / Accept-Encoding / Accept-Language
- Authorization / Cookie
- Content-Type / Content-Length
- Host / Origin / Referer
- User-Agent
- If-None-Match / If-Modified-Since
- Cache-Control

**常用响应头**：
- Content-Type / Content-Length / Content-Encoding
- Cache-Control / ETag / Last-Modified / Expires
- Set-Cookie
- Access-Control-Allow-Origin / Access-Control-Allow-Credentials
- Location（重定向）
- Server / X-Powered-By
- Content-Security-Policy
- Strict-Transport-Security

### 【Q588】什么是 HSTS
**HTTP Strict Transport Security**：强制浏览器仅通过 HTTPS 访问网站。服务器返回 `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`。好处：
- 避免 301 重定向 HTTPS 的性能损耗
- 防止 SSL 剥离攻击（中间人降级为 HTTP）
- 可申请加入浏览器 HSTS Preload 列表，首次访问也走 HTTPS

### 【Q589】http 中 referer 请求头是做什么的
指示**当前请求来自哪个页面 URL**。用途：
- 统计分析（知道用户从哪个页面跳转过来）
- 防盗链（检查 Referer 是否为本站域名，拒绝外站请求）
- CSRF 防御（验证 Referer 是否可信源）
- 缓存策略控制（如 Vary: Referer）
注意隐私问题：HTTPS→HTTP 不会发送 Referer（浏览器策略）。

### 【Q616】在 nginx 中如何配置 HTTP 协商缓存
```nginx
location /static/ {
    # 设置 ETag（默认开启）
    etag on;
    # 或手动设置 Last-Modified
    expires epoch;  # 不做强缓存，每次都走协商缓存
    add_header Cache-Control "no-cache";
}
# 配合强缓存
location ~* \.(js|css)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
# HTML 走协商
location / {
    expires -1;
    add_header Cache-Control "no-cache, must-revalidate";
}
```

### 【Q617】什么是 base64 与 URL Safe base64
- **Base64**：标准 64 字符（A-Z, a-z, 0-9, +, /），用 = 补齐。用于二进制到文本转换。
- **URL Safe Base64**：将 `+` 替换为 `-`，`/` 替换为 `_`，去掉尾部 `=`。因为标准 Base64 的 +/ 字符在 URL 中有特殊含义（+ 表示空格）。常用于 JWT Token 等 URL 场景。

### 【Q639】HTTP 与 TCP 中的 keep-alive 各是什么
- **HTTP Keep-Alive**：长连接（HTTP/1.1 默认），一次 TCP 连接发送多个 HTTP 请求/响应，复用 TCP 连接。HTTP 头 `Connection: keep-alive`。
- **TCP Keep-Alive**：TCP 协议层的保活机制，在连接空闲一段时间后发送探测包，确认对端是否仍存活，防止半开连接。操作系统设置，非 HTTP 特有。`net.ipv4.tcp_keepalive_time` 等。

### 【Q650】http 各个版本间各有什么改进
- **HTTP/0.9**：仅 GET，仅 HTML，无 Header
- **HTTP/1.0**：增加 Header、状态码、POST/HEAD、Content-Type
- **HTTP/1.1**：Keep-Alive 长连接、管道化、Host 头（虚拟主机）、缓存控制、断点续传、分块传输
- **HTTP/2**：多路复用、二进制分帧、首部压缩（HPACK）、Server Push、流优先级
- **HTTP/3**：基于 QUIC（UDP）、解决 TCP 队首阻塞、0-RTT 重连、连接迁移

### 【Q651】简述 http3，http3 解决了什么问题
HTTP/3 基于 **QUIC 协议（UDP）**：
- **解决 TCP 队首阻塞**：TCP 丢包导致整个连接阻塞，QUIC 每个 Stream 独立，丢包只影响单流
- **0-RTT 握手**：复用之前连接可实现 0-RTT 发送数据
- **连接迁移**：切换网络（WiFi→4G）时连接不中断（基于 Connection ID 而非 IP+端口）
- **内置 TLS 1.3**：安全性内建于传输层

### 【Q652】http2 中 Stream 与 Frame 是什么关系
- **Frame（帧）**：HTTP/2 最小通信单元，二进制格式，每个帧属于一个 Stream。帧类型：HEADERS、DATA、SETTINGS、PRIORITY、RST_STREAM、PUSH_PROMISE、PING、GOAWAY、WINDOW_UPDATE、CONTINUATION
- **Stream（流）**：虚拟的信道，每个请求/响应对应一个 Stream，由多个 Frame 组成（双向消息序列）。通过 Stream ID 标识（客户端发起的为奇数，服务器为偶数）
- **关系**：一个 TCP 连接包含多个 Stream，一个 Stream 包含多个 Frame。

### 【Q658】什么是点击劫持(ClickJacking)，如何预防
**点击劫持**：攻击者将目标网站嵌入透明的 iframe，诱骗用户点击看似无害的按钮，实际点击了目标网站的敏感操作（如转账、授权）。

**防御方法**：
1. **X-Frame-Options**：`DENY`（禁止被嵌入）、`SAMEORIGIN`（仅同源可嵌入）
2. **CSP frame-ancestors**：`Content-Security-Policy: frame-ancestors 'self'`
3. **JS Frame Busting**：`if (top !== self) { top.location = self.location; }`（不推荐，可被绕过）
4. 优先使用 CSP frame-ancestors（更灵活，被 CSP 规范替代了 X-Frame-Options 的现代能力）。

### 【Q687】https 如何被抓包，原理是什么
HTTPS 抓包本质是**中间人代理**：
1. 抓包工具（Charles/Fiddler）作为代理服务器
2. 客户端发出 CONNECT 请求到代理
3. 代理代替客户端与目标服务器建立 TLS 连接
4. 代理用自己的 CA 证书签发一个伪造的目标域名证书发给客户端
5. 客户端需**信任代理的根证书**（安装到系统），才能不被警告
6. 代理解密→查看→重新加密→转发，实现明文抓包

### 【Q696】OCSP Stapling 是什么
服务器提前从 CA 获取 OCSP 响应（证明证书未吊销），并将该响应缓存在服务器端。TLS 握手时服务器将已签署的 OCSP 响应随证书一起发给客户端。优势：
- 客户端不需要额外查询 OCSP 服务器，减少延迟
- 保护用户隐私（CA 不知道用户访问了哪个网站）
- 减轻 OCSP 服务器的负载

### 【Q700】http client 中如何得知已接收完所有响应数据
有以下几种方式判断：
1. **Content-Length**：响应头告知精确字节数，接收够就结束
2. **Transfer-Encoding: chunked**：分块传输，以 `0\r\n\r\n`（零长度块）标记结束
3. **连接关闭**：HTTP/1.0 或没有 Content-Length 时，TCP 连接关闭即结束
4. **特殊响应/HEAD 请求**：HEAD 响应没有响应体，直接结束
5. 对于 SSE（Server-Sent Events），流式响应持续不会主动结束

### 【Q738】websocket 和短轮询有什么区别
| 维度 | WebSocket | 短轮询 |
|------|-----------|--------|
| 通信方式 | 全双工 | 单向（客户端→服务器） |
| 连接 | 一次握手，持久连接 | 每次请求新建 HTTP 连接 |
| 实时性 | 服务器可主动推送，实时性高 | 依赖轮询间隔，有延迟 |
| 带宽消耗 | 帧头部小（2-14字节） | 每次完整的 HTTP 头 |
| 适用场景 | 聊天、协作、游戏 | 低频更新的简单数据 |
| 服务器压力 | 低（事件驱动） | 高（大量无用请求） |

### 【Q741】我们上传图片为 Blob/File 对象时，是如何向服务器端传送数据的
使用 **FormData** 或直接发送 **Blob/File** 数据：

**方式一：FormData（推荐，传统方式）**
```javascript
const formData = new FormData();
formData.append('file', file); // file 是 File/Blob 对象
fetch('/upload', { method: 'POST', body: formData });
```
浏览器自动设置 `Content-Type: multipart/form-data; boundary=...`

**方式二：直接发送 Blob/File**
```javascript
fetch('/upload', {
  method: 'POST',
  body: file, // 直接作为请求体
  headers: { 'Content-Type': file.type }
});
```

**方式三：Base64**
```javascript
const reader = new FileReader();
reader.readAsDataURL(file); // data:image/png;base64,...
```
