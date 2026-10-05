# 05 Lock 锁
> Last Format Time：10/6/2026 02:27:25

当用户抢购时，就会生成订单并保存到表中，而订单表如果使用数据库自增 ID 就存在一些问题：

* id的规律性太明显
* 受单表数据量的限制

如果我们的 id 具有太明显的规则，用户或者说商业对手很容易猜测出来我们的一些敏感信息，比如商城在一天时间内，卖出了多少单，这明显不合适

随着商城规模越来越大，mysql 的单表的容量不宜超过500W，数据量过大之后，我们要进行拆库拆表，但拆分表了之后，他们从逻辑上讲他们是同一张表，所以他们的id是不能一样的，于是乎我们需要保证id的唯一性

==全局ID生成器==，是一种在分布式系统下用来生成全局唯一ID的工具

![[Pasted image 20260930223140.png]]

ID的组成部分：符号位：1bit，永远为0，证书
时间戳：31bit，以秒为单位，可以使用69年
序列号：32bit，秒内的计数器，理论上支持每秒产生2^32个不同ID

我们也可以使用 UUID、snowflake

```java
@Component  
public class RedisIdWorker {  
    /**  
     * 开始时间戳  
     */  
    private static final long BEGIN_TIMESTAMP = 1640995200L;  
    /**  
     * 序列号的位数  
     */  
    private static final int COUNT_BITS = 32;  
  
    private final StringRedisTemplate stringRedisTemplate;  
  
    public RedisIdWorker(StringRedisTemplate stringRedisTemplate) {  
        this.stringRedisTemplate = stringRedisTemplate;  
    }  
  
    public long nextId(String prefix){  
        long nowSecond = LocalDateTime
	        .now()
	        .toEpochSecond(ZoneOffset.UTC);  
  
        long timestamp = nowSecond - BEGIN_TIMESTAMP;  
        String day  = LocalDateTime
	        .now()
	        .format(DateTimeFormatter.ofPattern("yyyyMMdd"));  
  
        // 这里不可能有空指针异常，以为如果这个 key下没有值，Redis 会自己建一个，报错不去管它  
        long countOfOneDay = stringRedisTemplate
	        .opsForValue()
	        .increment("icr:" + prefix + day);  
  
        return timestamp << COUNT_BITS | countOfOneDay;  
    }  
}
```


![[Pasted image 20260930232220.png]]

这里的实现有超卖的情况

```java
@Service  
public class VoucherOrderServiceImpl extends ServiceImpl<VoucherOrderMapper, VoucherOrder> implements IVoucherOrderService {  
    @Autowired  
    private SeckillVoucherServiceImpl seckillVoucherService;  
    @Autowired  
    private RedisIdWorker redisIdWorker;  
  
    @Transactional  
    public Result seckillVoucher(Long voucherId) {  
  
        SeckillVoucher voucher = seckillVoucherService.getById(voucherId);  
  
        if (voucher.getBeginTime().isAfter(LocalDateTime.now())) return Result.fail("秒杀未开始");  
        if (voucher.getEndTime().isBefore(LocalDateTime.now())) return Result.fail("秒杀已结束");  
  
        // 符合时间要求， 看看库存数量呢  
  
```

有关超卖问题

```java
        if (voucher.getStock() < 1) Result.fail("券的数量不够了");  
  
        //5，扣减库存  
        boolean success = seckillVoucherService.update()  
                .setSql("stock= stock -1")  
                .eq("voucher_id", voucherId).update();  
        if (!success) {  
            //扣减库存  
            return Result.fail("库存不足！");  
        }  
        //6.创建订单  
        VoucherOrder voucherOrder = new VoucherOrder();  
        // 6.1.订单id  
        long orderId = redisIdWorker.nextId("order");  
        voucherOrder.setId(orderId);  
        // 6.2.用户id  
        Long userId = UserHolder.getUser().getId();  
        voucherOrder.setUserId(userId);  
        // 6.3.代金券id  
        voucherOrder.setVoucherId(voucherId);  
        save(voucherOrder);  
  
        return Result.ok(orderId);  
    }  
}
```

假设线程1过来查询库存，判断出来库存大于1，正准备去扣减库存，但是还没有来得及去扣减
此时线程2过来，线程2也去查询库存，发现这个数量一定也大于1
那么这两个线程都会去扣减库存，最终多个线程相当于一起去扣减库存，此时就会出现库存的超卖问题

本质是这部分的操作是有状态的，不能重复的执行

---
## 乐观锁
乐观锁：会有一个==版本号==，每次操作数据会对版本号 +1，再提交回数据时，会去校验是否比之前的版本大1 ，如果大1 ，则进行操作成功，这套机制的核心逻辑在于，如果在操作过程中，版本号只比原来大1 ，那么就意味着操作过程中没有人对他进行过修改，他的操作就是安全的，如果不大1，则数据被修改过，当然乐观锁还有一些变种的处理方式比如 ==CAS（Compare And Set / Swap）== [[09 乐观锁]]

![[Pasted image 20261001001256.png]]

![[Pasted image 20261001001608.png]]

```java
boolean success = seckillVoucherService.update()
    .setSql("stock= stock -1") //set stock = stock -1
    .eq("voucher_id", voucherId)
    .eq("stock",voucher.getStock()).update(); 
    //where id = ？ and stock = ?
```

在使用乐观锁过程中假设100个线程同时都拿到了100的库存，然后大家一起去进行扣减，但是100个人中只有1个人能扣减成功，其他的人在处理时，他们在扣减时，库存已经被修改过了，所以此时其他99个线程都会失败

```java
boolean success = seckillVoucherService.update()
    .setSql("stock= stock -1")
    .eq("voucher_id", voucherId)
    .gt("stock",0) //where id = ? and stock > 0
    .update();
```

在高并发的情况下，如果有多个线程同时通过了 stock > 0 的限制条件判断，之后在进行减库存操作时会不会有竞态问题呢

只要你最终执行的是类似下面这一条 SQL：
```sql
UPDATE seckill_voucher
SET stock = stock - 1
WHERE voucher_id = ?
AND stock > 0;
```

那么在数据库层面，**“判断 `stock > 0` + `stock - 1`”属于同一条原子 UPDATE 操作**，不会出现你想象中的“多个线程都先判断通过，然后一起减成负数”的问题。

但这本身其实将锁转移到了数据库，数据库会成为性能的瓶颈，本质上并发冲突并没有消失

使用：
```text
UPDATE stock = stock - 1
WHERE stock > 0
```

并不是消除了锁，而是把并发一致性控制交给了数据库。

对于同一个秒杀商品：
```text
大量请求
   ↓
修改同一个 voucher_id
   ↓
竞争数据库中的同一行
```

数据库通过行锁等并发控制机制保证正确性，因此从这一行的角度看，大量修改操作实际上会被串行化。

这种问题叫**热点行竞争（Hot Row Contention）**

### 数据库可能成为秒杀系统的性能瓶颈
例如：
```text
库存：100

请求：100000
```

如果所有请求都直接访问 MySQL：
```text
100000 请求
      ↓
    MySQL
      ↓
UPDATE stock
```

最终：
```text
100 个成功
99900 个失败
```

但是数据库仍然处理了大量无意义的请求，同时还存在：
```text
数据库连接池压力
网络 IO
SQL 执行
事务开销
行锁竞争
undo log
redo log
binlog
commit
```

因此数据库虽然保证了正确性，却可能成为高并发秒杀场景下的瓶颈

### Redis 前置库存判断
*这里又要去学 MQ 了*
高并发系统通常把库存判断前移到 Redis：
```text
请求
 ↓
Redis
 ↓
判断库存
 ↓
扣 Redis 库存
 ↓
抢购成功
 ↓
MQ
 ↓
后台消费者
 ↓
MySQL 创建订单 / 扣库存
```

这样可以避免所有请求直接访问数据库，例如：
```text
10 万个请求
     ↓
   Redis
     ↓
只有 100 个成功请求
     ↓
     MQ
     ↓
   MySQL
```

数据库最终只需要处理真正抢购成功的请求

---
## 悲观锁
悲观锁可以实现对于数据的串行化执行，比如syn，和lock都是悲观锁的代表，同时，悲观锁中又可以再细分为公平锁，非公平锁，可重入锁，等等

### 一人一单
 现在的问题还是和之前一样，并发过来，查询数据库，都不存在订单，所以我们还是需要加锁，但是乐观锁比较适合更新数据，而现在是插入数据，所以我们需要使用悲观锁操作

```java

@Override
public Result seckillVoucher(Long voucherId) {
    // 1.查询优惠券
    SeckillVoucher voucher = seckillVoucherService.getById(voucherId);
    // 2.判断秒杀是否开始
    if (voucher.getBeginTime().isAfter(LocalDateTime.now())) {
        // 尚未开始
        return Result.fail("秒杀尚未开始！");
    }
    // 3.判断秒杀是否已经结束
    if (voucher.getEndTime().isBefore(LocalDateTime.now())) {
        // 尚未开始
        return Result.fail("秒杀已经结束！");
    }
    // 4.判断库存是否充足
    if (voucher.getStock() < 1) {
        // 库存不足
        return Result.fail("库存不足！");
    }
    // 5.一人一单逻辑
    // 5.1.用户id
    Long userId = UserHolder.getUser().getId();
    int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
    // 5.2.判断是否存在
    if (count > 0) {
        // 用户已经购买过了
        return Result.fail("用户已经购买过一次！");
    }

    //6，扣减库存
    boolean success = seckillVoucherService.update()
            .setSql("stock= stock -1")
            .eq("voucher_id", voucherId).update();
    if (!success) {
        //扣减库存
        return Result.fail("库存不足！");
    }
    //7.创建订单
    VoucherOrder voucherOrder = new VoucherOrder();
    // 7.1.订单id
    long orderId = redisIdWorker.nextId("order");
    voucherOrder.setId(orderId);

    voucherOrder.setUserId(userId);
    // 7.3.代金券id
    voucherOrder.setVoucherId(voucherId);
    save(voucherOrder);

    return Result.ok(orderId);

}
```

这里都要上锁：
```java
    // 5.一人一单逻辑
    // 5.1.用户id
    Long userId = UserHolder.getUser().getId();
    int count = query()
	    .eq("user_id", userId)
	    .eq("voucher_id", voucherId).count();
    // 5.2.判断是否存在
    if (count > 0) {
        // 用户已经购买过了
        return Result.fail("用户已经购买过一次！");
    }

    //6，扣减库存
    boolean success = seckillVoucherService.update()
            .setSql("stock= stock -1")
            .eq("voucher_id", voucherId).update();
    if (!success) {
        //扣减库存
        return Result.fail("库存不足！");
    }
    //7.创建订单
    VoucherOrder voucherOrder = new VoucherOrder();
    // 7.1.订单id
    long orderId = redisIdWorker.nextId("order");
    voucherOrder.setId(orderId);

    voucherOrder.setUserId(userId);
    // 7.3.代金券id
    voucherOrder.setVoucherId(voucherId);
    save(voucherOrder);
```

这里不给整个方法加锁，而是给 userId 加锁：
```java
@Transactional
public  Result createVoucherOrder(Long voucherId) {
	Long userId = UserHolder.getUser().getId();
	synchronized(userId.toString().intern()){
         // 5.1.查询订单
        int count = query()
	        .eq("user_id", userId)
	        .eq("voucher_id", voucherId).count();
        // 5.2.判断是否存在
        if (count > 0) {
            // 用户已经购买过了
            return Result.fail("用户已经购买过一次！");
        }

        // 6.扣减库存
        boolean success = seckillVoucherService.update()
                .setSql("stock = stock - 1") // set stock = stock - 1
                .eq("voucher_id", voucherId).gt("stock", 0) 
                // where id = ? and stock > 0
                .update();
        if (!success) {
            // 扣减失败
            return Result.fail("库存不足！");
        }

        // 7.创建订单
        VoucherOrder voucherOrder = new VoucherOrder();
        // 7.1.订单id
        long orderId = redisIdWorker.nextId("order");
        voucherOrder.setId(orderId);
        // 7.2.用户id
        voucherOrder.setUserId(userId);
        // 7.3.代金券id
        voucherOrder.setVoucherId(voucherId);
        save(voucherOrder);

        // 7.返回订单id
        return Result.ok(orderId);
    }
}
```

##### 细节问题
但是以上代码还是存在问题，问题的原因在于当前方法被spring的事务控制，如果你在方法内部加锁，可能会导致当前方法事务还没有提交，但是锁已经释放也会导致问题

实际上执行顺序类似：
```bash
开启事务

进入方法

获取synchronized锁

执行SQL

释放锁

# 这里可能被其他线程插入

提交事务
```

也就是在一个事务的过程中，最好是锁包事务，而不是事务包锁

但是以上做法依然有问题，因为你调用的方法，其实是this.的方式调用的，事务想要生效，还得利用代理来生效，所以这个地方，我们需要获得原始的事务对象，来操作事务

添加配置：
![[Pasted image 20261001155846.png]]

AOP 失效

```java
@Service  
@Slf4j  
public class VoucherOrderServiceImpl extends ServiceImpl<VoucherOrderMapper, VoucherOrder> implements IVoucherOrderService {  
    @Autowired  
    private SeckillVoucherServiceImpl seckillVoucherService;  
    @Autowired  
    private RedisIdWorker redisIdWorker;  
  
    @Transactional  
    public Result seckillVoucher(Long voucherId) {  
  
        SeckillVoucher voucher = seckillVoucherService.getById(voucherId);  
  
        if (voucher.getBeginTime().isAfter(LocalDateTime.now())) return Result.fail("秒杀未开始");  
        if (voucher.getEndTime().isBefore(LocalDateTime.now())) return Result.fail("秒杀已结束");  
  
        // 符合时间要求， 看看库存数量呢  
  
        //  
        if (voucher.getStock() < 1) {  
            log.warn("券的数量不够了");  
            return Result.fail("券的数量不够了");  
        }  
  
```

因为 `@Transactional` 并不是 Java 自己看到注解就自动开启事务，而是 Spring AOP 在外面套了一层代理，Spring AOP 自调用（self-invocation）导致事务注解失效

```java
        // 不这样写，事务会失效，直接 this. 时使用的是目标对象，而不是Spring的代理对象  
        Long userId = UserHolder.getUser().getId();  
        synchronized (userId.toString().intern()) {  
            IVoucherOrderService proxy = 
	            (IVoucherOrderService) AopContext.currentProxy();  
            return proxy.createVoucherOrder(voucherId);  
        }  
  
    }  
    
    @Transactional  
    public Result createVoucherOrder(Long voucherId) {  
        Long userId = UserHolder.getUser().getId();  
  
        // 5.1.查询订单  
        int count = query()  
                .eq("user_id", userId)  
                .eq("voucher_id", voucherId).count();  
        // 5.2.判断是否存在  
        if (count > 0) {  
            // 用户已经购买过了  
            return Result.fail("用户已经购买过一次！");  
        }  
  
        // 6.扣减库存  
        boolean success = seckillVoucherService.update()  
                .setSql("stock = stock - 1") // set stock = stock - 1  
                .eq("voucher_id", voucherId).gt("stock", 0)  
                // where id = ? and stock > 0  
                .update();  
        if (!success) {  
            // 扣减失败  
            return Result.fail("库存不足！");  
        }  
  
        // 7.创建订单  
        VoucherOrder voucherOrder = new VoucherOrder();  
        // 7.1.订单id  
        long orderId = redisIdWorker.nextId("order");  
        voucherOrder.setId(orderId);  
        // 7.2.用户id  
        voucherOrder.setUserId(userId);  
        // 7.3.代金券id  
        voucherOrder.setVoucherId(voucherId);  
        save(voucherOrder);  
  
        // 7.返回订单id  
        return Result.ok(orderId);  
  
    }  
}
```

---
## 分布式锁
![[Pasted image 20261001162245.png]]

我们利用 JVM 的锁监视器来实现，JVM是不共享的，这里就锁不住了：
```java
Long userId = UserHolder.getUser().getId();  
synchronized (userId.toString().intern()) {  
    IVoucherOrderService proxy = (IVoucherOrderService)AopContext.currentProxy();  
    return proxy.createVoucherOrder(voucherId);  
}  
```

![[Pasted image 20261001164110.png]]

### 实现方式
 ![[Pasted image 20261001165400.png]]
![[Pasted image 20261001173804.png]]

##### 简单实现
```java
public class SimpleRedisLock implements DanoLock{  
  
    private static final String prefix = "lock:";  
    private final StringRedisTemplate stringRedisTemplate;  
    private final String key;  
  
    public SimpleRedisLock(StringRedisTemplate stringRedisTemplate, String key) {  
        this.stringRedisTemplate = stringRedisTemplate;  
        this.key = key;  
    }  
  
    @Override  
    public boolean tryLock(long timeoutSec) {  
        Long threadName = Thread.currentThread().getId();  
        Boolean success = stringRedisTemplate
	        .opsForValue()
```

使用 `SET key value EX time NX ` 实现一个原子命令，设置过期时间，防止因为 Tomcat 宕机导致无法释放：
```java
	        .setIfAbsent(prefix + key, threadName + "", timeoutSec, TimeUnit.SECONDS);  
```

自动拆箱可能会有 null，避免空指针异常：
```java
        // 自动拆箱可能会有 null，避免空指针异常  
        return  Boolean.TRUE.equals(success);  
    }  
  
    @Override  
    public void unlock() {  
        stringRedisTemplate.delete(prefix + key);  
    }  
}
```

##### 使用
使用时要注意：
```java
@Transactional  
public Result seckillVoucher(Long voucherId) {  
  
    SeckillVoucher voucher = seckillVoucherService.getById(voucherId);  
  
    if (voucher.getBeginTime().isAfter(LocalDateTime.now())) return Result.fail("秒杀未开始");  
    if (voucher.getEndTime().isBefore(LocalDateTime.now())) return Result.fail("秒杀已结束");  
  
    if (voucher.getStock() < 1) {  
        log.warn("券的数量不够了");  
        return Result.fail("券的数量不够了");  
    }  
  
    // 直接这样写，事务会失效，是因为这里使用的是目标对象，而不是Spring的代理对象  
    Long userId = UserHolder.getUser().getId();  
  
    SimpleRedisLock simpleRedisLock = new SimpleRedisLock(stringRedisTemplate, userId + "");  
    boolean isLock = simpleRedisLock.tryLock(1200);  
  
    if (!isLock) {  
        return Result.fail("已领券");  
    }  
```

保证释放锁在有异常时，也能执行：
```java
    try {  
        IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();  
        return proxy.createVoucherOrder(voucherId);  
    } finally {  
        simpleRedisLock.unlock();  
    }  
}
```

但是在极端情况下，会有误删问题，线程因为阻塞导致锁自动释放了，此时若有其他线程来得到锁，线程1会释放线程2的锁，此时没有锁，线程3就可以获取锁...这样下去无限的：
![[Pasted image 20261001191452.png]]

所以在释放锁的时候，要去看看锁的标识是否是自己的锁：
![[Pasted image 20261001191843.png]]

```java
@Slf4j  
public class SimpleRedisLock implements DanoLock {  
  
    private static final String prefix = "lock:";  
    private final StringRedisTemplate stringRedisTemplate;  
    private final String key;  
    private final String uuid;  
  
  
    public SimpleRedisLock(StringRedisTemplate stringRedisTemplate, String key) {  
        this.stringRedisTemplate = stringRedisTemplate;  
        this.key = key;  
        this.uuid = UUID.randomUUID().toString(true);  
    }  
  
    @Override  
    public boolean tryLock(long timeoutSec) {  
```

在 JVM 中的 Thread ID 是会自增的，不同的 JVM 的 Thread ID 可能会重复，这里加上 UUID，确保唯一性：
```java
        String threadName = uuid + "-" + Thread.currentThread().getId();  
        Boolean success = stringRedisTemplate.opsForValue().setIfAbsent(prefix + key, threadName, timeoutSec, TimeUnit.SECONDS);  
  
        // 自动拆箱可能会有 null，避免空指针异常  
        return Boolean.TRUE.equals(success);  
    }  
  
    @Override  
    public void unlock() {  
        String threadName = uuid + "-" + Thread.currentThread().getId();  
        String lockedName = stringRedisTemplate.opsForValue().get(prefix + key);  
```

只有是自己建的锁，才会去删除：
```java
        if (threadName.equals(lockedName)) {  
            stringRedisTemplate.delete(prefix + key);  
            log.info("是当前线程创建的锁");  
        } else {  
            log.info("锁已自动过期");  
        }  
    }}
```

```shell
2026-10-01 19:39:44.240  INFO 40716 --- [nio-8081-exec-1] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2026-10-01 19:39:44.371  INFO 40716 --- [nio-8081-exec-1] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2026-10-01 19:39:44.400 DEBUG 40716 --- [nio-8081-exec-1] c.h.m.SeckillVoucherMapper.selectById    : ==>  Preparing: SELECT voucher_id,stock,create_time,begin_time,end_time,update_time FROM tb_seckill_voucher WHERE voucher_id=?
2026-10-01 19:39:44.417 DEBUG 40716 --- [nio-8081-exec-1] c.h.m.SeckillVoucherMapper.selectById    : ==> Parameters: 11(Long)
2026-10-01 19:39:44.433 DEBUG 40716 --- [nio-8081-exec-1] c.h.m.SeckillVoucherMapper.selectById    : <==      Total: 1
2026-10-01 19:39:44.484 DEBUG 40716 --- [nio-8081-exec-1] c.h.m.VoucherOrderMapper.selectCount     : ==>  Preparing: SELECT COUNT( * ) FROM tb_voucher_order WHERE (user_id = ? AND voucher_id = ?)
2026-10-01 19:39:44.484 DEBUG 40716 --- [nio-8081-exec-1] c.h.m.VoucherOrderMapper.selectCount     : ==> Parameters: 1010(Long), 11(Long)
2026-10-01 19:39:44.487 DEBUG 40716 --- [nio-8081-exec-1] c.h.m.VoucherOrderMapper.selectCount     : <==      Total: 1
2026-10-01 19:40:42.496  INFO 40716 --- [nio-8081-exec-1] com.hmdp.utils.SimpleRedisLock           : 锁已自动过期
```

但是依旧有问题，判断所标识和释放锁是两个动作，中间如果被阻塞，依旧会会回归旧的问题：
![[Pasted image 20261001194554.png]]
##### Lua
Redis 中的事务保证不了原子性，使用 Lua 保证原子性：
![[Pasted image 20261001195532.png]]

![[Pasted image 20261001195825.png]]

最终我们操作redis的拿锁比锁删锁的lua脚本就会变成这样

```lua
-- 这里的 KEYS[1] 就是锁的key，这里的ARGV[1] 就是当前线程标示
-- 获取锁中的标示，判断是否与当前线程标示一致
if (redis.call('GET', KEYS[1]) == ARGV[1]) then
  -- 一致，则删除锁
  return redis.call('DEL', KEYS[1])
end
-- 不一致，则直接返回
return 0
```

```java
@Slf4j  
public class SimpleRedisLock implements DanoLock {  
  
    private static final String prefix = "lock:";  
    private final StringRedisTemplate stringRedisTemplate;  
    private final String key;  
    private final String uuid;  
```

在类初始化的时候去加载脚本：
```java
    private static final DefaultRedisScript<Long> UNLOCK_SCRIPT;  
    static {  
        UNLOCK_SCRIPT = new DefaultRedisScript<>();  
        UNLOCK_SCRIPT.setLocation(new ClassPathResource("unlock.lua"));  
        UNLOCK_SCRIPT.setResultType(Long.class);  
    }  
  
    public SimpleRedisLock(StringRedisTemplate stringRedisTemplate, String key) {  
        this.stringRedisTemplate = stringRedisTemplate;  
        this.key = key;  
        this.uuid = UUID.randomUUID().toString(true);  
    }  
  
    @Override  
    public boolean tryLock(long timeoutSec) {  
        String threadName = uuid + "-" + Thread.currentThread().getId();  
        Boolean success = stringRedisTemplate.opsForValue().setIfAbsent(prefix + key, threadName, timeoutSec, TimeUnit.SECONDS);  
  
        // 自动拆箱可能会有 null，避免空指针异常  
        return Boolean.TRUE.equals(success);  
    }  
  
    @Override  
    public void unlock() {  
```

执行 Lua 脚本：
```java
        Long execute = stringRedisTemplate.execute(  
                UNLOCK_SCRIPT,  
                Collections.singletonList(prefix + key),  
                uuid + "-" + Thread.currentThread().getId()  
        );  
        if(execute == 0L){  
            log.info("锁已自动过期");  
        }else {  
            log.info("是当前线程创建的锁");  
        }  
    }}
```

这里线程1超时，那么线程1和2的业务同时执行，会出现线程安全问题：

### Redisson
配置：
```java
@Configuration  
public class RedissonConfig {  
  
    /**  
     * 复用 spring.redis 下的连接配置，避免 Redisson 与 StringRedisTemplate  
     * 分别维护两套 Redis 地址。  
     */  
    @Bean(destroyMethod = "shutdown")  
    public RedissonClient redissonClient(RedisProperties redisProperties) {  
        Config config = new Config();  
        SingleServerConfig singleServerConfig = config.useSingleServer()  
                .setAddress("redis://" + redisProperties.getHost() + ":" + redisProperties.getPort())  
                .setDatabase(redisProperties.getDatabase());  
  
        if (StringUtils.hasText(redisProperties.getPassword())) {  
            singleServerConfig.setPassword(redisProperties.getPassword());  
        }  
  
        return Redisson.create(config);  
    }  
}
```

之后正常使用即可：
```java
@Transactional  
public Result seckillVoucher(Long voucherId) {  
  
    SeckillVoucher voucher = seckillVoucherService.getById(voucherId);  
  
    if (voucher.getBeginTime().isAfter(LocalDateTime.now())) return Result.fail("秒杀未开始");  
    if (voucher.getEndTime().isBefore(LocalDateTime.now())) return Result.fail("秒杀已结束");  
  
    if (voucher.getStock() < 1) {  
        log.warn("券的数量不够了");  
        return Result.fail("券的数量不够了");  
    }  
  
    // 直接这样写，事务会失效，是因为这里使用的是目标对象，而不是Spring的代理对象  
    Long userId = UserHolder.getUser().getId();  
```

其实就是换了个锁对象：
```java
    RLock lock = redissonClient.getLock("lock:order:" + userId);  
    // 不指定租约时间，Redisson 看门狗会在业务未执行完时自动续期  
    boolean isLock = lock.tryLock();  
  
    if (!isLock) {  
        return Result.fail("已领券");  
    }  
  
    try {  
        IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();  
        return proxy.createVoucherOrder(voucherId);  
    } finally {  
        // 只释放当前线程持有的锁，避免业务异常时误解锁  
        if (lock.isHeldByCurrentThread()) {  
            lock.unlock();  
        }  
    }}
```

##### 可重入锁
[[08 ReentrantLock]]
使用 `SETNX` 设置的锁是没有办法重入（同一个线程重复的获取锁）

可以在获取锁的时候要去判断最开始的时候获取锁的线程是不是当前的线程，每次重入的时候记录从入的次数，删除的时候将重入次数 -1，为0的时候直接删掉

![[Pasted image 20261001212442.png]]

##### 可重试锁
##### 主从一致性
为了提高redis的可用性，我们会搭建集群或者主从，现在以主从为例

此时我们去写命令，写在主机上，主机会将数据同步给从机，但是假设在主机还没有来得及把数据写入到从机去的时候，此时主机宕机，哨兵会发现主机宕机，并且选举一个slave变成master，而此时新的master中实际上并没有锁信息，此时锁信息就已经丢掉了

![[Pasted image 20261002001753.png]]

![[Pasted image 20261002001816.png]]

我们使用多个主节点，每次获取锁都要在所有的主节点中得到锁：MultiLock 链锁
![[Pasted image 20261002002052.png]]

---
## 异步落库
[[06 MQ 消息队列]]
其实可以用 MQ 实现
![[Pasted image 20261002004012.png]]


![[Pasted image 20261002004639.png]]


```lua
---  
--- Generated by EmmyLua(https://github.com/EmmyLua)  
--- Created by 33536.  
--- DateTime: 2026/10/2 00:53  
---  
  
-- 1.参数列表  
-- 1.1.优惠券id  
local voucherId = ARGV[1]  
-- 1.2.用户id  
local userId = ARGV[2]  
-- 1.3.订单id  
local orderId = ARGV[3]  
  
-- 2.数据key  
-- 2.1.库存key  
local stockKey = 'seckill:stock:' .. voucherId  
-- 2.2.订单key  
local orderKey = 'seckill:order:' .. voucherId  
  
-- 3.脚本业务  
-- 3.1.判断库存是否充足 get stockKey
local stock = tonumber(redis.call('get', stockKey))  
  
if not stock or stock <= 0 then  
    return 1  
end  
  
-- 3.2.判断用户是否下单 SISMEMBER orderKey userId
if(redis.call('sismember', orderKey, userId) == 1) then  
-- 3.3.存在，说明是重复下单，返回2  
    return 2  
end  
-- 3.4.扣库存 incrby stockKey -1
redis.call('incrby', stockKey, -1)  
-- 3.5.下单（保存用户）sadd orderKey userId  
redis.call('sadd', orderKey, userId)  
-- 3.6.发送消息到队列中， XADD stream.orders * k1 v1 k2 v2 ...
redis.call('xadd', 'stream.orders', '*', 'userId', userId, 'voucherId', voucherId, 'id', orderId)  
return 0
```

```java
private BlockingQueue<VoucherOrder> orderBlockingQueue = 
	new ArrayBlockingQueue<>(1024 * 1024);

@Transactional  
public Result seckillVoucher(Long voucherId) {  
    Long userId = UserHolder.getUser().getId();  
```

因为redis是单线程，并且 lua 脚本保证原子性操作相当于上锁，已经判断超卖问题了，这个操作就不会出现并发问题：
```java
    Long execute = stringRedisTemplate.execute(  
            SECKILL_SCRIPT,  
            Collections.emptyList(),  
            voucherId.toString(), userId.toString()  
    );  
```

```java
    int result = execute.intValue();  
  
    if (result != 0) {  
        return Result.fail(result == 1 ? "库存不足" : "您已购买过");  
    }  
  
  
    // TODO 将userId 订单，和券id存入阻塞的队列中  
    VoucherOrder voucherOrder = new VoucherOrder();  
    long orderId = redisIdWorker.nextId("order");  
    voucherOrder.setId(orderId);  
    voucherOrder.setUserId(userId);  
    voucherOrder.setVoucherId(voucherId);  

```

在其他的线程获取阻塞队列的元素的时候，如果咩有，就会被阻塞：
```java
    orderBlockingQueue.add(voucherOrder);
    
    return Result.ok(orderId);  
}
```

完整实现，这里有不少问题：
```java
@Service  
@Slf4j  
public class VoucherOrderServiceImpl extends ServiceImpl<VoucherOrderMapper, VoucherOrder> implements IVoucherOrderService {  
    @Autowired  
    private SeckillVoucherServiceImpl seckillVoucherService;  
    @Autowired  
    private RedisIdWorker redisIdWorker;  
  
    @Autowired  
    private StringRedisTemplate stringRedisTemplate;  
  
    @Autowired  
    private RedissonClient redissonClient;  
  
    private static final DefaultRedisScript<Long> SECKILL_SCRIPT;  
  
    private IVoucherOrderService proxy  
  
    static {  
        SECKILL_SCRIPT = new DefaultRedisScript<>();  
        SECKILL_SCRIPT.setLocation(new ClassPathResource("seckill.lua"));  
        SECKILL_SCRIPT.setResultType(Long.class);  
    }  
  
    private ExecutorService EXECUTOR_SERVICE = Executors.newSingleThreadExecutor();  
  
    @PostConstruct  
    private void init() {  
        EXECUTOR_SERVICE.submit(() -> {  
            log.info("开始异步的去处理落库");  
            while (true) {  
                try {  
                    // 1.获取队列中的订单信息  
                    VoucherOrder voucherOrder = orderBlockingQueue.take();  
                    // 2.创建订单  
                    handleVoucherOrder(voucherOrder);  
                } catch (Exception e) {  
                    log.error("处理订单异常", e);  
                    //throw e;  
                }  
            }        });  
    }  
  
    private void handleVoucherOrder(VoucherOrder voucherOrder) {  
        proxy.createVoucherOrder(voucherOrder);  
    }  
  
    private BlockingQueue<VoucherOrder> orderBlockingQueue = new ArrayBlockingQueue<>(1024 * 1024);  
      
    public Result seckillVoucher(Long voucherId) {  
```

AopContext.currentProxy() 只能在一个正在执行的 AOP 代理方法内部调用：
```java
        // AopContext.currentProxy() 只能在一个正在执行的 AOP 代理方法内部调用  
        proxy = (IVoucherOrderService) AopContext.currentProxy();  
        Long userId = UserHolder.getUser().getId();  
        Long execute = stringRedisTemplate.execute(  
                SECKILL_SCRIPT,  
                Collections.emptyList(),  
                voucherId.toString(), userId.toString()  
        );  
  
        int result = execute.intValue();  
  
        if (result != 0) {  
            return Result.fail(result == 1 ? "库存不足" : "您已购买过");  
        }  
  
        // 创建订单  
        VoucherOrder voucherOrder = new VoucherOrder();  
        // 订单id  
        long orderId = redisIdWorker.nextId("order");  
        voucherOrder.setId(orderId);  
        // 用户id  
        voucherOrder.setUserId(userId);  
        // 代金券id  
        voucherOrder.setVoucherId(voucherId);  
  
        orderBlockingQueue.add(voucherOrder);  
  
        return Result.ok(orderId);  
    }  
  
    @Override  
    @Transactional    public  void createVoucherOrder(VoucherOrder voucherOrder) {  
        Long userId = voucherOrder.getUserId();  
        // 5.1.查询订单  
        int count = query().eq("user_id", userId).eq("voucher_id", voucherOrder.getVoucherId()).count();  
        // 5.2.判断是否存在  
        if (count > 0) {  
            // 用户已经购买过了  
            log.error("用户已经购买过了");  
            return ;  
        }  
  
        // 6.扣减库存  
        boolean success = seckillVoucherService.update()  
                .setSql("stock = stock - 1") // set stock = stock - 1  
                .eq("voucher_id", voucherOrder.getVoucherId()).gt("stock", 0) // where id = ? and stock > 0  
                .update();  
        if (!success) {  
            // 扣减失败  
            log.error("库存不足");  
            return ;  
        }  
        save(voucherOrder);  
    }  
}
```
