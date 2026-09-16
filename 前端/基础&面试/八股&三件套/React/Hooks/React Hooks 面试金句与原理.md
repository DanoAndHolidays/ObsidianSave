# React Hooks 面试金句与原理
> Last Format Time：6/15/2026 10:50:12

---
## 📝 题目 1：useEffect vs useLayoutEffect
### 核心结论
两者最大的区别在于**执行时机**和**是否阻塞浏览器绘制**。
- `useEffect`：**异步执行**，在浏览器完成页面绘制（Paint）**之后**运行，不阻塞渲染。
- `useLayoutEffect`：**同步执行**，在 DOM 更新后、浏览器绘制（Paint）**之前**运行，会阻塞渲染。

### 底层原理
React 的更新流程大致是：`Render` -> `Commit (DOM更新)` -> `useLayoutEffect` -> `浏览器绘制` -> `useEffect`。
因为 `useLayoutEffect` 在绘制前同步执行，所以如果你在里面做耗时操作（如大循环、复杂计算），会导致页面卡顿甚至白屏。

### 实战场景
- **99% 的场景用 `useEffect`**：数据请求、事件订阅、定时器、日志埋点等。
- **极少数场景用 `useLayoutEffect`**：
    1. **防止页面闪烁**：比如需要在渲染前同步修改 DOM 样式（如 Tooltip 定位、弹窗位置计算），如果用 `useEffect` 用户会看到元素先出现在原位再"瞬移"到目标位置。
    2. **同步测量 DOM**：需要在 DOM 更新后立即读取尺寸（如 `offsetWidth`）并基于此修改 DOM，必须用 `useLayoutEffect` 保证在浏览器绘制前完成这一套"测量+修改"的同步操作。

### 💡 面试金句

> "默认优先用 `useEffect`，只有当遇到 DOM 测量或样式修改导致的视觉闪烁问题时，才考虑替换为 `useLayoutEffect`，但要警惕它阻塞渲染的风险。"

---
## 📝 题目 2：useState vs useReducer
### 核心结论
`useReducer` 不是为了替代 `useState`，而是为了解决**复杂状态逻辑**和**状态流转可预测性**的问题。

### 什么时候放弃 useState 选 useReducer？
1. **状态逻辑复杂**：当一个状态的变化依赖多个条件分支（如表单验证、多步骤流程、状态机），用 `useState` 会导致 `setState` 散落在各处，难以追踪；`useReducer` 将所有变更逻辑集中在 `reducer` 函数中，一目了然。
2. **多个状态强关联**：比如一个对象包含 `loading`, `data`, `error`，这三个状态往往联动变化。用 `useReducer` 可以在一个 `dispatch` 中同时更新多个字段，避免多次 `setState` 导致的多次渲染或闭包陷阱。
3. **需要可预测性/调试**：`useReducer` 的 `dispatch` 是纯函数，状态变更路径清晰，非常适合配合 Redux DevTools 做时间旅行调试。
4. **跨层级传递更新逻辑**：结合 `useContext`，只把 `dispatch` 传给深层子组件，子组件无需知道状态结构，只需 `dispatch({ type: 'INCREMENT' })`，避免了 `useState` 需要传递具体 `setter` 函数的繁琐。

### 💡 面试金句

> "简单状态（如 boolean 开关、计数器）用 `useState`；一旦状态更新涉及复杂分支、多字段联动，或者我需要把更新逻辑从组件中解耦出来做单元测试，我会果断切到 `useReducer`。"

---
## 📝 题目 3：useMemo vs useCallback & 滥用问题
### 核心区别
- `useMemo`：缓存**计算结果**（值）。例如：`const sortedList = useMemo(() => list.sort(), [list])`。
- `useCallback`：缓存**函数引用**。例如：`const handleClick = useCallback(() => {}, [id])`。
- **本质联系**：`useCallback(fn, deps)` 等价于 `useMemo(() => fn, deps)`。

### 是不是越多越好？绝对不是！
1. **内存开销**：每个 Hook 都需要在 Fiber 节点上开辟内存存储缓存值和依赖数组。对于简单计算（如 `a + b`），缓存本身的比对成本可能比重新计算还高。
2. **代码可读性**：过度包裹会让代码变得臃肿，增加维护心智负担。
3. **无效优化**：如果子组件没有用 `React.memo`，或者父组件没有因为重渲染导致子组件 props 变化，那么 `useCallback` 缓存函数引用毫无意义，因为子组件本来就会跟着父组件一起渲染。

### 💡 面试金句

> "性能优化是有成本的。我只在**计算昂贵**（如大数据过滤/排序）或**引用稳定性影响子组件渲染**（配合 `React.memo`）这两个场景下使用它们。对于简单的 UI 状态，我相信 React 自身的优化能力，不手动干预。"

---
## 📝 题目 4：为什么 Hooks 不能写在条件/循环里？（底层原理）
### 核心结论
这是由 React 的**底层数据结构（链表）**和**调用顺序匹配机制**决定的。

### 底层原理拆解
1. **链表存储**：React 为每个组件的 Fiber 节点维护一个 **Hook 单向链表**。每个 Hook 调用对应链表中的一个节点，节点里存着 `memoizedState`（状态）、`queue`（更新队列）和 `next`（下一个 Hook）。
2. **顺序遍历**：
    - **首次渲染**：React 按代码执行顺序，依次创建节点并挂到链表上（Hook1 -> Hook2 -> Hook3）。
    - **重渲染**：React 重置指针到链表头，**严格按照代码执行顺序**依次遍历链表，把新状态赋给对应节点。
3. **错位灾难**：
    如果你把 Hook 写在 `if` 里：

    ```javascript
    if (flag) { useState(1); } // Hook A
    useState(2);               // Hook B
    ```

    - 当 `flag=true`：链表是 `A -> B`。
    - 当 `flag=false`：Hook A 被跳过，代码直接执行 Hook B。但 React 的指针还在链表头，它会以为当前的 Hook B 是链表里的第一个节点（原本 A 的位置），导致**状态读取错位**，甚至链表遍历到 `null` 报错。

### 💡 面试金句

> "Hooks 的规则不是风格建议，而是底层实现的必然约束。React 用**链表 + 索引顺序**来管理状态，一旦条件或循环改变了调用顺序，链表映射就会错位，导致状态错乱。这也是为什么 ESLint 的 `react-hooks/rules-of-hooks` 规则如此重要。"

---
## 🚀 给你的备考建议
1. **不要死记硬背**：面试官听到"背诵感"会很反感。试着用**"我遇到过一个问题..."**来引出这些知识点。
    - _例如_："我之前做列表页时，发现滚动时页面会闪烁，排查后发现是 `useEffect` 异步修改 DOM 导致的，后来换成 `useLayoutEffect` 同步处理就解决了..."
2. **串联知识点**：把 **题目 4（原理）** 和 **题目 3（优化）** 结合起来。
    - _例如_："正因为 Hooks 是按顺序存在链表里的，所以 `useMemo` 和 `useCallback` 的依赖数组比对也是基于位置的，如果顺序乱了，缓存也会失效。"
3. **准备一个"坑"**：面试官很喜欢问"你踩过什么坑？"。你可以把最开始问我的**闭包陷阱**（`useEffect` + `setInterval` + 旧闭包）讲出来，然后说出你的三种解法（依赖数组、`useRef`、函数式更新），这比背八股文加分太多！