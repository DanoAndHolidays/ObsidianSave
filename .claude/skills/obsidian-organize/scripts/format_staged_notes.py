#!/usr/bin/env python3
"""机械格式化 Git 暂存区中的 Obsidian 笔记，并安全地重新暂存。"""

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

from collect_changed_notes import decode_nul_paths, is_note_path, run_git
from normalize import (
    NormalizationConvergenceError,
    configure_console_output,
    normalize_content,
)


HARD_CODE_ISSUES = {'unclosed_fence'}


def git_paths(root: Path, *args: str) -> list[str]:
    """读取 Git 的 NUL 分隔路径输出。"""
    return decode_nul_paths(run_git(root, *args))


def staged_note_paths(root: Path) -> list[str]:
    """返回本次提交涉及的新增、复制、修改或重命名笔记。"""
    paths = git_paths(
        root,
        'diff',
        '--cached',
        '--name-only',
        '--diff-filter=ACMR',
        '-z',
        '--',
        '*.md',
    )
    return list(dict.fromkeys(path for path in paths if is_note_path(path)))


def unstaged_markdown_paths(root: Path) -> set[str]:
    """返回工作区中尚未暂存的 Markdown 路径。"""
    return set(git_paths(root, 'diff', '--name-only', '-z', '--', '*.md'))


def add_paths(root: Path, paths: list[str]) -> None:
    """分批重新暂存已机械格式化的文件，避免命令行过长。"""
    for start in range(0, len(paths), 100):
        subprocess.run(
            ['git', 'add', '--', *paths[start:start + 100]],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


def run(root: Path) -> tuple[dict, int]:
    """安全格式化暂存笔记；有部分暂存或硬错误时不写任何笔记。"""
    root = root.resolve()
    files = staged_note_paths(root)
    report = {
        'files': files,
        'count': len(files),
        'formatted_files': [],
        'warning_count': 0,
        'warnings': [],
    }
    if not files:
        return report, 0

    partially_staged = sorted(set(files) & unstaged_markdown_paths(root))
    if partially_staged:
        report['error'] = 'partially_staged_notes'
        report['error_files'] = partially_staged
        return report, 2

    fixed_now = datetime.datetime.now()
    prepared = []
    hard_errors = []
    warnings = []
    for relative in files:
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            hard_errors.append({'file': relative, 'kind': 'path_outside_root'})
            continue
        if not path.is_file():
            hard_errors.append({'file': relative, 'kind': 'missing_worktree_file'})
            continue

        original = path.read_text(encoding='utf-8')
        try:
            normalized, stats = normalize_content(
                original,
                now=fixed_now,
                expected_title=path.stem,
            )
        except NormalizationConvergenceError as exc:
            hard_errors.append({
                'file': relative,
                'kind': 'normalization_not_converged',
                'message': str(exc),
            })
            continue

        for issue in stats['code_issues']:
            item = {'file': relative, **issue}
            if issue['kind'] in HARD_CODE_ISSUES:
                hard_errors.append(item)
            else:
                warnings.append(item)
        for issue in stats['manual_issues']:
            warnings.append({'file': relative, **issue})
        prepared.append((path, relative, original, normalized))

    report['warnings'] = warnings
    report['warning_count'] = len(warnings)
    if hard_errors:
        report['error'] = 'unsafe_notes'
        report['hard_errors'] = hard_errors
        return report, 2

    # 防止预览和写回之间覆盖编辑器刚写入的新内容。
    changed_during_run = [
        relative
        for path, relative, original, _ in prepared
        if path.read_text(encoding='utf-8') != original
    ]
    if changed_during_run:
        report['error'] = 'notes_changed_during_format'
        report['error_files'] = changed_during_run
        return report, 2

    changed_paths = []
    for path, relative, original, normalized in prepared:
        if normalized == original:
            continue
        path.write_text(normalized, encoding='utf-8')
        changed_paths.append(relative)

    if changed_paths:
        add_paths(root, changed_paths)
    report['formatted_files'] = changed_paths
    report['formatted_count'] = len(changed_paths)
    return report, 0


def print_human_report(report: dict, quiet: bool = False) -> None:
    """输出适合 pre-commit 的简短结果。"""
    error = report.get('error')
    if error == 'partially_staged_notes':
        print(
            '[obsidian-format] 已暂存笔记仍有未暂存修改；为避免误提交，已停止。',
            file=sys.stderr,
        )
        for path in report['error_files']:
            print(f'  - {path}', file=sys.stderr)
        return
    if error:
        print(f'[obsidian-format] 机械格式化失败：{error}', file=sys.stderr)
        for issue in report.get('hard_errors', []):
            line = f':{issue["line"]}' if issue.get('line') else ''
            print(
                f'  - {issue["file"]}{line} {issue["kind"]}',
                file=sys.stderr,
            )
        for path in report.get('error_files', []):
            print(f'  - {path}', file=sys.stderr)
        return

    if not quiet and report.get('formatted_count'):
        print(
            f'[obsidian-format] 已自动格式化并重新暂存 '
            f'{report["formatted_count"]} 篇笔记。'
        )
    if report.get('warning_count'):
        print(
            f'[obsidian-format] {report["warning_count"]} 个问题留待 Agent 复查，'
            '不阻止本次提交。',
            file=sys.stderr,
        )
        for issue in report['warnings'][:10]:
            line = f':{issue["line"]}' if issue.get('line') else ''
            print(
                f'  - {issue["file"]}{line} {issue["kind"]}',
                file=sys.stderr,
            )
        if report['warning_count'] > 10:
            print('  - ...', file=sys.stderr)


def main() -> int:
    configure_console_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.', help='Git 仓库根目录')
    parser.add_argument('--json', action='store_true', help='输出 JSON 报告')
    parser.add_argument('--quiet', action='store_true', help='成功且无警告时保持安静')
    args = parser.parse_args()
    try:
        report, exit_code = run(Path(args.root))
    except (OSError, subprocess.CalledProcessError) as exc:
        report = {'error': 'command_failed', 'message': str(exc)}
        exit_code = 1
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human_report(report, quiet=args.quiet)
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
