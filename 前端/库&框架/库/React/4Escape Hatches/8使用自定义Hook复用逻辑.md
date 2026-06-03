# 使用自定义Hook复用逻辑

看的比较快，闲的时候再看一遍
[使用自定义 Hook 复用逻辑 – React 中文文档](https://zh-hans.react.dev/learn/reusing-logic-with-custom-hooks)

### Hook 的名称必须永远以 `use` 开头 [](https://zh-hans.react.dev/learn/reusing-logic-with-custom-hooks#hook-names-always-start-with-use "Link for this heading")

React 应用是由组件构成，而组件由内置或自定义 Hook 构成。可能你经常使用别人写的自定义 Hook，但偶尔也要自己写！

你必须遵循以下这些命名公约：

1. **React 组件名称必须以大写字母开头**，比如 `StatusBar` 和 `SaveButton`。React 组件还需要返回一些 React 能够显示的内容，比如一段 JSX。
2. **Hook 的名称必须以 `use` 开头，然后紧跟一个大写字母**，就像内置的 [`useState`](https://zh-hans.react.dev/reference/react/useState) 或者本文早前的自定义 `useOnlineStatus` 一样。Hook 可以返回任意值。
3. 组件和自定义 Hook 都 [需要是纯函数](https://zh-hans.react.dev/learn/keeping-components-pure)

如果你为 [React 配置了](https://zh-hans.react.dev/learn/editor-setup#linting) 代码检查工具，它会强制执行这个命名公约。现在滑动到上面的 sandbox，并将 `useOnlineStatus` 重命名为 `getOnlineStatus`。注意此时代码检查工具将不会再允许你在其内部调用 `useState` 或者 `useEffect`。只有 Hook 和组件可以调用其他 Hook！

#### 渲染期间调用的所有函数都应该以 use 前缀开头么？ [](https://zh-hans.react.dev/learn/reusing-logic-with-custom-hooks#should-all-functions-called-during-rendering-start-with-the-use-prefix "Link for 渲染期间调用的所有函数都应该以 use 前缀开头么？")

不。没有 **调用** Hook 的函数不需要 **变成** Hook。

如果你创建的函数没有调用任何 Hook 方法，在命名时应避免使用 `use` 前缀，把它当成一个常规函数去命名。