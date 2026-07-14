#!/usr/bin/env python3
"""一键收集并规范化当前 Obsidian 仓库中的变更笔记。"""

import argparse
import json
import sys
from pathlib import Path

from collect_changed_notes import collect_changed_notes
from normalize import configure_console_output, process_file


def summarize(results: list[dict]) -> dict:
    totals: dict[str, int] = {}
    for result in results:
        for key, value in result.items():
            if key in {'file', 'changed'}:
                continue
            if isinstance(value, int):
                totals[key] = totals.get(key, 0) + value
            elif isinstance(value, list):
                totals[key] = totals.get(key, 0) + len(value)
    return totals


def run(
    root: Path,
    baseline: str | None = None,
    limit: int = 20,
    write: bool = False,
    force_over_limit: bool = False,
) -> tuple[dict, int]:
    root = root.resolve()
    collected = collect_changed_notes(root, baseline)
    if collected.get('error'):
        return {'collection': collected, 'results': [], 'totals': {}}, 2
    if collected['count'] > limit and not force_over_limit:
        collected['limit'] = limit
        collected['over_limit'] = True
        return {'collection': collected, 'results': [], 'totals': {}}, 3

    collected['limit'] = limit
    collected['over_limit'] = collected['count'] > limit
    results = [
        process_file(root / path, write=write)
        for path in collected['files']
    ]
    report = {
        'mode': 'write' if write else 'preview',
        'collection': collected,
        'changed_count': sum(1 for result in results if result['changed']),
        'code_issue_count': sum(len(result['code_issues']) for result in results),
        'manual_issue_count': sum(len(result['manual_issues']) for result in results),
        'results': results,
        'totals': summarize(results),
    }
    return report, 0


def main() -> int:
    configure_console_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.', help='Obsidian 仓库根目录')
    parser.add_argument('--baseline', help='覆盖自动发现的整理 tag')
    parser.add_argument('--limit', type=int, default=20, help='需确认的文件数阈值')
    parser.add_argument('--write', action='store_true', help='写回机械修复')
    parser.add_argument(
        '--force-over-limit',
        action='store_true',
        help='用户确认后允许处理超过阈值的文件',
    )
    args = parser.parse_args()

    report, exit_code = run(
        Path(args.root),
        baseline=args.baseline,
        limit=args.limit,
        write=args.write,
        force_over_limit=args.force_over_limit,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
