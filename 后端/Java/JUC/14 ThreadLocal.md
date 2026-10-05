# 14 ThreadLocal
> Last Format Time：10/6/2026 02:27:25

[[03 Session 短信登录]]

`ThreadLocal` 是 Java 提供的**线程本地变量机制**，它的作用不是让多个线程共享数据，同一个 `ThreadLocal` 可以被多个线程使用，但==每个线程==保存==自己的独立数据==，==互不影响==

例如：
```text
ThreadLocal<String> local = new ThreadLocal<>();
```

线程 A：
```text
local.set("A");
local.get(); // A
```

线程 B：
```text
local.set("B");
local.get(); // B
```

虽然使用的是同一个 `ThreadLocal` 对象，但两个线程拿到的数据不同。

---
## 核心原理
数据实际上**不是存储在 ThreadLocal 对象中，而是存储在线程 Thread 对象中**

每个线程内部都有一个：
```text
ThreadLocal.ThreadLocalMap threadLocals;
```

结构可以理解为：
```text
Thread-1
└── ThreadLocalMap
    ├── threadLocalA → valueA
    └── threadLocalB → valueB

Thread-2
└── ThreadLocalMap
    ├── threadLocalA → valueC
    └── threadLocalB → valueD
```

因此不同线程操作的是自己的 `ThreadLocalMap`，从而实现**线程数据隔离**

### ThreadLocalMap
在解决冲突的时候使用的是==开放地址法==，有冲突去后面找，不是用的 HashMap 的拉链法

Map 中的 ==key==，是==弱引用==，在 GC 的时候，就可以回收。但是这里没有释放 value，在 key 被回收后，value 会变成 null：

- get(key) 发现是 null，会顺手清理
- set(key) 会清理附近的 null value
- 手动的调用 remove()


---
## 常用 API
### set()
保存当前线程的数据：
```text
threadLocal.set(value);
```

### get()
获取当前线程的数据：
```text
threadLocal.get();
```

### remove()
删除当前线程中的数据：
```text
threadLocal.remove();
```

---
## 典型使用场景
适合保存属于当前线程，并且需要在当前线程整个调用链中使用的数据

传统 Spring MVC 的==一次同步 HTTP 请求==中，Interceptor → Controller → Service → Repository 通常由同一个 Tomcat 工作线程一路执行，因此 ThreadLocal 可以贯穿整个调用链

一旦中途发生异步执行或线程切换，普通 ThreadLocal 就无法自动把数据传递到新线程，例如 Web 请求：
```text
请求
 ↓
Interceptor
 ↓
Controller
 ↓
Service
 ↓
Repository
```

登录后可以把当前用户保存到：
```text
ThreadLocal<User>
```

之后 Service 等位置可以直接：
```text
User user = UserHolder.getUser();
```

不需要：
```text
Controller(user)
    ↓
Service(user)
    ↓
Repository(user)
```

一路传参数。

---
## ThreadLocal 和线程共享变量的区别
普通共享变量：
```text
Thread-1 ─┐
          ├── sharedData
Thread-2 ─┘
```

多个线程访问同一份数据，因此可能需要考虑线程安全问题。

ThreadLocal：
```text
Thread-1 → value1

Thread-2 → value2

Thread-3 → value3
```

每个线程拥有自己的数据，主要解决的是线程隔离，而不是线程通信

如果需要线程 A 设置数据，线程 B 获取数据，通常不应该使用 `ThreadLocal`。

---
## 注意 remove()
线程池中的线程会被重复使用：
```text
请求 A
 ↓
Thread-1
 ↓
ThreadLocal = UserA

请求结束

请求 B
 ↓
继续使用 Thread-1
```

如果请求 A 没有清理：
```text
threadLocal.remove();
```

请求 B 就可能遇到上一个请求残留的数据。

因此通常：
```text
try {
    threadLocal.set(user);

    // 业务逻辑
} finally {
    threadLocal.remove();
}
```

在线程池、Tomcat 等环境中尤其重要。

---
## 一句话记忆

> `ThreadLocal` 是线程本地变量机制，每个 `Thread` 内部维护自己的 `ThreadLocalMap`，以 `ThreadLocal` 为 key 保存当前线程的数据，通过 `Thread.currentThread()` 找到当前线程，因此实现线程之间的数据隔离。

重点记：
```text
Thread
 ↓
ThreadLocalMap
 ↓
ThreadLocal → value
```

不是：
```text
ThreadLocal
 ↓
存所有线程的数据
```

### 面试高频
**ThreadLocalMap 存在哪里？**

```text
Thread 对象中
```

**ThreadLocal 是干什么的？**

```text
线程数据隔离
```

**多个线程的数据会互相影响吗？**

```text
不会，每个线程有自己的 ThreadLocalMap
```

**在线程池中为什么要 remove？**

```text
线程会复用，避免旧数据残留以及相关的内存泄漏风险。
```
