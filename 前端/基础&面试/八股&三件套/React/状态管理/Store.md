我比较熟悉的方案包括 Context、Zustand、Redux，以及原子化状态方案。

### Context

Context 适合传递低频变化的全局依赖，比如主题、当前用户、权限上下文或者页面级配置。

它的缺点是，如果 Context 的 value 发生变化，依赖这个 Context 的组件可能整体重新渲染。对于高频变化的列表、表单和筛选状态，不适合把所有状态都放在一个 Context 里。

### Zustand

Zustand 的优点是 API 简单、样板代码少，并且可以通过 selector 进行按需订阅。组件只订阅自己关心的字段，减少无关渲染。

在 Daedalus 项目中，我们把页面状态从组件内部抽离成 `Context + Zustand` 的页面级 Store，再通过 Slice 管理筛选、列表、弹窗和表单状态。这样可以减少 Props Drilling，也让不同组件之间的状态协作更清晰。

### Redux Toolkit

Redux 更适合大型团队、状态流转复杂、需要严格约束和完整 DevTools 追踪的场景。Redux Toolkit 已经减少了很多样板代码，但整体概念和约束仍然比 Zustand 更重。

如果团队非常重视统一的数据流、严格的 action/reducer 规范和时间旅行调试，我会考虑 Redux Toolkit。

### Jotai 或其他原子化方案

原子化方案适合把状态拆成很多相互独立的小单元，组件只订阅自己使用的 atom，粒度比较细。但是状态关系复杂时，需要团队建立比较清晰的组织方式，否则容易出现状态分散、不容易追踪的问题。

### 我的选择原则

我的选择通常是：

1. 能用组件本地状态解决，就不引入 Store；
2. 页面内多个组件共享，并且状态变化较频繁，优先考虑 Zustand；
3. 低频、稳定的依赖可以用 Context；
4. 服务端数据交给 TanStack Query 这类方案；
5. 大型团队且需要严格数据流和强审计能力时，考虑 Redux Toolkit。

### 总结成一句话

> 我不会因为项目用了 Zustand，就把所有状态都放进 Zustand。Store 的选择主要取决于状态的作用域、更新频率、团队协作成本和调试要求。