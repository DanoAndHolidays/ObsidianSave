# 04 React render phase 与 commit phase
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：render/commit phase、flags、completeWork、DOM mutation、layout effect 与 passive effect。

---
## 阅读说明
可以，下面我把我们这一轮关于 **render phase / completeWork / effect flags / commit phase / layout & passive effects** 的所有内容整理成一份适合留存的详细笔记。

---
## 一、这一阶段的核心问题
这一轮主要解决的是：

> reconciliation 已经给 WIP Fiber 标记了 `Placement / Deletion / Update`，那么 render phase 最终到底产出了什么？之后这些信息又如何真正变成 DOM 更新和 Effect 执行？

最终形成的主线是：

```text
setState
↓
Update + Lane
↓
render phase
↓
WIP Fiber Tree
↓
reconciliation
↓
effect flags
↓
completeWork
↓
finishedWork
↓
commit phase
↓
DOM mutation
↓
layout effects
↓
browser paint
↓
passive effects
```

---
## 二、render phase 最终到底产出了什么
不能再把 render phase 简单理解成：

```text
调用组件
↓
算 JSX
```

更准确的 mental model：

```text
render phase
=
构建下一棵 candidate Fiber Tree
+
计算这一轮 props / state
+
完成 reconciliation
+
准备 Host 相关信息
+
记录 commit phase 需要执行的工作
```

最终产出：

```text
finished WIP Fiber Tree
```

这棵树里面不仅包含：

```text
新的 Fiber topology
新的 props
新的 state
```

还包含：

```text
Placement
Update
Deletion
Layout
Passive
...
```

也就是：

> 如果最终采用这棵 candidate tree，那么 commit phase 应该做什么。

因此：

```text
render phase
```

实际上同时回答两个问题：

```text
1. 下一版 UI 应该是什么？
2. 从 current 变成下一版 UI，需要执行哪些工作？
```

---
## 三、effect flags 的意义
reconciliation 不会直接修改 DOM。

例如：

```text
C.flags = Placement
```

真正含义不是：

```text
现在插入 C
```

而是：

```text
如果这棵 WIP 最终 commit，
那么 commit phase 需要执行 Placement。
```

同理：

```text
Fiber.flags = Update
```

表示：

```text
这个 Fiber 在 commit phase 需要执行更新工作
```

所以：

```text
Fiber.flags
=
这个 Fiber 自己有什么 commit work
```

---
## 四、flags 与 subtreeFlags
我们推导过这个例子：

```text
Item B
flags = Placement

List
flags = NoFlags
subtreeFlags = Placement

App
flags = NoFlags
subtreeFlags = Placement

Root
subtreeFlags = Placement
```

核心区别：

```text
flags
=
我自己有 commit work

subtreeFlags
=
我的 subtree 里面有人有 commit work
```

为什么不能直接把 `Placement` 向上传到 parent 的 `flags`？

因为如果：

```text
Item B.flags = Placement
```

然后错误地传播成：

```text
List.flags = Placement
App.flags = Placement
```

commit phase 会误以为：

```text
List 自己也要 Placement
App 自己也要 Placement
```

但实际只是：

```text
Item B
```

需要 Placement。

因此必须区分：

```text
self work
vs
subtree work
```

---
## 五、与 lanes / childLanes 的对应关系
这个设计和之前学过的：

```text
fiber.lanes
fiber.childLanes
```

非常像。

可以整理成：

```text
                    render work        commit work

Fiber 自己           lanes              flags

Fiber 子树           childLanes         subtreeFlags
```

对应语义：

```text
lanes
=
我自己有 render work

childLanes
=
下面有 render work
```

而：

```text
flags
=
我自己有 commit work

subtreeFlags
=
下面有 commit work
```

区别在于服务阶段不同：

```text
lanes / childLanes
↓
帮助 render phase 判断哪里值得进入
```

```text
flags / subtreeFlags
↓
帮助 commit phase 判断哪里有副作用需要处理
```

---
## 六、subtreeFlags 为什么重要
我们明确了：

> commit phase 不是完全不遍历 Fiber Tree，而是可以通过 `subtreeFlags` 跳过没有 commit work 的整棵 subtree。

例如：

```text
Root
├── Header
│   └── Logo
├── Main
│   └── List
│       └── Item B [Placement]
└── Footer
```

如果：

```text
Header.subtreeFlags = NoFlags
Footer.subtreeFlags = NoFlags

Main.subtreeFlags = Placement
```

那么 commit traversal 可以直接跳过：

```text
Header subtree
Footer subtree
```

进入：

```text
Main
↓
List
↓
Item B
```

---
## 七、beginWork 与 completeWork 的方向
这一轮纠正了一个重要点。

正确方向：

```text
beginWork
=
parent → child
=
top-down（自顶向下）
```

而：

```text
completeWork
=
child 完成后再回到 parent
=
bottom-up（自底向上）
```

例如：

```text
A
├── B
└── C
```

大致顺序：

```text
beginWork(A)
↓
beginWork(B)
↓
completeWork(B)
↓
beginWork(C)
↓
completeWork(C)
↓
completeWork(A)
```

因此：

```text
beginWork
=
展开工作

completeWork
=
从下往上收尾工作
```

这是一个很好记的 mental model：

```text
beginWork
=
展开

completeWork
=
折叠
```

---
## 八、completeWork 为什么必须 bottom-up
关键前提：

> 当一个 Fiber 执行 `completeWork` 时，它的 children 已经全部完成。

例如：

```jsx
<div>
  <span>A</span>
  <button>B</button>
</div>
```

Fiber：

```text
div
├── span
└── button
```

顺序：

```text
completeWork(span)
↓
completeWork(button)
↓
completeWork(div)
```

因此到了：

```text
completeWork(div)
```

时：

```text
span 已经完成
button 已经完成
```

所以 parent 可以：

```text
读取 children 已完成的结果
↓
完成自己
↓
把 subtree 信息继续向上汇总
```

---
## 九、completeWork 到底在 complete 什么
现在的稳定 mental model：

```text
children 已完成
↓
completeWork(currentFiber)

├── 1. finalize self
│   完成当前 Fiber 自己
│
└── 2. bubble subtree information
    汇总 children 的结果
```

也就是：

```text
完成自己
+
向 parent 汇总
```

---
## 十、HostComponent mount 时 completeWork 的职责
例如：

```jsx
<div>
  <span>Hello</span>
</div>
```

首次 mount 时：

```text
completeWork(span)
```

可以创建：

```text
HTMLSpanElement
```

然后：

```text
spanFiber.stateNode
=
真实的 span DOM instance
```

接下来：

```text
completeWork(div)
```

由于 child 已经完成：

```text
创建 div DOM instance
↓
找到已经准备好的 Host children
↓
把 span append 到 div
```

可能形成：

```html
<div>
  <span>Hello</span>
</div>
```

但这时候：

> 这个 DOM subtree 还没有正式插入当前页面。

所以要特别区分：

```text
创建 DOM object
≠
修改 committed 页面
```

mount render phase 中可以创建 detached DOM：

```text
detached DOM subtree
```

但：

```text
#root.appendChild(...)
```

这种真正影响页面的操作，要等 commit mutation。

---
## 十一、“render phase 不操作 DOM”的精确修正
简单 mental model：

```text
render phase 不操作 DOM
```

并不完全精确。

更准确：

> render phase 不修改当前已经 committed、用户正在看到的 Host Tree。

因为 mount 时：

```text
completeWork
```

可能已经：

```text
createInstance
appendInitialChild
```

创建并组装新的 detached DOM nodes。

所以：

```text
render phase
```

可以准备 candidate Host Tree，

但不能让 candidate 提前污染当前 committed UI。

---
## 十二、HostComponent update 时 completeWork 的职责
例如 current DOM：

```html
<button class="primary">
  Save
</button>
```

下一轮：

```jsx
<button className="danger">
  Save
</button>
```

reconciliation 判断：

```text
same type
same identity
↓
reuse Fiber identity
```

这时候 `completeWork(button)` 不能直接：

```js
dom.className = "danger"
```

因为：

```text
render phase
```

仍然属于 candidate computation。

如果这一轮 WIP 后续被 abandon：

```text
真实 DOM 已经被改
```

就无法回滚。

所以 update 路径更像：

```text
oldProps
vs
newProps
↓
发现变化
↓
Fiber.flags |= Update
```

即：

> 先记录“commit 时需要 Update”，真实 DOM 修改留给 commit phase。

---
## 十三、mount 与 update 的区别
可以整理成：

```text
                mount                     update

DOM 节点         新建 candidate DOM        复用 committed DOM

render phase     可准备 detached DOM        不直接修改 committed DOM

记录工作         Placement 等              Update 等

真正生效         commit                    commit
```

---
## 十四、completeWork 的 bubble 行为
假设：

```text
List
├── A
└── B [Placement]
```

当：

```text
completeWork(B)
```

之后：

```text
B.flags = Placement
```

轮到：

```text
completeWork(List)
```

它会汇总：

```text
List.subtreeFlags
|=
A.flags
A.subtreeFlags
B.flags
B.subtreeFlags
```

最终：

```text
List.subtreeFlags = Placement
```

然后：

```text
completeWork(App)
```

继续向上：

```text
App.subtreeFlags = Placement
```

一直到 Root。

所以：

```text
completeWork
```

除了完成 Host Fiber 本身，

还负责：

```text
bubbleProperties
```

把：

```text
flags
subtreeFlags
childLanes
```

等 subtree 信息向上汇总。

---
## 十五、beginWork / completeWork 的统一理解
最终可以这样记：

```text
beginWork
=
根据当前 Fiber 的输入
计算它下一步应该有哪些 children

↓ top-down
```

```text
completeWork
=
children 已完成
↓
利用 child 结果完成自己
↓
把 subtree 结果向 parent 汇总

↑ bottom-up
```

整体：

```text
beginWork
=
展开问题

completeWork
=
收集已经完成的子问题，并完成自己
```

---
## 十六、render phase 完成后的系统状态
假设：

```text
current tree = A
```

render 得到：

```text
finished WIP tree = B
```

此时：

```text
current = A
DOM = A
WIP = B
```

也就是说：

```text
A
=
committed reality（已提交现实）

B
=
candidate（候选方案）
```

即使 B render 完成，也不能直接认为：

```text
B 已经生效
```

---
## 十七、为什么不能 render 一结束就 root.current = finishedWork
这是这一轮重点理解过的一点。

假设：

```text
current Fiber Tree = A
DOM = A
```

render 得到：

```text
finishedWork = B
```

例如 Fiber B 已经表示：

```text
className = "new"
```

但真实 DOM 还是：

```text
className = "old"
```

如果此时提前：

```text
root.current = B
```

就会变成：

```text
Fiber current = B
DOM           = A
```

React 内部事实和浏览器事实不一致。

但：

```text
root.current
```

的语义应该是：

> 当前已经提交、并且和 Host world 对齐的 Fiber Tree。

因此不能让 candidate 提前变成 committed truth。

---
## 十八、current / WIP mental model 的升级
以前：

```text
current = 事实
WIP = 草稿
```

现在更准确：

```text
current
=
已经和 Host world 对齐的 committed truth
```

而：

```text
WIP
=
render phase 正在构建的 candidate computation
```

所以：

```text
render phase
=
计算下一版事实
```

```text
commit phase
=
让下一版事实真正成立
```

---
## 十九、为什么需要独立的 commit phase
可以把 React 看成同时维护两个世界：

```text
React internal world
=
Fiber Tree
```

以及：

```text
Host world
=
DOM
```

render 结束：

```text
Fiber current = A
DOM           = A

WIP           = B
```

依然完全一致。

commit 的任务是：

```text
把 Host world 从 A → B
+
让 Fiber current 从 A → B
```

最终重新得到：

```text
Fiber current = B
DOM           = B
```

所以：

> commit phase 是 candidate 变成 committed reality 的边界。

---
## 二十、commit phase 的主要阶段
这一轮建立的高层结构：

```text
render phase
↓
finishedWork
↓
────────────────
commit phase
│
├── before mutation
├── mutation
├── root.current = finishedWork
└── layout
────────────────
↓
browser paint
↓
passive effects
```

---
## 二十一、before mutation
这个阶段发生时：

```text
current = old
DOM     = old
finishedWork = new
```

真实 DOM 还没变。

所以它提供：

> 读取旧 DOM 的最后机会。

经典场景：

```text
getSnapshotBeforeUpdate
```

例如保存：

```text
scrollHeight
scrollTop
```

然后 mutation 后根据新 DOM 修正滚动。

所以：

```text
before mutation
=
旧 Host Tree 最后的读取窗口
```

---
## 二十二、mutation phase
这里才真正执行：

```text
Placement
Update
Deletion
```

例如：

```text
Placement
↓
insert / move DOM
```

```text
Update
↓
修改 DOM properties
```

```text
Deletion
↓
remove DOM
```

这和 reconciliation 正好接起来：

```text
reconciliation
=
决定怎么变
```

```text
commit mutation
=
真正执行这些变化
```

---
## 二十三、reconciliation 与 mutation 的关系
例如：

```text
old:
A B

new:
B C
```

render phase：

```text
B → reuse
A → Deletion
C → Placement
```

此时 DOM 仍：

```text
A B
```

commit mutation 才真正：

```text
remove A
insert C
```

最后：

```text
B C
```

因此：

> reconciliation 本身只计算 Host Tree 应如何变化，不直接执行这些变化。

---
## 二十四、current tree 的切换
mutation 完成以后：

```text
DOM = new
```

然后：

```text
root.current = finishedWork
```

于是：

```text
Fiber current = new
DOM           = new
```

新的 WIP 正式成为 committed truth。

---
## 二十五、layout phase
此时：

```text
current = new
DOM     = new
```

所以适合执行：

```text
useLayoutEffect
```

因为它能够看到：

```text
新的 props
新的 state
新的 DOM
```

例如：

```js
ref.current.getBoundingClientRect()
```

能够获取新 DOM 的真实 layout。

---
## 二十六、为什么 useLayoutEffect 在 mutation 后
因为：

```text
getBoundingClientRect()
```

想获取的是：

```text
新 DOM 的位置 / 大小
```

如果 mutation 之前测：

```text
拿到的是旧 DOM
```

所以必须：

```text
DOM mutation
↓
new DOM exists
↓
useLayoutEffect
```

---
## 二十七、为什么 useLayoutEffect 又要在 paint 前
因为它常用于：

```text
测量 DOM
↓
根据测量结果修正 UI
```

例如 tooltip。

理想流程：

```text
DOM mutation
↓
临时 DOM 已创建
↓
useLayoutEffect
↓
getBoundingClientRect
↓
setState
↓
同步重新 render + commit
↓
browser paint
```

用户看到的直接是：

```text
最终正确位置
```

而不是：

```text
错误位置
↓
闪一下
↓
正确位置
```

因此：

> `useLayoutEffect` 的价值之一，就是在用户看到画面之前完成必须同步的 layout 修正。

---
## 二十八、DOM mutation 与 browser paint 不是同一件事
这是这一轮建立的一个重要区别：

```text
DOM mutation
≠
browser paint
```

React 可以：

```text
先修改 DOM
```

但浏览器还没有真正把这一帧画到屏幕。

中间这个窗口：

```text
DOM mutation
↓
useLayoutEffect
↓
browser paint
```

就是 layout effect 能完成同步测量和修正的原因。

---
## 二十九、useEffect 为什么可能产生抖动
如果同样的测量逻辑放在：

```text
useEffect
```

高层时间线通常是：

```text
DOM mutation
↓
browser paint
↓
useEffect
↓
测量
↓
setState
↓
再次 render + commit
↓
再次 paint
```

用户可能先看到：

```text
错误位置
```

下一帧才变成：

```text
正确位置
```

于是出现：

```text
flicker（闪烁）
layout shift（布局跳动）
```

因此：

```text
useLayoutEffect
=
DOM 已更新
+
paint 前
```

适合：

```text
必须在用户看到之前完成的 layout 测量/修正
```

而：

```text
useEffect
```

更适合：

```text
不需要阻塞视觉更新的副作用
```

例如：

```text
订阅
网络连接
WebSocket
analytics
外部系统同步
```

---
## 三十、Effect 不会在 render phase 直接执行
这是和 concurrent render 直接相关的。

假设 candidate B：

```text
render B
```

遇到：

```jsx
useEffect(() => {
  analytics.track(...)
}, [])
```

如果 render 时立即执行：

```text
B effect 已经生效
```

但随后：

```text
B 被 abandon
```

用户根本没看到 B，

但 B 的副作用已经影响外界。

这会破坏：

```text
candidate render 可以丢弃
```

这一基本能力。

因此：

```text
render phase
=
只记录 effect work
```

```text
commit / passive phase
=
真正执行 effect
```

---
## 三十一、Effect 与 Fiber flags
Function Component 里：

```jsx
useLayoutEffect(...)
useEffect(...)
```

render 时会：

```text
比较 deps
↓
判断这一轮是否需要执行 effect
↓
记录 effect information
↓
在 Fiber 上留下 Layout / Passive 等 commit 信息
```

高层可以理解：

```text
Fiber.flags
=
这个 Fiber 有 Layout / Passive work
```

然后：

```text
subtreeFlags
```

继续向上汇总。

---
## 三十二、Effect 的两级索引
我们建立了一个很重要的结构：

```text
Fiber flags
↓
哪个 Fiber 有 effect work？
```

进入 Fiber 后：

```text
Effect information / effect tags
↓
这个 Fiber 里面具体哪个 effect 要执行？
```

所以类似：

```text
subtreeFlags
↓
哪个 subtree 有 commit work

Fiber.flags
↓
哪个 Fiber 有 commit work

effect tag
↓
Fiber 内哪个 Effect 要执行
```

这与 Lane 的分层思路类似：

```text
root.pendingLanes
↓
哪类 work

fiber.lanes / childLanes
↓
哪里有 work

update.lane
↓
具体哪个 Update apply
```

---
## 三十三、Effect dependencies 是什么时候比较的
例如：

```jsx
useEffect(() => {
  connect(roomId)
}, [roomId])
```

render phase 会比较：

```text
previous deps
vs
next deps
```

如果：

```text
[1]
vs
[1]
```

则：

```text
effect 存在
但这一轮不需要重新执行
```

如果：

```text
[1]
vs
[2]
```

则：

```text
这一轮需要重新执行 effect
```

所以：

```text
render phase
=
判断 effect 是否需要执行
```

而不是：

```text
render phase
=
执行 effect
```

---
## 三十四、Effect 的 setup / cleanup mental model
`useEffect` 不应该简单理解成：

> render 后执行一个函数。

更准确：

```text
Effect
=
setup + cleanup 生命周期单元
```

比如：

```jsx
useEffect(() => {
  connect(roomId)

  return () => {
    disconnect(roomId)
  }
}, [roomId])
```

---
## Mount
```text
setup
```

---
## Update + deps changed
正确顺序：

```text
old cleanup
↓
new setup
```

例如：

```text
disconnect(1)
↓
connect(2)
```

而不是：

```text
connect(2)
↓
disconnect(1)
```

因为后者会造成旧、新副作用暂时重叠。

---
## Update + deps unchanged
```text
什么都不做
```

---
## Unmount
```text
cleanup
```

---
## 三十五、useLayoutEffect cleanup/setup 的阶段
这一轮进一步区分了：

```text
useLayoutEffect cleanup
```

和：

```text
useLayoutEffect setup
```

它们不会简单紧挨着执行。

高层：

```text
mutation phase
↓
old layout effect cleanup
↓
DOM mutation / ref changes
↓
root.current 切换
↓
layout phase
↓
new layout effect setup
```

意义：

> 旧 layout world 先 teardown，新 layout world 再 setup。

---
## 三十六、为什么旧 layout cleanup 先发生
假设 sibling：

```text
Parent
├── A
└── B
```

如果执行：

```text
A cleanup
A setup
B cleanup
B setup
```

可能：

```text
A setup 创建了新状态
↓
B 的旧 cleanup 又把它破坏
```

所以更合理：

```text
旧 layout effects
cleanup
cleanup
cleanup

↓ DOM 世界切换

新 layout effects
setup
setup
setup
```

即：

> 旧世界彻底退出以后，再建立新世界。

---
## 三十七、layout cleanup 与 DOM 删除
我们推理过：

```jsx
useLayoutEffect(() => {
  const node = ref.current

  return () => {
    // cleanup 可能访问 node
  }
}, [])
```

如果组件卸载，

更合理的是：

```text
layout cleanup
↓
detach ref / remove DOM
```

而不是：

```text
remove DOM
↓
ref.current = null
↓
cleanup
```

原因：

> layout cleanup 可能还需要访问旧 DOM / 旧 layout。

所以它和 Host Tree 生命周期绑定得更紧。

---
## 三十八、useEffect cleanup 的位置
普通 passive effect 则更晚。

高层：

```text
DOM 已经完成切换
↓
browser 已经有机会 paint
↓
passive effects
↓
old passive cleanup
↓
new passive setup
```

所以：

```text
useLayoutEffect
=
commit 同步生命周期的一部分
```

而：

```text
useEffect
=
UI commit 之后，再同步外部系统
```

---
## 三十九、完整 commit 时间线
目前可以记：

```text
OLD committed world

before mutation
↓
旧 DOM 最后的读取窗口

mutation phase
├── layout cleanup
├── ref detach
├── Placement
├── Update
└── Deletion
↓
Host Tree 进入 NEW

root.current = finishedWork
↓
Fiber current 进入 NEW

layout phase
├── ref attach
└── layout effect setup
↓
当前：
Fiber current = NEW
DOM           = NEW

browser paint

↓
passive phase
├── old passive cleanup
└── new passive setup
```

---
## 四十、为什么 commit phase 不能像 render phase 一样随意中断
render phase：

```text
current = A
DOM     = A

WIP = B
```

如果 B：

```text
暂停
重算
丢弃
```

都没关系。

因为：

```text
用户仍然看到完整的 A
```

但 commit mutation 不一样。

例如：

```text
A B C
↓
B D C
```

commit 到一半：

```text
A 已删
D 还没插
```

此时真实 DOM 可能暂时是：

```text
B C
```

如果 React像 concurrent render 一样随便 yield：

```text
停止 commit
↓
去做别的事
```

用户可能看到：

```text
半完成 Host Tree
```

而且：

```text
Fiber current 是谁？
refs 指向谁？
layout effect 看哪个世界？
event handler 属于哪个版本？
```

都会变得难以定义。

所以：

```text
render phase
=
speculative / interruptible
```

而：

```text
commit phase
=
让 candidate 成为 reality
```

需要近似 atomic（原子式）的切换。

---
## 四十一、完整一次 React update
把所有内容串起来：

```text
setState
│
↓
创建 Update
│
↓
Update.lane
│
↓
Hook queue
│
↓
fiber.lanes
│
↓
ancestor.childLanes
│
↓
root.pendingLanes
│
↓
选择 renderLanes
│
↓
════════ render phase ════════

beginWork
│
├── 执行 Function Component
├── 处理 Hook queue
├── apply / skip Update
├── 得到新的 state
├── 产生 new React Elements
└── reconciliation
    ├── reuse
    ├── mount
    ├── delete
    └── move

↓ child

completeWork
↑
├── Host Fiber 收尾
├── mount 时准备 detached Host instance
├── update 时记录 Update
├── flags
├── subtreeFlags
└── bubbleProperties

↑ parent

Root complete
↓
finishedWork
```

此时：

```text
current = OLD
DOM     = OLD
WIP     = NEW
```

然后：

```text
════════ commit phase ════════

before mutation
↓
读取旧 Host Tree

mutation
↓
Placement / Update / Deletion
+
layout cleanup

↓
DOM = NEW

root.current = finishedWork

↓
current = NEW
DOM     = NEW

layout
↓
layout setup
refs
DOM measurement

↓
browser paint

↓
passive effects
↓
old passive cleanup
↓
new passive setup
```

---
## 四十二、render / commit 最终统一 mental model
现在可以把两个阶段压缩成：

```text
render phase
=
calculate change（计算变化）
```

而：

```text
commit phase
=
apply change（应用变化）
```

更完整：

```text
render phase
=
“如果采用下一版 UI，
它应该是什么样，
以及需要做哪些事情？”
```

```text
commit phase
=
“正式采用这版 candidate，
让这些变化真正发生。”
```

---
## 四十三、reconciliation / flags / commit 的关系
你之前已经学过的 reconciliation，现在可以正式接到 commit：

```text
new React Elements
+
current Fibers
↓
reconciliation
↓
identity 判断
↓
reuse / mount / delete / move
↓
Placement / Deletion / Update...
↓
Fiber flags
↓
completeWork bubble subtreeFlags
↓
finishedWork
↓
commit phase
↓
真实 Host mutation
```

因此：

```text
reconciliation
=
决定“怎么变”
```

```text
effect flags
=
记录“需要做什么”
```

```text
commit phase
=
真正“把这些事情做掉”
```

---
## 四十四、candidate render 被 abandon 时会发生什么
最后我们验证了这个关键问题。

假设 concurrent render 已经：

```text
C.flags = Placement
App.flags = Passive
```

但是 commit 前：

```text
整棵 WIP 被 abandon
```

那么：

```text
C 对应 DOM
不会插入页面
```

因为：

```text
Placement 没有进入 commit
```

同时：

```text
App 的 useEffect
也不会执行
```

因为：

```text
Passive work 没有被 commit / flush
```

也就是说：

```text
WIP
├── Placement
├── Update
├── Deletion
├── Layout
└── Passive

↓ abandon

全部作废
```

即使 mount render phase 已经创建了：

```text
detached DOM instance
```

也不会进入真实页面。

---
## 四十五、这一阶段目前可以记住的最核心几句话
```text
current 是 committed truth。
WIP 是 candidate computation。

```

```text
render phase
不是只算 JSX，
而是在构建完整的 candidate transaction。
```

```text
reconciliation
决定 Fiber identity 和结构变化。

```

```text
flags
=
当前 Fiber 自己的 commit work。

subtreeFlags
=
子树里的 commit work。
```

```text
beginWork
=
top-down 展开。

completeWork
=
bottom-up 收尾。

```

```text
completeWork
=
完成自己
+
汇总 children 的结果。
```

```text
render phase
可以创建 detached DOM，
但不能修改 committed Host Tree。

```

```text
render phase
=
计算变化。

commit phase
=
应用变化。
```

```text
Placement / Update / Deletion
在 render 中被决定，
在 commit mutation 中真正执行。

```

```text
useLayoutEffect
=
新 DOM 已存在
+
paint 前执行。
```

```text
useEffect
=
通常允许 paint 后再执行。

```

```text
Effect 在 render 中只被记录，
不会真正执行。
```

```text
candidate 如果被 abandon，
对应 Placement / Layout / Passive 等全部不会生效。

```

```text
render 可以被中断和丢弃，
commit 不适合像 render 一样随意 yield。
```

---
## 四十六、当前这部分的完成度
这一段目前可以认为：

---
## render phase / commit phase 主干 mental model：已经基本建立
已掌握：

```text
render phase 的最终产物
WIP / finishedWork
effect flags
subtreeFlags
completeWork
Host mount/update 差异
before mutation
mutation
current 切换
layout phase
browser paint
passive effects
useLayoutEffect / useEffect 时机
Effect cleanup / setup
commit 不可随意中断的原因
candidate abandon 与副作用隔离
```

目前还没有系统深挖的细节包括：

```text
具体 commit traversal 源码
commitMutationEffects 的完整实现
Placement 如何找到 Host parent / Host sibling
Deletion subtree 的完整递归
ref attach / detach 的精确源码顺序
Effect linked list 的具体字段
Passive effect 调度与 flushPassiveEffects
Strict Mode 下 Effect 双调用机制
```

这些属于后续源码层深化，不代表当前主干没有完成。

目前最适合的阶段判断是：

> **render phase / commit phase 的核心 mental model 已基本完成，可以开始进入下一块内部机制；源码细节后续按需要补。**

