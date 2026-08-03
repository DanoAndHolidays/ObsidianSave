# 前端能力分类

使用稳定的 `id` 写入结构化画像。一个证据可以关联多个能力点，但必须说明它分别证明了什么。

| ID | 能力维度 | 核心范围 | React + TS 中大厂目标 |
|---|---|---|---|
| `html-semantics` | HTML 与语义化 | 语义标签、表单、SEO 基础、可访问名称 | L3 |
| `css-layout` | CSS 与布局 | 盒模型、层叠、Flex、Grid、响应式、动画 | L3–L4 |
| `javascript` | JavaScript | 类型、作用域、原型、异步、模块、错误处理 | L4 |
| `typescript` | TypeScript | 类型收窄、泛型、工具类型、领域建模、类型边界 | L4 |
| `browser-dom` | 浏览器与 DOM | 渲染、事件、Web API、存储、任务队列 | L4 |
| `network-security` | 网络与安全 | HTTP、缓存、跨域、认证、常见前端安全问题 | L3–L4 |
| `react-core` | React 核心 | 组件、Hooks、渲染、生命周期、并发与 Fiber 心智模型 | L4 |
| `react-ecosystem` | React 应用生态 | 路由、状态、请求缓存、表单、Schema、组件库 | L4 |
| `engineering` | 前端工程化 | Vite/Webpack、包管理、Lint、Git、CI、发布边界 | L3–L4 |
| `testing-quality` | 测试与质量 | 单元、组件、交互、回归、可维护性、改动控制 | L3–L4 |
| `performance-a11y` | 性能与可访问性 | CWV、加载优化、运行时性能、键盘与读屏语义 | L3 |
| `coding-algorithms` | 编码与算法 | 常见手写题、数据结构、复杂度、边界处理 | L3–L4 |
| `project-delivery` | 项目设计与交付 | 探索、拆解、数据流、调试、验证、风险控制 | L4 |
| `interview-communication` | 面试表达 | 项目叙述、原理解释、追问、取舍和证据表达 | L4 |

## 分类规则

- 将 React Query、Refine、Zustand、React Hook Form、Zod、路由和 UI 状态流归入 `react-ecosystem`；涉及 Hook 语义或渲染行为时同时关联 `react-core`。
- 将类型体操视为 `typescript` 的局部证据，不等同于真实领域建模能力。
- 将浏览器事件链同时关联 `browser-dom`；只有真实组件交互闭环才能额外关联 `project-delivery`。
- 将项目文件数量视为范围信息，不视为交付质量。
- 将面经参考答案视为学习材料；只有原回答、追问和真实反馈才能关联 `interview-communication`。
- 将后端、数据库和服务端实现排除出主画像；读取共享 Schema 或契约可作为前端边界理解证据。

## 聚合原则

- 先评具体知识点，再聚合维度；不要直接依据目录数量给维度打分。
- 维度分数只聚合具有独立验证的知识点。只有学习覆盖时显示“未定级”，并单独描述覆盖面。
- 记录 React 与 TypeScript 的组合能力，例如“用 Schema 驱动表单和接口边界”，不要只记录库名。
