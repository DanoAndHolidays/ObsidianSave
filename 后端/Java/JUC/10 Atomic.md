# 10 Atomic
> Last Format Time：10/6/2026 02:27:25

底层是 CAS 的循环

---
## AtomicBoolean、AtomicInteger 与 AtomicLong
这些方法保证是原子性的：
![[Pasted image 20261004205602.png]]


---
## 原子引用类型
AtomicReference、AtomicMarkableReference、AtomicStampedReference
### AtomicReference
![[Pasted image 20261004211654.png]]
![[Pasted image 20261004211708.png]]

### AtomicStampedReference
只要有其它线程修改过共享变量（ABA 问题），那么自己的 CAS 就算失败：
![[Pasted image 20261004213044.png]]

### AtomicMarkableReference
但是有时候，并不关心引用变量更改了几次，只是单纯的关心是否更改过
![[Pasted image 20261004213304.png]]

---
## 原子数组
### AtomicIntegerArray AtomicLongArray
保护数组中的项的线程安全性
### AtomicReferenceArray
---
## 字段更新器
AtomicIntegerFieldUpdater 
AtomicLongFieldUpdater
AtomicReferenceFieldUpdater
![[Pasted image 20261004214956.png]]
![[Pasted image 20261004215007.png]]

---
## 原子累加器
LongAdder，他的性能更优
