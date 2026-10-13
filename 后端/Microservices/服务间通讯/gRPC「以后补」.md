# 四、gRPC：微服务面试的真正重点

## 1. 什么是 gRPC？

![Generated-code reference | Java | gRPC](https://images.openai.com/static-rsc-4/TKzWtN1yiG287htc5x_cUIavOoBYrmvtF1zv_27G4KHB_tb641Q6OuLQm-DwYQyTXIDHYKPo1kMFYz5kEA_jc49Ty-8sQRbEtx6nF-8SVDwjLztJZdQwVfz7uo34Xotc_6TaVeXd1ZIUf-_R62b9sN-de1J8-zXejsJa0kTeYJ4?purpose=inline)

gRPC

高性能、跨语言 RPC 框架

[官方文档](https://grpc.io/docs/)

gRPC 是一套通用 RPC 框架，典型特点包括：

- 基于 HTTP/2 进行通信。
    
- 默认使用 Protobuf 定义服务接口及消息格式。
    
- 支持 Java、Go、Python、C++、JavaScript 等多种语言。
    
- 支持普通请求—响应，以及多种流式通信。
    
- 可以生成客户端和服务端的接口代码。
    
    ![](https://www.google.com/s2/favicons?domain=https://grpc.io&sz=32)
    
    gRPC
    
    +1
    

你会发现，gRPC 与 tRPC 的核心侧重点很不一样。

tRPC 强调 TypeScript 开发体验和类型推导；gRPC 更强调跨语言的服务契约、通信机制与流式能力。

## 2. Protobuf 是什么？

Protobuf = Protocol Buffers，是 Google 推出的结构化数据序列化方案。

传统的 JSON：

```
{
  "id": 1001,
  "name": "Dano"
}
```

它的优点是可读性很好，但是传输时包含字段名称和文本格式的数据表示。

而 Protobuf 可以使用紧凑的二进制格式编码数据，降低数据体积，并支持高效序列化、反序列化。

使用 Protobuf，首先要定义一个 `.proto` 文件：

```
syntax = "proto3";

package user;

service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
}

message UserRequest {
  int64 id = 1;
}

message UserResponse {
  int64 id = 1;
  string name = 2;
  int32 age = 3;
}
```

这段代码就是一份服务契约。

逐个解释：

`service UserService`：定义 RPC 服务。

`rpc GetUser`：声明远程调用的方法。

`UserRequest`：请求消息的数据结构。

`UserResponse`：响应消息的数据结构。

`int64 id = 1`：这里的 `1` 是 Protobuf 的字段编号（Field Number），而不是给 id 赋值为 1。

### 字段编号为什么重要？

Protobuf 二进制编码会依赖字段编号识别数据。

当 API 已经投入使用时，不应该随意修改已有字段编号，也不应该把废弃编号分配给其他字段。

这涉及跨版本兼容性。比如新增一个普通字段，在遵守兼容规则的情况下，旧客户端通常可以忽略这个不认识的字段。

![](https://www.google.com/s2/favicons?domain=https://protobuf.dev&sz=32)

Protocol Buffers Documentation

+1

这是一个很好的面试加分点。

## 3. `.proto` 文件有什么用？

gRPC 的典型开发流程：

```
编写 user.proto
       ↓
  protoc + 插件
       ↓
生成客户端 Stub / 服务端接口
       ↓
服务端实现接口
       ↓
客户端调用 Stub
       ↓
实际发生网络 RPC 调用
```

例如，你有一个 Java 用户服务，一个 Go 订单服务。

只需要双方遵守相同的 Protobuf 契约，就可以使用各自语言生成的 gRPC 代码进行通信。

这就是 gRPC 很适合跨语言微服务的原因之一。

## 4. HTTP/2 为什么有利于 gRPC？

HTTP/2 本身有多路复用、二进制分帧、头部压缩等能力。

其中最重要的是多路复用。

简化示意：多个 RPC 调用共享 HTTP/2 连接

Stream 是 HTTP/2 流，不代表必须使用 gRPC 的业务流式 RPC。

HTTP/2 可以让多个 RPC 请求作为不同的 Stream 在一条连接上并发传输，而不是每个请求都必须新建一条 TCP 连接。

但你不能说 HTTP/2 就完全消除了队头阻塞。TCP 层的丢包仍可能影响同一连接中的其他流，并且 HTTP/2 还有并发流数量限制。

也不能简单地说 gRPC 永远比 REST 快。是否更快取决于数据规模、连接复用、序列化成本、服务器实现和网络环境。gRPC 官方也明确提醒，过多长连接流式 RPC 可能增加负载均衡和扩展的复杂度。

![](https://www.google.com/s2/favicons?domain=https://grpc.io&sz=32)

gRPC

## 5. gRPC 的四种调用模式（必考）

这是面试里最容易展开的一部分。

Unary（一元调用）

一个请求 → 一个响应

Server Streaming

一个请求 → 多个响应

Client Streaming

多个请求 → 一个响应

Bidirectional Streaming

双方持续发送消息

客户端发送

服务端发送

四种模式分别举例：

|模式|业务场景|
|---|---|
|Unary|查询用户信息、检查库存|
|Server Streaming|日志实时推送、服务端分批返回数据|
|Client Streaming|客户端上传连续数据块，最后获得汇总|
|Bidirectional Streaming|实时双向通信、持续交换消息|

对应 Protobuf 的语法：

```
service ExampleService {
  // 普通请求-响应
  rpc GetUser (Request) returns (Response);

  // 服务端流
  rpc WatchLogs (Request) returns (stream Response);

  // 客户端流
  rpc UploadData (stream Request) returns (Response);

  // 双向流
  rpc Chat (stream Request) returns (stream Response);
}
```

这里的四种通信模式是 gRPC 官方定义的核心能力。

![](https://www.google.com/s2/favicons?domain=https://grpc.io&sz=32)

gRPC

## 6. 前端浏览器能直接调用 gRPC 吗？

这是适合你拿来展示前端背景的一道题。

浏览器中的普通 JavaScript 通常不能直接使用原生 gRPC 客户端那套完整的 HTTP/2 能力。

因为浏览器网络 API 不开放原生 gRPC 所需的全部 HTTP/2 帧和 Trailer 控制能力。

所以一般使用：

- gRPC-Web
    
- 支持浏览器协议转换的代理或网关
    

典型通信路径：

```
React 浏览器
     ↓
   gRPC-Web
     ↓
Envoy / Gateway
     ↓
   原生 gRPC
     ↓
  Java 后端
```

官方的 gRPC-Web 示例就是使用 Envoy 将浏览器侧请求转发到原生 gRPC 服务。

![](https://www.google.com/s2/favicons?domain=https://grpc.io&sz=32)

gRPC

还有一个细节：官方 gRPC-Web 的传统实现主要支持 Unary 和 Server Streaming，并不等价于直接在浏览器获得原生 gRPC 的所有四种调用模式。

这也是为什么你在浏览器实时应用中仍然经常看到 WebSocket、SSE，而不是全部使用 gRPC。
