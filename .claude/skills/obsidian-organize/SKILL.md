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

### 1. 标题层级

允许的标题层级：**H1、H2、H3、H5**（H4 禁用，H6 及以上禁用）

| 层级 | 用途 |
|------|------|
| H1 | 整篇文档标题，有且只有一个，与文件名（去掉 `.md`）完全一致；**紧跟一行** `> Last Format Time：M/D/YYYY HH:MM:SS` 元信息块 |
| H2 | 主要章节 |
| H3 | H2 下的子章节；同时**取代** H2 下的粗体小标题（如 `**核心结论**：`、`**实战场景**：`） |
| ~~H4~~ | **禁用**（跳过直接用 H5，或重新组织层级） |
| H5 | 仅在 H3 下需要进一步细分时使用 |

- H1 下面紧跟 `> Last Format Time：...` 元信息块（不空行）
- 元信息块后再接引言/第一段正文 / 外部链接（中间空一行）
- H2 下面不要再用 `**粗体小标题**：` 这种伪标题，**必须**升级为 H3
- 任何标题前都不要加数字标号（如 `## 1. 标题`、`### 1. xxx` 都是违规）

**H1 元信息块格式**（脚本自动维护）：

```markdown
# 文档标题
> Last Format Time：6/12/2026 19:19:42 

（外部链接，如无链接则此区域为空）

---
## 二级标题
```

```markdown
# 文档标题
> Last Format Time：6/12/2026 19:19:42 
## 二级标题
```

- 紧跟 H1，不空行
- 链接区域是 H1/meta 之下的连续行，裸 URL 自动包成 `[URL](URL)`
- 有链接时：H1/meta → 空行 → 链接 → 空行 → `---` → H2
- 无链接时：H1/meta → 直接接 H2

**例外处理**：若不能遵守（如 H1 与文件名不一致），在违规位置用斜体说明原因。

### 2. 分隔符

**非首个 H2 紧上面（不空行）放一个 `---` 分隔符**：

```markdown
上一节的最后一段正文
（空行）
---
## 下一个二级标题
（直接接正文，不空行）
```

**H1 跟第一个 H2 之间的 `---` 由"链接"决定**：

- H1 区域到 H2 之间有外部链接或裸 URL → 加 `---`
  ```markdown
  # Fetch API
  > Last Format Time：6/12/2026 19:19:42 

  [MDN文档](https://...)

  ---
  ## 二级标题
  ```
- H1 区域到 H2 之间**无**链接 → 不加 `---`（紧挨 H2）
  ```markdown
  # Fetch API
  > Last Format Time：6/12/2026 19:19:42 
  ## 二级标题
  ```

### 3. 空行规则

| 位置 | 规则 |
|------|------|
| 标题 → 紧跟的正文/列表/代码块 | **不空行** |
| 标题 → 紧跟的 `> 引用块` | **空一行**（引用是独立块） |
| 上一段正文结尾 → 下一个标题 | **空一行** |
| 上一段正文/标题 → 紧跟的列表 | **不空行** |
| 列表项之间 | 不空行 |
| 代码块前 | 紧跟标题/列表/描述性文字（如"如下代码："、"举例："）→ **不空行**；其他正文 → **空一行** |
| 代码块后 | 紧跟列表 → **不空行**；其他（标题/段落/引用块/代码块）→ **空一行**（代码块算正文） |
| 引用块 `> ` 前后 | 各空一行 |
| 不同章节之间 | 空一行 + `---` |

**列表项的推荐格式**（标题/正文后直接接列表，不空行）：

```markdown
## 章节标题
（不要空行）
- 第一点
- 第二点
- 第三点
```

### 4. 代码块

- **必须**指定语言标签
- 合法标签：jsx、tsx、ts、js、javascript、css、scss、html、bash、sh、shell、json、yaml、md、markdown、text
- 选错语言属于高把握违规 → 直接改成正确语言
- `js` 和 `javascript`、`md` 和 `markdown`、`bash` 和 `sh`/`shell` 都视为合法等价
- 不确定时优先选 `text` 而不是省略

### 5. 链接

- **内部笔记**：`[[双链]]`（指向仓库内其他笔记）
- **外部资源**：标准 markdown 链接 `[文本](url)`
- 两种都可以，按场景选最自然的

### 6. 例外说明

任何规则都允许有例外。例外必须**用斜体**在文档中标注，斜体里必须包含：

- **修改时间**：日期，格式 `M/D/YY`（如 `6/12/26`）
- **为什么**：方括号 `【】` 里的简短理由
- **原内容**：保留的原始文本
- **修改点**：本次具体改了什么（修改点显而易见时可省略）

格式模板：

```markdown
*<日期> 【<理由>】
原内容：<原始文本>*
```

**示例 1**：保留 AI 提问作为笔记上下文

```markdown
## useEffect 依赖项规则

*6/12/26 【保留 AI 提问作为笔记上下文】
原内容：要不要我整理一份 useEffect 依赖项数组的完整规则表？*

### 依赖项规则表
```

**示例 2**：旧标题因历史原因保留

```markdown
*6/12/26 【历史笔记保留原标题】
原内容：# 旧标题
修改点：保持 H1 = 文件名，移除原 H1*
```

斜体块放在原内容位置（或紧跟其后），新规范内容紧随其后。

### 7. 不在规则内的事项

以下内容**不**做规范化（避免过度发挥）：

- 内容的语义正确性
- 是否加 frontmatter
- 标签体系
- 目录迁移
- 笔记之间的引用关系

如果发现这些层面的问题，**停下来问用户**，不要自作主张。

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

1. **机械修复**（脚本）：跑 `scripts/normalize.py` 处理正则可解的违规（数字标号、H4→H5、标点空格、代码块语言）。1 次 Bash 调用搞定。
2. **判断修复**（Claude）：用 Read 拿脚本报告 + 当前内容，对需要上下文判断的修复（空行调整、--- 分隔符、H2 包装、斜体例外等）用 Write 一次性重写。

具体执行清单：

- **机械违规用脚本**：scripts/normalize.py 跑一遍，自动修掉绝大多数违规
- **大改用 Write**：判断性修复涉及 3+ 处时，Write 整个文件（1 次调用），不要用 Edit × N
- **小改用 Edit**：1-2 处微调用 Edit
- **绝不 re-read**：Edit 失败直接扩大 old_string 重试
- **不展示 git diff**：用户自己会看
- **不建任务**：单文件整理不 TaskCreate
- **不重读 reference**：规则已在上下文
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

脚本只处理以下机械违规：

| 违规 | 处理 |
|------|------|
| 标题前数字/中文数字标号（`## 1. xxx`、`### 一、 xxx`） | 去除 |
| H4 标题（`#### xxx`） | 升 H5（`##### xxx`） |
| 文件无 H2 时所有 H3 升 H2 | 升 H2 |
| H1 紧跟 `> Last Format Time：M/D/YYYY HH:MM:SS` 元信息块 | 插入 / 更新时间戳 |
| H1 下方的裸 URL（`https://...`） | 包成 `[URL](URL)` |
| 中文标点后多余空格（`。 **xxx**`） | 去除空格 |
| H1→H2 之间有外部链接/裸 URL | 加 `---` |
| H1→H2 之间无链接 | 不加 `---`（如已有则移除） |
| 非首个 H2 紧上方缺 `---` | 插入 |
| 代码块前/后缺空行 | 按规则补 |
| 代码块缺/非法语言标签 | 报告（不自动改） |

其他违规（语义正确性、frontmatter、标签体系、目录迁移、笔记引用关系）需要 Claude 上下文判断，脚本不做。
