# Dialog
> Last Format Time：7/14/2026 20:56:57

---
## 分析
这是一个非常典型的 **受控（Controlled）Dialog 组件**，里面其实包含了 React 中几个很重要的思想：

- **受控组件（Controlled Component）**
    
- **单向数据流（One-way Data Flow）**
    
- **组件职责分离**
    
- **useEffect 生命周期**
    
- **useCallback 的作用**
    
- **事件冒泡的利用**
    

我按整个执行流程来讲，而不是一行一行翻译。


# 先看整个组件的职责

这个 Dialog 自己其实**什么状态都不保存**。

它只负责：

> **"你告诉我开，我就显示；你告诉我关，我就消失。"**

它根本不决定自己什么时候打开。

所以 Props 只有

```ts
interface DialogProps {
  open: boolean;
  onClose: () => void;
}
```

意思就是

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

父组件说：

```text
open = true
```

Dialog 就显示。

父组件说：

```text
open = false
```

Dialog 就直接 return null。


# Dialog 为什么没有 useState？

很多初学 React 的人第一反应会写成这样：

```tsx
const [open, setOpen] = useState(false);
```

但是这里作者故意没有这么做。

为什么？

因为：

> **Dialog 不应该拥有这个状态。**

举个例子。

假设父组件：

```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

如果 Dialog 自己维护：

```tsx
const [open, setOpen] = useState(false);
```

那外面的按钮怎么办？

```text
按钮点击
     │
     ▼
Dialog里面的open？
```

外面根本拿不到。

因为：

```text
App
 │
 └── Dialog
       │
       └── open(state)
```

这个 state 被封死在 Dialog 里面。

父组件根本没法控制。

React 提倡：

> **谁拥有数据，谁负责修改数据。**

所以真正的写法应该是：

```tsx
const App = () => {
    const [open, setOpen] = useState(false);

    return (
        <>
            <button onClick={() => setOpen(true)}>
                打开
            </button>

            <Dialog
                open={open}
                onClose={() => setOpen(false)}
            />
        </>
    );
}
```

数据流就是：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

只有一份状态。

不会出现两个 open 不同步。


# 这就是 React 的受控组件

整个 Dialog 属于

> Controlled Component

受控组件的特点就是：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

这些状态全部来自父组件。

例如：

Input

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

Checkbox

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

Dialog

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

是不是一模一样？


# Dialog 是怎么关闭的？

看这里：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

它根本没有：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

而是：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

真正执行的是：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

所以：

```text
父组件
    │
    │ open=true
    ▼
 Dialog
```

整个关闭流程其实都是父组件完成的。


# 为什么 return null？

这里：

```text
open = true
```

React 中：

```text
open = true
```

意思就是：

> 什么都不渲染。

不是隐藏。

不是：

```text
open = true
```

而是：

```text
open = true
```

比如：

```text
open = true
```

关闭以后：

```text
open = true
```

React 连节点都不会创建。

所以性能很好。


# useEffect 为什么放这里？

```text
open = true
```

作用：

当 Dialog 打开以后：

```text
open = true
```

关闭以后：

```text
open = true
```

为什么？

如果一直监听：

```text
open = true
```

没有意义。

所以：

```text
open = false
```

只有：

```text
open = false
```


# 为什么要 return 一个函数？

React 的 Effect：

```text
open = false
```

所以：

第一次：

```text
open = false
```

关闭：

```text
open = false
```

这样不会越来越多。

否则：

```text
open = false
```

ESC 一按：

```text
open = false
```

典型的内存泄漏。


# handleKeyDown

```text
open = false
```

监听：

```text
open = false
```

这样用户体验很好。

几乎所有 Dialog 都支持 ESC。


# 为什么点击 Dialog 不关闭？

这里：

```text
open = false
```

里面：

```tsx
const [open, setOpen] = useState(false);
```

原因是：

事件会冒泡。

假设：

```tsx
const [open, setOpen] = useState(false);
```

点击 Dialog：

```tsx
const [open, setOpen] = useState(false);
```

如果 Overlay：

```tsx
const [open, setOpen] = useState(false);
```

那么：

点击 Dialog

↓

事件冒泡

↓

Overlay 收到

↓

关闭

这就出问题了。

所以：

```tsx
const [open, setOpen] = useState(false);
```

意思就是：

```tsx
const [open, setOpen] = useState(false);
```

这样：

```tsx
const [open, setOpen] = useState(false);
```


# 为什么 Overlay 单独放一个 div？

```tsx
const [open, setOpen] = useState(false);
```

而不是：

```tsx
const [open, setOpen] = useState(false);
```

原因是：

遮罩需要：

```tsx
const [open, setOpen] = useState(false);
```

Dialog：

```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

两者职责不同。

所以：

```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

这也是很多 UI 库的实现方式。


# useCallback 为什么这里大量使用？

例如：

```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

原因不是为了性能优化按钮点击，而是为了**保持函数引用稳定**。

特别是 `handleKeyDown` 被 `useEffect` 依赖：

```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

如果每次渲染都创建新的 `handleKeyDown`：

```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

那么 `handleKeyDown` 的引用每次都会变化，`useEffect` 就会先移除旧监听，再添加新监听。虽然功能仍然正确，但会产生不必要的重复工作。使用 `useCallback` 后，只要依赖没有变化，函数引用保持不变，`useEffect` 就不会重复执行。

需要说明的是，这里的 `useCallback` 并不是绝对必要的，因为 `Dialog` 本身在 `open` 为 `false` 时直接返回 `null`，重新渲染的次数通常不会很多。如果去掉它，组件依然能正常工作，只是在某些重新渲染场景下会多做几次事件解绑和绑定。很多团队会保留它，让依赖关系更清晰，也避免未来组件变复杂后出现不必要的 Effect 执行。

---
## 整个组件的数据流可以总结成下面这张图
```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

这个设计体现了 React 推荐的思想：**组件专注于展示和交互，状态由更高层统一管理**。这样 `Dialog` 就变成了一个高度可复用的组件——无论是点击按钮、接口返回、路由切换，还是其他业务逻辑，都可以通过修改 `open` 来控制它，而 `Dialog` 自身无需知道这些细节。

---
## 具体实现
```tsx
const App = () => {
    return (
        <>
            <Dialog />
            <button>打开</button>
        </>
    )
}
```

==insert==

|写法|等价于|
|---|---|
|`inset: 0`|`top: 0; right: 0; bottom: 0; left: 0;`|
|`inset: 10px`|四个方向都是 `10px`|
|`position: absolute; inset: 0;`|元素铺满父元素|
|`position: fixed; inset: 0;`|元素铺满整个视口（浏览器窗口）|
