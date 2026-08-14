#!/usr/bin/env python3
"""校验 Obsidian 笔记中的内容审核锚点与变更记录。"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


REVIEW_HEADING = '## 内容审核变更记录'
ANCHOR_RE = re.compile(r'〔(CR-\d{3})〕')
ENTRY_RE = re.compile(r'^### (CR-\d{3})｜(.+?)\s*$', re.MULTILINE)
DATE_RE = re.compile(r'^\d{1,2}/\d{1,2}/\d{4}$')
FIELD_NAMES = ('日期', '位置', '原内容', '调整后', '原因', '依据')
ALLOWED_TYPES = {
    '流畅性',
    '事实纠错',
    '顺序调整',
    '补充说明',
    '删减去重',
    '代码修正',
    '术语统一',
}
EVIDENCE_REQUIRED_TYPES = {'事实纠错', '代码修正'}


def configure_console_output() -> None:
    if sys.platform == 'win32':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')


def issue(kind: str, **details) -> dict:
    return {'kind': kind, **details}


def anchors_outside_code(content: str) -> tuple[list[str], list[dict]]:
    anchors: list[str] = []
    issues: list[dict] = []
    in_code = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if re.match(r'^\s*```', line):
            in_code = not in_code
            continue
        for anchor in ANCHOR_RE.findall(line):
            if in_code:
                issues.append(issue('anchor_in_code', id=anchor, line=line_number))
            else:
                anchors.append(anchor)
    return anchors, issues


def parse_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r'^- (日期|位置|原内容|调整后|原因|依据)：(.*)$', line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def validate_content_review(content: str) -> dict:
    issues: list[dict] = []
    heading_count = content.count(REVIEW_HEADING)
    all_anchors, anchor_issues = anchors_outside_code(content)
    issues.extend(anchor_issues)

    if heading_count == 0:
        if all_anchors:
            issues.append(issue('missing_review_log'))
        return {'entry_count': 0, 'anchor_count': len(all_anchors), 'issues': issues}

    if heading_count > 1:
        issues.append(issue('duplicate_review_log', count=heading_count))

    body, log = content.split(REVIEW_HEADING, 1)
    body_anchors, _ = anchors_outside_code(body)
    log_anchors = ANCHOR_RE.findall(log)
    for anchor in log_anchors:
        issues.append(issue('anchor_in_review_log', id=anchor))

    anchor_counts = Counter(body_anchors)
    for anchor, count in anchor_counts.items():
        if count > 1:
            issues.append(issue('duplicate_anchor', id=anchor, count=count))

    entries = list(ENTRY_RE.finditer(log))
    if not entries:
        issues.append(issue('empty_review_log'))

    entry_ids = [match.group(1) for match in entries]
    entry_counts = Counter(entry_ids)
    for entry_id, count in entry_counts.items():
        if count > 1:
            issues.append(issue('duplicate_entry', id=entry_id, count=count))

    for index, match in enumerate(entries):
        entry_id, review_type = match.groups()
        end = entries[index + 1].start() if index + 1 < len(entries) else len(log)
        block = log[match.end():end]
        fields = parse_fields(block)

        if review_type not in ALLOWED_TYPES:
            issues.append(issue('unsupported_type', id=entry_id, value=review_type))

        for field in FIELD_NAMES:
            if not fields.get(field):
                issues.append(issue('missing_field', id=entry_id, field=field))

        date = fields.get('日期')
        if date and not DATE_RE.fullmatch(date):
            issues.append(issue('invalid_date', id=entry_id, value=date))

        evidence = fields.get('依据', '')
        if review_type in EVIDENCE_REQUIRED_TYPES and '无需外部依据' in evidence:
            issues.append(issue('evidence_required', id=entry_id, type=review_type))

    anchor_ids = set(anchor_counts)
    entry_id_set = set(entry_ids)
    for anchor in sorted(anchor_ids - entry_id_set):
        issues.append(issue('orphan_anchor', id=anchor))
    for entry_id in sorted(entry_id_set - anchor_ids):
        issues.append(issue('orphan_entry', id=entry_id))

    trailing_h2 = re.search(r'^## (?!内容审核变更记录).+$', log, re.MULTILINE)
    if trailing_h2:
        issues.append(issue('review_log_not_last', heading=trailing_h2.group(0)))

    return {
        'entry_count': len(entries),
        'anchor_count': len(body_anchors),
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
