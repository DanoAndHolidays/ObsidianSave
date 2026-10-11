# WebSocket💡
https://juejin.cn/post/7444455886149795892#heading-31

![[Pasted image 20261011181815.png]]

WebSocket 仅在建立连接时使用 HTTP，之后独立运行，并不是基于 HTTP 协议的

WebSocket 和 Socket 是不同的概念，Java 中：
```java
// 创建一个 TCP Socket，连接到服务器
Socket socket = new Socket("127.0.0.1", 8080);

// 往连接中发送数据
OutputStream out = socket.getOutputStream();
out.write("hello".getBytes(StandardCharsets.UTF_8));

// 读取服务端返回的数据
InputStream in = socket.getInputStream();

// 关闭连接
socket.close();
```

这里没有直接使用 HTTP，也没有使用 WebSocket，通过 Socket 使用 TCP 连接，至于发送的数据是什么格式，可以由你自己决定，这就是为什么说 Socket 是==编程接口==，WebSocket 是应用层协议，两者不是一个层面的概念

WebSocket 继承了 TCP 的全双工能力，并提供了应用层的封装，特点：

- 基于 TCP 协议，而非基于 HTTP
- 支持服务器主动推送数据到客户端
- 全双工通信，双方都可以主动发送数据
- 适用于需要频繁交互的场景（游戏、聊天室、协同办公等）

---
## 服务器推送技术演进

- HTTP 定时轮询：客户端定期发送请求，频繁消耗带宽且有延迟
- 长轮询（Comet）：设置较长超时时间（如30秒），减少请求次数，响应更及时
- WebSocket：真正的全双工通信协议

---
## 连接建立
![](https://i0.hdslb.com/bfs/note/f2ce6d276e694ee9ccc2feeb30f679720ebce744.png@690w_!web-note.webp)

客户端先发起：
```
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

其中：

- `Upgrade: websocket`：希望切换为 WebSocket 协议。
- `Connection: Upgrade`：告诉当前 HTTP 连接需要升级。
- `Sec-WebSocket-Key`：用于握手校验，不是加密密钥。


服务器同意后返回：
```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: ...
```

WebSocket 连接生命周期

1. 建立底层网络连接，必要时完成 TLS 握手
2. 客户端发送 WebSocket HTTP 握手请求
3. 服务器返回 `101 Switching Protocols`
4. 切换到 WebSocket 数据帧通信
5. 双方双向收发消息，可以通过 Ping/Pong 检查连接
6. 发送 Close 帧，正常关闭连接



---
## 数据格式

- 使用 Frame(帧)结构传输数据
- 主要字段：
	- opcode：标识数据类型(文本、二进制等)
	- payload length：数据长度
	- payload data：实际数据内容
- 采用消息头+消息体格式，解决 TCP 粘包问题[[TCP & UDP]]


---
## 面经
这道题不是简单问 Java 垃圾回收，而是要看你是否理解长连接生命周期和高并发资源管理。

### 1. 为什么 WebSocket 比普通 HTTP API 更容易出现资源问题？
因为 WebSocket 通常维持较长时间的连接。

假设服务端有 10 万个在线用户。

每个连接可能需要维护：
```
WebSocket 连接
    ├── 连接对象
    ├── TCP 收发缓冲区
    ├── 用户身份信息
    ├── 消息发送队列
    ├── 心跳状态
    └── 相关任务与定时器
```

单个连接看起来开销不大，但乘以大量连接，就会消耗可观的内存。

还要分清两种问题：

- 内存泄漏：对象已经没有业务用途，却仍然被引用，导致无法回收。
- 内存占用过高：大量正常连接、数据缓冲、消息积压导致内存增加，不一定是泄漏。

### 2. 最常见的问题：断开的连接没有移除
例如你在 Java 中维护：
```
Map<Long, Session> sessions = new ConcurrentHashMap<>();
```

用户上线：
```
sessions.put(userId, session);
```

用户下线后，如果没有执行：
```
sessions.remove(userId, session);
```

Map 仍然持有这个 Session 对象。即便对应的网络连接已经断开，Session 及其引用的其他对象也可能继续留在内存中。

这样，服务器运行越久，内存占用就可能不断增加。因此应该在连接正常关闭、异常断开和服务器清理时，做好统一的资源释放。

### 3. 心跳机制：Ping/Pong
心跳主要用于发现失效连接。

例如用户突然断网，服务器未必能够立即察觉。WebSocket 协议提供 Ping/Pong 控制帧：
```
服务器                       客户端

Ping ───────────────────────→
     ←─────────────────────── Pong

Ping ───────────────────────→
     ←─────────────────────── Pong
```

假设服务器每 30 秒发送一次 Ping（只是配置示例）。

如果连续多次心跳失败，就可以按照超时策略关闭连接，清理相关资源。

注意两点：

- WebSocket 原生 Ping/Pong 和业务层的 JSON 心跳不是一回事。
- 浏览器原生 WebSocket API 不直接暴露发送 Ping 控制帧的方法。通常由底层实现自动响应，或者通过业务消息自行实现心跳。

### 4. 最容易被忽略的问题：消息队列无限增长
发送速度高于消耗速度，消息持续积压

这就引出了 背压（Backpressure）。背压是指：当下游处理能力不足时，上游需要减慢发送速度，或者采用其他措施限制积压。

工程中常见做法：

- 给每个连接设置有界发送队列。
- 限制单条消息最大大小。
- 对消息发送进行限流。
- 监控发送缓冲区和积压情况。
- 对持续消费过慢的客户端采取降速或断开连接，并依靠持久化记录重连补拉。

浏览器 WebSocket 有 `bufferedAmount` 属性，可以观察本地排队等待发送的数据量。

MDN 也特别指出，标准 `WebSocket` API 不具备自动背压机制，因此开发者需要自己控制消息生产速度。

### 5. 使用非阻塞 I/O 模型
如果你用传统的阻塞 I/O 模型，并且给每一个连接分配一个操作系统线程，那么大量并发连接会带来很高的线程资源成本。

少量 I/O 工作线程可以管理大量网络连接，而不需要为每条连接配置一个长期阻塞的操作系统线程。
