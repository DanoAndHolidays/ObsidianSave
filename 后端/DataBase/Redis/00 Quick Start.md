# 00 Quick Start
> Last Format Time：9/30/2026 01:00:03

Redis 是一种 NoSQL（非关系型数据库）

![[Pasted image 20260927221555.png]]

---
## Redis
Redis (Remote Dictionary Server)，特点：

- 键值型
- 单线程（基于内存、IO多路复用）
- 支持数据持久化
- 支持集群

*这玩意还得学Linux，绕了一圈又回来了*

[[后端/Linux/00 Quick Start]]


使用 Docker 来运行：
[[基础]]

```shell
docker exec -it redis redis-cli
```

其数据库的数量是有限的 1-16 个：
```shell
# 切换为 index 为 0 的数据库
select 0
```
