# 响应式Effect的生命周期

这部分有点难，我应该再看一遍

## Effect 的生命周期 [](https://zh-hans.react.dev/learn/lifecycle-of-reactive-effects#the-lifecycle-of-an-effect "Link for Effect 的生命周期")

每个 React 组件都经历相同的生命周期：

- 当组件被添加到屏幕上时，它会进行组件的 **挂载**。
- 当组件接收到新的 props 或 state 时，通常是作为对交互的响应，它会进行组件的 **更新**。
- 当组件从屏幕上移除时，它会进行组件的 **卸载**。

**代码中的每个 Effect 应该代表一个独立的同步过程。**

在上面的示例中，删除一个 Effect 不会影响另一个 Effect 的逻辑。这表明它们同步不同的内容，因此将它们拆分开是有意义的。另一方面，如果将一个内聚的逻辑拆分成多个独立的 Effects，代码可能会看起来更加“清晰”，但 [维护起来会更加困难](https://zh-hans.react.dev/learn/you-might-not-need-an-effect#chains-of-computations)。这就是为什么你应该考虑这些过程是相同还是独立的，而不是只考虑代码是否看起来更整洁。

#### 全局变量或可变值可以作为依赖项吗？ [](https://zh-hans.react.dev/learn/lifecycle-of-reactive-effects#can-global-or-mutable-values-be-dependencies "Link for 全局变量或可变值可以作为依赖项吗？")

可变值（包括全局变量）不是响应式的。

例如，像 [`location.pathname`](https://developer.mozilla.org/zh-CN/docs/Web/API/Location/pathname) 这样的可变值不能作为依赖项。它是可变的，因此可以在 React 渲染数据流之外的任何时间发生变化。更改它不会触发组件的重新渲染。因此，即使在依赖项中指定了它，React 也无法知道在其更改时重新同步 Effect。这也违反了 React 的规则，因为在渲染过程中读取可变数据（即在计算依赖项时）会破坏 [纯粹的渲染](https://zh-hans.react.dev/learn/keeping-components-pure)。相反，应该使用 [`useSyncExternalStore`](https://zh-hans.react.dev/learn/you-might-not-need-an-effect#subscribing-to-an-external-store) 来读取和订阅外部可变值。

**另外，像 [`ref.current`](https://zh-hans.react.dev/reference/react/useRef#reference) 或从中读取的值也不能作为依赖项。`useRef` 返回的 ref 对象本身可以作为依赖项**，但其 `current` 属性是有意可变的。它允许 [跟踪某些值而不触发重新渲染](https://zh-hans.react.dev/learn/referencing-values-with-refs)。但由于更改它不会触发重新渲染，它不是响应式值，React 不会知道在其更改时重新运行 Effect。