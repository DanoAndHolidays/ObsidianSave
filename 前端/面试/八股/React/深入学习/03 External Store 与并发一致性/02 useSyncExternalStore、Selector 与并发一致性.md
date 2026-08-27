# 02 useSyncExternalStore、Selector 与并发一致性
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：useSyncExternalStore、snapshot、selector、tearing 与 Zustand 的并发一致性模型。

---
## 整条学习链路
我们这部分实际上走完了这样一条路线：
```text
Context propagation（Context 更新传播）
        ↓
Context splitting（Context 拆分）
        ↓
Context 的能力边界
        ↓
selector subscription（选择器级订阅）
        ↓
External Store（外部 Store）
        ↓
useSyncExternalStore
        ↓
snapshot（快照）
        ↓
immutable snapshot（不可变快照）
        ↓
structural sharing（结构共享）
        ↓
selector + equality（选择器 + 相等性比较）
        ↓
snapshot cache（快照缓存）
        ↓
Concurrent Rendering（并发渲染）
        ↓
tearing（撕裂）
        ↓
useSyncExternalStoreWithSelector
        ↓
Zustand useStore / useShallow
```

其中最重要的认知升级是：

> External Store（外部 Store）的核心不只是“把状态放到 React 外面”，而是建立一套 **React 能安全订阅、读取和比较外部状态版本的协议**。


# 1. 为什么从 Context 走到 External Store

Context 很适合：

```text
Dependency Injection（依赖注入）
```

例如 Tabs：

```tsx
<TabsStoreContext.Provider value={store}>
```

每个 `TabsRoot` 都可以创建自己的 Store：

```text
TabsRoot A → Store A
TabsRoot B → Store B
```

所以：

```text
External Store ≠ Global Store（全局 Store）
```

Context 只负责：

```text
“这个组件应该使用哪一个 Store？”
```

真正的状态订阅交给 Store：

```text
Context
→ Dependency Injection（依赖注入）

Store
→ Reactive Subscription（响应式订阅）
```

这样 Context 中传递的：

```tsx
store
```

实例本身长期不变。

Store 内部：

```text
currentValue:
tab-1 → tab-2
```

不会导致：

```text
TabsStoreContext propagation
```


# 2. 最小 External Store

我们最开始的 Store：

```tsx
type TabsState = {
  currentValue: string
}

function createTabsStore(defaultValue: string) {
  let state: TabsState = {
    currentValue: defaultValue,
  }

  const listeners = new Set<() => void>()

  return {
    getState() {
      return state
    },

    setValue(value: string) {
      if (Object.is(state.currentValue, value)) {
        return
      }

      state = {
        ...state,
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

这里要明确区分三件事：

```text
Store update（Store 更新）
        ↓
subscriber notification（通知订阅者）
        ↓
React render（React 渲染）
```

它们不是同一件事。

Store 可以：

```text
通知 100 个 subscriber
```

但最终可能只有：

```text
2 个组件 render
```

因为 React 可以根据每个组件观察的 snapshot（快照）是否变化决定是否重新渲染。


# 3. `useSyncExternalStore` 的两个核心参数

最基本：

```tsx
useSyncExternalStore(
  subscribe,
  getSnapshot
)
```

可以理解成：

```text
subscribe
→ Store 什么时候发生了可能需要关注的变化？

getSnapshot
→ 当前这个组件观察到的值到底是什么？
```

官方文档也明确要求：`getSnapshot` 返回值没有实际变化时必须保持稳定；React 会根据返回值是否变化决定是否重新渲染。([React][1])


# 4. 第一版 `useTabsStore(selector)`

我们自己写出了：

```tsx
function useTabsStore<T>(
  selector: (state: TabsState) => T
): T {
  const store = useTabsContext()

  return useSyncExternalStore(
    store.subscribe,
    () => selector(store.getState())
  )
}
```

这里最重要的不是代码短，而是：

```tsx
selector(store.getState())
```

出现在了：

```text
getSnapshot
```

这一层。

---
## 4.1 错误方式：render 以后再 selector
例如：

```tsx
const state = useSyncExternalStore(
  store.subscribe,
  store.getState
)

const isActive =
  state.currentValue === value
```

React 实际订阅：

```text
整个 state
```

所以：

```text
oldState !== newState
        ↓
React 已经决定 render
        ↓
render 过程中才计算 isActive
```

假设 100 个 Trigger：

```text
tab-1 → tab-2
```

虽然 `tab-37`：

```text
false → false
```

但它还是先 render 了。

---
## 4.2 selector 进入 snapshot 层
改成：

```tsx
useSyncExternalStore(
  store.subscribe,
  () => store.getState().currentValue === value
)
```

对于 `tab-37`：

```text
old snapshot = false
new snapshot = false

Object.is(false, false)
→ true
```

React可以在：

```text
是否需要 render
```

这一层直接退出。

所以应该记住：

> selector（选择器）必须影响 React 所观察的 snapshot（快照），而不是只影响组件 render 后拿到的数据。


# 5. selector identity（选择器引用）不是最终变化边界

例如：

```tsx
useTabsStore(
  state => state.currentValue === value
)
```

每次 render：

```text
selectorA !== selectorB
```

这是正常的。

但：

```text
selector function identity（选择器函数引用）
```

并不是 React 最终判断 Store 更新是否需要 render 的依据。

例如：

```text
selectorA(S1) → false
selectorB(S1) → false
```

最终 selected snapshot（选择后的快照）仍然：

```text
false → false
```

所以：

```text
Object.is(false, false)
→ true
```

这里应该建立：

```text
selector identity
        ↓
不直接决定 render


selector(storeSnapshot)
        ↓
selected snapshot
        ↓
Object.is(old, new)
        ↓
决定是否因为 Store 更新而 render
```


# 6. 对象 selector 为什么出问题

primitive selector（原始值选择器）：

```tsx
state =>
  state.currentValue === value
```

返回：

```text
true / false
```

天然稳定。

但是：

```tsx
state => ({
  isActive: state.currentValue === value,
  orientation: state.orientation,
})
```

每次：

```text
getSnapshot()
→ object A

getSnapshot()
→ object B
```

即使内容完全一样：

```tsx
Object.is(A, B)
// false
```

React 官方文档直接指出：如果 `getSnapshot` 每次都返回新对象，即使实际数据没变化，也可能形成不断重新渲染的问题；如果数据是可变的，就必须缓存不可变 snapshot。([React][1])

因此问题不只是：

```text
“多 render 一次”
```

而是：

```text
React 无法判断：

Store 到底是真的变化了，
还是 getSnapshot 自己不断制造新对象。
```

### Zustand v5 对稳定 selector 输出的要求
Zustand v5 采用原生 `useSyncExternalStore` 后，selector 若每次返回新的数组、对象或函数，可能触发 `Maximum update depth exceeded`，而不只是多 render 一次。例如：
```tsx
const [searchValue, setSearchValue] = useStore((state) => [
  state.searchValue,
  state.setSearchValue,
]);
```

应改为返回 primitive 或稳定引用，或者使用：
```tsx
const [searchValue, setSearchValue] = useStore(
  useShallow((state) => [
    state.searchValue,
    state.setSearchValue,
  ]),
);
```

自定义 Hook 中的 fallback 也必须稳定；不要在 selector 内反复创建 `() => {}`、`[]` 或 `{}`。〔CR-001〕


# 7. snapshot stability（快照稳定性）

`getSnapshot()` 可以理解成：

> 给 React 一个**可以比较的状态版本观察值**。

理想模型：

```text
Store V1
→ snapshot A

Store 还是 V1
→ snapshot A

Store 还是 V1
→ snapshot A


Store V2
→ snapshot B
```

于是：

```text
Object.is(A, A)
→ 没变化

Object.is(A, B)
→ 发生变化
```

React 的 RFC 同样强调：`getSnapshot` 的结果必须保持 referential stability（引用稳定性）；如果是对象，就需要缓存 / memoize（记忆化）。([GitHub][2])


# 8. 为什么 snapshot 必须 immutable（不可变）

错误：

```tsx
let state = {
  currentValue: "tab-1"
}

state.currentValue = "tab-2"
```

那么：

```tsx
const snapshotA = state

state.currentValue = "tab-2"

const snapshotB = state
```

结果：

```tsx
snapshotA === snapshotB
// true
```

而且更严重：

```text
旧 snapshot A
```

里面的内容已经被未来 mutation（原地修改）污染。

所以它根本不再表示：

```text
“过去某个时刻的状态”
```

正确：

```tsx
state = {
  ...state,
  currentValue: value,
}
```

形成：

```text
S1 → object A
S2 → object B
```


# 9. Structural Sharing（结构共享）

例如：

```tsx
const oldState = {
  currentValue: "tab-1",
  config: configA,
}
```

只更新：

```text
currentValue
```

应该：

```tsx
const newState = {
  ...oldState,
  currentValue: "tab-2",
}
```

于是：

```tsx
oldState !== newState
```

但是：

```tsx
oldState.config === newState.config
```

应该继续为：

```text
true
```

所以：

```text
Immutable snapshot（不可变快照）
→ 保证变了能被检测出来
→ correctness（正确性）


Structural Sharing（结构共享）
→ 没变的部分保持引用
→ performance（性能）
```

这是两层不同职责。


# 10. equalityFn（相等性函数）的真正作用

假设：

```tsx
const previous = {
  active: false,
  orientation: "horizontal",
}

const next = {
  active: false,
  orientation: "horizontal",
}
```

虽然：

```tsx
Object.is(previous, next)
// false
```

但是：

```tsx
shallow(previous, next)
// true
```

那么我们希望：

```text
不要 return next
```

而是：

```text
return previous
```

于是 React 最终看到：

```tsx
Object.is(previous, previous)
// true
```

所以非常重要的一句话：

> equalityFn（相等性函数）的作用，是把**语义相等**转换成 React 能识别的**引用相等**。


# 11. selector cache（选择器缓存）

我们最终推导出了两个 cache：

```text
memoizedStoreSnapshot
memoizedSelection
```

它们形成一个关系：

```text
Store Snapshot
      ↓
selector
      ↓
Selection
```

可以抽象成：

```text
S1 / A
```

Store 更新后有三种情况。

### 情况 1：Store 没变
```text
S1 / A
↓
S1 / A
```

直接：

```text
return A
```

连 selector 都不需要重新执行。


### 情况 2：Store 变了，但 selection 没变
```text
S1 / A
↓
S2 / A
```

例如：

```text
theme 改变
```

但 selector：

```tsx
state => state.currentValue === value
```

仍然：

```text
false
```

应该：

```text
memoizedStoreSnapshot = S2
memoizedSelection = A
```

注意：

```text
Store snapshot 必须推进到 S2
```

即便 selection 没变化。


### 情况 3：两者都变化
```text
S1 / A
↓
S2 / B
```

则同时更新。


# 12. 为什么一定使用传入的 `nextStoreSnapshot`

我们写过：

```tsx
function memoizedSelector(
  nextStoreSnapshot: TabsState
) {
  const nextSelection =
    selector(nextStoreSnapshot)
}
```

你当时问：

> 为什么不用 `selector(store.getState())`？

因为：

```text
memoizedSelection
```

必须严格对应：

```text
memoizedStoreSnapshot
```

假设：

```text
React 拿到 S1
```

准备：

```tsx
memoizedSelector(S1)
```

这时候 Store：

```text
S1 → S2
```

如果内部重新：

```tsx
selector(store.getState())
```

可能算的是：

```text
selector(S2)
```

但是你又缓存：

```text
memoizedStoreSnapshot = S1
```

最后得到错误关系：

```text
Snapshot = S1
Selection = selector(S2)
```

正确 invariant（约束）应该始终是：

```text
memoizedSelection
语义上对应
selector(memoizedStoreSnapshot)
```

这其实就是 snapshot consistency（快照一致性）的局部版本。


# 13. `useEffect + subscribe + setState` 为什么不够

一种很自然的实现：

```tsx
function useStore(store) {
  const [state, setState] =
    useState(() => store.getState())

  useEffect(() => {
    return store.subscribe(() => {
      setState(store.getState())
    })
  }, [store])

  return state
}
```

存在：

```text
render:
读取 V1

        ↓

Store:
V1 → V2

        ↓

useEffect:
现在才 subscribe
```

也就是：

```text
read/check
   ↓
Store update
   ↓
subscribe
```

之间存在 race condition（竞态窗口）。

`V1 → V2` 发生时：

```text
listener 还不存在
```

所以可能漏通知。


# 14. 换 `useLayoutEffect` 为什么仍然不彻底

时序大致：

```text
Render Phase（渲染阶段）
        ↓
Commit Phase（提交阶段）
        ↓
真实 DOM mutation（DOM 修改）
        ↓
useLayoutEffect
        ↓
Browser Paint（浏览器绘制）
        ↓
useEffect
```

所以：

```text
commit ≠ paint
```

`useLayoutEffect` 执行的时候：

```text
DOM 已经修改
```

只是浏览器通常还没有 paint（绘制）。

因此它可以：

```text
错误 UI commit
↓
layout effect 发现
↓
同步修正
↓
paint
```

用户可能看不到闪烁。

但是：

> 错误结果依然已经进入过 commit（提交）。


# 15. tearing（撕裂）

Concurrent Rendering（并发渲染）的关键能力：

```text
render 可以：

暂停
继续
重做
丢弃
```

它不等于：

```text
多线程同时执行 React
```

核心是：

```text
render work（渲染工作）
可以被中断。
```

例如：

```text
Store = V1

Render 开始

Component A
→ 读取 V1

──── React 暂停 ────

Store:
V1 → V2

──── React 恢复 ────

Component B
→ 读取 V2
```

于是同一次候选 UI：

```text
A = V1
B = V2
```

这就是：

```text
tearing（撕裂）
```

即：

> 同一次 render（渲染）中不同部分观察到了不同时间点的外部状态。


# 16. tearing 的正确解决模型

不是：

```text
React render
↓
锁住 Store
↓
禁止更新
```

而是：

```text
Render R1
基于 V1
        ↓

Store:
V1 → V2
        ↓

React 发现 R1
使用的 snapshot 已经过期
        ↓

R1 ❌ 不作为有效结果提交
        ↓

重新基于 V2 render
        ↓

Commit V2
```

可以类比：

```text
Optimistic Concurrency Control
（乐观并发控制）
```

即：

```text
允许数据变化
↓
提交前验证
↓
版本不对就重试
```

而不是：

```text
全程加锁
```


# 17. `useSyncExternalStore` 首先是 correctness API（正确性 API）

这点非常重要。

它不是单纯：

```text
一个方便 subscribe 的 Hook
```

也不是：

```text
性能优化 Hook
```

它首先给 React 一套协议：

```text
subscribe
+
getSnapshot
```

React因此知道：

```text
这个组件依赖 external snapshot（外部快照）
```

可以把它纳入 React 自己的 render / commit（渲染 / 提交）一致性处理中。

RFC 设计 `useSyncExternalStore` 的目的之一，就是让外部数据源能够兼容 Concurrent Rendering（并发渲染）能力。([GitHub][2])


# 18. render 中修改 ref 到底什么时候危险

我们后来把一个过度简化的规则纠正了。

错误理解：

```text
render 中修改 ref
→ 一律错误
```

更准确应该是：

> 要看这个 ref 的**语义是什么**。

---
## 18.1 危险情况：committed state（已提交状态）
例如：

```tsx
ref.current = selected
```

如果 `ref.current` 被定义为：

```text
“上一次真正 commit 的 selection”
```

那么 speculative render（推测性渲染）不能修改它。

因为：

```text
Committed UI = A

开始 Render B

ref.current = B

Render B 最后被丢弃
```

此时：

```text
UI = A
ref = B
```

ref mutation（ref 修改）不会自动随着 render 被丢弃而回滚。

---
## 18.2 为什么 `useRef` 会出现这个问题
同一个组件实例的不同 render：

```text
Current Render
        ┐
        ├→ 同一个 ref object
        │
WIP Render
        ┘
```

`useRef` 保存的是：

```text
component-instance persistent mutable state
（组件实例级、跨渲染持久存在的可变状态）
```

不是：

```text
render-local state
（单次渲染局部状态）
```


# 19. 但 memoization cache（记忆化缓存）不一样

例如：

```tsx
prev.current = {
  count: 2
}
```

如果这个 ref 的语义只是：

```text
“最近一次 selector 算出来的、
用来 shallow 比较的缓存”
```

那么：

```text
Render B 没 commit
```

并不意味着：

```text
cache 必须回滚
```

假设：

```text
cache = { count: 2 }
```

下一次重新计算：

```text
next = { count: 1 }
```

shallow：

```text
false
```

于是 cache 自然更新成：

```text
{ count: 1 }
```

这里要求的是：

```text
语义正确
```

而不是：

```text
缓存永远必须和 committed UI 对齐
```

所以真正应该警惕的是：

```text
render 中修改一个具有

committed semantics（已提交语义）
或
externally observable semantics（外部可观察语义）

的 mutable value（可变值）
```

而不是看到：

```tsx
ref.current = ...
```

就机械判错。


# 20. React `useSyncExternalStoreWithSelector` 源码结构

React 当前源码确实采用了我们推导出的双层结构。

源码首先用一个 `ref` 保存“当前已经 render/commit 接受过的 selection”，然后用 `useMemo` 创建一套 closure-local cache（闭包局部缓存）。源码注释还明确解释：selector memo 状态故意不用 `useRef`，因为 ref 会被并发副本共享。([GitHub][3])

按源码逻辑改写，可以理解成：

```tsx
function useExternalStoreWithSelector(
  subscribe,
  getSnapshot,
  selector,
  isEqual
) {
  // 第一层：
  // 已经被 React 接受过的 selection
  const committedRef = useRef({
    hasValue: false,
    value: undefined,
  })

  // 第二层：
  // 当前 selector 对应的局部 memo cache
  const getSelectedSnapshot = useMemo(() => {
    let hasMemo = false
    let previousSnapshot
    let previousSelection

    return () => {
      const snapshot = getSnapshot()

      // 第一次执行
      if (!hasMemo) {
        hasMemo = true
        previousSnapshot = snapshot

        const nextSelection =
          selector(snapshot)

        if (
          committedRef.current.hasValue &&
          isEqual?.(
            committedRef.current.value,
            nextSelection
          )
        ) {
          previousSelection =
            committedRef.current.value

          return previousSelection
        }

        previousSelection = nextSelection
        return nextSelection
      }

      // Store snapshot 没变
      if (
        Object.is(
          previousSnapshot,
          snapshot
        )
      ) {
        return previousSelection
      }

      const nextSelection =
        selector(snapshot)

      // Store 变了，
      // selection 语义没变
      if (
        isEqual?.(
          previousSelection,
          nextSelection
        )
      ) {
        previousSnapshot = snapshot
        return previousSelection
      }

      // 两者都变
      previousSnapshot = snapshot
      previousSelection = nextSelection

      return nextSelection
    }
  }, [getSnapshot, selector, isEqual])

  const selection =
    useSyncExternalStore(
      subscribe,
      getSelectedSnapshot
    )

  useEffect(() => {
    committedRef.current.hasValue = true
    committedRef.current.value =
      selection
  }, [selection])

  return selection
}
```

这份是**按源码职责重新写的教学版**，但结构基本就是我们自己一步一步推出来的：`instRef` 保存已经接受的 selection，`useMemo` 里的 closure 保存 `hasMemo / memoizedSnapshot / memoizedSelection`。React 当前源码就在做这两层工作。([GitHub][3])


# 21. closure cache 和 committed cache 的区别

这是这段源码最重要的一点。

---
## closure-local memo（闭包局部缓存）
```text
memoizedSnapshot
memoizedSelection
```

表达：

```text
S1 → selection A
```

它是一条：

```text
纯计算缓存关系
```

即：

```text
selector(S1) ≈ A
```

它并不承诺：

```text
A 已经 commit
```

---
## committed selection（已提交选择结果）
```text
instRef.value
```

表达：

```text
React 上一次真正接受的 selection
```

所以它在：

```text
effect
```

之后更新。

这两个 cache 不能混为一谈。


# 22. 为什么 closure cache 不一定需要“回滚”

我们后来纠正过一个误区：

```text
Render R1 使用 closure A
↓
R1 暂停
↓
Store 更新
↓
R1 被丢弃
```

这里：

```text
R1 被丢弃
```

不等于：

```text
closure A 一定被销毁
```

Render work（渲染工作）与 closure 生命周期不是一一对应的。

更关键的是，即使 closure 计算过：

```text
S2 → true
```

而那次 UI 没 commit：

```text
这个缓存关系仍然可能是正确的
```

因为它只是：

```text
selector(S2) === true
```

并没有声称：

```text
UI 已经 commit 到 true
```

所以纯计算 cache 和 committed state 必须区分。


# 23. Zustand 当前 `useStore` 为什么这么薄

当前 Zustand 的 React `useStore` 核心只有一层：

```text
api.subscribe
+
selector(api.getState())
+
useSyncExternalStore
```

它还用 `getInitialState` 处理初始 / 服务端相关 snapshot。源码目前大约就是这个职责结构。([GitHub][4])

按源码逻辑简化：

```tsx
function useStore(
  api,
  selector = state => state
) {
  const slice = useSyncExternalStore(
    api.subscribe,

    () =>
      selector(api.getState()),

    () =>
      selector(api.getInitialState())
  )

  return slice
}
```

Zustand 默认把：

```text
snapshot consistency（快照一致性）
```

交给：

```text
React.useSyncExternalStore
```

自己只负责：

```text
Store API
+
selector
```


# 24. Zustand 为什么不用要求 selector `useCallback`

例如：

```tsx
useStore(
  state => state.currentValue === value
)
```

selector 每次 render 可能都是新函数。

没关系。

因为：

```text
selector identity
```

不是 selected snapshot（选择结果快照）。

真正决定：

```text
Store 更新是否使组件 render
```

的是：

```text
getSnapshot 最终返回值
```

例如：

```text
false → false
```

仍然：

```tsx
Object.is(false, false)
// true
```


# 25. `subscribe` identity（订阅函数引用）反而需要关注

这个和 selector 不一样。

React 文档明确说明：

如果 render 之间传入不同的 `subscribe` 函数，React 会重新订阅；所以稳定的 `subscribe` 可以避免无意义的 unsubscribe / subscribe。([React][1])

Zustand：

```tsx
api.subscribe
```

本身就是 Store 实例上的稳定方法。

所以不会因为：

```text
selectorA → selectorB
```

就重新建立 Store subscription（订阅）。


# 26. Zustand `useShallow`

Zustand 当前源码非常短，核心就是：

```text
用 ref 保存 previous result
↓
执行 selector
↓
shallow(prev, next)
↓
相等：
返回 prev

不等：
缓存 next
返回 next
```

源码确实使用了一个 `useRef` 来保存前一次结果。([GitHub][5])

按逻辑改写：

```tsx
function useShallow(selector) {
  const previousRef = useRef()

  return state => {
    const next =
      selector(state)

    if (
      shallow(
        previousRef.current,
        next
      )
    ) {
      return previousRef.current
    }

    previousRef.current = next
    return next
  }
}
```

官方文档同样建议：当 selector 产生新对象 / 数组，但 shallow comparison（浅比较）结果没有变化时，可以用 `useShallow` 防止无意义重新渲染。([GitHub][6])


# 27. `useShallow` 的真正作用链

普通：

```tsx
state => ({
  count: state.count,
  name: state.name,
})
```

Store只改变：

```text
theme
```

则：

```text
old result = A
new result = B

A !== B
```

React：

```text
Object.is(A, B)
→ false
→ render
```

使用 `useShallow`：

```text
selector
↓
B

shallow(A, B)
↓
true

return A
```

React最终看到：

```text
old snapshot = A
new snapshot = A

Object.is(A, A)
→ true
```

所以：

```text
useShallow
```

不是让 React 改成 shallow 比较。

React最后仍然：

```text
Object.is
```

而是：

> `useShallow` 在 React 比较之前，把“浅层语义相等”转换成“同一个对象引用”。


# 28. 三个 selector 示例

Store：

```tsx
old = {
  count: 1,
  name: "Dano",
  theme: "light",
}

new = {
  count: 1,
  name: "Dano",
  theme: "dark",
}
```

---
## A
```tsx
state => state.count
```

得到：

```text
old snapshot = 1
new snapshot = 1

Object.is(1, 1)
→ true
```

不 render。

---
## B
```tsx
state => ({
  count: state.count,
  name: state.name,
})
```

得到：

```text
old = object A
new = object B

Object.is(A, B)
→ false
```

render。

---
## C
```tsx
useShallow(
  state => ({
    count: state.count,
    name: state.name,
  })
)
```

内部：

```text
selector → object B

shallow(A, B)
→ true

return A
```

React最终：

```text
A → A

Object.is(A, A)
→ true
```

不 render。


# 29. 当前阶段最值得留下的 10 个结论

1. **Context splitting（Context 拆分）解决的是粗粒度订阅边界；selector（选择器）解决的是细粒度订阅。**

2. **Context 可以做 Dependency Injection（依赖注入），Store 做 Reactive Subscription（响应式订阅）。**

3. **selector 必须进入 `getSnapshot` 层，才能参与 React “要不要 render”的判断。**

4. **React最终关心的是 selected snapshot（选择后的快照），不是 selector function identity（选择器函数引用）。**

5. **`getSnapshot()` 在 Store 没变化时必须返回稳定结果。**

6. **Immutable snapshot（不可变快照）首先是 correctness（正确性）要求；Structural Sharing（结构共享）再进一步优化 performance（性能）。**

7. **equalityFn（相等性函数）的本质，是把语义相等转换成引用相等。**

8. **Concurrent Rendering（并发渲染）意味着 render 可以暂停、重做、丢弃；执行过不代表一定 commit。**

9. **`useSyncExternalStore` 首先解决 external snapshot consistency（外部快照一致性），不是单纯的性能问题。**

10. **不要机械记“render 里不能改 ref”，而要判断这个 mutable value（可变值）是否具有 committed semantics（已提交语义）或 externally observable semantics（外部可观察语义）。**

最后可以用一张图把这一阶段压缩下来：

```text
                External Store
                      │
       ┌──────────────┴──────────────┐
       │                             │
  subscribe                     getSnapshot
“什么时候变了”                  “我现在看到什么”
       │                             │
       └──────────────┬──────────────┘
                      ↓
           useSyncExternalStore
                      │
             snapshot comparison
             （快照比较）
                      │
                 Object.is
                      │
              ┌───────┴───────┐
            same            changed
              │                 │
          skip render        render


selector 加入以后：

Store Snapshot
      ↓
   selector
      ↓
Selected Snapshot
      ↓
  equality / shallow
      ↓
稳定引用
      ↓
useSyncExternalStore
      ↓
Object.is
```

这份笔记已经覆盖了我们这轮从 **Context 能力边界 → selector → External Store → `useSyncExternalStore` → snapshot / equality → tearing → Concurrent Rendering 基础 → React selector 源码 → Zustand** 的主要内容。下一次可以直接从这里往后进入 `startTransition`，不用再重新铺 External Store。

[1]: https://react.dev/reference/react/useSyncExternalStore "useSyncExternalStore – React"
[2]: https://github.com/reactjs/rfcs/blob/main/text/0214-use-sync-external-store.md?utm_source=chatgpt.com "rfcs/text/0214-use-sync-external-store.md at main · reactjs/rfcs · GitHub"
[3]: https://github.com/facebook/react/blob/main/packages/use-sync-external-store/src/useSyncExternalStoreWithSelector.js "react/packages/use-sync-external-store/src/useSyncExternalStoreWithSelector.js at main · react/react · GitHub"
[4]: https://github.com/pmndrs/zustand/blob/main/src/react.ts "zustand/src/react.ts at main · pmndrs/zustand · GitHub"
[5]: https://github.com/pmndrs/zustand/blob/main/src/react/shallow.ts "zustand/src/react/shallow.ts at main · pmndrs/zustand · GitHub"
[6]: https://github.com/pmndrs/zustand/blob/main/docs/learn/guides/prevent-rerenders-with-use-shallow.md?utm_source=chatgpt.com "zustand/docs/learn/guides/prevent-rerenders-with-use-shallow.md at main · pmndrs/zustand · GitHub"

---
## 内容审核变更记录
### CR-001｜补充说明
- 日期：8/25/2026
- 位置：`对象 selector 为什么出问题` 后的 `Zustand v5 对稳定 selector 输出的要求`
- 原内容：只说明对象 selector 会让 `getSnapshot` 不稳定，并可能不断重新渲染。
- 调整后：补充 Zustand v5 中新数组、对象或函数 selector 可能导致无限更新，并给出 `useShallow` 与稳定 fallback 的修正方式。
- 原因：Zustand v5 对 selector 输出稳定性提出了迁移约束，风险高于一般的额外 render。
- 依据：[Zustand：Migrating to v5](https://zustand.docs.pmnd.rs/migrations/migrating-to-v5#requiring-stable-selector-outputs)；[Zustand：Prevent rerenders with useShallow](https://zustand.docs.pmnd.rs/guides/prevent-rerenders-with-use-shallow)

