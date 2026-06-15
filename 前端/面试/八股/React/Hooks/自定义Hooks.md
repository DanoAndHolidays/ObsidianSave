# 自定义Hooks
> Last Format Time：6/15/2026 10:50:12

[https://www.robinwieruch.de/react-custom-hook/](https://www.robinwieruch.de/react-custom-hook/)

在 React 中实现自定义 Hooks，必须严格遵守官方制定的核心规则。这些规则不仅是代码规范，更是保证 React 内部状态管理机制正常运作的基础。具体需要遵守以下三大核心规则：

---
## 命名必须以 `use` 开头

自定义 Hook 的名称必须始终以 `use` 作为前缀，并紧跟一个大写字母（例如 `useAuth`、`useWindowSize`）。

- **原因**：这一命名公约能让 React 和代码检查工具（如 ESLint）一眼识别出该函数内部可能包含状态（State）或副作用（Effect），从而自动强制执行 Hooks 的相关规则。
- **注意**：如果函数内部没有调用任何 Hook，就不应该使用 `use` 前缀，应将其视为常规函数（如 `getSorted`），以便可以在条件语句等任意位置安全调用。

---
## 只能在顶层调用（禁止在循环、条件或嵌套函数中调用）

所有的 Hooks 必须始终在函数组件或自定义 Hook 的最顶层调用，绝不能在以下位置使用：

- 条件判断语句（`if` / `else`）
- 循环语句（`for` / `while` / `map`）
- 嵌套函数或事件处理函数（如 `handleClick`）
- `try` / `catch` / `finally` 代码块
- 条件性的 `return` 语句之后
- **原因**：React 依赖于每次渲染时 Hooks 的调用顺序完全一致来正确保存和追踪状态。如果在条件或循环中调用，可能导致某次渲染时 Hooks 数量或顺序发生变化，React 将无法知道哪个状态对应哪个 Hook，从而引发错误。

---
## 只能在 React 函数组件或自定义 Hook 中调用

Hooks 只能在以下两种环境中调用：

- React 的函数组件内部
- 其他自定义 Hook 内部（自定义 Hook 内部可以继续调用其他 Hooks，这也是自定义 Hook 的主要目的）
- **禁止**：绝不能在普通的 JavaScript 函数、类组件（Class Components）或非 React 函数生态系统中调用 Hooks。