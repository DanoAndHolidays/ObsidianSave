# React

### 【Q008】当新入职一家公司时，如何快速搭建开发环境并让应用跑起来
1. 阅读项目 README 和文档（onboarding、CONTRIBUTING）
2. 安装 Node 版本管理工具，确认 Node 版本（.nvmrc）
3. `git clone` + `npm install` / `pnpm install`
4. 配置环境变量（.env.local/.env.development）
5. 启动开发服务器（npm run dev / npm start）
6. 配置 IDE（VSCode 插件、ESLint、Prettier）
7. 了解项目目录结构和技术栈
8. 跑起来后浏览 / 了解路由和页面

### 【Q010】了解 React 中的 ErrorBoundary 吗，它有那些使用场景
React 16 引入的错误边界（类组件实现 `componentDidCatch` / `getDerivedStateFromError`，函数式组件不能直接作为 Error Boundary）：
- 捕获子组件树渲染过程中的错误，阻止整个应用崩溃
- 场景：第三方组件、复杂 UI 模块、异步数据渲染等
- 不捕获：事件回调中的错误、异步代码（setTimeout）、SSR 中的错误、Error Boundary 自身的错误

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error, info) { console.error(error, info); }
  render() {
    if (this.state.hasError) return <h1>Something went wrong.</h1>;
    return this.props.children;
  }
}
```

### 【Q013】有没有使用过 react hooks，它带来了那些便利
1. 函数组件中可以使用 state 和生命周期（不需要 class）
2. 逻辑复用变得容易（自定义 hook，脱离 this）
3. 关注点分离，相关逻辑聚拢，而不是分散在生命周期方法中
4. 减少嵌套（不用 render props / HOC）
5. 代码更简洁、Tree Shaking 友好

### 【Q014】如何使用 react hooks 实现一个计数器的组件
```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <button onClick={() => setCount(c => c - 1)}>-1</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

### 【Q021】React 中，cloneElement 与 createElement 各是什么，有什么区别
- `createElement(type, props, ...children)`：创建 React 元素，是 JSX 的编译结果
- `cloneElement(element, props, ...children)`：以已有 element 为基础、shallow 合并新 props 和 children。常用于给子组件传递 props（如 React.Children.map 遍历 children 时附加 props）

### 【Q038】使用 react 实现一个通用的 message 组件
```jsx
// Message 显示组件 + 命令式调用封装
function Message({ type, content, onClose }) {
  return <div className={`msg msg-${type}`}>{content}</div>;
}

// 命令式 API
function showMessage(type, content, duration = 3000) {
  const div = document.createElement('div');
  document.body.appendChild(div);
  const root = createRoot(div); // React 18
  const close = () => { root.unmount(); div.remove(); };
  root.render(<Message type={type} content={content} onClose={close} />);
  setTimeout(close, duration);
}
export const message = {
  success: (msg) => showMessage('success', msg),
  error: (msg) => showMessage('error', msg),
};

// React 17 兼容：import { render } from 'react-dom'
// React 18：import { createRoot } from 'react-dom/client'
```

### 【Q066】如何使用 react hooks 实现 useFetch 请求数⌚️
```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(url)
      .then(res => res.json())
      .then(data => { if (!cancelled) setData(data); })
      .catch(err => { if (!cancelled) setError(err); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [url]);

  return { data, loading, error };
}
```

### 【Q067】react 如何使用 render prop component 请求数据
```jsx
class Fetch extends React.Component {
  state = { data: null, loading: true };
  componentDidMount() {
    fetch(this.props.url)
      .then(res => res.json())
      .then(data => this.setState({ data, loading: false }));
  }
  render() {
    return this.props.children(this.state);
  }
}
// 使用
<Fetch url="/api/user">
  {({ data, loading }) => loading ? <div>Loading...</div> : <div>{data.name}</div>}
</Fetch>
```

### 【Q068】React Portal 有哪些使用场景
Portal 将子组件渲染到父组件 DOM 树以外的 DOM 节点，保持 React 组件树的层级不变（事件冒泡仍按 React 树）。

**场景**：模态框（Modal）、Tooltip、Dropdown 菜单、通知 Toast、全局 Loading。

```jsx
import { createPortal } from 'react-dom';
function Modal({ children }) {
  return createPortal(children, document.body);
}
```

### 【Q069】什么是 virtual DOM，它的引入带了什么好处
Virtual DOM 是真实 DOM 的 JS 对象映射。UI=f(data)，数据变化时：
1. 生成新的 Virtual DOM 树
2. Diff 新旧两棵树，找出最小变更（O(n)）
3. Patch 批量更新真实 DOM

**好处**：
- 开发者不必直接操作 DOM（声明式），框架自动化优化变更
- 跨平台（Virtual DOM → 不同渲染器：浏览器 DOM、React Native、Canvas）
- 批量更新、减少直接 DOM 操作

### 【Q071】react 与 vue 数组中 key 的作用是什么
key 帮助框架的 diff 算法**识别虚拟 DOM 节点的身份**（哪些元素改变了、新增、移除）。没有 key 时，默认用顺序对比（index），可能导致不必要的 DOM 更新/复用错误状态（如：输入框内容未随数据更新清空）。

### 【Q092】react 中 ref 是干什么用的，有哪些使用场景
ref 获取 DOM 元素或组件实例的引用：
- 焦点管理（自动 focus）
- 触发动画
- 获取 DOM 尺寸/位置
- 集成第三方 DOM 库
- 存储不触发重渲染的可变值（ref.current）

```jsx
const inputRef = useRef(null);
useEffect(() => { inputRef.current?.focus(); }, []);
return <input ref={inputRef} />;
```

### 【Q100】如何使用 react/vue 实现一个 message API
同 Q038。

### 【Q142】react hooks 中如何模拟 componentDidMount
```jsx
useEffect(() => {
  // 这里在组件挂载后执行（仅一次，类似 componentDidMount）
}, []); // 空依赖数组
```

### 【Q146】如果使用 SSR，可以在 created/componentWillMount 中访问 localStorage 吗
**不可以**。SSR 时没有浏览器环境，没有 window、localStorage、document 等对象。需要在客户端代码中用 `typeof window !== 'undefined'` 检查，或把相关逻辑放在 useEffect / componentDidMount 中（只在客户端执行）。

### 【Q151】react hooks 如何替代或部分替代 redux 功能
- `useContext` + `useReducer` 替代 Redux 全局状态
- `useState` 替代组件级状态
- 自定义 hook 封装业务逻辑（`useXXX`）
- Context 性能优化（拆分多个 Context 避免全树重渲染）

### 【Q152】如何实现一个 react hook，你有没有自己写过一个
自定义 hook 是以 `use` 开头的函数，内部可使用其他 Hooks：
- `useLocalStorage`：同步状态到 localStorage
- `useDebounce` / `useThrottle`：防抖/节流值
- `usePrevious`：获取上一次渲染的值
- `useWindowSize`：监听窗口尺寸

### 【Q154】在 react/vue 中数组是否可以以在数组中的次序为 key
**不建议**。用 index 作为 key 在增删/排序场景下会导致错误的复用（框架认为同一个 key 的元素未变，不会重新渲染内部状态，如输入框内容错位）。关键是要与数据唯一稳定 id 绑定。

### 【Q164】React 中 fiber 是用来做什么的 ⌚️
Fiber 是 React 16 的重写的 Reconciliation 架构：
1. 将渲染任务拆成小的"工作单元"，通过**可中断**的循环调度
2. 实现**时间切片（Time Slicing）**：在浏览器空闲时处理任务，高优先级任务（用户输入）可打断低优先级更新
3. 双缓存 Fiber Tree 和链表结构支持增量渲染

### 【Q211】React hooks 中 useCallback 的使用场景是什么
缓存函数引用，避免子组件因函数引用变化而无效渲染（配合 React.memo）。注意不一定需要所有函数都用 useCallback：只在传给子组件且子组件用 React.memo 优化时有用。

```jsx
const handleClick = useCallback(() => {
  doSomething(count);
}, [count]);
// 该 handleClick 只在 count 变化时创建新引用
```

### 【Q235】useEffect 中如何使用 async/await
useEffect 的回调不能直接是 async 函数（async 返回 Promise，useEffect 期望返回 undefined 或 cleanup 函数）：

```jsx
useEffect(() => {
  async function fetchData() {
    const data = await fetchSomething();
    setData(data);
  }
  fetchData();
}, []);
// 或 IIFE：
useEffect(() => {
  (async () => {
    const data = await fetchSomething();
  })();
}, []);
```

### 【Q271】react hooks 的原理是什么
Hooks 基于**链表**实现：每个组件关联一个 hook 链表（Fiber 节点的 memoizedState）。
- 首次渲染：按调用顺序创建 hook 节点（形成链表）
- 再次渲染：按顺序遍历链表读取对应 hook 的状态
- 这就是为什么 Hooks 不能被放在条件/循环中（打乱顺序导致错位）

### 【Q277】redux 解决什么问题，还有什么其他方案
**解决**：跨组件共享状态、统一的状态管理、可预测的状态变更、时间旅行调试。

**其他方案**：
- React Context + useReducer（轻量场景）
- MobX（响应式）
- Zustand（轻量、简洁）
- Jotai / Recoil（原子化状态）
- XState（状态机）
- Pinia（Vue 生态）

### 【Q278】为什么不能在表达式里面定义 react hooks
React 通过调用顺序识别每个 Hook 的身份。如果放在条件/循环中，不同渲染轮次的 Hook 数量/顺序不一致，会产生错位并导致状态混乱。所以 React 要求 Hooks 在顶层（Top Level）调用。

### 【Q367】redux 和 mobx 有什么不同
- **Redux**：单一 Store、纯函数 Reducer、不可变数据、中间件机制、显式 dispatch action
- **MobX**：多 Store、响应式（Observable）、可变数据（直接赋值）、隐式追踪依赖（autorun）、装饰器风格、学习成本更低

### 【Q368】关于 React hooks 的 caputre value，以下输出多少
（需看具体代码）Hooks Capture Value 是闭包的特性：state 是固定快照，回调中的 state 是创建时那个渲染周期的值。

### 【Q369】在 React 项目中 immutable 是优化性能的
Immutable（不可变数据）确保引用变更=数据变更，让 React.memo / PureComponent 的浅比较（shallow compare）能正确判断是否需要重渲染。相比直接 mutable 修改（引用不变但内容变了）、shallow compare 会跳过本应更新的组件。

### 【Q371】在 redux 中如何发送请求
使用 **Redux Thunk**（最常用）或 **Redux Saga**：
```javascript
// Redux Thunk
const fetchUser = (id) => async (dispatch) => {
  dispatch({ type: 'FETCH_USER_REQUEST' });
  try {
    const user = await api.getUser(id);
    dispatch({ type: 'FETCH_USER_SUCCESS', payload: user });
  } catch (err) {
    dispatch({ type: 'FETCH_USER_FAILURE', error: err.message });
  }
};
```

### 【Q375】在 redux 中如何写一个记录状态变更的日志插件
```javascript
// Redux Middleware 记录日志
const logger = store => next => action => {
  console.log('dispatching', action);
  console.log('prev state', store.getState());
  const result = next(action);
  console.log('next state', store.getState());
  return result;
};
// applyMiddleware(logger)
```

### 【Q378】React 在 setState 时发生了什么
1. 调用 setState/useState 的 dispatch
2. React 标记组件需要更新，创建更新对象（Update），加入更新队列
3. 调度（scheduler）协调优先级
4. Render Phase：重新执行组件函数/Render 方法，生成新 Fiber 树（Virtual DOM 的最新表示）
5. Reconciliation 阶段：Diff 新旧 Fiber 树，标记变更
6. Commit Phase：将变更应用到 DOM（同步，不可中断）
7. 执行相应的 Effect（useLayoutEffect 同步执行，useEffect 异步执行）

### 【Q380】如何设计一个UI组件库
1. **设计规范**：颜色、字体、间距、圆角、阴影等 Design Token
2. **组件分类**：基础组件（Button、Input）、布局组件、业务组件
3. **API 设计**：统一的 props 命名、组合 vs 配置、受控/非受控
4. **可访问性**：ARIA、键盘导航、屏幕阅读器
5. **主题**：CSS 变量 / ThemeProvider 支持多主题和自定义
6. **开发环境**：Storybook 用于开发和文档
7. **构建打包**：Rollup/Vite 构建，导出 ESM + CJS，支持 Tree Shaking
8. **测试**：单元测试 + 视觉回归测试

### 【Q403】React 中的 dom diff 算法如何从 O(n3) 优化到 O(n) 的
传统 Tree Diff 时间复杂度 O(n³)。React 基于三个假设进行优化：
1. **同层级比较**：只对同级节点进行比较（不跨层级 diff）
2. **类型不同直接替换**：元素类型改变时直接卸载旧树、新建整棵子树
3. **key 标识**：通过 key 在列表中识别元素身份，实现高效增删移动

### 【Q404】在 React 应用中如何排查性能问题
1. **React DevTools Profiler**：记录组件渲染时间，找出慢渲染组件
2. **Chrome Performance**：JS 执行、Layout、Paint 各阶段耗时
3. **why-did-you-render**：检测不必要的重渲染
4. **React.memo / useMemo / useCallback**：检查是否缺少 memo
5. **虚拟列表**：大数据量列表的性能
6. **Code Splitting**：检查 Bundle 大小是否过大

### 【Q408】React 17.0 有什么变化
- 无重大新特性，主要渐进式升级
- 新 JSX Transform（不需要 `import React from 'react'`）
- 事件委托从 document 改为 root 节点（便于多版本共存）
- 移除事件池（SyntheticEvent pooling 不再需要）
- 副作用清理时机（useEffect cleanup 在异步执行）
- 为 React 18 的 Concurrent Mode 铺路

### 【Q466】在 SSR 项目中如何判断当前环境时服务器端还是浏览器端
```javascript
const isServer = typeof window === 'undefined';
const isClient = typeof window !== 'undefined';
// 需要浏览器 API 的代码放在 if (isClient) { ... } 中
```

### 【Q497】React.setState 是同步还是异步的
**React 18 之前**：在 React 合成事件和生命周期中是**异步批量更新**，在 setTimeout/Promise/原生事件中是**同步**的。
**React 18（自动批处理）**：所有更新都是**异步批量**的（setTimeout 中也批处理）。可以使用 `flushSync` 强制同步。

### 【Q498】什么是服务器渲染 (SSR)
**SSR（Server-Side Rendering）**：服务端将 React/Vue 组件渲染为 HTML 字符串返回给浏览器，浏览器收到后直接展示 HTML，然后加载 JS 进行"注水"（Hydration：客户端 JS 接管交互）。

**优点**：更快的首屏加载（白屏短）、SEO 友好
**缺点**：服务器负载大、开发复杂度高、TTFB 可能较长

### 【Q499】在 React 中如何实现代码分割 (code splitting)
```jsx
// React.lazy + Suspense
const LazyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
}

// 路由级别分割（React Router）
const About = React.lazy(() => import('./About'));
```

### 【Q500】在 React 中如何做好性能优化
1. **React.memo** 避免不必要的重渲染
2. **useMemo / useCallback** 缓存计算结果和函数引用
3. **虚拟列表**（react-window/react-virtuoso）
4. **代码分割**（React.lazy + Suspense、路由懒加载）
5. **避免 inline object/function** 直接作为 props
6. **使用 useTransition / useDeferredValue** 降低低优先级状态更新的影响
7. **图片优化**（懒加载、WebP 格式、CDN）
8. **key 用稳定唯一 id** 不用 index

### 【Q501】在 React 中发现状态更新时卡顿，此时应该如何定位及优化
1. Profiler 找到慢组件 → 检查是否是高频更新（useMemo/useCallback/React.memo）
2. 查看是否触发了性能瓶颈 API（animate 读取了 layout 触发重排）
3. **拆分状态**，将独立的 state 拉到不同组件
4. **虚拟列表**处理长列表
5. 使用 **useTransition** 降低不紧急更新的优先级
6. 检查不必要的重渲染用 `why-did-you-render`

### 【Q502】当多次重复点击按钮时，以下三个 Heading 是如何渲染的
（需看具体代码）React 18 自动批处理：在事件回调中多次 setState 会合并为一次渲染。

### 【Q552】关于 setState 以下代码的输出
（需看具体代码）考点：setState 在 React 18 中的批处理行为变更、类组件的 setState 接收值/函数两种方式的区别、连续 setState 的合并。

### 【Q590】React 中什么是合成事件
**SyntheticEvent**：React 封装原生浏览器事件的跨浏览器包装对象。
- 统一不同浏览器事件 API（如 event.target、event.preventDefault()）
- 事件委托（React 17 开始挂载到 root 节点而非 document）
- 事件池回收（React 17 移除了事件池，不需要 e.persist()）

### 【Q592】前端项目中有哪些副作用
- 数据获取（fetch/API 请求）
- 订阅/取消订阅（websocket、event listener）
- 手动修改 DOM
- 计时器（setTimeout/setInterval）
- 写入 localStorage/cookie
- 日志上报
- 修改全局变量/ref

### 【Q593】React/Vue 中受控组件与不受控组件的区别
- **受控组件**：value 由 state 控制，onChange 更新 state。表单数据由 React/Vue 管理。
- **不受控组件**：value 由 DOM 自身管理，通过 ref 获取表单值。
- React 中受控组件用 useState 管理 input 的 value；不受控组件用 useRef 获取。

### 【Q600】在 React hooks 中如何模拟 forceUpdate
```jsx
const [, forceUpdate] = useReducer(x => x + 1, 0);
// 或
const [_, setTick] = useState(0);
const forceUpdate = () => setTick(t => t + 1);
// 或使用 useSyncExternalStore / useReducer 实现
```

### 【Q611】React/Vue 中兄弟组件如何进行通信
1. **状态提升**：将共享状态提升到最近的公共父组件，通过 props 传递
2. **全局状态管理**：Redux、Zustand、Context / Pinia、Vuex
3. **事件总线**：发布订阅（不推荐用在 React 中，但 Vue 可用 EventBus）
4. **URL 参数**：通过路由参数传递

### 【Q612】React.memo 中是如何实现性能优化的
React.memo 对组件进行包裹，通过**浅比较**（shallow compare）新旧 props 判断是否需要重渲染：props 相同则复用上次渲染结果（跳过 render 和后续的 diff 比较）。可传入自定义比较函数控制比较逻辑。

### 【Q614】immer 的原理是什么，为什么它的性能更高
Immer 基于 **Copy-on-Write + Proxy**：
1. 用 Proxy 追踪对草稿（draft）的操作
2. 只复制被修改的部分（结构共享），未修改的保持引用不变
3. 返回新的不可变状态

这种结构性共享（Structural Sharing）避免了深拷贝整个 state 树的性能开销，同时保证了不可变性。

### 【Q615】React.useMemo 与 React.useCallback 是如何进行性能优化的
- **useMemo**：缓存**计算结果**（值），依赖不变则直接返回缓存值，避免重复执行昂贵的计算
- **useCallback**：缓存**函数引用**，依赖不变则函数引用不变，配合 React.memo 避免子组件不必要的重渲染

### 【Q624】同一页面三个组件请求同一个 API 发送了三次请求，如何优化
- **请求缓存**：在请求层做缓存（SWR、React Query 的 dedup、共享一个 Promise 引用）
- **提升到共同父组件**：在父组件请求一次，通过 props/context 下发给三个子组件
- **状态管理**：放进全局 store（Redux/Zustand）
- **React Query/SWR** 自动去重（同一时间同一 key 只发一次请求）

### 【Q627】如何优化 React 项目的性能
同 Q500。

### 【Q653】useLayoutEffect 和 useEffect 有什么区别
- **useEffect**：DOM 更新 + 浏览器**绘制后**异步执行，不阻塞渲染（不阻塞视觉更新）
- **useLayoutEffect**：DOM 更新后、浏览器**绘制前**同步执行（阻塞渲染）。用于需要在浏览器绘制前读取/修改 DOM 尺寸/位置的场景（避免闪烁）
- 顺序：DOM 更新 → useLayoutEffect（同步）→ 浏览器绘制 → useEffect（异步）

### 【Q659】在 React Hooks 中实现 usePreviouseValue 取上次渲染的值
```jsx
function usePrevious(value) {
  const ref = useRef();
  useEffect(() => { ref.current = value; });
  return ref.current; // 返回上一次的值
}
```

### 【Q699】在虚拟 DOM 中进行 diff 算法时，介绍当根据 key 对数组进行重用时的算法
1. 遍历新 children，为每个元素建立 key → index 的 map
2. 遍历旧 children，对每个结点检查其 key 是否在新 map 中：
   - 在：如果可在对应位置复用，则直接移动（Fiber 架构中的 Placement）
   - 不在：旧结点需要被删除（标记 Deletion）
3. 新 children 中有但旧 map 中没有的 key → 新插入（标记 Placement）
4. 复杂度 O(n)

### 【Q474】在 react 中，以下父子组件的 useEffect/useLayoutEffect 顺序如何
**子组件的 effect 先于父组件执行**。挂载时：子 useEffect → 父 useEffect。Commit Phase 中的 useLayoutEffect 和 useEffect 的调用顺序均是**从子到父**。Unmount 时：cleanup 子 → 父。

### 【Q749】React18 有哪些新特性
1. **Concurrent Mode（并发特性）**：并发渲染，可中断
2. **自动批处理**：所有更新都批量（不只在事件回调）
3. **Transitions**：`startTransition` / `useTransition` 标记低优先级更新
4. **Suspense 改进**：支持服务端 Suspense、Transition 中的 Suspense
5. **新的 Hooks**：`useId`、`useDeferredValue`、`useSyncExternalStore`、`useInsertionEffect`
6. **createRoot API**：替代 ReactDOM.render
7. **Strict Mode 行为变化**：mount-unmount-remount 不修改 UI

### 【Q750】React19 有哪些新特性
1. **React Compiler（React Forget）**：自动 memo，开发者不再需要手动 useMemo/useCallback
2. **Server Components（RSC）**：正式稳定，服务端组件
3. **Actions**：`useActionState` / `useFormStatus` / `useOptimistic`（表单 actions 支持）
4. **Document Metadata**：`<title>`、`<meta>` 等原生支持
5. **ref as prop**：ref 可像普通 prop 传递
6. **改进的错误报告**
7. Suspense 等进一步改进

# React

## 核心概念篇

1. **React的虚拟DOM是什么？它有什么优势？** **参考答案：** 虚拟 DOM（Virtual DOM）本质上是使用 JavaScript 对象来描述真实 DOM 结构的轻量级抽象表示。它的核心优势在于：① 减少昂贵的真实 DOM 操作，通过 JS 层面的计算找出最小差异后再更新视图；② 保证跨平台能力，因为它是纯 JS 对象，除了渲染到浏览器 DOM，还可以映射到 Native、Canvas 等环境（如 React Native）；③ 提升开发体验，让开发者只需关注状态变化，无需手动维护复杂的 UI 更新逻辑。
    
2. **React的diff算法是如何工作的？** **参考答案：** React 的 Diff 算法是一种时间复杂度为 O(n) 的启发式算法，基于三个核心策略：① 同层比较（Tree Diff）：只对比同一层级的节点，忽略跨层级移动，若节点跨层则直接销毁重建；② 类型检查（Component Diff）：如果新旧节点类型不同，React 会判定为完全不同的树，直接销毁旧节点并创建新节点；③ Key 标识（Element Diff）：对于同级列表节点，通过 key 来判断节点是否仅仅是位置发生变化，从而实现节点的精准复用与移动。
    
3. **React的合成事件是什么？为什么要使用合成事件？** **参考答案：** 合成事件（SyntheticEvent）是 React 自己实现的一套事件系统，它是对浏览器原生事件的跨浏览器兼容封装。使用它的原因主要有三点：① 性能优化：利用事件委托机制，将事件统一绑定在根容器上，大幅减少内存占用和监听器数量；② 抹平浏览器差异：提供统一的 API 接口，解决不同浏览器下事件对象的兼容性问题；③ 更好的跨端能力：脱离底层 DOM 依赖，使得 React 逻辑更容易移植到 React Native 等非浏览器环境。
    
4. **React的setState是同步还是异步的？为什么？** **参考答案：** `setState` 本身并不是一个异步 API，而是 React 的状态更新表现为“调度式”的异步行为。这是因为 React 为了实现性能优化，采用了批处理（Batching）机制。当调用 `setState` 时，React 不会立即修改状态并重新渲染，而是将更新任务放入队列中，在合适的时机（如微任务阶段或事务结束时）统一处理。这种设计避免了频繁触发重渲染导致的布局抖动（Layout Thrashing）。
    
5. **React的Fiber架构解决了什么问题？** **参考答案：** Fiber 架构主要解决了复杂应用下的主线程阻塞问题。在 React 15 及之前的 Stack Reconciler 中，渲染是同步且不可中断的递归过程，大组件树会导致页面假死。Fiber 架构将渲染任务拆分为一个个小的工作单元（Fiber 节点），利用链表结构替代递归调用栈，实现了可中断、可恢复、带优先级的增量渲染，从而赋予了 React 真正的并发能力，确保高优先级交互（如用户输入）不被低优先级任务阻塞。
    
6. **React的 reconciliation 过程是怎样的？** **参考答案：** Reconciliation（协调）是 React 用于更新 UI 的核心算法过程。当组件状态或属性改变时，React 会生成新的 Virtual DOM 树，并与旧的树进行对比。协调过程遵循深度优先遍历，首先判断根节点类型是否相同，若不同则完全替换子树；若相同则保留 DOM 节点，仅更新变化的属性，并递归比对子节点。最终计算出最小化 DOM 操作的补丁（Patch），并在 Commit 阶段应用到真实 DOM 上。
    
7. **React的key属性有什么作用？** **参考答案：** `key` 是 React 识别列表项唯一性的核心标识，帮助 Diff 算法精准匹配新旧列表中的同一个节点。其作用是实现节点复用，避免无效的 DOM 销毁和重建，从而大幅提升列表增删、排序时的性能。同时，稳定的 key 还能防止包含本地状态的组件（如输入框）在列表变动时发生状态错位。注意，key 仅在 React 内部使用，不会作为 props 传递给组件。
    
8. **React的批处理更新机制是如何实现的？** **参考答案：** React 内部维护了一个更新队列（Update Queue）。当触发状态更新时，更新请求会被暂存到队列中，而不是立即执行。在 React 18 之前，批处理仅限于 React 合成事件和生命周期中；而在 React 18 引入 Automatic Batching 后，无论是 `setTimeout`、`Promise` 还是原生事件中的多次 `setState`，都会被自动收集并在微任务阶段统一处理，最终只触发一次重渲染，极大提升了性能。
    
9. **React的并发模式（Concurrent Mode）是什么？** **参考答案：** 并发模式是 React 18 引入的新特性，它允许 React 在渲染过程中中断工作，优先响应用户输入。其核心是基于 Fiber 架构的时间切片（Time Slicing）技术，将大型渲染任务拆分为多个小片。如果在执行过程中检测到更高优先级的任务（如点击、按键），React 会暂停当前渲染，让出主线程控制权，待空闲时再恢复，从而构建出高度响应式的用户界面。
    
10. **React的优先级调度是如何实现的？** **参考答案：** React 采用 Lane（车道）模型来实现优先级调度。Lane 使用 32 位二进制变量（位掩码）来表示不同的任务优先级，通过高效的位运算来判断和管理优先级。调度器（Scheduler）会根据任务的 Lane 将其分配到不同的优先级通道（如 SyncLane 代表同步高优先级，DefaultLane 代表普通优先级）。高优先级任务可以打断低优先级任务，相同优先级的任务则会被合并批量处理。
    

## 源码实现篇

11. **React.createElement的实现原理是什么？** **参考答案：** `React.createElement` 是 JSX 编译后的核心函数。它接收元素类型（type）、配置对象（config，包含 key、ref 和 props）以及子元素（children）作为参数。其内部逻辑主要是处理这些参数，构建并返回一个普通的 JavaScript 对象（即 ReactElement）。该对象包含 `$$typeof`（用于防御 XSS 攻击的安全标识）、`type`、`key`、`ref` 和 `props` 等核心属性，用于后续生成虚拟 DOM。
    
12. **React.render的内部实现流程是怎样的？** **参考答案：** 以 React 18 的 `createRoot().render()` 为例，其内部流程主要分为：① 创建 Fiber Root 和 Host Root 节点；② 将传入的 React Element 封装为更新任务（Update），加入更新队列；③ 触发调度器（Scheduler）开始工作；④ 进入 Render 阶段，构建 WorkInProgress 树并进行 Diff；⑤ 进入 Commit 阶段，将副作用同步应用到真实 DOM；⑥ 执行 useEffect 等异步副作用。
    
13. **Fiber节点的结构是怎样的？包含哪些关键属性？** **参考答案：** Fiber 节点是一个 JS 对象，核心属性包括：① 静态数据结构：`type`（组件类型）、`key`、`tag`（组件类型标识）；② 链表指针：`child`（第一个子节点）、`sibling`（下一个兄弟节点）、`return`（父节点）；③ 状态与属性：`memoizedState`（Hook 链表状态）、`memoizedProps`、`pendingProps`；④ 更新相关：`updateQueue`（更新队列）、`lanes`（优先级）；⑤ 双缓冲：`alternate`（指向另一棵树的对应节点）。
    
14. **React的调度器（Scheduler）是如何工作的？** **参考答案：** Scheduler 是 React 的调度中心，核心职责是管理任务队列和执行时间切片。它利用 `MessageChannel` 实现异步宏任务调度。在执行任务时，Scheduler 会开启一个 `while` 循环（workLoop），每处理完一个工作单元就检查当前时间片（默认约 5ms）是否耗尽。如果超时，则主动让出主线程（yield），等待浏览器空闲时再继续执行下一个切片，从而实现可中断渲染。
    
15. **React的渲染器（Renderer）是如何与Fiber协调的？** **参考答案：** Renderer（如 react-dom）负责将 Fiber 节点转换为特定平台的实际视图。在协调过程中，Renderer 提供了宿主配置（Host Config），定义了如何创建、更新、删除节点以及提交副作用。Fiber 协调器在 Render 阶段只进行内存中的 Diff 计算并生成 Effect List，随后交由 Renderer 在 Commit 阶段执行真实的 DOM 操作，实现了核心逻辑与平台渲染的解耦。
    
16. **React的commit阶段具体做了哪些事情？** **参考答案：** Commit 阶段是不可中断的同步过程，主要分为三个子阶段：① Before Mutation：读取 DOM 状态（如执行 getSnapshotBeforeUpdate）；② Mutation：执行真实的 DOM 增删改操作，卸载旧节点，插入新节点；③ Layout：执行 DOM 相关的生命周期和 Hook（如 useLayoutEffect、componentDidMount/Update）。最后还会异步调度 useEffect 的执行。
    
17. **React的reconciliation阶段是如何遍历Fiber树的？** **参考答案：** 协调阶段放弃了传统的递归遍历，改用基于链表的循环遍历。从根节点开始，通过 `child` 指针向下深入，处理完当前节点后通过 `sibling` 指针向右平移，如果没有兄弟节点则通过 `return` 指针向上回溯。这种深度优先的链表遍历方式使得遍历过程可以随时记录当前进度，从而实现任务的暂停与恢复。
    
18. **React的workLoop是如何实现的？** **参考答案：** `workLoop` 是 Fiber 调度的核心执行循环。在并发模式下，其伪代码逻辑为：`while (workInProgress !== null && !shouldYieldToHost()) { workInProgress = performUnitOfWork(workInProgress); }`。它不断取出当前的工作单元进行处理，并在每次处理后检查是否需要让出主线程。如果时间片用完或存在更高优先级任务，循环就会退出，将控制权交还给浏览器。
    
19. **React的lane模型是什么？如何表示优先级？** **参考答案：** Lane 模型是 React 17 引入的优先级管理系统，取代了早期的 expirationTime。它使用 32 位二进制数（位掩码）来表示优先级，每一位代表一个“车道”。例如，`SyncLane` 是最高优先级（最右侧的位），`DefaultLane` 是常规优先级。通过按位与（&）等位运算，React 能够极其高效地判断两个更新的优先级关系、合并相同优先级的任务，以及提取最高优先级任务。
    
20. **React的expirationTime机制是如何计算的？** **参考答案：** `expirationTime` 是 React 16 引入但在 17/18 中被 Lane 模型取代的旧机制。它的计算公式大致为：`currentTime + timeout`。其中 `timeout` 根据任务优先级决定（如用户交互为 0，普通数据请求为 5000ms）。通过比较过期时间与当前时间，React 判断任务是否已经超时，超时任务会被赋予更高优先级立即执行。由于其在批量处理和优先级合并时存在精度和计算缺陷，最终被更优雅的 Lane 模型替代。
    

## 性能优化篇

21. **React.memo的工作原理是什么？** **参考答案：** `React.memo` 是一个高阶组件，用于缓存组件的渲染结果。它在内部对传入的 props 进行浅比较（Shallow Compare），如果新旧 props 完全相同，则跳过当前组件的重渲染，直接复用上一次的渲染结果。这可以有效避免父组件更新导致的不必要的子组件重渲染，但需注意如果 props 包含引用类型且未做稳定化处理，可能会导致 memo 失效。
    
22. **useMemo和useCallback的区别和实现原理？** **参考答案：** 两者都用于缓存以避免不必要的重复计算或渲染。`useMemo` 缓存的是**计算结果的值**，只有当依赖项变化时才重新执行工厂函数；`useCallback` 缓存的是**函数的引用**，等价于 `useMemo(() => fn, deps)`。它们的底层实现都是依附于 Fiber 节点的 Hook 链表，通过对比依赖数组来决定是返回缓存值还是重新计算。
    
23. **React的lazy和Suspense是如何实现的？** **参考答案：** `React.lazy` 接收一个返回 Promise 的动态 import 函数，在渲染时会创建一个特殊的 Lazy 组件。当首次渲染该组件时，React 会捕获抛出的 Promise，并向上寻找最近的 `Suspense` 边界，暂时渲染其 `fallback` UI。当 Promise resolve 后，React 会重新触发渲染，加载并渲染真正的组件。结合并发模式，Suspense 还能实现流式 SSR 和选择性注水。
    
24. **如何实现React的shouldComponentUpdate？** **参考答案：** `shouldComponentUpdate(nextProps, nextState)` 是 Class 组件的生命周期方法，在渲染前被调用。开发者可以通过自定义逻辑对比新旧 state 和 props，返回 true 则继续渲染，返回 false 则跳过更新。在现代 React 中，通常推荐使用函数组件配合 `React.memo` 来实现相同的性能优化目的，或者通过 `useMemo/useCallback` 细粒度控制。
    
25. **React的Profiler API是如何收集性能数据的？** **参考答案：** `<Profiler>` 组件包裹需要测量的组件树，它接收 `onRender` 回调。每当包裹内的组件提交更新时，React 会将渲染耗时（包括 Render 阶段和 Commit 阶段的耗时）、触发更新的原因（如 setState、props change）等指标传递给该回调。这些数据可用于定位性能瓶颈，但 Profiler 仅在开发环境或显式启用的生产构建中生效。
    
26. **React的并发模式如何帮助性能优化？** **参考答案：** 并发模式通过将渲染任务分片和赋予优先级来优化性能。它允许 React 准备多个版本的 UI，并将非紧急更新（如大数据列表过滤）降级为 Transition。当用户进行紧急交互时，React 可以中断低优先级渲染，确保输入框不卡顿。此外，结合 `useDeferredValue` 和 `startTransition`，可以将重型计算延后到空闲期执行，彻底解决长任务阻塞主线程的问题。
    
27. **React的hydration过程是什么？** **参考答案：** Hydration（注水）是 SSR（服务端渲染）专属的过程。客户端加载 HTML 后，React 会复用服务端生成的真实 DOM 节点，而不是重新创建。React 会遍历服务端生成的 DOM 和客户端生成的 Virtual DOM，将事件监听器绑定到现有 DOM 上，并激活组件状态。如果两者结构不一致，React 会放弃复用并回退到客户端全量渲染。
    
28. **React的代码分割是如何实现的？** **参考答案：** 代码分割主要通过动态 `import()` 语法和 `React.lazy` 实现。打包工具（如 Webpack/Vite）会将动态导入的模块拆分为独立的 Chunk 文件。在运行时，当路由切换或条件满足触发懒加载组件时，浏览器才会去请求对应的 JS 文件。配合 Suspense 展示 Loading 状态，可以显著减小首屏包体积，加快初始加载速度。
    
29. **React的并发渲染如何避免卡顿？** **参考答案：** 并发渲染通过“时间切片”机制避免卡顿。浏览器通常以 60fps（每帧约 16.6ms）刷新屏幕，React 将渲染工作切分为小于 5ms 的小块。每完成一块，React 都会检查是否即将超出帧预算，如果是，则主动让出主线程，把控制权交还给浏览器去处理用户输入和绘制动画，从而保证界面的流畅响应。
    
30. **React的优先级中断机制是如何工作的？** **参考答案：** 当中断发生时，React 的调度器会停止执行当前的 `workLoop`。此时，正在处理的 WorkInProgress 树会被保留在内存中，不会被丢弃。当浏览器空闲或高优先级任务处理完毕后，调度器会恢复 `workLoop`，从上次中断的 Fiber 节点继续向下遍历和处理。这种机制确保了低优先级任务不会饿死，也不会阻塞高优先级交互。
    

## Hooks机制篇

31. **useState的实现原理是什么？** **参考答案：** `useState` 的底层依赖于 Fiber 节点上的单向链表结构。首次渲染时，React 会创建一个 Hook 对象（包含 `memoizedState` 和 `queue`），并将其挂载到当前 Fiber 的 `memoizedState` 链表上。调用 `setState` 时，会将更新动作推入队列并触发调度。再次渲染时，React 会根据 Hook 的调用顺序从链表中恢复对应的状态，并计算新的 state 值。
    
32. **useEffect的执行时机和清理机制？** **参考答案：** `useEffect` 是在 Commit 阶段之后**异步执行**的，不会阻塞浏览器绘制。它的执行时机是在浏览器完成布局和绘制之后。清理机制方面，React 会在执行新的 Effect 之前，先同步执行上一次 Effect 返回的清理函数（Cleanup Function）；在组件卸载时，也会执行最后一次清理函数，以防止内存泄漏。
    
33. **useLayoutEffect和useEffect的区别？** **参考答案：** 核心区别在于执行时机。`useLayoutEffect` 在 DOM 变更后、浏览器绘制前**同步执行**，因此它会阻塞页面渲染，适合用于测量 DOM 尺寸或在绘制前同步修改 DOM 以避免闪烁。而 `useEffect` 是异步执行的，不阻塞绘制，适合用于数据请求、订阅等不需要立即同步修改 DOM 的副作用。
    
34. **useReducer的实现原理？** **参考答案：** `useReducer` 适用于复杂的状态逻辑。它的底层实现与 `useState` 类似，也是存储在 Fiber 的 Hook 链表中。区别在于它的更新队列（queue）存储的是 action 而不是直接的 state。当 dispatch 一个 action 时，React 会在下一次渲染时，使用传入的 reducer 函数结合当前的 state 和 action 计算出新的 state。
    
35. **useContext的实现机制？** **参考答案：** `useContext` 接收一个 Context 对象并返回当前的 Context 值。其底层原理是：当组件调用 `useContext` 时，React 会沿着当前 Fiber 树的 `return` 指针向上查找，直到找到匹配的 Context Provider 节点，读取其 `_currentValue`。如果 Provider 的值发生变化，所有消费该 Context 的子组件都会被标记为需要更新。
    
36. **自定义Hooks的实现原理？** **参考答案：** 自定义 Hooks 本质上只是普通的 JavaScript 函数，其命名必须以 `use` 开头。它没有特殊的底层魔法，之所以能工作，是因为它内部调用了内置 Hooks（如 useState、useEffect）。由于每次渲染都会重新执行函数组件，自定义 Hooks 内的内置 Hooks 依然遵循严格的调用顺序和 Fiber 链表绑定规则，从而实现逻辑的复用。
    
37. **Hooks的调用顺序为什么必须一致？** **参考答案：** 因为 React 依赖 Hooks 的**调用顺序**来匹配状态。在 Fiber 节点上，所有的 Hooks 是通过单向链表连接的。React 在更新时，按照代码从上到下的执行顺序，依次从链表中取出对应的 Hook 节点。如果在条件语句或循环中使用 Hooks，会导致某次渲染时跳过了某个 Hook，后续的 Hook 就会错误地关联到错误的状态，引发严重 Bug。
    
38. **Hooks是如何存储在Fiber节点中的？** **参考答案：** Hooks 存储在 Fiber 节点的 `memoizedState` 属性上。对于函数组件，`memoizedState` 指向一个单向链表，链表的每个节点代表一个 Hook。每个 Hook 节点包含 `memoizedState`（当前状态值）、`queue`（更新队列）、`next`（指向下一个 Hook）等属性。这种链表结构使得 React 能够通过顺序遍历精确恢复每一个 Hook 的状态。
    
39. **useRef的实现原理和用途？** **参考答案：** `useRef` 返回一个包含 `current` 属性的普通 JS 对象 `{ current: initialValue }`。其底层实现非常简单：在首次渲染时创建一个普通对象挂在 Hook 链表上，后续渲染直接从链表中取出该对象返回，因此它的引用在整个组件生命周期内保持不变。常用于获取 DOM 引用、保存定时器 ID 或存储任何不需要触发重渲染的可变值。
    
40. **useImperativeHandle的作用和实现？** **参考答案：** `useImperativeHandle` 通常与 `forwardRef` 配合使用，用于自定义暴露给父组件的 ref 实例。它的实现原理是在 Commit 阶段（Layout 子阶段），将传入的工厂函数返回值赋给 ref 对象的 `current` 属性。这样父组件通过 ref 调用方法时，实际上调用的是我们自定义暴露的方法，而不是底层的 DOM 节点，实现了更好的封装性。
    

## 高级特性篇

41. **React的context机制是如何实现的？** **参考答案：** Context 的实现依赖于 Fiber 树的上下文传播机制。Provider 组件在渲染时，会创建一个 Context 对象并挂载到自身的 Fiber 节点上。当 Consumer（或 useContext）所在的组件更新时，React 会沿着 `return` 链向上遍历，检查路径上是否存在匹配的 Provider。如果 Provider 的值发生改变，React 会强制触发所有消费者的重渲染，绕过常规的 memo 优化。
    
42. **React的错误边界（Error Boundary）是如何工作的？** **参考答案：** 错误边界目前只能通过 Class 组件的 `componentDidCatch` 和 `getDerivedStateFromError` 生命周期实现。当子组件树在渲染、生命周期或构造函数中抛出 JS 错误时，React 会冒泡查找最近的 Error Boundary。找到后，React 会调用其生命周期更新状态以渲染 Fallback UI，并阻止错误导致整个应用崩溃。注意它无法捕获事件处理和异步代码中的错误。
    
43. **React的portal是如何实现的？** **参考答案：** Portal 提供了一种将子节点渲染到存在于父组件以外的 DOM 节点的能力。其底层实现是在 Fiber 树中创建一个特殊的 `HostPortal` 类型的节点。这个节点虽然逻辑上属于当前的组件树，但在 Commit 阶段，Renderer 会将其子节点挂载到指定的外部 DOM 容器中，而不是默认的父 DOM 节点下，常用于实现模态框、Tooltip 等需要突破 CSS 层叠上下文的场景。
    
44. **React的并发模式下的自动批处理？** **参考答案：** 在并发模式下，React 18 实现了 Automatic Batching。无论更新发生在同步代码、`setTimeout`、`Promise.then` 还是原生事件中，React 都会将这些更新收集起来，默认在微任务阶段统一处理。这意味着连续多次 `setState` 只会触发一次重渲染。如果需要强制同步更新，可以使用 `flushSync`，但这通常会损害并发性能。
    
45. **React的transition API是如何实现的？** **参考答案：** Transition API（如 `startTransition` 和 `useTransition`）允许开发者将某些更新标记为“非紧急的过渡更新”。其底层实现是为这些更新分配一个特殊的低优先级 Lane（如 `TransitionLane`）。当高优先级更新（如用户输入）到来时，调度器可以中断 Transition 渲染。`useTransition` 还会返回一个 `isPending` 状态，方便开发者在后台准备新 UI 时展示过渡指示器。
    
46. **React的server components原理？** **参考答案：** React Server Components (RSC) 允许组件在服务端运行并直接访问数据库或文件系统。它们在构建或服务端请求时被渲染，输出一种特殊的、紧凑的序列化格式（RSC Payload），而不是 HTML 字符串。客户端接收到 Payload 后，React 会将其与客户端组件树融合，按需 hydrate。RSC 不包含业务逻辑到客户端包中，极大减小了 JS 体积。
    
47. **React的streaming SSR是如何工作的？** **参考答案：** Streaming SSR 结合了 Suspense 和服务端渲染。服务端不再等待所有数据准备好才发送 HTML，而是先发送带有 Suspense fallback 的外壳 HTML。当某个 Suspense 边界内的数据准备好后，服务端会通过流（Stream）发送该部分的真实 HTML 和一个内联脚本，客户端接收到后无缝替换掉 fallback 内容。这实现了更快的首屏响应（FCP）。
    
48. **React的hydration with Suspense？** **参考答案：** 传统 SSR 的 hydration 是自上而下同步进行的，一旦遇到慢组件就会阻塞整个页面的交互。结合 Suspense 的 Selective Hydration（选择性注水）允许 React 优先 hydrate 用户正在交互的部分或视口内的部分。未被注水的 Suspense 边界会保持服务端生成的静态 HTML，直到 React 在空闲时或用户交互时才对其进行注水，大幅提升了 TTI（可交互时间）。
    
49. **React的并发渲染中的优先级继承？** **参考答案：** 优先级继承是指当一个低优先级的更新（如 Transition）阻塞了高优先级更新所需的资源或路径时，React 会临时提升该低优先级任务的 Lane，使其以高优先级执行，防止“饥饿”现象。在 React 的 Lane 模型中，这通常体现在调度器在处理更新队列时，对相互依赖的任务进行优先级对齐，确保紧急任务不会因为排在长任务后面而被无限期推迟。
    
50. **React的并发模式下的状态重置机制？** **参考答案：** 在并发模式下，如果一个正在渲染的低优先级任务被高优先级任务打断，并且高优先级任务导致了该组件的卸载或关键 props 改变，React 可能会直接丢弃（Abort）之前已完成的低优先级 WorkInProgress 树。当下次再恢复或重新触发该组件的渲染时，由于之前的中间状态已被废弃，组件会从最新的 props/state 重新开始渲染，这就是并发模式下的状态重置与防抖机制。