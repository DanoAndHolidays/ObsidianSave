# TCP & UDP
> Last Format Time：10/6/2026 02:27:25

TCP 和 UDP 都属于==传输层协议==：
```text
应用层
HTTP / HTTPS / DNS / WebSocket ...

传输层
TCP / UDP

网络层
IP、路由器 Router

数据链路层
MAC、以太网、交换机 Switch

物理层
网线、光纤、无线电波、中继器、Hub
```

面试直接问TCP 和 UDP 有什么区别？推荐答：

|TCP|UDP|
|---|---|
|面向连接|无连接|
|可靠传输|尽力而为，不保证可靠|
|面向字节流|面向报文|
|保证顺序|不保证顺序|
|有重传机制|本身没有重传|
|有流量控制|没有|
|有拥塞控制|没有|
|首部至少 20 字节|首部 8 字节|
|开销较大|开销较小|
|适合可靠性优先|适合实时性/低延迟优先|
TCP 用更多机制换取可靠性，UDP 用更少机制换取低开销和低延迟

![[Pasted image 20260928163439.png]]
TCP 20字节，UDP 8字节


---
## TCP
### 三次握手
SYN（Synchronization）
ACK（Acknowledgment）


```text
Client                  Server

		    SYN
   ---------------------->

         SYN + ACK
   <----------------------

		    ACK
   ---------------------->

========= 连接建立 =========
```

##### 三次的原因
两次握手无法可靠确认客户端已经收到了服务端的响应：
```text
Client → SYN → Server
Client ← SYN+ACK ← Server
```

服务端收到 SYN 后就认为连接建立了，但实际上第二个包可能丢了：
```text
Server：
我已经建立连接了。

Client：
？？？我根本没收到。
```

还可能出现一个更经典的问题，旧 SYN 报文

假设客户端以前发了一个 SYN，因为网络堵塞，它一直没到，客户端超时之后重新建立连接并完成通信，很久以后，旧 SYN 突然到了服务器，如果只有两次握手：
```text
Server：
哦，有人要连接。
连接建立。
```

然后服务器白白维护一个不存在的连接。

三次握手最后客户端还需要确认：
```text
Client → ACK
```

服务端才能确认客户端确实收到了我的响应，这个连接是真实有效的

### 四次挥手
TCP 断开连接：
```text
Client                    Server

FIN
------------------------->

ACK
<-------------------------

FIN
<-------------------------

ACK
------------------------->
```


因为 TCP 是全双工通信，两个方向需要分别关闭。

例如 Client：
```text
我没数据发了。
```

Server 回复：
```text
知道了。
```

但是 Server 此时可能：
```text
还有数据没发完。
```

所以不能直接一起关闭。

等 Server 发完：
```text
FIN
```

Client：
```text
ACK
```

连接才真正结束。

##### 为什么三次握手，四次挥手？
经典面试题。一句话，建立连接时，Server 的 SYN 和 ACK 可以合并发送；关闭连接时，ACK 和 FIN 不一定能立即一起发送。

建立：
```text
SYN
↓
SYN + ACK
↓
ACK
```

所以三次。

关闭：
```text
FIN + ACK
↓
ACK

FIN + ACK
↓
ACK
```

因为对方收到 FIN 后，可能还有数据没有发送完。所以通常是四次。

##### TIME_WAIT
关闭连接之后，主动关闭的一方不会立即删除连接。

而是进入：
```text
TIME_WAIT
```

通常等待：
```text
2MSL
```

MSL（Maximum Segment Lifetime）报文在网络中的最大生存时间。

### TCP 连接唯一确定
IP 地址 + 端口号 = socket 套接字

```text
源 IP
源端口
目标 IP
目标端口
```

例如：
```text
10.0.0.1:50000
    ↓
8.8.8.8:443
```

### 可靠传输
##### 序列号 Sequence Number
TCP 会给数据编号，比如发送：
```text
数据：
ABCDEFGH
```

可以理解为：
```text
1 ABC
4 DEF
7 GH
```

TCP 就可以发现数据不完整，所以序列号解决的是数据顺序、重复数据、数据缺失的问题

你可以回答四个功能：
```text
保证顺序
发现丢包
去除重复数据
支持 ACK / 重传
```

其实 TCP 的可靠传输体系核心就是：

```text
Sequence Number
        +
ACK
        +
Retransmission
```

##### ACK 确认机制
接收方收到数据后会回复 ACK 累计确认

比如：
```text
Client                    Server

Seq=100, 100 bytes
------------------------->

               ACK=200
<-------------------------
```

这里 ACK = 200

并不是 “我收到了第 200 个字节”，而是 **0~199 之前的数据我都收到了，我下一步期待 200。**

##### 超时重传
如果 ACK 没有收到，就会超时重传：
```text
Sender
  |
  | Data
  |------------>
  | × ACK 丢失
  |
  | 等待 timeout
  |
  | Data again
  |------------>
```

##### 快速重传
![[Pasted image 20260928165220.png]]
TCP 不一定非要等超时，例如：
```text
发送：

1
2
3
4
5
```

结果：
```text
1 ✅
2 ✅
3 ❌
4 ✅
5 ✅
```

接收端会连续告诉发送端：
```text
ACK 3
ACK 3
ACK 3
```

意思是我一直在等 3。

如果发送方连续收到多个重复 ACK，通常会判断：
```text
3 丢了
```

于是直接重传，经典机制通常是：
```text
3 个重复 ACK
```

##### 滑动窗口
如果 TCP 每发送一个包都等 ACK：
```text
发 1
等 ACK

发 2
等 ACK

发 3
等 ACK
```

效率非常差，所以 TCP 使用 Sliding Window 可以连续发送多个数据：
```text
Sender

1 →
2 →
3 →
4 →
5 →

        ← ACK
        ← ACK
        ← ACK
```

不用每一个都停下来等。

假设：
```text
window = 4
```

表示：
```text
最多允许 4 份未确认数据同时在网络里。
```

例如：
```text
[1][2][3][4] 5 6 7 8
 ↑--------↑
   window
```

ACK 1 回来：
```text
1 [2][3][4][5] 6 7 8
     ↑--------↑
```

窗口向右移动。


##### 流量控制 Flow Control
假设：
```text
发送方：10Gbps
接收方：100Mbps
```

如果发送方疯狂发，接收方 buffer 很快就爆掉，所以 TCP 有流量控制

接收方会告诉发送方：
```text
我还有多少 buffer。
```

也就是：
```text
rwnd
Receiver Window
```

##### 拥塞控制 Congestion Control
还有一个问题即使接收方很强，网络本身可能扛不住。

例如很多机器同时发送：
```text
Server A ─┐
Server B ─┼── Router ──>
Server C ─┘
```

路由器队列满了：
```text
packet loss
```

所以 TCP 还有拥塞控制，发送端维护：
```text
cwnd
Congestion Window
```

##### rwnd 和 cwnd 的区别
这是非常不错的面试点。

```text
rwnd
Receiver Window

解决：
接收方处理不过来
```

```text
cwnd
Congestion Window

解决：
网络处理不过来
```

最终发送窗口大致受：
```text
min(rwnd, cwnd)
```

限制。

一句话记忆：
```text
rwnd 看接收方脸色
cwnd 看网络脸色
```

### TCP 拥塞控制经典四个机制
传统面试中经常问：
```text
慢启动
拥塞避免
快速重传
快速恢复
```

##### 慢启动
![[Pasted image 20260928165051.png]]

名字叫慢启动，但增长其实很快，开始：
```text
cwnd = 1
```

然后：
```text
1
2
4
8
16
...
```

指数增长。

不能一上来发送 10000 个包，因为不知道当前网络能承受多少流量，所以先试探。

##### 拥塞避免
到某个阈值：
```text
ssthresh 慢开始阈值
```

之后不再指数增长，而改成：
```text
线性增长
```

大概：
```text
16
17
18
19
20
```

目的是慢慢探测网络容量

### TCP 是字节流
这是非常容易被忽略，但非常重要的区别，TCP **不保留应用层消息边界**

假设你调用两次：
```text
send("hello");
send("world");
```

接收端可能读到：
```text
helloworld
```

也可能：
```text
hel
lowor
ld
```

因为 TCP 看的是：
```text
连续字节流
```

而不是：
```text
第一个消息
第二个消息
```

所以 TCP 会有一个著名的问题：
### 粘包 / 拆包
例如发送：
```text
hello
world
```

收到可能是：
```text
helloworld
```

或者：
```text
hel
lo
world
```

本质上TCP 根本不知道你的“消息边界”，所以应用层协议必须定义边界，常见方案：

固定长度

```text
每条消息固定 100 bytes
```

分隔符

```text
hello\n
world\n
```

长度字段

```text
[length][body]
```

例如：
```text
5hello
5world
```

HTTP 就是一种定义了完整消息格式的应用层协议。

### UDP 不会粘包
因为 UDP 面向报文 ，发送：
```text
send("hello")
send("world")
```

接收方看到的仍然是两个 Datagram：
```text
hello

world
```

不会变成：
```text
helloworld
```

所以：
```text
TCP：维护字节流

UDP：维护报文边界
```

这是非常重要的面试点。


---
## UDP
不需要三次握手
没有 ACK
没有重传
没有流量控制
没有拥塞控制
首部更小

所以他更快

```text
TCP / UDP
│
├── TCP
│   │
│   ├── 面向连接
│   │     └── 三次握手
│   │
│   ├── 可靠
│   │     ├── Sequence Number
│   │     ├── ACK
│   │     ├── 超时重传
│   │     └── 快速重传
│   │
│   ├── 高效
│   │     └── 滑动窗口
│   │
│   ├── 控制
│   │     ├── rwnd → 流量控制 → 接收方
│   │     └── cwnd → 拥塞控制 → 网络
│   │
│   ├── 字节流
│   │     └── 粘包 / 拆包
│   │
│   └── 关闭
│         ├── 四次挥手
│         ├── TIME_WAIT
│         └── CLOSE_WAIT
│
└── UDP
    │
    ├── 无连接
    ├── 不保证可靠
    ├── 不保证顺序
    ├── 面向报文
    ├── Header 8B
    ├── 延迟低 / 开销低
    │
    └── 上层可以自己实现可靠性
          └── QUIC
                └── HTTP/3
```