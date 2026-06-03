# 使用Effect进行同步操作

## 什么是 Effect，它与事件（event）有何不同？ [](https://zh-hans.react.dev/learn/synchronizing-with-effects#what-are-effects-and-how-are-they-different-from-events "Link for 什么是 Effect，它与事件（event）有何不同？")

在接触 Effect 之前，你需要熟悉 React 组件中的两种逻辑类型：

- **渲染代码**（在 [描述 UI](https://zh-hans.react.dev/learn/describing-the-ui) 中有介绍）位于组件的顶层。你在这里处理 props 和 state，对它们进行转换，并返回希望在页面上显示的 JSX。[渲染代码必须是纯粹的](https://zh-hans.react.dev/learn/keeping-components-pure)——就像数学公式一样，它只应该“计算”结果，而不做其他任何事情。
    
- **事件处理程序**（在 [添加交互性](https://zh-hans.react.dev/learn/adding-interactivity) 中有介绍）是组件内部的嵌套函数，它们不光进行计算, 还会执行一些操作。事件处理程序可能会更新输入字段、提交 HTTP POST 请求来购买产品，或者将用户导航到另一个页面。事件处理程序包含由特定用户操作（例如按钮点击或输入）引起的“副作用”（它们改变了程序的状态）。
    

有时这还不够。考虑一个 `ChatRoom` 组件，它在页面上显示时必须连接到聊天服务器。连接到服务器并不是纯粹的计算（它是一个副作用），因此它不能在渲染期间发生。然而，并没有一个特定的事件（比如点击）能让 `ChatRoom` 被显示。

**Effect 允许你指定由渲染自身，而不是特定事件引起的副作用**。在聊天中发送消息是一个“事件”，因为它直接由用户点击特定按钮引起。然而，建立服务器连接是一个 Effect，因为无论哪种交互致使组件出现，它都应该发生。Effect 在 [提交](https://zh-hans.react.dev/learn/render-and-commit) 结束后、页面更新后运行。此时是将 React 组件与外部系统（如网络或第三方库）同步的最佳时机。

在本文此处和后续文本中，大写的 `Effect` 是 React 中的专有定义——由渲染引起的副作用。至于更广泛的编程概念(任何改变程序状态或外部系统的行为)，我们则使用“副作用（side effect）” 来指代。

## 如何编写 Effect [](https://zh-hans.react.dev/learn/synchronizing-with-effects#how-to-write-an-effect "Link for 如何编写 Effect")

要编写一个 Effect, 请遵循以下三个步骤：

1. **声明 Effect**。通常 Effect 会在每次 [提交](https://zh-hans.react.dev/learn/render-and-commit) 后运行。
2. **指定 Effect 依赖**。大多数 Effect 应该按需运行，而不是在每次渲染后都运行。例如，淡入动画应该只在组件出现时触发。连接和断开服务器的操作只应在组件出现和消失时，或者切换聊天室时执行。你将通过指定 **依赖项** 来学习如何控制这一点。
3. **必要时添加清理操作**。一些 Effect 需要指定如何停止、撤销，或者清除它们所执行的操作。例如，“连接”需要“断开”，“订阅”需要“退订”，而“获取数据”需要“取消”或者“忽略”。你将学习如何通过返回一个 **清理函数** 来实现这些。

### 第一步：声明 Effect [](https://zh-hans.react.dev/learn/synchronizing-with-effects#step-1-declare-an-effect "Link for 第一步：声明 Effect")

先从 React 中导入 [`useEffect` Hook](https://zh-hans.react.dev/reference/react/useEffect)：

```js
import { useEffect } from 'react';
```

再在组件顶部调用, 并在其中加入一些代码：

```js
function MyComponent() {
  useEffect(() => {
    // 每次渲染后都会执行此处的代码
  });
  return <div />;
}
```

每当你的组件渲染时，React 会先更新页面，然后再运行 `useEffect` 中的代码。换句话说，**`useEffect` 会“延迟”一段代码的运行，直到渲染结果反映在页面上**。

### 陷阱

默认情况下，Effect 会在 **每次** 渲染后运行。**正因如此，以下代码会陷入死循环**：

```
const [count, setCount] = useState(0);useEffect(() => {  setCount(count + 1);});
```

Effect 在渲染结束后运行。更新 state 会触发重新渲染。在 Effect 中直接更新 state 就像是把电源插座的插头插回自身：Effect 运行、更新 state、触发重新渲染、于是又触发 Effect 运行、再次更新 state，继而再次触发重新渲染。如此反复，从而陷入死循环。

Effect 应该用于将你的组件与一个 **外部** 的系统保持同步。如果没有外部系统，你只是想根据其他状态调整一些状态，那么 [你也许不需要 Effect](https://zh-hans.react.dev/learn/you-might-not-need-an-effect)。

### 第二步：指定 Effect 的依赖项 [](https://zh-hans.react.dev/learn/synchronizing-with-effects#step-2-specify-the-effect-dependencies "Link for 第二步：指定 Effect 的依赖项")

默认情况下，Effect 会在 **每次** 渲染后运行。但往往 **这并不是你想要的**：

- 有时，它可能会很慢。与外部系统的同步并不总是即时的，所以你可能希望在不必要时跳过它。例如，你不会想在每次打字时都得重新连接聊天服务器。
- 有时，它可能会出错。例如，你不会想在每次按键时都触发组件的淡入动画。动画应该只在组件首次出现时播放。

通过在调用 `useEffect` 时指定一个 **依赖数组** 作为第二个参数，你可以让 React **跳过不必要地重新运行 Effect**。传入一个空数组 `[]`：

```js
useEffect(() => {    
	// ...  
}, []);
```

指定 `[isPlaying]` 作为依赖数组会告诉 React：如果 `isPlaying` 与上次渲染时相同，就跳过重新运行 Effect。这样一来，输入框的输入不会触发 Effect 重新运行，只有按下播放/暂停按钮会触发。

依赖数组可以包含多个依赖项。只有当你指定的 **所有** 依赖项的值都与上一次渲染时完全相同，React 才会跳过重新运行该 Effect。React 使用 [`Object.is`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/is) 来比较依赖项的值。有关详细信息，请参阅 [`useEffect` 参考文档](https://zh-hans.react.dev/reference/react/useEffect#reference)。

**请注意，你不能随意“选择”依赖项**。如果你指定的依赖项与 React 根据 Effect 内部代码所推断出的依赖项不匹配，你将收到来自 linter 的错误提示。这有助于捕捉代码中的许多 bug。如果你不希望某些代码重新运行，[那么你应当 **修改 Effect 代码本身**，使其不再“需要”该依赖项](https://zh-hans.react.dev/learn/lifecycle-of-reactive-effects#what-to-do-when-you-dont-want-to-re-synchronize)。

### 陷阱

没有依赖数组和使用空数组 `[]` 作为依赖数组，行为是不同的：

```js
useEffect(() => {
  // 这里的代码会在每次渲染后运行
});

useEffect(() => {
  // 这里的代码只会在组件挂载（首次出现）时运行
}, []);

useEffect(() => {
  // 这里的代码不但会在组件挂载时运行，而且当 a 或 b 的值自上次渲染后发生变化后也会运行
}, [a, b]);
```

### 为什么依赖数组中可以省略 ref? 

下面的 Effect 同时使用了 `ref` 与 `isPlaying` prop，但是只有 `isPlaying` 被声明为依赖项：

```js
function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);
  useEffect(() => {
    if (isPlaying) {
      ref.current.play();
    } else {
      ref.current.pause();
    }
  }, [isPlaying]);
```

这是因为 `ref` 具有 **稳定** 的标识：React 确保你在 [每轮渲染中调用同一个 `useRef` 时，总能获得相同的对象](https://zh-hans.react.dev/reference/react/useRef#returns)。ref 不会改变，所以它不会导致重新运行 Effect。因此，在依赖数组中它可有可无。把它加进去也可以：

```js
function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);
  useEffect(() => {
    if (isPlaying) {
      ref.current.play();
    } else {
      ref.current.pause();
    }
  }, [isPlaying, ref]);
```

`useState` 返回的 [`set` 函数](https://zh-hans.react.dev/reference/react/useState#setstate) 也具有稳定的标识，因此它们通常也会被省略。如果在省略某个依赖项时 linter 不会报错，那么这么做就是安全的。

省略始终稳定的依赖项仅在 linter 能“看到”对象是稳定的时候才有效。例如，如果 `ref` 是从父组件传递过来的，则必须在依赖数组中指定它。这很有必要，因为你无法确定父组件是一直传递相同的 ref，还是根据条件传递不同的 ref。所以，你的 Effect 会依赖于被传递的是哪个 ref。

### 第三步：按需添加清理（cleanup）函数

```js
import { useEffect } from 'react';
import { createConnection } from './chat.js';

export default function ChatRoom() {
  useEffect(() => {
    const connection = createConnection();
    connection.connect();
  }, []);
  return <h1>欢迎来到聊天室！</h1>;
}
```

这里的 Effect 仅在组件挂载时运行，所以你可能以为 `"✅ 连接中……"` 只会在控制台中被打印一次。**然而实际情况是 `"✅ 连接中……"` 被打印了两次！为什么会这样**？

假设 `ChatRoom` 组件是一个大型多页面应用中的一部分。用户最初在 `ChatRoom` 页面上。组件挂载并调用 `connection.connect()` 。接着用户可能会导航到另一个页面，比如切换到“设置”页面，于是 `ChatRoom` 组件被卸载。最后，当用户点击“返回”时，`ChatRoom` 组件再次挂载。这将建立第二个连接——但第一个连接从未被销毁！随着用户在应用中来回切换，连接将会不断累积。

这类 bug 在没有大量手动测试的情况下很容易被忽略。为了帮助你快速发现它们，在开发环境中，React 会在组件首次挂载后立即重新挂载一次。

两次出现 `"✅ 连接中……"` 能够帮助你注意到真正的问题：在代码中，组件被卸载时没有关闭连接。

为了解决这个问题，可以在 Effect 中返回一个 **清理（cleanup）函数** 。

```js
useEffect(() => {
    const connection = createConnection();
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, []);
```

现在在开发环境下，你会看到三条控制台日志：

1. `"✅ 连接中……"`
2. `"❌ 连接断开。"`
3. `"✅ 连接中……"`

### 在 Effect 中进行数据请求的问题

在 Effect 中直接编写 `fetch` 请求 [是一种常见的数据获取方式](https://www.robinwieruch.de/react-hooks-fetch-data/)，特别是在完全客户端渲染的应用中。然而，这种方法非常手动化，并且有明显的弊端：

- **Effect 不会在服务端运行**。这意味着最初由服务器渲染的 HTML 只会包含加载状态，而没有实际数据。客户端必须先下载所有的 JavaScript 并渲染应用，才会发现它需要加载数据——这并不高效。
- **直接在 Effect 中进行数据请求，容易产生“网络瀑布（network waterfall）”**。首先父组件渲染时请求一些数据，随后渲染子组件，接着子组件开始请求它们的数据。如果网络速度不快，这种方式会比并行获取所有数据慢得多。
- **直接在 Effect 中进行数据请求往往无法预加载或缓存数据**。例如，如果组件卸载后重新挂载，它必须重新获取数据。
- **不够简洁**。编写 fetch 请求时为了避免 [竞态条件（race condition）](https://maxrozen.com/race-conditions-fetching-data-react-with-useeffect) 等问题，会需要很多样板代码。

**React 总是在执行下一轮渲染的 Effect 之前清理上一轮渲染的 Effect**。