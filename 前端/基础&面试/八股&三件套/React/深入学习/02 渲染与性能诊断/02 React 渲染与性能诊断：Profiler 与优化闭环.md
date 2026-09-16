# 02 React 渲染与性能诊断：Profiler 与优化闭环
> Last Format Time：9/16/2026 19:24:52

> Last Format Time：2026-08-28
> Status：进行中
> 笔记说明：用 Profiler、Ranked、Flamegraph 和可复现实验定位昂贵且不必要的渲染。


![[Pasted image 20260827162540.png]]


![[Pasted image 20260827162612.png]]

---
## 性能诊断的核心目标
React 性能优化不是：

```text
尽量减少所有 render
```

而是：

```text
找到真正昂贵的 render
↓
分析为什么它会发生
↓
缩小不必要的 render 范围
↓
再次用 Profiler 验证
```

最重要的原则：

> **re-render 本身不是问题，昂贵且没有必要的 re-render 才是问题。**

例如：

```text
组件 render 100 次
每次 0.01ms
```

可能完全不是问题。

而：

```text
某组件 render 1 次
耗时 80ms
```

反而更值得优化。



Profiler 用来回答两个核心问题：

```text
谁 render 了？
+
谁最贵？
```

一次 Profiler 记录中的一个 commit，可以理解为：

```text
Update
↓
render phase
↓
commit
↓
Profiler 记录此次更新
```

右侧常见：

```text
Render
Layout effects
Passive effects
```

例如：

```text
Render: 11.9ms
Layout effects: <0.1ms
Passive effects: 0.1ms
```

说明主要成本来自 render，而不是 Effect。

---
## Ranked 与 Flamegraph 的区别
---
## Ranked
回答：

> 这一次 commit 中，哪些组件最贵？

例如：

```text
PublicHeader              3.4ms
PublicHeaderDropdown      2.1ms
PublicHeaderDropdown      1.6ms
PublicCapabilityExplorer  1.5ms
```

适合快速定位 expensive component（昂贵组件）。

诊断顺序：

```text
慢 commit
↓
Ranked
↓
找到最贵组件
```

---
## Flamegraph
回答：

> 这些组件位于哪条组件树 / Fiber 路径中，以及 render 如何传播？

可以看到：

```text
Parent
├─ Child A
├─ Child B
└─ Child C
```

并区分：

```text
当前真的 render 的组件
vs
只是位于 Fiber 路径上的组件
```

所以：

```text
Fiber traversal 经过
≠
组件函数一定重新执行
```

这点和 Fiber bailout 是一致的。

---
## Flamegraph 中的颜色
大致可以理解为：

```text
灰色
→ 当前 commit 没有 render

绿色
→ render 了，但成本较低

黄 / 橙
→ render 了，而且相对更贵
```

注意：

> 颜色表示的是当前 commit 中的相对成本，不是绝对性能报警。

---
## Profiler 的正确使用流程
以后性能诊断可以固定使用：

```text
发现交互卡顿
↓
Profiler 录制
↓
找到慢 commit
↓
Ranked 找 expensive component
↓
Flamegraph 看传播路径
↓
确认为什么 render
↓
针对性优化
↓
重新 Profile
```

而不是：

```text
看到组件 render
↓
立即 memo
```

---
## 组件为什么会 render
常见来源可以归为：

```text
1. 自己的 state 变化
2. Parent render
3. props 变化
4. Context 更新
5. external store / subscription 更新
```

不同原因应该使用不同优化方式。

---
## Parent render 与 Child render
React 默认情况下：

```text
Parent render
↓
普通 Child 通常继续 render
```

即使 Child 的 props 没变化。

例如：

```tsx
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Child />
    </>
  );
}
```

`count` 改变：

```text
Parent render
↓
Child render
```

并不是因为 Child props 改了。

而是：

> Parent render propagation（父组件渲染传播）。

---
## `React.memo`
`memo` 主要用于：

> 阻断 Parent → Child 的 render propagation。

例如：

```tsx
const Child = memo(function Child(props) {
  ...
});
```

Parent render 后：

```text
进入 Memo Fiber
↓
比较 prevProps / nextProps
↓
props 没变化
↓
bailout
↓
Child function 不执行
```

更准确的源码级理解：

```text
memo
≠
Fiber 不被访问

memo
=
React 遍历到该 Fiber
↓
判断可以 bailout
↓
跳过组件 render / subtree work
```

---
## `memo` 不能解决什么
---
## 自身 state 更新
```text
Child own state changed
↓
Child render
```

`memo` 挡不住。

---
## Context 更新
```text
Context value changed
↓
Consumer 收到更新
↓
render
```

即使组件被：

```tsx
memo(...)
```

包裹也一样。

因此：

```text
memo
主要解决 Parent → Child props propagation
```

而不是所有更新来源。

---
## `memo` 的适用条件
比较适合：

```text
Parent 高频 render
+
Child render 成本较高
+
Child props 大部分时候不变
```

例如：

```text
输入框频繁更新
↓
昂贵列表 props 没变化
```

适合 memo。

不太值得：

```text
组件本身非常便宜
+
props 经常变化
```

例如：

```tsx
function Label({ text }) {
  return <span>{text}</span>;
}
```

这种组件可能 render 比做 props comparison 更便宜。

---
## `memo` 不是免费的
每次 Parent render，memo 仍需要：

```text
prevProps
vs
nextProps
↓
shallow comparison
```

所以它有：

```text
comparison cost
+
代码复杂度
```

不能把：

```tsx
memo(...)
```

当作默认模板。

---
## Props identity 会破坏 memo
---
## 函数
例如：

```tsx
<Child onClick={() => doSomething()} />
```

每次 Parent render：

```text
new function
```

所以：

```text
prev.onClick !== next.onClick
```

即使 Child 被 memo：

```text
memo bailout 失败
```

---
## 对象 / 数组
例如：

```tsx
<Child
  options={{ size: "large" }}
/>
```

每次：

```text
new object
```

所以：

```text
prev.options !== next.options
```

同样破坏 memo。

---
## `useCallback`
`useCallback` 的核心不是：

> 让函数执行得更快。

而是：

> 稳定 function identity（函数引用）。

例如：

```tsx
const handleClick = useCallback(() => {
  ...
}, []);
```

典型用途：

```text
Parent render
↓
function prop 需要保持引用稳定
↓
memo Child 才能 bailout
```

所以：

```text
useCallback
通常是为了帮助 memo boundary
```

而不是为了避免创建普通函数。

---
## Functional updater 与 useCallback
例如：

```tsx
const handleToggle = useCallback(() => {
  setTodos(
    todos.map(...)
  );
}, [todos]);
```

每次 `todos` 变化：

```text
dependency changed
↓
callback identity changed
↓
Child function prop changed
```

如果能改成：

```tsx
const handleToggle = useCallback(() => {
  setTodos(prevTodos =>
    prevTodos.map(...)
  );
}, []);
```

就不需要从闭包读取 `todos`。

于是：

```text
callback identity 可以长期稳定
```

这和之前学过的 functional updater / stale closure 能直接连接起来。

---
## `useMemo`
`useMemo` 有两个主要用途。

---
## 避免昂贵计算
```tsx
const result = useMemo(() => {
  return expensiveCalculation(data);
}, [data]);
```

避免无关 render 重复执行昂贵计算。

---
## 稳定引用
例如：

```tsx
const visibleItems = useMemo(
  () => items.filter(...),
  [items]
);
```

如果没有 useMemo：

```text
Parent render
↓
filter()
↓
new Array
↓
memo Child props changed
```

使用之后：

```text
items 没变
↓
visibleItems identity 没变
↓
memo Child 可以 bailout
```

---
## 三者的关系
可以记成：

```text
memo
→ 控制组件是否重新执行

useCallback
→ 稳定函数引用

useMemo
→ 稳定计算结果 / 对象引用
```

典型组合：

```text
Parent render
↓
useCallback 稳定 function prop
↓
useMemo 稳定 object / array prop
↓
memo 比较 props
↓
props 没变
↓
bailout
```

但不要理解成：

```text
性能优化
=
memo + useCallback + useMemo 三件套
```

正确顺序仍然是：

```text
Profiler
↓
发现 memo boundary 有价值
↓
发现 props identity 破坏 memo
↓
再使用 useCallback / useMemo
```

---
## State colocation：状态下沉
比 memo 更根本的一种优化是：

> 把 state 放到真正使用它的组件附近。

例如：

```tsx
function Page() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Header open={open} />
      <HugeContent />
      <Footer />
    </>
  );
}
```

如果 `open` 只有 Header 需要：

```text
Page state update
↓
Page render
↓
Header / HugeContent / Footer 都有机会进入 render
```

可以改成：

```tsx
function Header() {
  const [open, setOpen] = useState(false);

  return ...
}
```

于是：

```text
Header update
↓
Header subtree render
```

其他 sibling 不进入该更新区域。

---
## state 的位置决定 update source
从 Fiber 角度：

```text
state 所在组件
↓
对应 Fiber
↓
成为 update source
```

如果 state 在：

```text
Page Fiber
```

更新从 Page 开始。

如果 state 在：

```text
Header Fiber
```

更新从 Header subtree 开始。

因此：

> state placement（状态位置）本身就是 performance boundary（性能边界）。

---
## 状态上提
状态不能为了性能无限下沉。

如果：

```text
Sidebar
+
Detail
```

都需要同一个：

```text
selectedId
```

就应该把 state 放在：

> 两者的最近公共祖先。

例如：

```text
Page
├─ Sidebar
└─ Detail
```

state owner：

```text
Page
```

所以状态设计第一优先级仍然是：

> ownership 正确。

不是：

> state 放得越低越好。

---
## 状态上提的代价
state 放得越高：

```text
潜在 render surface 越大
```

例如：

```text
App
├─ Header
├─ Sidebar
├─ Content
└─ Footer
```

如果大量局部 state 都放 App：

```text
任何小更新
↓
App render
↓
整个 subtree 都有机会参与
```

所以不要因为：

```text
“放 App 最方便”
```

就把所有 state 提到最顶层。

---
## Context / Store / memo 本质上都是 render boundary 问题
这轮可以把之前学过的知识统一起来：

```text
state colocation
↓
缩小 update source

Context splitting
↓
缩小 Context consumer 范围

selector
↓
缩小 subscription 范围

memo
↓
阻断 Parent → Child propagation

useMemo / useCallback
↓
保证 memo boundary 所需的 identity 稳定
```

它们本质上都在解决：

> **哪些 Fiber 真正需要参与这次更新？**

---
## 性能优化的三个层次
可以记成：

---
## 第一层：State boundary
```text
state 放在哪个 Fiber？
```

决定：

```text
update 从哪里开始
```

---
## 第二层：Subscription boundary
例如：

```text
Context
external store selector
```

决定：

```text
哪些 consumer 收到更新
```

---
## 第三层：Memo boundary
```tsx
memo(Component)
```

决定：

```text
Parent render 时
哪些 Child 能 bailout
```

最终：

```text
State placement
↓
Subscription granularity
↓
Memoization boundary
```

---
## 性能优化总 mental model
最终可以压缩成一句：

> **React 性能优化的核心，不是消灭 render，而是让真正需要更新的 Fiber 尽可能局部，并让昂贵但无关的 subtree 尽早 bailout。**

诊断流程：

```text
用户感觉卡顿
↓
Profiler
↓
找慢 commit
↓
Ranked 找 expensive component
↓
Flamegraph 看 render propagation
↓
确定更新来源
↓
选择策略

state 问题
→ state colocation / lifting

Context
→ split Context

Store
→ selector

Parent propagation
→ memo

props identity
→ useCallback / useMemo

大型列表
→ virtualization
```

---
## 当前学习进度更新
这轮之后，「渲染与性能诊断」主干已经基本完成：

```text
Context 更新传播与拆分 ✅
Profiler ✅
Ranked / Flamegraph ✅
render cost 判断 ✅
memo ✅
useCallback / useMemo ✅
props identity ✅
state 上提 / 下沉 ✅
virtualization ✅（此前已掌握）
```

因此这一模块已经不再是明显短板。

后续更适合通过真实项目继续练：

```text
Profiler 定位
→ 分析更新原因
→ 优化
→ 再次 Profile 验证
```

而不是继续堆更多性能 API。
