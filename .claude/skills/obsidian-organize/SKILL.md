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

### 4. 收尾

1. 处理完所有文件后，提示用户审阅
2. 用户确认后，让用户提交 commit（不自动提交）
3. 打 tag：

```bash
git tag obsidian-organized-$(date +%Y-%m-%d)
```

## 规范化规则

<!-- TODO: 用户会补充具体的规则 -->

> **占位符**：等待用户提供具体规则后填充。
> 预期内容：frontmatter 格式、标题层级、标签体系、目录组织、链接规范、代码块风格等。

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
