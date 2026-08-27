# 00 React 深入学习路线
> Last Format Time：8/27/2026 15:20:25

> Last Format Time：8/27/2026
> Status：进行中

这组笔记按“组件设计 → 渲染传播 → 外部状态一致性 → 并发特性 → React 内部机制 → Mini React 实现”的依赖关系组织。当前已完成 React 并发特性主干，并进入 Fiber、Scheduler、Reconciliation、render/commit phase 的内部机制学习。

---
## 阅读导航
### 01｜组件架构与 API 设计
目标：掌握复杂组件的结构拆分、状态所有权、可访问性和多态 API。

- [[01 Compound Components 与受控模式]]：Compound Components 与 Controlled / Uncontrolled
- [[02 Tabs 组件库实现]]：Tabs 组件的完整职责拆分与交互实现
- [[03 Roving Tabindex 参考]]：Roving Tabindex 与 Tabs 可访问性规则
- [[04 稳定回调与 useControllableState]]：稳定回调、受控状态与非受控状态
- [[01 Slot 与 asChild 实现]]：Slot / `asChild` 的 props 合并与事件处理
- [[02 多态组件的语义与行为]]：多态组件的语义、类型与运行时行为

### 02｜渲染与性能诊断
目标：理解 render 的来源、Context 更新传播和性能问题的定位方法。

- [[01 Context 更新传播与拆分]]：Context 传播链路、拆分策略与重渲染边界
- 待补：React Profiler、`memo` / memoization、列表虚拟化、状态上提与下沉

### 03｜External Store 与并发一致性
目标：理解细粒度订阅、快照协议、selector 和 tearing 的关系。

- [[01 从 Context 到 Selector Store]]：从 Context 逐步演进到 Selector Store
- [[02 useSyncExternalStore、Selector 与并发一致性]]：`useSyncExternalStore`、selector、snapshot、tearing 与 Zustand

### 04｜React 并发特性
目标：理解非紧急更新、延迟值、Suspense 和 pending UI 的整体协作。

- [[01 Transition、useDeferredValue 与响应性]]：Transition、`useTransition` 与 `useDeferredValue`
- [[02 Suspense、Transition 与 Suspense、并发 UI 整体]]：Suspense、Transition、retry、reveal 与并发 UI

### 05｜React 内部机制
目标：把外部行为映射到 Fiber、Update Queue、Lanes、Scheduler、Reconciliation 和 Commit。

- [[01 Concurrent Rendering → Fiber → Update Queue → Lanes]]：Concurrent Rendering、Fiber、Update Queue 与 Lanes
- [[02 Scheduler 串联]]：Scheduler、cooperative scheduling、pause / resume / abandon
- [[03 reconciliation 与 key]]：`type + key` identity、列表 diff、复用、移动与删除
- [[04 React render phase 与 commit phase]]：render / commit、flags、completeWork、DOM mutation 与 Effects

### 06｜Mini React
目标：用最小实现验证 React 的核心模型。

- 待开始：`createElement`、DOM render、reconciliation、`useState`、Fiber、简化 Scheduler

---
## 当前进度
| 模块 | 进度 | 当前状态 | 主要产出 |
|---|---:|---|---|
| 组件架构与 API 设计 | 100% | 核心主题完成 | Tabs、受控/非受控、Slot、`asChild`、Roving Tabindex、多态组件 |
| 渲染与性能诊断 | 30% | 基础完成 | 已完成 Context 更新传播与拆分；诊断工具和列表性能待补 |
| External Store | 100% | 核心主题完成 | Selector Store、`useSyncExternalStore`、snapshot、tearing、Zustand |
| React 并发特性 | 100% | 当前阶段完成 | Transition、`useDeferredValue`、Suspense、retry、reveal、pending UI |
| React 内部机制 | 75% | 主干已打通 | Fiber、current / WIP、Update Queue、Lanes、Scheduler 基础、Reconciliation、render / commit |
| Mini React | 0% | 尚未开始 | 等内部机制主干稳定后，用代码实现并验证 |

> 当前判断：知识主干已从“并发特性”推进到“React 内部机制”。内部机制目前还需要深化 Scheduler 与 React Reconciler 的交界，并补充源码级 commit 细节。

---
## 已完成的学习链路
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
Scheduler 基础
↓
Reconciliation / key / Placement
↓
render phase / commit phase / Effects
```

---
## 下一步
1. **深化 Scheduler 与 Reconciler 的交界**：`pendingLanes`、`getNextLanes`、root scheduling、sync / concurrent work loop、`shouldYield`、resume / restart。
2. **补齐性能诊断**：使用 Profiler、`memo`、列表虚拟化和状态位置对比，形成可复现实验。
3. **补源码级 commit 细节**：Placement 如何寻找 Host parent / sibling、Deletion subtree、refs、Effect 链表和 passive effect flush。
4. **启动 Mini React**：先实现 `createElement` 和 DOM render，再逐步加入 reconciliation、`useState`、Fiber 与简化 Scheduler。

---
## 整理说明
- 保留原有目录结构，没有创建空的占位文档。
- 现有 Markdown 笔记共 **15 篇**，按 6 个学习模块归档。
- 各笔记保留原有正文和审核记录；本轮主要统一标题入口、笔记说明、路线索引和进度描述。
- `02 Suspense、Transition 与 Suspense、并发 UI 整体.md` 文件名沿用原名，避免破坏已有 Obsidian 双链。

---
## 内容审核变更记录
### CR-001｜顺序调整
- 日期：8/25/2026
- 位置：全文学习路线
- 原内容：按组件架构、性能、并发、External Store、内部机制、Mini React 罗列主题。
- 调整后：按组件架构、渲染与性能、External Store、并发特性、内部机制、Mini React 的依赖顺序组织。
- 原因：External Store 的 snapshot、tearing 和 render/commit 区分是理解并发特性的直接前置知识。
- 依据：现有笔记之间的知识依赖关系（顺序整理）

### CR-002｜进度更新
- 日期：8/25/2026
- 位置：`当前进度` 表格及其后说明
- 原内容：并发特性为“尚未开始”，其余方向以字符进度条记录。
- 调整后：并发特性更新为第一阶段完成，并明确 Suspense 的学习状态。
- 原因：目录中已存在 Transition 与 `useDeferredValue` 相关笔记。
- 依据：[[01 Transition、useDeferredValue 与响应性]]

### CR-003｜目录索引
- 日期：8/25/2026
- 位置：`学习顺序` 各章节
- 原内容：路线仅列主题，没有指向已有笔记。
- 调整后：为已有主题建立双链，并将未创建的内容保留为待补清单。
- 原因：让路线同时承担学习顺序和目录索引职责，避免创建空占位文档。
- 依据：当前 `深入学习` 目录中的实际笔记

### CR-004｜当前进度重新核对
- 日期：8/27/2026
- 位置：`当前进度`、`下一步`、`整理说明`
- 原内容：Suspense、React 内部机制仍被标记为未开始，且现有笔记数量记录为 10 篇。
- 调整后：将 Suspense 标记为已完成，将 React 内部机制更新为 75%，并按实际目录修正为 15 篇笔记。
- 原因：目录中已经补充 Suspense、Fiber、Scheduler、Reconciliation、render/commit 等笔记。
- 依据：当前 `深入学习` 目录及各笔记末尾的学习进度说明

### CR-005｜描述格式统一
- 日期：8/27/2026
- 位置：各笔记标题入口与路线图
- 调整后：统一 `Last Format Time`、`笔记说明`、模块目标、当前状态和下一步的表达方式；修复内部机制笔记的标题入口与明显的伪标题格式。
- 原因：提升 Obsidian 大纲浏览、检索和复习时的可读性，同时保留正文内容。
- 依据：本目录内 Markdown 结构整理
