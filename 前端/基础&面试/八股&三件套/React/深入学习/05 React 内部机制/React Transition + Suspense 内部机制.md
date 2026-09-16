# React Transition + Suspense 内部机制
> Last Format Time：9/16/2026 19:24:52

---
## 整体主线
可以先把整个过程压缩成：

```text
startTransition
↓
Update 获得 Transition Lane
↓
Transition render 可以被 urgent update 抢占
↓
render 过程中组件 suspend
↓
Suspense 捕获这次 suspend
↓
选择 fallback 或继续保留旧 UI
↓
Promise resolve
↓
ping / retry
↓
重新调度
↓
重新 render primary content
↓
成功后 commit
```

其中最核心的三个概念是：

```text
Transition
=
决定“这次更新急不急”

Suspense
=
决定“candidate UI 当前能不能完成”

Ping / Retry
=
决定“之前没完成的 work 什么时候重新尝试”
```


# 2. `startTransition` 到底做了什么

```tsx
startTransition(() => {
  setTab("posts");
});
```

不要理解成：

```text
稍后执行 setTab
```

`startTransition` 中的 callback 仍然是同步执行的。

真正发生的是：

```text
startTransition
↓
建立 Transition context（Transition 上下文）
↓
同步执行 callback
↓
callback 内调用 setState
↓
创建 Update
↓
Update 请求 Lane
↓
发现当前处于 Transition context
↓
获得 Transition Lane
```

所以：

> `startTransition` 不是直接给 `setState` 打标签，而是建立一个 Transition execution context（Transition 执行上下文）。

Update 在创建时读取这个上下文，从而获得 Transition Lane。


# 3. Transition Lane 表示什么

Lane 可以理解成：

> 一份 Update / render work 的调度身份。

所以：

```text
Transition Lane
```

表达的是：

> 这个 Update 属于 non-urgent update（非紧急更新），可以给更紧急的工作让路。

例如：

```tsx
startTransition(() => {
  setTab("posts");
});
```

产生：

```text
setTab
↓
Update
↓
Transition Lane
```

而输入框：

```tsx
setText(value);
```

如果不在 Transition 中，则通常属于更高优先级的用户交互更新。


# 4. Transition 为什么可以被 urgent update 抢占

假设 React 正在：

```text
render Posts
```

对应：

```text
Transition Lane
```

这时候用户继续输入：

```text
setText("a")
↓
urgent Lane
```

Root 中可能同时存在：

```text
urgent Lane
Transition Lane
```

调度时更高优先级的 urgent work 会先执行。

所以：

```text
Transition render
↓
暂时停止 / 放弃当前 candidate work

urgent render
↓
完成
↓
commit

然后
↓
Transition 仍然 pending
↓
以后重新 render
```

关键：

> 被抢占时，丢弃的是当前 speculative render（推测性渲染结果），不是 Transition Update 本身。

即：

```text
❌ Transition Update 消失

✅ 当前 WIP candidate 可以被放弃
✅ Update 仍然存在
✅ 后续重新计算
```


# 5. React 的抢占不是暂停 JavaScript 到任意一行

React 的 concurrent rendering（并发渲染）本质上仍然是 cooperative scheduling（协作式调度）。

可以理解成：

```text
处理一个 Fiber
↓
处理一个 Fiber
↓
处理一个 Fiber
↓
检查是否该让出执行权
↓
yield
```

不是：

```text
组件函数执行到第 37 行
↓
强制冻结 JavaScript
↓
未来从第 38 行继续
```

Fiber 保存的是 React 自己的工作结构，而不是完整 JavaScript call stack。


# 6. 什么是 suspend

例如：

```tsx
function Page() {
  const posts = use(postsPromise);

  return <PostList posts={posts} />;
}
```

如果：

```text
postsPromise = pending
```

那么：

```text
Page
↓
当前缺少完成 render 所需的数据
↓
无法产出完整 UI
↓
suspend
```

最适合的理解是：

> suspend = 当前这条 render 路径暂时无法完成。

也就是说：

```text
candidate UI
```

目前不能完整构建出来。


# 7. Suspense 本质不是“显示 loading 的组件”

例如：

```tsx
<Suspense fallback={<Spinner />}>
  <Page />
</Suspense>
```

第一次处理 Suspense 时，React 并不知道 `Page` 会 suspend。

所以流程是：

```text
Suspense
↓
先尝试 primary content

Page
↓
suspend
```

这时候：

```text
Suspense → Page
```

这条 render 路径失败。

React 会向上找到最近能够处理 suspend 的 Suspense Boundary。


# 8. Suspense 如何切到 fallback

核心过程：

```text
第一次 render Suspense
↓
尝试 primary children
↓
Page
↓
suspend
↓
当前 primary 路径失败
↓
回退到最近 Suspense Boundary
↓
标记“这个 Boundary 捕获到了 suspend”
↓
再次处理 Suspense
↓
这次选择 fallback branch
↓
Spinner
```

所以不要理解成：

```text
Page suspend
↓
React 直接把 Page 替换成 Spinner
```

更准确的是：

```text
第一次：
Suspense
↓
Page
↓
失败

第二次：
Suspense
↓
Spinner
```


# 9. fallback 本身也是一棵正常 React Tree

可以把 Suspense 想成有两个 branch（分支）：

```text
Suspense
│
├── primary branch
│   └── Page
│
└── fallback branch
    └── Spinner
```

正常情况：

```text
选择 primary
```

suspend 后：

```text
primary 无法完成
↓
选择 fallback
```

`Spinner` 依然需要正常经历：

```text
render
↓
Fiber 构建
↓
complete
↓
commit
```

不是 React 绕过 Fiber 偷偷插入 DOM。


# 10. Nested Suspense 为什么能局部 loading

例如：

```tsx
<Suspense fallback={<PageSpinner />}>
  <Header />

  <Suspense fallback={<CommentsSpinner />}>
    <Comments />
  </Suspense>
</Suspense>
```

如果：

```text
Comments suspend
```

React 会向上找到最近的 Boundary：

```text
Comments
↑
Inner Suspense
```

于是变成：

```text
Outer Suspense
│
├── Header
│
└── Inner Suspense
    └── CommentsSpinner
```

而不会直接：

```text
整个页面 → PageSpinner
```

因此：

> Suspense Boundary 决定 loading / reveal 的隔离范围。


# 11. Promise resolve 不代表 UI 自动恢复

假设 fallback 已经 commit：

```text
当前屏幕：

Spinner
```

然后：

```text
postsPromise
pending
↓
fulfilled
```

UI 并不会直接：

```text
Spinner → Page
```

Promise resolve 只是：

> 通知 React：“之前阻塞你的条件可能已经满足，可以再试一次了。”

可以把它理解成：

```text
Promise resolve
=
按门铃
```

React收到通知后：

```text
安排一次新的 render
```


# 12. 为什么 Promise resolve 后还必须重新 render

例如：

```tsx
function Page() {
  const user = use(userPromise);
  const posts = use(postsPromise);

  return ...
}
```

即使：

```text
userPromise fulfilled
```

也可能：

```text
postsPromise pending
```

所以 React 不能认为：

```text
一个 Promise resolve
=
整个 Page 一定 ready
```

必须重新：

```text
render Page
↓
重新执行逻辑
↓
检查所有依赖
↓
确认能否完成
```


# 13. Retry 到底是什么

Retry 不是什么新的渲染系统。

它本质上只是：

> 告诉 Scheduler：“这个 Suspense Boundary 现在值得再尝试一次 render 了。”

如果 fallback 已经显示，可以理解成：

```text
Promise resolve
↓
Suspense 获得 retry work
↓
Root 被重新调度
↓
再次 render Suspense
```

Retry Lane 可以理解为：

```text
“这是一次 Suspense 恢复尝试”
```

对比：

```text
Transition Lane
=
“我要切换到 Posts”

Retry Lane
=
“Posts 之前没完成，现在可能好了，再试一下”
```


# 14. Promise resolve 后如何恢复 primary content

假设当前：

```text
current：

Suspense
└── Spinner
```

Promise resolve：

```text
Promise fulfilled
↓
React 收到通知
↓
schedule retry
↓
重新 render
```

再次处理 Suspense：

```text
Suspense
↓
重新尝试 primary branch
↓
Page()
```

这次：

```text
use(postsPromise)
↓
fulfilled
↓
得到 postsData
↓
继续 render
```

最终得到：

```text
WIP：

Suspense
└── Page
    └── PostList
```

render 成功后：

```text
commit
```

最终：

```text
Spinner
↓
Page
```


# 15. Suspense 恢复是 restart，不是 resume

这是非常重要的一点。

第一次：

```tsx
function Page() {
  const a = calculateA();

  const data = use(promise);

  const b = calculateB(data);

  return ...
}
```

如果在：

```text
use(promise)
```

这里 suspend。

Promise resolve 后 React 不会：

```text
从 use() 后面继续执行
```

而是：

```text
重新调用 Page()
↓
从函数开头重新执行
```

即：

```text
第一次：

Page()
↓
use()
↓
suspend


第二次：

Page()
↓
use()
↓
fulfilled
↓
继续完成
```

所以：

> Suspense recovery（Suspense 恢复）本质是 restart render，而不是 resume JavaScript function。


# 16. 为什么 render 必须保持 pure（纯）

因为 React 可能：

```text
render
↓
suspend
↓
丢弃

重新 render
↓
又被抢占

再 render
↓
成功
```

所以如果 render 中有：

```tsx
function Page() {
  chargeCreditCard();

  const data = use(promise);

  ...
}
```

可能执行多次。

因此 render 必须尽量只做：

```text
输入
↓
计算 UI
```

不能依赖“组件函数只执行一次”。


# 17. 普通 Suspense 与 Transition + Suspense 的区别

---
## 普通更新
```text
Home
↓
切 Posts
↓
Posts suspend
↓
Spinner
↓
Promise resolve
↓
retry
↓
Posts
```

用户看到：

```text
Home
↓
Spinner
↓
Posts
```

---
## Transition 更新
```tsx
startTransition(() => {
  setTab("posts");
});
```

React可能：

```text
Home current
↓
后台构建 Posts candidate
↓
Posts suspend
↓
继续保留 Home
↓
Promise resolve
↓
重新尝试 Posts
↓
成功
↓
commit
```

用户看到：

```text
Home
↓
Home
↓
Posts
```

不会一定经过 Spinner。


# 18. Transition 为什么可以继续保留旧 UI

核心原则：

> 已经展示给用户的完整 UI，不要因为一个 non-urgent update 突然消失。

例如当前：

```text
Suspense
└── Home ✅
```

然后：

```tsx
startTransition(() => {
  setTab("posts");
});
```

candidate：

```text
Suspense
└── Posts
```

Posts suspend。

React有两个选择：

```text
A：
Home
↓
Spinner
↓
Posts
```

或者：

```text
B：
Home
↓
Home
↓
Posts
```

由于这是 Transition，React倾向 B。

原因：

```text
Home
=
已经 revealed（展示）
+
完整
+
可交互

Posts
=
non-urgent
+
暂时无法完成
```

因此没必要为了一个非紧急 candidate 把当前好好的 UI 隐藏。


# 19. Transition 不代表“永远不显示 fallback”

这一点非常重要。

错误理解：

```text
startTransition
=
禁止 Suspense fallback
```

正确理解：

```text
Transition
+
已经展示过的 Boundary
+
新的 primary render suspend
↓
尽量保留旧 primary
```


# 20. 新 Suspense Boundary 仍然可以显示 fallback

例如：

```tsx
function ArtistPage() {
  return (
    <>
      <Biography />

      <Suspense fallback={<AlbumsSkeleton />}>
        <Albums />
      </Suspense>
    </>
  );
}
```

如果这个页面是刚进入的：

```text
ArtistPage
│
├── Biography ✅
└── Albums Suspense
    └── Albums ❌
```

这个内层 Boundary 以前根本没显示过自己的 primary content。

因此没有：

```text
旧 Albums UI
```

需要保护。

所以完全可以 commit：

```text
ArtistPage
│
├── Biography
└── AlbumsSkeleton
```

等 Albums 好了：

```text
AlbumsSkeleton
↓
Albums
```


# 21. Nested Suspense 决定 UI reveal granularity

例如：

```tsx
<Suspense fallback={<PageSpinner />}>
  <Header />
  <Biography />
  <Albums />
</Suspense>
```

如果：

```text
Albums suspend
```

那么整个外层 Boundary 都不能完成。


如果改成：

```tsx
<Suspense fallback={<PageSpinner />}>
  <Header />
  <Biography />

  <Suspense fallback={<AlbumsSkeleton />}>
    <Albums />
  </Suspense>
</Suspense>
```

即使：

```text
Albums suspend
```

外层仍然可以得到一棵完整 candidate：

```text
Page
│
├── Header
├── Biography
└── AlbumsSkeleton
```

因为：

> Inner Suspense 显示 fallback，本身也是一棵完整 UI。

因此新页面可以先 commit。


# 22. Suspense Boundary 真正定义的是什么

不要只理解成：

```text
loading 放在哪里
```

更准确的是：

> Suspense Boundary 定义 UI 的 reveal unit（展示单元）。

也就是：

```text
哪些东西需要一起 ready
哪些东西可以以后再出现
```

例如：

```text
Page
├── Header
├── Biography
├── Suspense Albums
├── Suspense Comments
└── Suspense Recommendations
```

意味着：

```text
页面主体可以先出现

Albums
Comments
Recommendations

分别准备好以后再 reveal
```


# 23. urgent update 为什么不一定保留 stale UI

如果不是：

```tsx
startTransition(...)
```

而是：

```tsx
setTab("posts");
```

这是 urgent update。

如果 Posts suspend，React不再拥有：

```text
“这个更新不急，可以继续显示旧页面”
```

这个语义。

所以可能：

```text
Home
↓
Spinner
↓
Posts
```

可以简单理解：

### Urgent
```text
“用户要求现在更新。”

React：
旧 UI 不能继续假装是最新状态。
```

### Transition
```text
“这个更新可以后台准备。”

React：
旧 UI 再保持一段时间也可以。
```


# 24. `key` 可以主动重置 Suspense Boundary

例如：

```tsx
<Suspense
  key={userId}
  fallback={<ProfileSkeleton />}
>
  <Profile userId={userId} />
</Suspense>
```

从：

```text
userId = 1
```

变成：

```text
userId = 2
```

因为 `key` 改变：

```text
Boundary identity 改变
```

React会把它看作新的 Boundary。

于是即使在 Transition 中，也可以：

```text
User 1
↓
ProfileSkeleton
↓
User 2
```

而不是继续把 User 1 当作 User 2 的 stale UI。


# 25. Transition + Suspense 的最终 mental model

---
## Transition
```text
“这版 UI 不急着马上替换 current。”
```

它解决：

> 这次更新应该以什么调度优先级处理？

---
## Suspense
```text
“这部分 candidate 现在完成不了。”
```

它解决：

> 当前 render 遇到暂时缺失的数据怎么办？

---
## Suspense Boundary
```text
“如果 primary 完成不了，
我可以切到 fallback。”
```

同时它定义：

> 哪些内容应该作为一个 reveal unit 一起出现。

---
## 已展示的 Suspense Boundary
在 Transition 中：

```text
新的 primary suspend
↓
尽量继续保留旧 primary
```

避免：

```text
完整 UI
↓
突然消失
↓
Spinner
```

---
## 新 Suspense Boundary
```text
没有旧 primary content 可以保留
↓
允许立即显示 fallback
```

---
## Nested Suspense
```text
把一个很大的 loading 单元
拆成多个独立 reveal 单元
```

---
## Promise resolve
```text
不是：
直接修改 UI

而是：
“之前阻塞你的东西可能好了，
可以再 render 一次。”
```

---
## Retry
```text
“这个 Suspense Boundary
现在值得重新尝试 primary content。”
```


# 26. 最终完整闭环

```text
startTransition
↓
建立 Transition context
↓
setState
↓
Update 获得 Transition Lane
↓
Scheduler 开始 concurrent render
↓
Transition 可以被 urgent update 抢占
↓
抢占只丢弃当前 candidate work
↓
Transition Update 仍然 pending
↓
重新 render
↓
组件读取 pending Promise
↓
suspend
↓
当前 primary candidate 无法完成
↓
找到最近 Suspense Boundary
↓
回退到 Boundary
↓
重新处理 Suspense
↓
决定：

├─ 保留旧 revealed UI
│
└─ 或 render fallback

↓
Promise resolve
↓
通知 React
↓
ping / retry
↓
重新调度
↓
重新 render Suspense primary
↓
组件函数从头重新执行
↓
Promise fulfilled
↓
primary render 成功
↓
commit
↓
candidate 成为新的 current UI
```


# 27. 最值得记住的几句话

> **Transition Lane 描述“这个 Update 应该怎么被调度”。**

> **Transition 被抢占时，丢掉的是 speculative render，不是 Update。**

> **Suspense 描述“这次 candidate render 当前能不能完成”。**

> **Suspense fallback 不是临时插入的 DOM，而是 Boundary 选择的另一棵 React subtree。**

> **Promise resolve 不会直接恢复 UI，只会让 React 获得一次重新尝试 render 的机会。**

> **Suspense 恢复是 restart render，不是从原 JavaScript 函数暂停位置继续执行。**

> **Transition 决定旧 UI 能不能继续保留；Suspense Boundary 决定新 UI 至少准备到什么粒度才能 reveal。**

> **Nested Suspense 决定哪些区域可以先展示，哪些区域以后再补。**