# React
> Last Format Time：7/30/2026 10:45:21

这是一份面向前端面试的 React 知识树，按“核心概念 → Hooks → 渲染原理 → 性能 → 服务端 → 工程实践 → 手写题”组织。回答时建议先给结论，再解释原理，最后补充适用场景与边界。

参考资料：
- [React 官方文档](https://react.dev/)
- [React 19 发布说明](https://react.dev/blog/2024/12/05/react-19)
- [React 19.2 发布说明](https://react.dev/blog/2025/10/01/react-19-2)
- [React Compiler](https://react.dev/learn/react-compiler)

---
## 复习路线
建议按面试频率分三轮复习：
- 第一轮：组件、props/state、key、受控组件、Hooks、Effect、状态更新与批处理
- 第二轮：Reconciliation、Fiber、Render/Commit、并发渲染、性能优化、状态管理
- 第三轮：SSR/RSC、Suspense、React 19、组件库设计、测试和手写 Hooks

高频追问通常不是“API 怎么用”，而是：为什么这样设计、什么时候会失效、错误方案会造成什么后果、如何用 Profiler 或最小示例证明判断。

---
## 核心概念与组件模型
### React 的核心思想是什么
React 用组件描述 UI，并把界面视为状态的函数：`UI = f(state)`。开发者声明“某个状态下 UI 应该是什么”，React 负责协调前后两次结果并提交必要的宿主环境变更。核心特征包括**组件化**、**单向数据流**、**声明式渲染**和**跨平台 Renderer**。

### JSX 是什么，最终会变成什么
JSX 是 JavaScript 的==语法扩展==，不是模板字符串，也不能被浏览器直接执行。现代 JSX Transform 会把它编译成 `jsx/jsxs` 调用；旧转换则编译成 `React.createElement` 调用，最终得到 ==React Element 描述对象==。

### React Element、Component 与 Fiber 有什么区别
- React Element：一次渲染产生的不可变描述对象，描述元素类型、props、key 等
- Component：生成 UI 描述的函数或类
- Fiber：React 运行时内部的工作单元，保存组件状态、更新队列、树关系、优先级和副作用标记（后面有更详细的）

### createElement 与 cloneElement 有什么区别
- `createElement(type, props, ...children)`：根据类型和 props 创建新 React Element
- `cloneElement(element, props, ...children)`：以现有 Element 为基础浅合并 props，并可替换 children

`cloneElement` 会让数据来源变得隐蔽，现代代码通常优先使用显式 props、Context 或组合模式。

### 函数组件与类组件有什么区别
函数组件是现代 React 的主流写法，通过 Hooks 使用状态、副作用和 Context；类组件通过实例、生命周期和 `this.setState` 管理逻辑。函数组件更利于逻辑复用和组合，但 Error Boundary 目前仍通常使用类组件实现。

### props 和 state 有什么区别
- props：由父组件传入，组件不应直接修改
- state：组件对某次渲染的内部状态快照，通过更新函数请求下一次渲染
- 二者变化都可能触发重新渲染，但重新渲染不等于一定修改 DOM

### 为什么 React 强调单向数据流
数据从父组件流向子组件，子组件通过回调表达事件。这样能明确状态所有权，使变化路径更容易追踪、测试和调试。兄弟组件共享状态时，优先把状态提升到最近的公共父组件。

### 什么是组合，为什么通常优于继承
组合通过 `children`、具名插槽式 props 或自定义 Hook 拼装能力，耦合更低。React 很少需要组件继承；继承适合真正的类型层次，而 UI 复用通常是行为与结构的组合。

### React 中如何进行条件渲染
常见方式包括提前 `return`、三元表达式和 `&&`。注意 `0 && <View />` 会渲染出 `0`，需要显式转换为布尔值；也不要在条件分支中调用 Hooks。

### Fragment 有什么作用
Fragment 可以在不增加额外 DOM 节点的情况下返回多个兄弟元素。短语法 `<>...</>` 不能传 `key`；列表中需要 `key` 时应使用 `<Fragment key={id}>`。

### Portal 有什么作用，事件如何冒泡
Portal 把 DOM 渲染到另一个容器，但子节点在 React 组件树中的位置不变。因此 Context 和 React 事件冒泡仍按 React 树工作，而不是按 DOM 树工作。常用于 Modal、Tooltip、Dropdown 和 Toast。

```jsx
import { createPortal } from 'react-dom';

function Modal({ children }) {
  return createPortal(children, document.body);
}
```

### Error Boundary 能捕获哪些错误
Error Boundary 能捕获后代组件在渲染、构造和生命周期中的错误并展示降级 UI；不能捕获事件处理器、普通异步回调、SSR 阶段以及边界自身抛出的错误。事件和请求错误应在对应流程中显式处理。

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    reportError(error, info);
  }

  render() {
    return this.state.hasError ? <Fallback /> : this.props.children;
  }
}
```

---
## 状态、数据流与表单
### 为什么说 state 是一次渲染的快照
每次渲染都会获得当次固定的 props、state 和事件处理函数。调用更新函数不会修改当前闭包里的 state，只会请求下一次渲染。这解释了连续执行 `setCount(count + 1)` 为什么可能只增加一次。

### 连续更新依赖旧状态时为什么要用函数式更新
值形式捕获的是当前渲染的快照；函数式更新会按队列依次接收前一个计算结果：
```jsx
setCount(count + 1);
setCount(count + 1); // 两次都基于同一个 count

setCount(value => value + 1);
setCount(value => value + 1); // 在前一次结果上继续计算
```

### setState 是同步还是异步
更准确的说法是：状态更新是被 React 排队和调度的，而不是把 `setState` 简单归类为 Promise 式“异步”。React 18 使用 `createRoot` 后，React 事件、Promise、定时器和原生事件中的多次更新通常都会自动批处理。确需立即同步提交 DOM 时可用 `flushSync`，但应少用。

### React 如何决定保留还是重置组件状态
状态与组件在渲染树中的位置绑定。相同位置且元素类型与 `key` 相同通常会保留状态；类型或 `key` 改变会创建新的组件身份并重置状态。不要在组件函数内部定义组件，否则每次渲染都会得到新的组件类型。

### key 的作用是什么
`key` 用于标识同一父节点下兄弟元素的身份，帮助 React 匹配新增、删除、移动和复用。它不是全局唯一，也不会作为普通 prop 传入组件。稳定的==业务 ID ==通常是最佳 key。

### 为什么不建议使用数组下标作为 key
当列表插入、删除或排序时，下标会对应到不同业务项，可能造成组件本地状态、输入内容和动画==错位==。只有列表静态、不会重排且没有稳定 ID 时才可谨慎使用下标。

### 受控组件与非受控组件有什么区别
- 受控组件：表单值来自 React state，通过 `value/checked` 与 `onChange` 同步，便于校验和联动
- 非受控组件：值由 DOM 保存，通过 `defaultValue` 和 ref 读取，接入简单、更新开销较低

同一个输入框生命周期内不要在受控与非受控之间切换。

### 状态提升、Context 与全局 Store 如何选择
- 只被一个组件使用：本地 state
- 少量相邻组件共享：状态提升或组合
- 跨层级且变化不频繁：Context
- 跨页面、更新频繁、需要中间件或调试能力：Redux、Zustand 等外部 Store
- 服务端数据：优先交给路由框架或 TanStack Query、SWR 等缓存层，不必都塞进全局 Store

### 不可变更新为什么重要
React 和许多状态库会使用==引用相等性==快速判断数据是否变化。不可变更新能保留未修改分支的引用并为修改分支创建新引用，使浅比较、时间旅行和并发渲染更可靠。它不是要求深拷贝整个对象。

### Immer 的原理是什么
Immer 使用 Proxy 记录对 draft 的读写，并在完成时进行写时复制。只有被修改的路径会生成新对象，未修改部分继续结构共享，因此写法看似可变，结果仍是不可变数据。

---
## Hooks
### Hooks 带来了什么
Hooks 让函数组件可以使用状态、Context、ref 和副作用，并把相关逻辑聚合到自定义 Hook 中，减少类组件的 `this`、生命周期拆散和 HOC/render props 嵌套。

### Hooks 的两条核心规则是什么
- 只在 React 函数组件或自定义 Hook 中调用 Hook
- 在组件顶层调用，不放在条件、循环、事件处理函数或普通函数中

React 依赖稳定的调用顺序，把每次 Hook 调用与 Fiber 上对应的 Hook 状态关联起来。

### Hooks 的底层数据结构是什么
函数组件 Fiber 的 `memoizedState` 会关联一组 Hook 节点。渲染时 React 按调用顺序读取或创建这些节点；状态 Hook 还维护更新队列。理解到“调用顺序必须稳定”即可，具体字段属于内部实现，不能作为业务代码契约。

### useState 与 useReducer 如何选择
`useState` 适合独立、简单的状态；`useReducer` 适合多个字段由同一事件共同变化、状态转移复杂或希望把更新规则集中测试的场景。二者都不能替代跨组件共享机制。

### useRef 有哪些用途
- 获取 DOM 节点或命令式实例
- 保存定时器 ID、上一次值等跨渲染可变数据
- 保存最新回调或第三方实例

修改 `ref.current` 不会触发渲染，因此参与 UI 展示的数据应放在 state 中，也不应在渲染期间随意读写 ref。

### useMemo 与 useCallback 有什么区别
- `useMemo` 缓存计算结果
- `useCallback` 缓存函数引用，近似 `useMemo(() => fn, deps)`

它们是性能优化手段而不是语义保证。只有昂贵计算、稳定引用确实能避免下游工作，或依赖项需要稳定时才使用；滥用会增加比较和维护成本。

### React.memo 如何工作
`React.memo` 默认用 `Object.is` 逐个浅比较新旧 props。props 相同则可跳过该组件的渲染，但组件==自身 state 或消费的 Context 变化==仍会更新。自定义比较函数必须比较所有影响输出的 props，包括函数闭包。

### 什么是闭包捕获值或 stale closure
事件处理函数和 Effect 捕获创建它们那次渲染的值。如果依赖数组缺项、异步回调长时间保存旧函数，就可能读到旧状态。常见解法是补全依赖、使用函数式更新、重新设计数据流，或在确实需要“最新值但不触发 Effect”时使用 Effect Event 等模式。

### 自定义 Hook 的本质是什么
自定义 Hook 是以 `use` 开头、内部组合其他 Hooks 的普通函数。它复用的是有状态逻辑，不共享同一份状态；每个调用方都有独立的 Hook 状态。

### useContext 的更新特点是什么
组件调用 `useContext` 后会订阅最近 Provider 的值。Provider 的 `value` 与上次相比发生变化时，消费者会重新渲染，`React.memo` 不能屏蔽其读取到的 Context 更新。高频场景可拆分 Context、稳定 value 或改用支持 selector 的外部 Store。

### useId 解决什么问题
`useId` 生成适合无障碍属性关联且能在服务端与客户端匹配的 ID。它不应作为列表 key；key 应来自业务数据。

### useImperativeHandle 有什么作用
[[useImperativeHandle]]
它允许组件自定义通过 ref 暴露的命令式能力，例如只暴露 `focus()` 和 `reset()`，避免把整个 DOM 节点泄漏给父组件。React 19 中函数组件可以直接把 `ref` 作为 prop 接收；旧版本通常配合 `forwardRef`。

### useSyncExternalStore 解决什么问题
它为外部 Store 提供一致的订阅协议，通过 `subscribe`、`getSnapshot` 和可选的 `getServerSnapshot` 读取快照，避免并发渲染中的 tearing，并支持 SSR hydration 一致性。状态库应优先基于它接入 React。

### useInsertionEffect 适合什么场景
它主要供 CSS-in-JS 库在布局 Effect 读取样式前注入样式使用，不是普通业务副作用的替代品。业务代码通常使用 `useEffect` 或 `useLayoutEffect`。

### 如何用 Hook 模拟 componentDidMount
`useEffect(fn, [])` 表示 Effect 不依赖响应式值，通常可表达挂载后的同步逻辑，但它不等价于“生命周期模拟器”。开发环境 Strict Mode 会额外执行一次 setup → cleanup → setup，用来暴露清理不完整的问题。

---
## Effect、事件与 Ref
### 什么是副作用
副作用是渲染计算之外与外部系统的同步，例如网络请求、订阅、定时器、日志、浏览器 API、手动 DOM 操作和第三方组件实例。纯数据派生通常不需要 Effect。

### useEffect 的执行与清理时机是什么
Effect 在提交后运行。依赖变化时，React 会先用旧 props/state 执行上一次 cleanup，再用新值执行 setup；卸载时执行 cleanup。Effect 具体是否严格发生在一次浏览器绘制之后不能作为业务契约，视觉测量应使用 `useLayoutEffect`。

### useEffect 为什么不能直接传 async 函数
Effect 回调只能返回 `undefined` 或清理函数，而 `async` 函数总会返回 Promise。应在 Effect 内定义并调用异步函数，同时处理取消、竞态和错误。

```jsx
useEffect(() => {
  const controller = new AbortController();

  async function load() {
    try {
      const response = await fetch(url, { signal: controller.signal });
      const result = await response.json();
      setData(result);
    } catch (error) {
      if (error.name !== 'AbortError') setError(error);
    }
  }

  load();
  return () => controller.abort();
}, [url]);
```

### 依赖数组应该如何填写
Effect 中读取的每个响应式值都应作为依赖，包括 props、state 和组件内声明的函数或变量。不要靠删依赖“控制执行次数”；应通过移出非响应式逻辑、函数式更新、拆分 Effect 或稳定必要引用来解决重复执行。

### 哪些逻辑不应该放进 useEffect
- 根据 props/state 计算派生值：直接在渲染时计算，昂贵时再用 `useMemo`
- 用户点击引起的动作：放进事件处理函数
- 重置子树状态：用不同 `key`
- 调整同一份状态的多个字段：合并状态模型或使用 reducer

### useEffect 与 useLayoutEffect 有什么区别
[[React Hooks 面试金句与原理]]
`useLayoutEffect` 在 DOM 提交后、浏览器重新绘制前同步执行，会阻塞绘制，适合测量布局并立即修正；`useEffect` 不应阻塞视觉更新，适合大多数订阅和外部同步。SSR 环境二者都不在服务端执行。

### 父子组件的 Effect 顺序是什么
常见实现中，挂载提交时子组件的 layout/passive Effect setup 先于父组件。但更新、整棵子树删除、Strict Mode 和未来实现的清理顺序存在差异。业务逻辑不应依赖跨组件 Effect 的先后，只依赖“同一个 Effect 的旧 cleanup 先于新 setup”等公开保证。

### React 合成事件是什么
`SyntheticEvent` 是 React 对浏览器事件的统一封装。React 17 起事件委托主要绑定到 React 根容器，且移除了旧的事件池机制。需要原生事件时可读取 `event.nativeEvent`，但不要假设原生与 React 事件传播细节完全相同。

### 如何阻止事件传播与默认行为
使用 `event.stopPropagation()` 阻止 React 事件继续冒泡，使用 `event.preventDefault()` 阻止浏览器默认行为。返回 `false` 不会自动实现这两件事。

### ref、state 与普通变量如何选择
- 影响渲染输出：state
- 跨渲染保留但变化不触发 UI：ref
- 仅服务于本次函数执行：普通变量
- 可从现有 props/state 得出：直接派生，不重复存 state

---
## Reconciliation、Fiber 与渲染流程
### Virtual DOM 是什么，它解决了什么问题
Virtual DOM 是对 UI 的 JavaScript 描述。它让开发者以声明式方式表达界面，并使 React 可以在提交前比较、调度和跨平台渲染。它不保证每次都生成理论上的最少 DOM 操作，也不意味着一定比手写 DOM 更快。

### Reconciliation 与 Diff 是什么关系
Reconciliation 是 React 根据新旧元素树决定组件复用、状态保留和宿主节点变更的整个协调过程；Diff 是其中比较新旧子节点的重要部分。最终变更会记录到 Fiber 树并在 Commit 阶段应用。

### React 为什么能把通用树比较从 O(n³) 降为近似 O(n)
React 采用启发式假设：
- 不跨层级寻找任意移动
- 元素类型不同则替换对应子树
- 同级列表由 `key` 辅助匹配

因此常见协调过程近似线性，但实际成本仍受组件工作量、列表变化模式和 DOM 操作影响。

### 列表 Diff 如何利用 key
React 先顺序匹配可复用节点；不再匹配时会为剩余旧节点建立映射，再根据新节点的 key 或位置查找可复用 Fiber。它还利用旧索引判断节点是否需要移动，并为插入、移动和删除记录相应标记。`key` 相同但元素类型不同仍不能复用。

### Fiber 解决了什么问题
旧的递归协调工作一旦开始就难以暂停。Fiber 把组件树表示为可逐个处理的工作单元，使 Render 阶段具备暂停、恢复、重做和按优先级调度的能力，并承载状态、更新队列和副作用信息。

### Fiber 节点包含哪些关键数据
可按五类理解：
- 身份：`tag`、`type`、`key`
- 树关系：`return`、`child`、`sibling`
- 输入与状态：`pendingProps`、`memoizedProps`、`memoizedState`
- 更新与副作用：`updateQueue`、`flags`、`lanes`
- 双缓冲：`alternate`

字段是内部实现，版本间可能变化。

### 双缓冲 Fiber 树是什么
屏幕当前对应 current 树，React 在内存中基于它构建 work-in-progress 树。渲染成功提交后，两棵树的角色互换，`alternate` 连接同一逻辑节点的两个版本。被中断或失败的工作不会污染当前屏幕。

### 一次状态更新经历哪些阶段
大致流程是：创建更新并入队 → 选择优先级并调度 → Render 阶段执行组件、协调子节点并构建 work-in-progress 树 → Commit 阶段应用 DOM 变更和 Effect → 浏览器绘制与后续 passive Effect。Render 可暂停或废弃，Commit 必须保持同步和一致。

### Render 阶段与 Commit 阶段有什么区别
- Render：计算下一棵树，没有可见 DOM 变更，可被打断、重做，因此必须保持纯函数特性
- Commit：应用 DOM、ref 和布局 Effect 等变更，不可中断，应尽量短

### Commit 阶段做了什么
可概括为：提交前读取必要快照、执行 DOM mutation 与相关清理、更新 ref、执行 layout Effect 和类组件布局生命周期，之后再安排 passive Effect。具体内部子阶段和遍历方式可能随版本变化。

### Scheduler 与 Lane 分别负责什么
Scheduler 负责在主线程上安排可中断任务并在合适时让出执行权；Lane 是 React Reconciler 内部表示更新优先级和批次关系的位掩码模型。二者协作，但浏览器任务优先级、Scheduler 优先级和 Lane 不是同一个概念。

### 为什么渲染必须保持纯粹
并发渲染下 React 可能多次调用、暂停或丢弃一次渲染。如果渲染期间修改外部变量、发请求或操作 DOM，会产生重复和不可回滚的副作用。副作用应放在事件或 Effect 中。

---
## 并发渲染与 Suspense
### 并发渲染是什么
并发渲染是一组底层能力：React 可以按优先级准备多个 UI 版本，并暂停、继续或放弃低优先级 Render。它不是让 JavaScript 多线程执行，Commit 仍然同步完成。

### useTransition 与 startTransition 有什么作用
它们把某些状态更新标记为非紧急 Transition，使输入等紧急更新可以优先响应。`useTransition` 还提供 `isPending`。Transition 不能用于控制文本输入本身，也不能让同步的重计算自动变快；计算仍应拆分、缓存或移出主线程。

### useDeferredValue 与防抖有什么区别
`useDeferredValue` 允许非关键 UI 使用某个值的延迟版本，React 会在后台尝试更新且能被新输入打断。它没有固定延迟，不会减少网络请求；防抖按时间窗口减少触发次数，语义不同。

### Suspense 的工作机制是什么
子树在渲染时挂起后，React 找到最近的 Suspense 边界显示 fallback；资源就绪后重试渲染。Suspense 本身不是通用的数据请求库，数据源必须与框架或 Suspense 集成。它还用于懒加载、流式 SSR 和选择性 hydration。

### React.lazy 如何实现代码分割
`lazy(() => import('./Page'))` 让打包器生成独立 chunk。模块 Promise 未完成时组件会挂起，由最近的 Suspense 展示 fallback；成功后 React 重试渲染。路由级分割通常比对大量小组件分割更有效。

```jsx
const SettingsPage = lazy(() => import('./SettingsPage'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <SettingsPage />
    </Suspense>
  );
}
```

### 什么是自动批处理
React 18 的 `createRoot` 默认会把同一时机中的多次状态更新合并为较少的提交，包括 Promise、定时器和原生事件中的更新。批处理不意味着不同状态更新会互相覆盖；更新队列仍按规则计算。

### Strict Mode 为什么会出现“执行两次”
开发环境 Strict Mode 会额外调用部分纯函数逻辑，并对 Effect 执行 setup → cleanup → setup，以发现渲染副作用、不可重复初始化和缺失清理。生产环境不会保留这类开发检查，不应通过关闭 Strict Mode 掩盖问题。

---
## 状态管理与数据请求
### Redux 解决什么问题
Redux 通过单一状态树、action、reducer 和订阅机制，让跨组件状态变更可预测、可追踪，并提供中间件与开发工具。现代 Redux 推荐 Redux Toolkit，减少样板代码并内置合理默认配置。

### Context 加 useReducer 能替代 Redux 吗
小型、低频更新场景可以。它缺少 Redux Toolkit 完整的中间件、DevTools、selector 优化和成熟生态，而且 Context value 变化会影响全部消费者。是否替代取决于规模、更新频率和调试需求。

### Redux、MobX 与 Zustand 有什么区别
- Redux Toolkit：显式 action/reducer、不可变更新、工具链成熟，适合复杂可追踪流程
- MobX：基于 observable 自动追踪依赖，样板少但数据流更隐式
- Zustand：轻量 Store 与 selector API，上手快，适合中小型客户端状态

服务端状态应优先评估 TanStack Query、SWR 或框架数据层。

### Redux 中如何处理异步请求
简单流程可用 `createAsyncThunk`，复杂缓存和请求生命周期优先考虑 RTK Query。Thunk 本质是允许 dispatch 一个函数，该函数可读取 state、执行异步逻辑并继续 dispatch action。

```js
const fetchUser = createAsyncThunk('user/fetch', async id => {
  return api.getUser(id);
});
```

### Redux 中如何实现日志中间件
中间件签名是 `store => next => action`，必须调用并返回 `next(action)`，否则 action 链会被截断。

```js
const logger = store => next => action => {
  const prevState = store.getState();
  const result = next(action);
  console.log({ action, prevState, nextState: store.getState() });
  return result;
};
```

### 同一页面多个组件请求相同 API，如何避免重复请求
优先把请求交给带缓存与去重的数据层，用统一 query key 共享结果；也可在最近公共父级请求一次后下发。还要定义缓存时效、错误重试、取消、失效和并发竞态，而不是只缓存最终值。

### useFetch 应该考虑哪些边界
至少包含 loading、error、取消请求、组件卸载、参数变化竞态、响应状态校验、缓存与重试。生产项目优先使用成熟请求库；手写 Hook 主要用于展示思路。

### 客户端状态与服务端状态有什么区别
客户端状态由前端拥有，例如弹窗、主题和草稿；服务端状态由远端拥有，具有缓存、过期、重取、并发和一致性问题。把二者分开能避免全局 Store 变成难维护的数据仓库。

---
## 性能优化与排查
### React 性能优化的正确顺序是什么
先测量，再定位根因，最后选择优化：
1. React DevTools Profiler 找出慢提交和高频渲染组件
2. Chrome Performance 区分脚本、样式计算、布局、绘制和网络问题
3. 检查状态放置、组件边界、列表规模和 props 稳定性
4. 再使用 memo、虚拟列表、代码分割、缓存或并发 API
5. 优化后重新测量，确认收益且没有引入错误

### 组件为什么会重新渲染
常见原因包括自身 state 更新、父组件重新渲染、消费的 Context 变化以及外部 Store 快照变化。props 引用变化本身不是普通组件“被触发”的独立来源，而是父组件渲染后子组件默认也会执行；`React.memo` 才会比较 props 决定是否跳过。

### 如何减少不必要的重新渲染
- 把 state 放到真正需要它的最低公共位置
- 拆分高频与低频更新区域
- 通过 `children` 组合隔离不相关子树
- 必要时使用 `React.memo` 并稳定关键 props
- 拆分 Context 或使用 selector
- 避免 Effect 造成级联状态更新

不要机械地消灭所有重渲染，便宜且正确的渲染通常比复杂 memo 更好。

### inline object 和 inline function 一定有性能问题吗
不一定。创建小对象或函数通常很便宜；只有当它破坏了下游 memo、触发 Effect 或导致昂贵第三方组件更新时，稳定引用才有实际价值。应以 Profiler 证据为准。

### 长列表如何优化
使用虚拟列表只渲染可视区域，保证稳定 key，减少每项渲染成本，并处理动态高度、滚动定位和无障碍。分页或增量加载减少数据量，但不能替代 DOM 虚拟化。

### 状态更新导致输入卡顿时如何排查
先确认是事件处理、组件 Render、DOM 布局还是网络导致；再缩小高频 state 的影响范围，对昂贵派生计算做缓存，把非紧急列表更新放入 Transition，长列表使用虚拟化，CPU 密集计算移到 Web Worker。

### 代码分割有哪些策略
- 路由级分割：收益通常最大
- 重型且低频功能按交互加载
- 预加载下一步高概率访问的 chunk
- 避免过度切分造成请求瀑布和 fallback 闪烁

### React Compiler 会让 useMemo 和 useCallback 消失吗
React Compiler 能基于静态分析自动 memoize 组件和表达式，减少手写 memo 的需要，但不是“React 19 自动内置并默认开启”。它需要单独配置且受代码可分析性约束；语义上必要的稳定引用、第三方 API 边界和经测量的特殊场景仍需判断。

### Profiler API 能提供什么
`<Profiler>` 的 `onRender` 可获得提交阶段的 `actualDuration`、`baseDuration`、开始时间等信息，用于量化某个子树的渲染成本。React DevTools Profiler 更适合交互式定位；生产分析需注意采样与构建配置的额外开销。

---
## SSR、Hydration 与 Server Components
### CSR、SSR、SSG 有什么区别
- CSR：浏览器下载 JavaScript 后生成主要 UI，交互灵活但首屏和 SEO 依赖资源加载
- SSR：每次请求在服务端生成 HTML，再在客户端 hydration
- SSG：构建时生成 HTML，访问快但内容更新需要重新生成或增量策略

实际项目常由框架按路由和数据选择混合渲染。

### 什么是 Hydration
Hydration 是客户端 React 复用服务端 HTML、建立组件树并绑定交互的过程。服务端和客户端首屏输出必须一致，否则会产生 hydration mismatch，严重时 React 会放弃局部复用并重新客户端渲染。

### 常见 hydration mismatch 原因有哪些
- 渲染时读取 `window`、`localStorage` 或视口尺寸
- `Date.now()`、随机数、时区或本地化结果不同
- 无效 HTML 嵌套被浏览器自动修正
- 服务端与客户端数据快照不一致
- 条件分支导致 DOM 结构不同

浏览器专属逻辑放到客户端 Effect，稳定 ID 使用 `useId`，数据应传递同一快照。

### SSR 中能访问 localStorage 吗
不能。服务端没有 `window`、`document` 和 `localStorage`。可以用 `typeof window !== 'undefined'` 做能力判断，但为了首屏一致性，通常应在客户端 Effect 中读取并提供明确的初始 UI。

### 流式 SSR 是什么
服务端可先发送应用 shell 和已完成内容，再随数据就绪逐步流出 Suspense 边界内容，改善 TTFB 和首屏呈现。Node 环境常用 `renderToPipeableStream`，Web Streams 环境常用 `renderToReadableStream`。

### 选择性 Hydration 是什么
Suspense 边界让 React 可以按优先级 hydration 页面不同区域。用户交互的区域可被优先激活，而不是等待整棵树从上到下完成，改善可交互性。

### React Server Components 与 SSR 有什么区别
- SSR：把组件首屏渲染成 HTML，客户端通常仍需下载对应组件代码并 hydration
- RSC：组件只在服务端执行，结果以 RSC Payload 传给客户端，Server Component 自身代码不进入客户端包

二者可以组合。RSC 需要框架和打包器集成，不是仅调用一个 React API 就能完整落地。

### Server Component 与 Client Component 如何划分
Server Component 适合靠近数据源、读取后端资源和减少客户端 JavaScript；Client Component 适合 state、Effect、浏览器 API 和事件交互。边界之间传递的 props 必须可序列化，敏感信息不能越过服务端到客户端边界。

### use API 有什么作用
React 19 的 `use(resource)` 可以在渲染中读取 Promise 或 Context。读取未完成 Promise 会触发 Suspense，拒绝则交给 Error Boundary。与普通 Hooks 不同，`use` 可在条件和循环中调用，但仍必须在组件或 Hook 内调用，也不能放在 `try/catch` 中吞掉挂起行为。

---
## React 版本与现代特性
### React 17 的主要变化是什么
React 17 主要为渐进升级铺路：事件委托从 `document` 移到 React 根容器、移除合成事件池、新 JSX Transform 得到支持，并调整部分 Effect 清理行为。它没有引入新的面向开发者核心特性。

### React 18 的主要变化是什么
- `createRoot` 与 `hydrateRoot`
- 并发渲染基础能力
- 自动批处理
- `startTransition`、`useTransition`、`useDeferredValue`
- `useId`、`useSyncExternalStore`、`useInsertionEffect`
- Suspense SSR、流式渲染和选择性 hydration 改进
- Strict Mode 开发检查增强

“Concurrent Mode”不再是一个需要整体打开的独立模式，而是由并发根和具体功能逐步采用相关能力。

### React 19 的主要变化是什么
- Actions 与表单 action，统一 pending、error、乐观更新和提交结果处理
- `useActionState`、`useOptimistic`、`use`，以及 React DOM 的 `useFormStatus`
- 函数组件可把 `ref` 作为 prop，ref cleanup 函数得到支持
- `<Context value={...}>` 可直接作为 Provider
- 原生支持文档 metadata、样式表优先级、异步脚本和资源预加载 API
- Server Components 与 Server Actions 相关能力进入稳定发布面，但底层打包器集成 API 仍需跟随框架
- 改善 hydration 和错误报告

React Compiler 是独立工具链能力，不能简单当作“安装 React 19 就自动获得”。

### React 19 Actions 解决什么问题
Action 可以接收异步函数，并把 pending、错误、表单重置和乐观更新串成统一流程。`useActionState` 管理 action 结果，`useFormStatus` 读取父表单提交状态，`useOptimistic` 在请求完成前展示预测结果。

### useOptimistic 的适用场景是什么
它适合点赞、评论、状态切换等成功概率高且容易回滚的交互。必须设计失败提示、回滚/重试和重复提交策略；资金、权限等高风险操作不应只依赖无确认的乐观 UI。

### React 19.2 值得关注什么
React 19.2 增加了 `<Activity>`、`useEffectEvent`、面向 Server Components 的 `cacheSignal`，并增强性能分析与服务端渲染能力。面试中应说明这些是 19.2 能力，避免和 React 19.0 的首发特性混为一谈。

### useEffectEvent 解决什么问题
它允许 Effect 中的非响应式逻辑始终读取最新 props/state，而不因为这些值变化重新同步整个 Effect。返回的 Effect Event 只能从 Effect 相关逻辑调用，不能用来逃避本应声明的依赖。

### Activity 组件解决什么问题
`<Activity>` 用于隐藏和恢复一部分 UI：隐藏时可清理 Effect，同时保留组件状态，并让隐藏内容以更低优先级准备。它适合标签页预渲染、返回页面状态保留等场景，不等同于简单的 CSS `display: none`。

---
## 工程实践与架构设计
### 新加入项目后如何快速把 React 应用跑起来
1. 阅读 README、CONTRIBUTING 和部署文档
2. 确认 Node、包管理器与锁文件版本，不混用 npm、pnpm、yarn
3. 安装依赖并复制环境变量模板，确认哪些变量可以暴露到客户端
4. 运行 lint、类型检查、测试和开发服务器
5. 从入口、路由、状态层、请求层和构建配置理解目录
6. 用一个小改动走通本地开发、提交检查和预览环境

### 如何设计 React 组件 API
- 明确受控与非受控模式，避免双重数据源
- 优先组合和语义化 props，避免大量互斥布尔参数
- 支持 `className`、`style`、ref 和必要的原生属性透传
- 保持事件命名和参数一致
- 为 loading、empty、error、disabled 和边界数据设计状态
- 默认满足键盘操作、焦点管理和 ARIA 要求

### 如何设计 UI 组件库
从 Design Token、基础组件和组合规则开始；统一 API、主题、样式隔离和无障碍；提供文档与交互示例；输出 ESM 并验证 tree shaking；使用单元测试、交互测试、视觉回归和多框架/多版本兼容矩阵；同时管理版本、变更日志与迁移指南。

### Render Props、HOC 与自定义 Hook 如何选择
- 自定义 Hook：复用无 UI 的有状态逻辑，现代代码首选
- Render Props：调用方需要完全控制渲染结构时仍有价值
- HOC：适合横切增强或维护旧代码，但要处理 props 冲突、ref 和调试层级

三者都不等于共享同一份状态。

### React 应用如何做错误治理
按层级设置 Error Boundary，提供可恢复的 fallback；事件和请求错误单独处理；上报错误、组件栈、版本、路由和用户操作上下文；避免记录隐私；对动态 import 失败、离线、权限和接口降级设计重试或回退。

### 如何测试 React 组件
优先测试用户可观察行为而不是内部 state：使用语义化查询模拟点击、输入和键盘操作；对网络使用可控 mock；覆盖 loading、成功、空数据、错误和竞态；关键流程再使用端到端测试。不要把快照测试当作主要断言。

### 如何保证组件可访问性
优先使用原生语义元素；表单具有 label；交互元素支持键盘；Modal 正确管理焦点、Esc 和焦点恢复；状态变化通过合适的 ARIA 通知；颜色对比满足要求。可结合 eslint-plugin-jsx-a11y、Testing Library 和 axe 自动检查。

### 如何组织大型 React 项目
按业务特性而不是纯文件类型组织模块，明确页面、领域组件、共享 UI、数据访问和工具边界；限制跨层导入；让状态靠近使用位置；公共抽象需由多个真实场景推动，避免提前建立“万能组件”。

---
## 常见手写题
### 使用 useState 实现计数器
```jsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <output>{count}</output>
      <button onClick={() => setCount(value => value + 1)}>+1</button>
      <button onClick={() => setCount(value => value - 1)}>-1</button>
      <button onClick={() => setCount(0)}>重置</button>
    </div>
  );
}
```

### 实现 usePrevious
Effect 在提交后更新 ref，因此本次渲染读取到的是上一次提交保存的值。

```jsx
function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

### 实现一个基础 useFetch
下面用于面试展示取消与状态建模；生产项目还应考虑缓存、重试、竞态策略和框架数据层。

```jsx
function useFetch(url) {
  const [state, setState] = useState({
    data: null,
    error: null,
    loading: false,
  });

  useEffect(() => {
    const controller = new AbortController();
    setState({ data: null, error: null, loading: true });

    fetch(url, { signal: controller.signal })
      .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then(data => setState({ data, error: null, loading: false }))
      .catch(error => {
        if (error.name !== 'AbortError') {
          setState({ data: null, error, loading: false });
        }
      });

    return () => controller.abort();
  }, [url]);

  return state;
}
```

### 使用 Render Props 请求数据
```jsx
class Fetch extends React.Component {
  state = { data: null, error: null, loading: true };

  componentDidMount() {
    fetch(this.props.url)
      .then(response => response.json())
      .then(data => this.setState({ data, loading: false }))
      .catch(error => this.setState({ error, loading: false }));
  }

  render() {
    return this.props.children(this.state);
  }
}

<Fetch url="/api/user">
  {({ data, error, loading }) => {
    if (loading) return <Loading />;
    if (error) return <ErrorView error={error} />;
    return <User user={data} />;
  }}
</Fetch>;
```

### 实现命令式 Message API
真实组件库应使用单一容器和队列，避免每条消息创建一个独立 React Root。下面展示最小思路：
```jsx
import { createRoot } from 'react-dom/client';

let root;
let container;

function ensureRoot() {
  if (!container) {
    container = document.createElement('div');
    container.setAttribute('aria-live', 'polite');
    document.body.appendChild(container);
    root = createRoot(container);
  }
  return root;
}

export function showMessage(content) {
  ensureRoot().render(<div role="status">{content}</div>);
}
```

### 使用 useReducer 实现 forceUpdate 是否合理
可以通过递增无业务意义的状态触发渲染，但通常说明数据没有正确建模。应先检查是否直接修改了对象、是否把 UI 数据错误放进 ref，或外部 Store 是否缺少订阅。

```jsx
const [, forceUpdate] = useReducer(value => value + 1, 0);
```

### 如何实现一个可取消的防抖 Hook
```jsx
function useDebouncedValue(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### 如何回答代码输出题
先按以下顺序推导：
1. 标记每次渲染的 state 快照与闭包
2. 区分值更新和函数式更新
3. 确认更新是否处于同一批次
4. 区分 Render、DOM Commit、layout Effect 和 passive Effect
5. 检查 Strict Mode 是否只存在于开发环境

题目缺少具体代码时不能直接断言输出。
