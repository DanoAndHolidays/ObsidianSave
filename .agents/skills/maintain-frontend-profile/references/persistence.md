# 画像持久化规范

## 目录与文件

固定保存到 `前端/面试/能力画像/`：

```text
能力画像/
├── profile-data.json
├── 能力证据.jsonl
├── 前端能力画像.md
├── 秋招学习计划.md
├── 更新记录.md
└── .scan-state.json
```

- `profile-data.json`：结构化当前状态，作为渲染源。
- `能力证据.jsonl`：一行一条不可重复的证据记录。
- 两个 Markdown 文件：由 `render_profile.py` 生成，不手工维护派生表格。
- `更新记录.md`：记录每次判断变化及原因，不记录流水扫描噪声。
- `.scan-state.json`：成功更新后保存文件哈希，只负责增量候选发现。

## 证据记录

每行 JSON 至少包含：

```json
{
  "id": "evidence-unique-id",
  "date": "2026-08-03",
  "source": "前端/路径/文件.md",
  "type": "exam|defense|project|code|interview|note",
  "strength": "trace|low|medium|high",
  "independence": "independent|assisted|unknown",
  "capabilities": ["react-core"],
  "summary": "该证据实际证明的内容",
  "verification": "测试、评分、原回答或其他可观察结果",
  "supersedes": []
}
```

- ID 必须稳定且唯一；推荐使用来源类型、日期和短主题。
- 同一来源包含多个不同验证时可以拆分记录，但不能重复计算同一结果。
- 来源失效时保留记录并标记 `active: false`，不要静默删除历史。

## `profile-data.json`

顶层必须包含 `schema_version`、`updated`、`target`、`inventory`、`dimensions`、`verified_points`、`priorities` 和 `caveats`。

每个维度至少包含：

- `id`、`name`、`target_level`；
- `exposure`：`unknown|narrow|moderate|broad`；
- `scores`：四个分项，允许 `null`；
- `mastery_level`、`confidence`、`status`；
- `evidence_ids`、`strengths`、`gaps`、`next_action`。

`verified_points` 记录具体知识点，不用维度平均值覆盖它们。`priorities` 最多三项，每项包含排序输入、任务和验收标准。

## 更新事务

1. 读取磁盘最新版本和 Git 状态。
2. 收集候选文件，不写扫描状态。
3. 校验并更新证据台账。
4. 更新 `profile-data.json`。
5. 运行渲染脚本。
6. 运行校验脚本并重新读取派生文件。
7. 追加一条有实质变化的更新记录。
8. 最后运行收集脚本的 `--write-state`。

任一步失败时，不执行第 8 步，不声称更新成功。

## 冲突处理

- 新证据与旧结论冲突时保留两者，说明时间、任务范围和证据强度，再调整当前判断。
- 面经原回答与后补参考答案冲突时，以原回答评估当时表现，以后补答案记录学习覆盖。
- 画像与代达罗斯考试画像冲突时，具体考试评分优先；全局画像负责解释聚合差异。
- 不修改代达罗斯考试索引、题目和阅卷事务。
