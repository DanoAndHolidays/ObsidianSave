# Skills 架构分析

> 本文档系统性梳理 skills 目录结构、分类方式、核心模式与最佳实践约定。
> 最后更新：2026-06-30

---

## 一、目录结构全貌

```
skills/                                  # 根目录（56个技能）
├── AGENTS.md                            # 仓库级代理指引（创建技能规范）
├── README.md                            # 技能索引表（名称 + 描述 + 链接）
├── LICENSE
└── skills/
    └── {skill-name}/                    # 单个技能，kebab-case 命名
        ├── SKILL.md                     # ★ 必需：YAML前言 + 极简主体
        ├── references/                  # ★ 必需：详细参考文档
        │   ├── checklist.md             # 动词型/best-practice 均需
        │   ├── standard.md              # 仅 best-practice 需要（规范定义）
        │   ├── workflow.md              # 可选：顺序/条件工作流
        │   ├── philosophy.md            # 可选：设计哲学
        │   └── examples/                # 可选：示例文件目录
        ├── best-practice-examples/      # ★ 仅 best-practice：正例代码
        ├── scripts/                     # 可选：可执行脚本 (.ts/.py/.sh)
        └── assets/                      # 可选：静态资源（图片等）
```

### 结构约束（硬性规则）

| 规则 | 说明 |
|------|------|
| `SKILL.md` 必须大写 | `skill.md`、`Skill.md`、`README.md` 均无效 |
| 禁止辅助文档 | 不得有 `README.md`、`CHANGELOG.md`、`INSTALLATION_GUIDE.md` |
| 禁止临时文件 | `__pycache__/`、`.DS_Store`、`*.log`、`tmp/` |
| 无空目录 | `scripts/`、`references/` 无文件时必须删除 |
| 引用一级深度 | SKILL.md → references/*，禁止 references 间互相引用 |
| 无孤立文件 | `references/` 中每个文件必须在 SKILL.md 中被引用 |

---

## 二、分类体系（三层分类）

### 分类决策树

```
技能名称
├── 以 -best-practice 结尾？
│   └── YES → best-practice 型（Must follow when）
│       所需：references/checklist.md + references/standard.md + best-practice-examples/
│       示例：dao-best-practice、component-unit-best-practice、skill-best-practice
│
└── NO → 动词型（Use when）
    ├── check-*   → 检查/验证类：检查代码是否符合某规范
    │   示例：check-checklist、check-components、check-props-drilling
    ├── implement-* → 实现/执行类：按规范完成某项工作
    │   示例：implement-feature、implement-split、implement-trpc-query
    ├── integrate-* → 集成/接入类：将外部库集成到项目
    │   示例：integrate-better-auth、integrate-zod-env
    ├── refactor-* → 重构/转换类：将代码从一种形式转为另一种
    │   示例：refactor-classname、refactor-ui-components
    ├── create-* / generate-* → 创建/生成类
    │   示例：create-skill、generate-preview
    └── 其他动词 → 工作流/流程类
        示例：brainstorming、writing-plans、subagent-driven-development
```

### 56 个技能分类统计

| 分类 | 数量 | 典型示例 | 描述前缀 |
|------|------|----------|----------|
| **best-practice**（规范定义） | 18 | `dao-best-practice`、`form-best-practice`、`store-best-practice` | `Must follow when` |
| **check**（检查验证） | 16 | `check-checklist`、`check-components`、`check-props-drilling` | `Use when` |
| **implement**（执行实现） | 5 | `implement-feature`、`implement-split`、`implement-trpc-query` | `Use when` |
| **integrate**（集成接入） | 2 | `integrate-better-auth`、`integrate-zod-env` | `Use when` |
| **refactor**（重构转换） | 2 | `refactor-classname`、`refactor-ui-components` | `Use when` |
| **工作流/流程** | 6 | `brainstorming`、`writing-plans`、`subagent-driven-development` | `Use when` |
| **创建/生成** | 2 | `create-skill`、`generate-preview` | `Use when` |
| **其他** | 5 | `clean-hardcode`、`remove-comments`、`fix-all-best-practices` | `Use when` |

---

## 三、SKILL.md 核心结构

### 前言区（YAML Frontmatter）—— 唯一元数据入口

```yaml
---
name: skill-name           # ★ 必须与目录名完全一致（字符级）
description: [前缀] [描述]  # ★ 单行，100-150字符，无 < > 符号
---
```

**严格约束：**

- **仅允许 `name` 和 `description`** —— 禁止 `version`、`author`、`tags`、`dependency` 等任何额外字段
- description 必须同时说明 **做什么** + **何时触发**
- 前缀协议：
  - best-practice 型：`Must follow when` + 中文描述
  - 动词型：`Use when` + 触发词列表

### 主体（Markdown Body）—— 极简原则

```markdown
# 技能标题

## 使用说明

1. 读取 [参考文件](references/xxx.md) 了解规范
2. 对照 [检查清单](references/checklist.md) 逐项验证
3. 输出报告 / 执行修复

**核心原则：** 一句话总结
```

**严格约束：**

| 规则 | 说明 |
|------|------|
| 主体 ≤ 500 行 | 理想 ≤ 20 行，超出时拆到 `references/` |
| **禁止代码块** | 代码/命令/SQL 必须放 `scripts/` 或 `references/` |
| 禁止"何时使用"节 | 该内容应只在 description 字段 |
| 禁止重复 references 内容 | 每条信息只在一处维护 |
| 引用必须标注触发条件 | 如"**步骤3时**读取 xxx.md" |

### 主体四种结构模式

1. **基于工作流**（顺序过程）：`概述 → 工作流决策树 → 步骤1 → 步骤2…`
2. **基于任务**（工具集合）：`概述 → 快速开始 → 任务A → 任务B…`
3. **参考/指南**（标准规范）：`概述 → 指南 → 规范 → 用法…`
4. **基于能力**（集成系统）：`概述 → 核心能力 → 1.功能 → 2.功能…`

---

## 四、触发器约定

### 两级触发机制

```
┌─────────────────────────────────────────────┐
│ 第1级：description 前缀（始终可见）          │
│  "Must follow when" → 上下文匹配自动触发      │
│  "Use when"        → 用户提示词匹配触发       │
├─────────────────────────────────────────────┤
│ 第2级：触发词（description 内声明）          │
│  "触发词：检查checklist规范、checklist审查"   │
└─────────────────────────────────────────────┘
```

### 触发模式

| 模式 | 适用类型 | 机制 |
|------|----------|------|
| **上下文驱动** | best-practice | AI 遇到相关代码时自动加载（如编写 DAO 时自动加载 `dao-best-practice`） |
| **关键词驱动** | 动词型 | description 中声明触发词，用户说出关键词时触发 |
| **链式触发** | 工作流型 | 技能完成后硬性指定下一个技能（如 brainstorming → writing-plans → subagent-driven-development） |
| **批量触发** | check-all-* | 自动发现匹配前缀的技能并依次执行（如 `check-all-best-practices` 自动发现所有 `*-best-practice`） |

### 技能链（硬 Gate）

```
brainstorming ──→ writing-plans ──→ subagent-driven-development
                                      │
                                      └── test-driven-development (每个任务)
```

箭头上方标注了硬性约束——如 brainstorming 完成后**只能**进入 writing-plans，不得跳过。

---

## 五、输入/输出格式

### 输入（渐进式加载）

```
始终加载：  YAML frontmatter (name + description)
触发加载：  SKILL.md 主体（~20行）
按需加载：  references/ 文件（checklist.md、standard.md、workflow.md）
不加载：    scripts/、assets/（通过命令行调用，不占上下文）
```

### 输出（标准化报告模板）

**检查报告 JSON Schema：**

```json
{
  "skill_name": "my-skill",
  "status": "pass|warning|error",
  "stats": { "total": 20, "pass": 19, "warning": 1, "error": 0 },
  "checks": [
    {
      "name": "naming_convention",
      "status": "pass",
      "message": "目录名 'my-skill' 符合命名规范",
      "fix_suggestion": ""
    }
  ]
}
```

**严重级别：**

- **error**：违反强制规范，必须修复（如缺少必需字段、禁用文件）
- **warning**：建议修复但不阻断（如 description 长度略超）
- **pass**：完全合规

### Checklist 格式规范

```markdown
- [ ] 1.1 判定项（可明确判断 true/false）
- [ ] 1.2 每条至少一个正确或错误示例
- [ ] ❌ 不存在反模式情况（Bad Case 节）
```

两类 checklist：
- **规范 Checklist**：定义规则（编号格式、含 Bad Case 节、每条有示例）
- **操作完成 Checklist**：验证执行（5-8 条、动作导向语态）

---

## 六、上下文管理策略

### 核心原则：信息密度最大化

```
┌──────────────────────────────────────────────────────┐
│  上下文预算分配                                       │
│  ┌──────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ frontmatter   │  │ body     │  │ references     │  │
│  │ ~150 chars    │  │ ≤20行    │  │ 按需加载        │  │
│  │ 始终在上下文中 │  │ 触发后加载│  │ 用完即释放      │  │
│  └──────────────┘  └──────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### 六条上下文铁律

1. **信息单一来源**：SKILL.md 与 references 不得重复内容，每条信息只在一处维护
2. **一级引用深度**：SKILL.md → references/*，禁止 references 间互相引用形成链条
3. **渐进式披露**：前言→主体→references 逐层加载，AI 按需读取
4. **禁止内联代码**：所有代码块移至 `scripts/` 或 `references/`，SKILL.md 只保留步骤指引
5. **引用带触发条件**：每个 `references/xxx.md` 链接旁必须说明"何时读取"
6. **主体极致精简**：目标 ≤ 20 行，绝对上限 500 行

---

## 七、命名最佳实践与边界约定

### 目录命名

```
正则：^[a-z0-9]+(-[a-z0-9]+)*$
长度：≤ 64 字符
```

| 规则 | ✅ 正确 | ❌ 错误 |
|------|---------|---------|
| kebab-case | `dao-best-practice` | `DAO_BestPractice` |
| 无首尾连字符 | `pdf-parser` | `-pdf-parser`、`pdf-parser-` |
| 无连续连字符 | `check-list` | `check--list` |
| 动词+名词语序 | `create-skill`、`check-components` | `skill-creator`、`classname-refactor` |
| 无赘余 `-skill` 后缀 | `exam-grading`（除非：`create-skill`） | `exam-grading-skill` |
| `name` 与目录一致 | 目录 `log-monitor` → `name: log-monitor` | 目录 `log-monitor` → `name: log-monitor-skill` |

### 动词前缀体系

| 前缀 | 语义 | 示例 |
|------|------|------|
| `check-` | 检查/验证是否符合规范 | `check-checklist`、`check-components` |
| `implement-` | 按规范实现/执行 | `implement-feature`、`implement-split` |
| `integrate-` | 集成外部库/工具 | `integrate-better-auth`、`integrate-zod-env` |
| `refactor-` | 重构/转换代码 | `refactor-classname`、`refactor-ui-components` |
| `create-` | 创建/生成 | `create-skill` |
| `generate-` | 生成制品 | `generate-preview` |
| `fix-` | 修复问题 | `fix-all-best-practices` |
| `clean-` | 清理代码 | `clean-hardcode` |
| `remove-` | 删除内容 | `remove-comments` |

### 技能边界
**一个技能只做一件事，通过链式组合完成复杂工作流：**
```
设计阶段：    brainstorming ──→ writing-plans
实现阶段：    subagent-driven-development ──→ test-driven-development
质量阶段：    check-all-best-practices ──→ fix-all-best-practices
```

**技能间关系声明模板（SKILL.md 中）：**
```markdown
## 与其他技能的关系

| 上游 | 当前 | 下游 |
|------|------|------|
| brainstorming | writing-plans | subagent-driven-development |
```

### 领域覆盖

| 领域 | best-practice | check | implement/fix |
|------|---------------|-------|---------------|
| 组件设计 | `component-design-*`、`component-unit-*` | `check-components`、`check-all-components-design` | `implement-split` |
| 数据流/状态 | `use-store-not-props-*`、`store-*` | `check-props-drilling` | — |
| 数据层 | `dao-*`、`db-table-*`、`schema-*`、`service-*`、`repository-*` | — | — |
| tRPC | `refine-trpc-*` | `check-refine-trpc` | `implement-trpc-query` |
| 类型系统 | `zod-infer-type-*` | `check-zod-infer-type` | — |
| 错误处理 | `error-handling-*` | `check-error-handling` | — |
| UI | `ui-components-*`、`svg-icon-*` | `check-ui-components`、`check-svg` | `refactor-ui-components` |
| 表单 | `form-*` | — | — |
| 导出 | `barrel-export-*`、`no-re-export-*` | `check-barrel-export` | — |
| Skill 质量 | `skill-*`、`checklist-*` | `check-all-skills`、`check-checklist` | `create-skill` |
| 工作流 | — | — | `brainstorming`、`writing-plans`、`subagent-driven-development`、`test-driven-development` |

---

## 八、核心模式总结

```
                    ┌──────────────────────┐
                    │     SKILL.md          │
                    │  name + description   │  ← 始终在上下文
                    │  (YAML frontmatter)   │
                    ├──────────────────────┤
                    │  使用说明（≤20行）     │  ← 触发后加载
                    │  1. 读取 references/A  │
                    │  2. 对照 checklist.md  │
                    │  3. 输出/执行          │
                    └──┬──────┬──────┬─────┘
                       │      │      │
              ┌────────▼┐ ┌──▼───┐ ┌▼────────┐
              │standard │ │check │ │workflow  │  ← 按需加载
              │.md      │ │list  │ │.md       │
              │(规范定义)│ │.md   │ │(流程步骤)│
              └─────────┘ └──────┘ └──────────┘
```

### 四条核心设计原则

1. **渐进式披露** — 前言常驻（150字符），主体精简（20行），细节按需加载
2. **职责分离** — best-practice 定义规范 / check 验证规范 / implement 执行规范
3. **信息不重复** — 每条规则只在一处定义，SKILL.md 只做路由，不做容器
4. **链式组合** — 单技能做单件事，通过硬 Gate 串联为完整工作流
