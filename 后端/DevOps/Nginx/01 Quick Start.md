---

---
# 01 Quick Start
> Last Format Time：9/30/2026 01:00:03

---
## 反向代理
这里和[[跨域&跨站]]串起来了，学到了，好爽

![[Pasted image 20260918011917.png]]


前端请求地址：http://localhost/api/employee/login
后端接口地址：http://localhost:8080/admin/employee/login

前端请求地址后端接口地址

![](https://ocn8gnorkt9i.feishu.cn/space/api/box/stream/download/asynccode/?code=YWFmNDk0NzllODhhYjE1Mzg3YWMwMTY5YTdjMDU5ZjdfSlFRVDV0c3p3azlnSWFDNHFiWUxZd21sMldDZkRMMlVfVG9rZW46Wkp6eWJ2dGtXb2hWNXl4V0pOQ2MwWEpzbkNmXzE3OTA1MTQ0MjM6MTc5MDUxODAyM19WNA&add_watermark=true&scene_type=CCM)

![](https://ocn8gnorkt9i.feishu.cn/space/api/box/stream/download/asynccode/?code=NjBjNGJlZGQxYjIwM2FmMzQ2NDg0YjdkZmM5MDNkZjFfZGJkUDMxMVFTM00zRGV5bnlieGdvYm45V3VqejZZdjRfVG9rZW46TlVmWWJFT0Vpb0ZRZXp4VTRNVGNJRzh0bkVkXzE3OTA1MTQ0MjM6MTc5MDUxODAyM19WNA&add_watermark=true&scene_type=CCM)

**nginx 反向代理**，就是将前端发送的动态请求由 nginx 转发到后端服务器
![](https://ocn8gnorkt9i.feishu.cn/space/api/box/stream/download/asynccode/?code=ZTAxYjgyYTE2NjA2OTYyZmRmOTQ1YmY4YTUyOWM4ZDNfUWd2UHBCYnZrREVNcWJ5SmhHWW1BMXVtbWRXTU9FMGdfVG9rZW46UTdtQ2I1VFhrb2tBWkZ4cldkdWNDWHZwbjZiXzE3OTA1MTQ0MjM6MTc5MDUxODAyM19WNA&add_watermark=true&scene_type=CCM)


### nginx 反向代理的好处
- 提高访问速度因为nginx本身可以进行==缓存==，如果访问的同一接口，并且做了数据缓存，nginx就直接可把数据返回，不需要真正地访问服务端，从而提高访问速度。
- 进行==负载均衡==所谓负载均衡,就是把大量的请求按照我们指定的方式均衡的分配给集群中的每台服务器。
- 保证后端服务安全因为一般后台==服务地址不会暴露==，所以使用浏览器不能直接访问，可以把nginx作为请求访问的入口，请求到达nginx后转发到具体的服务中，从而保证后端服务的安全。

![](https://ocn8gnorkt9i.feishu.cn/space/api/box/stream/download/asynccode/?code=YTE4NmE5YzAwMjJiYzYxNGI1Y2RlMTNlZWQzYTMwNWVfeENvTEpqdUx4enFzY1hQSnlxZ1Nld2xxMjZDZ1lkNU9fVG9rZW46WDlUcWJ6dGRKb09HTG14U1Z0SWNCbGtUblNoXzE3OTA1MTQ0MjM6MTc5MDUxODAyM19WNA&add_watermark=true&scene_type=CCM)

配置方式：
```nginx
server{
    listen 80;
    server_name localhost;

    location /api/{
        proxy_pass http://localhost:8080/admin/; #反向代理
    }
}
```

proxy_pass：该指令是用来设置代理服务器的地址，可以是主机名称，IP地址加端口号等形式。

如上代码的含义是：监听80端口号，然后当我们访问` http://localhost:80/api/../..` 这样的接口的时候，它会通过 `location /api/ {}` 这样的反向代理到 `http://localhost:8080/admin/` 上来

接下来，进到nginx-1.20.2\conf，打开nginx配置

```nginx
# 反向代理,处理管理端发送的请求
location /api/ {
	proxy_pass   http://localhost:8080/admin/;
    #proxy_pass   http://webservers/admin/;
}
```

当在访问http://localhost/api/employee/login，nginx接收到请求后转到http://localhost:8080/admin/，故最终的请求地址为http://localhost:8080/admin/employee/login，和后台服务的访问地址一致。


---
## 负载均衡
当如果服务以集群的方式进行部署时，那nginx在转发请求到服务器时就需要做相应的负载均衡

nginx 负载均衡的配置方式：
```nginx
upstream webservers{
    server 192.168.100.128:8080;
    server 192.168.100.129:8080;
}
server{
    listen 80;
    server_name localhost;

    location /api/{
        proxy_pass http://webservers/admin;#负载均衡
    }
}
```

upstream：如果代理服务器是一组服务器的话，我们可以使用 upstream 指令配置后端服务器组

### 负载均衡策略
|**名称**|**说明**|
|---|---|
|轮询|默认方式|
|weight|权重方式，默认为1，权重越高，被分配的客户端请求就越多|
|ip_hash|依据ip分配方式，这样每个访客可以固定访问一个后端服务|
|least_conn|依据最少连接方式，把请求优先分配给连接数少的后端服务|
|url_hash|依据url分配方式，这样相同的url会被分配到同一个后端服务|
|fair|依据响应时间方式，响应时间短的服务将会被优先分配|

具体配置方式：

### 轮询
```nginx
upstream webservers{
    server 192.168.100.128:8080;
    server 192.168.100.129:8080;
}
```

### weight
```nginx
upstream webservers{
    server 192.168.100.128:8080 weight=90;
    server 192.168.100.129:8080 weight=10;
}
```

### ip_hash
```nginx
upstream webservers{
    ip_hash;
    server 192.168.100.128:8080;
    server 192.168.100.129:8080;
}
```

### least_conn
```nginx
upstream webservers{
    least_conn;
    server 192.168.100.128:8080;
    server 192.168.100.129:8080;
}
```

### url_hash
```nginx
upstream webservers{
    hash &request_uri;
    server 192.168.100.128:8080;
    server 192.168.100.129:8080;
}
```

### fair
```nginx
upstream webservers{
    server 192.168.100.128:8080;
    server 192.168.100.129:8080;
    fair;
}
```
