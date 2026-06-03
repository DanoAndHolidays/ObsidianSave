# State的批量更新
**React 会等到事件处理函数中的** 所有 **代码都运行完毕再处理你的 state 更新。** 这就是重新渲染只会发生在所有这些 `setNumber()` 调用 **之后** 的原因。

这让你可以更新多个 state 变量——甚至来自多个组件的 state 变量——而不会触发太多的 [重新渲染](https://zh-hans.react.dev/learn/render-and-commit#re-renders-when-state-updates)。但这也意味着只有在你的事件处理函数及其中任何代码执行完成 **之后**，UI 才会更新。这种特性也就是 **批处理**，它会使你的 React 应用运行得更快。它还会帮你避免处理只​​更新了一部分 state 变量的令人困惑的“半成品”渲染。

## 在下次渲染前多次更新同一个 state [](https://zh-hans.react.dev/learn/queueing-a-series-of-state-updates#updating-the-same-state-multiple-times-before-the-next-render "Link for 在下次渲染前多次更新同一个 state")

这是一个不常见的用例，但是如果你想在下次渲染之前多次更新同一个 state，你可以像 `setNumber(n => n + 1)` 这样传入一个根据队列中的前一个 state 计算下一个 state 的 **函数**，而不是像 `setNumber(number + 1)` 这样传入 **下一个 state 值**。这是一种告诉 React “用 state 值做某事”而不是仅仅替换它的方法。

在这里，`n => n + 1` 被称为 **更新函数**。当你将它传递给一个 state 设置函数时：

1. React 会将此函数加入队列，以便在事件处理函数中的所有其他代码运行后进行处理。
2. 在下一次渲染期间，React 会遍历队列并给你更新之后的最终 state。

下面是 React 在执行事件处理函数时处理这几行代码的过程：

1. `setNumber(n => n + 1)`：`n => n + 1` 是一个函数。React 将它加入队列。
2. `setNumber(n => n + 1)`：`n => n + 1` 是一个函数。React 将它加入队列。
3. `setNumber(n => n + 1)`：`n => n + 1` 是一个函数。React 将它加入队列。

当你在下次渲染期间调用 `useState` 时，React 会遍历队列。之前的 `number` state 的值是 `0`，所以这就是 React 作为参数 `n` 传递给第一个更新函数的值。然后 React 会获取你上一个更新函数的返回值，并将其作为 `n` 传递给下一个更新函数，以此类推：

|更新队列|`n`|返回值|
|---|---|---|
|`n => n + 1`|`0`|`0 + 1 = 1`|
|`n => n + 1`|`1`|`1 + 1 = 2`|
|`n => n + 1`|`2`|`2 + 1 = 3`|

React 会保存 `3` 为最终结果并从 `useState` 中返回。这就是为什么在上面的示例中点击“+3”正确地将值增加“+3”。

### 在替换 state 后更新 state 与在更新 state 后替换 state

```js
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5);
        setNumber(n => n + 1);
      }}>增加数字</button>
    </>
  )
}
```

这是事件处理函数告诉 React 要做的事情：

1. `setNumber(number + 5)`：`number` 为 `0`，所以 `setNumber(0 + 5)`。React 将 _“替换为 `5`”_ 添加到其队列中。
2. `setNumber(n => n + 1)`：`n => n + 1` 是一个更新函数。 React 将 **该函数** 添加到其队列中。

>`setState(x)` 实际上会像 `setState(n => x)` 一样运行，只是没有使用 `n`！

```js
export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5);
        setNumber(n => n + 1);
        setNumber(42);
      }}>增加数字</button>
    </>
  )
}
```

以下是 React 在执行事件处理函数时处理这几行代码的过程：

1. `setNumber(number + 5)`：`number` 为 `0`，所以 `setNumber(0 + 5)`。React 将 _“替换为 `5`”_ 添加到其队列中。
2. `setNumber(n => n + 1)`：`n => n + 1` 是一个更新函数。React 将该函数添加到其队列中。
3. `setNumber(42)`：React 将 _“替换为 `42`”_ 添加到其队列中。

在下一次渲染期间，React 会遍历 state 队列：

|更新队列|`n`|返回值|
|---|---|---|
|“替换为 `5`”|`0`（未使用）|`5`|
|`n => n + 1`|`5`|`5 + 1 = 6`|
|“替换为 `42`”|`6`（未使用）|`42`|

然后 React 会保存 `42` 为最终结果并从 `useState` 中返回。

总而言之，以下是你可以考虑传递给 `setNumber` state 设置函数的内容：

- **一个更新函数**（例如：`n => n + 1`）会被添加到队列中。
- **任何其他的值**（例如：数字 `5`）会导致“替换为 `5`”被添加到队列中，已经在队列中的内容会被忽略。

事件处理函数执行完成后，React 将触发重新渲染。在重新渲染期间，React 将处理队列。更新函数会在渲染期间执行，因此 **更新函数必须是 [纯函数](https://zh-hans.react.dev/learn/keeping-components-pure)** 并且只 **返回** 结果。不要尝试从它们内部设置 state 或者执行其他副作用。在严格模式下，React 会执行每个更新函数两次（但是丢弃第二个结果）以便帮助你发现错误。

通常可以通过相应 state 变量的第一个字母或者更长的名字来命名更新函数的参数：

```js
setEnabled(e => !e);  
setLastName(ln => ln.reverse());  
setFriendCount(fc => fc * 2);

setEnabled(enabled => !enabled)
setEnabled(prevEnabled => !prevEnabled)
```

### 手动实现状态队列

```js
export function getFinalState(baseState, queue) {
  let finalState = baseState

  for (let update of queue){
    if(typeof update==='function'){
	  // 调用更新函数
      finalState=update(finalState)
    }else{
      // 直接替换值
      finalState=update
    }
  }
  return finalState;
}
```