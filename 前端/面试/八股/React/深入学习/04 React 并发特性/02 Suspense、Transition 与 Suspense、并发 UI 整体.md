# 02 Suspense、Transition 与 Suspense、并发 UI 整体
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：Suspense、Transition、retry、reveal 和 pending UI 的并发渲染整体模型。

---
## Concurrent Rendering 的核心目标
Concurrent Rendering 的重点不是：

```text
让 React 算得更快
```

而是：

```text
让 React 更合理地安排工作，
优先保证用户交互响应性。
```

因此需要区分：

```text
urgent update
non-urgent / Transition update
```

### Urgent Update
通常需要立即响应的 UI：

```text
输入框输入
按钮反馈
鼠标/键盘直接交互
```

例如：

```tsx
setKeyword(e.target.value)
```

用户输入必须立刻反映到 input。

### Non-urgent Update
可以稍晚完成的派生 UI：

```text
大型搜索结果
复杂列表
图表
页面切换后的重内容
```

关键不是业务重要性，而是：

> **这个 UI 是否必须立刻跟上用户操作。**


# 2. Responsiveness vs Throughput

Transition 不一定减少：

```text
总计算量
总 render 次数
总 CPU 工作量
```

它主要改善：

```text
responsiveness
```

也就是：

> React 可以先处理更紧急的事情。

所以：

```text
5000 个可以被 React 分割的组件 render
```

可能比：

```text
一个连续执行 500ms 的同步 JS 函数
```

用户体验更好。

因为 React 可以在自己的工作单元之间 yield。


# 3. Cooperative Scheduling

React 使用的是：

```text
cooperative scheduling
```

不是：

```text
preemptive scheduling
```

React不能做到：

```js
function heavy() {
  // 执行到任意 JS 指令时
  // React 突然把它暂停
}
```

如果某段同步 JavaScript 已经开始连续执行：

```js
heavyCalculation()
```

React必须等 JavaScript 控制权返回。

因此：

> **React只能中断自己掌控的 render work，而不能任意暂停同步 JavaScript。**


# 4. Interruptible Rendering

Concurrent Rendering 允许：

```text
开始 render candidate
↓
发现更高优先级 update
↓
中断
↓
去处理更重要的 update
↓
之后 retry / 放弃原 work
```

所以：

```text
render 开始
≠
render 一定完成
≠
一定 commit
```

这就是 speculative rendering：

```text
React 可以尝试未来 UI，
最后却完全不让用户看到它。
```


# 5. Render 和 Commit

这是整个 Concurrent React 最核心的前提：

```text
render
≠
commit
```

Render：

```text
计算未来 UI
构造 candidate
```

Commit：

```text
真正把结果应用到 DOM / 屏幕
```

因此可能：

```text
render B
↓
被打断
↓
放弃
```

用户仍然只看到了：

```text
A
```


# 6. React State 是 Snapshot

例如：

```tsx
setCount(1)
```

不是：

```js
count = 1
```

更接近：

```text
enqueue 一个 update
```

当前 render 已经拿到：

```text
count = 0
```

之后不会因为 `setCount(1)` 而突然变成 1。

后续 render：

```text
读取 update queue
↓
计算新的 state
↓
得到新的 snapshot
```

因此：

```text
update enqueue
≠
update render
≠
update commit
```


# 7. startTransition

```tsx
startTransition(() => {
  setSearchKeyword(keyword)
})
```

最重要的误区：

```text
startTransition callback
不是异步 callback
```

它依然立即同步执行。

例如：

```tsx
startTransition(() => {
  console.log("A")
  setValue("B")
  console.log("C")
})
```

`A`、`setValue`、`C` 都同步执行。

真正发生的是：

> callback 中产生的 React update 被标记成 Transition / non-urgent update。

因此：

```tsx
startTransition(() => {
  heavySyncCalculation()
})
```

不会解决同步 JS 阻塞问题。


# 8. stale UI

Concurrent React 允许：

```text
latest value
```

和：

```text
currently displayed value
```

暂时不同。

例如：

```text
input:
"react suspense"

ProductList:
仍然显示 "react" 的结果
```

这可能是：

```text
stale but valid UI
```

不是 incorrect UI。

关键是：

> ProductList 明确代表“最近已经完成的搜索结果”。


# 9. stale UI 和 tearing 不一样

例如：

```text
keyword = "react suspense"
searchKeyword = "react"
```

如果这是设计允许的两个时间版本：

```text
latest
+
stale
```

完全合法。

Tearing 则是：

> 同一个 source of truth，在同一个 candidate UI 中被不同部分观察成不同版本。

因此：

```text
stale UI
≠
tearing
```


# 10. useTransition

```tsx
const [isPending, startTransition] = useTransition()
```

`startTransition`：

```text
标记 Transition update
```

`isPending`：

```text
表示该 Transition 生命周期仍然没有结束
```

非常重要：

```text
callback lifecycle
≠
Transition lifecycle
```

例如：

```tsx
startTransition(() => {
  setPage("B")
})
```

callback 可能瞬间执行结束：

```text
callback finished
```

但是：

```text
render B
↓
suspend
↓
等待
```

Transition 仍然：

```text
isPending = true
```

所以：

```tsx
page !== targetPage
```

只能表达业务值关系。

不能完整替代：

```tsx
isPending
```


# 11. latest value / stale value

例如搜索：

```tsx
const [keyword, setKeyword] = useState("")
const [searchKeyword, setSearchKeyword] = useState("")
```

可以理解成：

```text
keyword
=
用户当前最新输入
```

```text
searchKeyword
=
搜索结果目前跟进到的版本
```

它们不是简单的“重复 state”。

而是：

> **同一个逻辑值的两个时间版本。**

最终：

```text
keyword === searchKeyword
```

但 Transition 期间可以暂时不同。


# 12. useDeferredValue

```tsx
const deferredKeyword = useDeferredValue(keyword)
```

可以理解：

```text
keyword
=
latest value
```

```text
deferredKeyword
=
允许暂时滞后的版本
```

适合：

```tsx
<ProductList keyword={deferredKeyword} />
```

---
## startTransition vs useDeferredValue
### startTransition
适合：

> **我控制这个 update 的产生。**

```tsx
startTransition(() => {
  setSearchKeyword(value)
})
```

### useDeferredValue
适合：

> **value 已经来到我这里了，但某些 consumer 可以晚一点跟上。**

例如：

```tsx
function SearchResults({ keyword }) {
  const deferredKeyword = useDeferredValue(keyword)
}
```

尤其当：

```text
value 来自 props
```

没有 setter 可以包进 `startTransition` 时，非常自然。


# 13. useDeferredValue vs debounce

这是两种完全不同的机制。

### debounce
```text
time-based
```

例如：

```text
用户停止输入 300ms
↓
发请求
```

核心目标：

```text
降低执行频率
```

适合：

```text
API 请求
搜索请求
昂贵副作用
```

### useDeferredValue / Transition
```text
priority / scheduling based
```

没有：

```text
固定 200ms
固定 500ms
```

核心目标：

```text
降低 React UI 工作的紧急程度
```

一句话：

```text
debounce
=
降低频率
```

```text
Transition / deferred value
=
降低优先级 / 改变调度
```

两者甚至可以一起使用。


# Suspense

# 14. Suspense 是什么

最基本形式：

```tsx
<Suspense fallback={<Loading />}>
  <Profile />
</Suspense>
```

Suspense 不是简单的：

```text
loading component
```

它解决的是：

> **当某部分 UI 在 render 时暂时无法完成，React 应该如何处理这棵 UI。**

基本流程：

```text
render Profile
↓
发现依赖还没 ready
↓
当前 render 无法完成
↓
suspend
↓
向上寻找能够处理此次挂起的最近 Suspense Boundary
↓
由该 Boundary 的 fallback 替换其 children 区域
↓
资源 ready
↓
retry render
↓
成功
↓
commit
```


# 15. Suspense 和手写 loading 的区别

传统：

```tsx
if (loading) {
  return <Skeleton />
}
```

这里对于 React：

```text
组件 render 成功
```

因为：

```tsx
return <Skeleton />
```

就是合法 render result。

React不知道：

```text
Skeleton 只是临时的
组件还在等资源
```


Suspense：

```text
render
↓
资源没有 ready
↓
当前 render 本身无法完成
```

于是 React知道：

> **当前 candidate UI 还没有准备好。**

因此 React renderer 可以参与：

```text
fallback
stale UI
Transition
streaming
reveal coordination
```


# 16. 什么叫“组件没 ready”

一定要区分：

```text
业务数据没 ready
```

和：

```text
React render 没完成
```

例如：

```tsx
if (!data) {
  return <Loading />
}
```

属于：

```text
数据没 ready
但 render 已成功
```

而 Suspense 是：

```text
组件无法完成当前 render
```


# 17. 子组件 suspend 与父组件

假设：

```tsx
function App() {
  return (
    <>
      <Header />
      <Profile />
      <Footer />
    </>
  )
}
```

`App()` 函数执行完得到 children：

```text
Header
Profile
Footer
```

不代表整棵 subtree 已经 render 完成。

React还需要继续处理：

```text
Header
Profile
Footer
```

如果：

```text
Profile suspend
```

没有合适的 Suspense boundary：

```text
这次 subtree render 无法正常形成可 commit 的完整结果
```

因此：

```text
父组件函数执行结束
≠
父 subtree render 完成
```


# 18. Suspense Boundary

例如：

```tsx
<>
  <Header />

  <Suspense fallback={<ProfileSkeleton />}>
    <Profile />
  </Suspense>

  <Footer />
</>
```

如果：

```text
Profile suspend
```

React可以得到：

```text
Header
ProfileSkeleton
Footer
```

因此 Suspense boundary 可以理解为：

> **给暂时无法完成的 subtree 提供一个合法替代 subtree。**


# 19. Suspense 的底层 mental model

历史上最容易理解 Suspense 的方式是：

```js
throw promise
```

更准确说：

```text
throw thenable
```

这是理解模型，不是建议项目中手写的数据获取方式。

概念：

```js
function read() {
  if (status === "pending") {
    throw promise
  }

  if (status === "error") {
    throw error
  }

  return data
}
```

组件：

```tsx
function Profile() {
  const user = resource.read()

  return <div>{user.name}</div>
}
```

如果 pending：

```text
resource.read()
↓
throw thenable
↓
当前控制流结束
↓
Profile suspend
```


# 20. Suspense 不是暂停 JavaScript

这个结论非常重要。

假设：

```tsx
function Profile() {
  console.log("A")

  const user = use(userPromise)

  console.log("B")

  return <div>{user.name}</div>
}
```

第一次 Promise pending：

```text
A
↓
use()
↓
suspend
```

所以只打印：

```text
A
```

Promise ready 后：

React不是：

```text
从 use() 后面恢复
```

而是：

```text
重新调用 Profile()
```

于是：

```text
A
B
```

总日志：

```text
A
A
B
```

因此：

> **suspend = 当前 render attempt 无法完成，然后 retry。**

不是：

> 保存 JavaScript 调用栈，之后 resume。


# 21. 为什么 render 必须纯

因为：

```text
render
↓
suspend
↓
retry
```

可能导致组件函数多次执行。

例如：

```tsx
function Profile() {
  analytics.send("rendered")

  const user = use(promise)

  ...
}
```

可能：

```text
analytics.send()
↓
suspend
↓
retry
↓
analytics.send()
```

因此 render 中不应该放这种副作用。

Concurrent Rendering 下更应该牢记：

```text
render invocation
≠
commit
```


# 22. React `use(promise)`

React 19 的 `use` API 可以：〔CR-001〕

```tsx
function Profile({ userPromise }) {
  const user = use(userPromise)

  return <div>{user.name}</div>
}
```

概念上：

```text
Promise pending
→ 挂起当前 render
```

```text
Promise fulfilled
→ 返回 Promise 的 value
```

```text
Promise rejected
→ 抛出错误，由错误边界处理
```

所以：

```text
             Promise
                │
       ┌────────┼────────┐
       │        │        │
    pending fulfilled rejected
       │        │        │
   Suspense    UI   ErrorBoundary
```


# 23. Suspense 和 Error Boundary

例如：

```tsx
<ErrorBoundary fallback={<ErrorPage />}>
  <Suspense fallback={<Skeleton />}>
    <Profile />
  </Suspense>
</ErrorBoundary>
```

可以表达：

```text
资源 pending
→ Skeleton
```

```text
资源 ready
→ Profile
```

```text
资源 error
→ ErrorPage
```

两者语义：

```text
Suspense:
现在暂时做不到
```

```text
Error Boundary:
发生错误
```


# 24. Promise identity 必须稳定

错误示例：

```tsx
function Profile() {
  const promise = fetch("/api/user").then(r => r.json())

  const user = use(promise)

  return ...
}
```

可能：

```text
render
↓
Promise A
↓
suspend

retry
↓
重新执行组件
↓
Promise B
↓
suspend

retry
↓
Promise C
...
```

因此 Suspense 数据资源通常必须：

```text
cached
stable
reusable across retries
```

这里的“稳定”是指由资源层、框架或缓存提供的 Promise，在同一资源仍未完成时可以跨 retry 复用；并不是要求所有业务代码中的 Promise 都必须全局单例。〔CR-002〕

实际项目通常由：

```text
framework
data cache
Suspense-aware data layer
```

处理。


# 25. Suspense 不等于 fetch

仅仅这样：

```tsx
<Suspense fallback={<Loading />}>
  <User />
</Suspense>
```

而 `User`：

```tsx
useEffect(() => {
  fetch(...)
}, [])
```

不会自动触发 Suspense。

因为：

```text
render
↓
commit
↓
useEffect
↓
fetch
```

Suspense需要：

```text
render 阶段
↓
发现依赖未 ready
↓
suspend
```


# 嵌套 Suspense

# 26. 最重要的规则：找最近 Boundary

例如：

```tsx
<Suspense fallback={<PageSkeleton />}>
  <Profile />

  <Suspense fallback={<PostsSkeleton />}>
    <Posts />
  </Suspense>
</Suspense>
```

结构：

```text
Outer Suspense
│
├── Profile
│
└── Inner Suspense
    └── Posts
```

如果：

```text
Posts suspend
```

寻找：

```text
Posts
↑
Inner Suspense ← 最近
↑
Outer Suspense
```

所以：

```text
Profile
PostsSkeleton
```

Outer 不需要处理。


# 27. Boundary fallback 替换的是整个 children 区域

假设：

```tsx
<Suspense fallback={<PageSkeleton />}>
  <A />
  <B />
  <C />
</Suspense>
```

`B` suspend。

不是：

```text
A
PageSkeleton
C
```

而是：

```text
PageSkeleton
```

因为：

> **哪个 boundary 接住 suspend，就由那个 boundary 的 fallback 替代整个 children 区域。**


# 28. Inner Suspense 的意义

Inner boundary：

```tsx
<Suspense fallback={<PostsSkeleton />}>
  <Posts />
</Suspense>
```

相当于：

> Posts 慢没关系，不要拖累外面的 Profile。

因此：

```text
Profile ready
Posts pending
```

可以：

```text
Profile
PostsSkeleton
```

这就是：

```text
progressive reveal
```


# 29. 没有 Inner Suspense

如果：

```tsx
<Suspense fallback={<PageSkeleton />}>
  <Profile />
  <Posts />
</Suspense>
```

即使：

```text
Profile ready
Posts pending
```

也只能：

```text
PageSkeleton
```

因为 Profile + Posts 是同一个 reveal unit。

等全部 ready：

```text
Profile
Posts
```

一起出现。


# 30. 嵌套 Suspense 四种情况

对于：

```tsx
<Suspense fallback={<PageSkeleton />}>
  <Profile />

  <Suspense fallback={<PostsSkeleton />}>
    <Posts />
  </Suspense>
</Suspense>
```

|Profile|Posts|显示|
|---|---|---|
|ready|ready|Profile + Posts|
|ready|suspend|Profile + PostsSkeleton|
|suspend|ready|PageSkeleton|
|suspend|suspend|PageSkeleton|

因为：

```text
Posts
→ Inner 可以处理
```

而：

```text
Profile
→ 只能找 Outer
```


# 31. fallback 自己也 suspend

例如：

```text
Posts
↓ suspend
Inner Suspense
↓
尝试 PostsSkeleton
↓
PostsSkeleton 也 suspend
```

那么：

```text
继续向外寻找 Suspense
↓
Outer Suspense
↓
PageSkeleton
```

所以 Suspense 是层层兜底的。


# 32. Suspense Boundary 本质是 reveal boundary

不要简单理解：

```text
Outer = 大 loading
Inner = 小 loading
```

更准确：

> **Suspense Boundary 定义哪些 UI 应该作为一个 reveal unit。**

例如：

```text
ProductInfo
+
Reviews
```

产品可能希望：

```text
ProductInfo 是核心
Reviews 可以晚一点
```

那么：

```tsx
<Suspense fallback={<PageSkeleton />}>
  <ProductInfo />

  <Suspense fallback={<ReviewsSkeleton />}>
    <Reviews />
  </Suspense>
</Suspense>
```

就是 UI 设计语义，而不是单纯技术优化。


# Transition + Suspense

# 33. 普通 update 导致已经展示的内容再次 suspend

当前：

```text
Page A
```

更新：

```tsx
setPage("B")
```

B suspend：

```text
Page A
↓
Skeleton
↓
Page B
```

这是合法行为。


# 34. Transition 可以保留 already revealed content

改成：

```tsx
startTransition(() => {
  setPage("B")
})
```

当前：

```text
Page A
```

后台：

```text
render Page B
↓
suspend
```

因为：

```text
A 是已经 reveal 的合法 UI
+
B 是 non-urgent
```

React可以：

```text
Page A
─────────────
后台准备 B
─────────────
Page B
```

而避免：

```text
A
↓
Skeleton
↓
B
```

核心：

> **不要因为未来 UI 暂时没准备好，就破坏当前仍然有用的 UI。**


# 35. Transition 不是永远不显示 fallback

错误理解：

```text
Transition + Suspense
=
永远不会 fallback
```

正确理解：

> Transition 尽量防止 **already revealed content** 被重新隐藏。


# 36. 新 Suspense Boundary 可以显示 fallback

例如从 Home Transition 到 Product 页面。

Product 页面第一次出现：

```tsx
<ProductInfo />

<Suspense fallback={<ReviewsSkeleton />}>
  <Reviews />
</Suspense>
```

如果：

```text
ProductInfo ready
Reviews suspend
```

这个 Reviews boundary 是新的。

因此可以：

```text
Home
↓
ProductInfo
ReviewsSkeleton
↓
ProductInfo
Reviews
```

Transition 不需要等 Reviews 全部完成。


# 37. 已 reveal Boundary 再次 suspend

当前：

```text
Profile A
Posts A
```

结构：

```tsx
<Suspense fallback={<PageSkeleton />}>
  <Profile userId={userId} />

  <Suspense fallback={<PostsSkeleton />}>
    <Posts userId={userId} />
  </Suspense>
</Suspense>
```

Outer：

```text
已经 revealed
```

Inner：

```text
也已经 revealed
```

Transition：

```tsx
setUserId("B")
```

结果：

```text
Profile B ready
Posts B suspend
```

此时 Inner boundary 已经显示 Posts A。

Transition 会尽量避免：

```text
Posts A
↓
PostsSkeleton
```

因此当前 committed UI 可以继续保留，直到新的 candidate 达到合适的 reveal 条件。


# 38. 不要理解成 React 随意拼两个版本

不要简单想象：

```text
Profile B
+
Posts A
```

一定会被 commit。

更安全的 mental model：

```text
当前 committed tree:
Profile A
Posts A
```

同时：

```text
candidate tree:
Profile B
Posts B
```

其中：

```text
Posts B suspend
```

所以新 candidate 没完成。

React继续保留旧 committed tree。


# 39. Boundary identity 很重要

判断 Transition + Suspense 时，可以问：

```text
这个 boundary 是：
已经 reveal 的？
还是新的？
```

### 已 reveal
```text
Transition 中再次 suspend
→ 尽量保留旧内容
```

### 新 Boundary
```text
第一次 suspend
→ 可以显示 fallback
```


# 40. `key` 可以重置 Suspense identity

例如：

```tsx
<Suspense
  key={userId}
  fallback={<PostsSkeleton />}
>
  <Posts userId={userId} />
</Suspense>
```

A：

```text
key=A
```

B：

```text
key=B
```

React会把它们理解成不同 identity。

于是：

```text
A Posts
↓
B PostsSkeleton
↓
B Posts
```

可能就是正确产品语义。

因为：

> A 用户内容和 B 用户内容本来就是不同页面实体。


# 41. 判断嵌套 Suspense 的三步法

以后直接：

```text
① 谁 suspend？
```

```text
② 最近的 Suspense boundary 是谁？
```

```text
③ 如果这是 Transition：

   boundary 已 reveal？
   → 尽量保留旧内容

   boundary 是新的？
   → 可以 fallback
```


# `isPending` 与 candidate UI

# 42. Transition update 已 enqueue，不代表已经 commit

例如：

```tsx
startTransition(() => {
  setPage("B")
})
```

执行完成之后：

```text
B update 已 enqueue
```

但是屏幕仍可能：

```text
page=A
```

因为：

```text
enqueue
≠
commit
```


# 43. 当前 UI 与 candidate UI 可以同时存在

概念上：

```text
Current committed:

page=A
Page A
```

同时 React 正在处理：

```text
Candidate:

page=B
Page B
```

每一个 render 自己的 snapshot 都是一致的。

不是：

```text
同一个 render 里
page 同时是 A 和 B
```

而是：

```text
两个不同版本的 render
```


# 44. `isPending` 表示 Transition lifecycle

用户点击：

```text
A → B
```

可以出现：

```text
page=A
isPending=true
Page A
```

后台：

```text
candidate page=B
↓
suspend
```

Promise ready：

```text
retry B
↓
success
↓
commit
```

最后：

```text
page=B
isPending=false
Page B
```

因此用户可能看到：

```text
Page A

↓ 点击

正在加载...
Page A

↓ ready

Page B
```


# 45. Concurrent React 可以保留“现在”和计算“未来”

这是非常重要的抽象：

```text
Current committed UI
=
现在
```

```text
Work being rendered
=
可能的未来
```

React可以：

```text
保持现在可用
+
后台计算未来
```

未来不满意：

```text
丢掉
```

未来准备好：

```text
commit
```


# 46. A → B → C

当前：

```text
A committed
```

开始：

```text
Transition → B
```

B：

```text
render
↓
suspend
```

此时用户又：

```text
想去 C
```

React不需要执着完成 B。

可以：

```text
B unfinished candidate
↓
被 supersede / 中断 / 放弃
↓
开始处理 C
```

最终：

```text
A → C
```

B 可能：

```text
render 过
```

但：

```text
从未 commit
```

这就是 speculative rendering 最典型的例子。


# 47. 丢弃 render ≠ 取消网络请求

例如：

```text
B render
↓
发起/依赖 HTTP request
↓
B candidate 被放弃
```

不意味着：

```text
HTTP 自动取消
```

React render 生命周期：

```text
一套系统
```

网络请求：

```text
另一套生命周期
```

真正取消通常需要：

```text
AbortController
数据层
框架
```

负责。


# 48. Concurrent UI 最终 Mental Model

现在可以把整个阶段压缩成：

```text
                       Update
                          │
             ┌────────────┴────────────┐
             │                         │
          urgent                   Transition
             │                         │
             ▼                         ▼
        render candidate          render candidate
             │                         │
      ┌──────┼──────┐          ┌──────┼──────┐
      │      │      │          │      │      │
   success interrupt suspend success interrupt suspend
      │      │      │          │      │      │
      ▼      ▼      ▼          ▼      ▼      ▼
   commit  retry/  Suspense   commit retry/  Suspense
           discard  boundary          discard boundary
                    │                         │
                 fallback             已 reveal 内容？
                                             │
                                  ┌──────────┴─────────┐
                                  │                    │
                                 yes                  no
                                  │                    │
                                  ▼                    ▼
                             保留旧 UI             fallback
                             后台 retry
```


# 49. 最终统一理解

以前容易把 React 理解成：

```text
state 改了
↓
render
↓
DOM 改了
```

Concurrent React 更准确应该理解成：

```text
update 产生
↓
进入 update system
↓
React 根据优先级尝试未来 UI
↓
candidate render
↓
可能成功 / suspend / interrupt / discard / retry
↓
得到某个完整 candidate
↓
commit
```

而整个过程中：

```text
当前 committed UI
```

可以继续存在。


# 50. 这一阶段最重要的几句话

建议重点记住：

> **`setState` 更接近 enqueue update，而不是直接修改 state。**

> **Render 是计算 candidate UI，Commit 才是真正改变用户看到的 UI。**

> **Concurrent Rendering 允许 React 开始一份未来 UI，然后中断甚至永远不 commit 它。**

> **Transition 不一定减少工作量，它主要改变工作的优先级和可调度性。**

> **Suspense 不是 loading 组件，而是 React 对“当前 render 暂时无法完成”的处理机制。**

> **Suspend 不是暂停 JavaScript，而是当前 render attempt 无法完成，之后重新 retry。**

> **Suspense Boundary 决定一部分 UI 的 fallback 和 reveal 边界。**

> **嵌套 Suspense 的核心规则是：谁 suspend，就找最近的祖先 Suspense。**

> **Transition + Suspense 的核心不是“永远不显示 fallback”，而是避免已经 reveal 的合法 UI 因新 candidate suspend 而突然消失。**

> **Concurrent React 的核心思想之一：不要因为未来 UI 还没准备好，就破坏现在仍然可用的 UI。**


# 下一阶段

到这里：

```text
External Store
↓
Concurrent Features
↓
Suspense
↓
Transition + Suspense
↓
Concurrent UI mental model
```

已经基本完成。

下一阶段正式进入 React 内部机制：

```text
Fiber
↓
current tree / workInProgress tree
↓
render phase 如何遍历 Fiber
↓
update queue
↓
lanes / priority
↓
Scheduler
↓
再反过来解释 Transition / Suspense 的内部实现
```

第一题会从：

> **为什么 React 需要 Fiber？普通递归组件树为什么不能满足 Concurrent Rendering？**

开始。

