# Cookie
用于在前端对后端发送请求时会带上cookie中的内容，但其存储在本地且可以直接访问查看的特性，使其不能存储用户的私密信息与账密
**单个 Cookie 的大小不能超过 4KB（即 4096 字节）**。

cookie 没有设置 Expires 和 Max-Age 时，被当作**会话 Cookie（Session Cookie）**，浏览器关闭时自动删除。只在浏览器会话期间存在，关闭浏览器标签/窗口即清除。

判断 Cookie 是否生效的核心维度是**域名、路径和协议**，而端口号是被浏览器完全忽略的因素：
1. 不区分端口号（共享）根据 RFC 6265 规范，Cookie 的作用域仅由 Domain（域名）和 Path（路径）决定，端口号不参与 Cookie 的匹配逻辑。这意味着，只要域名相同，无论端口是否不同，Cookie 都是共享的。例如，在 http://localhost:8080 设置的 Cookie，在访问 http://localhost:3000 时同样会被携带发送。如果两个端口的服务使用了相同的 Cookie 键名和 Path，后写入的值会直接覆盖前面的值，这在多应用部署时极易引发登录态错乱等安全问题。
2. 严格区分协议（隔离）浏览器为 http 和 https 维护了完全独立的 Cookie 容器。即使域名和端口完全相同，只要协议不同，Cookie 也是相互隔离、无法共享的。例如，http://localhost:8080 写入的 Cookie，在 https://localhost:8080 中是完全不可见的。此外，如果 Cookie 被设置了 Secure 属性，则它只能在 HTTPS 协议的请求中被发送；若目标地址是 HTTP 协议，浏览器会直接拒绝发送该 Cookie。

### 属性详解
```javascript
// Cookie 格式：key=value; attributes
document.cookie = "username=john; domain=.example.com; path=/; max-age=3600; secure; samesite=strict";
```

Cookie 主要属性包括：
- **key=value**：键值对
- **domain**：作用域名
	  - 设置为 `.a.com` 与`a.com`可作用于 a.com 及其所有子域名
	  - 不设置和设置则仅作用于当前域名
- **path**：URL路径限制（较少使用）
- **max-age**：存活时间（秒），优先级高于**expires**
	  - 正数：存活时间
	  - 为零：会话结束时删除
	  - 负数：立刻删除
- **expires**：绝对过期时间（GMT格式）
- **secure**：仅通过HTTPS传输![[Pasted image 20260610100327.png]]
- **httponly**：禁止JavaScript访问（增强安全性），这种cookie只能由浏览器与服务器来控制![[Pasted image 20260610100200.png]]
- **samesite**：跨站请求限制
	  - `Strict`：严格模式，完全禁止跨站发送
	  - `Lax`：宽松模式，允许部分安全请求跨站发送
	  - `None`：无限制（必须与secure同时使用）
- 剩余的属性使用的不多，就不看了

![[Pasted image 20260610094548.png]]

仔细来看，一条cookie就是一个键值对 + 后面的属性
对于更新操作，我们可以直接覆盖cookie的键值，如果新增，就使用新的键，更新属性就使用对应的键，属性可以不写：
```js
// 1. 创建/设置 Cookie (有效期为1小时)
document.cookie = "username=John Doe; max-age=3600; path=/";

// 2. 读取 Cookie
var allCookies = document.cookie;
console.log(allCookies); // 输出当前页面所有可访问的cookie字符串

// 3. 修改 Cookie (直接重新赋值同名cookie即可覆盖)
document.cookie = "username=Jane Doe; max-age=3600; path=/";
// 不写键的值也可以
document.cookie = "username=; max-age=3600; path=/";

// 4. 删除 Cookie (将过期时间设置为过去的时间点)
document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
```
