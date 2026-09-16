我根据 Linear 中**当前由你负责的 COD 团队 Issue**做了汇总。查询范围包含已归档 Issue，当前共找到 **30 个**：

- **26 个 Done**
- **1 个 Todo：COD-77**
- **3 个 Duplicate：COD-170、COD-175、COD-197**
- 时间跨度大约是 **2026 年 6 月 21 日至 2026 年 8 月 28 日**

整体来看，你做的不是零散的页面功能，而是在持续搭建 Daedalus 的完整产品链路：

> **代码治理元数据 → 结构和规则校验 → AI 扫描 → Finding 审查处理 → Coding Agent / MCP 操作 → CMS 内容管理 → 对外公开 Web**

下面按工作主线详细总结。


# Daedalus项目经历
> Last Format Time：9/16/2026 19:24:52

这是你前期和中期工作的基础。核心目标是：不要只把代码当成文件和仓库，而是为代码建立一套可被系统理解、校验和审查的结构化治理模型。

---
## Crate：描述代码组织单元
### COD-80：建立 Crate 代码组织元数据
你引入了 **Crate** 这一核心概念，用于描述代码中的组织单元。

支持的 Crate 类型包括：

- package
- module
- feature
- library
- service
- utility

每个 Crate 可以记录：

- 名称
- 类型
- 职责
- 额外元数据

同时完成了对应的全栈 CRUD 能力：

- 列表
- 详情
- 创建
- 编辑
- 删除

并且加入了一些业务约束：

- Crate 名称在 Workspace 内必须唯一。
- Crate 类型必须来自定义好的枚举。
- 初期 Crate 只描述逻辑上的代码组织关系。
- 不直接绑定具体 Repository、文件路径或物理目录。

这一步为后续的 Archetype、Anatomy、Rule 和 Scan Profile 打下了基础。

### COD-172：校验 Crate 元数据格式
在 Crate 基础 CRUD 之后，你进一步补充了 Crate 的格式和业务规则校验，使 Crate 不只是“可以保存的数据”，而是必须符合系统定义的数据契约。

### COD-174：支持按类型和职责筛选 Crate
你还增加了 Crate 的筛选能力，可以按照以下维度过滤：

- Crate 类型
- Crate 负责的职责范围

这让 Crate 从单纯的配置对象，变成了可以被检索和管理的治理数据。

---
## Archetype：描述设计层契约
### COD-86：管理 Archetype 定义
你建立了 **Archetype** 作为设计层契约，用于表达一个模块、组件或代码单元应该满足什么条件。

Archetype 支持两种类型的 Condition：

1. **文本型 Condition**
2. **引用其他 Archetype 的 Condition**

围绕 Archetype，你完成了：

- 创建
- 编辑
- 删除
- 列表
- 分页
- Condition 管理

同时重点处理了依赖关系约束：

- 一个 Archetype 至少需要一个 Condition。
- 不允许 Archetype 自引用。
- 不允许形成循环引用。
- Archetype 之间的引用关系必须形成 DAG，也就是有向无环图。
- 名称在 Workspace 内必须唯一。

这说明你不仅实现了基本的后台管理页面，还处理了领域模型中的依赖图和循环依赖问题。

### COD-87：查看 Archetype 依赖树
你为 Archetype 增加了依赖树视图，用来展示：

- 直接依赖
- 间接依赖
- Archetype 之间的层级关系

这个功能解决的是架构理解问题。架构师或开发者可以看到某个设计契约依赖了哪些其他契约，也能够理解修改一个 Archetype 可能影响到哪些下游对象。

### COD-88：将 Crate 绑定到 Archetype
你把 Crate 和 Archetype 连接起来：

- 一个 Crate 可以关联一个或多个 Archetype。
- Crate 表示代码组织单元。
- Archetype 表示设计层约束。
- 两者关联后，可以表达“这个代码模块应当遵循哪些设计契约”。

这一步让代码组织模型和设计治理模型产生了实际联系。

---
## Anatomy：描述文件和目录结构
### COD-225：定义 Crate 内部的文件和目录结构
这是治理模型中比较重要的一次扩展。你引入了 **Anatomy**，用来描述一个 Crate 内部应该具备什么样的文件和目录结构。

Anatomy 支持：

- 创建 Draft
- 编辑目录树
- 添加文件 Entry
- 添加目录 Entry
- 发布 Anatomy Version
- 查看已发布版本

结构约束支持多种形式：

- 固定名称
- 占位名称
- Exactly one
- Optional
- One or more
- Zero or more
- `One of` 替代结构

你还为结构校验定义了不同级别的处理方式：

- Block
- Warn
- Allow

可以针对以下问题设置不同的策略：

- 缺失项
- 未声明项
- 名称不匹配
- 层级不匹配

同时，你建立了 Draft 和 Published Version 之间的生命周期：

- Draft 可以继续编辑。
- Draft 发布后变成不可变的 Anatomy Version。
- Crate 只能选择已经发布的 Anatomy 版本。
- 新版本发布后，不会自动让已有 Crate 切换过去。
- Anatomy 本身不保存真实仓库、项目或物理路径。

这套设计让结构规则具备版本化能力，也避免了规则变更直接影响已有项目。

### COD-291：优化 Anatomy 页面首屏体验
在功能完成后，你又对 Anatomy 的 UI 和信息架构进行了重构。

主要调整包括：

- 重构 Anatomy 列表页。
- 重构 Anatomy 详情页。
- 重构 Anatomy 编辑页。
- 移除面包屑导航。
- 将名称、状态、版本、主要操作放到首屏。
- 将目录结构直接放入核心可视区域。
- 适配桌面端和窄屏布局。
- 统一 Draft、Published、Loading、Empty、Error 和只读状态。

这项工作重点不是增加领域能力，而是降低用户理解和操作 Anatomy 的成本。

### COD-292：通过 Anatomy CLI 校验项目结构
你把 Anatomy 从后台配置页面进一步落到了 CLI 中。

现在 Anatomy 不只是一种存储的规则，还可以用于：

- 通过命令行扫描项目目录。
- 校验项目的文件和目录结构。
- 发现缺失、未声明、命名错误、层级错误等问题。
- 根据 Anatomy 中定义的 Block、Warn、Allow 策略处理结果。

这意味着治理规则真正进入了开发和审查流程，而不是停留在管理后台。

---
## Dictionary：建立项目级词典
你还建立了一个可复用的项目词典体系。

### COD-193：建立项目词典能力
你引入了项目级 Dictionary，用来统一管理项目术语。

目标包括：

- 管理项目中的标准术语。
- 让多个模块复用同一套词汇。
- 为后续规则、AI 分析和代码审查提供统一语义基础。

### COD-194：创建完整的名词词条
支持创建包含以下信息的名词词条：

- 名称
- 释义
- 示例

这样可以明确一个领域名词到底代表什么，减少团队成员之间的理解偏差。

### COD-195：增强动词词条和跨模块引用
你进一步扩展了词典能力：

- 支持动词词条。
- 支持标准写法。
- 支持跨模块引用词条。

这让 Dictionary 不只是名词表，而是开始覆盖项目中“对象”和“动作”的统一表达。

### COD-196：为词条定义标准写法
你增加了词条的规范化能力，可以为一个词条维护：

- 标准拼写
- 标准表达
- 推荐使用形式

这对保证代码命名、文档表达和 AI 输出的一致性非常重要。

### COD-198：允许其他模块引用词典词条
你让其他业务模块可以引用 Dictionary Entry，而不是各自保存一份字符串。

这样可以保证：

- 词条来源统一。
- 修改词条后，引用关系仍然可追踪。
- 规则、审查、元数据之间可以共享领域词汇。
- 避免不同模块重复定义同一个概念。

### COD-197：为词条补充释义和示例
这个 Issue 当前是 **Duplicate**，并且已经在 **2026 年 7 月 14 日**取消，说明相关需求已经被其他 Issue 合并或替代。


# 二、搭建代码审查和 Finding 工作台

在治理元数据建立之后，你开始把这些数据用于真实的代码审查流程。

---
## COD-186：Finding 工作台定位并处理问题
你完成了 Finding 工作台的核心交互，让用户可以从扫描结果中定位、理解和处理问题。

支持组合筛选：

- 严重级别
- 检查层级
- 文件路径
- 处理状态

用户可以查看 Finding 的来源链路，包括：

- Scan Run
- Scan Profile
- Rule
- Checklist

并且能够从 Finding 跳转到相关对象，查看完整上下文。

Finding 处理能力包括：

- 从列表标记为已解决。
- 从详情标记为已解决。
- 处理过程中防止重复操作。
- 操作失败时保留原状态。
- 给出可理解的错误提示。

最终形成了一个比较完整的处理闭环：

> **筛选 Finding → 查看来源和上下文 → 定位问题 → 标记解决**

这个 Issue 也承接了 COD-187、COD-188 中的相关能力。

---
## COD-220：保持大型仓库文件树流畅
你还专门处理了大型 Repository 文件树的性能问题。

目标是保证在仓库文件较多、目录层级较深时：

- Explorer 不明显卡顿。
- 文件树展开和浏览保持响应。
- 用户可以正常定位审查涉及的文件。
- 大型仓库不会因为前端渲染或数据加载造成严重阻塞。

这项工作虽然看起来偏性能优化，但它直接影响 Finding 定位和代码审查体验。


# 三、建设 Coding Agent / MCP 能力

这是你后期非常重要的一条工作主线。你把 Daedalus 从一个主要依赖 Web UI 的内部工具，扩展成了可以被外部 Coding Agent 操作的平台。

---
## COD-305：安全接入 Coding Agent
你先建立了 MCP 接入入口。

在 Settings 中新增 MCP Tab，并支持多种客户端：

- Codex
- Claude Code
- OpenCode
- 通用 MCP Client

接入方式包括：

1. 提供命令。
2. 提供接入文档。
3. 提供“复制给 AI Prompt”的快捷方式。

同时建立了重要的 Workspace 隔离规则：

- 一个 MCP Connection 固定绑定一个 Workspace。
- 连接必须明确归属。
- 不同 Workspace 之间不能混用连接。

连接管理能力包括：

- 查看连接状态。
- 重新检查连接。
- 撤销连接。
- 查看连接详情。

这个 Issue 是 MCP 能力的基础设施层，关联 PR #50。

---
## COD-306：让 Coding Agent 操作 Daedalus 审查流程
在 MCP 连接建立后，你为 Coding Agent 暴露了 Daedalus 的审查能力。

Coding Agent 可以读取：

- Workspace
- Project
- Repository
- Crate
- Archetype
- Anatomy
- Dictionary
- Rule
- Scan Profile

同时可以执行和追踪扫描流程：

- 发起 Scan。
- 查看 Scan Run。
- 查看 Trace。
- 查看 Finding。
- 查看代码证据。

Finding 方面还支持：

- 更新 Finding 状态。
- 标记 Finding 已解决。
- 提交反馈。

但你没有把所有后台能力都暴露出去，而是明确限制了高风险范围。

暂不开放或不允许 Coding Agent 直接操作：

- Team 管理
- 元数据写入
- Harness
- GitHub Delivery
- Pull Request
- 其他高风险管理能力

这体现了你在 MCP 设计中采用了“最小权限”的思路。

该 Issue 关联 PR #53，并且被 COD-305 阻塞，属于连接能力之后的业务能力层。

---
## COD-330：通过 Coding Agent 创建治理元数据并完成扫描
在 COD-306 只读和审查操作能力的基础上，你继续增加了写入能力。

Coding Agent 现在可以创建和更新：

- Crate
- Archetype
- Anatomy
- Dictionary
- Rule
- Scan Profile

同时可以配置它们之间的关系：

- Crate 与 Archetype 的关系。
- Crate 与 Anatomy 的关系。
- Archetype 之间的引用关系。
- Rule 与治理模型的关系。
- Scan Profile 与规则、范围之间的关系。

但这些写操作并不是无条件开放，而是有边界：

- 所有写入固定发生在 MCP Connection 所属的 Workspace。
- 写操作需要明确确认。
- 复用已有 Schema。
- 复用已有 Service。
- 复用既有权限校验。
- 复用审计逻辑。
- 不允许删除元数据。
- 不允许管理 Team。
- 不开放 GitHub Delivery、PR、Harness 等高风险能力。

最终形成了一个从治理数据创建到审查结果读取的闭环：

> **创建治理数据 → 配置关系 → 发起扫描 → 跟踪 Run/Trace → 读取 Finding**

这个 Issue 关联 PR #59。

---
## COD-366：为远端 Coding Agent 增加无浏览器 API Token 鉴权
你解决了远程 Coding Agent 接入时的实际鉴权问题。

原问题是：

- 远程 Pi 或 `mcp-remote` 环境没有正常浏览器。
- OAuth 授权回调可能错误地回到远程机器的 localhost。
- 用户无法完成正常授权。

为了解决这个问题，你为 MCP Connection 增加了 API Token 体系。

主要能力包括：

- 生成 API Token。
- 轮换 API Token。
- 撤销 API Token。
- Token 过期控制。
- Token 与 OAuth 2.1 并存。
- 更新 Setup Descriptor。
- 更新 MCP 连接详情 UI。

安全设计方面：

- 数据库只保存 Token hash。
- 只保存 Token 末四位用于识别。
- 保存生命周期信息。
- 不保存明文 Token。
- Token 继承 Connection 的 owner。
- Token 固定绑定 Workspace。
- Token 不能跨 Workspace 使用。
- 撤销 Connection 时，关联 Token 也失效。
- 日志中需要脱敏 Token 信息。

还覆盖了测试场景：

- 远端读取。
- 远端写入。
- Token 轮换。
- Token 撤销。
- Token 过期。
- Workspace 隔离。
- 日志脱敏。

该工作关联 PR #80、#81。


# 四、建设 Payload CMS 和公开 Web

在内部代码治理和 Coding Agent 能力之外，你又把产品扩展到了内容管理和公开展示场景。

---
## COD-362：通过 Payload CMS 管理 Daedalus 对外内容
你建立了 Daedalus 的内容管理能力。

Payload CMS 中涉及的内容模型包括：

- Pages
- 内容区块
- CTA
- Media
- Site Navigation
- SEO 配置
- Site Settings

内容生命周期包括：

- Draft
- Preview
- Publish
- Unpublish

权限边界也被明确区分：

- 编辑者可以保存 Draft。
- 编辑者不能直接发布。
- 编辑者不能直接下线内容。
- 只有具备发布权限的用户才能发布或下线。

发布前还会校验：

- 必填内容是否完整。
- 导航目标是否有效。
- 页面结构是否满足要求。
- 发布者是否具备权限。

公开 Web 只允许读取 Published 内容：

- Draft 不得泄露。
- Unpublished 内容不得出现在公开页面。
- CMS 读取失败时返回最后有效版本或明确的兜底状态。
- 内容缺失时需要有清晰的恢复方式。

这个 Issue 关联 PR #76。

---
## COD-363：建立独立公开 Web
你使用 TanStack Start 构建了一个独立的公开 Web，而不是让外部用户直接访问内部 App。

公开 Web 提供：

- 首页
- 产品介绍
- 使用场景
- FAQ
- 全局导航
- 页脚
- 404 页面
- 内容缺失时的兜底页面

主要边界是：

- 只消费 Payload CMS 中的 Published 内容。
- 不要求用户登录内部 App。
- 不暴露 CMS 管理功能。
- 不暴露内部审查数据。
- Draft 和 Unpublished 内容不会展示到公开侧。

同时完成了前端体验处理：

- 桌面端响应式布局。
- 移动端响应式布局。
- Loading 状态。
- Empty 状态。
- Error 状态。
- CTA 操作。
- 返回首页路径。
- 内容缺失和 CMS 不可用时的降级处理。

这个 Issue 关联 PR #85。

---
## COD-380：通过 Payload CMS 提供受控 MCP 内容管理与发布
这是你截至 **2026 年 8 月 28 日**完成的最新一批工作之一。

你接入了 Payload 官方的：

`@payloadcms/plugin-mcp`

并且明确采用官方插件提供的 `/api/mcp` Endpoint，而不是自行实现 MCP Route。

通过 MCP，Coding Agent 可以在受控范围内操作内容：

### Pages
支持：

- 创建
- 更新
- 删除
- 自定义发布

### Media
支持：

- 创建
- 更新
- 删除
- 上传指引

### Site Navigation 和 Site Settings
支持更新。

页面发布继续复用已有能力：

- `publisherOnly`
- `validatePublishIntent`

也就是说，MCP 并没有绕过 CMS 原本的权限和发布规则，而是接入到现有治理链路中。

你还明确禁止 MCP 管理以下内容：

- CMS Users
- 发布快照
- 版本恢复
- Schema
- 统计数据
- 其他内部或高风险能力

同时强调了几个安全原则：

- 最小权限。
- 鉴权失败必须明确返回错误。
- 不能把失败伪装成空数据。
- MCP 写入必须遵循既有权限和发布校验。
- 内容发布必须经过合法的发布意图验证。

这个 Issue 关联 PR #86。


# 五、用户体验、布局和工程质量改进

除了核心产品功能，你还持续处理了体验和工程维护问题。

---
## COD-205：让主工作区内容真正居中
你调整了主工作区的布局，使页面主要内容更加真正地居中。

重点改善：

- 内容区域视觉平衡。
- 主工作区的左右留白。
- 页面主体定位。
- 大屏幕下的内容展示比例。

这个工作和 Anatomy 页面优化一起出现在 PR #40 中。

---
## COD-291：改善 Anatomy 页面信息架构
前面提到的 Anatomy 页面优化，本质上也属于体验升级工作：

- 重要信息前置。
- 减少不必要的导航层级。
- 首屏直接呈现状态、版本、操作和结构。
- 适配不同屏幕宽度。
- 统一各种状态页面。

---
## COD-265：周期性重构负责模块
你建立了一个周期性工程维护任务：

> 每个 Cycle 的最后一个星期五，重构自己负责的模块。

关注内容包括：

- 代码结构。
- 模块边界。
- 可维护性。
- 技术债。
- 长期演进能力。
- 领域模块的一致性。

这说明你不仅在交付功能，也在建立持续维护代码质量的工作机制。

---
## COD-104：调研描述代码架构的数据结构方案
这是比较早期的研究型 Issue。

你调研了如何用稳定的数据结构描述代码架构，为后续这些能力提供基础：

- Crate
- Archetype
- Anatomy
- Dictionary
- Rule
- Scan Profile

从结果上看，后续多个治理模块都围绕这个方向逐步落地了。因此 COD-104 可以看作后续架构治理体系的前置探索。


# 六、目前尚未完成的核心能力

---
## COD-77：Ask Daedalus 基于项目上下文提问
这是目前你负责 Issue 中明确仍然处于 **Todo** 状态的主要功能。

目标是提供一个 Ask Daedalus 对话入口，让用户可以针对项目上下文提问。

计划能力包括：

- 引用文件。
- 引用 Rule。
- 引用 Finding。
- 基于项目上下文回答问题。
- 回答带有来源。
- 支持连续追问。
- 处理无权限引用。
- 处理失效引用。
- 处理回答失败。
- 为失败场景提供清晰恢复路径。

该 Issue 关联 PR #65。

需要特别注意的是，虽然它历史状态中曾经出现过其他状态，但截至目前 Linear 中的实际状态是 **Todo**，因此它应当被视为当前尚未完成的核心能力。


# 七、重复或被其他需求替代的 Issue

---
## COD-170：从 Crate 详情页发起扫描
当前状态：**Duplicate**

已于 **2026 年 7 月 18 日**取消。

相关能力很可能已经被后续 Coding Agent、Scan 或治理流程 Issue 合并覆盖。

---
## COD-175：追踪 Archetype 变更影响的 Crate
当前状态：**Duplicate**

已于 **2026 年 7 月 14 日**取消。

这个需求与 Archetype 依赖关系、Crate 绑定以及后续影响分析方向相关，但目前已经由其他需求替代或合并。

---
## COD-197：为词条补充释义和示例
当前状态：**Duplicate**

已于 **2026 年 7 月 14 日**取消。

它的目标已经被 Dictionary 相关的其他 Issue，例如 COD-194 等能力覆盖。


# 八、按时间和产品发展阶段看，你完成了什么

---
## 第一阶段：定义治理模型
早期重点是把代码治理对象抽象出来：

- COD-104：研究架构数据结构。
- COD-80：建立 Crate。
- COD-86：建立 Archetype。
- COD-87：展示 Archetype 依赖。
- COD-88：绑定 Crate 和 Archetype。
- COD-172、COD-174：完善 Crate 校验和筛选。
- COD-193～COD-198：建立 Dictionary。

这个阶段解决的是：

> Daedalus 到底要管理哪些代码治理对象，以及这些对象之间如何关联。

---
## 第二阶段：把治理模型落到代码结构和审查流程
随后你把治理模型真正应用到代码中：

- COD-225：用 Anatomy 描述文件和目录结构。
- COD-292：通过 CLI 校验项目结构。
- COD-186：建立 Finding 工作台。
- COD-220：优化大型仓库文件树性能。
- COD-291：优化 Anatomy 页面体验。

这个阶段解决的是：

> 不只是保存治理数据，还要用这些数据发现代码问题，并支持用户处理审查结果。

---
## 第三阶段：让 Coding Agent 能够操作平台
之后工作重点转向 MCP 和 AI Agent：

- COD-305：建立 MCP 连接。
- COD-306：让 Agent 读取治理上下文、发起扫描和处理 Finding。
- COD-330：让 Agent 创建和更新治理数据。
- COD-366：为远端 Agent 提供无浏览器 Token 鉴权。

这个阶段解决的是：

> 用户不必只通过 Daedalus UI 操作，也可以让 Codex、Claude Code、OpenCode 等 Coding Agent 在安全边界内完成治理和审查任务。

---
## 第四阶段：扩展到内容管理和公开 Web
最近一阶段，你开始建设产品的对外内容能力：

- COD-362：建立 Payload CMS 内容模型和发布生命周期。
- COD-363：建立独立公开 Web。
- COD-380：让 Coding Agent 通过受控 MCP 管理和发布 CMS 内容。

这个阶段解决的是：

> 产品的对外内容不再完全依赖代码发布，同时可以通过 CMS 和受控 AI Agent 管理公开内容。


# 九、整体工作评价

综合这些 Issue，你做的事情可以概括为以下几个方面。

---
## 从零散的后台功能发展成完整治理平台
你不是单独做了几个 CRUD 页面，而是逐步建立了完整的治理对象：

- Crate 描述代码组织。
- Archetype 描述设计契约。
- Anatomy 描述目录结构。
- Dictionary 描述项目术语。
- Rule 描述审查规则。
- Scan Profile 描述扫描配置。
- Finding 记录审查问题。

这些对象之间形成了相互关联的治理体系。

---
## 从配置管理发展到实际代码校验
你没有让这些元数据停留在数据库和管理页面里，而是继续把它们用于：

- CLI 项目结构校验。
- Repository 文件树浏览。
- Scan 执行。
- Finding 生成。
- Finding 处理。
- 代码证据追踪。

也就是从“描述代码应该是什么样”发展到了“检查代码现在是否符合要求”。

---
## 从 Web UI 扩展到 Coding Agent
你把 Daedalus 的能力开放给了外部 Coding Agent：

- Agent 可以读取 Workspace 和项目上下文。
- 可以读取治理元数据。
- 可以发起扫描。
- 可以查看 Run、Trace 和 Finding。
- 可以更新 Finding 状态。
- 在明确确认下可以创建和更新治理元数据。
- 远端环境可以通过 API Token 接入。

而且整个过程中一直保留了：

- Workspace 隔离。
- 权限控制。
- 写操作确认。
- Token 撤销。
- 审计逻辑。
- 高风险操作限制。

这说明你的重点不仅是“让 AI 能操作”，还包括“让 AI 在可控范围内操作”。

---
## 从内部开发工具扩展到对外产品内容
通过 Payload CMS 和公开 Web，你又完成了产品对外展示能力：

- 内容模型。
- Draft/Preview/Publish 生命周期。
- 发布权限。
- 内容校验。
- 独立公开 Web。
- Published 内容隔离。
- CMS 故障降级。
- MCP 受控内容管理。

这让 Daedalus 从内部审查工具进一步向完整产品形态发展。

---
## 持续关注体验和工程质量
除了功能交付，你还做了：

- 主工作区布局优化。
- Anatomy 首屏体验优化。
- 大型仓库文件树性能优化。
- 周期性模块重构。
- 架构数据结构调研。

说明你同时关注：

- 用户使用体验。
- 大型数据量下的性能。
- 代码长期维护。
- 产品架构的可扩展性。


# 最终总结

你的这 30 个 COD Issue，整体可以总结成一句话：

> 你围绕 Daedalus 建立了一套从代码架构建模、治理规则定义、项目结构校验、AI 扫描、Finding 处理，到 Coding Agent 操作和 CMS/公开 Web 发布的完整产品链路。

具体发展路径是：

```text
架构数据结构研究
    ↓
Crate / Archetype / Dictionary
    ↓
Anatomy 文件结构治理
    ↓
CLI 结构校验
    ↓
Scan 与 Finding 工作台
    ↓
MCP 连接与 Coding Agent 操作
    ↓
远程 API Token 鉴权
    ↓
Payload CMS 内容管理
    ↓
独立公开 Web
    ↓
通过 MCP 受控管理和发布内容
```

目前整体完成度很高，主要尚未完成的核心方向是：

> **COD-77：Ask Daedalus 项目上下文问答能力**

也就是说，你已经基本完成了 Daedalus 的治理数据层、审查执行层、Finding 处理层、Agent 接入层和内容发布层，下一步比较自然的产品延伸就是把这些结构化上下文进一步用于对话式问答和解释。