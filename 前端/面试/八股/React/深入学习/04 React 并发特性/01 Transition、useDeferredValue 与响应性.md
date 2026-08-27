# 01 Transition、useDeferredValue 与响应性
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> 笔记说明：Transition、useTransition、useDeferredValue，以及响应性与吞吐量的区别。

---
## 一、当前学习进度
目前已经完成：
```text
urgent update / non-urgent update
        ↓
startTransition
        ↓
Transition 不是“异步执行代码”
        ↓
interruptible rendering
        ↓
cooperative scheduling
        ↓
responsiveness vs throughput
        ↓
stale UI
        ↓
useTransition / isPending
        ↓
useDeferredValue
        ↓
useDeferredValue vs debounce
```

暂未开始：

```text
Suspense
Transition + Suspense
并发 UI 整体 mental model
```

你之前已经掌握：

```text
Concurrent Rendering
= render work 可以暂停 / 重做 / 丢弃

render 执行过
≠
一定 commit
```

这次学到的 Transition，实际上就是把这个能力放进真实 UI 场景中。


# 二、urgent update 与 non-urgent update

假设有搜索页面：

```tsx
function ProductSearch() {
  const [keyword, setKeyword] = useState("")
  const [products, setProducts] = useState(allProducts)

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const nextKeyword = e.target.value

    setKeyword(nextKeyword)

    const nextProducts = expensiveFilter(
      allProducts,
      nextKeyword
    )

    setProducts(nextProducts)
  }

  return (
    <>
      <input
        value={keyword}
        onChange={handleChange}
      />

      <ProductList products={products} />
    </>
  )
}
```

这里同时存在两种 update。

### `setKeyword`
```text
用户按键
↓
输入框必须马上产生反馈
```

属于：

```text
urgent update（紧急更新）
```

因为输入框是用户**正在直接操控的 UI**。

如果输入：

```text
react
```

但按下 `t` 后输入框卡住半秒：

```text
reac
...
react
```

用户会直接感觉页面失去响应。


### `setProducts`
列表属于输入行为产生的**派生 UI**：

```text
用户输入
↓
根据输入计算产品结果
```

它通常可以稍晚完成：

```text
input = react

ProductList
暂时还是 rea 的结果
```

所以更适合：

```text
non-urgent update（非紧急更新）
```

---
## 判断 urgent / non-urgent 不能只看“业务重要性”
更好的判断方式是：

```text
urgent
→ 用户当前直接交互所需要的即时反馈

non-urgent
→ 交互派生出来，但允许稍后完成的 UI
```

例如：

```text
urgent:
- 输入
- focus
- 用户正在操作的控件反馈

non-urgent:
- 大型搜索结果列表
- 图表
- 很重的页面内容
- 页面切换后需要准备的大量 UI
```


# 三、stale UI 不等于 tearing

假设：

```text
input = "react"

ProductList
= "rea" 对应的结果
```

表面上它们来自不同时间点。

但这**不一定是 correctness（正确性）错误**。

因为它们可以拥有不同语义：

```text
input
= 用户当前最新输入

ProductList
= 最近一次已经完成的搜索结果
```

所以 UI 可以表达：

```text
“用户已经输入 react，
新的搜索结果还在准备，
当前暂时继续展示 rea 的结果。”
```

这叫：

```text
stale UI（旧 UI）
```

而不是 necessarily：

```text
incorrect UI（错误 UI）
```

---
## 与 tearing 的区别
之前 External Store 学过：

```text
Store = V1

Component A → V1

Store V1 → V2

Component B → V2
```

最终同一次候选 UI：

```text
A = V1
B = V2
```

这叫 tearing（撕裂）。

关键在于：

> A 和 B 都声称自己观察的是同一个 source of truth 的“当前值”。

例如：

```text
Header:
余额 ¥100

Checkout:
余额 ¥200
```

这是 consistency（一致性）问题。

但：

```text
input = react
results = rea
```

可以被设计成：

```text
input
= 最新用户意图

results
= 最近完成的结果
```

它们并没有同时声称：

```text
“我们代表同一个时间点的同一个值”
```

所以可以是合法 UI。

---
## 一个重要判断问题
以后看到两个区域数据不一致，不要只问：

```text
“它们是不是不同？”
```

而应该问：

> **它们是否声称自己代表同一个 source of truth 的同一个版本？**


# 四、为什么旧 render 可以直接丢弃

假设 React 正在 render：

```text
ProductList("rea")
```

用户突然继续输入：

```text
"reac"
```

这时候理想策略不是：

```text
rea render
↓
rea commit
↓
reac render
↓
reac commit
```

因为 `"rea"` 已经失效。

更合理：

```text
ProductList("rea")
████████░░░░
        ↓
用户输入 c
        ↓
urgent update 到达
        ↓
暂停 / 放弃 "rea"
        ↓
处理 input = "reac"
        ↓
准备 ProductList("reac")
```

这就是：

```text
render 执行过
≠
必须 commit
```

在真实 UI 中的意义。


# 五、`startTransition` 的真正作用

基本使用：

```tsx
setKeyword(nextKeyword)

startTransition(() => {
  setSearchKeyword(nextKeyword)
})
```

可以粗略理解：

```text
setKeyword
→ urgent

setSearchKeyword
→ Transition update
→ non-urgent
```

但非常重要：

> `startTransition` 不是把 callback 变成异步函数。


# 六、`startTransition` 不会延后调用 Action

错误 mental model：

```text
startTransition(action)
↓
Action 被扔到后台
↓
handleChange 立即返回
↓
之后再调用 Action
```

不是这样。`startTransition` 会立即调用传入的 Action；Action 可以是同步函数，也可以是 `async` 函数。它不会把任意 JavaScript 调度到后台。〔CR-001〕

例如：

```tsx
startTransition(() => {
  const products =
    expensiveFilter(allProducts, keyword)

  setProducts(products)
})
```

如果：

```ts
expensiveFilter(...)
```

同步计算需要：

```text
500ms
```

那么仍然会：

```text
startTransition Action
↓
立即执行
↓
expensiveFilter()
████████████ 500ms
↓
setProducts(...)
```

这 500ms：

```text
仍然占用 JS 主线程
```

所以输入框还是会卡。

如果 Action 包含 `await`，React 可以把异步 Action 纳入 Transition 的 pending 状态；但在当前 React 中，`await` 之后执行的 state setter 需要再包一层 `startTransition`，才能继续标记为 Transition update。〔CR-002〕

---
## `startTransition` 改变的是 update 的调度语义
更适合这样：

```tsx
const [keyword, setKeyword] = useState("")
const [searchKeyword, setSearchKeyword] =
  useState("")

function handleChange(e) {
  const next = e.target.value

  setKeyword(next)

  startTransition(() => {
    setSearchKeyword(next)
  })
}
```

真正耗时的是：

```tsx
<ProductList keyword={searchKeyword} />
```

例如它下面有：

```text
5000 个 Product
```

那么 Transition 能影响的是：

```text
setSearchKeyword
↓
React 开始处理对应 render work
↓
这些 work 是 non-urgent
↓
urgent update 可以插队
```

所以：

```text
startTransition
不是调度任意 JavaScript

而是在告诉 React：

“这个 state update 产生的 UI 工作可以不紧急。”
```


# 七、React 无法任意中断同步 JavaScript

我们比较三种慢任务。

---
## A：Transition callback 里直接计算 500ms
```tsx
startTransition(() => {
  const result = expensiveCalculation()

  setResult(result)
})
```

流程：

```text
expensiveCalculation()
████████████ 500ms
↓
setResult
↓
React 才真正收到需要 render 的 update
```

前面的 500ms Transition 帮不了。

---
## B：Transition 触发 5000 个组件 render
```tsx
startTransition(() => {
  setKeyword(next)
})

function ProductList() {
  return products.map(product => (
    <Product
      key={product.id}
      product={product}
    />
  ))
}
```

这里大量工作属于：

```text
React render work
```

React有机会：

```text
Product 1
Product 2
Product 3
...
↓
检查有没有更高优先级任务
↓
yield
```

所以这种情况最能发挥 Concurrent Rendering 的价值。

---
## C：组件 render 内部单次执行 500ms JS
```tsx
function ProductList() {
  const result = expensiveCalculation()
  return <div>{result}</div>
}
```

虽然发生在：

```text
React render phase
```

但一旦：

```text
React
↓
ProductList()
↓
expensiveCalculation()
```

React 就必须等这个同步函数返回。

不能：

```text
expensiveCalculation
执行到 200ms

↓ React 强行暂停

处理 input

↓ 再从 200ms 继续
```


# 八、React 的可中断性粒度

所以不能简单记：

```text
“发生在 React render 中
就一定能被中断”
```

更准确：

> React 可以在自己掌控的 work unit（工作单元）之间重新进行调度，但不能任意暂停正在运行的同步 JavaScript 调用栈。


# 九、cooperative scheduling（协作式调度）

假设：

```tsx
function ProductList({ products }) {
  return products.map(product => (
    <Product
      key={product.id}
      product={product}
    />
  ))
}
```

每个 Product：

```text
render ≈ 0.2ms
```

虽然：

```text
5000 个 Product
总工作量可能很大
```

但是 React 在工作单元之间可能重新获得控制权：

```text
Product 1
Product 2
Product 3
...
↓
React 判断是否应该 yield
↓
处理更紧急工作
```

这更接近：

```text
cooperative scheduling
（协作式调度）
```

而不是：

```text
preemptive scheduling
（抢占式调度）
```

React 不能在：

```ts
while (...) {
  heavyCalculation()
}
```

执行到任意一条机器指令时把它抢占。


# 十、总耗时和响应性不是一回事

这是这一阶段非常重要的性能认知。

例如：

```text
任务 A：

1000ms
但能够分成很多 React work units
```

和：

```text
任务 B：

300ms
但就是一次连续同步 JS
```

B 反而可能让用户感觉更卡。

因为：

```text
300ms 内
React 和 Browser 都拿不回主线程
```

而 A 虽然总工作量更大：

```text
work
↓
yield
↓
urgent input
↓
work
↓
yield
```

输入可能依然很流畅。


# 十一、Transition 优化的主要不是 throughput

可以区分两个概念。

### Throughput（吞吐量）
```text
完成所有工作的总效率
```

例如：

```text
5000 个 Product
总共需要多少 CPU 工作
```

### Responsiveness（响应性）
```text
用户操作以后
UI 多快能产生反馈
```

`startTransition` 主要改善的是：

```text
responsiveness
+
scheduling
```

而不是：

```text
减少总计算量
```

所以：

```text
startTransition
≠ 让 800ms 的工作变成 300ms

startTransition
≈ 让 800ms 工作不要连续霸占用户交互
```

用户就会感觉：

```text
“页面快了”
```

虽然：

```text
总工作量可能完全没减少
```


# 十二、React state 不是被 setter 立即 mutation

这里修正了一个重要 state mental model。

假设当前 render：

```tsx
const [keyword, setKeyword] = useState("rea")

function handleClick() {
  setKeyword("react")

  console.log(keyword)
}
```

打印的仍然是：

```text
rea
```

而不是：

```text
react
```

因为当前 render 已经拿到了一份：

```text
state snapshot
```

调用：

```ts
setKeyword("react")
```

不是：

```text
keyword 变量立即
"rea" → "react"
```

---
## 更准确的模型
```text
Render R0

keyword = "rea"

        ↓

setKeyword("react")

        ↓

enqueue update
将 update 放入 React 更新系统

        ↓

React 调度后续 render

        ↓

Render R1

根据需要处理的 updates
计算新的 state snapshot

keyword = "react"
```

所以不是：

```text
setState
↓
直接修改当前 state 对象
↓
React 再追着 state 更新 DOM
```

也不是：

```text
setState
↓
维护一个临时 state
↓
commit 后再复制到真实 state
```

更接近：

```text
当前 render snapshot
+
update queue
+
下一次 render 重新计算 snapshot
```


# 十三、为什么 `keyword` 和 `searchKeyword` 可以暂时不同

代码：

```tsx
const [keyword, setKeyword] = useState("rea")

const [searchKeyword, setSearchKeyword] =
  useState("rea")

function handleChange(e) {
  const next = e.target.value

  setKeyword(next)

  startTransition(() => {
    setSearchKeyword(next)
  })
}
```

用户输入：

```text
reac
```

React 可以先完成 urgent update：

```text
keyword       = "reac"
searchKeyword = "rea"
```

commit：

```text
input = reac

ProductList
= rea 的结果
```

之后才尝试：

```text
keyword       = "reac"
searchKeyword = "reac"
```


# 十四、两个 state 不是简单的数据重复

最终：

```text
keyword
searchKeyword
```

通常会相等。

但它们承担不同的**时间语义**。

```text
keyword
= latest value
= 用户当前最新输入
```

```text
searchKeyword
= lagging value
= ProductList 当前已经跟进到哪个版本
```

所以真正需要的不是：

```text
“两份 keyword”
```

而是：

```text
同一个逻辑值
拥有两个时间版本
```

即：

```text
latest
vs
stale / deferred
```


# 十五、`useTransition` 为什么需要 `isPending`

如果只使用：

```ts
startTransition(...)
```

组件并不知道：

```text
Transition 对应的 React UI 工作
到底完成没有
```

因为：

```text
startTransition callback 执行完
≠
Transition render 完成
```

因此：

```tsx
const [isPending, startTransition] =
  useTransition()
```

多出了：

```ts
isPending
```

---
## Action 调用与 Transition lifecycle 不一样
### Action 调用
```text
startTransition(async () => {
  setSomething(...)
  await saveSomething()

  startTransition(() => {
    setResult(...)
  })
})
```

Action 会被立即调用；同步部分会立刻执行，异步 Action 则可以跨越 `await`。`isPending` 用于表示这次 Transition 是否仍在进行，而不是表示“传入函数是否已被调用”。〔CR-003〕

对应的 Transition 可能经历：

```text
Transition 开始
↓
Action 执行或等待
↓
render
↓
被 urgent update 打断
↓
重新 render
↓
再次被打断
↓
最终完成
↓
commit
↓
Transition 结束
```

所以：

```text
Action 调用
≠
Transition lifecycle
```

`isPending` 描述的是后者，并会在相关 Action 完成且最终 UI 呈现后结束。


# 十六、为什么不能简单用两个业务 state 推导 Transition 状态

例如：

```ts
const isPending =
  keyword !== searchKeyword
```

这个可以表达：

```text
“ProductList 当前使用的 keyword
是否落后于最新输入”
```

但它的业务语义是：

```text
两个值是否不同
```

不是：

```text
React 是否存在 pending Transition
```

两者不是同一个概念。

所以：

```text
keyword !== searchKeyword
```

可以用来判断：

```text
结果是否 stale
```

但不能泛化成：

```text
Transition lifecycle 状态
```


# 十七、`isPending` 的典型时间线

初始：

```text
keyword       = "rea"
searchKeyword = "rea"
isPending     = false
```

输入 `c`：

```text
keyword       = "reac"
searchKeyword = "rea"
isPending     = true
```

页面：

```text
reac

Updating...

[rea results]
```

然后又输入 `t`：

一种可能：

```text
keyword       = "react"
searchKeyword = "rea"
isPending     = true
```

正在准备的：

```text
ProductList("reac")
```

可能已经失效：

```text
render
██████░░░
    ✕
```

重新准备：

```text
ProductList("react")
```

最终：

```text
keyword       = "react"
searchKeyword = "react"
isPending     = false
```

---
## 注意：`searchKeyword` 不一定一直停留在最旧值
比如 `"reac"` 的 Transition 很快完成：

```text
keyword       = "reac"
searchKeyword = "reac"
isPending     = false
```

之后用户才输入：

```text
react
```

那么：

```text
keyword       = "react"
searchKeyword = "reac"
isPending     = true
```

所以应该理解：

> 当前 committed UI 保持“最近一次已经成功完成的版本”，而不是一定保持最开始的旧版本。


# 十八、pending 不代表 state 正处于“半修改状态”

例如：

```text
keyword       = "react"
searchKeyword = "rea"
isPending     = true
```

屏幕上当前已有的：

```text
searchKeyword = "rea"
```

仍然是一份完整的 committed UI。

而 React 可能正在准备：

```text
searchKeyword = "react"
```

对应的新 UI。

所以粗略可以想成：

```text
屏幕：
最近一次完成的 UI

React：
可能正在准备下一份 UI
```

暂时不深入 current tree / work-in-progress tree，因为这是之后 React 内部机制阶段。你的原始路线也把 Fiber、current tree、WIP tree 放在 Concurrent Features 之后。


# 十九、`useDeferredValue`

之前我们为了得到：

```text
latest value
+
lagging value
```

手工维护：

```tsx
const [keyword, setKeyword] = useState("")
const [searchKeyword, setSearchKeyword] =
  useState("")

setKeyword(next)

startTransition(() => {
  setSearchKeyword(next)
})
```

但 `searchKeyword` 本质上只是：

```text
keyword 的一个
允许暂时滞后的版本
```

所以 React 提供：

```tsx
const [keyword, setKeyword] = useState("")

const deferredKeyword =
  useDeferredValue(keyword)
```

使用：

```tsx
return (
  <>
    <input
      value={keyword}
      onChange={e =>
        setKeyword(e.target.value)
      }
    />

    <ProductList
      keyword={deferredKeyword}
    />
  </>
)
```


# 二十、`useDeferredValue` 的核心语义

可以粗略理解：

```text
keyword
= latest value

deferredKeyword
= deferred version
= 可以暂时落后的版本
```

图：

```text
             keyword
                │
        ┌───────┴────────┐
        ↓                ↓
      input       deferredKeyword
    立即使用              │
                          ↓
                     ProductList
                     可以晚点跟上
```


# 二十一、`startTransition` 与 `useDeferredValue`

这是目前最重要的区别之一。

---
## `startTransition`
```text
我控制 update
```

例如：

```ts
setSearchKeyword(...)
```

所以：

```tsx
startTransition(() => {
  setSearchKeyword(next)
})
```

意思接近：

> “我知道这次 state update 可以是 non-urgent。”

---
## `useDeferredValue`
有时候 value 来自 props：

```tsx
function SearchPage({
  keyword
}: {
  keyword: string
}) {
  // 没有 setKeyword
}
```

你根本无法：

```tsx
startTransition(() => {
  setKeyword(...)
})
```

因为 setter 不属于你。

这时：

```tsx
const deferredKeyword =
  useDeferredValue(keyword)
```

更自然。

---
## 一句话区分
```text
startTransition

我控制 update
↓
给 update 较低的调度优先级
```

```text
useDeferredValue

我已经拿到了 value
↓
让 value 的某些消费者
允许暂时使用旧版本
```


# 二十二、`useDeferredValue` 同样建立在 interruptible rendering 上

假设：

```text
keyword         = "rea"
deferredKeyword = "rea"
```

输入：

```text
react
```

可以先 commit：

```text
keyword         = "react"
deferredKeyword = "rea"
```

React 后台尝试：

```text
deferredKeyword = "react"
```

还没完成：

```text
ProductList("react")
████████░░
```

用户又输入：

```text
reactj
```

那么之前的：

```text
ProductList("react")
```

可以失效：

```text
████████░░
      ✕
```

然后重新准备：

```text
ProductList("reactj")
```

所以：

```text
useDeferredValue
```

不是：

```text
“固定晚 500ms 修改 value”
```

而是：

```text
先允许旧 value 继续存在
↓
后台尝试 render 新 value
↓
urgent update 来了可以打断
↓
之后基于最新值重新尝试
```


# 二十三、`useDeferredValue` 和 debounce 完全不是一回事

这是当前阶段最后一个核心结论。

---
## debounce
例如：

```tsx
const [keyword, setKeyword] = useState("")
const [searchKeyword, setSearchKeyword] =
  useState("")

useEffect(() => {
  const timer = setTimeout(() => {
    setSearchKeyword(keyword)
  }, 500)

  return () => {
    clearTimeout(timer)
  }
}, [keyword])
```

快速输入：

```text
r
100ms
re
100ms
rea
100ms
reac
100ms
react
```

前面的 timer：

```text
取消
取消
取消
取消
```

用户停止：

```text
等待 500ms
↓
searchKeyword = "react"
```

它属于：

```text
time-based delay
（基于时间的延迟）
```

---
## `useDeferredValue`
```tsx
const deferredKeyword =
  useDeferredValue(keyword)
```

没有：

```text
500ms
300ms
1s
```

这样的固定延迟。

React 可以：

```text
当前 urgent render 完成
↓
马上尝试 deferred render
```

如果机器很快：

```text
很快就跟上
```

如果 urgent updates 不断出现：

```text
r
re
rea
reac
react
```

可能：

```text
r     background render ✕
re    background render ✕
rea   background render ✕
reac  background render ✕
react background render ✓
```

原因不是：

```text
“React 在等 500ms timer”
```

而是：

```text
低优先级工作不断被
更高优先级工作打断
```


# 二十四、debounce 与 Concurrent Features 解决不同层面的问题

你的总结非常准确：

> **一个降低频率，一个降低优先级。**

可以进一步整理成：

```text
debounce
→ frequency（频率）
```

```text
Transition / useDeferredValue
→ priority + scheduling
（优先级 + 调度）
```

---
## 典型 debounce 场景：控制请求频率
产品要求：

```text
用户停止输入 500ms
才允许发送搜索请求
```

用户输入：

```text
r
re
rea
reac
react
```

希望只请求：

```text
GET /search?q=react
```

这里应该使用：

```text
debounce
```

因为需求本身就是：

```text
减少请求次数
```

---
## 典型 Concurrent 场景：解决重 render
如果：

```text
网络请求不是问题

但是 SearchResults
render 很重
```

目标是：

```text
输入框保持流畅
```

那么 Transition / `useDeferredValue` 更适合解决：

```text
UI scheduling
```


# 二十五、debounce 也不只用于接口请求

例如：

```ts
debounce(sendRequest, 500)

debounce(saveDraft, 500)

debounce(expensiveCalculation, 500)
```

所以 debounce 的本质不是：

```text
“接口优化工具”
```

而是：

> 在一段连续事件中，把动作推迟到某个时间窗口之后执行，从而减少执行频率。


# 二十六、三者最终对照

|能力|主要控制什么|核心|
|---|---|---|
|`startTransition`|React update|降低 update 的调度优先级|
|`useDeferredValue`|value 的消费节奏|允许消费者暂时使用旧 value|
|debounce|某个动作何时真正执行|基于时间降低执行频率|

最简记忆：

```text
startTransition
→ 我控制 update
```

```text
useDeferredValue
→ 我控制 value 的消费
```

```text
debounce
→ 我控制事情什么时候发生
```


# 二十七、这一阶段形成的整体 mental model

目前可以把 React Concurrent Features 理解成：

```text
并发特性不是：

“让 JavaScript 多线程运行”

也不是：

“让代码本身计算更快”
```

而是：

```text
不同 UI update
可能具有不同紧急程度

        ↓

React 可以让 non-urgent render
具有更低调度优先级

        ↓

当 urgent work 到达

        ↓

低优先级 render
可以暂停 / 放弃 / 重做

        ↓

先保证用户直接交互的响应性

        ↓

之后再完成派生 UI
```


# 二十八、目前几个最重要的结论

可以直接作为速记版：

```text
1. urgent / non-urgent 描述的是 UI 更新的紧迫程度，
   不是简单的“业务重要性”。

2. 用户正在直接操作的 UI 通常应该 urgent。

3. 派生出来的大型 UI 通常可以 non-urgent。

4. stale UI 不一定意味着 correctness 被破坏。

5. tearing 是同一个 source of truth
   在同一次候选 UI 中出现不一致观察。

6. startTransition 会立即调用 Action，但 Action 本身可以是 async。

7. startTransition Action 中的同步 JS
   仍然会直接阻塞主线程。

8. Transition 主要影响 state update
   后续产生的 React render work。

9. React 不能暂停任意正在执行的同步 JS。

10. React 的调度属于 cooperative scheduling。

11. React 可以在自己掌控的 work unit 之间 yield。

12. 总计算量和 responsiveness 是不同概念。

13. Transition 通常提高 responsiveness，
    不一定提高 throughput。

14. setState 不会修改当前 render 的 state snapshot。

15. setter 更接近 enqueue update。

16. keyword / searchKeyword 可以代表
    同一逻辑数据的不同时间版本。

17. isPending 描述 Transition lifecycle，
    不是 Action 是否已被调用。

18. Action 调用
    ≠ Transition lifecycle。

19. useDeferredValue 允许一个 value 的消费者
    暂时落后于最新值。

20. startTransition 更适合“我控制 update”。

21. useDeferredValue 更适合
    “我只有 value，没有 setter”。

22. useDeferredValue 同样建立在
    interruptible rendering 上。

23. useDeferredValue 没有固定 500ms 延迟。

24. debounce 是 time-based。

25. debounce 主要降低事情执行的频率。

26. Transition / useDeferredValue
    主要改变 React scheduling。

27. debounce 和 Concurrent Features
    可以组合使用，它们解决不同问题。
```

以上速记同步区分了“立即调用 Action”和“Action 可以异步”这两个概念。〔CR-004〕


# 更新后的学习进度 / 续接记忆版

这段你以后可以直接粘贴给我续接：

```text
【React 深入学习当前进度 - 2026-08-25】

当前已正式进入 React Concurrent Features（React 并发特性）阶段。

External Store 阶段已经暂时结束，此前已掌握：
- useSyncExternalStore
- snapshot consistency
- tearing
- immutable snapshot
- structural sharing
- selector
- equalityFn
- selector cache
- useSyncExternalStoreWithSelector 基础模型
- Zustand useStore / useShallow
- concurrent rendering 基础
- speculative render / commit 区别

本次已经完成：

1. urgent update / non-urgent update
- 用户直接交互 UI 通常属于 urgent。
- 大型派生 UI 可以作为 non-urgent。
- 判断依据是响应性和 UI 语义，不是简单业务重要性。

2. stale UI
- stale UI 不一定是 incorrect UI。
- input = 最新 keyword、ProductList = 最近完成结果，可以是合法设计。
- tearing 则涉及同一个 source of truth 在同一次候选 UI 中出现不同版本。

3. startTransition
- startTransition 会立即调用 Action，Action 可以是同步函数或 async 函数。
- Action 内长耗时同步 JS 仍然阻塞主线程。
- 当前 React 中，`await` 后的 setter 需要再包一层 startTransition 才会继续作为 Transition update。
- startTransition 的核心是把其中产生的 React update 标记为 Transition / non-urgent update。

4. interruptible rendering
- React 能中断自己掌控的 render work。
- React 不能任意暂停正在执行的同步 JavaScript。
- 5000 个组件的 render 比一个连续 500ms 同步函数更有调度空间。
- 可中断粒度与 React work units 有关。

5. cooperative scheduling
- React 的调度是 cooperative scheduling，而不是任意 JS 指令级的 preemptive scheduling。
- React 在工作单元之间获得控制权后才能 yield。

6. responsiveness vs throughput
- Transition 不一定减少总计算量。
- 主要改善 responsiveness / scheduling。
- 总耗时较长但可切分的任务，交互体验可能比短但不可切分的同步 JS 更好。

7. React state snapshot
- setState 不会修改当前 render 已拿到的 state。
- setter 更接近 enqueue update。
- 后续 render 根据需要处理的 updates 计算新的 state snapshot。

8. useTransition
- const [isPending, startTransition] = useTransition()
- Action 调用 != Transition lifecycle。
- Action 已被调用不代表相关异步工作和 render 已完成。
- isPending 用于表示 Transition 是否仍处于 pending 状态。
- keyword !== searchKeyword 只能表达业务值是否落后，不能完整表示 Transition 生命周期。

9. latest value / stale value
- keyword 表示用户当前最新输入。
- searchKeyword 可以表示 ProductList 最近跟进到的版本。
- 两者最终相等，但在 Transition 期间允许暂时不相等。
- 这不是简单重复 state，而是同一个逻辑值的两个时间版本。

10. useDeferredValue
- const deferredKeyword = useDeferredValue(keyword)
- keyword = latest value。
- deferredKeyword = 可以暂时滞后的版本。
- startTransition 更偏向“我控制 update”。
- useDeferredValue 更偏向“我已经拿到 value，希望某些消费者晚一点跟上”。
- props 没有 setter 时 useDeferredValue 尤其自然。
- useDeferredValue 的后台 render 同样可以被 urgent update 打断和丢弃。

11. useDeferredValue vs debounce
- useDeferredValue 没有固定延迟时间。
- 它依赖 React priority / scheduling / interruptible rendering。
- debounce 是 time-based delay。
- debounce 主要降低动作执行频率，例如减少 API 请求。
- Transition / useDeferredValue 主要降低 React UI 工作的紧急程度。
- 最简区别：
  debounce = 降低频率
  Transition / deferred value = 降低优先级 / 改变调度。

当前阶段已经完成：

Transition / useTransition
→ useDeferredValue
→ Suspense
→ Transition + Suspense
→ 并发 UI 整体 mental model

之后进入 React 内部机制：
Fiber、current tree / WIP tree、update queue、lanes、scheduler、reconciliation、render / commit phase 等。

本笔记负责并发特性的行为模型；源码级调度和 commit 细节转入 `05 React 内部机制`。〔CR-006〕

```

---
## 内容审核变更记录
### CR-001｜事实纠错
- 日期：8/25/2026
- 位置：`startTransition 不会延后调用 Action` 开头
- 原内容：`startTransition` callback 是同步执行的。
- 调整后：`startTransition` 会立即调用 Action，但 Action 可以是同步函数或 `async` 函数。
- 原因：原描述把“立即调用”和“只能同步”混为一谈，无法覆盖 React 当前支持的异步 Action。
- 依据：[React：useTransition](https://react.dev/reference/react/useTransition)；[React：startTransition](https://react.dev/reference/react/startTransition)
### CR-002｜补充说明
- 日期：8/25/2026
- 位置：`startTransition 不会延后调用 Action` 末尾
- 原内容：未说明异步 Action 中 `await` 之后的 state update 如何保持 Transition 标记。
- 调整后：补充当前 React 中 `await` 后的 setter 需要再包一层 `startTransition`。
- 原因：这是异步 Action 的当前使用限制，遗漏会导致调用者误以为所有 `await` 后更新都会自动继承 Transition 标记。
- 依据：[React：useTransition](https://react.dev/reference/react/useTransition)；[React：startTransition](https://react.dev/reference/react/startTransition)
### CR-003｜事实纠错
- 日期：8/25/2026
- 位置：`Action 调用与 Transition lifecycle 不一样`
- 原内容：callback 同步执行且可能几乎立刻结束，`isPending` 仅描述之后的 render lifecycle。
- 调整后：Action 立即开始但可以跨越 `await`；`isPending` 覆盖相关 Action 与 UI Transition 仍在进行的阶段。
- 原因：原模型不能解释 async Action 和其 pending 状态。
- 依据：[React：useTransition](https://react.dev/reference/react/useTransition)
### CR-004｜事实纠错
- 日期：8/25/2026
- 位置：`目前几个最重要的结论` 第 6、7、17、18 条
- 原内容：`startTransition` callback 不会异步，callback lifecycle 与 Transition lifecycle 不同。
- 调整后：Action 会立即调用但本身可以 async，并区分 Action 调用与完整 Transition lifecycle。
- 原因：让速记总结与前文修正后的 React Action 模型一致。
- 依据：[React：useTransition](https://react.dev/reference/react/useTransition)
### CR-005｜事实纠错
- 日期：8/25/2026
- 位置：`更新后的学习进度 / 续接记忆版` 中 `startTransition` 与 `useTransition`
- 原内容：callback 是立即同步执行的，不会变成异步任务。
- 调整后：Action 立即调用但允许 async，并补充 `await` 后 setter 的嵌套 `startTransition` 要求。
- 原因：续接摘要会被后续学习直接复用，必须与当前 React 行为保持一致。
- 依据：[React：useTransition](https://react.dev/reference/react/useTransition)；[React：startTransition](https://react.dev/reference/react/startTransition)

### CR-006｜进度同步
- 日期：8/27/2026
- 位置：`更新后的学习进度 / 续接记忆版` 末尾
- 原内容：仍写着“Suspense 之前”，并把 Suspense 标记为下一步。
- 调整后：标记 Transition、`useDeferredValue`、Suspense、Transition + Suspense 和并发 UI mental model 已完成，并把后续源码级内容交给内部机制模块。
- 原因：目录中已经存在并完成 `02 Suspense、Transition 与 Suspense、并发 UI 整体.md`。
- 依据：当前目录中的 Suspense 笔记及其末尾完成度说明

