# SSE💡
**S**erver-**S**ent **E**vents（服务器发送事件）

https://www.bilibili.com/video/BV15F7J6dEdm

浏览器发起一次 HTTP 请求，服务器在==同一个响应==中持续向浏览器推送事件，支持==自动断线重连==

比如 AI 聊天的流式输出，用户提交一句话后，服务端逐步生成文字，并持续发送给前端，不必等完整答案生成后才返回
![[Pasted image 20261011182723.png]]


---
## 流程
前端正常发送请求

服务器返回：
![[Pasted image 20261011183018.png]]

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
```

然后持续写入：
```
id: 1
event: message
data: 你好

id: 2
event: message
data: 我是 AI 助手

id: 3
event: done
data: [DONE]
```

这里的空行很关键，用于分隔事件

---
## 传输数据
SSE 事件有几个常见字段：

- data：事件的数据
- event：事件类型
- id：事件 ID，可用于断线恢复
- retry：建议浏览器重新连接的等待时间

![[Pasted image 20261011183101.png]]

原生浏览器 `EventSource` API 支持自动重连，也可以利用 `Last-Event-ID` 配合服务端进行事件续传，但服务端必须具备重放能力

---
## 传输结束
协议本身没有定义，可以自己实现：

- 断开连接
- 发送自定义的事件
- 发送自定义的消息
