---
name: obsidian-organize
description: Review, organize, and diagnose Markdown notes in this Obsidian vault. Use when the user asks to整理、清理、规范化、审核、复查或检查 Obsidian 笔记. Mechanical formatting is enforced automatically for staged notes by the repository pre-commit hook; when invoked, collect changes since the latest obsidian-reviewed-* tag, verify formatting, review fluency/correctness/order, and add validated audit markers for semantic adjustments.
---

# Obsidian 笔记整理

仓库采用两层流程：Git 提交时由确定性脚本自动完成机械格式化；用户调用本技能时，Agent 才逐篇完整阅读并审核内容。Agent 不手工重复脚本能确定的格式任务；凡是改变表达、事实、代码含义或章节顺序的语义调整，都必须按 `CR-xxx` 协议留下可见锚点和完整变更记录。

## 日常提交自动化

仓库使用 `.githooks/pre-commit`。首次克隆后安装一次：

```bash
git config --local core.hooksPath .githooks
```

之后正常执行 `git add` 和 `git commit` 即可。hook 自动：

- 只收集暂存区中的新增、复制、修改或重命名笔记
- 在内存中运行机械规则直到固定点，再一次性写回并重新暂存
- 跳过 `CLAUDE.md`、`README.md`、技能目录、附件目录和 Obsidian 配置
- 对空标题、未知代码语言等 Agent 问题只警告，不阻止提交
- 对未闭合代码围栏、不收敛、文件在运行中变化等硬错误阻止提交
- 发现同一笔记同时有已暂存与未暂存修改时停止，避免误提交未暂存内容

hook 不调用 Agent、不访问网络、不做语义调整，也不受 20 文件审核阈值限制。直接排查暂存笔记时运行：

```bash
python .claude/skills/obsidian-organize/scripts/format_staged_notes.py --json
```

## 技能按需审核流程

用户明确要求整理或审核时，在仓库根目录先预览：

```bash
python .claude/skills/obsidian-organize/scripts/organize_changed_notes.py
```

根据 JSON 报告执行：

1. `collection.error=missing_baseline`：询问用户使用哪个 commit、tag 或分支，不自行猜测。优先使用最新 `obsidian-reviewed-*`，不存在时兼容旧 `obsidian-organized-*`。
2. 退出码为 3 或 `collection.over_limit=true`：报告数量；用户确认后加 `--force-over-limit`。
3. `manual_issue_count>0`：只读取对应文件和行号，处理无法推断的问题。
4. 预览无异常后写回：

```bash
python .claude/skills/obsidian-organize/scripts/organize_changed_notes.py --write
```

5. 再运行一次预览。要求 `changed_count=0`；未闭合围栏等硬错误必须解决。未知语言、空标题等判断项可记录后进入 Agent 审核。
6. 按候选列表逐篇完整阅读，依照 [内容审核与变更标记规则](reference/content-review-rules.md) 检查流畅性、事实、代码、顺序、完整性、去重和术语。不能只读脚本报告的行号。
7. 高把握问题直接修复；事实与代码调整先用官方/一手来源验证。低把握或来源冲突的问题不猜测，向用户说明。
8. 每个语义调整添加唯一可见锚点 `〔CR-xxx〕`，并在笔记末尾的 `## 内容审核变更记录` 中逐项记录日期、位置、原内容、调整后、原因和依据。
9. 语义调整后再次执行写回与预览，直到以下计数全部为 0：

```text
changed_count
code_issue_count
manual_issue_count
review_marker_issue_count
```

最终报告候选篇数、实际完整审核篇数、语义调整数（`review_entry_count`）及未解决问题。候选篇数与审核篇数不一致时不得声称完成。

超过 20 个候选并经用户确认进行 Agent 审核时：

```bash
python .claude/skills/obsidian-organize/scripts/organize_changed_notes.py --write --force-over-limit
```

## 脚本职责

`collect_changed_notes.py` 自动：

- 选择最新 `obsidian-reviewed-*` tag；不存在时兼容旧 `obsidian-organized-*`
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
- 为缺失代码块标签自动使用 `text`，规范化已知语言标签大小写与别名，修复带后缀的闭合围栏
- 报告未知、未闭合代码围栏和空标题
- 单次调用在内存中运行到固定点；循环或超过 5 轮时拒绝写回
- 保证重复运行幂等；写回必须使用预览时的同一份计算结果
- CLI 只在入口配置 Windows UTF-8，模块导入不得修改全局输出流

`format_staged_notes.py` 自动：

- 只机械格式化暂存笔记，并自动重新暂存实际发生变化的文件
- 预览所有目标后再写回，避免某篇硬错误导致半批次修改
- 拒绝部分暂存笔记，防止扩大用户本次提交范围
- 将需要 Agent 判断的问题作为软警告留待本技能按需处理

`validate_content_review.py` 自动：

- 校验 `〔CR-xxx〕` 可见锚点与 `### CR-xxx｜类型` 记录一一对应
- 拒绝重复编号、孤立锚点、孤立记录和代码块内锚点
- 要求日期、位置、原内容、调整后、原因、依据字段完整
- 校验允许的审核类型、日期格式和事实/代码纠错的依据要求
- 要求内容审核变更记录位于笔记末尾

单文件审核标记排查：

```bash
python .claude/skills/obsidian-organize/scripts/validate_content_review.py --json <file.md>
```

单文件排查时才直接运行：

```bash
python .claude/skills/obsidian-organize/scripts/normalize.py --json <file.md>
python .claude/skills/obsidian-organize/scripts/normalize.py --write <file.md>
```

## Agent 处理范围

Agent 负责下列脚本无法可靠推断的内容：

- 空标题应删除还是补成什么标题
- 引用块等仍被报告的复杂结构
- 永久例外说明
- 不流畅、歧义、上下文跳跃
- 事实错误、代码错误、注释与正文不一致
- 定义/前提/结论顺序不当，重复或缺少关键前提
- 术语和大小写不一致

语义修改必须遵守 `content-review-rules.md`；frontmatter、标签、目录、附件和引用关系仍须用户明确授权。

机械格式规则见 [规范化规则](reference/normalization-rules.md)，正反例见 [格式速查](reference/formatting-rules.md)，语义审核见 [内容审核与变更标记规则](reference/content-review-rules.md)，完整结构见 [结构示例](reference/structure-example.md)。机械格式冲突时以 `normalization-rules.md` 为准；内容审核与标记冲突时以 `content-review-rules.md` 为准。

## 验证与安全边界

修改脚本后运行：

```bash
python -m unittest discover -s .claude/skills/obsidian-organize/tests -v
```

回归测试至少覆盖 frontmatter、超过 10 个代码块、占位符碰撞、代码围栏、语言标签规范化、H1/文件名、伪标题、空标题、链接幂等、单次调用固定点、Git 候选收集、暂存区自动重写、部分暂存保护、“预览→写回→零改动预览”，以及有效/无效内容审核标记。

- 允许在完整审核后修改笔记表达、事实、代码和顺序，但每个语义调整必须可追溯。
- 不静默改变作者核心观点；不确定时先询问用户。
- 不修改 frontmatter、标签体系、目录结构、附件或引用关系，除非用户明确授权。
- 不覆盖用户的新改动；始终从磁盘读取最新内容。
- 不自动 commit 或打 tag。
- 没有候选文件时直接报告。

用户审阅并自行提交后，才建议创建 `obsidian-reviewed-YYYY-MM-DD` tag。机械格式化由提交 hook 保证，不再为它创建单独 tag。
