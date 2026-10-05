# 12 AQS
> Last Format Time：10/6/2026 02:27:25

抽象队列同步器，一个类，锁可以通过继承他来实现

AQS = 状态变量 + 等待队列 + CAS + 线程阻塞/唤醒，组成的一套同步器框架

可以记成：
```text
AQS
├── state       条件变量 / 同步状态，类似于 Monitor 的 WaitSet
├── FIFO 队列   排队等待的线程，类似于 EntryList
└── CAS         修改 state
```

利用 AQS 实现一个 Lock 是很简单的：
```java 
/**  
 * 非可重入  
 */  
public class MyLock implements Lock {  
  
    class MySync extends AbstractQueuedSynchronizer {  
  
        @Override  
        protected boolean tryAcquire(int arg) {  
            if (compareAndSetState(0, 1)) {  
                // 加锁，并设置当前线程运行  
                setExclusiveOwnerThread(Thread.currentThread());  
                return true;
            }  
            return false;  
        }  
  
        @Override  
        protected boolean tryRelease(int arg) {  
            setExclusiveOwnerThread(null);  
```

这里和 volatile 有关，我没看懂  

```java
            setState(0);  
            return true;  
        }  
  
        @Override  
        protected boolean isHeldExclusively() {  
            return getState() == 1;  
        }  
  
        // 由 AQS 提供  
        public Condition newCondition() {  
            return new ConditionObject();  
        }  
    }  
    private MySync sync = new MySync();  
  
    /**  
     * 加锁  
     */  
    @Override  
    public void lock() {  
        sync.acquire(1);  
    }  
  
    /**  
     * 加锁，可打断  
     */  
    @Override  
    public void lockInterruptibly() throws InterruptedException {  
        sync.acquireInterruptibly(1);  
    }  
  
    /**  
     * 加锁，尝试一次  
     */  
    @Override  
    public boolean tryLock() {  
        return sync.tryAcquire(1);  
    }  
  
    /**  
     * 加锁，带超时  
     */  
    @Override  
    public boolean tryLock(long time, TimeUnit unit) throws InterruptedException {  
        return sync.tryAcquireNanos(1, unit.toNanos(time));  
    }  
  
    /**  
     * 解锁  
     */  
    @Override  
    public void unlock() {  
        sync.release(1);  
    }  
  
    /**  
     * 创建条件变量  
     */  
    @Override  
    public Condition newCondition() {  
        return sync.newCondition();  
    }  
}
```

