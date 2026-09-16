#!/usr/bin/env python3
"""校验 Obsidian 笔记中的局部内容审核标记。"""

import argparse
import json
import re
import sys
from pathlib import Path


LEGACY_HEADING = '## 内容审核变更记录'
LEGACY_MARKER_RE = re.compile(r'〔CR-\d{3}〕')
LEGACY_ENTRY_RE = re.compile(r'^### CR-\d{3}｜', re.MULTILINE)
LOCAL_MARKER_RE = re.compile(r'\*(?:已修改|已补充|已纠正)\*')


def configure_console_output() -> None:
    if sys.platform == 'win32':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')


def issue(kind: str, **details) -> dict:
    return {'kind': kind, **details}


def scan_markers(content: str) -> tuple[list[str], list[dict], list[dict]]:
    """返回局部标记、旧协议问题和代码块内标记问题。"""
    markers: list[str] = []
    issues: list[dict] = []
    in_code = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if re.match(r'^\s*```', line):
            in_code = not in_code
            continue
        legacy_matches = LEGACY_MARKER_RE.findall(line)
        if LEGACY_HEADING in line or LEGACY_ENTRY_RE.search(line):
            issues.append(issue('legacy_review_protocol', line=line_number))
        local_matches = LOCAL_MARKER_RE.findall(line)
        if in_code and (legacy_matches or local_matches):
            for marker in legacy_matches + local_matches:
                issues.append(issue('marker_in_code', marker=marker, line=line_number))
        elif not in_code:
            markers.extend(local_matches)
        if legacy_matches and not in_code:
            issues.append(issue('legacy_review_marker', marker=legacy_matches[0], line=line_number))
    return markers, issues, []


def validate_content_review(content: str) -> dict:
    markers, issues, _ = scan_markers(content)
    return {
        # 保留 entry_count/anchor_count 字段，兼容整理脚本；现在表示局部标记数量。
        'entry_count': len(markers),
        'anchor_count': len(markers),
        'issues': issues,
    }


def validate_file(path: Path) -> dict:
    result = validate_content_review(path.read_text(encoding='utf-8'))
    return {'file': str(path), **result}


def main() -> int:
    configure_console_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', help='要校验的 Markdown 文件')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    args = parser.parse_args()

    results = [validate_file(Path(file)) for file in args.files]
    issue_count = sum(len(result['issues']) for result in results)
    report = {
        'file_count': len(results),
        'entry_count': sum(result['entry_count'] for result in results),
        'issue_count': issue_count,
        'results': results,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for result in results:
            state = '✓' if not result['issues'] else f'✗ {len(result["issues"])} 个问题'
            print(f'{result["file"]}: {state}')
            for item in result['issues']:
                print(f'  - {json.dumps(item, ensure_ascii=False)}')
    return 1 if issue_count else 0


if __name__ == '__main__':
    sys.exit(main())
