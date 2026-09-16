# 05 Scheduler 与 Reconciler：并发渲染工作循环
> Last Format Time：9/16/2026 19:24:52

> Last Format Time：2026-08-28
> Status：进行中
> 笔记说明：从 pendingLanes、root scheduling 到 workLoopConcurrent，串起 Scheduler 与 Reconciler 的边界。

---
## 当前学习位置
React 内部机制目前约 **80%**。

已经打通的主链：

```text
setState
↓
Update
↓
Lane
↓
Hook / Update Queue
↓
FiberRoot.pendingLanes
↓
ensureRootIsScheduled
↓
getNextLanes
↓
Scheduler Task
↓
Host Callback
↓
performConcurrentWorkOnRoot
↓
renderRootConcurrent
↓
workLoopConcurrent
↓
performUnitOfWork
↓
beginWork / completeWork
↓
finishedWork
↓
commitRoot
```

目前已经基本理解：

- Fiber 为什么支持可中断工作
    
- sync / concurrent work loop
    
- `shouldYield`
    
- pause / resume
    
- interrupt / restart
    
- Scheduler 与 FiberRoot 如何连接
    
- Scheduler 如何通过宿主环境重新获得执行机会
    
- Transition 被高优先级工作抢占时发生什么
    



需要区分两个东西。

### work-in-progress tree
正在构建的整棵 candidate Fiber Tree（候选 Fiber 树）。

### `workInProgress`
当前遍历位置的指针：

```text
App
├─ Header ✅
└─ Main ✅
   └─ List ✅
      ├─ A ✅
      ├─ B ✅
      └─ C ← workInProgress
```

可以理解成：

> React 当前做到哪里了。

它直接指向一个 Fiber，而不是简单保存：

```text
index = 37
```

Fiber 自己通过：

```text
child
sibling
return
```

记录遍历关系，因此 React 知道下一步该去哪。

---
## `performUnitOfWork`
可以简单理解为：

> 推进一个 Fiber 工作单元。

```js
performUnitOfWork(workInProgress)
```

过程中主要涉及：

```text
beginWork
↓
向下处理 Fiber

completeWork
↓
向上完成 Fiber
```

---
## `beginWork` 与 `completeWork`
### beginWork
可以理解成：

> 进入这个 Fiber，计算它下一步应该长什么样。

例如函数组件：

```text
执行 Component()
↓
得到 children
↓
reconciliation
↓
创建 / 复用 child Fiber
```


### completeWork
当一个 Fiber 的子树处理完：

> 开始收尾，并向父节点汇总结果。

例如：

```text
begin App
  begin List
    begin Item
    complete Item
  complete List
complete App
```

这也解释了为什么诸如：

```text
subtreeFlags
```

这样的信息可以从子节点向父节点聚合。

---
## `workLoopSync`
同步模式非常简单：

```js
while (workInProgress !== null) {
  performUnitOfWork(workInProgress)
}
```

也就是：

> 有活就一直做，直到整棵树完成。

不会主动问浏览器：

> 我是不是该停一下？

---
## `workLoopConcurrent`
Concurrent Render（并发渲染）多了一个判断：

```js
while (
  workInProgress !== null &&
  !shouldYield()
) {
  performUnitOfWork(workInProgress)
}
```

所以：

```text
处理 Fiber
↓
处理 Fiber
↓
处理 Fiber
↓
shouldYield?
```

如果：

```text
false
```

继续。

如果：

```text
true
```

退出当前 work loop。

---
## `shouldYield`
`shouldYield()` 的核心问题是：

> React 这一轮占用主线程够久了吗？

不是：

> 有没有更高优先级 Lane？

所以要区分：

```text
Lane / getNextLanes
→ 决定做谁

shouldYield
→ 决定还能做多久
```

这是 Scheduler 部分非常重要的 mental model（心智模型）。

---
## Concurrent 并不是多线程
Concurrent Rendering 不是：

```text
Thread A → React
Thread B → Browser
```

而是在一个主线程上交错执行：

```text
React ███
Browser █
React ███
Browser █
React ███
```

所以更准确的概念是：

> interleaving（交错执行）

而不是：

> parallelism（并行执行）。

---
## Fiber 为什么能暂停
普通递归依赖：

```text
JavaScript Call Stack
```

保存：

```text
现在在哪
从谁进来的
处理完回哪
```

一旦调用栈退出，这些上下文就没了。

Fiber 把它们显式保存：

```text
child
sibling
return
```

再通过：

```text
workInProgress
```

保存当前工作位置。

因此 JS 调用栈可以退出：

```text
React return
↓
浏览器获得主线程
```

但 React 的工作现场仍然存在。

---
## pause / resume
假设：

```text
A ✅
B ✅
C ← workInProgress
D
E
```

此时：

```text
shouldYield() === true
```

React 停下来。

但：

```text
WIP Tree
+
workInProgress
```

仍然存在。

下一次 Scheduler 再给执行机会：

```text
C
↓
D
↓
E
```

继续。

这就是：

```text
pause → resume
```

### 核心
pause：

> 工作没变，只是暂时不做。

resume：

> 继续原来的 WIP。

---
## interrupt
假设当前正在做：

```text
TransitionLane
```

然后来了更高优先级更新。

Root：

```text
pendingLanes

UrgentLane
+
TransitionLane
```

重新：

```text
getNextLanes(root)
```

得到：

```text
UrgentLane
```

于是：

> 当前低优先级 Transition 不再是最值得继续做的事情。

这就是 interrupt（中断 / 抢占）。

---
## restart
interrupt 之后不代表旧工作一定能继续。

如果 React 再回来时发现：

```text
旧 render 条件
!=
当前需要 render 的条件
```

那么旧 WIP 不能直接 resume。

需要：

```text
prepareFreshStack
↓
重新从 root 开始
```

这就是 restart。

所以：

```text
pause
→ 工作没变

resume
→ 继续旧工作

interrupt
→ 更高优先级工作抢占

restart
→ 旧 render progress 已经不能继续使用
```

---
## yield ≠ interrupt
这是容易混淆的地方。

### yield
通常是：

```text
时间片到了
↓
主动让出主线程
```

并不意味着当前 render 作废。

更接近：

```text
pause → resume
```


### interrupt
通常是：

```text
更高优先级工作来了
↓
当前低优先级工作不再继续
```

之后旧工作可能需要：

```text
restart
```

---
## `pendingLanes` 与 `renderLanes`
### `root.pendingLanes`
表示：

> Root 上所有尚未完成的工作。

例如：

```text
UrgentLane
+
TransitionLane
```

### `renderLanes`
表示：

> 当前这一轮 render 正在处理哪批工作。

例如：

```text
renderLanes = TransitionLane
```

如果这时：

```text
getNextLanes(root)
```

重新选择出了：

```text
UrgentLane
```

说明：

```text
当前正在做的
TransitionLane

现在更应该做的
UrgentLane
```

已经不同。

这就可能触发抢占。

---
## `ensureRootIsScheduled`
可以理解成：

> FiberRoot 的排班员。

它不是直接 render。

主要负责确认：

```text
Root 有没有工作？
↓
最高优先级是什么？
↓
现在已有 Scheduler callback 吗？
↓
这个 callback 的优先级还合适吗？
↓
是否需要重新安排？
```

因此：

```text
FiberRoot.pendingLanes
↓
ensureRootIsScheduled
↓
getNextLanes
↓
Scheduler Priority
↓
scheduleCallback
```

它是：

> FiberRoot → Scheduler

之间的重要桥梁。

---
## Lane Priority 与 Scheduler Priority
两者不要直接视为同一个东西。

### Lane
属于 React 更新系统：

> 哪批 Update 应该一起处理、优先级如何。

### Scheduler Priority
属于 Scheduler：

> Scheduler 里的这个 Task 有多紧急。

因此中间存在：

```text
Lane Priority
↓
映射
↓
Scheduler Priority
```

---
## Scheduler Task
`scheduleCallback` 不是：

```js
callback()
```

而是：

> 把 callback 作为 Task 安排进 Scheduler。

可以简单理解：

```text
Task {
  priority
  callback
  expirationTime
}
```

Scheduler 内部维护：

```text
taskQueue
```

然后选择合适的 Task 执行。

---
## Host Callback / MessageChannel
Scheduler 自己也是 JavaScript。

所以它需要依赖浏览器：

> 未来再给我一次 JavaScript 执行机会。

概念上：

```text
Scheduler 有任务
↓
请求 host callback
↓
MessageChannel 等宿主机制
↓
当前 JS 结束
↓
浏览器重新获得控制权
↓
未来再执行 Scheduler
```

`MessageChannel` 可以理解成：

> 请求浏览器稍后尽快再执行一次 JS。

它不是多线程。

---
## `performConcurrentWorkOnRoot`
Scheduler 真正执行 React Task 后，会进入类似：

```text
performConcurrentWorkOnRoot
```

这可以理解为：

> Scheduler 把执行权重新交回 React Root。

主链：

```text
Scheduler Task
↓
performConcurrentWorkOnRoot
↓
getNextLanes
↓
renderRootConcurrent
↓
workLoopConcurrent
```

---
## 为什么又要 `getNextLanes`
安排 Task 时已经：

```text
getNextLanes
```

执行 Task 时可能还会重新判断。

原因是：

```text
Task 被安排
↓
过了一段时间
↓
Task 真正执行
```

中间可能来了新的 Update。

例如安排时：

```text
Transition
```

执行时：

```text
Urgent + Transition
```

所以不能相信之前的判断。

要重新问：

> 现在真正应该做谁？

---
## Scheduler 的最小职责
现在可以简单总结为三件事：

```text
1. 保存任务
   scheduleCallback → taskQueue

2. 请求执行机会
   host callback / MessageChannel

3. 控制一轮执行时间
   shouldYield
```

所以：

> Scheduler 负责的是“什么时候做、一次做多久”。

Reconciler 才负责：

> “具体怎么算 Fiber”。

---
## `startTransition + BigList` 完整案例
```jsx
setInput(value)

startTransition(() => {
  setQuery(value)
})
```

产生：

```text
setInput
→ urgent update

setQuery
→ transition update
```

Root：

```text
pendingLanes
=
Urgent
+
Transition
```

React 首先：

```text
getNextLanes
↓
Urgent
```

于是 input 可以先：

```text
render
↓
commit
```

用户马上看到最新输入。

Transition 仍然 pending：

```text
BigList(query)
```

然后：

```text
Scheduler
↓
renderRootConcurrent
↓
BigList concurrent render
```

---
## BigList 可以 yield
例如：

```text
Item 1 ✅
Item 2 ✅
...
Item 500 ✅
Item 501 ← workInProgress
```

时间片到了：

```text
shouldYield = true
```

于是：

```text
pause
↓
browser
↓
Scheduler 再回来
↓
resume
```

而屏幕上始终还是：

```text
current tree
```

未完成的 WIP 用户看不到。

---
## 用户继续输入时发生什么
假设正在 render：

```text
query = "a"
```

只算到：

```text
Item 500
```

用户已经输入：

```text
"ab"
```

出现新的 urgent update。

旧 Transition：

```text
query = "a"
```

就可能被 interrupt。

新的 input 更新可以先：

```text
render
↓
commit
```

然后 React 再处理：

```text
query = "ab"
```

旧的 `"a"` candidate 甚至可能：

> 从来没有 commit 过。

所以：

```text
render ≠ commit
```

React 完全可能：

```text
current A
↓
render B
↓
B 做了一半
↓
放弃 B
↓
render C
↓
commit C
```

用户从来没有看到 B。

---
## 旧 Transition 的 WIP 去哪里了？
假设：

```text
query = "a"

Item1 ✅
Item2 ✅
Item3 ✅
Item4 ←
```

后来目标变成：

```text
query = "ab"
```

那么旧的部分 WIP：

```text
Item1~3
```

是按照：

```text
query = "a"
```

算出来的。

不能简单继续：

```text
Item4 → query = "ab"
```

否则一棵 candidate tree 内会混入两个不同 render 条件的计算结果。

所以 restart 时：

> 旧 partial render result（部分渲染结果）的逻辑有效性被丢弃。

---
## 但 Fiber 对象不一定被销毁
这里要区分：

```text
render result
```

和：

```text
Fiber object
```

旧 WIP 被放弃意味着：

```text
旧 candidate result
旧 render progress
```

作废。

不代表：

```text
Fiber 对象全部 delete
↓
立刻 GC
```

React 有：

```text
current Fiber
     ↕
 alternate
     ↕
WIP Fiber
```

机制。

下一轮：

```text
createWorkInProgress(current)
```

可能直接拿已有：

```text
current.alternate
```

重新使用。

所以更准确地说：

```text
丢弃：
旧 WIP 的计算结果 / 有效进度

不一定丢弃：
Fiber Object 本身
```

类比：

> 擦掉草稿重新写，而不是把草稿本扔掉。

---
## 最终职责划分
现在整个体系可以压缩成：

### Fiber

> 工作单元。

### `workInProgress`

> 当前做到哪。

### WIP Tree

> 正在构建的 candidate UI。

### Lane

> Update 属于哪批工作、优先级如何。

### `getNextLanes`

> 当前应该先做哪批工作。

### FiberRoot

> 整个 Root 工作状态的控制中心。

### `ensureRootIsScheduled`

> 确保 Root 当前 Scheduler 安排正确。

### Scheduler

> 什么时候执行、一次执行多久。

### `performConcurrentWorkOnRoot`

> Scheduler 回到 React 的入口。

### `workLoopConcurrent`

> 不断推进 Fiber work。

### `shouldYield`

> 当前该不该把主线程还给浏览器。

### `commitRoot`

> candidate 已经完整，可以真正对外生效。

---
## 当前最重要的完整 mental model
```text
Update
↓
Lane
↓
FiberRoot.pendingLanes
↓
getNextLanes
↓
ensureRootIsScheduled
↓
Scheduler Task
↓
Host Callback
↓
performConcurrentWorkOnRoot
↓
renderRootConcurrent
↓
workLoopConcurrent
↓
performUnitOfWork
↓
beginWork / completeWork
↓
shouldYield
│
├─ true
│   ↓
│ pause
│   ↓
│ resume / 或被高优先级 interrupt
│
└─ false
    ↓
继续

↓

如果旧 render 已不适合继续
↓
restart

↓

workInProgress = null
↓
finishedWork
↓
commitRoot
↓
新的 current tree
```

---
## 下一阶段
接下来已经不需要继续深挖 Scheduler 的枝节，可以正式进入：

```text
startTransition 内部
↓
为什么 Update 获得 Transition Lane
↓
Transition 如何被 urgent update 抢占
↓
Suspense 如何 suspend
↓
thenable 如何被捕获
↓
Promise resolve
↓
retry lane
↓
重新调度
↓
Transition + Suspense 完整内部闭环
```

完成这一部分之后，你之前学过的 **Concurrent Features（并发特性）** 和现在的 **Fiber / Lane / Scheduler 内部机制** 就会真正合流。
