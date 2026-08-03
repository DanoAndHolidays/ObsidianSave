#!/usr/bin/env python3
"""Collect frontend-note metadata and changed-file candidates without scoring mastery."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_PREFIXES = (
    ".git/",
    ".obsidian/",
    ".agents/",
    ".claude/",
    ".codex/",
    ".skill-staging/",
    "attachments/",
    "附件/",
    "前端/面试/能力画像/",
)

DIMENSION_PATTERNS = {
    "html-semantics": (r"(^|/)html(/|$)", r"语义", r"表单元素", r"seo"),
    "css-layout": (r"css", r"样式", r"flex", r"grid", r"布局", r"tailwind", r"sass"),
    "javascript": (r"(^|/)js(/|$)", r"javascript", r"es6", r"promise", r"generator", r"闭包", r"原型"),
    "typescript": (r"typescript", r"(^|/)ts(/|$)", r"类型体操", r"类型检查", r"泛型"),
    "browser-dom": (r"浏览器", r"web api", r"(^|/)dom(/|$)", r"事件", r"event\.", r"存储"),
    "network-security": (r"网络", r"http", r"请求", r"协议", r"跨域", r"安全", r"认证", r"缓存"),
    "react-core": (r"react", r"hook", r"fiber", r"jsx", r"context", r"生命周期"),
    "react-ecosystem": (r"react query", r"tanstack", r"refine", r"zustand", r"redux", r"router", r"hook form", r"zod", r"schema"),
    "engineering": (r"工程化", r"vite", r"webpack", r"rollup", r"npm", r"pnpm", r"git", r"构建", r"打包", r"lint", r"ci"),
    "testing-quality": (r"测试", r"vitest", r"jest", r"playwright", r"代码质量", r"重构", r"阅卷"),
    "performance-a11y": (r"性能", r"core web vitals", r"lcp", r"cls", r"可访问", r"a11y"),
    "coding-algorithms": (r"算法", r"代码题", r"手写", r"leetcode", r"数据结构"),
    "project-delivery": (r"项目笔记", r"交付说明", r"答辩记录", r"踩坑", r"需求", r"复盘"),
    "interview-communication": (r"面经", r"面试", r"简历", r"自我介绍", r"项目讲解"),
}


def configure_console() -> None:
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def posix_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_included(relative: str) -> bool:
    return relative.startswith("前端/") and relative.endswith(".md") and not any(
        relative.startswith(prefix) for prefix in EXCLUDED_PREFIXES
    )


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def evidence_type(relative: str) -> str:
    lowered = relative.lower()
    if "阅卷报告" in relative:
        return "exam"
    if "答辩记录" in relative:
        return "defense"
    if "/考试/" in relative:
        return "exam"
    if "/面经/" in relative:
        return "interview"
    if "/面试/代码/" in relative or "代码题" in relative or "手写" in relative:
        return "code"
    if "/项目笔记/" in relative:
        return "project"
    return "note"


def classify_dimensions(text: str) -> list[str]:
    lowered = text.lower()
    return [
        dimension
        for dimension, patterns in DIMENSION_PATTERNS.items()
        if any(re.search(pattern, lowered) for pattern in patterns)
    ]


def inspect_file(path: Path, root: Path) -> dict:
    data = path.read_bytes()
    text = data.decode("utf-8", "replace")
    lines = text.splitlines()
    headings = [
        re.sub(r"^#{1,6}\s+", "", line).strip()
        for line in lines
        if re.match(r"^#{1,6}\s+\S", line)
    ][:40]
    relative = posix_relative(path, root)
    kind = evidence_type(relative)
    strength_hint = {
        "exam": "high",
        "defense": "high",
        "project": "medium",
        "code": "medium",
        "interview": "medium",
        "note": "low",
    }[kind]
    searchable = "\n".join([relative, *headings])
    return {
        "path": relative,
        "sha256": file_hash(data),
        "modified": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
        "bytes": len(data),
        "line_count": len(lines),
        "headings": headings,
        "evidence_type_hint": kind,
        "strength_hint": strength_hint,
        "capability_hints": classify_dimensions(searchable),
    }


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "files": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect(root: Path, mode: str, state_path: Path) -> tuple[dict, dict]:
    root = root.resolve()
    records = []
    for path in sorted(root.joinpath("前端").rglob("*.md")):
        relative = posix_relative(path, root)
        if is_included(relative):
            records.append(inspect_file(path, root))

    current_hashes = {record["path"]: record["sha256"] for record in records}
    old_state = load_state(state_path)
    old_hashes = old_state.get("files", {})
    changed = [record for record in records if old_hashes.get(record["path"]) != record["sha256"]]
    selected = records if mode == "all" else changed
    deleted = sorted(path for path in old_hashes if path not in current_hashes)

    type_counts = Counter(record["evidence_type_hint"] for record in records)
    dimension_counts = Counter(
        dimension for record in records for dimension in record["capability_hints"]
    )
    result = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "state_found": state_path.exists(),
        "total_frontend_markdown": len(records),
        "selected_count": len(selected),
        "deleted_since_state": deleted,
        "inventory": {
            "by_evidence_type": dict(sorted(type_counts.items())),
            "by_capability_hint": dict(sorted(dimension_counts.items())),
        },
        "files": selected,
        "warnings": [
            "Capability hints and file counts describe coverage only; they must not be converted directly into mastery scores."
        ],
    }
    new_state = {
        "schema_version": 1,
        "updated": result["generated_at"],
        "files": current_hashes,
    }
    return result, new_state


def main() -> int:
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Obsidian vault root")
    parser.add_argument("--mode", choices=("all", "changed"), default="changed")
    parser.add_argument("--state", help="Scan-state path; defaults inside the profile directory")
    parser.add_argument("--json-out", help="Write collection result to this JSON file")
    parser.add_argument("--paths-only", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="Suppress stdout; use with --json-out")
    parser.add_argument("--write-state", action="store_true", help="Persist current hashes after a successful profile transaction")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    state_path = Path(args.state) if args.state else root / "前端" / "面试" / "能力画像" / ".scan-state.json"
    if not state_path.is_absolute():
        state_path = root / state_path

    result, new_state = collect(root, args.mode, state_path)
    if args.json_out:
        output = Path(args.json_out)
        if not output.is_absolute():
            output = root / output
        write_json(output, result)
    if args.write_state:
        write_json(state_path, new_state)

    if args.quiet:
        pass
    elif args.paths_only:
        print("\n".join(record["path"] for record in result["files"]))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
