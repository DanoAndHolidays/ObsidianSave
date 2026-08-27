# 02 Scheduler 串联
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：Scheduler、cooperative scheduling、pause/resume/abandon，以及 Hook 更新到 DOM 的链路。

---
## 当前阶段
本轮主要把之前已经学过但比较分散的几个概念重新串了起来：

- Fiber
    
- current tree / work-in-progress tree
    
- update queue
    
- lanes / priority
    
- Scheduler / cooperative scheduling
    
- Hook state storage
    
- rebase
    

目前已经能够从一个 `setState` 出发，理解它如何一路影响 Hook、Fiber、WIP render，最终 commit。

---
## Scheduler / Cooperative Scheduling
Scheduler（调度器）主要解决：

> React 什么时候执行工作，以及执行多久后应该把主线程还给浏览器。

几个模块的职责可以这样区分：

```text
Fiber
→ 工作怎么拆成一个个小单元

WIP Tree
→ 未完成的 render 结果放在哪里

Lane
→ 哪些更新更优先

Scheduler
→ 什么时候执行、什么时候 yield
```

React 的调度属于：

> cooperative scheduling（协作式调度）

不是浏览器强制暂停 React，而是 React 主动检查：

```js
shouldYield()
```

概念模型：

```text
Fiber A
↓
Fiber B
↓
Fiber C
↓
shouldYield() === true
↓
React 主动暂停
↓
浏览器获得主线程
↓
之后继续
```

---
## Fiber 为什么能支持暂停
Fiber 将原本隐藏在 JavaScript call stack 中的递归 render 工作显式化。

普通递归：

```text
render A
  render B
    render C
```

依赖 JS 调用栈保存上下文。

Fiber 后变成：

```text
Fiber A
Fiber B
Fiber C
```

React 自己维护：

```text
child
sibling
return
```

以及：

```text
workInProgress
```

其中：

```text
child / sibling / return
→ Fiber Tree 怎么走

workInProgress
→ 当前走到哪个 Fiber
```

因此 render 可以：

```text
A ✓
B ✓
C ✓
D ← workInProgress
```

暂停之后，如果这一轮 render 仍然有效，可以从附近继续。

---
## Pause / Resume / Abandon
需要区分三个概念。

### Pause
时间片到了：

```text
A → B → C
        ↓
      yield
```

当前 render 暂停。

### Resume
如果没有更高优先级工作：

```text
A B C
    ↓
resume
    ↓
D E F
```

继续当前 WIP。

### Abandon
如果暂停期间来了更高优先级 update：

```text
Transition WIP
A → B → C
        ↓

Urgent Update 到来
```

React 可能放弃当前 candidate render：

```text
WIP candidate
→ abandon
```

转而处理高优先级工作。

---
## current 和 WIP
这是并发 render 的安全基础。

```text
current tree
= 已经 commit 的可靠世界

WIP tree
= 当前正在计算的候选结果
```

例如：

```text
current:
count = 3

WIP:
count = 10
```

如果 WIP 被中断：

```text
WIP count = 10
→ 可以丢弃
```

但：

```text
current count = 3
```

不会变化。

核心原则：

> current 是事实，WIP 是草稿。

因此 React 可以安全进行 speculative render（推测性渲染）。

---
## 丢弃的不是 Update
这个区分非常重要。

```text
Update
= “状态应该发生什么变化”

WIP Render
= “这一轮根据这些 Update 算出的结果”
```

例如：

```text
Update A:
+10
Transition Lane
```

React计算：

```text
current state = 0
↓ apply A
WIP state = 10
```

如果当前 render 被中断：

```text
WIP state = 10
→ 可以丢弃
```

但是：

```text
Update A
→ 不能因为 WIP 被丢弃而消失
```

因此：

> WIP 是可丢弃的计算草稿，Update 是需要被正确消费的状态变化记录。

---
## Update Queue + Lanes
每个 Update 都带有自己的 lane：

```text
Update A
├── action
└── lane
```

render 时 React 有一个：

```text
renderLanes
```

然后遍历 update queue：

```text
update.lane 属于 renderLanes
→ apply

update.lane 不属于 renderLanes
→ skip
```

但：

> skip ≠ 删除。

被跳过的 update 会保留，等待后续处理。

---
## Rebase
例子：

```text
initial state = 1

A: +1
lane = Transition

B: ×10
lane = Urgent

C: +5
lane = Urgent
```

第一轮：

```text
renderLanes = Urgent
```

执行：

```text
A → skip

B:
1 × 10 = 10

C:
10 + 5 = 15
```

因此：

```text
memoizedState = 15
```

但为了之后恢复正确的 update 顺序：

```text
baseState = 1

baseQueue:
A → B → C
```

这里 B、C 虽然已经执行过，但因为前面出现了被跳过的 A，也必须保留用于 replay。

之后处理 Transition：

```text
baseState = 1

1
↓ A +1
2
↓ B ×10
20
↓ C +5
25
```

最终：

```text
state = 25
```

所以 rebase 不是：

```text
15 + 1 = 16
```

而是：

> 从第一次发生 skip 时保存的 `baseState` 开始，按照正确顺序 replay 后续 update sequence。

---
## Fiber 和 Update Queue 的关系
之前容易把：

```text
Fiber
Update Queue
Lane
Scheduler
```

理解成四套独立系统。

实际上它们是嵌套关系。

对于 Function Component：

```text
Fiber
│
├── child / sibling / return
│
└── memoizedState
      ↓
    Hook 链
      ↓
    Hook queue
      ↓
    Update
      ↓
    Lane
```

Scheduler 在外层：

```text
Scheduler
    ↓
驱动 Fiber work loop
    ↓
Fiber → Fiber → Fiber
```

所以可以这样理解：

```text
Scheduler
→ 什么时候工作

Lane
→ 优先处理哪些 Update

Fiber
→ 当前处理哪个组件的 render work

Hook Queue
→ 这个组件具体有哪些 state updates
```

---
## Function Component 的 Fiber.memoizedState
对于 Function Component：

```text
Fiber.memoizedState
```

不是直接：

```text
count = 3
```

而是指向：

> 第一个 Hook 节点。

例如：

```jsx
function App() {
  const [count] = useState(0)
  const ref = useRef()
  const [name] = useState('')
}
```

内部大致：

```text
App Fiber
    │
    │ memoizedState
    ▼
Hook 1: useState(count)
    │ next
    ▼
Hook 2: useRef
    │ next
    ▼
Hook 3: useState(name)
```

Hook 节点中可能保存：

```text
memoizedState
baseState
baseQueue
queue
next
```

---
## 为什么 Function Component 每次执行还能拿回 state
函数组件每次 render 都是新的函数调用：

```js
Counter()
```

上一轮函数执行结束以后，函数调用栈已经不存在。

状态不是存在函数调用里的，而是在：

```text
current Fiber
↓
current Hook
↓
Hook.memoizedState
```

中保存。

例如已经 commit：

```text
current Hook.memoizedState = 3
```

下一次 render：

```text
current Hook
state = 3

        ↓ 作为参考

WIP Hook
正在计算新 state
```

因此：

```js
useState(0)
```

update render 时并不会重新用 `0`。

`0` 主要只是 mount 时的 initial state。

---
## Mount 时 useState
第一次：

```js
useState(0)
```

React会：

```text
创建 Hook
↓
挂到 Fiber.memoizedState
↓
memoizedState = 0
baseState = 0
↓
创建 update queue
↓
创建 setCount
```

结构类似：

```text
Counter Fiber
    ↓
Hook
├── memoizedState = 0
├── baseState = 0
├── baseQueue = null
└── queue
      ├── pending = null
      └── dispatch = setCount
```

---
## setState 为什么之后还能找到对应 Hook
例如：

```js
const [count, setCount] = useState(0)
```

第一次 render 时，React 创建 `setCount`。

它会和：

```text
Counter Fiber
+
count Hook 的 queue
```

建立关联。

mental model：

```js
setCount = action => {
  dispatchSetState(
    counterFiber,
    countQueue,
    action
  )
}
```

所以即使：

```text
Counter()
```

那一次函数调用早就结束，用户后来点击：

```js
setCount(c => c + 1)
```

React仍然知道应该把 Update 加到哪个 Hook queue。

---
## setState 不直接修改 state
调用：

```js
setCount(c => c + 1)
```

不会直接：

```text
Hook.memoizedState:
0 → 1
```

而是创建：

```text
Update
├── action = c => c + 1
└── lane
```

然后放入 queue。

当前 committed Hook：

```text
memoizedState = 0
```

仍然不变。

真正的 `1` 是下一次 render 时计算出来的。

---
## Update Render 时 useState
下一次 render：

```text
current Fiber
↓
current Hook
memoizedState = 0
```

React构建：

```text
WIP Fiber
↓
WIP Hook
```

并处理 queue：

```text
old state = 0

Update:
c => c + 1

↓ apply

newState = 1
```

得到：

```text
WIP Hook.memoizedState = 1
```

于是组件这一轮：

```js
const [count] = useState(0)
```

得到：

```text
count = 1
```

---
## Hook 调用顺序
React识别 Hook 不是靠变量名。

不是：

```text
找到叫 count 的 Hook
```

而是：

```text
本轮第 1 次 Hook 调用
→ current Hook 1

本轮第 2 次 Hook 调用
→ current Hook 2
```

所以：

```jsx
const [a] = useState(1)
const [b] = useState(10)
```

对应：

```text
Hook 1 = a
Hook 2 = b
```

---
## 为什么不能条件调用 Hook
例如：

```jsx
const [a] = useState(1)

if (condition) {
  useRef()
}

const [b] = useState(10)
```

第一次：

```text
Hook 1 → a
Hook 2 → ref
Hook 3 → b
```

下一次 condition 为 false：

```text
Hook 1 → a
Hook 2 → b
```

但 React 会把第二次 Hook 调用对应到：

```text
current Hook 2 = ref
```

因此整个 Hook 链错位。

所以 Rules of Hooks 的内部原因是：

> React 依赖稳定的 Hook 调用顺序，把当前 render 的 Hook 和上一轮 current Hook 一一对应。

---
## 为什么没变化的 Hook 也要构建 WIP Hook
例如：

```jsx
function App() {
  const [a] = useState(1)
  const [b] = useState(10)
}
```

只更新：

```js
setB(b => b + 5)
```

React不能只执行第二个 `useState`。

因为 Function Component 下一次 render：

```text
App()
↓
第一个 useState
↓
第二个 useState
↓
return
```

始终是从头执行。

因此：

```text
current             WIP

Hook 1              Hook 1'
a = 1               a = 1

Hook 2              Hook 2'
b = 10              b = 15
```

即使第一个 Hook 没有 update，它仍然属于本轮 candidate render，因此仍然需要构建对应的 WIP Hook。

---
## 从 setState 到 DOM 的完整链路
目前已经可以完整理解：

```text
setState
    ↓
创建 Update
    ↓
Update 带 Lane
    ↓
进入 Hook queue
    ↓
Fiber / Root 被标记有工作
    ↓
选择 renderLanes
    ↓
Scheduler 给 React 执行机会
    ↓
Fiber Work Loop
    ↓
处理 Function Component Fiber
    ↓
renderWithHooks
    ↓
从 current Hook 链读取上一轮状态
    ↓
根据 renderLanes 处理 update queue
    ↓
构建 WIP Hook
    ↓
执行 Component()
    ↓
得到新的 React Element
    ↓
reconcile children
    ↓
继续构建 WIP Fiber Tree
    ↓
整个 render 完成
    ↓
commit
    ↓
DOM 更新
    ↓
WIP 成为新的 current
```

---
## 当前最重要的统一 Mental Model
可以浓缩成：

```text
Scheduler
    ↓
决定 React 什么时候获得执行机会

FiberRoot / Lanes
    ↓
决定整棵树下一步优先处理哪些工作

Fiber Tree
    ↓
把 render 拆成一个个工作单元

Function Component Fiber
    ↓
保存 Hook 链

Hook
    ↓
保存 state / baseState / baseQueue / queue

Update
    ↓
描述一次状态变化，并携带 Lane

current
    ↓
已提交、可靠状态

WIP
    ↓
正在计算、可以暂停/重做/丢弃的候选状态
```

一句话版：

> **Scheduler 决定什么时候算，Lane 决定优先算什么，Fiber 决定一个个算哪些组件，Hook 保存组件状态，Update 描述状态变化，current 保存已提交事实，WIP 承载可丢弃的候选计算。**

---
## 当前学习进度
已完成或基本打通：

```text
✅ 为什么 React 需要 Fiber
✅ current tree / WIP tree
✅ Fiber render traversal
✅ update queue
✅ lanes / priority
✅ rebase
✅ Scheduler / cooperative scheduling 基础
✅ pause / resume / abandon
✅ Function Component Hook linked list
✅ useState mount / update mental model
✅ setState 与 Fiber / Hook queue 的关系
✅ Rules of Hooks 的内部原因
```

后续适合继续的内容：

```text
Scheduler 与 React Reconciler 的交界
↓
pending lanes
↓
getNextLanes
↓
root scheduling
↓
sync render / concurrent render
↓
yield / resume / restart
```

也就是不再重复 Fiber traversal / update queue，而是继续补完 **Scheduler 如何真正驱动一棵 Fiber Root**。

