# 02 Synchronized
> Last Format Time：10/6/2026 02:27:25

[[15 多线程与并发]]

`synchronized` 是 Java 内置的同步关键字，底层通过对象的 Monitor 实现锁机制，并且这把锁是可重入的

```java
synchronized(单例锁对象){
	// ...
}
```

```java
class Test { 
	public synchronized void test() { 
		// ...
	}
}
// 等价于
class Test { 
	public void test() { 
		synchronized(this) { 
			// ...
		} 
	} 
}
```

```java
class Test { 
	public synchronized static void test() { 
		// ...
	}
}
// 等价于
class Test { 
	public static void test() { 
		synchronized(Test.class) { 
			// ...
		} 
	} 
}
```

可以理解成：
```text
尝试获取 obj 对应的锁
        ↓
获取成功
        ↓
执行 synchronized 代码块
        ↓
退出代码块
        ↓
自动释放锁
```

`synchronized` 本身虽然是**可重入锁**，能避免“线程被自己再次获取同一把锁卡死”，但如果多个线程获取**多把锁的顺序不一致**，仍然会发生死锁，最经典的例子：
```java
Object lockA = new Object();
Object lockB = new Object();

Thread t1 = new Thread(() -> {
    synchronized (lockA) {
        synchronized (lockB) {
            // ...
        }
    }
});

Thread t2 = new Thread(() -> {
    synchronized (lockB) {
        synchronized (lockA) {
            // ...
        }
    }
});
```

可能出现：
```text
T1：拿到 lockA
T2：拿到 lockB

T1：等待 lockB
T2：等待 lockA

双方互相等待
→ 死锁
```


---
## Monitor 管程
### 对象头
Java 里说的“对象头（Object Header）”，通常是指 **HotSpot JVM 中每个对象最前面的一块元数据**。它不属于你定义的 Java 字段，而是 JVM 为了管理对象额外存进去的信息。

可以先把一个普通 Java 对象理解成：
```text
Java 对象
┌──────────────────────────┐
│ Object Header 对象头      │
├──────────────────────────┤
│ Instance Data 实例数据    │
├──────────────────────────┤
│ Padding 对齐填充          │
└──────────────────────────┘
```

其中对象头主要有两部分：
```text
Object Header
├── Mark Word
└── Klass Pointer
```

如果是数组，还会多一个：
```text
Array Object Header
├── Mark Word
├── Klass Pointer
└── Array Length
```

##### Mark Word
**Mark Word 是对象自身运行时状态的信息。**
在典型的 64 位 HotSpot JVM 中，Mark Word 通常占：
```text
8 bytes = 64 bit
```

里面可能记录：
```text
┌──────────────────────────┐
│ Mark Word                │
├──────────────────────────┤
│ identity hashCode        │
│ GC 分代年龄               │
│ 锁相关状态                │
│ GC 标记信息               │
│ 其他 JVM 状态             │
└──────────────────────────┘
```

例如：
```text
Object obj = new Object();

System.identityHashCode(obj);
```

`identityHashCode` 对应的信息通常就和 **Mark Word** 有关。

你最近正在学 `synchronized`，所以这里尤其重要：
```text
synchronized (obj) {
    // JVM 会使用 obj 的对象头参与锁管理
}
```

因为 JVM 可以利用这个对象的 **Mark Word** 保存或表示和锁相关的状态。

不过要注意：**Mark Word 的具体 bit 布局不是 Java 语言规范规定死的**，它属于 JVM 实现细节，不同 HotSpot 版本、锁实现和 GC 下可能有所变化。

### 重量级锁与轻量级锁
在使用 synchronized 时：
```java
synchronized (obj) {
    // ...
}
```

如果一个对象虽然有多线程访问，但多线程访问的时间是错开的（也就是没有竞争），那么可以使用轻量级锁来优化，是透明的，和重锁的语法一致：
![[Pasted image 20261003162415.png]]

这里的交换是个 CAS 的过程，01 交换为 00，不是 01 就会失败：

- 如果 obj 一开始是 00 说明是有竞争的，会锁膨胀，变为重量级锁
- 如果是自己再次获取锁，就会添加一条 Lock Record 作为重入的记录

出锁之后就会恢复保存在Lock Record 中的 Mark Word：
![[Pasted image 20261003162457.png]]

obj 会变为重锁状态：
![[Pasted image 20261003160223.png]]

一个对象有一个 Monitor，不同的对象的 Monitor 不同：
![[Pasted image 20261003160705.png]]

![[Pasted image 20261003160444.png]]

##### 锁膨胀
![[Pasted image 20261003163420.png]]

Thread-1 申请 Monitor，转换为重锁：
![[Pasted image 20261003163530.png]]

##### 自旋优化
![[Pasted image 20261003163812.png]]

##### 偏向锁
自 JDK15 起，偏向锁已被废弃，JDK20 被移除，可以在 JDK8 中将其关闭以提高性能

##### 锁消除
和 JVM [[逃逸分析]]有关，可以移除没必要的 synchronized

### WaitSet
![[Pasted image 20261003165355.png]]
Owner 线程发现条件不满足，调用 wait 方法，即可进入 WaitSet 变为 WAITING 状态
BLOCKED 和 WAITING 的线程都处于阻塞状态，不占用CPU时间片，BLOCKED 线程会在 Owner 线程释放锁时唤醒
WAITING 线程会在 Owner 线程调用 notify 或 notifyAll 时唤醒，但唤醒后并不意味者立刻获得锁，仍需进入 EntryList 重新竞争 

注意，这些方法必须在线程是 Monitor 的 Owner 的时候，才能调用：

- obj.wait() 让进入 object 监视器的线程到 waitSet 等待，放弃 Owner 的身份，Monitor 被释放
- obj.notify() 在object 上正在 waitSet 等待的线程中挑—个唤醒
- obj.notifyAll() 让 object 上正在 waitSet 等待的线程全部唤醒

---
## 线程八锁
### 同一个对象，两个 synchronized 方法
```java
class Number {

    public synchronized void a() {
        System.out.println("a");
    }

    public synchronized void b() {
        System.out.println("b");
    }
}
```

调用：
```java
Number n = new Number();

new Thread(n::a).start();
new Thread(n::b).start();
```

两个方法都锁：
```text
n
```

所以：
```text
a 和 b 互斥
```

谁先拿到锁谁先执行。

### 加入 sleep
```java
public synchronized void a() {
    Thread.sleep(1000);
    System.out.println("a");
}
```

另一个线程：
```java
public synchronized void b() {
    System.out.println("b");
}
```

如果 `a()` 先拿到锁：
```text
a 获得锁
↓
sleep 1 秒
↓
打印 a
↓
释放锁
↓
b 执行
```

结果：
```text
a
b
```

`sleep()` 不会释放锁

### 增加一个普通方法
```java
public synchronized void a() {
    Thread.sleep(1000);
    System.out.println("a");
}

public synchronized void b() {
    System.out.println("b");
}

public void c() {
    System.out.println("c");
}
```

其中：
```text
c()
```

没有 `synchronized`。

所以：

```text
c 不需要获取锁
```

即使 `a()` 正持有对象锁：
```text
a 获得锁
↓
sleep

与此同时：
c 可以直接执行
```

可能输出：
```text
c
a
b
```

synchronized 只影响需要获取同一把锁的代码。

不是说：
```text
对象被锁住之后，整个对象所有方法都不能访问
```

这是错误理解。

### 两个不同对象
```java
Number n1 = new Number();
Number n2 = new Number();

new Thread(n1::a).start();
new Thread(n2::b).start();
```

虽然：
```text
a()
b()
```

都是 synchronized 方法。

但是：
```text
n1.a() 锁的是 n1
n2.b() 锁的是 n2
```

也就是：
```text
锁 n1
锁 n2
```

不是同一把锁，可以并发执行。

### 两个 static synchronized 方法
```java
public static synchronized void a() {
}

public static synchronized void b() {
}
```

这两个方法锁的都是：
```text
Number.class
```

所以：
```text
a 和 b 互斥
```

即使这样调用：
```java
Number n1 = new Number();
Number n2 = new Number();

new Thread(n1::a).start();
new Thread(n2::b).start();
```

依然会互斥。

### 两个对象 + static synchronized
例如：
```java
Number n1 = new Number();
Number n2 = new Number();

new Thread(n1::a).start();
new Thread(n2::b).start();
```

其中：
```java
public static synchronized void a() {
}

public static synchronized void b() {
}
```

虽然：
```text
n1 != n2
```

但锁仍然都是：
```text
Number.class
```

所以：
```text
仍然互斥
```

### 一个 static synchronized，一个普通 synchronized
```java
public static synchronized void a() {
}

public synchronized void b() {
}
```

假设：
```java
Number n = new Number();
```

此时：
```text
a() 锁：Number.class
b() 锁：n
```

两把锁不同。

可以同时执行。

### 两个对象，一个 static synchronized，一个普通 synchronized
例如：
```java
Number n1 = new Number();
Number n2 = new Number();

new Thread(n1::a).start();
new Thread(n2::b).start();
```

其中：
```java
public static synchronized void a() {
}

public synchronized void b() {
}
```

锁分别是：
```text
a → Number.class

b → n2
```

依然不是同一把锁。

所以：
```text
互不影响
```

可以并发执行。
