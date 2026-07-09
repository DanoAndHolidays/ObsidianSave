# skill的定义与最佳实践

---
## 定义
一个skill就是包含了`SKILL.md`的文件夹📂

一个 skill 的本质，应该是是一套**可复用的任务执行系统**，而不是一个简单的提示词模板。它至少可以回答以下五个问题：

1. 用户说什么话时，应该触发这个 skill？
2. 这个 skill 负责什么，不负责什么？
3. 任务来了以后，Agent 应该按什么路线处理？
4. 哪些资料需要按需读取？
5. 哪些动作必须用脚本（代码）保证稳定？

### 目录结构
在我们的[skill代码仓库](https://github.com/forge-town/skills)的规定中可以看到skill的结构：
```
skills/
  {skill-name}/           # kebab-case 目录名
    SKILL.md              # 必需：技能定义
    scripts/              # 必需：可执行脚本
      {script-name}.ts    # TypeScript 脚本（首选）
```

所有的skill全部位于`skills/`目录下，每个skill中必定含有一个`SKILL.md`与`scripts/`

而在官方的定义中我们可以看到更多的内容，其实一个最简单的skill只需要有`SKILL.md`这个文档就可以了：
```text
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

### SKILL.md 格式
`SKILL.md`在Markdown的正文内容前必须有一个使用 YAML 格式定义的 `frontmatter`，其中必须的也是最常用的是name与description:

| Field           | Required | Constraints                                                                                                       |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.             |
| `description`   | Yes      | Max 1024 characters. Non-empty. Describes what the skill does and when to use it.                                 |
| `license`       | No       | License name or reference to a bundled license file.                                                              |
| `compatibility` | No       | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                              |
| `allowed-tools` | No       | Space-separated string of pre-approved tools the skill may use. (Experimental)                                    |
一个简单的示例:
```md
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

在`frontmatter`之后的是body，其中描述了skill的具体内容
```md
---
name: {skill-name}
description: {一句描述何时使用此技能的话。包括触发短语如“部署我的应用”、“检查日志”等。}
---

# {技能标题}

{简要描述技能的功能。}

## 工作原理

{编号列表解释技能的工作流程}

## 使用方法

```bash
pnpx tsx /mnt/skills/user/{skill-name}/scripts/{script}.ts [args]
```

### 命名约定
- **技能目录**：`kebab-case`（例如 `vercel-deploy`、`log-monitor`）
- **SKILL.md**：始终大写，始终为此确切文件名
- **脚本**：`kebab-case.ts`（例如 `deploy.ts`、`fetch-logs.ts`）

---
## 最佳实践
我们的skill除了常见的技巧，也使用很多新颖的组织方式
### 使用不同的description前缀
在我们的项目中skill的description中的元信息中有着**两种不同的开头**：
- 以**Use when**开始：
```md
---
name: generate-preview
description: Use when 需要对 React 组件文件生成结构化 .json 描述和可视化 .md 目录树预览，用于组件拆分前的详细结构分析、复杂度评估与规划。触发词：生成组件预览文档、拆分前分析、组件结构可视化。
---
```
- 以**Must follow when**开始：
```md
---
name: i18n-best-practice
description: Must follow when 创建或重构 i18n 国际化代码，确保遵循 react-i18next 最佳实践（初始化配置、翻译文件结构、组件用法、SSR 同步、语言切换与测试 Mock）。
---
```

具体定义：
```md
### 2.7 `description` 前缀协议
- [ ] ✅ **动词型 Skill**（执行操作/检查，名称不以 `-best-practice` 结尾）`description` 必须以 `Use when` 开头
  - ❌ 错误示例：`description: 自动检查并转换 className...` → 必须改为 `description: Use when 需要检查或转换...`
- [ ] ✅ **名词型 Skill**（定义规范/标准，名称以 `-best-practice` 结尾）`description` 必须以 `Must follow` 开头
  - ❌ 错误示例：`description: 规范化 DAO 文件...` → 必须改为 `description: Must follow when 创建或重构 DAO...`
  - ✅ 判断依据：目录名以 `-best-practice` 结尾 → Must follow；否则 → Use when
```

### 创建不同类型的技能
仓库中存在两种不同类型的skill，包含 57 个技能：25 个“最佳实践”skill（名词型，-best-practice 后缀）和 32 个动作skill（动词型，verb-noun 格式）。

“最佳实践”skill的部分定义：
- 最佳实践类 Skill 必须有 `-best-practice` 后缀
- `references/checklist.md` 文件存在（强制要求）
- `best-practice-examples/` 目录存在且包含至少一个示例文件/文件夹（强制要求）
- checklist 包含 Bad Case 确认节（列出**不得出现**的反模式）
- ...

### 用渐进式披露组织大型技能
将 SKILL.md 保持在 **500 行和 5,000 token以内**——只包含智能体每次运行都需要的核心指令。当技能确实需要更多内容时，将详细的参考材料移到 references/ 或类似目录中的**单独文件中。**

关键是告诉智能体**何时加载**每个文件。"如果 API 返回非 200 状态码，请阅读 references/api-errors.md"比泛泛的"详见references/"更有用。这让智能体按需加载上下文，而非一次性全部加载，这正是渐进式披露的设计初衷。

在我们的技能仓库中可以看到几乎所有的技能都遵循了这个规范：
![[Pasted image 20260630165006.png]]

除了这些，我们的技能还依托于之前的技能分类与description前缀构建起了更加复杂的技能关系 — 每个技能独立可用，也能通过上游/下游关系串联成工作流，在create-skill这个技能中：
```md
...省略

1. 阅读 [skill-initialization-guide.md](references/skill-initialization-guide.md) 了解 Skill 结构与命名规则
2. 参考 [anatomy.json](references/anatomy.json) 确认目录结构
3. 参考 [workflows.md](references/workflows.md) 了解创建/更新流程
4. 使用 [checklist.md](references/checklist.md) 验证创建/更新结果

**重要：** SKILL.md 主体保持极简，详细内容全部放入 `references/`；完成后强制触发 `skill-best-practice` 检查

...省略
```

##### 两级触发机制
我们可以看到在最后强制使用了skill-best-practice这个技能，而这个技能本身又是一个以Must follow when前缀开头的“最佳实践类”技能，也就是说除了技能的body，技能的description也描述了技能间的关系：
```
┌─────────────────────────────────────────────┐
│ 第1级：description 前缀（始终可见）           │
│  "Must follow when" → 上下文匹配自动触发      │
│  "Use when"        → 用户提示词匹配触发       │
├─────────────────────────────────────────────┤
│ 第2级：触发词（description 内声明）           │
│  "触发词：检查checklist规范、checklist审查"   │
└─────────────────────────────────────────────┘
```

##### 触发模式

| 模式 | 适用类型 | 机制 |
|------|----------|------|
| **上下文驱动** | best-practice | AI 遇到相关代码时自动加载（如编写 DAO 时自动加载 `dao-best-practice`） |
| **关键词驱动** | 动词型 | description 中声明触发词，用户说出关键词时触发 |
| **链式触发** | 工作流型 | 技能完成后硬性指定下一个技能（如 brainstorming → writing-plans → subagent-driven-development） |
| **批量触发** | check-all-* | 自动发现匹配前缀的技能并依次执行（如 `check-all-best-practices` 自动发现所有 `*-best-practice`） |


### 对多步骤的任务使用检查清单
显式的检查清单帮助智能体跟踪进度并避免跳过步骤，尤其是当步骤存在依赖关系或验证关卡时。检查清单是我们仓库中的**二等公民** — 每个技能都必须有 checklist，它是质量门禁，不是可选附录。

在我们的项目中有大量优秀的实践，举个例子🌰：
![[Pasted image 20260630165944.png]]

### 好代码在文件里，坏代码在文档里
Good Case 只在文件中。文档中禁止出现 Good Case 代码块；所有好示例放在 best-practice-examples/ 真实文件中 。

Bad Case 只在文档中。references/ 下文档只放反模式代码块，不放可运行的代码。

禁止纯 Good Case 的 .md 文件 如 references/patterns.md 这类只含好代码的文档必须删除       

### 使用json来表示具体的结构
相比于使用自然语言，json能更好表达结构化的规则，举个🌰：
```json
{
  "description": "一个合规 Skill 的标准目录结构",
  "structure": {
    "{skill-name}/": {
      "_note": "kebab-case，不得以 -skill 结尾；best-practice 类必须以 -best-practice 结尾",
      "SKILL.md": "必需 — 唯一根目录文件，含 name + description 前言区，正文 ≤20 行",
      "references/": {
        "_required": false,
        "_note": "存放实现细节：清单、流程、示例、模板等",
        "checklist.md": "（best-practice 类强制要求）",
        "workflow.md": "（可选）步骤化执行流程",
        "anatomy.json": "（可选）结构解剖定义",
        "examples/": "（可选）代码示例子目录",
        "templates/": "（可选）模板文件子目录"
      },
      "scripts/": {
        "_required": false,
        "_note": "可执行脚本（.ts 优先，其次 .py/.sh），不得为空目录"
      },
      "assets/": {
        "_required": false,
        "_note": "静态资源（图片、数据文件等），不得为空目录"
      }
    }
  },
  "forbidden": [
    "README.md（必须用 SKILL.md）",
    "__pycache__/、*.pyc、.DS_Store、Thumbs.db、tmp/、*.log 等临时文件"
  ]
}
```


> 以下是通用的一些技巧，详细的内容可以阅读原文[skill最佳实践](https://agentskills.io/skill-creation/best-practices)
### 从真实的经验出发
技能创建中的一个常见陷阱是让 LLM 在没有提供领域特定上下文的情况下生成技能——仅依赖 LLM的通用训练知识。结果就是**模糊、泛泛的流程**（"适当地处理错误"、"遵循认证的最佳实践"），而非让技能有价值的那些具体的 API模式、边缘情况和项目约定。

举个例子🌰：
```md
name: 简历优化  
description: 你是一个专业、耐心、有经验的简历优化专家。你需要帮助用户优化简历，让简历更有竞争力。
```

什么是**专业**、什么是怎么判断是**有竞争力的**，全部没有解答。而这正是让技能有价值的部分。

### 从现有的项目中去创建skill
skill始终围绕一个特定的问题，想要解决特定问题，那就需要特定的环境。

从真实的故障报告和操作手册中合成的技能，会比从一篇泛泛的文章中合成的技能更出色，因为它捕获了团队的模式、故障模式和恢复流程。关键在于使用项目特定的材料，而非泛泛的参考资料：
  - 内部文档、操作手册和风格指南
  - API 规范、模式文件和配置文件
  - 代码审查评论和问题追踪器（捕捉反复出现的关注点和审查者的期望）
  - 版本控制历史，尤其是补丁和修复（通过实际变更揭示模式）
  - 真实世界的失败案例及其解决方案

### 不要想着一次就将技能创建好
技能的第一版通常需要打磨。让技能面对真实任务运行，然后将结果反馈到创建过程中。问问自己：什么触发了误报？遗漏了什么？什么可以删减？

即使只做一轮"执行-修正"也能显著提升质量，而复杂领域往往需要多轮。所以一个好的技能是值得被沉淀下来的。

关于更结构化的迭代方法，包括测试用例、断言和评分，见[技能评估](https://agentskills.io/skill-creation/evaluating-skills)

### 不要将一些显然的内容写进去
技能一旦激活，其完整的 SKILL.md 内容就会加载到智能体的上下文窗口中，与对话历史、系统上下文和其他已激活的技能共存。技能中的每个token 都在与窗口中的其他所有内容竞争智能体的注意力。

专注于智能体没有你的技能就不会知道的内容：项目特定的约定、领域特定的流程、非显而易见的边缘情况，以及要使用的特定工具或API。你不需要解释什么是 PDF、HTTP 如何工作，或数据库迁移是什么。
````markdown theme={null}
<!-- Too verbose — the agent already knows what PDFs are -->
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. pdfplumber is recommended because it handles most cases well.

<!-- Better — jumps straight to what the agent wouldn't know on its own -->
## Extract PDF text

Use pdfplumber for text extraction. For scanned documents, fall back to
pdf2image with pytesseract.

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

### 一个skill解决一个问题
这是 Bash 乃至整个 Unix 哲学的灵魂：**“做一件事，并把它做好”**，这也同样适用于skill。

过于全能的技能可能弊大于利——智能体难以提取相关内容，可能会被不适用于当前任务的指令引导到无效路径。

**一个技能只做一件事，通过链式组合完成复杂工作流：**
```
设计阶段：    writing-plans
实现阶段：    subagent-driven-development ──→ test-driven-development
质量阶段：    check-all-best-practices ──→ fix-all-best-practices
```


### 总结
再写 skill 的时候，要明确自己三个问题：

- 这句话是在帮助 Agent 行动，还是只是在表达我的期待？
- 这段内容应该放在 `SKILL.md`，还是应该拆到 `references/`？
- 这个动作应该让 AI 判断，还是应该用脚本固定？

## 参考
[如何写出一个好的 skill](https://mp.weixin.qq.com/s/9Nvx_FRrcvKlX_-cApezow)
[skill代码仓库](https://github.com/forge-town/skills)
[skill最佳实践](https://agentskills.io/skill-creation/best-practices)
[Agent Skills Marketplace](https://skillsmp.com/)这里收录着大量的优质skill仓库
[在ClaudeCode中使用skill](https://code.claude.com/docs/zh-CN/skills)