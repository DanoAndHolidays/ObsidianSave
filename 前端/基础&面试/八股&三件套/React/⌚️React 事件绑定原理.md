# ⌚️React 事件绑定原理
> Last Format Time：9/16/2026 19:24:51

Event Delegation（事件委托） + SyntheticEvent（合成事件） + Fiber 事件分发机制：
```text
JSX 中声明事件
    ↓
React 记录事件处理函数
    ↓
Root 容器统一监听原生 DOM 事件
    ↓
浏览器事件触发并冒泡到 Root
    ↓
React 根据 target 找到对应 Fiber
    ↓
沿 Fiber 树收集事件处理函数
    ↓
按照 capture / bubble 顺序执行
```

---
## 不是简单的 DOM 直接绑定
例如：
```jsx
<button onClick={handleClick}>
  Click
</button>
```

不能简单理解为 React 就执行：
```js
button.addEventListener("click", handleClick)
```

React 通常采用 事件委托：
```text
root
 └─ div
     └─ button
```

React 会在 Root 容器统一监听 `click` 等原生事件，当用户点击 `button`：
```text
button
  ↓
div
  ↓
root
```

原生事件冒泡到 Root 后，再由 React 进行事件分发。

---
## 事件委托
如果页面有大量元素：
```jsx
<button onClick={...} />
<button onClick={...} />
<button onClick={...} />
...
```

如果每个 DOM 都直接绑定大量原生监听器，管理会更加复杂，React 通过 Root 统一监听，可以：
- 集中管理事件
- 统一处理事件传播
- 配合 React 更新调度
- 支持组件树 / Fiber 树上的事件传播
- 避免大量重复的 DOM 事件管理逻辑

---
## 如何找到事件处理函数
当浏览器产生：
```js
nativeEvent.target
```

例如 target 是：
```html
<button>
```

React 可以通过 DOM 节点找到其对应的：
```text
DOM Node
   ↓
Fiber
```

然后沿 Fiber：
```text
Button Fiber
     ↓ return
Parent Fiber
     ↓ return
App Fiber
```

向上查找事件处理函数。

例如：
```jsx
<div onClick={handleParent}>
  <button onClick={handleChild}>
    Click
  </button>
</div>
```

React 可以收集：
```text
Button Fiber
→ handleChild

Parent Fiber
→ handleParent
```

然后按照事件传播顺序执行。

---
## Capture 和 Bubble
React 同样支持：
```jsx
<div
  onClickCapture={handleCapture}
  onClick={handleBubble}
>
  <button onClick={handleButton}>
    Click
  </button>
</div>
```

事件执行可以理解为两个阶段。

### Capture Phase
从外向内：
```text
Parent
 ↓
Child
```

对应：
```jsx
onClickCapture
```

### Bubble Phase
从内向外：
```text
Child
 ↑
Parent
```

对应：
```jsx
onClick
```

所以整体可以理解成：
```text
Root
 ↓
Parent Capture
 ↓
Button Capture

Button Bubble
 ↑
Parent Bubble
 ↑
Root
```

---
## SyntheticEvent 合成事件
React 事件处理函数拿到的：
```jsx
function handleClick(event) {
  console.log(event)
}
```

这里的 `event` 是 React 提供的：
```text
SyntheticEvent
合成事件
```

而不是简单直接暴露浏览器的原生 Event，SyntheticEvent 对原生事件做了一层统一封装。

常用 API：
```js
event.target

event.currentTarget

event.preventDefault()

event.stopPropagation()
```

如果需要访问原生事件：
```js
event.nativeEvent
```

关系可以理解为：
```text
Browser Native Event
        ↓
 React SyntheticEvent
        ↓
  事件处理函数
```

---
## React 17 前后的变化
### React 16 及之前
事件委托主要绑定在：
```text
document
```

大致：
```text
document
   ↑
React App
```

### React 17+
事件主要委托到：
```text
React Root Container
```

例如：
```js
createRoot(
  document.getElementById("root")
)
```

结构：
```text
document
   ↓
#root
   ↓
React App
```

这样更利于：
- 多个 React Root 共存
- React 和其他框架共存
- 微前端
- 不同 React 版本共存

---
## 整体流程
记住这一条即可：
```text
用户点击 DOM
   ↓
浏览器产生 native click event
   ↓
事件冒泡到 React Root
   ↓
React 统一事件监听器收到事件
   ↓
根据 event.target 找到对应 Fiber
   ↓
沿 Fiber 树收集监听器
   ↓
构造 SyntheticEvent
   ↓
执行 Capture listeners
   ↓
执行 Bubble listeners
   ↓
事件处理函数触发 setState
   ↓
进入 React 更新调度流程
```

---
## 面试版回答

> React 的事件系统主要基于 Event Delegation，也就是事件委托。React 不会简单地给每个 JSX DOM 节点分别绑定对应的原生监听器，而是在 Root 容器统一监听一批原生事件。
> 
> 当浏览器事件触发后，事件会冒泡到 Root，React 根据 `event.target` 找到对应的 Fiber，然后沿 Fiber 树收集 `onClickCapture` 和 `onClick` 等事件处理函数，按照捕获和冒泡顺序执行。
> 
> 同时 React 会使用 `SyntheticEvent` 对浏览器原生事件进行封装。React 17 之后，主要的事件委托位置从 `document` 调整为了 React Root Container。
> 
> 因此 React 的事件系统可以理解成：**事件委托 + SyntheticEvent + Fiber 上的事件分发。**
