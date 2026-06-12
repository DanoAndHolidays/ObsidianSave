#!/usr/bin/env python3
"""
Obsidian 笔记机械化规范化脚本

处理纯正则可解的违规，不做任何需要判断的修改。
所有改动幂等（重复运行无副作用）。

使用：
    python normalize.py <file1.md> [file2.md ...]         # 只报告
    python normalize.py --write <file1.md> [file2.md ...] # 写回文件
    python normalize.py --json <file1.md>                 # JSON 输出供程序消费
"""

import argparse
import io
import json
import re
import sys
from pathlib import Path

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 数字标号：## 1. xxx / ## 1、xxx / ### 一、 xxx / ### 1) xxx
NUMBER_PREFIX = re.compile(
    r'^(#{1,6})\s+([一二三四五六七八九十]+|\d+)[.、．\)]\s+',
    re.MULTILINE,
)

# H4 标题行
H4_PATTERN = re.compile(r'^####(\s)', re.MULTILINE)

# 代码块围栏
FENCE = re.compile(r'^```(\S*)\s*$')

# 合法语言标签
LEGAL_LANGS = {
    'jsx', 'tsx', 'ts', 'js', 'javascript', 'css', 'scss', 'html',
    'bash', 'sh', 'shell', 'powershell', 'pwsh', 'cmd', 'batch',
    'json', 'yaml', 'yml', 'md', 'markdown', 'text',
    # 等价别名（保留原样，不强制转换）
    'vue', 'py', 'go', 'java', 'c', 'cpp', 'rust', 'sql', 'xml',
}

# 中英文标点之间多余空格（如 "。 **" → "。**"），不跨换行
PUNCT_SPACE = re.compile(r'([。！？，：；])[ \t]+(?=\*\*|[一-龥])')

# 标题行
H1 = re.compile(r'^#\s+\S')
H2 = re.compile(r'^##\s+\S')
H3 = re.compile(r'^###\s+\S')


def remove_number_prefixes(content: str) -> tuple[str, int]:
    """去除标题前的数字/中文数字标号。"""
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        return m.group(1) + ' '

    return NUMBER_PREFIX.sub(repl, content), count


def h4_to_h5(content: str) -> tuple[str, int]:
    """#### 标题升为 #####。"""
    matches = H4_PATTERN.findall(content)
    if not matches:
        return content, 0
    return H4_PATTERN.sub(r'#####\1', content), len(matches)


def check_code_blocks(content: str) -> list[dict]:
    """检查所有代码块的围栏：缺标签/非法标签。"""
    issues = []
    in_block = False
    open_line = 0
    for i, line in enumerate(content.splitlines(), 1):
        m = FENCE.match(line)
        if not m:
            continue
        if not in_block:
            lang = m.group(1)
            in_block = True
            open_line = i
            if not lang:
                issues.append({'line': i, 'kind': 'missing_lang'})
            elif lang not in LEGAL_LANGS:
                issues.append({'line': i, 'kind': 'unknown_lang', 'lang': lang})
        else:
            in_block = False
    return issues


def fix_punct_space(content: str) -> tuple[str, int]:
    """中文标点后跟粗体/汉字时的多余空格。"""
    return PUNCT_SPACE.subn(r'\1', content)


def h3_to_h2_if_loose(content: str) -> tuple[str, int]:
    """
    文件级判断：若文件中没有任何 H2（只有 H1 和 H3），把所有 H3 升级为 H2。
    这种情况下 H3 被当作主要章节使用，违反"主要章节用 H2"的规则。

    触发条件：文件至少有一个 H1 + 至少一个 H3 + 零个 H2。
    """
    lines = content.split('\n')

    has_h1 = any(H1.match(l) for l in lines)
    has_h2 = any(H2.match(l) for l in lines)
    if has_h2 or not has_h1:
        return content, 0

    out = []
    count = 0
    for line in lines:
        if H3.match(line):
            out.append('##' + line[3:])
            count += 1
        else:
            out.append(line)

    return '\n'.join(out), count


def ensure_h2_separators(content: str) -> tuple[str, int]:
    """
    确保每个非首个 H2 紧上方有 `---` 分隔符（一行空行 + --- + H2）。
    首个 H2：
      - 若 H1 与 H2 之间有正文 → 加 `---`
      - 若 H1 与 H2 直接相连（无正文） → 移除 `---`（如存在）
    """
    lines = content.split('\n')

    # 找 H1 和所有 H2 的位置
    h1_idx = None
    h2_indices = []
    for i, l in enumerate(lines):
        if h1_idx is None and H1.match(l):
            h1_idx = i
        if H2.match(l):
            h2_indices.append(i)

    if not h2_indices:
        return content, 0

    n_changes = 0
    new_lines = list(lines)

    # 自底向上处理（避免插入影响前面的索引）
    for idx in reversed(h2_indices):
        is_first_h2 = (idx == h2_indices[0])

        # 检测 `---` 位置：idx-1（紧邻）或 idx-2（隔一空行）
        has_sep_direct = (
            idx - 1 >= 0 and new_lines[idx - 1].strip() == '---'
        )
        has_sep_with_blank = (
            idx - 2 >= 0
            and new_lines[idx - 1].strip() == ''
            and new_lines[idx - 2].strip() == '---'
        )
        has_sep = has_sep_direct or has_sep_with_blank

        if is_first_h2 and h1_idx is not None:
            # 首个 H2：取决于 H1 与 H2 之间是否有正文
            has_content = any(
                l.strip() and not H1.match(l)
                for l in new_lines[h1_idx + 1:idx]
            )
            if not has_content:
                # 不应有 ---；如存在则删除
                if has_sep_direct:
                    new_lines = new_lines[:idx - 1] + new_lines[idx:]
                    n_changes += 1
                elif has_sep_with_blank:
                    new_lines = new_lines[:idx - 2] + [''] + new_lines[idx:]
                    n_changes += 1
                continue
            # 有内容，需要 --- ；如缺失则插入
            if has_sep_with_blank:
                # 规范化：删除 --- 与 H2 之间的空行
                new_lines = new_lines[:idx - 1] + new_lines[idx:]
                n_changes += 1
            elif not has_sep_direct:
                new_lines, n_changes = _insert_separator(new_lines, idx, n_changes)
            continue

        # 非首个 H2：必须 --- 紧邻
        if has_sep_with_blank:
            # 规范化：删除 --- 与 H2 之间的空行
            new_lines = new_lines[:idx - 1] + new_lines[idx:]
            n_changes += 1
        elif not has_sep_direct:
            new_lines, n_changes = _insert_separator(new_lines, idx, n_changes)

    return '\n'.join(new_lines), n_changes


def _insert_separator(lines: list[str], h2_idx: int, n_changes: int) -> tuple[list[str], int]:
    """
    在 lines[h2_idx]（H2 标题）上方插入 ['', '---']，并删除原 h2_idx 上方的多余空行。
    确保结构是：content\n\n---\n## H2
    """
    # 找到 H2 上方最后一个非空行
    j = h2_idx - 1
    while j >= 0 and lines[j].strip() == '':
        j -= 1
    if j < 0:
        # H2 在文件最顶部，无可插入位置
        return lines, n_changes

    # 重组：lines[:j+1] + ['', '---'] + lines[h2_idx:]
    new_lines = lines[:j + 1] + ['', '---'] + lines[h2_idx:]
    return new_lines, n_changes + 1


def fix_code_block_blank_lines(content: str) -> tuple[str, int]:
    """
    代码块前/后空行调整：
    - 前：若上一行是正文（不是标题/列表/以冒号结尾的描述性文字），加一空行
    - 后：若下一行是标题/段落/引用块（不是列表），加一空行
    """
    lines = content.split('\n')
    new_lines = []
    in_code = False
    n_changes = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        is_fence = bool(FENCE.match(line))

        if is_fence and not in_code:
            # 代码块开始
            if new_lines and new_lines[-1].strip() != '':
                prev = new_lines[-1]
                needs_blank = not (
                    re.match(r'^#{1,6}\s', prev)
                    or re.match(r'^\s*[-*+]\s', prev)
                    or re.match(r'^\s*\d+[.)、]\s', prev)
                    or prev.rstrip().endswith((':', '：'))
                )
                if needs_blank:
                    new_lines.append('')
                    n_changes += 1
            new_lines.append(line)
            in_code = True
            i += 1
        elif is_fence and in_code:
            # 代码块结束
            new_lines.append(line)
            in_code = False
            i += 1
        else:
            new_lines.append(line)
            i += 1

    # 第二遍：代码块后空行
    final_lines = []
    in_code = False
    for i, line in enumerate(new_lines):
        final_lines.append(line)
        is_fence = bool(FENCE.match(line))
        if is_fence and not in_code:
            in_code = True
        elif is_fence and in_code:
            in_code = False
            # 代码块刚结束，检查下一行
            if i + 1 < len(new_lines):
                nxt = new_lines[i + 1]
                if nxt.strip() == '':
                    continue  # 已经有空行
                # 下一行是列表 → 不空行
                if re.match(r'^\s*[-*+]\s', nxt) or re.match(r'^\s*\d+[.)、]\s', nxt):
                    continue
                # 下一行是其他正文/标题/引用 → 插入空行
                final_lines.append('')
                n_changes += 1

    return '\n'.join(final_lines), n_changes


def process_file(path: Path) -> dict:
    """处理单个文件，返回变更报告（不写回）。"""
    original = path.read_text(encoding='utf-8')
    content = original

    content, n_prefix = remove_number_prefixes(content)
    content, n_h4 = h4_to_h5(content)
    content, n_h3 = h3_to_h2_if_loose(content)
    content, n_sep = ensure_h2_separators(content)
    content, n_code_blanks = fix_code_block_blank_lines(content)
    content, n_punct = fix_punct_space(content)
    code_issues = check_code_blocks(content)

    return {
        'file': str(path),
        'changed': content != original,
        'number_prefixes_removed': n_prefix,
        'h4_to_h5': n_h4,
        'h3_to_h2': n_h3,
        'h2_separators_added': n_sep,
        'code_block_blanks_fixed': n_code_blanks,
        'punct_space_fixed': n_punct,
        'code_issues': code_issues,
    }


def _apply_writes(path: Path) -> None:
    """应用所有 transform 并写回。"""
    content = path.read_text(encoding='utf-8')
    for transform in (
        remove_number_prefixes,
        h4_to_h5,
        h3_to_h2_if_loose,
        ensure_h2_separators,
        fix_code_block_blank_lines,
        fix_punct_space,
    ):
        content, _ = transform(content)
    path.write_text(content, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('files', nargs='+', help='要处理的文件')
    parser.add_argument('--write', action='store_true', help='写回文件（默认只报告）')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    args = parser.parse_args()

    results = []
    totals = {
        'number_prefixes_removed': 0,
        'h4_to_h5': 0,
        'h3_to_h2': 0,
        'h2_separators_added': 0,
        'code_block_blanks_fixed': 0,
        'punct_space_fixed': 0,
        'code_issues': 0,
    }

    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f'[!] 跳过不存在的文件: {f}', file=sys.stderr)
            continue
        result = process_file(path)
        results.append(result)

        if args.write and result['changed']:
            _apply_writes(path)

        for k in totals:
            if k == 'code_issues':
                totals[k] += len(result[k])
            else:
                totals[k] += result[k]

    if args.json:
        print(json.dumps({'results': results, 'totals': totals}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            status = '✓ 改动' if r['changed'] else '— 无变化'
            print(f'{r["file"]}: {status}')
            if r['number_prefixes_removed']:
                print(f'  数字标号去除: {r["number_prefixes_removed"]}')
            if r['h4_to_h5']:
                print(f'  H4 → H5: {r["h4_to_h5"]}')
            if r['h3_to_h2']:
                print(f'  H3 → H2 (无 H2 时): {r["h3_to_h2"]}')
            if r['h2_separators_added']:
                print(f'  H2 分隔符 ---: {r["h2_separators_added"]}')
            if r['code_block_blanks_fixed']:
                print(f'  代码块空行: {r["code_block_blanks_fixed"]}')
            if r['punct_space_fixed']:
                print(f'  标点空格修复: {r["punct_space_fixed"]}')
            for issue in r['code_issues']:
                msg = f'line {issue["line"]}: 缺语言标签' if issue['kind'] == 'missing_lang' \
                    else f'line {issue["line"]}: 未知语言 "{issue["lang"]}"'
                print(f'  代码块: {msg}')
        print(
            f'\n合计: 数字标号 {totals["number_prefixes_removed"]}, '
            f'H4→H5 {totals["h4_to_h5"]}, '
            f'H3→H2 {totals["h3_to_h2"]}, '
            f'H2 分隔符 {totals["h2_separators_added"]}, '
            f'代码块空行 {totals["code_block_blanks_fixed"]}, '
            f'标点空格 {totals["punct_space_fixed"]}, '
            f'代码块问题 {totals["code_issues"]}'
        )

    return 0


if __name__ == '__main__':
    sys.exit(main())
