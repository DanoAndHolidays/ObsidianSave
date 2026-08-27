# 03 reconciliation 与 key
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：Reconciliation、type/key identity、列表 diff、state preservation、Placement 与 Deletion。

---
## 可直接运行的示例
```tsx
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>React key 示例</title>
  <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    * { box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 24px; }
    .card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin: 12px 0; }
    button { margin-right: 8px; padding: 6px 12px; border-radius: 8px; border: 1px solid #d1d5db; background: white; cursor: pointer; }
    button:hover { background: #f3f4f6; }
    .counter { display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: #f9fafb; border: 1px solid #e5e7eb; }
    .tag { font-weight: 700; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    function Counter({ name, initial = 0 }) {
      const [count, setCount] = useState(initial);
      return (
        <div className="counter">
          <span className="tag">{name}:</span>
          <span>{count}</span>
          <button onClick={() => setCount(c => c + 1)}>+1</button>
        </div>
      );
    }

    // ========= 没有 key =========
    function AppNoKey({ swapped }) {
      return swapped ? (
        <>
          <Counter name="B" />
          <Counter name="A" />
        </>
      ) : (
        <>
          <Counter name="A" />
          <Counter name="B" />
        </>
      );
    }

    // ========= 有 key =========
    function AppWithKey({ swapped }) {
      return swapped ? (
        <>
          <Counter key="A" name="A" />
          <Counter key="B" name="B" />
        </>
      ) : (
        <>
        <Counter key="B" name="B" />
        <Counter key="A" name="A" />
        </>
      );
    }

    function Demo() {
      const [swapped, setSwapped] = useState(false);
      const [useKey, setUseKey] = useState(true);

      const App = useKey ? AppWithKey : AppNoKey;

      return (
        <div>
          <h2>React key 示例</h2>
          <p>
            <button onClick={() => setSwapped(s => !s)}>切换顺序</button>
            <button onClick={() => setUseKey(k => !k)}>当前：{useKey ? '有 key' : '无 key'}</button>
          </p>

          <div className="card">
            <h3>渲染结果：</h3>
            <App swapped={swapped} />
          </div>

          <div className="card">
            <h3>观察要点：</h3>
            <ul>
              <li>先点 <b>+1</b> 给两个计数器分别增加计数。</li>
              <li>再点 <b>切换顺序</b>。</li>
              <li><b>有 key 时：</b>count 跟着组件走，A 还是 A，B 还是 B。</li>
              <li><b>无 key 时：</b>React 只按位置复用组件，count 会“粘”在位置上，导致 A/B 的数值看起来交换了。</li>
            </ul>
          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<Demo />);
  </script>
</body>
</html>

```

---
## 阅读说明
下面这版按“可直接记笔记”的方式整理，重点保留我们这轮真正打通的 mental model，并明确区分：**已经理解的内容**、**暂时搁置的 Scheduler 抽象部分**、以及**下一步**。

# 03 reconciliation 与 key
> Last Format Time：8/27/2026


---
## 一、从 Hook Update 到 FiberRoot
一次：

```js
setState(...)
```

不会直接修改 state，而是：

```text
setState
↓
创建 Update
↓
Update 获得 Lane
↓
进入对应 Hook queue
```

但 Hook queue 只解决：

> Update 存在哪里。

Scheduler 最终需要知道的是：

> 哪一棵 FiberRoot 有工作需要处理。

因此还需要把 Lane 信息从局部 Fiber 传播到 Root。

---
## 二、`fiber.lanes` 与 `childLanes`
假设：

```text
App
└── Page
    └── Counter
```

Counter 产生：

```text
DefaultLane
```

那么可以理解为：

```text
Counter.lanes
= DefaultLane
```

`fiber.lanes` 表示：

> 当前 Fiber 自己有哪些工作。

而祖先不会把：

```text
parent.lanes
```

也设置成 DefaultLane。

因为父组件自己并没有产生 Update。

祖先记录的是：

```text
parent.childLanes
```

例如：

```text
App.childLanes
= DefaultLane

Page.childLanes
= DefaultLane

Counter.lanes
= DefaultLane
```

所以：

```text
fiber.lanes
→ 自己有工作

fiber.childLanes
→ subtree（子树）里有工作
```

---
## 三、Lane 向上传播，不是 Update 向上传播
Update 本身仍然待在：

```text
Counter Hook queue
```

沿 Fiber Tree 向上传播的是：

```text
“这里存在某个 Lane 的工作”
```

而不是整个 Update 对象。

可以理解为：

```text
Counter.lanes |= lane

Counter.return
↓
Page.childLanes |= lane
↓
App.childLanes |= lane
↓
HostRoot.childLanes |= lane
```

所以：

> Update 保存具体状态变化；Lane 是工作的调度信号。

---
## 四、为什么需要 `childLanes`
假设：

```text
App
└── Page
    └── Counter
```

如果：

```text
App.lanes = NoLanes
```

React 不能因此直接跳过整个 App subtree，因为 Counter 下面可能还有工作。

因此：

```text
App.childLanes
```

相当于：

> subtree 工作索引。

之后 render 时：

```text
当前 renderLanes
和
fiber.lanes / childLanes
没有交集
```

React 就有机会 bailout（跳过）对应 Fiber / subtree。

所以 Lane propagation 不只是为了找到 Root，也服务于后续 Fiber traversal 的剪枝。

---
## 五、FiberRoot 的 `pendingLanes`
Fiber Tree 上的信息最终需要升级成 Root-level summary（Root 级摘要）。

例如：

```text
A Fiber
TransitionLane

B Fiber
SyncLane
```

那么：

```text
App.childLanes
=
TransitionLane | SyncLane
```

同时：

```text
root.pendingLanes
=
TransitionLane | SyncLane
```

区别：

```text
fiber.lanes / childLanes
→ 工作具体分布在哪些 Fiber / subtree

root.pendingLanes
→ 整棵 Root 当前有哪些 Lane 的工作尚未完成
```

可以概括为：

```text
Hook queue
↓
Update.lane
↓
fiber.lanes
↓
ancestor.childLanes
↓
FiberRoot.pendingLanes
```

---
## 六、为什么最终调度的是 Root，不是 Component
虽然 Update 发生在：

```text
Counter Fiber
```

但是 React 最终不会：

```text
“单独 render Counter”
```

因为 Component 的结果可能依赖：

```text
Parent props
Context
Suspense
Transition
兄弟 reconciliation
父组件 bailout
...
```

React render 的目标是：

> 构建一棵一致的 candidate Fiber Tree。

因此：

```text
Component Fiber
=
工作发生的位置

FiberRoot
=
工作调度的单位
```

这和：

```text
current tree
WIP tree
```

是对应的。

---
## 七、Root-level scheduling 不等于整棵树全部重新执行
虽然调度的是 Root：

```text
FiberRoot
```

但并不代表：

```text
Root 下所有组件全部 render
```

因为：

```text
lanes
childLanes
renderLanes
```

可以帮助 React 判断：

```text
这个 subtree 有没有当前这一轮需要的工作
```

没有则 bailout。

所以：

```text
Root
→ 决定什么时候开始一轮工作

lanes / childLanes
→ 决定这一轮哪些路径值得继续深入
```

---
## 八、`getNextLanes` 的基本职责
假设：

```text
root.pendingLanes
=
SyncLane | TransitionLane
```

`pendingLanes` 只能回答：

> Root 有哪些工作。

不能直接等于：

```text
renderLanes
```

否则 Sync 和昂贵的 Transition 会被绑在一起处理。

因此需要：

```text
root.pendingLanes
↓
getNextLanes(...)
↓
nextLanes
```

它解决的是：

> Root-level work selection（Root 级工作选择）。

也就是：

> 下一轮应该处理哪一批 Lane？

---
## 九、Root / Fiber / Update 三层选择
可以分成：

### Root level
```text
getNextLanes
```

回答：

> 这一轮选哪些 Lane？


### Fiber level
```text
fiber.lanes
fiber.childLanes
```

回答：

> 哪些 Fiber / subtree 值得进入？


### Update level
```text
update.lane ∈ renderLanes
→ apply

update.lane ∉ renderLanes
→ skip
```

回答：

> Hook queue 里的哪些 Update 真正执行？


这和之前学过的 rebase 接起来：

```text
getNextLanes
→ 决定这一轮算哪些 Lane

rebase
→ 解决这一轮跳过某些 Update 后，
未来如何恢复正确的 update sequence
```

---
## 十、关于 starvation（饥饿）的修正
之前讨论：

```text
Sync
Sync
Sync
Sync
...
```

可能不断压住：

```text
Transition
```

这里需要一个重要修正：

> `expiredLanes` 不会简单把 TransitionLane 变成 SyncLane，也不会让 Transition 一定越过持续存在的 SyncLane。

即：

```text
TransitionLane
```

即使 expired，仍然还是 TransitionLane。

更准确的 starvation protection 是：

```text
普通 Transition
↓
允许 time slicing
↓
可以 yield
↓
可能反复被抢占
```

等待太久后：

```text
Transition ∈ expiredLanes
↓
不再 time slicing
↓
renderRootSync
```

也就是：

> 一旦它获得执行机会，就尽量一次把这一轮 render 做完，避免反复 yield / restart。

所以：

```text
Lane
→ 算哪些 Update

sync / concurrent work loop
→ 算的过程中允不允许 yield
```

这是两个不同维度。

如果高优先级 Sync 工作真的无限持续产生，那么 Transition 仍然可能持续延后。

---
## 十一、Scheduler 部分目前暂时搁置
已经接触但暂时不继续深入的内容：

```text
getNextLanes
↓
Root scheduling
↓
Lane priority
↓
Scheduler priority
↓
sync / concurrent render
↓
shouldYield
↓
resume / restart
```

当前已知道的大方向：

```text
Lane
→ 决定“算什么”

Scheduler priority
→ 决定“什么时候获得执行机会”

sync / concurrent work loop
→ 决定“开始算以后允不允许 yield”
```

但因为这部分过于抽象，目前先暂停，不标记为正式完成。

---
## 十二、转入 Reconciliation（协调）
Reconciliation 的核心问题：

> 下一次 render 得到新的 React Element 后，React 怎么判断它和旧 Fiber 是否代表同一个 UI identity（UI 身份）？

---
## 十三、React Element 与 Fiber 的区别
React Element：

```text
一次 render 产生的 UI 描述
```

例如：

```jsx
<Counter name="A" />
```

可以理解为：

```js
{
  type: Counter,
  key: null,
  props: {
    name: "A"
  }
}
```

每次 render 都会产生新的 Element 对象。

所以：

```text
element1 !== element2
```

并不能说明组件 identity 不同。


Fiber：

```text
React 内部持久化的 UI identity / 工作节点
```

它保存：

```text
memoizedState
memoizedProps
child
sibling
return
alternate
...
```

因此 reconciliation 本质上是：

```text
new React Element
+
old Fiber
↓
这个 old Fiber identity 能不能继续复用？
```

---
## 十四、`type + key` 与 identity
简化 mental model：

```text
same key
+
same type
↓
reuse Fiber identity
↓
preserve state
```

否则：

```text
different key
or
different type
↓
new Fiber identity
↓
state reset
```

---
## props 改变不会自动改变 identity
例如：

```jsx
<Counter key="x" label="A" />
```

变成：

```jsx
<Counter key="x" label="B" />
```

因为：

```text
type:
Counter → Counter

key:
x → x
```

所以：

```text
reuse identity
```

只是：

```text
props.label
A → B
```

而内部 Hook state 继续保留。

---
## 十五、严格来说不是“不创建 Fiber”
需要精确区分：

```text
reuse Fiber identity
```

和：

```text
完全复用同一个 Fiber JS 对象
```

React render phase 仍然会有：

```text
current Fiber
↕
WIP Fiber
```

所以更准确的说法是：

> props 改变不会产生一个全新的 component identity，而是基于 current Fiber 构建对应的 WIP Fiber。

---
## 十六、改变 `key` 可以主动 reset state
例如：

```jsx
<Counter key="x" />
```

变成：

```jsx
<Counter key="y" />
```

虽然：

```text
type = Counter
```

没变，但是：

```text
key:
x → y
```

所以 React认为：

```text
old Counter(x)
≠
new Counter(y)
```

结果：

```text
old Fiber
→ deletion

new Fiber
→ mount

useState(initialState)
→ 重新初始化
```

因此：

> `key` 是显式控制 component identity 的重要工具。

---
## 十七、State preservation 的本质
state 并不是：

> 跟 JSX 标签绑定。

而是：

> 跟 React 判断出的 Fiber identity 绑定。

所以：

```text
Fiber identity 被复用
→ Hook state 延续

Fiber identity 被替换
→ Hook state reset
```

---
## 十八、列表中 `key` 的真正作用
常见说法：

> key 是为了提高列表性能。

不够准确。

更核心的作用：

> key 帮 React 在 siblings（兄弟节点）中识别 identity。

例如：

```text
old:
A B C

new:
B A C
```

如果：

```text
key=A
key=B
key=C
```

React 可以知道：

```text
new B
↔ old B Fiber

new A
↔ old A Fiber

new C
↔ old C Fiber
```

所以：

```text
A reuse
B reuse
C reuse
```

全部 identity 保留。

---
## 十九、列表 reconciliation 的两阶段算法
---
## Phase 1：顺序 fast path（快速路径）
React先尝试：

```text
old[0] vs new[0]
old[1] vs new[1]
old[2] vs new[2]
```

如果当前位置 key 等还能匹配，就继续。

例如：

```text
[A,B,C]
→
[A,B,C,D]
```

不需要建立 Map。


一旦：

```text
old slot
和
new slot
不匹配
```

就退出 fast path。

---
## Phase 2：Map lookup
把剩余 old Fibers 建立：

```text
Map<key, oldFiber>
```

有显式 key：

```text
key → Fiber
```

没有 key：

```text
old index → Fiber
```

然后遍历剩余 new children：

```text
new child
↓
根据 key 找 old Fiber
↓
检查 type
↓
reuse / create
```

最后 Map 中还剩下的 old Fiber：

```text
→ Deletion
```

---
## 二十、`key` 与 `type` 的顺序理解
高层可以记：

```text
type + key
→ identity
```

更接近实际算法：

```text
先根据 key / slot
找到 candidate old Fiber

↓
再检查 type

same type
→ reuse

different type
→ new identity
```

例如：

```jsx
old:
<Counter key="A" />

new:
<Profile key="A" />
```

虽然 key 一样：

```text
A
```

但：

```text
Counter !== Profile
```

仍然不能 reuse。

---
## 二十一、Reuse identity ≠ DOM 不移动
例如：

```text
old:
[A, B, C]

new:
[B, A, C]
```

三个 identity：

```text
A reuse
B reuse
C reuse
```

但 DOM 顺序变了，因此 React还要判断：

> 哪些节点需要 Placement？

---
## 二十二、`lastPlacedIndex`
React使用：

```text
lastPlacedIndex
```

帮助判断：

> 已经处理过的新 children 中，旧 Fiber 的相对顺序还能不能继续保持。

核心规则：

```text
oldIndex < lastPlacedIndex
→ Placement

oldIndex >= lastPlacedIndex
→ stay
→ lastPlacedIndex = oldIndex
```

重要：

> React不是通过 `oldIndex !== newIndex` 判断 move。

它关心的是：

> 旧 Fiber 的相对顺序是否被破坏。

---
## 二十三、例子：`[A,B,C] → [B,A,C]`
旧 index：

```text
A = 0
B = 1
C = 2
```

初始：

```text
lastPlacedIndex = 0
```

### B
```text
oldIndex = 1
1 >= 0
→ stay

lastPlacedIndex = 1
```

### A
```text
oldIndex = 0
0 < 1
→ Placement
```

### C
```text
oldIndex = 2
2 >= 1
→ stay
```

最终：

```text
B
reuse + stay

A
reuse + Placement

C
reuse + stay
```

虽然人类直觉可能认为：

> B 被移动到了前面。

但 React 可以选择：

```text
B 保持
A 移到 B 后面
```

最终 DOM 一样。

---
## 二十四、更复杂例子
旧：

```text
A0 B1 C2 D3
```

新：

```text
B D A C
```

推导：

```text
B:
oldIndex = 1
1 >= 0
→ stay
lastPlacedIndex = 1
```

```text
D:
oldIndex = 3
3 >= 1
→ stay
lastPlacedIndex = 3
```

```text
A:
oldIndex = 0
0 < 3
→ Placement
```

```text
C:
oldIndex = 2
2 < 3
→ Placement
```

最终：

```text
B → reuse + stay
D → reuse + stay
A → reuse + Placement
C → reuse + Placement
```

---
## 二十五、Insertion / Move / Deletion
---
## 新节点
如果 new child 找不到 old Fiber：

```text
create new Fiber
↓
alternate = null
↓
Placement
```

表示：

```text
insert
```

---
## 已有节点，但需要移动
如果：

```text
Fiber 可以 reuse
+
oldIndex < lastPlacedIndex
```

则：

```text
Placement
```

表示：

```text
move
```

所以：

```text
Placement
```

这个 flag 本身可能代表：

```text
新 Fiber
→ insert

旧 identity
→ move
```

---
## 旧节点未被使用
如果 reconciliation 结束后：

```text
existingChildren Map
```

中还有 old Fiber：

```text
→ Deletion
```

因为新 UI 已经不需要它。

---
## 二十六、列表 reconciliation 的统一 mental model
```text
new child
↓
能找到 old Fiber？
│
├─ no
│  ↓
│  new Fiber
│  ↓
│  Placement (insert)
│
└─ yes
   ↓
   type 相同？
   │
   ├─ no
   │  ↓
   │  old → Deletion
   │  new → Placement
   │
   └─ yes
      ↓
      reuse identity
      ↓
      oldIndex < lastPlacedIndex ?
      │
      ├─ yes → Placement (move)
      └─ no  → stay
```

最后：

```text
剩余 old Fiber
→ Deletion
```

---
## 二十七、为什么 `key={index}` 危险
最重要的问题不是：

> DOM 操作多一点。

而是：

> Fiber identity 可能和业务数据错位。

例如：

```text
old:
A B C

key:
0 1 2
```

删除 A：

```text
new:
B C

key:
0 1
```

React看到：

```text
old key=0
new key=0
type 相同
→ reuse
```

于是：

```text
旧 A Fiber
→ 被当成新 B
```

同理：

```text
旧 B Fiber
→ 被当成新 C
```

所以可能出现：

```text
B props
+
A 的旧 Hook state

C props
+
B 的旧 Hook state
```

也就是：

> state 跟错数据。

---
## 二十八、数量不变也可能出问题
例如：

```text
old:
[A, B, C]

new:
[B, A, C]
```

即使数量完全不变，只要使用：

```jsx
key={index}
```

React仍然看到：

```text
key 0:
old A
→ new B
→ reuse

key 1:
old B
→ new A
→ reuse
```

于是：

```text
B 拿到 A 的 state
A 拿到 B 的 state
```

因此问题不在于：

> 数量是否变化。

而在于：

> 数据 identity 是否和 index identity 一致。

---
## 二十九、什么时候 `key={index}` 相对安全
通常需要同时满足：

```text
列表稳定

不会 reorder

不会在中间 insertion

不会 deletion

item identity 本身不依赖位置变化
```

如果这些条件不能保证，更合适的是：

```jsx
key={item.id}
```

因为：

```text
key=index
→ Fiber identity 绑定位置

key=item.id
→ Fiber identity 绑定数据本身
```

---
## 三十、目前已经形成的 Reconciliation mental model
```text
Parent render
↓
产生 new React Elements
↓
和 current child Fibers reconciliation
↓
根据 key 找 candidate
↓
根据 type 判断 identity 是否能 reuse
↓
─────────────────
reuse
→ preserve Fiber identity
→ preserve Hook state

不能 reuse
→ old deletion
→ new mount
→ state reset
─────────────────
↓
列表情况下计算 relative order
↓
lastPlacedIndex
↓
Placement / stay
↓
生成新的 WIP Fiber Tree
+
effect flags
```

这里非常重要：

> reconciliation 还没有真正操作 DOM。

它主要是在 render phase 里回答：

```text
谁被复用
谁新建
谁删除
谁需要移动
```

然后给 Fiber 标记：

```text
Placement
Deletion
Update
...
```

真正的：

```text
DOM insert
DOM move
DOM delete
```

是在后面的 commit phase。

---
## 当前学习状态
这轮可以认为已经比较系统地打通：

```text
React Element
↓
Fiber identity
↓
type / key
↓
Fiber reuse
↓
state preservation
↓
列表 reconciliation
↓
fast path
↓
Map lookup
↓
lastPlacedIndex
↓
Placement / Deletion
↓
index key 的真实问题
```

因此 **reconciliation + key 的核心 mental model 已经基本完成**。

Scheduler 与 Reconciler 交界已经理解到：

```text
Hook Update
↓
Lane
↓
fiber.lanes
↓
childLanes
↓
FiberRoot.pendingLanes
↓
getNextLanes
```

但：

```text
Scheduler priority
sync/concurrent work loop
shouldYield
resume / restart
```

这部分目前主动暂停，暂时不要标记为正式完成。

---
## 下一步
render phase 与 commit phase 的主干已经在 `04 React render phase 与 commit phase.md` 中完成。当前更自然的下一阶段，是把本笔记的 reconciliation 结果接到调度与工作循环：

```text
Scheduler priority
↓
getNextLanes
↓
sync / concurrent work loop
↓
shouldYield
↓
performUnitOfWork / completeUnitOfWork
↓
Placement 如何寻找 Host parent / Host sibling
↓
reconciliation 源码细节
```

重点复盘：

- `getNextLanes` 如何从 pending lanes 中选择下一批工作；
- sync work loop 与 concurrent work loop 的边界；
- `shouldYield` 如何影响可中断 render；
- `Placement`、`Deletion`、`Update` 等 effect flags 如何在 reconciliation 中产生并交给 commit phase；
- Placement 时如何寻找真正的 Host parent 与 Host sibling；
- key、类型变化和 sibling diff 如何映射到源码路径。

这样可以把已经掌握的：

```text
key
→ identity
→ reuse / remount
→ Placement / Deletion / Update
→ effect flags
→ render / commit
```

继续向 `Scheduler` 与 `Reconciler` 的交界推进，而不是重新开一个已经完成的抽象主题。