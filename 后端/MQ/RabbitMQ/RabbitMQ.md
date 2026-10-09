# RabbitMQ
> Last Format Time：10/9/2026 20:05:50

---
## 初识 MQ
### 同步通讯
我们之前学习的 Feign 调用就属于==同步方式==，调用可以实时得到结果

同步调用的优点：

- 时效性较强，可以立即得到结果

同步调用的问题：

- 耦合度高
- 性能和吞吐能力下降
- 有额外的资源消耗
- 有级联失败问题

*一般的项目中两个都有的，不会一棒子打死*

### 异步通讯
异步调用则可以避免上述问题，为了解除事件发布者与订阅者之间的耦合，两者并不是直接通信，而是有一个中间人（Broker）

发布者发布事件到 Broker，不关心谁来订阅事件，订阅者从 Broker 订阅事件，不关心谁发来的消息

![[Pasted image 20261009212737.png]]

Broker 是一个像数据总线一样的东西，所有的服务要接收数据和发送数据都发到这个总线上，这个总线就像协议一样，让服务间的通讯变得标准和可控。

- 好处：
	
	- 吞吐量提升：无需等待订阅者处理完成，响应更快速
	
	- 故障隔离：服务没有直接调用，不存在级联失败问题
	
	- 调用间没有阻塞，不会造成无效的资源占用
	
	- 耦合度极低，每个服务都可以灵活插拔，可替换
	
	- 流量削峰：不管发布事件的流量波动多大，都由 Broker 接收，订阅者可以按照自己的速度去处理事件


- 缺点：
	
	- 架构复杂了，业务没有明显的流程线，不好管理
	
	- 需要依赖于 Broker 的可靠、安全、性能


好在现在开源软件或云平台上 Broker 的软件是非常成熟的，比较常见的一种就是我们今天要学习的 MQ 技术。

### 技术对比
Message Queue，存放消息的队列，也就是事件驱动架构中的 Broker

几种常见 MQ 的实现的对比：

|       | **RabbitMQ**         | **Kafka**  | **RocketMQ** | **ActiveMQ**                  |
| ----- | -------------------- | ---------- | ------------ | ----------------------------- |
| 公司/社区 | Rabbit               | Apache     | 阿里           | Apache                        |
| 开发语言  | Erlang               | Scala&Java | Java         | Java                          |
| 协议支持  | AMQP，XMPP，SMTP，STOMP | 自定义协议      | 自定义协议        | OpenWire,STOMP，REST,XMPP,AMQP |
| 可用性   | 高                    | 高          | 高            | 一般                            |
| 单机吞吐量 | 一般                   | 非常高        | 高            | 差                             |
| 消息延迟  | 微秒级                  | 毫秒以内       | 毫秒级          | 毫秒级                           |
| 消息可靠性 | 高                    | 一般         | 高            | 一般                            |

---
## RabbitMQ
### 安装 RabbitMQ
安装 RabbitMQ，直接 Docker，记得安装带有 management tag 的

```sh
docker run -e RABBITMQ_DEFAULT_USER=itcast -e RABBITMQ_DEFAULT_PASS=123321 --name mq --hostname mq1 -p 15672:15672 -p 5672:5672 -d rabbitmq:management
```

登录：
![[Pasted image 20261009214929.png]]

MQ的基本结构：
![[Pasted image 20261009215423.png]]

RabbitMQ中的一些角色：

- Publisher：生产者
- Consumer：消费者
- Exchange：交换机，负责消息路由
- Queue：队列，存储消息
- VirtualHost：虚拟主机，隔离不同租户的 Exchange、Queue、消息

### RabbitMQ 消息模型
RabbitMQ 官方提供了 [5 个不同的 Demo 示例](https://www.rabbitmq.com/tutorials)，对应了不同的消息模型：
![[Pasted image 20261009221127.png]]

### 入门案例
*我们一般会这么去调用 MQ 的*推荐[[SpringAMQP]]
##### Publisher 实现
思路：

- 建立连接
- 创建Channel
- 声明队列
- 发送消息
- 关闭连接和channel

代码实现：
```java
package cn.itcast.mq.helloworld;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.junit.Test;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class PublisherTest {
    @Test
    public void testSendMessage() throws IOException, TimeoutException {
        // 1.建立连接
        ConnectionFactory factory = new ConnectionFactory();
        // 1.1.设置连接参数，分别是：主机名、端口号、vhost、用户名、密码
        factory.setHost("192.168.150.101");
        factory.setPort(5672);
        factory.setVirtualHost("/");
        factory.setUsername("itcast");
        factory.setPassword("123321");
        // 1.2.建立连接
        Connection connection = factory.newConnection();

        // 2.创建通道Channel
        Channel channel = connection.createChannel();

        // 3.创建队列
        String queueName = "simple.queue";
        channel.queueDeclare(queueName, false, false, false, null);

        // 4.发送消息
        String message = "hello, rabbitmq!";
        channel.basicPublish("", queueName, null, message.getBytes());
        System.out.println("发送消息成功：【" + message + "】");

        // 5.关闭通道和连接
        channel.close();
        connection.close();

    }
}
```

##### Consumer实现
代码思路：

- 建立连接
- 创建Channel
- 声明队列
- 订阅消息

代码实现：
```java
package cn.itcast.mq.helloworld;

import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class ConsumerTest {

    public static void main(String[] args) throws IOException, TimeoutException {
        // 1.建立连接
        ConnectionFactory factory = new ConnectionFactory();
        // 1.1.设置连接参数，分别是：主机名、端口号、vhost、用户名、密码
        factory.setHost("192.168.150.101");
        factory.setPort(5672);
        factory.setVirtualHost("/");
        factory.setUsername("itcast");
        factory.setPassword("123321");
        // 1.2.建立连接
        Connection connection = factory.newConnection();

        // 2.创建通道Channel
        Channel channel = connection.createChannel();

        // 3.创建队列
        String queueName = "simple.queue";
        channel.queueDeclare(queueName, false, false, false, null);

        // 4.订阅消息
        channel.basicConsume(queueName, true, new DefaultConsumer(channel){
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope,
                                       AMQP.BasicProperties properties, byte[] body) throws IOException {
                // 5.处理消息
                String message = new String(body);
                System.out.println("接收到消息：【" + message + "】");
            }
        });
        System.out.println("等待接收消息。。。。");
    }
}
```
