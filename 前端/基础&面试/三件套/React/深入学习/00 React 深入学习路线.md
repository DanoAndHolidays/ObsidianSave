# 00 React 深入学习路线
> Last Format Time：9/16/2026 19:24:51

> Last Format Time：2026-08-28
> Status：进行中
> 笔记说明：按依赖关系组织 React 深入学习资料，并区分学习覆盖与已验证能力。

---
## 学习目标
建立一条从组件 API 设计出发，经过渲染传播、外部状态一致性和并发特性，最终进入 Fiber / Scheduler / Reconciler 内部机制的 React 学习主线；最后用 Mini React 把抽象模型落到可运行代码。

> 本目录的“已完成”表示对应主题已有整理后的学习材料，不等同于已经通过独立练习、真实交付或面试答辩。能力判断遵循仓库 `maintain-frontend-profile` skill 的证据规则。

---
## 推荐学习路线
### 01｜组件架构与 API 设计
目标：掌握复杂组件的结构拆分、状态所有权、可访问性和多态 API。

- [[01 Compound Components：受控与非受控]]：复合组件与 Controlled / Uncontrolled 状态模型
- [[02 Tabs 组件库：职责与交互实现]]：Root、List、Trigger、Content 与交互职责
- [[03 Tabs 无障碍：Roving Tabindex]]：焦点移动、selection 与 ARIA Tabs Pattern
- [[04 稳定回调与 useControllableState]]：稳定回调与受控/非受控状态边界
- [[01 Slot 与 asChild：Props 合并与 Ref 传递]]：Slot、事件合并与 ref 传递
- [[02 多态组件：语义、类型与行为]]：语义 HTML、`as` API 与类型约束

### 02｜渲染与性能诊断
目标：理解 React 更新传播边界，并形成“定位 → 假设 → 修改 → Profiler 验证”的性能闭环。

- [[01 Context 更新传播：传播链路与拆分策略]]：Context 传播、value identity 与拆分
- [[02 React 渲染与性能诊断：Profiler 与优化闭环]]：Profiler、Ranked、Flamegraph、memo 与列表优化

### 03｜外部 Store 与并发一致性
目标：理解 Context、Selector Store 与 `useSyncExternalStore` 在订阅粒度和一致性上的差异。

- [[01 从 Context 到 Selector Store]]：从粗粒度订阅演进到细粒度订阅
- [[02 useSyncExternalStore：Selector、Snapshot 与 Tearing]]：snapshot、tearing、selector 与 Zustand

### 04｜React 并发特性
目标：理解更新优先级、响应性、Suspense 边界和 UI reveal 粒度。

- [[01 Transition 与 useDeferredValue：响应性]]：Transition、`useTransition` 与 `useDeferredValue`
- [[02 Suspense + Transition：Retry、Reveal 与并发 UI]]：Suspense、retry、reveal、fallback 与 pending UI

### 05｜React 内部机制
目标：把公开 API 映射到 Fiber 树、Update Queue、Lanes、Scheduler、Reconciliation 和 commit 工作。

1. [[01 Concurrent Rendering、Fiber、Update Queue 与 Lanes]]：先建立统一的 Fiber / Lane 心智模型
2. [[02 ⌚️ Hook 更新与并发工作循环]]：理解更新如何进入调度系统
3. [[05 Scheduler 与 Reconciler：并发渲染工作循环]]：串起 root scheduling、work loop 与 `shouldYield`
4. [[03 Reconciliation 与 Key：复用、移动与删除]]：理解 identity、state preservation 与 Placement / Deletion
5. [[04 Render Phase 与 Commit Phase]]：理解 finishedWork、flags、DOM mutation 与 Effects
6. [[06 Transition + Suspense：内部机制]]：用完整案例收束 Transition、Suspense、retry 与 restart

### 06｜Mini React（待开始）
目标：用最小实现验证 React 的核心模型。

建议顺序：`createElement` → DOM render → reconciliation → `useState` → Fiber → 简化 Scheduler。

---
## 当前进度
| 模块 | 资料覆盖 | 当前状态 | 下一项可验证产出 |
|---|---:|---|---|
| 组件架构与 API 设计 | 100% | 主题材料已完成 | 完成一次可访问 Tabs 组件的独立实现与答辩 |
| 渲染与性能诊断 | 60% | 基础材料已完成 | 用 Profiler 对一个列表或 Context 场景做前后对比 |
| 外部 Store 与并发一致性 | 100% | 核心主题材料已完成 | 独立解释 snapshot、tearing 与 selector 的关系 |
| React 并发特性 | 100% | 核心主题材料已完成 | 解释 Transition + Suspense 的 fallback / reveal 取舍 |
| React 内部机制 | 100% | 主干材料已完成，仍需独立验证 | 画出一次更新从 setState 到 commit 的完整链路 |
| Mini React | 0% | 尚未开始 | 完成 `createElement` 和 DOM render 的最小版本 |

> 目前目录共有 **18 篇主题笔记**（不含本路线文档）。这里的百分比表示资料覆盖度，不是能力等级；真实掌握仍需要代码、测试、答辩或现场接管等证据。

---
## 已完成的知识链路
```text
组件 API 设计
↓
Context 更新传播
↓
Selector Store / useSyncExternalStore
↓
Transition / useDeferredValue
↓
Suspense / retry / reveal
↓
Fiber / current / WIP
↓
Update Queue / Lanes
↓
Scheduler / root scheduling
↓
Reconciler work loop / shouldYield
↓
Reconciliation / key / Placement
↓
render phase / commit phase / Effects
```

---
## 下一步学习与验证
1. **性能诊断实战**：使用 Profiler、`memo`、列表虚拟化和状态位置对比，形成可复现实验。
2. **Scheduler 与 Reconciler 复述**：不看笔记画出 `pendingLanes → getNextLanes → Scheduler Task → workLoop → commitRoot`。
3. **源码级 commit 细节**：补齐 Placement 如何寻找 Host parent / sibling、Deletion subtree、refs、Effect 链表和 passive effect flush。
4. **启动 Mini React**：先实现 `createElement` 和 DOM render，再逐步加入 reconciliation、`useState`、Fiber 与简化 Scheduler。

---
## 整理说明
- 本轮按知识依赖重新命名文件和目录，目录编号表示推荐学习顺序。
- 清理聊天式开场、重复的 `Last Format Time`、多余 H1 和大小写不一致的标题；保留原有代码示例与正文推导。
- 将“资料覆盖”与“能力掌握”分开表达，避免把笔记数量或篇幅当成独立能力证据。
- 所有文件统一为“标题 → 元信息 → 分隔线 → 正文”的 Markdown 入口格式。
