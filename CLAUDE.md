# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是个人 **Obsidian 笔记库**（Git 同步），不是软件项目。内容以中文 Markdown 笔记为主，包含前端、后端、面试、AI 工具、学习记录等方向的学习沉淀与项目笔记。所有笔记都经过 AI 辅助撰写，可能含有错误信息（见 `index.md` 末段说明）。

## 目录结构

- `前端/` `后端/` `学习/` `公共技术/` `AI/` `docs/` — 笔记主题分类（具体子目录按需探索）
- `attachments/` `附件/` — 图片、PDF 等资源
- `.obsidian/` — Obsidian 自身配置，**不要**手工修改
- `.claude/skills/obsidian-organize/` — 笔记规范化 skill（核心工具）
- `index.md` / `README.md` — 知识库入口

## 核心 skill：obsidian-organize

负责把新增/修改的笔记按规范化规则整理。工作流详见 `.claude/skills/obsidian-organize/SKILL.md`，但日常最常用的入口是直接调用其脚本：

```bash
# 查看哪些机械违规可修（不写文件）
python .claude/skills/obsidian-organize/scripts/normalize.py <file.md> [file2.md ...]

# 写回修复结果
python .claude/skills/obsidian-organize/scripts/normalize.py --write <file.md> [file2.md ...]

# JSON 输出供其他工具消费
python .claude/skills/obsidian-organize/scripts/normalize.py --json <file.md>
```

脚本只做**纯正则可解的机械修复**（H4→H5、文件无 H2 时 H3 升 H2、H1 元信息块时间戳、`---` 分隔符、代码块空行等），不做语义判断。判断性修复（标题层级重构、斜体保留例外等）由 Claude 配合 `Edit` / `Write` 完成。

整理时**跳过**以下路径：`.obsidian/`、`attachments/`、`docs/superpowers/specs/`。

## Git Tag 约定

每次整理完一轮笔记，**必须**打 tag 作为下次整理的基线：

```bash
git tag obsidian-organized-YYYY-MM-DD-N   # N 为当天序号，1, 2, 3 ...
```

查询最近基线 tag：

```bash
git tag --list 'obsidian-organized-*' --sort=-creatordate | head -1
```

skill 默认取最新 `obsidian-organized-*` tag 作为 `git diff` 基线。

## 提交信息风格

参考最近 commit 沿用的约定：

- `chore: 整理 X 篇 Y 笔记` — 单/多篇笔记规范化
- `feat(obsidian-organize): <要点>` — skill 规则或脚本调整
- `fix(obsidian-organize): <要点>` — skill bugfix

## Python 运行环境

脚本对 Windows 终端做了 UTF-8 stdout 包装（见 `normalize.py` 顶部）。在 Windows + Git Bash 下可直接 `python` 调用，无需额外编码参数。macOS / Linux 无需特殊处理。
