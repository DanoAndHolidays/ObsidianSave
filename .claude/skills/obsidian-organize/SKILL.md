---
name: obsidian-organize
description: Use when user asks to organize, clean up, or normalize notes in this Obsidian vault. Identifies changed/new notes via git diff against the last `obsidian-organized-*` tag, then applies normalization rules file-by-file. Handles each file with confidence-tiered behavior: high-confidence fixes applied directly, medium-confidence fixes preserve original content as italic for user review, low-confidence items pause to ask the user.
---

# Obsidian 整理

## 概述

整理本仓库（Obsidian 笔记）的核心 skill：基于 git tag 基线找出新增/修改的笔记，逐个文件应用规范化规则。

**核心原则**：边扫边改，把握度分档，保留用户原始内容可追溯。

## 触发

当用户说类似以下的话时调用：

- "整理 obsidian 仓库"
- "规范笔记"
- "normalize notes"
- "整理一下笔记"

## 工作流

### 1. 确定基线

```bash
# 查找最近的 obsidian-organized-* tag
git tag --list 'obsidian-organized-*' --sort=-creatordate | head -1
```

- **有 tag**：用最新 tag 作为基线
- **没 tag**：询问用户指定基线（commit / tag / 分支名）
- **完全第一次整理**：建议从一周前或某个明显的 commit 开始

### 2. 找出变更的笔记

```bash
# 列出新增(A)和修改(M)的 markdown 文件
git diff <基线>..HEAD --name-status -- '*.md'
```

过滤规则：

- ✅ 保留：状态为 `A`（新增）或 `M`（修改）
- ❌ 跳过：状态为 `D`（删除）
- ❌ 跳过：路径包含 `.obsidian/`、`attachments/`、`docs/superpowers/specs/`

### 3. 逐个文件处理

对每个变更文件按顺序处理：

1. **读取**当前内容
2. **应用规则**（见下方「规范化规则」章节）
3. **按把握度处理**：

| 把握度 | 处理方式 |
|--------|---------|
| 🟢 高 | 直接修改（错别字、明显格式错误、必填字段缺失） |
| 🟡 中 | 在原位置保留原内容为斜体（用 `*...*`），新规范内容紧随其后 |
| 🔴 无 | 暂停，列出问题点用 AskUserQuestion 请用户决定 |

**斜体保留示例**：

```markdown
## 标题

*原标题：随机起的一个名字*

## 标准化的标题
```

> **🟡 斜体 vs 例外斜体**：🟡 斜体是**临时的**（用 `*原xxx：...*`），留给用户审阅后决定去留。规则6 的例外斜体是**永久的**（含日期+【理由】+原内容），用于标明故意的规则偏离。**不要**在 🟡 场景套用例外格式模板，反之亦然。

### 4. 收尾

1. 处理完所有文件后，提示用户审阅
2. 用户确认后，让用户提交 commit（不自动提交）
3. 打 tag：

```bash
git tag obsidian-organized-$(date +%Y-%m-%d)
```

## 规范化规则

> 完整规则详见 [`reference/normalization-rules.md`](reference/normalization-rules.md)。速查正反例见 [`reference/formatting-rules.md`](reference/formatting-rules.md)。如有冲突以 normalization-rules.md 为准。

**七条规则速览**：

| # | 规则 | 核心要点 |
|---|------|---------|
| 1 | 标题层级 | H1/H2/H3/H5 可用；H4/H6+ 禁用；H1=文件名；H3 取代粗体伪标题 |
| 2 | 分隔符 | **所有 H2 前**必有 `---`；H3 前**不得**使用 `---` |
| 3 | 空行 | 标题后**不空行**直接接内容（唯一例外：接引用块时空一行） |
| 4 | 代码块 | 必须指定语言标签；不确定用 `text` |
| 5 | 链接 | 内部用 `[[双链]]`，外部用 `[文本](url)` |
| 6 | 例外说明 | 用斜体 `*日期 【理由】原内容：xxx*` 标注 |
| 7 | 不碰的领域 | 语义正确性、frontmatter、标签体系、目录迁移、引用关系 |

**🟡 斜体 vs 例外斜体**：🟡 斜体是**临时的**（`*原xxx：...*`），留给用户审阅。例外斜体是**永久的**（含日期+【理由】），标明故意偏离。

## 边界情况

| 情况 | 处理 |
|------|------|
| 没有变更文件 | 告知用户"自基线以来无笔记变更"，结束 |
| 变更 > 20 个文件 | 先告知数量，问用户是否要继续 |
| 遇到非 markdown 文件 | 跳过 |
| 文件路径含 `.obsidian/`、`attachments/` | 跳过 |
| 文件被用户在工作区手动修改过 | 先读最新内容，git diff 显示的状态可能滞后 |

## 反模式

- ❌ 一次性批量改完不跟用户确认
- ❌ 把拿不准的"规范化"强行套上去
- ❌ 跳过斜体保留环节，让用户失去原内容
- ❌ 自动 commit（让用户自己决定提交信息和时机）
- ❌ 整理 `.obsidian/`、`attachments/` 等系统目录

## 性能优化

**两阶段执行**：

1. **机械修复**（脚本）：跑 `scripts/normalize.py --write <file>` 处理所有正则可解的违规（见下方脚本违规表）。1 次 Bash 调用搞定。
2. **判断修复**（Claude）：用 Read 拿脚本报告 + 当前内容，对脚本无法处理的违规（代码块语言修正、粗体伪标题→H3、例外斜体标注、引用块空行）用 Write 一次性重写。

具体执行清单：

- **先跑脚本**：scripts/normalize.py --write 自动修掉 ~90% 违规
- **再读文件**：Read 拿脚本修改后的内容
- **大改用 Write**：判断性修复涉及 3+ 处时，Write 整个文件（1 次调用），不要用 Edit × N
- **小改用 Edit**：1-2 处微调用 Edit
- **绝不 re-read**：Edit 失败直接扩大 old_string 重试
- **不展示 git diff**：用户自己会看
- **不建任务**：单文件整理不 TaskCreate
- **输出极简**：1-2 句清单 + 改动数量

## 脚本使用

```bash
# 只报告不修改
python scripts/normalize.py <file.md>

# 写回文件
python scripts/normalize.py --write <file.md>

# JSON 输出（供其他工具消费）
python scripts/normalize.py --json <file.md>
```

脚本覆盖的机械违规（`--write` 全部自动修）：

| 违规 | 处理 |
|------|------|
| 标题前数字/中文数字标号 | 去除 |
| H4 标题 | 升 H5 |
| 文件无 H2 时所有 H3 升 H2 | 升 H2 |
| H1 缺/过时元信息块 | 插入 / 更新时间戳 |
| H1 下方的裸 URL | 包成 `[URL](URL)` |
| H3 前误用的 `---` | 删除 |
| 所有 H2 紧上方缺 `---` | 插入 |
| 标题后多余空行 | 删除（引用块除外） |
| 代码块前/后缺空行 | 按规则补 |
| 中文标点后多余空格 | 去除 |
| 代码块缺/非法语言标签 | **仅报告**，Agent 判断后改 |

Agent 判断类违规（脚本不做）：

| 违规 | 处理 |
|------|------|
| 代码块缺/错误语言标签 | 高把握直接改，不确定用 `text` |
| H2 下粗体伪标题 | 升级为 H3 |
| 例外斜体标注 | 用 `*日期 【理由】原内容：xxx*` 格式 |
| 引用块空行等复杂场景 | 按规则判断 |
| 规则7范围外的问题 | 停下来问用户 |
