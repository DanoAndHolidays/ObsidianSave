# 4 store
> Last Format Time：8/24/2026 15:33:00

---
## Context 拆分解决的是什么
原生 `useContext` 订阅的是整个 Context value：

```ts
const context = useContext(TabsContext)
```

如果 Provider：

```tsx
<TabsContext.Provider
  value={{
    currentValue,
    setValue,
    orientation,
  }}
>
```

只要整个 `value` 的 identity 变化，所有消费这个 Context 的组件都会收到更新。

例如：

```text
currentValue:
tab-1 → tab-2
```

即使 `TabsList` 只使用 `orientation`，也可能因为 Context propagation 重新 render。

因此可以拆分：

```ts
TabsValueContext
TabsActionsContext
TabsConfigContext
```

目的不是“Context 越多越好”，而是：

> 缩小一次 Context 更新影响的 consumer 集合。

---
## Context 什么时候值得拆
主要看四件事：

```text
1. 更新频率
2. Consumer 集合是否重叠
3. 被隔离组件的 render 成本
4. 拆分后的维护复杂度
```

其中非常重要的是：

> 更新频率只能告诉我们“这个状态值不值得关注”，Consumer 集合决定“拆 Context 能不能真正减少 render”。

例如：

```text
currentValue consumers:
Trigger
Content
Indicator

focusedValue consumers:
Trigger
FocusRing
```

共同 consumer 只有 `Trigger`，所以拆开后可以明显隔离 `Content / Indicator / FocusRing`，拆分价值较高。

反过来，如果：

```text
Consumer(A) = { X, Y, Z }
Consumer(B) = { X, Y, Z }
```

即使 A 高频、B 几乎不变，拆成两个 Context：

```text
A 改变
→ X Y Z 还是全部 render
```

收益很低。

---
## Context 拆分的能力边界
假设：

```tsx
function TabsTrigger({ value }) {
  const currentValue = useContext(TabsValueContext)

  const isActive = currentValue === value
}
```

有 100 个 Trigger：

```text
tab-1
tab-2
...
tab-100
```

当：

```text
currentValue:
tab-1 → tab-2
```

真正 UI 状态发生改变的只有：

```text
Trigger(tab-1)
true → false

Trigger(tab-2)
false → true
```

其余 98 个都是：

```text
false → false
```

但是它们全部订阅：

```ts
TabsValueContext
```

因此 Context propagation 仍会让 100 个 Trigger render。

---
## `memo` 为什么解决不了
即使：

```tsx
const TabsTrigger = memo(function TabsTrigger() {
  const currentValue = useContext(TabsValueContext)
})
```

也没用。

因为这里不是：

```text
Parent render
→ props 改变
→ Child render
```

而是：

```text
Context 更新
→ Context consumer 自己收到更新
→ render
```

`memo` 主要阻挡的是父组件带来的 props render propagation，不能阻止组件自身消费的 Context 更新。

---
## Trigger 真正想订阅的并不是 `currentValue`
对于：

```tsx
<TabsTrigger value="tab-37" />
```

它并不真正关心：

```ts
currentValue
```

它只关心：

```ts
currentValue === 'tab-37'
```

也就是：

```ts
isActive: boolean
```

所以理想订阅模型是：

```text
不是：

Trigger37
→ 订阅 currentValue

而是：

Trigger37
→ 订阅 isActive
```

这样：

```text
tab-1 → tab-2
```

对 `Trigger37`：

```text
false → false
```

就不需要 render。

这就是 **selector 级订阅**。

---
## Context splitting 和 selector 的区别
可以理解成两个层级：

```text
Context splitting
↓
不要让我订阅“不属于我”的那类状态
```

例如：

```text
ValueContext
ActionsContext
ConfigContext
```

而 selector：

```text
即使大家都需要同一份 state，
每个组件也只订阅自己真正关心的结果
```

例如：

```ts
state => state.currentValue === value
```

所以：

```text
Context splitting
= 粗粒度订阅边界

selector
= 细粒度订阅
```

---
## 为什么会引入 Store
可以创建一个局部 store：

```ts
function createTabsStore(defaultValue: string) {
  let state = {
    currentValue: defaultValue,
  }

  const listeners = new Set<() => void>()

  return {
    getState() {
      return state
    },

    setValue(value: string) {
      if (Object.is(state.currentValue, value)) return

      state = {
        currentValue: value,
      }

      listeners.forEach(listener => listener())
    },

    subscribe(listener: () => void) {
      listeners.add(listener)

      return () => {
        listeners.delete(listener)
      }
    },
  }
}
```

核心 API：

```text
getState()
→ 获取当前 snapshot

subscribe(listener)
→ 注册订阅者

setValue()
→ 更新 state + notify subscribers
```

---
## External Store 不等于 Global Store
Store 完全可以是每一个 Tabs 实例自己的：

```text
TabsRoot A
→ store A

TabsRoot B
→ store B
```

可以通过 Context 传递 store：

```tsx
<TabsStoreContext.Provider value={store}>
  {children}
</TabsStoreContext.Provider>
```

这里 Context 传递的是一个生命周期内稳定的：

```ts
store
```

而不是：

```ts
{
  currentValue
}
```

所以：

```text
currentValue 改变
```

但：

```ts
oldStore === newStore
```

Context value 没变，因此：

```text
不会发生 TabsStoreContext propagation
```

此时 Context 的职责发生变化：

```text
以前：
Context 负责传播状态变化

现在：
Context 只负责告诉组件：
“你属于哪个 Tabs store？”
```

可以概括成：

> **Context 负责 Dependency Injection，Store 负责 Reactive Subscription。**

---
## “subscriber 被通知” ≠ “组件 render”
这是 Store 模型非常关键的一点。

Store 更新：

```ts
listeners.forEach(listener => listener())
```

可能会通知 100 个 subscriber。

但通知的含义只是：

> Store 可能变了，你检查一下自己关心的数据。

不是：

> 你必须 render。

例如：

```ts
Trigger37 selector:
state => state.currentValue === 'tab-37'
```

更新：

```text
tab-1 → tab-2
```

它收到通知，但 selector：

```text
old = false
new = false
```

所以：

```text
无需 render
```

而：

```text
Trigger1:
true → false
render

Trigger2:
false → true
render
```

最终可能是：

```text
100 次 subscriber 通知
100 次轻量 selector 检查

只有 2 次 React render
```

所以：

```text
notify
≠
render
```

---
## useSyncExternalStore
可以把它理解成 React 和 external store 之间的桥梁：

```ts
useSyncExternalStore(
  subscribe,
  getSnapshot
)
```

两个核心职责：

```text
subscribe
→ Store 变化时怎么通知 React？

getSnapshot
→ 这个组件当前观察到的数据是什么？
```

例如：

```ts
const isActive = useSyncExternalStore(
  store.subscribe,
  () => store.getState().currentValue === value
)
```

对于 `Trigger37`：

```text
tab-1 → tab-2

oldSnapshot = false
newSnapshot = false
```

React 判断：

```ts
Object.is(false, false) === true
```

因此不 render。

---
## Selector 必须发生在 render 判断之前
下面两种写法性能模型完全不同。

### ❌ 订阅整个 state
```ts
const state = useSyncExternalStore(
  store.subscribe,
  store.getState
)

const isActive = state.currentValue === value
```

更新时：

```text
oldState !== newState
↓
React 先决定 render
↓
render 之后才计算 isActive
```

100 个 Trigger 都订阅整个 state，因此可能全部 render。


### ✅ snapshot 本身就是 selector 结果
```ts
const isActive = useSyncExternalStore(
  store.subscribe,
  () => store.getState().currentValue === value
)
```

流程：

```text
Store update
↓
先计算新的 isActive
↓
比较 old / new snapshot
↓
真的变了才 render
```

所以 selector 必须进入：

> React 判断“是否需要 render”的这一层。

---
## Store 应该保存 Source of Truth，而不是派生状态
推荐：

```ts
type TabsState = {
  currentValue: string
}
```

然后：

```ts
state => state.currentValue === value
```

派生 `isActive`。

不推荐：

```ts
type TabsState = {
  currentValue: string

  activeMap: {
    [value: string]: boolean
  }
}
```

因为：

```text
currentValue
+
activeMap
```

变成两份需要保持同步的状态。

例如：

```text
tab-1 → tab-2
```

还需要同时：

```text
activeMap.tab1 = false
activeMap.tab2 = true
```

容易出现状态不一致。

原则：

> **能够从 source of truth 推导出的数据，通常不要再存第二份 state。**

---
## Selector 返回对象时的 identity 问题
下面 selector：

```ts
state => ({
  isActive: state.currentValue === value,
})
```

每次都会创建新对象：

```ts
{} !== {}
```

所以即使：

```text
false → false
```

结果对象 identity 仍然变化。

因此：

```ts
state => state.currentValue === value
```

这种 primitive selector 最简单：

```ts
Object.is(false, false) === true
```

---
## selector + equalityFn
如果确实需要一次选择多个值：

```ts
state => ({
  isActive: state.currentValue === value,
  orientation: state.orientation,
})
```

可以配合：

```text
shallow equality
```

例如：

```text
old:
{
  isActive: false,
  orientation: "horizontal"
}

new:
{
  isActive: false,
  orientation: "horizontal"
}
```

虽然：

```ts
old !== new
```

但 shallow compare：

```text
false === false
"horizontal" === "horizontal"
```

所以可以认为 selected slice 没变。

---
## shallow equality 只能比较第一层
如果：

```ts
state => ({
  isActive,
  config: {
    orientation: state.orientation,
  },
})
```

每次 selector 都创建新的 `config`：

```ts
old.config !== new.config
```

即使里面：

```text
orientation:
horizontal === horizontal
```

普通 shallow equality 仍然会认为不相等。

因此 selector 输出通常应该尽量：

```text
扁平
引用稳定
shallow-friendly
```

---
## Structural Sharing
假设：

```ts
type State = {
  currentValue: string
  config: {
    orientation: string
  }
}
```

更新：

```ts
state = {
  ...state,
  currentValue: 'tab-2',
}
```

会得到：

```ts
oldState !== newState
```

但：

```ts
oldState.config === newState.config
```

因为 `config` 没有变化，所以继续复用旧对象。

原则：

```text
发生变化的节点
→ 创建新 identity

没有变化的节点
→ 保持原 identity
```

这叫 **Structural Sharing（结构共享）**。

好处是 selector + equality 可以利用引用稳定性快速判断：

```text
这一部分没有变化
```

---
## Immutable update 不等于“全部创建新对象”
错误理解：

```text
immutable
=
每次所有对象都重新创建
```

实际上应该：

```text
只重新创建发生变化的路径
```

例如：

```ts
state = {
  currentValue: value,
  config: {
    ...state.config,
  },
}
```

如果 `config` 根本没变，却重新创建：

```ts
oldState.config !== newState.config
```

那么订阅：

```ts
state => state.config
```

的组件会产生不必要更新。

所以：

> **Immutable update 的重点不是创建尽可能多的新对象，而是准确地改变引用。**

---
## Snapshot 为什么必须不可变
`snapshot` 可以理解成：

> **外部 Store 在某一个时间点的固定观察结果。**

例如：

```ts
const snapshot1 = store.getState()

store.setValue('tab-2')

const snapshot2 = store.getState()
```

我们希望：

```text
snapshot1
永远代表 t1

snapshot2
永远代表 t2
```

不能更新 store 后：

```text
snapshot1 内部的数据也偷偷变成 t2
```

否则 React 就无法可靠比较：

```text
上一次观察到的状态
vs
这一次观察到的状态
```

因此：

> **Immutable snapshot 首先保证 correctness；Structural Sharing 再进一步帮助 performance。**

---
## 嵌套 Set / Map 也要注意 mutation
例如：

```ts
state.disabledValues.add('tab-3')

state = {
  ...state,
}
```

虽然：

```ts
oldState !== newState
```

但是：

```ts
oldState.disabledValues === newState.disabledValues
```

而且旧 snapshot 中的 Set 也已经被修改。

这会污染旧 snapshot。

正确做法：

```ts
state = {
  ...state,
  disabledValues: new Set([
    ...state.disabledValues,
    'tab-3',
  ]),
}
```

保证：

```ts
oldSet !== newSet
```

以及旧 snapshot 保持原状。

---
## 最终模型
可以把整条学习链整理成：

```text
原生 Context
↓
所有 consumer 订阅整个 Context value

Context Splitting
↓
隔离不同类型的 consumer
↓
解决“我根本不需要这个状态，却被连带更新”

但大量组件仍然订阅同一个高频 state
↓
Context 到达能力边界

External Store
↓
Context 只传稳定的 store instance

subscribe
↓
通知 subscriber：Store 可能变化了

selector
↓
计算组件真正关心的 slice

equality
↓
selected slice 真变了吗？

没变
→ skip render

变了
→ React render
```

核心区分可以记成一句：

> **Context splitting 解决“订阅哪一类状态”，selector store 解决“订阅同一类状态时，我到底关心其中什么”。**

再进一步：

> **Store update ≠ subscriber notification ≠ React render。**

三者是三个不同阶段。
