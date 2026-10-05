# 00 JMM
> Last Format Time：10/6/2026 02:27:25

JMM 是 **Java Memory Model（Java 内存模型）**

将物理内存分为主内存与工作内存，JMM 规定了多线程环境下，一个线程对共享变量的读写，什么时候能被其他线程看到，以及这些读写操作允许怎样被重排序

JMM 经常会使用这两个概念：
```text
主内存
Working Memory（线程工作内存）
```

可以简单理解：
```text
              主内存
          ┌───────────┐
          │ 共享变量   │
          │ count = 0 │
          └─────┬─────┘
                │
        ┌───────┴───────┐
        ↓               ↓
┌──────────────┐  ┌──────────────┐
│ Thread A     │  │ Thread B     │
│ 工作内存      │  │ 工作内存      │
│ count = 0    │  │ count = 0    │
└──────────────┘  └──────────────┘
```

线程不会简单地理解成“每次都直接访问主内存”。

它可能把变量的值：
```text
主内存
↓
加载到寄存器 / CPU Cache
↓
线程使用
```

所以：
```text
线程 A 修改了变量
```

并不天然意味着：
```text
线程 B 马上看到
```

JMM 就规定了，在什么条件下这些修改必须可见。

注意，这里的主内存 / 工作内存是 **JMM 的抽象概念**。

不等于：
```text
主内存 = JVM Heap
工作内存 = JVM Stack
```

不要直接对应。

假设有两个线程：
```java
int num = 0;
boolean ready = false;

// 线程 A
num = 42;
ready = true;

// 线程 B
if (ready) {
    System.out.println(num);
}
```

你可能觉得：
```text
A：
num = 42
↓
ready = true

B：
看到 ready == true
↓
肯定打印 42
```

![[Pasted image 20261003223749.png]]

但如果没有任何同步措施，这个结论在 Java 内存模型下**不一定成立**。

原因主要有三个：

- CPU 缓存导致的 **可见性问题**
- 多线程交错导致的 **原子性问题**
- 编译器 / CPU 优化导致的 **指令重排序问题**

---
## 原子性
---
## 可见性
volatile 它可以用来修饰==成员变量==和==静态成员变量==，他可以避免线程从自己的工作缓存中查找变量的值，必须到主存中获取它的值，线程操作 volatile 变量都是直接操作主存

所以你现在可以把 `synchronized` 理解成两层：
```text
synchronized
├── Monitor / 锁层面
│   └── 保证互斥
│
└── JMM 层面
    ├── 保证可见性
    └── 建立 happens-before
```

使用 volatile 来实现两阶段终止：


---
## 有序性
JVM 会在不影响正确性的情况下进行语句顺序的调整（指令重排），但是在多线程模式下，就可能会有问题

加 volatile 禁用指令重排

volatile 的底层实现原理是内存屏障，Memory Barrier(Memory Fence)
对 volatile 变量的写指令后会加入写屏障，写屏障前面的变量的改动都同步到主存，保证可见性
对 volatile 变量的读指令前会加入读屏障，读屏障后的的变量的读取，加载的都是最新的主存数据

写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后
读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前

### 流水线
![[Pasted image 20261003231033.png]]

### Double Check Balking
假如代码都是在 sync 保护下，根本不会有多个线程同时操作，那么重不重排无所谓了

```java
public class MonitorService {

    // volatile：
    // 1. 保证 started 在线程之间的可见性
    // 2. 因为第一次判断没有加 synchronized，所以必须保证能看到其他线程修改后的值
    private volatile boolean started = false;

    public void start() {

        // 第一次检查：
        // 大部分情况下任务已经启动了，
        // 直接返回，不需要每次都进入 synchronized，提高性能
        if (started) {
            return; // Balking：条件不满足，直接放弃执行
        }

        synchronized (this) {

            // 第二次检查：
            // 因为多个线程可能同时通过第一次 started == false
            //
            // 例如：
            // Thread-A                     Thread-B
            // started == false             started == false
            //        ↓                            ↓
            // 进入 synchronized             等待锁
            //
            // A 将 started = true 后释放锁
            // B 获得锁时必须再检查一次
            //
            // 如果没有第二次检查，B 也会启动一个线程
            if (started) {
                return; // 再次 Balking
            }

            // 到这里说明：
            // 当前线程是真正第一个负责启动任务的线程
            started = true;
        }

        // 真正启动后台任务
        new Thread(() -> {
            while (true) {
                System.out.println("监控任务执行中...");

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }).start();
    }
}
```

---
## happens-before
如果操作 A happens-before 操作 B，那么 A 的执行结果必须对 B 可见，并且 A 在顺序上先于 B

```java
int num = 0;
volatile boolean ready = false;

// Thread A
num = 42;
ready = true;

// Thread B
if (ready) {
    System.out.println(num);
}
```

synchronized 也可以做到类似的效果
