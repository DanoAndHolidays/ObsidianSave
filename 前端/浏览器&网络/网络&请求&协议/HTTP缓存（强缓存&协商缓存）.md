# HTTP缓存（强缓存&协商缓存）
[B站视频详解](https://www.bilibili.com/video/BV1Yb421B7Vg/?buvid=YA42DFA5A2C477DE4765996C4F2779201672&from_spmid=search.search-result.0.0&is_story_h5=false&mid=SJWPVQBk8Es5O8sHoXsqQg%3D%3D&plat_id=116&share_from=ugc&share_medium=iphone&share_plat=ios&share_session_id=9C5E44C0-B84F-4D64-A2CB-29EC18427AE9&share_source=WEIXIN&share_tag=s_i&spmid=united.player-video-detail.0.0&timestamp=1778555772&unique_k=xoLjQuK&up_id=31452330&vd_source=47c9acd507be61251cd2bb730416395c)
HTTP缓存主要分为强缓存和协商缓存两种机制

==所有的缓存策略仅仅针对`GET`生效==
![[Pasted image 20260610104321.png]]

首先看一个真实的GET响应头：
![[Pasted image 20260610104121.png]]

---
### 强缓存
![[Pasted image 20260610101731.png]]

强缓存流程，当浏览器请求资源时，会==先检查强缓存==是否有效：
1. 检查Cache-Control的max-age或s-maxage
2. 如果不存在，检查Expires字段
3. 如果缓存有效，在缓存的有效期内，直接使用缓存资源，不发送请求到服务器

---
### 协商缓存
使用Last-Modified的例子：
![[Pasted image 20260610102100.png]]

Last-Modified与Etag值的例子：
![[Pasted image 20260610102740.png]]


协商缓存流程，当==强缓存失效==时，进入==协商缓存==阶段：
1. 浏览器携带If-None-Match(缓存的ETag值)和If-Modified-Since(缓存的Last-Modified值)向服务器发起请求
2. 服务器验证资源是否修改：
   - 如果ETag匹配（一个hash值），返回304 Not Modified
   - 如果资源已修改，返回200和新资源

上述流程结束后，强缓存的时间就重置了

---
### HTTP缓存相关头部
`Expires`：绝对过期时间（HTTP/1.0）【已逐渐被Cache-Control取代】
`Cache-Control`：缓存控制指令（HTTP/1.1）【现代浏览器首选】，这里可以组合多种的属性，实现更细致的控制
- `max-age`：资源最大存活时间（秒）`max-age`优先级高于`expires`
- `public`：允许所有缓存节点缓存（包括代理服务器）【修正：public和private对于浏览器缓存效果相同，但影响中间代理缓存】![[Pasted image 20260610102918.png]]
- `private`：仅允许客户端缓存，不允许代理服务器缓存（默认值）![[Pasted image 20250910172246.png]]

- `no-cache`：需向服务器验证新鲜度（使用协商缓存），也就是只开启协商缓存，强缓存不开启。
- `no-store`：禁止任何缓存（内存、磁盘都不缓存）
- `s-maxage`：对代理服务器的有效时长（只有public属性存在的时候生效），用于共享缓存（如CDN），优先级高于`max-age`

这四个很少使用【补充说明：这些是Cache-Control扩展指令，使用场景较特殊】
- `max-stale`：客户端可以接受过期的缓存（请求头中使用）
- `min-fresh`：要求缓存至少还能保持指定秒数的新鲜度（请求头中使用）
- `must-revalidate`：一旦缓存过期，必须向服务器验证【补充：常见于重要资源】
- `no-transform`：禁止代理服务器对资源进行转换（如压缩图片）

---
### 推荐缓存策略
```http
# 静态资源（可长期缓存）
Cache-Control: public, max-age=31536000, immutable

# 经常变动的资源
Cache-Control: no-cache

# 敏感数据
Cache-Control: private, no-store, max-age=0
```

```http
# 带hash值的资源（长期缓存，设置为一年）
Cache-Control: public, max-age=31536000

# 不带hash值的资源（需要验证）
Cache-Control: no-cache
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2023 07:28:00 GMT
```