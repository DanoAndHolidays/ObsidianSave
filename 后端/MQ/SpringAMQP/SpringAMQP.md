# SpringAMQP
> Last Format Time：10/10/2026 01:16:05

SpringAMQP 是基于 RabbitMQ 封装的一套模板，并且还利用 SpringBoot 对其实现了自动装配，使用起来非常方便。

[SpringAMQP官网](https://spring.io/projects/spring-amqp)

**A**dvanced **M**essage **Q**ueuing **P**rotocol 是用于在应用程序或之间传递业务消息的开放标准该协议与语言和平台无关，更符合微服务中独立性的要求

SpringAMQP提供了三个功能：

- 自动声明队列、交换机及其绑定关系
- 基于注解的监听器模式，异步接收消息
- 封装了 RabbitTemplate 工具，用于发送消息

---
## Basic Queue 简单队列模型
在父工程`mq-demo`中引入依赖：
```xml
<!--AMQP依赖，包含RabbitMQ-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

##### 消息发送
首先配置 MQ 地址，在 Publisher 服务的 application.yml 中添加配置：
```yaml
spring:
  rabbitmq:
    host: 192.168.150.101 # 主机名
    port: 5672 # 端口
    virtual-host: / # 虚拟主机
    username: itcast # 用户名
    password: 123321 # 密码
```

然后在 Publisher 服务中编写测试类 SpringAmqpTest，并利用 RabbitTemplate 实现消息发送：
```java
package cn.itcast.mq.spring;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest
public class SpringAmqpTest {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Test
    public void testSimpleQueue() {
        // 队列名称
        String queueName = "simple.queue";
        // 消息
        String message = "hello, spring amqp!";
        // 发送消息
        rabbitTemplate.convertAndSend(queueName, message);
    }
}
```

##### 消息接收
首先配置 MQ 地址，在 Consumer 服务的 application.yml 中添加配置：
```yaml
spring:
  rabbitmq:
    host: 192.168.150.101 # 主机名
    port: 5672 # 端口
    virtual-host: / # 虚拟主机
    username: itcast # 用户名
    password: 123321 # 密码
```

然后在 Consumer 服务的 `cn.itcast.mq.listener` 包中新建一个类 SpringRabbitListener，代码如下：
```java
package cn.itcast.mq.listener;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class SpringRabbitListener {

    @RabbitListener(queues = "simple.queue")
    public void listenSimpleQueueMessage(String msg) throws InterruptedException {
        System.out.println("spring 消费者接收到消息：【" + msg + "】");
    }
}
```

---
## Work Queue
Work Queues，也被称为（Task queues），任务模型。简单来说就是**让多个消费者绑定到一个队列，共同消费队列中的消息**。

当消息处理比较耗时的时候，可能生产消息的速度会远远大于消息的消费速度。长此以往，消息就会堆积越来越多，无法及时处理。

此时就可以使用 Work 模型，多个消费者共同处理消息，速度就能大大提高了。 

##### 消息发送
这次我们循环发送，模拟大量消息堆积现象。

在 Publisher 服务中的 SpringAmqpTest 类中添加一个测试方法：
```java
/**
     * workQueue
     * 向队列中不停发送消息，模拟消息堆积。
     */
@Test
public void testWorkQueue() throws InterruptedException {
    // 队列名称
    String queueName = "simple.queue";
    // 消息
    String message = "hello, message_";
    for (int i = 0; i < 50; i++) {
        // 发送消息
        rabbitTemplate.convertAndSend(queueName, message + i);
        Thread.sleep(20);
    }
}
```

##### 消息接收
要模拟多个消费者绑定同一个队列，我们在 Consumer 服务的 SpringRabbitListener 中添加2个新的方法：
```java
@RabbitListener(queues = "simple.queue")
public void listenWorkQueue1(String msg) throws InterruptedException {
    System.out.println("消费者1接收到消息：【" + msg + "】" + LocalTime.now());
    Thread.sleep(20);
}

@RabbitListener(queues = "simple.queue")
public void listenWorkQueue2(String msg) throws InterruptedException {
    System.err.println("消费者2........接收到消息：【" + msg + "】" + LocalTime.now());
    Thread.sleep(200);
}
```

但是这样是会有消息预取的问题，使得慢的 Consumer 拿到超过其能力的 Message

##### 能者多劳
在 Spring 中有一个简单的配置，可以解决这个问题。我们修改 Consumer 服务的application.yml文件，添加配置： 
```yaml
spring:
  rabbitmq:
    listener:
      simple:
        prefetch: 1 # 每次只能获取一条消息，处理完成才能获取下一个消息
```

##### 总结
Work 模型的使用：

- 多个消费者绑定到一个队列，同一条消息只会被一个消费者处理
- 通过设置 prefetch 来控制消费者预取的消息数量

### 发布/订阅
发布订阅的模型如图：

- 可以看到，在订阅模型中，多了一个 Exchange 角色，而且过程略有变化：
	
	- Publisher：生产者，也就是要发送消息的程序，但是不再发送到队列中，而是发给X（交换机）
	
	- Exchange：交换机，图中的X。一方面，接收生产者发送的消息。另一方面，知道如何处理消息，例如递交给某个特别队列、递交给所有队列、或是将消息丢弃。到底如何操作，取决于 Exchange 的类型。Exchange 有以下3种类型：
		
		- Fanout：广播，将消息交给所有绑定到交换机的队列
		
		- Direct：定向，把消息交给符合指定routing key 的队列
		
		- Topic：通配符，把消息交给符合routing pattern（路由模式） 的队列
	
	- Consumer：消费者，与以前一样，订阅队列，没有变化
	
	- Queue：消息队列也与以前一样，接收消息、缓存消息


Exchange（交换机）只负责转发消息，==不具备存储消息==的能力，因此如果没有任何队列与Exchange绑定，或者没有符合路由规则的队列，那么消息会丢失！

### Fanout
Fanout，英文翻译是扇出，我觉得在 MQ 中叫广播更合适。

在广播模式下，消息发送流程是这样的：

1. 可以有多个队列
2. 每个队列都要绑定到 Exchange（交换机）
3. 生产者发送的消息，只能发送到交换机，交换机来决定要发给哪个队列，生产者无法决定
4. 交换机把消息发送给绑定过的所有队列
5. 订阅队列的消费者都能拿到消息

##### 声明队列和交换机
Spring 提供了一个接口 Exchange，来表示所有不同类型的交换机：

在 Consumer 中创建一个类，声明队列和交换机：
```java
package cn.itcast.mq.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.FanoutExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FanoutConfig {
    /**
     * 声明交换机
     * @return Fanout类型交换机
     */
    @Bean
    public FanoutExchange fanoutExchange(){
        return new FanoutExchange("itcast.fanout");
    }

    /**
     * 第1个队列
     */
    @Bean
    public Queue fanoutQueue1(){
        return new Queue("fanout.queue1");
    }

    /**
     * 绑定队列和交换机
     */
    @Bean
    public Binding bindingQueue1(Queue fanoutQueue1, FanoutExchange fanoutExchange){
        return BindingBuilder.bind(fanoutQueue1).to(fanoutExchange);
    }

    /**
     * 第2个队列
     */
    @Bean
    public Queue fanoutQueue2(){
        return new Queue("fanout.queue2");
    }

    /**
     * 绑定队列和交换机
     */
    @Bean
    public Binding bindingQueue2(Queue fanoutQueue2, FanoutExchange fanoutExchange){
        return BindingBuilder.bind(fanoutQueue2).to(fanoutExchange);
    }
}
```

##### 消息发送
在 Publisher 服务的 SpringAmqpTest 类中添加测试方法：
```java
@Test
public void testFanoutExchange() {
    // 队列名称
    String exchangeName = "itcast.fanout";
    // 消息
    String message = "hello, everyone!";
    rabbitTemplate.convertAndSend(exchangeName, "", message);
}
```

##### 消息接收
在 Consumer 服务的 SpringRabbitListener 中添加两个方法，作为消费者：
```java
@RabbitListener(queues = "fanout.queue1")
public void listenFanoutQueue1(String msg) {
    System.out.println("消费者1接收到Fanout消息：【" + msg + "】");
}

@RabbitListener(queues = "fanout.queue2")
public void listenFanoutQueue2(String msg) {
    System.out.println("消费者2接收到Fanout消息：【" + msg + "】");
}
```

##### 总结
交换机的作用是什么？

- 接收 Publisher 发送的消息
- 将消息按照规则路由到与之绑定的队列
- 不能缓存消息，路由失败，消息丢失
- FanoutExchange 会将消息路由到每个绑定的队列

声明队列、交换机、绑定关系的Bean是什么？

- Queue
- FanoutExchange
- Binding

### Direct
在 Fanout 模式中，一条消息，会被所有订阅的队列都消费。但是，在某些场景下，我们希望不同的消息被不同的队列消费。这时就要用到 Direct 类型的 Exchange。

在 Direct 模型下：

- 队列与交换机的绑定，不能是任意绑定了，而是要指定一个 `RoutingKey`（路由key）
- 消息的发送方在向 Exchange 发送消息时，也必须指定消息的 `RoutingKey`。
- Exchange 不再把消息交给每一个绑定的队列，而是根据消息的 `Routing Key` 进行判断，只有队列的 `Routingkey` 与消息的 `Routing key` 完全一致，才会接收到消息

##### 基于注解声明队列和交换机
1. 利用 @RabbitListener 声明 Exchange、Queue、RoutingKey
2. 在 Consumer 服务中，编写两个消费者方法，分别监听 direct.queue1 和 direct.queue2
3. 在 Publisher 中编写测试方法，向 itcast.direct 发送消息 


基于@Bean的方式声明队列和交换机比较麻烦，Spring还提供了基于注解方式来声明。

在 Consumer 的 SpringRabbitListener 中添加两个消费者，同时基于注解来声明队列和交换机：
```java
@RabbitListener(bindings = @QueueBinding(
    value = @Queue(name = "direct.queue1"),
    exchange = @Exchange(name = "itcast.direct", type = ExchangeTypes.DIRECT),
    key = {"red", "blue"}
))
public void listenDirectQueue1(String msg){
    System.out.println("消费者接收到direct.queue1的消息：【" + msg + "】");
}

@RabbitListener(bindings = @QueueBinding(
    value = @Queue(name = "direct.queue2"),
    exchange = @Exchange(name = "itcast.direct", type = ExchangeTypes.DIRECT),
    key = {"red", "yellow"}
))
public void listenDirectQueue2(String msg){
    System.out.println("消费者接收到direct.queue2的消息：【" + msg + "】");
}
```

##### 消息发送
在publisher服务的SpringAmqpTest类中添加测试方法：
```java
@Test
public void testSendDirectExchange() {
    // 交换机名称
    String exchangeName = "itcast.direct";
    // 消息
    String message = "红色警报！日本乱排核废水，导致海洋生物变异，惊现哥斯拉！";
    // 发送消息
    rabbitTemplate.convertAndSend(exchangeName, "red", message);
}
```

##### 总结
描述下 Direct 交换机与 Fanout 交换机的差异？

- Fanout 交换机将消息路由给每一个与之绑定的队列
- Direct 交换机根据 RoutingKey 判断路由给哪个队列
- 如果多个队列具有相同的 RoutingKey，则与 Fanout 功能类似

基于 @RabbitListener 注解声明队列和交换机有哪些常见注解？

- @Queue
- @Exchange

### Topic
##### 说明
`Topic` 类型的 `Exchange` 与 `Direct` 相比，都是可以根据 `RoutingKey` 把消息路由到不同的队列。只不过 `Topic` 类型 `Exchange` 可以让队列在绑定 `Routing key` 的时候使用通配符！

`RoutingKey` 一般都是由一个或多个单词组成，多个单词之间以“.”分割，例如： `item.insert` 

通配符规则：

- `#`：匹配0个或多个词
- `*`：匹配不多不少恰好1个词

举例：

- `item.#`：能够匹配 `item.spu.insert` 或者 `item.spu`
- `item.*`：只能匹配 `item.spu`

解释：

- Queue1：绑定的是 `china.#` ，因此凡是以 `china.`开头的 `routing key` 都会被匹配到。包括china.news和china.weather

- Queue2：绑定的是 `#.news` ，因此凡是以 `.news` 结尾的 `routing key` 都会被匹配。包括china.news和japan.news

案例需求：

实现思路如下：

1. 利用 @RabbitListener 声明 Exchange、Queue、RoutingKey
2. 在 Consumer 服务中，编写两个消费者方法，分别监听 topic.queue1 和 topic.queue2
3. 在 Publisher 中编写测试方法，向 itcast.topic 发送消息

##### 消息发送
在 Publisher 服务的 SpringAmqpTest 类中添加测试方法：
```java
/**
     * topicExchange
     */
@Test
public void testSendTopicExchange() {
    // 交换机名称
    String exchangeName = "itcast.topic";
    // 消息
    String message = "喜报！孙悟空大战哥斯拉，胜!";
    // 发送消息
    rabbitTemplate.convertAndSend(exchangeName, "china.news", message);
}
```

##### 消息接收
在 Consumer 服务的 SpringRabbitListener 中添加方法：
```java
@RabbitListener(bindings = @QueueBinding(
    value = @Queue(name = "topic.queue1"),
    exchange = @Exchange(name = "itcast.topic", type = ExchangeTypes.TOPIC),
    key = "china.#"
))
public void listenTopicQueue1(String msg){
    System.out.println("消费者接收到topic.queue1的消息：【" + msg + "】");
}

@RabbitListener(bindings = @QueueBinding(
    value = @Queue(name = "topic.queue2"),
    exchange = @Exchange(name = "itcast.topic", type = ExchangeTypes.TOPIC),
    key = "#.news"
))
public void listenTopicQueue2(String msg){
    System.out.println("消费者接收到topic.queue2的消息：【" + msg + "】");
}
```

---
## 消息转换器
之前说过，Spring 会把你发送的消息==序列化为字节==发送给 MQ，接收消息的时候，还会把字节反序列化为 Java 对象

只不过，默认情况下 Spring 采用的序列化方式是 JDK 序列化。众所周知，JDK 序列化存在下列问题：

- 数据体积过大
- 有安全漏洞
- 可读性差

显然，JDK 序列化方式并不合适。我们希望消息体的体积更小、可读性更高，因此可以使用JSON 方式来做序列化和反序列化。

在 Publisher 和 Consumer 两个服务中都引入依赖：
```xml
<dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
    <version>2.9.10</version>
</dependency>
```

配置消息转换器。

在启动类中添加一个 Bean 即可：
```java
@Bean
public MessageConverter jsonMessageConverter(){
    return new Jackson2JsonMessageConverter();
}
```

*看到这里用的Jackson*
