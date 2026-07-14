---
name: obsidian-organize
description: Organize and normalize changed Markdown notes in this Obsidian vault. Use when the user asks to整理、清理、规范化或检查 Obsidian 笔记格式. Collect committed and working-tree changes since the latest obsidian-organized-* tag, apply deterministic script-based formatting, preserve YAML frontmatter and note meaning, and report only issues that require human judgment.
---

# Obsidian 笔记整理

以脚本为主完成候选收集、格式修复和验证。Agent 不手工重复脚本能确定处理的格式任务，只处理脚本报告的 `manual_issues`。

## 首选流程

在仓库根目录先预览：

```bash
python .claude/skills/obsidian-organize/scripts/organize_changed_notes.py
```

根据 JSON 报告执行：

1. `collection.error=missing_baseline`：询问用户使用哪个 commit、tag 或分支，不自行猜测。
2. 退出码为 3 或 `collection.over_limit=true`：报告数量；用户确认后加 `--force-over-limit`。
3. `manual_issue_count>0`：只读取对应文件和行号，处理无法推断的问题。
4. 预览无异常后写回：

```bash
python .claude/skills/obsidian-organize/scripts/organize_changed_notes.py --write
```

5. 再运行一次预览。要求 `changed_count=0`、`code_issue_count=0`；否则先修脚本或报告原因，不继续手工批量格式化。

超过 20 个文件并经用户确认时：

```bash
python .claude/skills/obsidian-organize/scripts/organize_changed_notes.py --write --force-over-limit
```

## 脚本职责

`collect_changed_notes.py` 自动：

- 选择最新 `obsidian-organized-*` tag
- 合并 `<tag>..HEAD` 与 staged、unstaged、untracked Markdown 文件
- 跳过删除、重命名、`.obsidian/`、`attachments/`、`docs/superpowers/specs/`、`.claude/skills/`、`.agents/`、`.codex/`
- 去重并执行 20 文件阈值

`normalize.py` 自动：

- 完整保留 YAML frontmatter
- 用带边界的定长占位符保护任意数量的 fenced code 内容
- 让 H1 存在并与文件名一致，维护时间戳和 H1 区域空行
- 修复 H2-H6 数字前缀、H4/H6、无 H2 时的 H3、短粗体伪标题
- 自动删除文件末尾无内容的空标题；仅报告后面仍有内容的空标题
- 修复 H2 分隔符、标题空行、代码块周边空行、中文标点空格和 H1 裸 URL
- 为缺失代码块标签自动使用 `text`，修复带后缀的闭合围栏
- 报告未知、未闭合代码围栏和空标题
- 保证重复运行幂等；写回必须使用预览时的同一份计算结果
- CLI 只在入口配置 Windows UTF-8，模块导入不得修改全局输出流

单文件排查时才直接运行：

```bash
python .claude/skills/obsidian-organize/scripts/normalize.py --json <file.md>
python .claude/skills/obsidian-organize/scripts/normalize.py --write <file.md>
```

## Agent 处理范围

仅处理下列脚本无法可靠推断的内容：

- 空标题应删除还是补成什么标题
- 引用块等仍被报告的复杂结构
- 永久例外说明
- 规则之外的语义、frontmatter、标签、目录或引用关系问题；必须先问用户

详细规则见 [规范化规则](reference/normalization-rules.md)，正反例见 [格式速查](reference/formatting-rules.md)，完整结构见 [结构示例](reference/structure-example.md)。冲突时以 `normalization-rules.md` 为准。

## 验证与安全边界

修改脚本后运行：

```bash
python -m unittest discover -s .claude/skills/obsidian-organize/tests -v
```

回归测试至少覆盖 frontmatter、超过 10 个代码块、占位符碰撞、代码围栏、H1/文件名、伪标题、空标题、链接幂等、Git 候选收集和“预览→写回→零改动预览”。

- 不修改笔记语义、frontmatter、标签体系、目录结构或引用关系。
- 不覆盖用户的新改动；始终从磁盘读取最新内容。
- 不自动 commit 或打 tag。
- 没有候选文件时直接报告。

用户审阅并自行提交后，才建议创建 `obsidian-organized-YYYY-MM-DD` tag。
