# 01 数据类型与 Commands
> Last Format Time：9/30/2026 01:00:03

[https://redis.io/docs/latest/commands/](https://redis.io/docs/latest/commands/)

---
## 数据类型
![[Pasted image 20260927225130.png]]


---
## 通用 Commands
Redis 命令关键字不区分大小写，但 value 区分大小写的

### 查看符合模板的 key
keys：
```text
127.0.0.1:6379> help keys

  KEYS pattern
  summary: Returns all key names that match a pattern.
  since: 1.0.0
  group: generic

127.0.0.1:6379> keys *
1) "name"
127.0.0.1:6379> keys a*
(empty array)
```

### 删除
del：
```text
127.0.0.1:6379> mset k1 v1 k2 v2 k3 v3
OK
127.0.0.1:6379> keys *
1) "k3"
2) "k2"
3) "k1"
127.0.0.1:6379> del k1
(integer) 1
127.0.0.1:6379> keys *
4) "k3"
5) "k2"
127.0.0.1:6379>
```

### 是否存在
exists：
```text
127.0.0.1:6379> exists k1
(integer) 0
127.0.0.1:6379> exists k2
(integer) 1
127.0.0.1:6379>
```

### 设置与查看有效期
expire 与 ttl：
```text
127.0.0.1:6379> expire k3 10
(integer) 1
127.0.0.1:6379> TTL k3
(integer) 2
127.0.0.1:6379> TTL k3
(integer) -2
127.0.0.1:6379>
```


---
## String
String类型，也就是字符串类型，是Redis中最简单的存储类型

其 value 是字符串，不过根据字符串的格式不同，又可以分为3类：

- string：普通字符串
- int：整数类型，可以做自增、自减操作
- float：浮点类型，可以做自增、自减操作

### 常见命令
SET：添加或者修改已经存在的一个String类型的键值对
GET：根据key获取String类型的value

MSET：批量添加多个String类型的键值对
MGET：根据多个key获取多个String类型的value

INCR:让一个整型的key自增1
INCRBY:让一个整型的key自增并指定步长，例如：incrby num 2让num值自增2

INCRBYFLOAT:让一个浮点类型的数字自增并指定步长

SETNX：添加一个String类型的键值对，前提是这个key不存在，否则不执行

```shell
# 也可以写成这样
SET k1 v1 NX
```

SETEX：添加一个String类型的键值对，并且指定有效期

```shell
SET k1 v1 EX 100
```

### 格式
![[Pasted image 20260927231523.png]]

```text
127.0.0.1:6379> MSET dano:k1 v1 dano:k2 v2 dano:k3 v3
OK
127.0.0.1:6379> KEYS dano*
1) "dano:k2"
2) "dano:k1"
3) "dano:k3"
127.0.0.1:6379>
```

在图形界面就可以看见层级结构了：
![[Pasted image 20260927231757.png]]


---
## Hash
![[Pasted image 20260927232051.png]]

HSET key field value：添加或者修改hash类型key的field的值
HGET key field：获取一个hash类型key的field的值

HMSET：批量添加多个hash类型key的field的值
HMGET：批量获取多个hash类型key的field的值

HGETALL：获取一个hash类型的key中的所有的field和value

```text
127.0.0.1:6379> hgetall dano:666
1) "name"
2) "Tom"
3) "age"
4) "13"
127.0.0.1:6379>
```

HKEYS：获取一个hash类型的key中的所有的field
HVALS：获取一个hash类型的key中的所有的value

HINCRBY:让一个hash类型key的字段值自增并指定步长

HSETNX:添加一个hash类型的key的field值，前提是这个field不存在，否则不执行


---
## List
![[Pasted image 20260928230136.png]]

LPUSH key element...：向列表左侧插入一个或多个元素
LPOP key：移除并返回列表左侧的第一个元素，没有则返回nil

RPUSH key element...：向列表右侧插入一个或多个元素
RPOP key：移除并返回列表右侧的第一个元素

LRANGE key star end:返回一段角标范围内的所有元素

BLPOP和BRPOP：与LPOP和RPOP类似，只不过在没有元素时等待指定时间，而不是直接返回nil


---
## Set
![[Pasted image 20260928230849.png]]

SADD key member ...：向set中添加一个或多个元素
SREM key member ...：移除set中的指定元素
SCARD key:返回set中元素的个数
SISMEMBER key member：判断一个元素是否存在于set中
SMEMBERS：获取set中的所有元素

---
## SortedSet
![[Pasted image 20260928231210.png]]

ZADD key score member：添加一个或多个元素到sorted set，如果已经存在则更新其score值
ZREM key member:删除sorted set中的一个指定元素
ZSCORE key member：获取sorted set中的指定元素的score值
ZRANK key member：获取sorted set 中的指定元素的排名
ZCARD key：获取sorted set中的元素个数
ZCOUNT key min max：统计score值在给定范围内的所有元素的个数
ZINCRBY key increment member：让sorted set中的指定元素自增，步长为指定的increment值
ZRANGE key min max：按照score排序后，获取指定排名范围内的元素
ZRANGEBYSCORE key min max：按照score排序后，获取指定score范围内的元素
ZDIFF、ZINTER、ZUNION：求差集、交集、并集
