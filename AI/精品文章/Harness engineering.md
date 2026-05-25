# Harness engineering
**人类掌舵，智能体执行。**
**要给 Codex 的是一张地图，而不是一本 1,000 页的说明书。**

我们尝试了“一个大型的 [`AGENTS.md`⁠（在新窗口中打开）](https://agents.md/)”方法。可想而知，这是一次失败的尝试：

- **情境是一种稀缺资源。**一个巨大的指令文件会挤掉任务、代码和相关文档 — 因此智能体要么会错过关键约束条件，要么开始针对错误的约束条件进行优化。
- **过多的指导反而变得****_无效_****。**当一切都 "重要"时，一切都不重要了。智能体最终会在本地进行模式匹配，而不是有意识地进行导航。
- **它会立即腐烂。**一本庞杂的手册会变成陈旧规则的坟场。智能体无法判断哪些信息仍然有效，一旦人类停止维护它，此文件就会悄然成为一个颇具吸引力的麻烦源头。
- **这很难核实。**单个 blob 不适合进行机械检查（覆盖率、新鲜度、所有权、交叉链接），因此漂移是不可避免的。

**渐进式披露**：智能体从一个小而稳定的切入点开始，并被指导下一步该去哪里查看，而不是一开始就被淹没。

这篇来自 OpenAI 官方博客的文章 _Harness engineering: leveraging Codex in an agent-first world_（驾驭工程：在以 Agent 为主导的世界中利用 Codex）非常有前瞻性。文章详细记录了 OpenAI 一个团队在过去五个月中进行的一项激进实验：**从零开始，完全依靠 AI Agent（Codex）构建一个包含百万行代码的内部产品，且人类不写任何一行代码**。

这不仅仅是关于 AI 编程的讨论，更是关于未来软件工程范式的深刻变革。以下是该文章的核心结论与关键洞察：

### 1. 核心实验成果：零手工代码的可行性

团队在 2025 年 8 月启动项目，历时 5 个月，通过 **1,500 个 PR** 构建了约 **100 万行代码**的产品。

- **效率提升**：相比传统手工编写代码，时间成本降低了约 **1/10**。
- **核心原则**：**人类负责引导（Steer），Agent 负责执行（Execute）**。人类从未直接贡献代码，而是通过设计环境、指定意图和构建反馈循环来工作。

### 2. 工程师角色的根本性转变

当代码由 AI 生成时，工程师的工作重心发生了位移：

- **从“写代码”到“设计环境”**：工程师的主要工作不再是具体的编码，而是构建能够让 AI 高效工作的**系统、脚手架和杠杆**。
- **解决瓶颈**：早期进度慢不是因为 AI 能力不足，而是环境定义不足。人类需要不断问自己：“AI 缺少什么能力？如何让它既能理解又能执行？”
- **工作流**：人类通过 Prompt 下达任务 -> Agent 运行并提交 PR -> Agent 自我审查/互相审查 -> 人类仅在需要判断时介入。

### 3. 关键技术架构与策略

为了支撑“全 AI 生成代码”，团队建立了一套全新的基础设施：

- **提升“可读性”**：
    - **给 AI 看的文档**：放弃了冗长的 `AGENTS.md` 手册，转而使用结构化的 `docs/` 目录作为记录系统。AI 需要像人类新人一样，通过“地图”去寻找具体的知识。
    - **应用可读性**：让 AI 能直接“看”懂应用状态。例如，将 Chrome DevTools 协议接入 Agent 运行时，让 AI 能自己启动应用、截图、复现 Bug 并验证修复；让 AI 能直接查询日志和监控指标（LogQL/PromQL）。
- **严格的架构约束**：
    - **分层架构**：强制实施严格的分层（如 Types → Config → Repo → Service → Runtime → UI），通过机械化的 Linter（由 Codex 生成）强制执行依赖方向。
    - **为什么需要约束？** 在人类开发中，架构约束往往是为了长期维护；在 AI 开发中，**严格的约束是速度的前提**，它防止了架构漂移和熵增，让 AI 能在确定的边界内自由发挥。
- **合并策略的改变**：
    - 由于 AI 吞吐量极高，传统的严格合并门禁变得低效。团队采用了更宽松的策略：**修正很便宜，等待很昂贵**。允许通过后续运行修复问题，而不是无限期阻塞进度。

### 4. 挑战与应对：熵增与垃圾回收

全 AI 自治带来了一个新问题：**熵增**。AI 会复制现有的（即使是不完美）模式，导致“AI 垃圾”积累。

- **解决方案**：**自动化的垃圾回收**。
    - 团队不再手动清理，而是定义了“黄金原则”（Golden Principles），并设置定期的后台任务（Background Codex tasks）来扫描代码库。
    - 这些任务会自动打开重构 PR 来修正技术债务，就像垃圾回收机制一样，将人类从繁琐的维护中解放出来。

### 5. 总结与展望

- **当前状态**：AI 现在可以实现端到端驱动新功能（从复现 Bug -> 录屏 -> 修复 -> 验证 -> 提交 PR -> 回应评论 -> 合并）。
- **未来挑战**：目前的策略在内部发布阶段有效，但**长期（数年）的架构一致性**以及如何最好地将人类判断力编码进系统，仍是未知数。
- **核心结论**：构建软件依然需要纪律，但这种纪律更多体现在**脚手架、抽象和反馈循环**的设计上，而不是具体的代码行上。

---

### 💡 核心洞察总结表

|维度|传统人类工程|Agent-First 工程 (本文模式)|
|:--|:--|:--|
|**核心资源**|工程师的时间与代码产出|工程师的引导与意图指定|
|**文档策略**|外部文档 (Google Doc/Slack)|**内部化知识库** (docs/ 目录，版本化)|
|**架构作用**|指导开发，防止混乱|**速度加速器**，通过约束减少 AI 犯错空间|
|**代码审查**|人类主导，耗时且昂贵|**Agent-to-Agent** 为主，人类仅介入关键判断|
|**技术债务**|定期专项清理|**持续垃圾回收** (自动化 Agent 定期重构)|
|**主要瓶颈**|人类的打字速度和认知负荷|**人类的 QA 能力和环境定义能力**|

这篇文章实际上是在告诉我们：**未来的顶尖工程师，可能不再是写代码最快的人，而是最懂得如何“驯化”和“指挥” AI 队伍的人。**


## 文章链接
OpenAI: 
- Harness engineering: leveraging Codex in an agent-first world https://openai.com/index/harness-engineering/ 

Anthropic: 
- Effective harnesses for long-running agents https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents 
- Harness design for long-running application development https://www.anthropic.com/engineering/harness-design-long-running-apps 

LangChain: 
- The Anatomy of an Agent Harness https://www.langchain.com/blog/the-anatomy-of-an-agent-harness 

Mitchell Hashimoto: 
- My AI Adoption Journey https://mitchellh.com/writing/my-ai-adoption-journey 

martinfowler.com: 
- Harness Engineering - first thoughts https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html 
- Harness engineering for coding agent users https://martinfowler.com/articles/harness-engineering.html