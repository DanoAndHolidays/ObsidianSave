#!/usr/bin/env python3
"""收集自最近整理 tag 以来以及当前工作区中的变更笔记。"""

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath


DEFAULT_EXCLUDES = (
    '.obsidian/',
    'attachments/',
    'docs/superpowers/specs/',
    '.claude/skills/',
    '.agents/',
    '.codex/',
)


def configure_console_output() -> None:
    """仅在 CLI 入口启用 Windows UTF-8 输出。"""
    if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def run_git(root: Path, *args: str) -> bytes:
    """运行 Git 并返回原始输出，保留 NUL 分隔与 Unicode 路径。"""
    return subprocess.check_output(
        ['git', '-c', 'core.quotepath=false', *args],
        cwd=root,
        stderr=subprocess.PIPE,
    )


def latest_baseline(root: Path) -> str | None:
    output = run_git(
        root,
        'tag',
        '--list',
        'obsidian-organized-*',
        '--sort=-creatordate',
    ).decode('utf-8', 'surrogateescape')
    return next((line.strip() for line in output.splitlines() if line.strip()), None)


def decode_nul_paths(output: bytes) -> list[str]:
    return [
        item.decode('utf-8', 'surrogateescape').replace('\\', '/')
        for item in output.split(b'\0')
        if item
    ]


def working_tree_paths(root: Path) -> list[str]:
    output = run_git(
        root,
        'status',
        '--porcelain=v1',
        '-z',
        '--untracked-files=all',
        '--',
        '*.md',
    )
    entries = output.split(b'\0')
    paths: list[str] = []
    i = 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if not entry:
            continue
        text = entry.decode('utf-8', 'surrogateescape')
        status = text[:2]
        path = text[3:].replace('\\', '/')
        is_rename_or_copy = any(flag in status for flag in ('R', 'C'))
        if is_rename_or_copy and i < len(entries):
            i += 1  # 跳过 rename/copy 的另一路径；不猜测应整理哪一侧
            continue
        if 'D' in status:
            continue
        if status == '??' or any(flag in status for flag in ('A', 'M')):
            paths.append(path)
    return paths


def is_note_path(path: str) -> bool:
    normalized = str(PurePosixPath(path))
    return (
        normalized.lower().endswith('.md')
        and not any(normalized.startswith(prefix) for prefix in DEFAULT_EXCLUDES)
    )


def collect_changed_notes(root: Path, baseline: str | None = None) -> dict:
    root = root.resolve()
    baseline = baseline or latest_baseline(root)
    if not baseline:
        return {
            'baseline': None,
            'files': [],
            'count': 0,
            'error': 'missing_baseline',
        }

    committed = decode_nul_paths(
        run_git(
            root,
            'diff',
            '--name-only',
            '--diff-filter=AM',
            '-z',
            f'{baseline}..HEAD',
            '--',
            '*.md',
        )
    )
    working = working_tree_paths(root)
    files = list(dict.fromkeys(
        path for path in [*committed, *working] if is_note_path(path)
    ))
    return {
        'baseline': baseline,
        'files': files,
        'count': len(files),
    }


def main() -> int:
    configure_console_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.', help='Obsidian 仓库根目录')
    parser.add_argument('--baseline', help='覆盖自动发现的整理 tag')
    parser.add_argument('--limit', type=int, default=20, help='需确认的文件数阈值')
    parser.add_argument('--paths-only', action='store_true', help='每行输出一个路径')
    args = parser.parse_args()

    try:
        result = collect_changed_notes(Path(args.root), args.baseline)
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode('utf-8', 'replace').strip()
        print(json.dumps({'error': 'git_failed', 'message': message}, ensure_ascii=False))
        return 1

    result['limit'] = args.limit
    result['over_limit'] = result['count'] > args.limit
    if args.paths_only:
        print('\n'.join(result['files']))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result.get('error') else 0


if __name__ == '__main__':
    sys.exit(main())
