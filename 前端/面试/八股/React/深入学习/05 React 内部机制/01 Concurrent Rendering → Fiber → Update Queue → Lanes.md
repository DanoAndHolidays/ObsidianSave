# 01 Concurrent Rendering → Fiber → Update Queue → Lanes
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：从 Concurrent Rendering 串起 Fiber、current/WIP、Update Queue、Lanes 与优先级。

---
## 一、Concurrent React 的统一 Mental Model
React 中：

```text
setState
≠
立即修改当前 state
```

更准确是：

```text
setState
↓
enqueue update
↓
React 根据优先级安排 render
↓
构造 candidate UI
↓
可能：
  success
  interrupt
  suspend
  retry
  discard
↓
完整 candidate
↓
commit
```

因此必须明确区分：

```text
enqueue update
≠
render update
≠
commit update
```

### Current UI / Candidate UI
```text
current committed UI
=
用户当前真正看到的稳定版本
```

React 同时可以计算：

```text
candidate UI
=
可能成为下一版 UI 的未来版本
```

例如：

```text
Current:
Page A

Candidate:
Page B
```

B 即使已经 render 了一部分，也可能：

```text
被中断
被 suspend
被丢弃
永远不 commit
```

所以：

> render 是 speculative（推测性的），commit 才真正让结果生效。


# 二、为什么 React 需要 Fiber？

---
## 普通递归 render 的问题
最朴素的组件树遍历：

```js
function render(node) {
  process(node)

  for (const child of node.children) {
    render(child)
  }
}
```

对应：

```text
App
↓
Layout
↓
Main
↓
Content
↓
Item
```

这种递归依赖：

```text
JavaScript call stack
```

保存：

```text
当前在哪里
parent 是谁
函数结束后回哪里
下一个 sibling 是谁
```

如果同步一口气 render 完：

```text
render(root)
↓
完成
```

没有问题。

但 Concurrent Rendering 要求：

```text
做一点 render work
↓
yield
↓
把控制权还给浏览器
↓
以后继续
```

甚至：

```text
正在 render B
↓
urgent update C 到来
↓
中断 B
↓
处理 C
```

普通递归并不适合让 React 自己管理这种执行进度。

---
## Fiber 的核心动机
Fiber 将原本隐含在：

```text
JavaScript call stack
```

中的组件树执行状态，显式保存成 React 自己管理的数据结构。

暂时只需要理解三个关系：

```ts
Fiber {
  child
  sibling
  return
}
```

其中：

```text
child
=
第一个子 Fiber

sibling
=
下一个兄弟 Fiber

return
=
父 Fiber
```

例如：

```text
A
├─ B
│  ├─ D
│  └─ E
└─ C
```

可以通过：

```text
A.child = B

B.child = D
D.sibling = E

B.sibling = C

D.return = B
E.return = B
B.return = A
C.return = A
```

显式描述遍历关系。

---
## Fiber = React 管理的 Work Unit
Fiber 可以理解成：

> React 自己管理的 render work unit（渲染工作单元）。

Fiber traversal：

```text
遍历 Fiber
=
逐个执行 render phase work
```

但：

```text
Fiber work
≠
只调用 Function Component
```

因为 Fiber 还可能表示：

```text
div
span
Fragment
Suspense
HostRoot
Context
...
```

所以更准确：

> 遍历 Fiber，就是逐个执行各 Fiber 对应的 render-phase 工作。

---
## Fiber 为什么支持 Cooperative Scheduling？
概念上：

```js
while (nextFiber !== null) {
  nextFiber = performUnitOfWork(nextFiber)

  if (shouldYield()) {
    break
  }
}
```

与普通递归最大的区别：

```text
普通递归：
控制流主要由 JS call stack 管理

Fiber：
遍历进度被显式数据结构化，
控制权能不断回到 React
```

因此 React 可以在工作单元之间：

```text
Fiber A
↓
Fiber B
↓
Fiber C
↓
shouldYield()
↓
暂停
```

但 Fiber 不能打断：

```js
function Component() {
  expensiveWorkFor500ms()
}
```

因为一旦 React 调用这个同步 JS：

```text
React 暂时失去控制权
```

直到函数返回。

因此：

> Fiber 让 React 的 render traversal 可中断，但不能让 JavaScript 变成可抢占执行。


# 三、Current Tree / Work-in-Progress Tree

Fiber 解决了“怎么管理 render work”。

但还需要解决：

> 正在构造未来 UI 时，能不能直接修改当前已经显示的 Fiber tree？

答案是不可以。

---
## Current Tree
```text
current tree
```

表示：

> 当前已经 commit 的 Fiber 版本。

例如：

```text
current

App
└─ Counter count=0
```

对应当前稳定 UI。

---
## Work-in-Progress Tree
发生：

```tsx
setCount(1)
```

React不会直接把 current Fiber 改成：

```text
count=1
```

而是构造：

```text
work-in-progress tree
简称 WIP
```

例如：

```text
current
Counter count=0

WIP
Counter count=1
```

WIP 可以理解成：

> 当前正在构建的 candidate UI 的 Fiber 表示。

---
## 为什么需要两棵版本？
因为 WIP 可能：

```text
render 一半
suspend
被打断
被 discard
```

而 current 必须保持稳定。

例如：

```text
current:
Page A

WIP:
Page B
```

B render 到一半 suspend：

```text
Page B
├─ Header ✓
└─ Content suspend
```

此时：

```text
current A
```

仍然没有被破坏。

所以：

```text
current
=
stable / committed

WIP
=
speculative / candidate
```

---
## Commit 的意义
WIP 成功完成：

```text
current:
A

WIP:
B
```

commit 后概念上：

```text
WIP B
↓
成为新的 current
```

所以：

> commit 是 candidate 获得 current 身份的关键边界。

---
## Double Buffering
不要理解成：

```text
Tree A 永远是 current
Tree B 永远是 WIP
```

更接近：

```text
Tree 1 = current
Tree 2 = WIP
```

commit 后：

```text
Tree 2 = current
```

下一次 Tree 1 可以重新作为 WIP 使用。

因此可以类比：

> double buffering（双缓冲）。


# 四、Render Phase 如何遍历 Fiber？

Fiber traversal 是一种显式化的深度优先遍历。

每个 Fiber 通常经历：

```text
beginWork
↓
向下

completeWork
↑
向上
```

---
## 示例
```text
A
├─ B
│  ├─ D
│  └─ E
└─ C
```

完整执行顺序：

```text
begin A
begin B
begin D
complete D
begin E
complete E
complete B
begin C
complete C
complete A
```

---
## beginWork
对于 Function Component：

```tsx
function B() {
  return (
    <>
      <D />
      <E />
    </>
  )
}
```

概念上：

```text
beginWork(B)
↓
读取 props / state
↓
调用 B()
↓
得到新的 React Elements
↓
与旧 children Fibers reconciliation
↓
得到新的 child Fiber 结构
↓
继续 child
```

所以方向是：

```text
parent
↓
child
```

---
## completeWork
当：

```text
B
├─ D ✓
└─ E ✓
```

children 都已经完成后：

```text
completeWork(B)
```

做当前 Fiber 的收尾工作。

方向：

```text
child
↑
parent
```

---
## Traversal Rule
可以记成：

> 能向下就向下，不能向下就 complete；complete 后能向右就向右，不能向右就向上。

对应：

```text
child
→ down

sibling
→ right

return
→ up
```

概念算法：

```text
beginWork(current)

有 child
→ child

没有 child
→ completeWork(current)

有 sibling
→ sibling

没有 sibling
→ return parent
→ complete parent
```

---
## 为什么这比普通递归容易中断？
普通递归：

```text
回到 parent 的信息
=
存在 JS call stack
```

Fiber：

```text
return
=
显式保存 parent
```

所以 React 不需要依赖完整的递归调用栈，就知道：

```text
当前做到哪
下一步去哪
```

这就是 Fiber 有时被类比为：

> virtual stack frame（虚拟栈帧）

的原因。


# 五、Render Phase ≠ 修改 DOM

必须保持：

```text
beginWork
completeWork
```

都属于：

```text
render phase
```

它们主要是在：

```text
计算未来 UI
构造 / 更新 WIP Fiber
记录变化
```

而不是立即修改真实 DOM。

所以可以暂时记：

```text
render phase
=
算 candidate

commit phase
=
应用 candidate
```


# 六、Update Queue

现在把：

```text
setState = enqueue update
```

落实成内部结构。

---
## Function Component 的 state queue 在哪里？
对于：

```tsx
function App() {
  const [count, setCount] = useState(0)
  const [name, setName] = useState("Dano")
}
```

概念结构：

```text
App Fiber
│
└─ memoizedState
      ↓
    Hook1
      count
      queue
      ↓
    Hook2
      name
      queue
```

所以：

```text
setCount
→ count Hook queue

setName
→ name Hook queue
```

不是所有 state update 全部直接塞进一个 Fiber queue。

---
## setState 创建 Update
例如：

```tsx
setCount(1)
```

概念上：

```ts
Update {
  action: 1,
  lane: ...,
  next: ...
}
```

而：

```tsx
setCount(c => c + 1)
```

对应：

```ts
Update {
  action: c => c + 1,
  lane: ...,
  next: ...
}
```

所以：

> Update 是数据，不是立即执行的 state 修改命令。

---
## setState 为什么知道操作哪个 state？
第一次 mount Hook 时：

```text
Hook
├─ state
└─ queue
```

React 创建 dispatch。

概念上类似：

```js
setCount = dispatchSetState.bind(
  null,
  fiber,
  queue
)
```

因此 `setCount` 已经知道：

```text
Fiber
+
对应 Hook queue
```

后续调用不需要重新定位。


# 七、Update Queue 如何计算新 State？

假设：

```text
base state = 0
```

queue：

```tsx
setCount(c => c + 1)
setCount(c => c + 1)
setCount(10)
setCount(c => c * 2)
```

概念上：

```text
U1 +1
U2 +1
U3 replace 10
U4 *2
```

处理：

```text
0
↓ U1
1
↓ U2
2
↓ U3
10
↓ U4
20
```

最终：

```text
memoizedState = 20
```

---
## useState 可以理解为 basic reducer
概念：

```js
function basicStateReducer(state, action) {
  return typeof action === "function"
    ? action(state)
    : action
}
```

所以：

```tsx
setState(5)
```

相当于：

```text
replace with 5
```

而：

```tsx
setState(x => x + 1)
```

相当于：

```text
基于前一个队列结果继续计算
```


# 八、memoizedState / baseState / baseQueue

如果所有 update 每次都全部执行：

```text
queue
→ 从头跑到尾
→ 得新 state
```

那么根本不需要复杂的 `baseState / baseQueue`。

问题来自：

> 不同 lane 的 update 可以在同一 queue 中共存，而某次 render 只处理其中一部分。

---
## 为什么同一个 queue 会有不同 lane？
不是因为现实业务经常故意写：

```tsx
setCount(...)

startTransition(() => {
  setCount(...)
})

setCount(...)
```

这种代码主要只是教学实验。

现实中更自然的是：

```text
t1
Transition update 到来
↓
还没有完成

t2
新的 urgent update 到来
↓
进入同一个 Hook queue
```

例如：

```tsx
const [filter, setFilter] = useState(defaultFilter)

function changeFilter(next) {
  startTransition(() => {
    setFilter(next)
  })
}

function reset() {
  setFilter(defaultFilter)
}
```

时间线上可能形成：

```text
U1
filter = complexFilter
Transition

U2
filter = defaultFilter
Urgent
```

因此：

> 同一 queue 出现不同 lane，是多个不同时间的 update 在 Concurrent Rendering 下发生 overlap（重叠）的自然结果。


# 九、为什么需要 Base State / Replay？

假设：

```text
baseState = 1
```

queue：

```text
U1 urgent:
x => x * 2

U2 transition:
x => x + 10

U3 urgent:
x => x * 3
```

完整顺序正确结果：

```text
1
↓ U1
2
↓ U2
12
↓ U3
36
```

---
## Urgent Render
当前 render 只处理 urgent：

```text
U1
1 → 2

U2
skip

U3
2 → 6
```

本轮：

```text
memoizedState = 6
```

但以后不能：

```text
6 + 10 = 16
```

因为原始 update 顺序是：

```text
U1
U2
U3
```

正确结果仍然必须是：

```text
36
```

所以 React 需要保留：

```text
baseState = 2

baseQueue:
U2
U3
```

注意：

> U3 即使这次已经执行过，也需要保留用于未来 replay。

未来 Transition render：

```text
2
↓ U2 +10
12
↓ replay U3 *3
36
```

因此：

```text
memoizedState
=
本轮 render 当前算出的 state
```

而：

```text
baseState
=
为了未来重新处理被跳过 updates
所保存的重新计算起点
```

`baseQueue` 则保存未来需要 replay 的 update 序列。


# 十、Update 的优先级到底是什么？

首先要明确：

```text
setState 函数本身
没有固定优先级
```

而是：

> 每一次 `setState()` 调用产生的 Update，会被分配一个 lane。

例如：

```tsx
setCount(1)
```

可能产生：

```text
Update A
lane = Urgent
```

而：

```tsx
startTransition(() => {
  setCount(2)
})
```

同一个 `setCount` 产生：

```text
Update B
lane = Transition
```

所以：

```text
state
没有固定 priority

setState
也没有固定 priority

Update
才有 lane
```


# 十一、Update 的 Lane 会随着多次 Render 改变吗？

当前 mental model：

> 一次 Update 在 enqueue 时获得 lane；后续 render 根据 `renderLanes` 决定 process 还是 skip。

例如：

```text
Update B
lane = Transition
```

可能经历：

```text
Render #1
renderLanes = Urgent
↓
B skip
```

之后：

```text
Render #2
renderLanes = Transition
↓
B process
```

如果被打断：

```text
Render #3
renderLanes = Transition
↓
B retry
```

不是：

```text
B:
low
→ high
→ low
```

而是：

```text
Update.lane 基本保持其工作归属

变化的是：
每次 render 要处理的 renderLanes
```

真实源码存在 rebasing、cloning、entanglement 等更复杂 bookkeeping，但现阶段不要破坏这个核心 mental model。


# 十二、Lane 是什么？

Lane 不应该简单理解为：

```text
priority = high
priority = low
```

更准确：

> **Lane 是带有优先级语义的 React 工作标签 / 工作集合标识。**

一个 Update：

```text
Update
└─ lane
```

表达：

> “我属于哪一批 React work？”

而一次 render：

```text
renderLanes
```

表达：

> “我这次准备处理哪些 React work？”


# 十三、为什么 Lane 使用 Bitmask？

假设：

```text
Lane A = 0001
Lane B = 0010
Lane C = 0100
Lane D = 1000
```

这次处理：

```text
A + C
```

可以表示：

```text
0001
OR
0100
=
0101
```

于是：

```text
renderLanes = 0101
```

判断某 Update 是否属于当前 render：

```js
(updateLane & renderLanes) !== 0
```

例如：

```text
updateLane = 0100

0100
&
0101
=
0100
```

非 0：

```text
process
```

而：

```text
0010
&
0101
=
0000
```

则：

```text
skip
```

所以 bitmask 非常适合：

```text
合并 lanes
判断包含
筛选工作
表示工作集合
```


# 十四、为什么 Lane 不只是普通 Priority Number？

如果只有：

```text
priority = 1
priority = 2
priority = 3
```

很容易表达：

```text
谁更重要？
```

但 React 还需要表达：

```text
当前 root pending 哪些工作？

这次 render 处理哪几批 work？

某个 subtree 是否包含当前 render 需要的 work？

多批 Transition / Retry work 如何同时存在？
```

Lane 可以：

```text
pendingLanes =
A | B | C
```

而：

```text
renderLanes =
A | C
```

所以：

> Lane 不只是优先级，而是带有调度语义的工作集合表示。


# 十五、Root / Fiber 为什么也需要 Lane 信息？

假设：

```text
App
├─ Search
└─ Sidebar
```

现在：

```text
Search
→ Transition work

Sidebar
→ Urgent work
```

Root 可以记录：

```text
root.pendingLanes
=
Urgent | Transition
```

于是 React 不需要每次从整棵树扫描：

```text
“到底哪里有 pending work？”
```

Fiber 本身也可以保存：

```text
lanes
childLanes
```

概念上：

```text
Fiber.lanes
=
这个 Fiber 自己有什么 pending work

Fiber.childLanes
=
它的 subtree 有什么 pending work
```

这样 render 时如果发现：

```text
当前 subtree 的 lanes
和
renderLanes
完全没有交集
```

就可能：

```text
bailout
跳过整个 subtree
```


# 十六、Lane + Update Queue 如何配合？

假设：

```text
baseState = 1

U1
lane = Urgent
action = *2

U2
lane = Transition
action = +10

U3
lane = Urgent
action = *3
```

Root：

```text
pendingLanes =
Urgent | Transition
```

React先选：

```text
renderLanes = Urgent
```

处理 queue：

```text
U1
Urgent ∈ renderLanes
→ process

U2
Transition ∉ renderLanes
→ skip

U3
Urgent ∈ renderLanes
→ process
```

所以：

```text
lanes
=
决定本轮允许处理哪些 Update
```

而：

```text
baseState + baseQueue
=
保证跳过 Update 后仍然维持原始 update 顺序
```

两者是配套机制。


# 十七、`startTransition` 在真实业务中的意义

不要把它理解成：

```text
“在一个 handler 里故意制造高低优先级 state”
```

真实场景是：

> 同一次用户 intent 中，有些 UI 必须立即反馈，有些 UI 可以晚一点跟上。

例如搜索：

```tsx
function handleChange(e) {
  const value = e.target.value

  setInput(value)

  startTransition(() => {
    setKeyword(value)
  })
}
```

语义：

```text
input
=
latest
=
必须立即跟手
=
urgent
```

```text
keyword / result list
=
可以暂时落后
=
Transition
```

再比如：

```tsx
function handleTabClick(tab) {
  setSelectedTab(tab)

  startTransition(() => {
    setPage(tab)
  })
}
```

其中：

```text
Tab 按钮反馈
→ urgent

大型页面切换
→ Transition
```

判断标准不是：

```text
“这个 state 重要吗？”
```

而是：

> **这部分 UI 是否允许暂时落后于用户最新 intent？**


# 十八、一个 Event Handler 中为什么能产生不同 Lane？

例如：

```tsx
function handleClick(tab) {
  setSelectedTab(tab)

  startTransition(() => {
    setPage(tab)
  })
}
```

两笔 Update 都来自同一个：

```text
click
```

但第一笔执行时：

```text
没有 Transition context
+
当前是 discrete event
```

所以得到较高优先级 lane。

第二笔：

```text
处于 Transition context
```

所以：

```text
requestUpdateLane
↓
检测到 Transition
↓
分配 Transition Lane
```

因此：

> Event 只是 lane 分配的输入之一，不是最终 lane 本身。


# 十九、Event Priority / Lane / Scheduler Priority

这三个非常容易混。

必须分层。

---
## Event Priority（事件优先级）
描述：

> Update 产生于什么外部交互语境？

例如：

```text
Discrete Event
离散事件

click
keydown
```

特点：

```text
每一次都是明确用户意图
需要尽快响应
```


```text
Continuous Event
连续事件

mousemove
pointer move
...
```

特点：

```text
仍然来自用户交互
但不一定每一帧都必须独立完成
```


```text
Default Priority
```

普通更新，例如一些：

```text
timer
异步完成后的普通更新
```


# 二十、Transition Context

如果：

```tsx
startTransition(() => {
  setPage(...)
})
```

callback 仍然：

```text
同步立即执行
```

但是执行 `setPage` 时，React 当前处于：

```text
Transition context
```

因此：

```text
requestUpdateLane()
↓
优先发现 Transition
↓
requestTransitionLane()
↓
Update 获得 Transition Lane
```

所以之前的：

```text
startTransition
=
把其中的 update 标记为 non-urgent
```

现在可以升级为：

```text
startTransition
↓
建立 Transition context
↓
其中产生的 setState
↓
获得 Transition Lane
↓
进入 queue
↓
Root 标记该 lane pending
↓
React 后续可以和 urgent work 分开 render
```


# 二十一、Lane 和 Scheduler Priority 不是同一个东西

可以分成三层：

```text
Event Priority
事件层

“这个 update 为什么这么急？”
```

↓

```text
Lane
React Reconciler 层

“这笔 update 属于哪批 React work？”
```

↓

```text
Scheduler Priority
Scheduler 层

“什么时候给这批 JS work 执行时间？”
```

所以：

```text
Event Priority
≠
Lane
≠
Scheduler Priority
```

它们有关系，但不是一个概念。


# 二十二、完整的 Update → Render 链路

现在可以把目前内部机制串成：

```text
用户事件 / Transition context
↓
setState(action)
↓
dispatchSetState
↓
requestUpdateLane
↓
创建 Update
├─ action
├─ lane
└─ next
↓
加入 Hook update queue
↓
把 lane 标记到 Fiber / Root
↓
root.pendingLanes
↓
React 选择 getNextLanes()
↓
得到 renderLanes
↓
创建 / 复用 WIP tree
↓
Fiber traversal
↓
beginWork
↓
处理 Hooks
↓
process update queue

对于每个 Update：

Update.lane ∈ renderLanes
├─ yes → process
└─ no  → skip + preserve

↓
得到：
memoizedState
baseState
baseQueue
↓
继续构造 candidate UI
↓
completeWork
↓
WIP 完成
↓
commit
↓
WIP 成为新的 current
```


# 二十三、目前最核心的统一 Mental Model

---
## Fiber
```text
Fiber
=
React 将递归 render work
显式化后的可管理工作单元
```

它让 React 可以：

```text
暂停
继续
中断
丢弃
重新安排
```

---
## Current / WIP
```text
current
=
当前 committed Fiber 版本

WIP
=
正在构建的 candidate Fiber 版本
```

因此：

```text
render 可以失败
current 仍然稳定
```

---
## Fiber Traversal
```text
beginWork
=
向下处理当前 Fiber，
产生 / reconcile children

completeWork
=
children 完成后，
向上完成当前 Fiber
```

遍历依赖：

```text
child
sibling
return
```

而不是完全依赖 JS call stack。

---
## Update Queue
```text
setState
=
创建 Update
+
enqueue
```

Update 保存：

```text
action
lane
```

render 时才真正消费 queue。

---
## baseState / baseQueue
解决：

```text
某些 Update 因 priority 被 skip
但之后必须保持原始 update 顺序
```

因此需要：

```text
skip
preserve
replay
rebase
```

---
## Lane
```text
Lane
≠
单纯 high / low priority

Lane
=
带有优先级语义的工作标签 / 集合标识
```

它贯穿：

```text
Update
↓
Fiber
↓
Root
↓
work selection
↓
renderLanes
```

---
## Event Priority / Lane / Scheduler
```text
Event Priority
=
为什么急？

Lane
=
属于哪批 React work？

Scheduler Priority
=
什么时候给这些 work CPU 时间？
```


# 二十四、目前 React 内部机制学习进度

已经完成：

```text
1. 为什么需要 Fiber
✓

2. current tree / WIP tree
✓

3. render phase 如何遍历 Fiber
✓

4. update queue
✓

5. lanes / priority
✓ 基础 mental model
```

已经能够把：

```text
Concurrent Features
```

和内部结构连接：

```text
startTransition
↓
Transition context
↓
Transition Lane
↓
Update Queue
↓
root.pendingLanes
↓
renderLanes
↓
WIP candidate
↓
可中断 render
```


当前阶段已经完成：

```text
Concurrent Rendering
→ Fiber
→ current tree / WIP tree
→ Update Queue
→ Lanes
→ 可中断 render
```

Scheduler 的基础概念已经在 `02 Scheduler、Work Loop 与可中断渲染.md` 中完成串联；并发特性的行为模型也已经在 `04 React 并发特性` 模块完成。接下来不再把 Scheduler、Transition 或 Suspense 当作尚未开始的主题，而是集中做源码级交界复盘：

```text
lanes
↓
getNextLanes
↓
Scheduler priority
↓
sync / concurrent work loop
↓
shouldYield
↓
reconciliation
↓
render / commit
```

后续重点包括：

- Scheduler priority 与 React lanes 如何相互映射；
- `getNextLanes` 如何决定下一次 render 的工作集合；
- sync/concurrent work loop 如何执行、暂停、恢复或重启；
- `shouldYield` 如何把 Fiber work 切成可协作调度的工作单元；
- Transition、Suspense、`isPending`、interrupt、retry、stale UI 等行为如何落到上述内部模型；
- 在需要时回到源码，对齐 `Fiber`、`WIP tree`、`update queue`、`lanes`、`Scheduler` 和 `Suspense boundary` 的调用关系。

本笔记负责 Fiber、更新队列和 lanes 的基础模型；源码级调度与 reconciliation 细节分别在后续内部机制笔记中展开。〔CR-007〕