# 05 Park
> Last Format Time：10/6/2026 02:27:25

线程状态是 WAITTING

```java
LockSupport.park();
```

```java
LockSupport.unpark(thread);
```

unpark 可以在 park 前调用，park / unpark 不必配合 Monitor