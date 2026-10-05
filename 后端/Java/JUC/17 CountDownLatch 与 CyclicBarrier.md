# 17 CountDownLatch 与 CyclicBarrier
> Last Format Time：10/6/2026 02:27:25

---
## CountDownLatch
用来进行线程同步协作，等待所有线程完成倒计时。
其中构造参数用来初始化等待计数值，await() 用来等待计数归零，countDown() 用来让计数减一
![[Pasted image 20261005214913.png]]

与 Join() 的作用很像，但是在线程池中，他的效果更好


---
## CyclicBarrier
循环栅栏，用来进行线程协作，等待线程满足某个计数。构造时设置计数个数，每个线程调用 await() 方法进行等待，当等待的线程数满足计数个数时，继续执行
![[Pasted image 20261005221544.png]]

