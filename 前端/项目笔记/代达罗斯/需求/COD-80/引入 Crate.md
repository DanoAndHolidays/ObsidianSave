# 「Feature」Introduce Crate as an independent metadata entity[ˈentəti] | 引入 Crate 作为独立元数据实体
---
## 背景
Daedalus 目前已有 Repository 作为一等实体，但缺少一个更高层的抽象来描述代码如何组织、每个部分承担什么职责。在讨论架构或规划代码结构图时，团队目前只能回退到 Package、Module、Feature、Library、Service 等 overloaded 的术语，这常常导致混淆，因为同一个词在不同实现上下文中含义不同。

---
## 用户故事
作为一个在 Daedalus 中审查项目架构的用户
我希望定义和管理代表有边界代码组织单元的 Crate 实体
从而能够清晰地描述职责与结构，而不再依赖 overloaded 的实现术语

---
## 功能概览
引入 Crate 作为与 Repository 平级的独立元数据实体。Crate 是一个以职责驱动的、有名字的代码组织单元，可以表现为 package、module、feature、library、service、utility 或任何其他可复用的软件构造。目前 Crate 被有意设计为轻量级元数据实体，不需要绑定到物理位置或 Repository。

---
## 用户流程
步骤 1：用户进入 Crate 管理视图
→ 步骤 2：用户新建 Crate，填写 name、type、responsibility 和可选 metadata
→ 步骤 3：用户保存 Crate 定义
→ 结果：Crate 出现在列表中，可在架构讨论和未来仓库映射中引用

---
## 前端变更
### 页面
* Crate 列表页
* Crate 详情 / 创建 / 编辑页

### UI 变更
* 新增 Crate 卡片 / 列表项
* 新增 Crate 创建与编辑表单
* 新增 Crate 管理导航入口

### 交互变更
* 用户可在 UI 中创建、查看、更新、删除 Crate 定义
* 创建或更新 Crate 时即时触发校验反馈
* 删除 Crate 需要确认，防止误删元数据

---
## 数据与业务逻辑变更
### 数据结构变更
* 新增字段：Crate { id, name, type, responsibility, metadata }

### 业务规则变更
* 新增校验规则：Crate name 必填且在工作空间内唯一
* 新增校验规则：type 必须是允许值之一（package、module、feature、library、service、utility 或其他）

### 数据流变更
* 输入变化：用户或 API 客户端提供 Crate 定义（name、type、responsibility、可选 metadata）
* 处理变化：Crate 数据作为工作空间级元数据持久化，并与所属工作空间关联
* 输出变化：Crate 列表与详情视图将存储的定义返回给客户端

---
## 技术说明（可选）
### 影响模块
* 领域模型
* API 层
* 数据库表结构
* UI 工作空间设置 / 架构模块

### 系统约束
* 当前迭代中，Crate 有意不绑定仓库物理位置或文件路径

### 性能考虑
* Crate 是轻量级元数据实体，每个工作空间预期记录数较少

### 非目标
* 基于仓库扫描自动识别 Crate
* Crate 依赖图或 ownership 视图
* Crate 与 Archetype 的关联（参见 [COD-81](https://linear.app/code-forge-official/issue/COD-81/featureintroduce-archetype-as-a-design-paradigm-entity-or-引入-archetype)）
* Crate 的物理文件或路径映射

### 验收标准
- [ ] UI 正确实现：用户可以完成 Crate 定义的增删改查
- [ ] 数据正确变化：Crate 数据跨会话准确持久化与读取
- [ ] 业务规则正确执行：校验强制要求必填且唯一的 name，以及合法的 type
- [ ] 无回归问题：Repository 及其他现有实体不受影响
- [ ] 边界情况处理完整：重复名称、缺少必填字段、超长文本、删除确认等均已覆盖
