# React
## 核心概念篇

1. **React的虚拟DOM是什么？它有什么优势？**
2. **React的diff算法是如何工作的？**
3. **React的合成事件是什么？为什么要使用合成事件？**
4. **React的setState是同步还是异步的？为什么？**
5. **React的Fiber架构解决了什么问题？**
6. **React的 reconciliation 过程是怎样的？**
7. **React的key属性有什么作用？**
8. **React的批处理更新机制是如何实现的？**
9. **React的并发模式（Concurrent Mode）是什么？**
10. **React的优先级调度是如何实现的？**

## 源码实现篇

11. **React.createElement的实现原理是什么？**
12. **React.render的内部实现流程是怎样的？**
13. **Fiber节点的结构是怎样的？包含哪些关键属性？**
14. **React的调度器（Scheduler）是如何工作的？**
15. **React的渲染器（Renderer）是如何与Fiber协调的？**
16. **React的commit阶段具体做了哪些事情？**
17. **React的reconciliation阶段是如何遍历Fiber树的？**
18. **React的workLoop是如何实现的？**
19. **React的lane模型是什么？如何表示优先级？**
20. **React的expirationTime机制是如何计算的？**

## 性能优化篇

21. **React.memo的工作原理是什么？**
22. **useMemo和useCallback的区别和实现原理？**
23. **React的lazy和Suspense是如何实现的？**
24. **如何实现React的shouldComponentUpdate？**
25. **React的Profiler API是如何收集性能数据的？**
26. **React的并发模式如何帮助性能优化？**
27. **React的hydration过程是什么？**
28. **React的代码分割是如何实现的？**
29. **React的并发渲染如何避免卡顿？**
30. **React的优先级中断机制是如何工作的？**

## Hooks机制篇

31. **useState的实现原理是什么？**
32. **useEffect的执行时机和清理机制？**
33. **useLayoutEffect和useEffect的区别？**
34. **useReducer的实现原理？**
35. **useContext的实现机制？**
36. **自定义Hooks的实现原理？**
37. **Hooks的调用顺序为什么必须一致？**
38. **Hooks是如何存储在Fiber节点中的？**
39. **useRef的实现原理和用途？**
40. **useImperativeHandle的作用和实现？**

## 高级特性篇

41. **React的context机制是如何实现的？**
42. **React的错误边界（Error Boundary）是如何工作的？**
43. **React的portal是如何实现的？**
44. **React的并发模式下的自动批处理？**
45. **React的transition API是如何实现的？**
46. **React的server components原理？**
47. **React的streaming SSR是如何工作的？**
48. **React的hydration with Suspense？**
49. **React的并发渲染中的优先级继承？**
50. **React的并发模式下的状态重置机制？**

---

## 题目解析要点

### 核心概念解析要点

- 虚拟DOM：JavaScript对象表示DOM结构，减少直接DOM操作
- Diff算法：分层比较，key优化，tree diff、component diff、element diff
- 合成事件：跨浏览器兼容，事件委托，性能优化
- setState异步：批量更新，性能优化，事务机制
- Fiber架构：可中断渲染，优先级调度，增量渲染

### 源码实现解析要点

- createElement：创建React元素对象
- Fiber节点：包含child、sibling、return指针
- 调度器：requestIdleCallback，优先级队列
- commit阶段：DOM操作，生命周期调用，ref处理
- Lane模型：位运算表示优先级，优先级压缩

### Hooks解析要点

- useState：基于Fiber的memoizedState链表
- useEffect：commit阶段执行，异步调度
- 调用顺序：链表遍历依赖调用顺序一致性
- 存储位置：Fiber节点的memoizedState属性

### 并发模式解析要点

- 可中断渲染：浏览器空闲时执行
- 优先级调度：高优先级任务中断低优先级
- 自动批处理：多个状态更新合并为一次渲染
- Suspense：组件加载状态管理

---

*注：这些题目涵盖了React的核心原理和最新特性，建议结合源码阅读和实际项目经验深入理解每个问题的底层实现机制。*

