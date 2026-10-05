# 08 ReentrantLock
> Last Format Time：10/6/2026 02:27:25

[[05 Lock 锁]]

![[Pasted image 20261005174541.png]]

基本使用：
```java
Lock l = ...;
l.lock(); // lock() as the last statement before the try block
try {
	// access the resource protected by this lock
} finally {
	l.unlock(); // unlock() as the first statement in the finally block
}
```

---
## 可重入
可重入锁：==同一个线程==已经获得某把锁之后，在还没有释放这把锁的情况下，可以再次获取同一把锁，而不会把自己阻塞住
在外层函数获取到该锁之后，内存的递归函数仍可以继续获取该锁，也可以叫递归锁

Java 里的 `synchronized` 和 `ReentrantLock` 都是可重入锁

---
## 可中断
其中：
```text
等待 synchronized 锁             ❌ 不可中断
等待 lock.lock()                 ❌ 不可中断
等待 lock.lockInterruptibly()    ✅ 可中断
sleep()                         ✅ 可中断
wait()                          ✅ 可中断
join()                          ✅ 可中断
```

那说白了，所有的锁不都是可中断的：
![[Pasted image 20261003193451.png]]

synchronized 已经获得锁后==其他线程==无法去中断这个锁，这里说的可中断指的是在等待锁的阻塞状态是可以通过方法中断的


---
## 公平锁
先阻塞先得到，一般不用
非公平锁，在等待队列链表中的线程还是公平的，非公平指的是有新的线程来的时候，在等待队列中排队第一的线程和当前的线程去竞争，而不是让当前线程直接去队尾

---
## Condition
与 wait 类似：
```java
Lock lock = new ReentrantLock();  
Condition condition = lock.newCondition();  
Condition condition1 = lock.newCondition();  

// 先加锁
lock.lock();  
try {  
    // 进入 
    Condition1condition1.await();  
} catch (InterruptedException e) {  
    throw new RuntimeException(e);  
}  

condition1.signal();  
condition1.signalAll();
```


---
## ReentrantReadWriteLock
读写锁
![[Pasted image 20261005181207.png]]
![[Pasted image 20261005181220.png]]

多个线程都想要获取读锁，是不会阻塞住的
如果一个想要读锁，一个写锁，就是互斥的了
两个读锁一样的，互斥

这样实际就是将一部分互斥的情况转化成了读读并发的情况，提高了效率同时保证了线程安全

```java
/**
 * {@code Lock} implementations provide more extensive locking
 * operations than can be obtained using {@code synchronized} methods
 * and statements.  They allow more flexible structuring, may have
 * quite different properties, and may support multiple associated
 * {@link Condition} objects.
 *
 * <p>A lock is a tool for controlling access to a shared resource by
 * multiple threads. Commonly, a lock provides exclusive access to a
 * shared resource: only one thread at a time can acquire the lock and
 * all access to the shared resource requires that the lock be
 * acquired first. However, some locks may allow concurrent access to
 * a shared resource, such as the read lock of a {@link ReadWriteLock}.
 *
 * <p>The use of {@code synchronized} methods or statements provides
 * access to the implicit monitor lock associated with every object, but
 * forces all lock acquisition and release to occur in a block-structured way:
 * when multiple locks are acquired they must be released in the opposite
 * order, and all locks must be released in the same lexical scope in which
 * they were acquired.
 *
 * <p>While the scoping mechanism for {@code synchronized} methods
 * and statements makes it much easier to program with monitor locks,
 * and helps avoid many common programming errors involving locks,
 * there are occasions where you need to work with locks in a more
 * flexible way. For example, some algorithms for traversing
 * concurrently accessed data structures require the use of
 * &quot;hand-over-hand&quot; or &quot;chain locking&quot;: you
 * acquire the lock of node A, then node B, then release A and acquire
 * C, then release B and acquire D and so on.  Implementations of the
 * {@code Lock} interface enable the use of such techniques by
 * allowing a lock to be acquired and released in different scopes,
 * and allowing multiple locks to be acquired and released in any
 * order.
 *
 * <p>With this increased flexibility comes additional
 * responsibility. The absence of block-structured locking removes the
 * automatic release of locks that occurs with {@code synchronized}
 * methods and statements. In most cases, the following idiom
 * should be used:
 *
 * <pre> {@code
 * Lock l = ...;
 * l.lock(); // lock() as the last statement before the try block
 * try {
 *   // access the resource protected by this lock
 * } finally {
 *   l.unlock(); // unlock() as the first statement in the finally block
 * }}</pre>
 *
 * When locking and unlocking occur in different scopes, care must be
 * taken to ensure that all code that is executed while the lock is
 * held is protected by try-finally or try-catch to ensure that the
 * lock is released when necessary.
 *
 * <p>{@code Lock} implementations provide additional functionality
 * over the use of {@code synchronized} methods and statements by
 * providing a non-blocking attempt to acquire a lock ({@link
 * #tryLock()}), an attempt to acquire the lock that can be
 * interrupted ({@link #lockInterruptibly}, and an attempt to acquire
 * the lock that can timeout ({@link #tryLock(long, TimeUnit)}).
 *
 * <p>A {@code Lock} class can also provide behavior and semantics
 * that is quite different from that of the implicit monitor lock,
 * such as guaranteed ordering, non-reentrant usage, or deadlock
 * detection. If an implementation provides such specialized semantics
 * then the implementation must document those semantics.
 *
 * <p>Note that {@code Lock} instances are just normal objects and can
 * themselves be used as the target in a {@code synchronized} statement.
 * Acquiring the
 * monitor lock of a {@code Lock} instance has no specified relationship
 * with invoking any of the {@link #lock} methods of that instance.
 * It is recommended that to avoid confusion you never use {@code Lock}
 * instances in this way, except within their own implementation.
 *
 * <p>Except where noted, passing a {@code null} value for any
 * parameter will result in a {@link NullPointerException} being
 * thrown.
 *
 * <h2>Memory Synchronization</h2>
 *
 * <p>All {@code Lock} implementations <em>must</em> enforce the same
 * memory synchronization semantics as provided by the built-in monitor
 * lock, as described in
 * Chapter 17 of
 * <cite>The Java Language Specification</cite>:
 * <ul>
 * <li>A successful {@code lock} operation has the same memory
 * synchronization effects as a successful <em>Lock</em> action.
 * <li>A successful {@code unlock} operation has the same
 * memory synchronization effects as a successful <em>Unlock</em> action.
 * </ul>
 *
 * Unsuccessful locking and unlocking operations, and reentrant
 * locking/unlocking operations, do not require any memory
 * synchronization effects.
 *
 * <h2>Implementation Considerations</h2>
 *
 * <p>The three forms of lock acquisition (interruptible,
 * non-interruptible, and timed) may differ in their performance
 * characteristics, ordering guarantees, or other implementation
 * qualities.  Further, the ability to interrupt the <em>ongoing</em>
 * acquisition of a lock may not be available in a given {@code Lock}
 * class.  Consequently, an implementation is not required to define
 * exactly the same guarantees or semantics for all three forms of
 * lock acquisition, nor is it required to support interruption of an
 * ongoing lock acquisition.  An implementation is required to clearly
 * document the semantics and guarantees provided by each of the
 * locking methods. It must also obey the interruption semantics as
 * defined in this interface, to the extent that interruption of lock
 * acquisition is supported: which is either totally, or only on
 * method entry.
 *
 * <p>As interruption generally implies cancellation, and checks for
 * interruption are often infrequent, an implementation can favor responding
 * to an interrupt over normal method return. This is true even if it can be
 * shown that the interrupt occurred after another action may have unblocked
 * the thread. An implementation should document this behavior.
 *
 * @see ReentrantLock
 * @see Condition
 * @see ReadWriteLock
 * @jls 17.4 Memory Model
 *
 * @since 1.5
 * @author Doug Lea
 */
```
