# 移除Effect

## 如何移除不必要的 Effect [](https://zh-hans.react.dev/learn/you-might-not-need-an-effect#how-to-remove-unnecessary-effects "Link for 如何移除不必要的 Effect")

有两种不必使用 Effect 的常见情况：

- **你不必使用 Effect 来转换渲染所需的数据**。例如，你想在展示一个列表前先做筛选。你的直觉可能是写一个当列表变化时更新 state 变量的 Effect。然而，这是低效的。当你更新这个 state 时，React 首先会调用你的组件函数来计算应该显示在屏幕上的内容。然后 React 会把这些变化“[提交](https://zh-hans.react.dev/learn/render-and-commit)”到 DOM 中来更新屏幕。然后 React 会执行你的 Effect。如果你的 Effect 也立即更新了这个 state，就会重新执行整个流程。为了避免不必要的渲染流程，应在你的组件顶层转换数据。这些代码会在你的 props 或 state 变化时自动重新执行。
- **你不必使用 Effect 来处理用户事件**。例如，你想在用户购买一个产品时发送一个 `/api/buy` 的 POST 请求并展示一个提示。在这个购买按钮的点击事件处理函数中，你确切地知道会发生什么。但是当一个 Effect 运行时，你却不知道用户做了什么（例如，点击了哪个按钮）。这就是为什么你通常应该在相应的事件处理函数中处理用户事件。

### 根据 props 或 state 来更新 state [](https://zh-hans.react.dev/learn/you-might-not-need-an-effect#updating-state-based-on-props-or-state "Link for 根据 props 或 state 来更新 state")

假设你有一个包含了两个 state 变量的组件：`firstName` 和 `lastName`。你想通过把它们联结起来计算出 `fullName`。此外，每当 `firstName` 和 `lastName` 变化时，你希望 `fullName` 都能更新。你的第一直觉可能是添加一个 state 变量：`fullName`，并在一个 Effect 中更新它：

```js
function Form() {
  const [firstName, setFirstName] = useState('Taylor');
  const [lastName, setLastName] = useState('Swift');

  // 🔴 避免：多余的 state 和不必要的 Effect
  const [fullName, setFullName] = useState('');
  useEffect(() => {
    setFullName(firstName + ' ' + lastName);
  }, [firstName, lastName]);
  // ...
}
```

大可不必这么复杂。而且这样效率也不高：它先是用 `fullName` 的旧值执行了整个渲染流程，然后立即使用更新后的值又重新渲染了一遍。让我们移除 state 变量和 Effect：

```js
function Form() {
  const [firstName, setFirstName] = useState('Taylor');
  const [lastName, setLastName] = useState('Swift');
  // ✅ 非常好：在渲染期间进行计算
  const fullName = firstName + ' ' + lastName;
  // ...
}
```

**如果一个值可以基于现有的 props 或 state 计算得出，[不要把它作为一个 state](https://zh-hans.react.dev/learn/choosing-the-state-structure#avoid-redundant-state)，而是在渲染期间直接计算这个值**。这将使你的代码更快（避免了多余的 “级联” 更新）、更简洁（移除了一些代码）以及更少出错（避免了一些因为不同的 state 变量之间没有正确同步而导致的问题）。

### 缓存昂贵的计算

你可以使用 [`useMemo`](https://zh-hans.react.dev/reference/react/useMemo) Hook 缓存（或者说 [记忆（memoize）](https://en.wikipedia.org/wiki/Memoization)）一个昂贵的计算。

### 注意

[React 编译器](https://zh-hans.react.dev/learn/react-compiler) 可以自动记忆化昂贵计算，从而减少很多手动调用 `useMemo` 的场景。
你传入 [`useMemo`](https://zh-hans.react.dev/reference/react/useMemo) 的函数会在渲染期间执行，所以它仅适用于 [纯函数](https://zh-hans.react.dev/learn/keeping-components-pure) 场景。

```js
import { useMemo, useState } from 'react';

function TodoList({ todos, filter }) {
  const [newTodo, setNewTodo] = useState('');
  const visibleTodos = useMemo(() => {
    // ✅ 除非 todos 或 filter 发生变化，否则不会重新执行
    return getFilteredTodos(todos, filter);
  }, [todos, filter]);
  // ...
}
```

这部分有非常多的例子，我先不看了，等明天再说