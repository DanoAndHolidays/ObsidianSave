# Obsidian 整理 Skill 设计

**日期**：2026-06-12
**状态**：框架已批准，等待用户补充规范化规则

## 目标

创建一个 Claude Code skill，让用户在需要整理 Obsidian 仓库时能被自动调用，主要流程：

1. 通过 git diff 找出指定基线以来的新增/修改笔记
2. 按既定规则规范化这些笔记的内容

## 存放位置

- **项目级 skill**：`G:\Save\Obsidian\ObsidianSave\.claude\skills\obsidian-organize\SKILL.md`
- 跟随项目版本控制

## 触发条件

- 用户说"整理 obsidian 仓库"、"规范笔记"、"normalize notes"等
- 用户要求批量处理新写的 markdown 笔记

## 工作流

### 第一步：确定基线

- 查找 `obsidian-organized-*` tag 列表，按时间倒序
- 找到最新的 tag 作为基线
- 如果没有任何 tag，询问用户："这是第一次整理，请指定一个基线（commit/tag/日期）"

### 第二步：找出变更的笔记

- 运行 `git diff <基线>..HEAD -- '*.md' --name-status`
- 关注 `A`（新增）和 `M`（修改）状态
- 排除删除的笔记（`D`）和特殊目录（如 `.obsidian/`、`attachments/`）

### 第三步：逐个文件处理

对每个变更文件：

1. 先读取当前内容
2. 应用规范化规则
3. 根据把握度分三档处理：

| 把握度 | 处理方式 |
|--------|---------|
| 🟢 高把握 | 直接修改（如：删除多余空行、补全 frontmatter、修正标题层级） |
| 🟡 中等把握 | 把原内容以斜体保留，新规范内容跟在后面（让用户后续可清理） |
| 🔴 无把握 | 暂停，列出问题点请用户决定 |

### 第四步：收尾

- 全部处理完后，提示用户审阅
- 用户确认后，提交 commit
- 打 tag：`git tag obsidian-organized-YYYY-MM-DD`

## 待补充

- [ ] 具体的规范化规则（frontmatter 字段、标题风格、标签体系、目录组织等）

## 边界情况

- 没有变更 → 直接告知用户，无需处理
- 大量变更（>20 个文件）→ 提醒用户确认范围
- 文件不是 markdown → 跳过
- 文件在 `.obsidian/` 或 `attachments/` → 跳过
