# 01 Process & Thread
> Last Format Time：10/6/2026 02:27:25

创建看这里[[15 多线程与并发]]

---
## 并发与并行
并发：在同一时刻，有多个指令在单个CPU上交替执行
并行：在同一时刻，有多个指令在多个CPU上同时执行

---
## Process
进程（Process）是计算机中的程序关于某数据集合上的一次运行活动，是系统进行==资源==分配和调度的基本单位，是操作系统结构的基础。在当代面向线程设计的计算机结构中，进程是线程的容器。程序是指令、数据及其组织形式的描述，进程是程序的实体。是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础。程序是指令、数据及其组织形式的描述，进程是程序的实体

---
## Thread
线程（thread）是操作系统能够进行==运算调度的最小单位==。它被包含在进程之中，是进程中的实际运作单位。一条线程指的是进程中一个单一顺序的控制流，一个进程中可以并发多个线程，每条线程并行执行不同的任务

### 创建线程
##### 继承 Thread 类
Thread 本身实现了 Runable 接口，本质上还是实现了实现Runable接口的，而且组合优于继承，一般是实现 Runable 接口：
```java
public class MyThread extends Thread {  
    @Override  
    public void run() {  
        for (int i = 0; i < 50; i++) {  
            System.out.println(getName() + "线程来了");  
        }  
    }
}

MyThread mt = new MyThread();  
MyThread mt2 = new MyThread();  
  
mt.setName("1");  
mt2.setName("2");  
  
mt.start();  
mt2.start();
```

##### 实现 Runable 接口
```java
public class MyThread implements Runnable {  
    @Override  
    public void run() {  
        for (int i = 0; i < 50; i++) {  
            System.out.println("线程来了");  
        }  
    }
}

Thread t = new Thread(new MyThread());  
  
t.start();
```

##### Callable 接口与 FutureTask
```java
public class MyCallable implements Callable<Integer> {  
    @Override  
    public Integer call() throws Exception {  
        return 0;  
    }  
}

MyCallable m = new MyCallable();  
FutureTask<Integer> f = new FutureTask<>(m);  
Thread t = new Thread(f);  
t.start();  
System.out.println(f.get());
```

### 成员方法
![[Pasted image 20260911003759.png]]

### sleep & wait
1. sleep 是 Thread 的静态方法，而 wait 是 Object 的方法：
```java
private static void sleepNanos(long nanos) throws InterruptedException {  
    ThreadSleepEvent event = beforeSleep(nanos);  
    try {  
        if (currentThread() instanceof VirtualThread vthread) {  
            vthread.sleepNanos(nanos);  
        } else {  
            sleepNanos0(nanos);  
        }  
    } finally {  
        afterSleep(event);  
    }  
}  
  
private static native void sleepNanos0(long nanos) throws InterruptedException;
```

```java
public final void wait(long timeoutMillis) throws InterruptedException {  
    if (timeoutMillis < 0) {  
        throw new IllegalArgumentException("timeout value is negative");  
    }  
  
    if (Thread.currentThread() instanceof VirtualThread vthread) {  
        try {  
            wait0(timeoutMillis);  
        } catch (InterruptedException e) {  
            // virtual thread's interrupt status needs to be cleared  
            vthread.getAndClearInterrupt();  
            throw e;  
        }  
    } else {  
        wait0(timeoutMillis);  
    }  
}  
```

这个方法的实现位于 JVM / 本地代码（通常是 C/C++）中，而不是 `.java` 文件中，具体怎么让线程等待，我这里不管，交给 JVM 实现

```java
// final modifier so method not in vtable  
private final native void wait0(long timeoutMillis) throws InterruptedException;
```

2. sleep ==不会释==放锁，它也不需要占用锁。wait 会释放锁，但调用它的前提是==当前线程占有这个对象的 Monitor（内置锁 / intrinsic lock 即代码要在 synchronized 中）== `wait()` 会让当前线程主动放弃 Monitor 的 Owner 身份，因此 Monitor 被释放 [[02 Synchronized]]
3. 他们都会被 interrupt 方法中断，抛出 InterruptedException
4. 带参数的 wait(Long n) 和 sleep(Long n) 进入 TIMED_WAITING（不带参数的wait进入的是WAITING状态）

### 中断
对于 `sleep()`、`wait()`、`join()` 来说，如果线程正在这些阻塞状态中，此时别人调用：
```java
thread.interrupt();
```

```text
interrupt()
   ↓
发现线程正在 sleep / wait / join
   ↓
提前结束阻塞
   ↓
抛出 InterruptedException
   ↓
interrupt 标记会被清除为 false
```

如果线程正在正常运行：
```java
thread.interrupt();
```

一般只是：
```java
isInterrupted() == true
```

线程不会停止：
```java
while (true) {
    // 还是会继续跑
}
```

需要线程自己检查：
```java
while (!Thread.currentThread().isInterrupted()) {
    // 工作
}
```

这叫**协作式中断**

```java
public void interrupt() {  
    // Setting the interrupt status must be done before reading nioBlocker.  
    interrupted = true;  
    interrupt0();  // inform VM of interrupt  
  
    // thread may be blocked in an I/O operation
    if (this != Thread.currentThread()) {  
        Interruptible blocker;  
        synchronized (interruptLock) {  
            blocker = nioBlocker;  
            if (blocker != null) {  
                blocker.interrupt(this);  
            }  
        }        
        if (blocker != null) {  
            blocker.postInterrupt();  
        }  
    }
}

public static boolean interrupted() {  
    return currentThread().getAndClearInterrupt();  
}

public boolean isInterrupted() {  
    return interrupted;  
}
```

### Two-Phase Termination 两阶段终止
![[Pasted image 20261002223149.png]]

在 Java 里通常直接利用 `interrupt()` 实现：
```java
public class TwoPhaseTermination {

    private Thread monitor;

    public void start() {
        monitor = new Thread(() -> {
            while (true) {
                Thread current = Thread.currentThread();

                // 第一阶段：检查是否收到中断请求
                if (current.isInterrupted()) {
                    System.out.println("收到终止请求");
                    // 第二阶段：进行清理
                    cleanup();
                    System.out.println("线程安全退出");
                    break;
                }

                try {
                    System.out.println("执行监控任务...");
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    /*
                     * sleep 被 interrupt 后：
                     *
                     * 1. sleep 立即结束
                     * 2. 抛 InterruptedException
                     * 3. interrupt 标记被清除为 false
                     *
                     * 所以这里必须重新设置中断标记
                     */
                    current.interrupt();
                }
            }
        });
        monitor.start();
    }

    public void stop() {
        monitor.interrupt();
    }

    private void cleanup() {
        System.out.println("保存数据...");
        System.out.println("释放资源...");
    }
}
```

### 启动
在启动的时候，我们使用 run() 方法是不会启动线程的，执行方法的依旧是主线程，正确的是调用 start()：
```java
public class MyThread extends Thread {  
    public MyThread() {  
    }  
    public MyThread(String name) {  
        super(name);  
    }  
	
    @Override  
    public void run() {  
        for (int i = 0; i < 50; i++) {  
            try {  
                Thread.sleep(1000);  
            } catch (InterruptedException e) {  
                throw new RuntimeException(e);  
            }  
            System.out.println(getName() + "shit");  
        }  
    }
}

MyThread mt = new MyThread("1");  
MyThread mt2 = new MyThread("2");  
```

看源码就知道 start() 调用了原生方法 start0()和[[01 Process & Thread]]中的 wait0() 一样的

```java
mt.start();  
mt2.start();  
  
System.out.println(Thread.currentThread());
```

### 线程状态
[[06 线程状态转换]]
![[Pasted image 20261003183241.png]]

- NEW 线程刚被创建，但是还没有调用 start() 方法 
- RUNNABLE 当调用了 start() 方法之后，注意，Java API 层面的 RUNNABLE 状态涵盖了 操作系统 层面的 【可运行状态】、【运行状态】和【阻塞状态】（由于 BIO 导致的线程阻塞，在 Java 里无法区分，仍然认为 是可运行） 
- BLOCKED ， WAITING ， TIMED_WAITING 都是 Java API 层面对【阻塞状态】的细分
- TERMINATED 当线程代码运行结束

仔细看，没有运行运行状态交由操作系统，所以没有定义：
```java
public enum State {
        /**
         * Thread state for a thread which has not yet started.
         */
        NEW,

        /**
         * Thread state for a runnable thread.  A thread in the runnable
         * state is executing in the Java virtual machine but it may
         * be waiting for other resources from the operating system
         * such as processor.
         */
        RUNNABLE,

        /**
         * Thread state for a thread blocked waiting for a monitor lock.
         * A thread in the blocked state is waiting for a monitor lock
         * to enter a synchronized block/method or
         * reenter a synchronized block/method after calling
         * {@link Object#wait() Object.wait}.
         */
        BLOCKED,

        /**
         * Thread state for a waiting thread.
         * A thread is in the waiting state due to calling one of the
         * following methods:
         * <ul>
         *   <li>{@link Object#wait() Object.wait} with no timeout</li>
         *   <li>{@link #join() Thread.join} with no timeout</li>
         *   <li>{@link LockSupport#park() LockSupport.park}</li>
         * </ul>
         *
         * <p>A thread in the waiting state is waiting for another thread to
         * perform a particular action.
         *
         * For example, a thread that has called {@code Object.wait()}
         * on an object is waiting for another thread to call
         * {@code Object.notify()} or {@code Object.notifyAll()} on
         * that object. A thread that has called {@code Thread.join()}
         * is waiting for a specified thread to terminate.
         */
        WAITING,

        /**
         * Thread state for a waiting thread with a specified waiting time.
         * A thread is in the timed waiting state due to calling one of
         * the following methods with a specified positive waiting time:
         * <ul>
         *   <li>{@link #sleep Thread.sleep}</li>
         *   <li>{@link Object#wait(long) Object.wait} with timeout</li>
         *   <li>{@link #join(long) Thread.join} with timeout</li>
         *   <li>{@link LockSupport#parkNanos LockSupport.parkNanos}</li>
         *   <li>{@link LockSupport#parkUntil LockSupport.parkUntil}</li>
         * </ul>
         */
        TIMED_WAITING,

        /**
         * Thread state for a terminated thread.
         * The thread has completed execution.
         */
        TERMINATED;
    }
```

### 用户线程与守护线程
JVM 在没有用户线程存活的时候就会退出，用户线程结束后，守护线程自动释放

默认情况下，Java进程需要等待所有线程都运行结束，才会结束。有一种特殊的线程叫做守护线程，只要其它非守护线程运行结束了，即使守护线程的代码没有执行完，也会强制结束

垃圾回收器就是一种守护线程
### 优先级
设置了不一定执行，看任务调度的情况

### 礼让线程
调用 yield() 不一定会让出，看任务调度的情况

### 插入线程
join() 底层就是 wait()：
```java
public final void join(long millis) throws InterruptedException {  
    if (millis < 0)  
        throw new IllegalArgumentException("timeout value is negative");  
  
    if (this instanceof VirtualThread vthread) {  
        if (isAlive()) {  
            long nanos = MILLISECONDS.toNanos(millis);  
            vthread.joinNanos(nanos);  
        }  
        return;  
    }  
  
    synchronized (this) {  
        if (millis > 0) {  
            if (isAlive()) {  
                final long startTime = System.nanoTime();  
                long delay = millis;  
                do {  
                    wait(delay);  
                } while (isAlive() && (delay = millis -  
                         NANOSECONDS.toMillis(System.nanoTime() - startTime)) > 0);  
            }  
        } else {  
            while (isAlive()) {  
                wait(0);  
            }  
        }    
	}
}
```

等待 join() 线程执行结束，才会继续本线程的执行，这个不看任务调度的情况，类似于前端的 await，将线程间的关系变成了同步

需要等待结果返回，才能继续运行就是同步
不需要等待结果返回，就能继续运行就是异步

join(Long n) 显示等待



