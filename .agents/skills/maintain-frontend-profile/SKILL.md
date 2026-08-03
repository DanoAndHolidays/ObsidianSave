---
name: maintain-frontend-profile
description: Maintain an evidence-backed frontend capability profile and targeted autumn-recruitment learning plan from this Obsidian vault. Use when the user asks to initialize, update, inspect, explain, or calibrate their React and TypeScript frontend skill profile; analyze recent learning notes, projects, exams, interview reviews, or code exercises; identify job-readiness gaps; or generate a prioritized study and verification plan for medium-to-large internet-company campus recruitment.
---

# 维护前端秋招能力画像

以可追溯证据描述能力，不把笔记数量、参考答案或 Agent 生成内容直接视为掌握。默认目标是 React + TypeScript 前端岗位、互联网中大厂校招。

## 固定位置

- 将画像数据保存到 `前端/面试/能力画像/`。
- 将代达罗斯考试画像 `前端/项目笔记/代达罗斯/考试/能力画像.md` 作为高置信历史证据源保留，不覆盖它。
- 将生成目录、附件、`.obsidian/`、`.agents/`、`.claude/` 和 `.codex/` 排除出证据扫描。

## 开始前

1. 完整阅读 [能力分类](references/capability-taxonomy.md) 与 [证据评分](references/evidence-rubric.md)。
2. 初始化或写回画像时完整阅读 [持久化规范](references/persistence.md)。
3. 制定秋招计划或调整目标时完整阅读 [目标岗位](references/target-role.md)。
4. 读取 `git status --short`，保留用户已有改动，不自动提交、打 tag 或整理笔记。

## 工作模式

### 初始化画像

1. 运行 `scripts/collect_evidence.py --root . --mode all --json-out <临时文件>`，先建立路径、标题、目录和证据类型清单。
2. 将文件数量和标题只用于判断知识覆盖，不用于判定独立掌握。
3. 优先完整读取考试阅卷报告、答辩记录、项目复盘、代码练习和包含原始回答的面经；再按能力分类抽样读取普通笔记。
4. 区分面经中的“原回答”和“参考答案”。仅将原回答、真实结果和后续验证计入面试表现。
5. 按持久化规范创建结构化画像和证据台账，运行渲染与校验脚本。

### 增量更新

1. 运行 `scripts/collect_evidence.py --root . --mode changed --state 前端/面试/能力画像/.scan-state.json --json-out <临时文件>`。
2. 只读取候选新增或变化笔记；发现重命名、删除或来源冲突时核对旧证据，不静默保留失效引用。
3. 为每条新证据记录能力点、证据类型、独立性、验证方式、日期和来源路径。
4. 先更新 `profile-data.json` 与 `能力证据.jsonl`，再渲染 Markdown。
5. 只有画像写回和校验全部成功后，才用 `--write-state` 更新扫描状态。

### 只做分析或学习建议

读取现有画像、证据台账和最近更新记录。除非用户明确要求更新，否则不写文件。结论必须区分“已验证能力”“仅有学习覆盖”“证据不足”。

## 评分规则

- 使用 L0–L5 掌握等级；同时保留知识理解、实践应用、独立交付、表达接管四个分项。
- 将总准备度作为透明派生指标，不用它替代分项和置信度。
- 普通知识笔记最多证明 L1；带本人推导和可运行例子的笔记通常最多证明 L2。
- 独立练习或真实代码证据才能支持 L3；真实任务交付与验证才能支持 L4。
- 至少两次独立、跨时间的高质量验证才能支持 L5 或“稳定”。
- Agent 参与不直接扣分；无法解释、预测、举证或现场接管时，不将交付结果当作独立掌握。
- 不因时间流逝自动降低历史掌握等级；单独降低“复习新鲜度”和秋招准备度。

详细阈值、证据强度和反失真规则见 [证据评分](references/evidence-rubric.md)。

## 生成学习计划

1. 只选择最多三个本周期重点。
2. 按目标差距 40%、秋招相关性 25%、复习到期 20%、证据不确定性 15% 排序。
3. 为每个重点给出可执行任务、可观察验收标准、预计时间和完成后可产生的证据类型。
4. 默认分配 60% 时间给高频薄弱项，25% 给真实任务或代码验证，15% 给项目表达、面经复盘和简历证据。
5. 需要真实项目考试时调用 `create-exam`；沿用其“交付 + 独立答辩 + 现场接管”规则，不在本 Skill 中复制考试实现。

## 写回与验证

按顺序执行：

```powershell
python .agents/skills/maintain-frontend-profile/scripts/render_profile.py --profile 前端/面试/能力画像/profile-data.json --evidence 前端/面试/能力画像/能力证据.jsonl --output-dir 前端/面试/能力画像
python .agents/skills/maintain-frontend-profile/scripts/validate_profile.py --root . --profile 前端/面试/能力画像/profile-data.json --evidence 前端/面试/能力画像/能力证据.jsonl
```

重新读取生成的 `前端能力画像.md`、`秋招学习计划.md`、结构化数据和校验结果。任何一步失败时，不更新 `.scan-state.json`，也不声称画像已完成更新。

## 安全边界

- 不修改来源笔记语义、目录、frontmatter 或链接。
- 不扫描或保存凭据、个人联系方式和无关私人内容。
- 不把后端、数据库和服务端实现计入前端主能力；只能作为协作边界或加分项记录。
- 不补造考试、面试、代码运行或项目验证结果。
- 对无法判断是否独立完成的证据标记 `unknown`，不要乐观推断。
