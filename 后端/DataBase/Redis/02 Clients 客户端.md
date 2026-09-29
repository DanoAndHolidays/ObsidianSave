# 02 Clients 客户端
> Last Format Time：9/30/2026 01:00:03

---
## Jedis
https://redis.github.io/jedis/

语法一致，简单易学，但是线程不安全

```java
@SpringBootTest
public class RedisTest {
    private Jedis jedis;

    @BeforeEach
    void setJedis() {
        jedis = new Jedis("127.0.0.1", 6379);
        jedis.select(0);
    }

    @Test
    void testString() {
        String result = jedis.set("name", "Dano");

        System.out.println("Result: " + result);

        String name = jedis.get("name");
        System.out.println("Name: " + name);
    }

    @Test
    void testHash() {
        jedis.hset("dano:v1", "name", "Dano");
        jedis.hset("dano:v1", "age", "22");

        Map<String, String> hget = jedis.hgetAll("dano:v1");
        System.out.println("Hash: " +  hget);
    }

    @AfterEach
    void tearDown() {
        // 不判断会有空指针风险
        if (jedis != null) jedis.close();
    }
}
```

要区分两个“安全”概念：

1. **Jedis 对象的线程安全**
    - 一个 `Jedis` 不要被多个线程同时用。
    - 多个线程分别使用不同的 `Jedis`，没问题。

2. **Redis 数据操作的并发安全**
    - 即使两个线程用了不同的 Jedis，也可能同时修改同一个 Redis key。
    - 这时候不会导致 Jedis 崩掉，但可能出现业务上的并发问题。

Jedis 的线程安全问题是客户端连接层面的，就是一个链接不要给多个线程去用

不同线程使用不同 Jedis 实例通常是安全的，但如果它们并发修改同一份 Redis 数据，仍然需要通过 Redis 原子命令、事务或 Lua 脚本保证业务层面的并发安全

使用 Jedis 线程池来代替直连的方式：
```java
public class JedisConnectionFactory {

    //虽然它是 final，但这里没有立刻赋值,只要保证它在静态初始化阶段只赋值一次
    private static final JedisPool jedisPool;

    // 在类第一次被加载时执行一次，用来初始化静态变量
    static {
        JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();

        jedisPoolConfig.setMaxTotal(8);
        jedisPoolConfig.setMaxIdle(8);
        jedisPoolConfig.setMinIdle(0);
        jedisPoolConfig.setMaxWaitMillis(1000);

        jedisPool = new JedisPool(jedisPoolConfig, "127.0.0.1", 6379);
    }

    public static Jedis getJedis(){
        return jedisPool.getResource();
    }
}
```

```java
...
@BeforeEach
void setJedis() {
    //jedis = new Jedis("127.0.0.1", 6379);
    jedis = JedisConnectionFactory.getJedis();
    jedis.select(0);
}
...
```

---
## SpringDataRedis
![[Pasted image 20260929000956.png]]

![[Pasted image 20260929001045.png]]

### 序列化
默认的序列化方式会导致一些问题：
![[Pasted image 20260929002903.png]]

![[Pasted image 20260929002951.png]]

![[Pasted image 20260929003210.png]]

我们可以手动序列化、反序列化：

![[Pasted image 20260929003432.png]]
