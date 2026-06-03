# State
React普通的变量的变化是不会导致使用这个数据的视图也发生变化的：
```js
import { sculptureList } from './data.js';

export default function Gallery() {
  // 这里的index变化不会导致组件UI的变化，就算变化了也会因为重新渲而失去状态，重新变为0
  let index = 0;

  function handleClick() {
    index = index + 1;
  }

  let sculpture = sculptureList[index];
  return (
    <>
      <button onClick={handleClick}>
        Next
      </button>
      <h2>
        <i>{sculpture.name} </i> 
        by {sculpture.artist}
      </h2>
      <h3>  
        ({index + 1} of {sculptureList.length})
      </h3>
      <img 
        src={sculpture.url} 
        alt={sculpture.alt}
      />
      <p>
        {sculpture.description}
      </p>
    </>
  );
}
```

`handleClick()` 事件处理函数正在更新局部变量 `index`。但存在两个原因使得变化不可见：
1. **局部变量无法在多次渲染中持久保存。** 当 React 再次渲染这个组件时，它会从头开始渲染——不会考虑之前对局部变量的任何更改。
2. **更改局部变量不会触发渲染。** React 没有意识到它需要使用新数据再次渲染组件。

要使用新数据更新组件，需要做两件事：
1. **保留** 渲染之间的数据。
2. **触发** React 使用新数据渲染组件（重新渲染）。

[`useState`](https://zh-hans.react.dev/reference/react/useState) Hook 提供了这两个功能：
1. **State 变量** 用于保存渲染间的数据。
2. **State setter 函数** 更新变量并触发 React 再次渲染组件。

## 添加一个 state 变量 
要添加 state 变量，先从文件顶部的 React 中导入 `useState`：
```
import { useState } from 'react';
```

然后，替换这一行：
```
let index = 0;
```

将其修改为
```
const [index, setIndex] = useState(0);
```

`index` 是一个 state 变量，`setIndex` 是对应的 setter 函数。

> 这里的 `[` 和 `]` 语法称为[数组解构](https://zh.javascript.info/destructuring-assignment)，它允许你从数组中读取值。 `useState` 返回的数组总是正好有两项。

以下展示了它们在 `handleClick()` 中是如何共同起作用的：
```
function handleClick() {  setIndex(index + 1);}
```

`useState` 的唯一参数是 state 变量的**初始值**。在这个例子中，`index` 的初始值被`useState(0)`设置为 `0`。

每次你的组件渲染时，`useState` 都会给你一个包含两个值的数组：
1. **state 变量** (`index`) 会保存上次渲染的值。
2. **state setter 函数** (`setIndex`) 可以更新 state 变量并触发 React 重新渲染组件。

这里的index与setIndex可以理解为Vue中的ref对象的拆分，Vue中不需要手动去调用setter，直接修改ref对象的value值皆可以

同样的与Vue一样，每个组件中的State是独立的，不会因为你声明了多个组件而共享State（这种数据共享的方式，应该使用集中的转态管理）
### 遇见你的第一个 Hook 
在 React 中，`useState` 以及任何其他以“`use`”开头的函数都被称为 **Hook**。

Hook 是特殊的函数，只在 React [渲染](https://zh-hans.react.dev/learn/render-and-commit#step-1-trigger-a-render)时有效（我们将在下一节详细介绍）。它们能让你 “hook” 到不同的 React 特性中去。

State 只是这些特性中的一个，你之后还会遇到其他 Hook。

**Hooks ——以 `use` 开头的函数——只能在组件或[自定义 Hook](https://zh-hans.react.dev/learn/reusing-logic-with-custom-hooks) 的最顶层调用。** 你不能在条件语句、循环语句或其他嵌套函数内调用 Hook。Hook 是函数，但将它们视为关于组件需求的无条件声明会很有帮助。在组件顶部 “use” React 特性，类似于在文件顶部“导入”模块。

你可能已经注意到，`useState` 在调用时没有任何关于它引用的是_哪个_ state 变量的信息。没有传递给 `useState` 的“标识符”，它是如何知道要返回哪个 state 变量呢？它是否依赖于解析函数之类的魔法？答案是否定的。

相反，为了使语法更简洁，**在同一组件的每次渲染中，Hooks 都依托于一个稳定的调用顺序**。这在实践中很有效，因为如果你遵循上面的规则（“只在顶层调用 Hooks”），Hooks 将始终以相同的顺序被调用。此外，[linter 插件](https://www.npmjs.com/package/eslint-plugin-react-hooks)也可以捕获大多数错误。

在 React 内部，为每个组件保存了一个数组，其中每一项都是一个 state 对。它维护当前 state 对的索引值，在渲染之前将其设置为 “0”。每次调用 useState 时，React 都会为你提供一个 state 对并增加索引值。你可以在文章 [React Hooks: not magic, just arrays](https://medium.com/@ryardley/react-hooks-not-magic-just-arrays-cd4f1857236e)中阅读有关此机制的更多信息。

