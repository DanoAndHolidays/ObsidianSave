# Fiber
https://www.bilibili.com/video/BV1mCqEBxEBv/?spm_id_from=333.337.search-card.all.click&vd_source=47c9acd507be61251cd2bb730416395c
- 实现了增量渲染，避免了主线程的阻塞
- 实现了更新的优先级：
	- 最高：用户打字，点击
	- 中级：动画更新
	- 低级：网络请求
- 作为一个鸡架，为后续的特性铺平了道路，提供了更多的可能性
## React Fiber 的核心原理

React 16 引入的 **Fiber 架构**，核心目标是实现**可中断的异步渲染**，解决旧版栈调和（Stack Reconciler）在复杂页面中卡顿掉帧的问题。

这里实际上是用到了浏览器留的一个后门

### 一、旧架构的问题：同步不可中断

旧版 React 使用递归调用栈进行虚拟 DOM 比对（Reconciliation）。一旦开始渲染，就会**同步、递归**地处理整个组件树，直到完整计算完所有更新才能让出浏览器主线程。

如果组件树很深、更新频繁，这个“大任务”会长时间占用主线程，导致用户输入、动画等无法及时响应，产生明显的卡顿。

### 二、Fiber 的核心思想：任务拆分 + 可中断 + 优先级

Fiber 将渲染工作拆分成一个个**小的任务单元**，每个单元完成后可以主动让出主线程，让浏览器先处理更高优先级的任务（如用户点击、动画），之后恢复未完成的工作。

这需要解决三个问题：
1. 如何把递归遍历拆成可暂停的单元？
2. 如何知道什么时候该暂停/恢复？
3. 如何协调不同任务的优先级？

### 三、Fiber 节点的数据结构

每个 React 元素（组件、DOM 节点）都会对应一个 **Fiber 节点**。它是一个普通的 JavaScript 对象，记录了组件的类型、状态、副作用以及**链表结构**的连接关系。

```js
// 简化版 Fiber 节点
{
  // 节点类型（HostComponent, ClassComponent, FunctionComponent...）
  tag: WorkTag,
  // 关联的真实 DOM 或组件实例
  stateNode: ...,
  
  // 组件自身的状态（props, state, hooks）
  pendingProps: nextProps,
  memoizedProps: prevProps,
  memoizedState: prevState,
  
  // 链表连接
  return: parentFiber,      // 父节点
  child: firstChildFiber,   // 第一个子节点
  sibling: nextSiblingFiber,// 兄弟节点
  
  // 工作进度
  alternate: currentFiber,  // 双缓冲中指向另一棵树的对应节点
  
  // 副作用列表
  effectTag: 'Placement' | 'Update' | 'Deletion',
  nextEffect: nextEffectNode,
  
  // 调度优先级
  lanes: Lanes,  // React 17+ 使用 lane 模型替代 expirationTime
}
```

每个 Fiber 节点通过 `child`、`sibling`、`return` 形成一棵 **Fiber 树**。这种链表结构使得遍历可以随时暂停、恢复，而不必依赖函数调用栈。

### 四、双缓冲技术（Current & WorkInProgress）

React 内存中同时维护两棵 Fiber 树：
- **current 树**：当前屏幕上已经渲染的内容对应的 Fiber 树。
- **workInProgress 树**：正在内存中构建的新树，代表未来将要渲染的内容。

每次更新（setState、props 变化等）都会基于 current 树克隆出 workInProgress 树，然后在 workInProgress 树上进行协调计算。计算完成后，用 workInProgress 树直接替换 current 树（称为“提交”阶段）。这个过程类似图形学中的双缓冲，避免了 UI 出现不完整渲染。

Fiber 节点通过 `alternate` 属性指向自己在另一棵树中的对应节点，以便复用状态。

### 五、工作循环：中断与恢复

React 的调度与工作循环分布在两个主要阶段：**渲染阶段（Reconciliation Phase）** 和 **提交阶段（Commit Phase）**。

#### 1. 渲染阶段（可中断）

这个阶段负责找出哪些节点发生了改变（增、删、改），并为它们打上 `effectTag`。整个过程是**异步可中断**的。

核心代码逻辑（简化）：

```js
let nextUnitOfWork = rootFiber;   // 下一个待处理的 Fiber 节点

function workLoop(deadline) {
  // 是否应该暂停（让出主线程）
  let shouldYield = false;
  while (nextUnitOfWork && !shouldYield) {
    // 执行当前工作单元，并返回下一个工作单元
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
    // 检查剩余时间是否不足
    shouldYield = deadline.timeRemaining() < 1;
  }
  // 如果没有剩余工作单元，说明渲染阶段完成，可以进入提交阶段
  if (!nextUnitOfWork) {
    commitRoot();
  }
  // 否则继续请求下一帧执行
  requestIdleCallback(workLoop);
}

// 开始调度
requestIdleCallback(workLoop);
```

- `performUnitOfWork` 会处理当前 Fiber 节点（调用函数组件、协调子节点等），然后根据 `child` / `sibling` 返回下一个需要处理的节点。
- **时间切片**：React 使用 `requestIdleCallback`（polyfill 或用 `MessageChannel` 实现）来获取浏览器空闲时段。每个工作单元执行后检查剩余时间，不足则主动交还控制权。

#### 2. 提交阶段（同步不可中断）

当 `nextUnitOfWork === null` 表示所有 Fiber 节点处理完毕，此时进入提交阶段。提交阶段会遍历“副作用链表”（通过 `nextEffect` 连接所有需要更新的节点），一次性将 DOM 变更应用到真实 DOM 上。这个过程是**同步的**，保证 UI 最终状态一致。

### 六、优先级与调度

为了让高优先级任务（如动画、输入）能打断低优先级任务（如数据请求后的渲染），React 设计了**优先级模型**（React 17+ 使用 Lane 模型）。

- 每个更新任务被赋予一个 **lane**（二进制位，如 `SyncLane`、`InputContinuousLane`、`DefaultLane` 等）。
- 调度器会维护一个任务队列，每次循环时取出优先级最高的任务执行。
- 若高优先级任务出现，当前正在进行的低优先级工作会被中断，并且其 workInProgress 树会被丢弃；然后重新基于 current 树为高优先级任务克隆新的 workInProgress 树。

这个优先级机制让 React 可以“先响应用户，再慢慢算数据”。

### 七、完整的渲染流程示例

1. 调用 `setState` 产生一个更新，进入 **调度器**（Scheduler）。
2. 调度器根据优先级为该更新分配一个 lane，并放入任务队列。
3. 浏览器空闲时，调度器从队列中取出最高优先级任务，开始**渲染阶段**。
4. 构建 workInProgress 树：
   - 从 rootFiber 开始，调用 `performUnitOfWork` 深度优先遍历。
   - 遇到类组件调用其 render 方法；函数组件调用函数自身。
   - 对比 current 树上的旧 Fiber 与新的 React 元素，决定是复用、更新还是删除节点。
   - 每处理完一个节点，返回下一个待处理的节点（child 或 sibling）。
   - 每次检查剩余时间，不够则暂停循环，保存 `nextUnitOfWork` 等待下一帧继续。
5. 整个 workInProgress 树构建完成 → 所有变化以 `effectTag` 形式记录在 Fiber 的副作用链表中。
6. **提交阶段**：
   - 遍历副作用链表，对每个 Fiber 执行 DOM 操作（如 `appendChild`、`removeChild`、`setAttribute`）。
   - 触发生命周期（如 `componentDidMount`、`componentDidUpdate`）。
   - 将 workInProgress 树赋值给 `current` 树，以备下次更新复用。

### 八、与旧架构的对比

| 特性 | 旧版 Stack Reconciler | Fiber Reconciler |
|------|----------------------|------------------|
| 遍历方式 | 递归调用栈（不可中断） | 链表遍历（可中断、恢复） |
| 任务粒度 | 整个组件树作为一个任务 | 每个 Fiber 节点是独立工作单元 |
| 优先级 | 无，同步执行 | 支持任务优先级和抢占 |
| 渲染输出 | 全部同步更新 DOM | 分两阶段：可中断的渲染 + 同步提交 |
| 时间切片 | 不支持 | 支持，可避免长时间阻塞主线程 |

### 九、总结

React Fiber 本质上是一种**重新实现协调算法**的方式，通过**链表结构** + **时间切片** + **双缓冲** + **任务优先级**，把原来不可中断的递归更新打散成一个个可中断的小任务。这使得 React 应用在复杂交互和渲染之间能保持流畅，也为后续的 Concurrent Mode（并发模式）和 Suspense 等特性奠定了基础。