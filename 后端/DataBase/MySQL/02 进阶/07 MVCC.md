# 07 MVCC
> Last Format Time：10/7/2026 22:01:26

Multi-Version ConcurrencyControl，多版本并发控制

指维护一个数据的多个版本，使得读写操作没有冲突，快照读为MySQL实现

实现原理主要是==隐藏字段==，==undo log==，==Read View== 来实现的


---
## 隐藏字段
InnoDB 存储引擎，数据库中的==聚簇索引==每行数据，除了自定义的字段，还有数据库隐式定义的字段：

* DB_TRX_ID：最近修改事务 ID，记录创建该数据或最后一次修改该数据的事务 ID
* DB_ROLL_PTR：回滚指针，指向记录对应的 undo log 日志
* DB_ROW_ID：如果数据表没有主键，InnoDB 会自动以 DB_ROW_ID 作为聚簇索引

![](https://seazean.oss-cn-beijing.aliyuncs.com/img/DB/MySQL-MVCC版本链隐藏字段.png)

---
## 版本链
undo log 是==逻辑日志==，记录的是每个事务对数据执行的操作，而不是记录的全部数据，要**根据 undo log 逆推出以往事务的数据**

undo log 的作用：

* 保证事务进行 rollback 时的原子性和一致性，当事务进行回滚的时候可以用 undo log 的数据进行恢复
* 用于 MVCC 快照读，通过读取 undo log 的历史版本数据可以实现不同事务版本号都拥有自己独立的快照数据

undo log 主要分为两种：

* insert undo log：事务在 insert 新记录时产生的 undo log，只在事务回滚时需要，并且在事务提交后可以被立即丢弃

* update undo log：事务在进行 update 或 delete 时产生的 undo log，在事务回滚时需要，在快照读时也需要。不能随意删除，只有在当前读或事务回滚不涉及该日志时，对应的日志才会被 purge 线程统一清除

每次对数据库记录进行改动，都会产生的新版本的 undo log，随着更新次数的增多，所有的版本都会被 roll_pointer 属性连接成一个链表，把这个链表称之为**版本链**，版本链的头节点就是当前的最新的 undo log，链尾就是最早的旧 undo log

说明：因为 DELETE 删除记录，都是移动到垃圾链表中，不是真正的删除，所以才可以通过版本链访问原始数据

<img src="https://seazean.oss-cn-beijing.aliyuncs.com/img/DB/MySQL-MVCC版本链.png" style="zoom: 80%;" />

注意：undo 是==逻辑==日志，这里只是直观的展示出来

工作流程：

* 有个事务插入 persion 表一条新记录，name 为 Jerry，age 为 24

* 事务 1 修改该行数据时，数据库会先对该行加排他锁，然后先记录 undo log，然后修改该行 name 为 Tom，并且修改隐藏字段的事务 ID 为当前事务 1 的 ID（默认为 1 之后递增），回滚指针指向拷贝到 undo log 的副本记录，事务提交后，释放锁

* 以此类推

---
## 读视图
Read View 是事务进行读数据操作时产生的读视图，该事务执行快照读的那一刻会生成数据库系统当前的一个快照，记录并维护系统当前==活跃事务的 ID==，用来做可见性判断，根据视图判断当前事务能够看到哪个版本的数据

注意：这里的快照并不是把所有的数据拷贝一份副本，而是由 ==undo log== 记录的逻辑日志，根据库中的数据进行==计算出==历史==数据==

工作流程：

将版本链的头节点的事务 ID（最新数据事务 ID，大概率不是当前线程）DB_TRX_ID 取出来，与系统当前活跃事务的 ID 对比进行==可见性分析==

不可见就通过 DB_ROLL_PTR 回滚指针去取出 undo log 中的==下一个 DB_TRX_ID== 比较，直到找到最近的满足可见性的 DB_TRX_ID，该事务 ID 所在的旧记录就是当前事务能看见的最新的记录


- Read View 几个属性：
	
	- m_ids：生成 Read View 时当前系统中活跃的事务 id 列表（未提交的事务集合，当前事务也在其中）
	- min_trx_id：生成 Read View 时当前系统中活跃的最小的事务 id，也就是 m_ids 中的最小值（已提交的事务集合）
	- max_trx_id：生成 Read View 时当前系统应该分配给下一个事务的 id 值，m_ids 中的最大值加 1（未开始事务）
	- creator_trx_id：生成该 Read View 的事务的事务 id，就是判断该 id 的事务能读到什么数据


- creator 创建一个 Read View，进行可见性分析：（解决了读未提交）
	
	*  db_trx_id == creator_trx_id：表示这个数据就是当前事务自己生成的，自己生成的数据自己肯定能看见，所以此数据对 creator 是可见的
	
	*  db_trx_id <  min_trx_id：该版本对应的事务 ID 小于 Read view 中的最小活跃事务 ID，则这个事务在当前事务之前就已经被提交了，对 creator 可见（因为比已提交的最大事务 ID 小的并不一定已经提交，所以应该判断是否在活跃事务列表）
	
	*  db_trx_id >= max_trx_id：该版本对应的事务 ID 大于 Read view 中当前系统的最大事务 ID，则说明该数据是在当前 Read view 创建之后才产生的，对 creator 不可见
	
	*  min_trx_id <= db_trx_id <= max_trx_id：判断 db_trx_id 是否在活跃事务列表 m_ids 中
		
		* 在列表中，说明该版本对应的事务正在运行，数据不能显示（**不能读到未提交的数据**）
		* 不在列表中，说明该版本对应的事务已经被提交，数据可以显示（**可以读到已经提交的数据**）

##### RC RR
Read View 用于支持 RC（Read Committed，读已提交）和 RR（Repeatable Read，可重复读）隔离级别的实现，所以 **SELECT 在 RC 和 RR 隔离级别使用 MVCC 读取记录**

RR、RC 生成时机：

- RC 隔离级别下，每次读取数据前都会生成最新的 Read View（当前读）
- RR 隔离级别下，在第一次数据读取时才会创建 Read View（快照读）

RC、RR 级别下的 InnoDB 快照读区别

- RC 级别下，事务中每次快照读都会新生成一个 Read View，这就是在 RC 级别下的事务中可以看到别的事务提交的更新的原因

- RR 级别下，某个事务的对某条记录的**第一次快照读**会创建一个 Read View，将当前系统活跃的其他事务记录起来，此后在调用快照读的时候，使用的是同一个 Read View，所以一个事务的查询结果每次都是相同的

  RR 级别下，通过 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 开启事务，会在执行该语句后立刻生成一个 Read View，不是在执行第一条 SELECT 语句时生成（所以说 `START TRANSACTION` 并不是事务的起点，执行第一条语句才算起点）

##### 当前读
读取的是记录的最新版本，读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁

对于我们日常的操作，如：select .. lock in share mode（共享锁）， select ... for update、update、insert、delete（排他锁）都是—种当前读

线程 1 开事务，去读一个数据，此时线程 2 也开一个事务去更新这个数据并提交事务，此时线程 1 读到的数据依旧是之前旧的，不是最新的已提交数据（避免了不可重复读），但是我们加上共享锁就可以读到最新的，这就是当前读

##### 快照读
简单的 select（不加锁）就是快照读，读取的是记录数据的可见版本，有可能是历史数据，不加锁，是非阻塞读。

- Read Committed：每次select，都生成—个快照读
- Repeatable Read：开启事务后第一个 select 语句才是快照读的地方，之后再读就去复用读视图，所以可以读到的数据的版本是一样的
- Serializable：快照读会退化为当前读
