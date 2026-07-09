# 引入Archetype
> Last Format Time：7/9/2026 23:46:20

---
## 背景
Daedalus 正在引入 Crate 作为独立的代码组织实体。但 Crate 本身只回答“它是什么”（package、module、feature、library 等），还不能表达“某个东西必须满足什么条件才能被视为某一类事物”。

为了把这两个层次分开，我们引入 **Archetype** 作为设计层契约。Archetype 不关乎物理结构，而是一组 **Condition（条件）**，描述一个实例必须在概念上满足什么。Condition 既可以是描述性语句，也可以是对另一个 Archetype 的引用，要求实例同时满足那个 Archetype。

---
## 用户故事
作为一个 **产品设计师 / 技术负责人**

我希望 **创建 Archetype 并通过 Condition 来定义它**

从而能够 **让团队从第一版起就能清晰表达并组合设计契约**。

---
## 功能概览
在 Sidebar 提供独立的 Archetype 管理入口。用户可以创建 Archetype，并通过 Condition 列表来定义它。Condition 支持两种类型：

* **文本型 Condition**：描述性约束，例如“必须提供登录表单”
* **Archetype 引用型 Condition**：引用另一个 Archetype，要求实例同时满足，例如“必须符合 Landing Page Archetype”

这样 Archetype 组合从第一天起就是一等的概念。

---
## 用户流程
步骤 1：用户点击主 Sidebar 中的 **Archetype** 入口

→ 步骤 2：Content 区域加载 Archetype 管理页面

→ 步骤 3：用户点击 **“New Archetype”** 按钮

→ 步骤 4：打开表单，填写 Name、Concept、Scope、Description 和 Conditions

→ 步骤 5：对每个 Condition，用户选择类型（文本或 Archetype 引用）并填写值

→ 步骤 6：用户保存

→ 结果：Archetype 出现在列表中，并展示其 Conditions

---
## 前端变更
### 页面
* Archetype 主页面（Content 区域）
* Archetype 创建/编辑表单（Modal）

### UI 变更
* 主 Sidebar 新增 **Archetype** 一级导航项
* Content 区域新增 Archetype 列表视图
* 新增 “New Archetype” 按钮
* 新增创建/编辑表单（Modal / Drawer）
* 新增动态 Condition 列表编辑器
* 新增 Condition 类型选择器（文本 / Archetype 引用）
* 为 Archetype 引用型 Condition 新增 Archetype 选择器

### 交互变更
* 点击 Sidebar 入口进入 Archetype 主页面
* 点击 “New Archetype” 打开创建表单
* 点击已有 Archetype 打开编辑表单或详情
* 用户可添加、移除、调整 Condition 顺序
* 用户可切换 Condition 类型
* 保存后自动关闭表单并刷新列表

---
## 数据与业务逻辑变更
### 概念字段定义
**Archetype**

| 英文名称 | 中文名称 | 类型 | 说明 |
| -- | -- | -- | -- |
| Name | 名称 | 短文本 | Archetype 的唯一标识名，如 `SaaS Project` |
| Concept | 概念 | 短文本 | 一句话说明该 Archetype 代表什么 |
| Scope | 适用范围 | 枚举 | 该 Archetype 应用于什么层级：`project`、`repository`、`crate`、`page`、`service` |
| Description | 描述 | 长文本 | 设计意图的详细说明 |
| Conditions | 条件 | Condition 列表 | 定义该 Archetype 的条件集合 |

**Condition**

| 英文名称 | 中文名称 | 类型 | 说明 |
| -- | -- | -- | -- |
| Type | 类型 | 枚举 | `text` 或 `archetype_ref` |
| Value | 值 | 文本或关联 | `text` 时为条件描述；`archetype_ref` 时为引用的 Archetype |

### 业务规则变更
* `Name` 在工作空间内必须唯一
* `Scope` 必须是预定义值之一
* 一个 Archetype 至少有一个 Condition
* 文本型 Condition 必须有非空值
* Archetype 引用型 Condition 必须指向已存在的 active Archetype
* 不允许循环 Archetype 引用

### 数据流变更
* 输入：用户提交带 Conditions 的 Archetype 表单
* 处理：校验字段、校验 Conditions、检测循环引用
* 输出：持久化 Archetype 记录及 Conditions，列表刷新

---
## 技术说明
### 影响模块
* Sidebar 导航
* Archetype 页面模块
* Archetype service / DAO
* Condition 校验逻辑

### 系统约束
* 名称在工作空间内唯一
* Archetype 引用型 Condition 必须构成有向无环图

### 性能考虑
* 列表页支持分页和简单文本搜索
* 循环引用检查在中小规模 Archetype 图中应足够高效

---
## 非目标
* Crate-Archetype 绑定
* 一致性校验
* Condition 模板或继承
* 市场/导入导出

---
## 验收标准
* UI 正确实现：Sidebar 导航、列表、创建、编辑、Condition 编辑器可用
* 数据正确变化：保存后带 Conditions 的 Archetype 立即出现在列表中
* 业务规则正确执行：阻止重复名称、阻止循环 Archetype 引用
* 无现有 Sidebar 或页面流程回归
* 边界情况处理完整：空 Conditions、切换 Condition 类型、阻止自引用
