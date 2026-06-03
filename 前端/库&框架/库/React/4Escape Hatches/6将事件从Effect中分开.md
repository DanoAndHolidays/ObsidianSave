# 将事件从Effect中分开

事件处理函数只有在你再次执行同样的交互时才会重新运行。Effect 和事件处理函数不一样，它只有在读取的 props 或 state 值和上一次渲染不一样时才会重新同步。有时你需要这两种行为的混合体：即一个 Effect 只在响应某些值时重新运行，但是在其他值变化时不重新运行。本章将会教你怎么实现这一点。

组件内部声明的 state 和 props 变量被称为 响应式值。

- **事件处理函数内部的逻辑是非响应式的**。除非用户又执行了同样的操作（例如点击），否则这段逻辑不会再运行。事件处理函数可以在“不响应”他们变化的情况下读取响应式值。
- **Effect 内部的逻辑是响应式的**。如果 Effect 要读取响应式值，[你必须将它指定为依赖项](https://zh-hans.react.dev/learn/lifecycle-of-reactive-effects#effects-react-to-reactive-values)。如果接下来的重新渲染引起那个值变化，React 就会使用新值重新运行 Effect 内的逻辑。

## 从 Effect 中提取非响应式逻辑 [](https://zh-hans.react.dev/learn/separating-events-from-effects#extracting-non-reactive-logic-out-of-effects "Link for 从 Effect 中提取非响应式逻辑")

当你想混合使用响应式逻辑和非响应式逻辑时，事情变得更加棘手。

例如，假设你想在用户连接到聊天室时展示一个通知。并且通过从 props 中读取当前 theme（dark 或者 light）来展示对应颜色的通知：

```js
function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      showNotification('Connected!', theme);
    });
    connection.connect();
    // ...
```

但是 `theme` 是一个响应式值（它会由于重新渲染而变化），并且 [Effect 读取的每一个响应式值都必须在其依赖项中声明](https://zh-hans.react.dev/learn/lifecycle-of-reactive-effects#react-verifies-that-you-specified-every-reactive-value-as-a-dependency)。现在你必须把 `theme` 作为 Effect 的依赖项之一：

```js
function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      showNotification('Connected!', theme);
    });
    connection.connect();
    return () => {
      connection.disconnect()
    };
  }, [roomId, theme]); // ✅ 声明所有依赖项
  // ......
```

当 `roomId` 变化时，聊天会和预期一样重新连接。但是由于 `theme` 也是一个依赖项，所以每次你在 dark 和 light 主题间切换时，聊天 **也会** 重连。这不是很好！

换言之，即使它在 Effect 内部（这是响应式的），你也不想让这行代码变成响应式：

```js
      // ...
      showNotification('Connected!', theme);
      // ...
```

你需要一个将这个非响应式逻辑和周围响应式 Effect 隔离开来的方法。

### 声明一个 Effect Event [](https://zh-hans.react.dev/learn/separating-events-from-effects#declaring-an-effect-event "Link for 声明一个 Effect Event")

使用 [`useEffectEvent`](https://zh-hans.react.dev/reference/react/useEffectEvent) 这个特殊的 Hook 从 Effect 中提取非响应式逻辑：

```js
import { useEffect, useEffectEvent } from 'react';

function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });
  // ...
```

这里的 `onConnected` 被称为 **Effect Event**。它是 Effect 逻辑的一部分，但是其行为更像事件处理函数。它内部的逻辑不是响应式的，而且能一直“看见”最新的 props 和 state。

现在你可以在 Effect 内部调用 `onConnected` Effect Event：

```js
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      onConnected();
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ 声明所有依赖项
  // ...
```

这个方法解决了问题。注意你必须从 Effect 依赖项中 **移除** `theme`，因为 Effect 中没有使用它。你也不需要 **添加** `onConnected`，因为 **Effect Event 是非响应式的并且必须从依赖项中删除**。****

### Effect Event 的局限性 [](https://zh-hans.react.dev/learn/separating-events-from-effects#limitations-of-effect-events "Link for Effect Event 的局限性")

Effect Event 的局限性在于你如何使用他们：

- **只在 Effect 内部调用他们**。
- **永远不要把他们传给其他的组件或者 Hook**，永远直接在使用他们的 Effect 旁边声明 Effect Event