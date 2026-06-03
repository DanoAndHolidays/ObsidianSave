# 使用Reducer与Context拓展应用

结合使用就能得到一个类似全局状态管理（Pinia）的效果

1. **创建** context。
2. 将 state 和 dispatch **放入** context。
3. 在组件树的任何地方 **使用** context。

像 `useTasks` 和 `useTasksDispatch` 这样的函数被称为 **[自定义 Hook](https://zh-hans.react.dev/learn/reusing-logic-with-custom-hooks)。** 如果你的函数名以 `use` 开头，它就被认为是一个自定义 Hook。这让你可以使用其他 Hook，比如 `useContext`。