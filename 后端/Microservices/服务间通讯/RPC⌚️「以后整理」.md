# RPC
**R**emote **P**rocedure **C**all，远程过程调用

RPC 是一种通信模型，让开发者能够像调用本地函数一样，调用另一台机器上的函数或服务方法。

普通的本地方法调用：
```
User user = userService.getUserById(1001);
```

但现在你把系统拆成两个微服务：

- 订单服务：Order Service
- 用户服务：User Service

订单服务需要用户信息，但用户服务部署在另一台服务器上

这时，你可以使用 RPC：
```
User user = userRpcService.getUserById(1001);
```

背后发生的是 RPC 的典型请求—响应流程（简化示意）
![[Pasted image 20261013220357.png]]

具体经历六个步骤：

1. 客户端调用本地代理（Stub）
2. RPC 框架把方法名、参数等信息编码并序列化
3. 通过网络将请求发送到远程服务器
4. 服务端解码请求，找到并执行目标方法
5. 服务端将执行结果序列化并返回
6. 客户端反序列化结果，交给业务代码

RPC 的本质并不是让远程函数变成真正的本地函数，而是==隐藏==底层网络通信的==复杂性==

本地调用主要考虑函数执行错误，而远程调用还要考虑网络延迟、连接中断、超时、重试、服务不可用、请求重复执行等问题

## 通信模型
严格来说，RPC ==不是==某一个特定的==网络协议==，而是一种远程调用的通信模型

RPC 系统往往涉及几个不同层次：

|层次|作用|示例|
|---|---|---|
|API 定义|定义服务与方法|Java Interface、`.proto`、TypeScript 类型|
|序列化|将数据编码用于传输|JSON、Protobuf|
|通信传输|将请求发送给对方|HTTP/1.1、HTTP/2、TCP|
|RPC 框架|封装调用、编码、错误等|gRPC、tRPC、Dubbo|

例如 gRPC 的常见组合是：`gRPC + HTTP/2 + Protobuf`

但并不是所有 RPC 都要走 HTTP，也不是所有 RPC 都采用二进制数据

### RPC 和 HTTP
HTTP 是通信协议；RPC 是调用模型。RPC 可以基于 HTTP 实现，因此两者并不是互斥关系。

比如你使用 HTTP POST 请求：
```
POST /rpc
Content-Type: application/json

{
  "method": "getUserById",
  "params": {
    "id": 1001
  }
}
```

这就是一种基于 HTTP 的 RPC 风格通信。

### RPC、tRPC、gRPC、REST、Dubbo
先看这张表，把整个知识体系建立起来

|技术|本质|核心特点|
|---|---|---|
|RPC|通信模型|像调用函数一样调用远程服务|
|REST|API 架构风格|围绕资源和 HTTP 语义设计|
|tRPC|TypeScript RPC 框架|端到端类型安全、自动类型推导|
|gRPC|通用 RPC 框架|跨语言、Protobuf、HTTP/2、流式通信|
|JSON-RPC|RPC 协议规范|使用 JSON 表示远程调用|
|Apache Dubbo|分布式 RPC 与服务治理框架|Java 生态、服务发现、负载均衡等|
|Apache Thrift|跨语言 RPC 框架|IDL、代码生成、多种传输与序列化方案|

假设我们要获取用户信息

REST 风格：
```
GET /users/1001
```

RPC 风格：
```
userService.getUserById(1001)
```

从 API 设计思想来看：

- REST 更关注资源（Resource），例如用户、订单、商品。
- RPC 更关注操作（Procedure），例如获取用户、创建订单、取消支付。

REST 通常使用 GET、POST、PUT、PATCH、DELETE 等 HTTP 方法来表达操作语义。

RPC 不要求必须把操作映射到某个特定 HTTP 方法上。

但是别被表面形式误导了。
```
POST /users/getUserById
```

虽然使用 HTTP，但它更偏向 RPC 风格，而不是典型的 REST 资源风格。

两者并不是直接对立的：

- REST 更适合提供通用、资源导向的 HTTP API，方便浏览器、第三方系统和调试工具调用
- RPC 更强调服务方法调用和类型契约，在微服务内部通信和复杂服务调用中非常常见。具体选择要结合调用场景、性能要求以及团队技术栈

注意，REST 不等于 JSON，RPC 也不等于二进制协议



# 五、其他 RPC 技术，你也要能分得清

## 1. JSON-RPC

JSON-RPC 是一种使用 JSON 表示远程方法调用的轻量级协议规范。

例如客户端发送：

```
{
  "jsonrpc": "2.0",
  "method": "getUser",
  "params": {
    "id": 1001
  },
  "id": 1
}
```

服务端返回：

```
{
  "jsonrpc": "2.0",
  "result": {
    "id": 1001,
    "name": "Dano"
  },
  "id": 1
}
```

其中：

- `method`：远程方法名。
    
- `params`：调用参数。
    
- `id`：请求标识，用于匹配响应。
    
- `result`：执行结果；失败时返回 `error`。
    

JSON-RPC 2.0 还支持 Notification（不要求响应的通知）和批量调用。

![](https://www.google.com/s2/favicons?domain=https://www.jsonrpc.org&sz=32)

JSON-RPC

### JSON-RPC 和 MCP 的关系

这里可以联系 Agent。

你最近关注的 MCP（Model Context Protocol），其消息格式就是基于 JSON-RPC 2.0 的。

比如 MCP Client 想调用一个工具，可以发送类似：

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Shanghai"
    }
  }
}
```

这里 JSON-RPC 负责表达“调用哪个方法、传什么参数、如何对应响应”。

MCP 则在上面进一步定义工具发现、资源、协议生命周期等约定。

![](https://www.google.com/s2/favicons?domain=https://github.com&sz=32)

GitHub

所以：

MCP 是一个具体的协议体系，JSON-RPC 是其消息通信基础之一。

## 2. Apache Dubbo

![Apache Dubbo Logo PNG Vector (SVG) Free Download](https://images.openai.com/static-rsc-4/CDsc9VnYc7-IRFrrbioIhOJ9y5k0QqdwQCNGfNyVss4C2nlkaHGUWl3bypce7kWAUpAEr4XFMw5Nr4Zq9JMUCpuctWeX5mczlqPM1w23SwJnwdONGuyQC0A-cTMFOAFnaVXhJbAiN-5xT1ObtfbBj7LW6TJLb3-q1FFInDI1IQ4?purpose=inline)

Apache Dubbo

Java 微服务体系里非常值得了解的 RPC 框架

Dubbo 不仅提供 RPC 通信能力，还提供服务发现、负载均衡、集群容错等服务治理功能。

Java 服务之间可以通过接口定义服务：

```
public interface UserService {
    User getUserById(Long id);
}
```

调用方通过 Dubbo 提供的远程服务引用来调用它，实际网络访问由框架完成。

Dubbo 支持不止一种通信协议，包括传统 Dubbo2 协议和 Triple 协议。

尤其要了解 Triple：它是 Dubbo3 引入的、兼容 gRPC 的 HTTP RPC 协议，支持 HTTP/1、HTTP/2 和流式通信。Dubbo 官方目前推荐新项目优先考虑 Triple。

![](https://www.google.com/s2/favicons?domain=https://dubbo.apache.org&sz=32)

Apache Dubbo

Dubbo 和 gRPC 的区别：

gRPC 更侧重跨语言 RPC 的通信规范与实现，Dubbo 还提供较完整的分布式服务治理能力。

但不是说 gRPC 无法实现服务发现、负载均衡等功能，它也具备相应机制或生态集成。

## 3. Thrift、XML-RPC、RMI

这几个有概念就可以，不需要在你现在的学习阶段深入源码。

|技术|了解什么|
|---|---|
|Thrift|类似 gRPC，支持 IDL、代码生成和多语言 RPC|
|XML-RPC|使用 XML 编码远程调用消息|
|Java RMI|Java 的远程方法调用机制，偏 Java 生态|
|SOAP|XML 消息协议，常与 Web Service 一起出现|

# 六、真正厉害的部分：RPC 的分布式难题

前面那些是框架知识。接下来这些，是面试官判断你有没有工程思维的地方。

## 1. RPC 请求超时了，服务端到底有没有执行？

这是非常经典的难题。

假设客户端调用支付服务：

```
paymentService.pay(orderId);
```

结果发生了：

```
客户端                    服务端
   |                         |
   | ------ 支付请求 ------>  |
   |                         | 支付成功
   |                         |
   |    X 响应在网络中丢失    |
   |                         |
   | ----- 客户端超时 -----   |
```

客户端观察到的是超时，但并不能证明服务端没有完成支付。

此时如果直接重试，就可能产生重复扣款。

怎么解决？

需要考虑幂等性（Idempotency）。

例如给每笔支付请求分配唯一业务请求 ID：

```
{
  "requestId": "pay-1001",
  "orderId": 1001,
  "amount": 100
}
```

服务端需要持久化记录该请求的处理结果，并通过数据库唯一约束、事务等机制避免重复执行业务操作。

客户端再次使用同一个 `requestId` 请求时，服务端可以识别这是重复操作，返回之前的结果或当前处理状态。

这就把 RPC 和你学过的幂等键、数据库唯一索引、事务联系起来了。

## 2. RPC 的超时和重试应该怎么设计？

假设微服务之间存在调用链：

```
浏览器 → 网关 → 订单服务 → 库存服务 → 数据库
```

如果订单服务没有限制库存服务的调用时间，而库存服务一直无响应，就可能导致线程或连接资源长期被占用。

因此需要设计：

- Timeout / Deadline：明确整个调用最多能等待多长时间。
    
- Retry：对符合条件的失败进行有限次数重试。
    
- Backoff + Jitter：退避与随机抖动，避免所有请求同时重试。
    
- Circuit Breaker：熔断，在依赖服务持续异常时减少无效请求。
    
- 限流与隔离：避免下游故障拖垮其他服务。
    
- Tracing：使用 Trace ID 追踪跨服务调用链。
    

这里最容易犯的错误是：认为所有超时都应该重试。

gRPC 有 `DEADLINE_EXCEEDED`、`UNAVAILABLE` 等状态码，但重试策略必须结合业务语义判断。gRPC 本身不会替你解决业务重复执行的问题。

![](https://www.google.com/s2/favicons?domain=https://grpc.io&sz=32)

gRPC

+1

## 3. RPC 如何找到目标服务？

这个问题叫服务发现（Service Discovery）。

假设用户服务部署了三个实例：

```
UserService
  ├── 10.0.0.1:8080
  ├── 10.0.0.2:8080
  └── 10.0.0.3:8080
```

订单服务不应该把某一台机器的地址永久写死。

典型解决方案：

1. 用户服务实例向注册中心注册，或由服务发现系统维护实例信息。
    
2. 订单服务根据服务名称获取可用实例列表。
    
3. 通过负载均衡算法选择某个实例。
    
4. 发生实例变化时更新服务发现结果。
    

常见服务发现方案包括 Nacos、Consul、Kubernetes Service 等。

还要分清：

- 注册中心：回答“有哪些实例可以访问”。
    
- 负载均衡：回答“这一次应该访问哪一个实例”。
    

服务发现与负载均衡可以通过框架、客户端库、网关或基础设施协作实现，并不是必须绑定某个独立注册中心。

# 七、面试高强度追问：12 道题

你可以把下面当成模拟面试卡片。先自己在心里回答，再展开标准回答。

模拟面试 · 逐题练习

1 / 12

## RPC 和 HTTP 有什么区别？

先自己组织 30～60 秒的回答，再查看参考答案。

上一题查看答案下一题


# 九、最后：给你一版可以直接用于面试的回答

面试官：你对 RPC 有什么了解？

> RPC 就是远程过程调用，它的核心思想是让开发者以类似本地方法调用的方式访问远程服务。
> 
> 从原理上讲，RPC 需要解决接口定义、代理调用、参数序列化、网络传输、服务端方法分发和响应反序列化等问题。
> 
> 比较常见的框架有 gRPC、Dubbo 和 tRPC。
> 
> gRPC 一般通过 Protobuf 定义服务契约，基于 HTTP/2 通信，支持跨语言调用和四种流式通信模式，适合微服务之间的通信。
> 
> Dubbo 在 Java 生态中比较常见，除 RPC 通信外，还提供服务发现、负载均衡等服务治理能力。
> 
> tRPC 则主要面向 TypeScript 全栈应用，通过共享 Router 类型实现端到端类型推导，减少前后端手动维护接口类型的工作。
> 
> 我认为 RPC 最重要的设计问题不只是调用性能，而是如何处理网络不可靠带来的超时、重试、幂等性、服务发现和故障隔离等问题。比如一次支付 RPC 超时，并不能证明服务端没有执行，因此不能简单重试，需要配合业务幂等机制保证不会重复扣款。
> 
> 在技术选型上，我会结合调用方环境、是否跨语言、性能要求和系统复杂度判断，而不是认为 RPC 一定比 REST 更好。

这段的层次是：定义 → 原理 → 框架区别 → 分布式难点 → 技术选型。 面试中能自然地讲到最后两部分，比单纯记忆几个协议名更有说服力。

## 建议你接下来重点练习的三个方面

1. 手写最简 RPC 原理：用 Node.js 实现一个方法名 + 参数 + HTTP 请求 + 服务端执行 + 返回结果的小系统。理解 Stub 到底隐藏了什么。
    
2. 实际跑一次 gRPC：编写 `.proto`，让一个 Java 服务提供接口，用另一个客户端调用，观察代码生成、Protobuf 和 HTTP/2 的作用。
    
3. 深入分布式故障题：重点练超时、幂等性、重试、熔断、服务发现。它们也是很多后端面试官继续追问的核心内容。
    

现在你可以直接进入更真实的模拟面试：

开始 RPC 压力面试 手写 Mini RPC，理解源码原理