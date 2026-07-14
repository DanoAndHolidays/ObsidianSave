# LoadingState
> Last Format Time：7/14/2026 20:56:57

---
## 分析
最后这一行：

```tsx
LoadingState.displayName = "LoadingState";
```

**它不会影响组件的功能，也不会影响页面渲染。**它的作用主要是**给组件起一个显示名称（Display Name）**，方便 React 的开发工具和错误信息显示。

---
## 什么是 displayName？
React 的每个组件都有一个名字。

例如：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

React 会自动知道它叫：

```text
LoadingState
```

在 React DevTools 中，你会看到：

```text
<App>
  <LoadingState>
```

---
## 为什么这里还要手动设置？
你的组件写法是：

```tsx
export const LoadingState = function ({
  message = "Loading...",
  className,
}: LoadingStateProps) {
  ...
};
```

实际上这是一个**匿名函数赋值**：

```tsx
const LoadingState = function (...) {
}
```

虽然现代 JavaScript 引擎通常能推断出它叫 `LoadingState`，但并不是所有场景都能可靠推断。

因此很多组件库都会显式指定：

```tsx
LoadingState.displayName = "LoadingState";
```

这样 React 一定知道它叫什么。

---
## forwardRef 更需要 displayName
真正经常看到 `displayName` 的地方，其实是 `forwardRef`。

例如你前面那个 `Label`：

```tsx
export const Label = forwardRef(...)
```

如果不写：

```tsx
Label.displayName = "Label";
```

React DevTools 里可能显示：

```text
ForwardRef
```

而不是：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

甚至更糟：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

这样调试的时候完全不知道哪个组件是谁。

加上：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

以后：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

一眼就知道。

---
## 普通函数组件需要吗？
对于普通函数组件：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

通常**不需要**。

因为 React 已经知道名字。

甚至：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

React 现在一般也能识别。

所以：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

很多时候只是为了：

- 保持整个项目代码风格一致
    
- 防止构建压缩后名字丢失
    
- 方便 React DevTools 调试
    

---
## 为什么很多 UI 库都会写？
像 shadcn/ui、Radix UI、Material UI 等组件库几乎都会写：

```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

原因就是**统一规范**。

无论这个组件是不是：

- `forwardRef`
    
- `memo`
    
- `lazy`
    
- `HOC`（高阶组件）
    

React DevTools 都能稳定显示正确名字。


### 总结
```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```

的作用只有一个：

> **告诉 React，这个组件的显示名称叫 `LoadingState`，方便开发调试和 React DevTools 展示。**

它**不会影响组件逻辑、性能或最终页面效果**。对于普通函数组件来说通常是可选的，但对于 `forwardRef`、`memo` 等包装后的组件，设置 `displayName` 是一种很好的实践。

---
## 源码
```tsx
function LoadingState() {
  return <div>Loading...</div>;
}
```