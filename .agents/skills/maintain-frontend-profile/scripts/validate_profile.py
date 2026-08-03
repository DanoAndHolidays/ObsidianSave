#!/usr/bin/env python3
"""Validate frontend profile structure, evidence references, scores, and source paths."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


DIMENSIONS = {
    "html-semantics", "css-layout", "javascript", "typescript", "browser-dom",
    "network-security", "react-core", "react-ecosystem", "engineering",
    "testing-quality", "performance-a11y", "coding-algorithms",
    "project-delivery", "interview-communication",
}
SCORE_KEYS = {"knowledge", "application", "delivery", "explanation"}
CONFIDENCE = {"low", "medium", "high"}
EXPOSURE = {"unknown", "narrow", "moderate", "broad"}
STATUS = {"未定级", "薄弱", "发展中", "稳定"}
EVIDENCE_TYPES = {"exam", "defense", "project", "code", "interview", "note"}
STRENGTHS = {"trace", "low", "medium", "high"}
INDEPENDENCE = {"independent", "assisted", "unknown"}


def configure_console() -> None:
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def parse_date(value: str, label: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError):
        errors.append(f"{label} must be YYYY-MM-DD: {value!r}")


def local_path(root: Path, source: str) -> Path:
    return root.joinpath(*source.replace("\\", "/").split("/"))


def load_evidence(path: Path, root: Path, errors: list[str]) -> dict[str, dict]:
    records = {}
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"evidence line {line_number}: invalid JSON: {exc}")
            continue
        evidence_id = record.get("id")
        if not evidence_id:
            errors.append(f"evidence line {line_number}: missing id")
            continue
        if evidence_id in records:
            errors.append(f"duplicate evidence id: {evidence_id}")
        records[evidence_id] = record
        if record.get("type") not in EVIDENCE_TYPES:
            errors.append(f"{evidence_id}: invalid type")
        if record.get("strength") not in STRENGTHS:
            errors.append(f"{evidence_id}: invalid strength")
        if record.get("independence") not in INDEPENDENCE:
            errors.append(f"{evidence_id}: invalid independence")
        parse_date(record.get("date"), f"{evidence_id}.date", errors)
        capabilities = record.get("capabilities", [])
        unknown = set(capabilities) - DIMENSIONS
        if unknown:
            errors.append(f"{evidence_id}: unknown capabilities {sorted(unknown)}")
        source = record.get("source")
        if not source:
            errors.append(f"{evidence_id}: missing source")
        elif record.get("active", True) and not local_path(root, source).is_file():
            errors.append(f"{evidence_id}: source does not exist: {source}")
    return records


def validate_profile(data: dict, evidence: dict[str, dict], errors: list[str]) -> None:
    if data.get("schema_version") != 1:
        errors.append("profile.schema_version must be 1")
    parse_date(data.get("updated"), "profile.updated", errors)
    target = data.get("target", {})
    stack = set(target.get("stack", []))
    if not {"React", "TypeScript"}.issubset(stack):
        errors.append("target.stack must include React and TypeScript")

    dimensions = data.get("dimensions", [])
    ids = [item.get("id") for item in dimensions]
    if set(ids) != DIMENSIONS or len(ids) != len(DIMENSIONS):
        errors.append("profile.dimensions must contain every taxonomy id exactly once")
    for item in dimensions:
        item_id = item.get("id", "<missing>")
        if item.get("exposure") not in EXPOSURE:
            errors.append(f"{item_id}: invalid exposure")
        if item.get("confidence") not in CONFIDENCE:
            errors.append(f"{item_id}: invalid confidence")
        if item.get("status") not in STATUS:
            errors.append(f"{item_id}: invalid status")
        level = item.get("mastery_level")
        if level is not None and (not isinstance(level, (int, float)) or not 0 <= level <= 5):
            errors.append(f"{item_id}: mastery_level outside 0..5")
        scores = item.get("scores", {})
        if set(scores) != SCORE_KEYS:
            errors.append(f"{item_id}: scores must contain {sorted(SCORE_KEYS)}")
        for key, value in scores.items():
            if value is not None and (not isinstance(value, int) or not 0 <= value <= 100):
                errors.append(f"{item_id}.{key}: score must be null or integer 0..100")
        for evidence_id in item.get("evidence_ids", []):
            if evidence_id not in evidence:
                errors.append(f"{item_id}: missing evidence reference {evidence_id}")

    points = data.get("verified_points", [])
    point_ids = [point.get("id") for point in points]
    if len(point_ids) != len(set(point_ids)):
        errors.append("verified_points contain duplicate ids")
    for point in points:
        point_id = point.get("id", "<missing>")
        if point.get("dimension_id") not in DIMENSIONS:
            errors.append(f"{point_id}: unknown dimension_id")
        if point.get("status") not in STATUS - {"未定级"}:
            errors.append(f"{point_id}: invalid verified status")
        if point.get("confidence") not in CONFIDENCE:
            errors.append(f"{point_id}: invalid confidence")
        level = point.get("level")
        if not isinstance(level, (int, float)) or not 0 <= level <= 5:
            errors.append(f"{point_id}: level outside 0..5")
        parse_date(point.get("last_verified"), f"{point_id}.last_verified", errors)
        if point.get("next_review"):
            parse_date(point["next_review"], f"{point_id}.next_review", errors)
        for evidence_id in point.get("evidence_ids", []):
            if evidence_id not in evidence:
                errors.append(f"{point_id}: missing evidence reference {evidence_id}")

    priorities = data.get("priorities", [])
    if not 1 <= len(priorities) <= 3:
        errors.append("priorities must contain 1 to 3 items")
    for item in priorities:
        topic = item.get("topic", "<missing>")
        factors = item.get("factors", {})
        expected = {"target_gap", "recruitment_relevance", "review_urgency", "evidence_uncertainty"}
        if set(factors) != expected:
            errors.append(f"priority {topic}: invalid factor keys")
        for key, value in factors.items():
            if not isinstance(value, int) or not 0 <= value <= 100:
                errors.append(f"priority {topic}.{key}: must be integer 0..100")
        if not item.get("acceptance"):
            errors.append(f"priority {topic}: acceptance must not be empty")


def main() -> int:
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    profile_path = Path(args.profile)
    evidence_path = Path(args.evidence)
    if not profile_path.is_absolute():
        profile_path = root / profile_path
    if not evidence_path.is_absolute():
        evidence_path = root / evidence_path
    errors = []
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [f"profile unreadable: {exc}"]}, ensure_ascii=False, indent=2))
        return 1
    try:
        evidence = load_evidence(evidence_path, root, errors)
    except OSError as exc:
        print(json.dumps({"ok": False, "errors": [f"evidence unreadable: {exc}"]}, ensure_ascii=False, indent=2))
        return 1
    validate_profile(data, evidence, errors)

    for derived in (profile_path.parent / "前端能力画像.md", profile_path.parent / "秋招学习计划.md"):
        if not derived.is_file():
            errors.append(f"derived file missing: {derived}")

    result = {"ok": not errors, "evidence_count": len(evidence), "dimension_count": len(data.get("dimensions", [])), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
