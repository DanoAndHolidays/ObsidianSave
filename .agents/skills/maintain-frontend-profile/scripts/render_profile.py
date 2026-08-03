#!/usr/bin/env python3
"""Render the human-readable frontend profile and learning plan from structured data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


WEIGHTS = {"knowledge": 0.20, "application": 0.30, "delivery": 0.30, "explanation": 0.20}
SCORE_LABELS = {"knowledge": "理解", "application": "应用", "delivery": "交付", "explanation": "表达接管"}


def configure_console() -> None:
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def load_evidence(path: Path) -> dict[str, dict]:
    records = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        record = json.loads(raw)
        records[record["id"]] = record
    return records


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def score_summary(scores: dict) -> tuple[str, str]:
    values = []
    weighted = 0.0
    available_weight = 0.0
    for key, weight in WEIGHTS.items():
        value = scores.get(key)
        values.append(f"{SCORE_LABELS[key]} {value if value is not None else '—'}")
        if value is not None:
            weighted += value * weight
            available_weight += weight
    if not available_weight:
        readiness = "—"
    elif available_weight == 1:
        readiness = str(round(weighted))
    else:
        readiness = f"{round(weighted / available_weight)}（观测 {round(available_weight * 100)}%）"
    return " / ".join(values), readiness


def evidence_links(ids: list[str], evidence: dict[str, dict], limit: int = 3) -> str:
    links = []
    for evidence_id in ids[:limit]:
        record = evidence.get(evidence_id)
        if not record:
            links.append(evidence_id)
            continue
        source = record.get("source", "")
        if source.endswith(".md"):
            links.append(f"[[{source[:-3]}|{evidence_id}]]")
        else:
            links.append(evidence_id)
    if len(ids) > limit:
        links.append(f"另 {len(ids) - limit} 条")
    return "、".join(links) if links else "—"


def bullet_lines(items: list[str], empty: str = "暂无") -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {empty}"]


def render_profile(data: dict, evidence: dict[str, dict]) -> str:
    target = data["target"]
    inventory = data["inventory"]
    lines = [
        "---",
        "type: frontend-career-profile",
        f"updated: {data['updated']}",
        f"target: {target['role']}",
        "---",
        "",
        "# 前端能力画像",
        "",
        f"> 目标：{target['role']}；主栈：{', '.join(target['stack'])}；公司档位：{target['company_tier']}。",
        "> 分数只描述已有证据。`—` 表示尚未形成足够的独立验证，不等于能力为零。",
        "",
        "## 当前结论",
        "",
        data["summary"],
        "",
        "## 证据覆盖",
        "",
        f"- 前端 Markdown：{inventory['frontend_markdown']} 篇。",
        f"- 项目与考试类候选：{inventory['practice_candidates']} 篇。",
        f"- 面试与代码类候选：{inventory['interview_candidates']} 篇。",
        f"- 已登记能力证据：{len(evidence)} 条。",
        "",
        "目录和标题只表示学习覆盖，画像等级以证据台账中的独立实践和验证为准。",
        "",
        "## 能力维度",
        "",
        "| 维度 | 覆盖 | 四项观测 | 准备度 | 等级 | 状态 | 置信度 | 主要证据 |",
        "|---|---|---|---:|---:|---|---|---|",
    ]
    for dimension in data["dimensions"]:
        scores, readiness = score_summary(dimension["scores"])
        level = dimension.get("mastery_level")
        lines.append(
            "| "
            + " | ".join(
                md(value)
                for value in (
                    dimension["name"],
                    dimension["exposure"],
                    scores,
                    readiness,
                    f"L{level}" if level is not None else "—",
                    dimension["status"],
                    dimension["confidence"],
                    evidence_links(dimension.get("evidence_ids", []), evidence),
                )
            )
            + " |"
        )

    lines.extend(["", "## 分维度说明", ""])
    for dimension in data["dimensions"]:
        lines.extend(
            [
                f"### {dimension['name']}",
                "",
                "优势或已有基础：",
                "",
                *bullet_lines(dimension.get("strengths", [])),
                "",
                "缺口或证据不足：",
                "",
                *bullet_lines(dimension.get("gaps", [])),
                "",
                f"下一步：{dimension['next_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## 已验证知识点",
            "",
            "| 知识点 | 维度 | 等级 | 最近分数 | 状态 | 置信度 | 最近验证 | 下次复习 | 证据 |",
            "|---|---|---:|---:|---|---|---|---|---|",
        ]
    )
    dimensions = {item["id"]: item["name"] for item in data["dimensions"]}
    for point in data["verified_points"]:
        lines.append(
            "| "
            + " | ".join(
                md(value)
                for value in (
                    point["name"],
                    dimensions.get(point["dimension_id"], point["dimension_id"]),
                    f"L{point['level']}",
                    f"{point['recent_score']}%" if point.get("recent_score") is not None else "—",
                    point["status"],
                    point["confidence"],
                    point["last_verified"],
                    point.get("next_review", "—"),
                    evidence_links(point.get("evidence_ids", []), evidence),
                )
            )
            + " |"
        )

    lines.extend(["", "## 画像限制", "", *bullet_lines(data.get("caveats", [])), ""])
    return "\n".join(lines)


def priority_score(item: dict) -> int:
    factors = item["factors"]
    return round(
        0.40 * factors["target_gap"]
        + 0.25 * factors["recruitment_relevance"]
        + 0.20 * factors["review_urgency"]
        + 0.15 * factors["evidence_uncertainty"]
    )


def render_plan(data: dict) -> str:
    target = data["target"]
    priorities = sorted(data["priorities"], key=priority_score, reverse=True)
    lines = [
        "---",
        "type: frontend-autumn-recruitment-plan",
        f"updated: {data['updated']}",
        f"period: {data.get('plan_period', '下一学习周期')}",
        "---",
        "",
        "# 秋招学习计划",
        "",
        f"> 面向 {target['company_tier']}的 {target['role']}，主栈为 {', '.join(target['stack'])}。",
        "",
        "## 本周期目标",
        "",
        "只处理以下三个最高优先级主题。完成标准是产出可观察证据，不是新增笔记数量。",
        "",
    ]
    for index, item in enumerate(priorities, 1):
        factors = item["factors"]
        lines.extend(
            [
                f"### {index}. {item['topic']}（优先级 {priority_score(item)}）",
                "",
                f"原因：{item['reason']}",
                "",
                f"任务：{item['task']}",
                "",
                "验收标准：",
                "",
                *bullet_lines(item["acceptance"]),
                "",
                f"预计投入：{item['estimated_time']}；完成后证据：{item['evidence_output']}。",
                "",
                f"排序输入：目标差距 {factors['target_gap']} / 招聘相关性 {factors['recruitment_relevance']} / 复习紧迫度 {factors['review_urgency']} / 证据不确定性 {factors['evidence_uncertainty']}。",
                "",
            ]
        )
    lines.extend(
        [
            "## 时间分配",
            "",
            "- 60%：高频薄弱项和重复错误。",
            "- 25%：真实任务、代码题或测试验证。",
            "- 15%：项目表达、面经复盘和简历证据。",
            "",
            "## 更新画像的完成条件",
            "",
            "- 把实现、运行结果、测试或答辩记录写入对应来源笔记。",
            "- 明确区分独立完成、Agent 辅助和参考答案。",
            "- 重新运行能力画像 Skill；只有通过校验后才更新扫描状态。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    profile_path = Path(args.profile)
    evidence_path = Path(args.evidence)
    output_dir = Path(args.output_dir)
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    evidence = load_evidence(evidence_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "前端能力画像.md").write_text(render_profile(data, evidence), encoding="utf-8")
    (output_dir / "秋招学习计划.md").write_text(render_plan(data), encoding="utf-8")
    print(json.dumps({"rendered": [str(output_dir / "前端能力画像.md"), str(output_dir / "秋招学习计划.md")]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
