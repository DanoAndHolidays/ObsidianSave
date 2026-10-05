# 04 Cache 缓存
> Last Format Time：10/6/2026 02:27:25

在我们查询商户信息时，直接操作从数据库去查询，查询数据库慢，需要增加缓存：
```java
@GetMapping("/{id}")
public Result queryShopById(@PathVariable("id") Long id) {
    //这里是直接查询数据库
    return shopService.queryById(id);
}
```

![[Pasted image 20260930161127.png]]

```java
@Service  
public class ShopServiceImpl extends ServiceImpl<ShopMapper, Shop> implements IShopService {  
    @Autowired  
    private StringRedisTemplate stringRedisTemplate;  
  
    @Override  
    public Result queryById(Long id) {  
        String key = "catch:shop:" + id;  
        String shopJson = stringRedisTemplate.opsForValue().get(key);  
        if (StrUtil.isNotBlank(shopJson)) {  
            return Result.ok(JSONUtil.toBean(shopJson, Shop.class));  
        }  
  
        Shop shop = getById(id);  
        if(shop == null){  
            return Result.fail("商铺id错误");  
        }  
  
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop));  
  
        return Result.ok(shop);  
    }  
}
```

---
## 缓存更新策略
![[Pasted image 20260930172832.png]]

### 主动更新
- Cache Aside Pattern 人工编码方式，缓存调用者在更新完数据库后再去更新缓存，也称之为双写方案
- Read/Write Through Pattern 由系统本身完成，数据库与缓存的问题交由系统本身去处理
- Write Behind Caching Pattern 调用者只操作缓存（Redis），其他线程去异步处理数据库，实现最终一致

如果采用第一个方案，那么假设我们每次操作数据库后，都操作缓存，但是中间如果没有人查询，那么这个更新动作实际上只有最后一次生效，中间的更新动作意义并不大，我们可以把缓存删除，等待再次查询时，将缓存中的数据加载出来

* 删除缓存还是更新缓存？
  * 更新缓存：每次更新数据库都更新缓存，无效写操作较多
  * ==删除缓存==：更新数据库时让缓存失效，查询时再更新缓存 ✅





* 如何保证缓存与数据库的操作的同时成功或失败？
  * 单体系统，将缓存与数据库操作放在一个事务
  * 分布式系统，利用 TCC 等==分布式事务==方案

应该具体操作缓存还是操作数据库，我们应当是先操作数据库，再删除缓存，原因在于，如果你选择第一种方案，在两个线程并发来访问时，假设线程1先来，他先把缓存删了，此时线程2过来，他查询缓存数据并不存在，此时他写入缓存，当他写入缓存后，线程1再执行更新动作时，实际上写入的就是旧的数据，新的数据被旧数据覆盖了。

* 先操作缓存还是先操作数据库？
  * 先删除缓存，再操作数据库
  * ==先操作数据库，再删除缓存== ✅

![[Pasted image 20261005205056.png]]

![[Pasted image 20261005205213.png]]

```java
@Override  
public Result queryById(Long id) {  
    String key = "cache:shop:" + id;  
    String shopJson = stringRedisTemplate.opsForValue().get(key);  
    if (StrUtil.isNotBlank(shopJson)) {  
        return Result.ok(JSONUtil.toBean(shopJson, Shop.class));  
    }  
  
    Shop shop = getById(id);  
    if (shop == null) {  
        return Result.fail("商铺id错误");  
    }  
  
    stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop), 30L, TimeUnit.MINUTES);  
  
    return Result.ok(shop);  
}  
  
@Transactional  
public Result updateShop(Shop shop) {  
    Long id = shop.getId();  
    if (id == null) {  
        return Result.fail("店铺的ID不能为空");  
    }  
    String key = "cache:shop:" + id;  
  
    // 优先更新数据库  
    updateById(shop);  
  
    // 之后清除缓存  
    stringRedisTemplate.delete(key);  
  
    return Result.ok();  
}
```

---
## 缓存问题
### 缓存穿透
指客户端请求的数据在==缓存==中和==数据库==中==都不存在==，这样缓存永远不会生效，这些请求都会持续的打到数据库，如果有坏B一直搞，很快就爆了，常见的解决方案：

- 加权限、登录
- 限流
- ==缓存空对象==
	* 优点：实现简单，维护方便
	* 缺点：
		* 额外的内存消耗
		* 可能造成短期的不一致（可以主动在==新建数据==的时候将数据加入缓存 / 删除空缓存）

- 布隆过滤
	* 优点：内存占用较少，没有多余key
	* 缺点：
	    * 实现复杂
	    * 存在误判可能

![[Pasted image 20260930185948.png]]


![[Pasted image 20260930190238.png]]

```java
@Override  
public Result queryById(Long id) {  
    String key = "cache:shop:" + id;  
    String shopJson = stringRedisTemplate.opsForValue().get(key);  
    if (StrUtil.isNotBlank(shopJson)) {  
        return Result.ok(JSONUtil.toBean(shopJson, Shop.class));  
    }  
  
    // 缓存命中了并且是空的  
    if(StrUtil.isBlank(shopJson) && shopJson != null){  
        return Result.fail("没有对应id的商铺");  
    }  
  
    Shop shop = getById(id);  
    if (shop == null) {  
        // 写入空数据到缓存中  
        stringRedisTemplate.opsForValue().set(key, "", 3L, TimeUnit.MINUTES);  
        return Result.fail("商铺id错误");  
    }  
  
    stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop), 30L, TimeUnit.MINUTES);  
  
    return Result.ok(shop);  
}
```

### 缓存雪崩
在同一时段大量的==缓存 key 同时失效==或者 Redis 服务==宕机==，导致大量请求到达数据库，带来巨大压力，解决方案：

* 给不同的 Key 的 TTL 添加随机值
* 利用 Redis 集群提高服务的可用性
* 给缓存业务添加降级限流策略，直接返回
* 给业务添加多级缓存，比如在 Nginx 中建立缓存

在做==缓存预热==的时候，会批量的将数据导入缓存中，这时就有可能会有大量相同 TTL 的数据

你可能这样写：
```text
Random random = new Random();
random.nextInt(10);
```

功能完全没问题，但是高并发服务里，这意味着每次执行都要创建一个新对象

那我共享呢？单线程没什么问题，但多个线程如果**共享一个 `Random` 对象**：
```text
Random random = new Random();
```

多个线程都要修改同一个随机数生成器内部状态，会产生竞争，可以简单想象：
```text
线程 A ─┐
线程 B ─┼─→ 同一个 Random 状态
线程 C ─┘
```

并发高的时候性能会受影响，而 `ThreadLocalRandom`：
```text
线程 A → 自己的随机状态
线程 B → 自己的随机状态
线程 C → 自己的随机状态
```

线程之间基本不用争，这和你前面学的 `ThreadLocal` 思路非常像：
```java
long expireTime = ThreadLocalRandom.current().nextLong(0, 6) + 30L;  

stringRedisTemplate.opsForValue().set(
	key, 
	JSONUtil.toJsonStr(shop), 
	expireTime, 
	TimeUnit.MINUTES
);
```

### 缓存击穿
也叫热点 Key 问题，就是一个==被高并发访问==并且==缓存重建==业务较==复杂==的 key 突然失效了，无数的请求访问会在瞬间给数据库带来巨大的冲击

常见的解决方案有两种：

* 互斥锁
* 逻辑过期

![[Pasted image 20260930194502.png]]

![[Pasted image 20260930194651.png]]

*这里可以使用 Redission 不要自己造轮子*

##### 互斥锁
![[Pasted image 20260930195249.png]]

核心思路就是利用redis的setnx方法来表示获取锁，该方法含义是redis中如果没有这个key，则插入成功，返回1，在stringRedisTemplate中返回true，如果有这个key则插入失败，则返回0，在stringRedisTemplate返回false，我们可以通过true，或者是false，来表示是否有线程成功插入key，成功插入的key的线程我们认为他就是获得到锁的线程
![[Pasted image 20260930195346.png]]

```java
private boolean tryLock(String key) {
    Boolean flag = stringRedisTemplate.opsForValue().setIfAbsent(
	    key,
	    "1", 
	    10, 
	    TimeUnit.SECONDS
	);
	
    return BooleanUtil.isTrue(flag);
}

private void unlock(String key) {
    stringRedisTemplate.delete(key);
}
```

##### 逻辑过期时间
 ![[Pasted image 20260930214956.png]]
