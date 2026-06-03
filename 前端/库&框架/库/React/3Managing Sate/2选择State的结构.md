# 选择State的结构
## 构建 state 的原则 [](https://zh-hans.react.dev/learn/choosing-the-state-structure#principles-for-structuring-state "Link for 构建 state 的原则")

当你编写一个存有 state 的组件时，你需要选择使用多少个 state 变量以及它们都是怎样的数据格式。尽管选择次优的 state 结构下也可以编写正确的程序，但有几个原则可以指导你做出更好的决策：

1. **合并关联的 state**。如果你总是同时更新两个或更多的 state 变量，请考虑将它们合并为一个单独的 state 变量。
2. **避免互相矛盾的 state**。当 state 结构中存在多个相互矛盾或“不一致”的 state 时，你就可能为此会留下隐患。应尽量避免这种情况。
3. **避免冗余的 state**。如果你能在渲染期间从组件的 props 或其现有的 state 变量中计算出一些信息，则不应将这些信息放入该组件的 state 中。
4. **避免重复的 state**。当同一数据在多个 state 变量之间或在多个嵌套对象中重复时，这会很难保持它们同步。应尽可能减少重复。
5. **避免深度嵌套的 state**。深度分层的 state 更新起来不是很方便。如果可能的话，最好以扁平化方式构建 state。

这些原则背后的目标是 **使 state 易于更新而不引入错误**。从 state 中删除冗余和重复数据有助于确保所有部分保持同步。这类似于数据库工程师想要 [“规范化”数据库结构](https://docs.microsoft.com/zh-CN/office/troubleshoot/access/database-normalization-description)，以减少出现错误的机会。用爱因斯坦的话说，**“让你的状态尽可能简单，但不要过于简单。”**

## 合并关联的 state [](https://zh-hans.react.dev/learn/choosing-the-state-structure#group-related-state "Link for 合并关联的 state")

有时候你可能会不确定是使用单个 state 变量还是多个 state 变量。你会像下面这样做吗？

```
const [x, setX] = useState(0);const [y, setY] = useState(0);
```

或这样？

```
const [position, setPosition] = useState({ x: 0, y: 0 });
```

从技术上讲，你可以使用其中任何一种方法。但是，**如果某两个 state 变量总是一起变化，则将它们统一成一个 state 变量可能更好**。

## 不要在 state 中镜像 props [](https://zh-hans.react.dev/learn/choosing-the-state-structure#don-t-mirror-props-in-state "Link for 不要在 state 中镜像 props")

以下代码是体现 state 冗余的一个常见例子：

```
function Message({ messageColor }) {  const [color, setColor] = useState(messageColor);
```

这里，一个 `color` state 变量被初始化为 `messageColor` 的 prop 值。这段代码的问题在于，**如果父组件稍后传递不同的 `messageColor` 值（例如，将其从 `'blue'` 更改为 `'red'`），则 `color`** state 变量**将不会更新！** state 仅在第一次渲染期间初始化。

这就是为什么在 state 变量中，“镜像”一些 prop 属性会导致混淆的原因。相反，你要在代码中直接使用 `messageColor` 属性。如果你想给它起一个更短的名称，请使用常量：

```
function Message({ messageColor }) {  const color = messageColor;
```

这种写法就不会与从父组件传递的属性失去同步。

只有当你 **想要** 忽略特定 props 属性的所有更新时，将 props “镜像”到 state 才有意义。按照惯例，prop 名称以 `initial` 或 `default` 开头，以阐明该 prop 的新值将被忽略：

```
function Message({ initialColor }) {  // 这个 `color` state 变量用于保存 `initialColor` 的 **初始值**。  // 对于 `initialColor` 属性的进一步更改将被忽略。  const [color, setColor] = useState(initialColor);
```