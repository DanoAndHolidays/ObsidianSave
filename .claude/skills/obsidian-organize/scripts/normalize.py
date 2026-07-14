#!/usr/bin/env python3
"""
Obsidian 笔记机械化规范化脚本

处理纯正则可解的违规，不做任何需要判断的修改。
所有改动幂等（重复运行无副作用），并保留 YAML frontmatter 与代码块内容。

使用：
    python normalize.py <file1.md> [file2.md ...]         # 只报告
    python normalize.py --write <file1.md> [file2.md ...] # 写回文件
    python normalize.py --json <file1.md>                 # JSON 输出供程序消费
    python normalize.py --write --default-lang text <file.md>  # 经判断后补缺失标签
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

def configure_console_output() -> None:
    """仅在 CLI 入口配置 Windows UTF-8，避免模块导入时修改全局输出流。"""
    if sys.platform == 'win32':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')

# 数字标号：## 1. xxx / ## 1、xxx / ### 一、 xxx / ### 1) xxx
NUMBER_PREFIX = re.compile(
    r'^(#{2,6})\s+([一二三四五六七八九十]+|\d+)[.、．\)]\s+',
    re.MULTILINE,
)

# H4 标题行
H4_PATTERN = re.compile(r'^####(\s)', re.MULTILINE)
H6_PATTERN = re.compile(r'^######(\s)', re.MULTILINE)

# 独占一行、以冒号结尾的粗体伪标题
BOLD_PSEUDO_HEADING = re.compile(
    r'^\*\*(.{1,80}?)[：:]\*\*\s*$',
    re.MULTILINE,
)

# 代码块围栏
FENCE = re.compile(r'^```(\S*)\s*$')

# 合法语言标签
LEGAL_LANGS = {
    'jsx', 'tsx', 'ts', 'typescript', 'js', 'javascript', 'css', 'scss', 'html',
    'bash', 'sh', 'shell', 'powershell', 'pwsh', 'cmd', 'batch',
    'json', 'yaml', 'yml', 'md', 'markdown', 'text',
    # 等价别名（保留原样，不强制转换）
    'vue', 'py', 'python', 'go', 'java', 'c', 'cpp', 'rust', 'sql', 'xml',
}

# 中英文标点之间多余空格（如 "。 **" → "。**"），不跨换行
PUNCT_SPACE = re.compile(r'([。！？，：；])[ \t]+(?=\*\*|[一-龥])')

# 标题行
H1 = re.compile(r'^#\s+\S')
H2 = re.compile(r'^##\s+\S')
H3 = re.compile(r'^###\s+\S')
HEADING_H2_H6 = re.compile(r'^#{2,6}\s+\S')
HEADING_ANY = re.compile(r'^#{1,6}\s+\S')

# H1 + `> Last Format Time：M/D/YYYY HH:MM:SS` 紧邻
H1_WITH_META = re.compile(
    r'^(# .+)\n(> Last Format Time：\d+/\d+/\d+ \d+:\d+:\d+ ?)$',
    re.MULTILINE,
)
META_LINE = re.compile(
    r'^> Last Format Time：\d+/\d+/\d+ \d+:\d+:\d+ ?$'
)

# 裸 URL（一行就是 URL）
BARE_URL = re.compile(r'^https?://\S+$')


def split_frontmatter(content: str) -> tuple[str, str]:
    """分离文件开头的 YAML frontmatter；返回值可直接拼接复原。"""
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != '---':
        return '', content

    for i, line in enumerate(lines[1:], 1):
        if line.strip() in {'---', '...'}:
            return ''.join(lines[:i + 1]), ''.join(lines[i + 1:])
    return '', content


def mask_fenced_code(content: str) -> tuple[str, dict[str, str]]:
    """用占位行保护 fenced code，避免文本正则修改代码内容。"""
    lines = content.split('\n')
    output: list[str] = []
    blocks: dict[str, str] = {}
    current: list[str] = []
    in_block = False

    for line in lines:
        if not in_block and FENCE.match(line):
            in_block = True
            current = [line]
            continue
        if in_block:
            current.append(line)
            if FENCE.match(line):
                token = f'\x00CODEBLOCK{len(blocks):08d}\x00'
                blocks[token] = '\n'.join(current)
                output.append(token)
                current = []
                in_block = False
            continue
        output.append(line)

    if current:
        token = f'\x00CODEBLOCK{len(blocks):08d}\x00'
        blocks[token] = '\n'.join(current)
        output.append(token)
    return '\n'.join(output), blocks


def restore_fenced_code(content: str, blocks: dict[str, str]) -> str:
    """还原由 mask_fenced_code 生成的占位行。"""
    for token, block in blocks.items():
        content = content.replace(token, block)
    return content


def apply_outside_fenced_code(content: str, transform) -> tuple[str, int]:
    """仅对 fenced code 之外的文本运行单个机械转换。"""
    masked, blocks = mask_fenced_code(content)
    transformed, count = transform(masked)
    return restore_fenced_code(transformed, blocks), count


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


def h6_to_h5(content: str) -> tuple[str, int]:
    """###### 标题调整为 #####。"""
    matches = H6_PATTERN.findall(content)
    if not matches:
        return content, 0
    return H6_PATTERN.sub(r'#####\1', content), len(matches)


def bold_pseudo_headings_to_h3(content: str) -> tuple[str, int]:
    """把独占一行且以冒号结尾的粗体小标题转换为 H3。"""
    return BOLD_PSEUDO_HEADING.subn(r'### \1', content)


def ensure_h1_title(content: str, expected_title: str) -> tuple[str, int]:
    """确保正文第一个 H1 存在且与文件名一致，不触碰代码块。"""
    if not expected_title:
        return content, 0

    masked, blocks = mask_fenced_code(content)
    lines = masked.split('\n')
    expected = f'# {expected_title}'
    h1_index = next(
        (i for i, line in enumerate(lines) if re.match(r'^#(?:\s.*)?$', line)),
        None,
    )
    if h1_index is None:
        masked = expected + '\n' + masked.lstrip('\n')
        return restore_fenced_code(masked, blocks), 1
    if lines[h1_index] == expected:
        return content, 0
    lines[h1_index] = expected
    return restore_fenced_code('\n'.join(lines), blocks), 1


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
            if m.group(1):
                issues.append({
                    'line': i,
                    'kind': 'invalid_closing_fence',
                    'lang': m.group(1),
                })
            in_block = False
    if in_block:
        issues.append({'line': open_line, 'kind': 'unclosed_fence'})
    return issues


def check_manual_issues(content: str) -> list[dict]:
    """报告无法可靠推断的结构问题，保留给用户或 Agent 判断。"""
    issues = []
    frontmatter, body = split_frontmatter(content)
    line_offset = frontmatter.count('\n')
    in_code = False
    for i, line in enumerate(body.splitlines(), 1 + line_offset):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r'^(#{1,6})\s*$', line)
        if match:
            issues.append({
                'line': i,
                'kind': 'empty_heading',
                'level': len(match.group(1)),
            })
    return issues


def remove_trailing_empty_heading(content: str) -> tuple[str, int]:
    """删除文件末尾没有任何内容的空标题；非末尾空标题仍交给报告。"""
    masked, blocks = mask_fenced_code(content)
    lines = masked.split('\n')
    last_nonblank = next(
        (i for i in range(len(lines) - 1, -1, -1) if lines[i].strip()),
        None,
    )
    if last_nonblank is None:
        return content, 0
    if not re.match(r'^#{1,6}\s*$', lines[last_nonblank]):
        return content, 0
    del lines[last_nonblank]
    while len(lines) > 1 and lines[-1] == '' and lines[-2] == '':
        lines.pop()
    return restore_fenced_code('\n'.join(lines), blocks), 1


def set_missing_code_languages(
    content: str,
    language: str,
) -> tuple[str, int, int]:
    """显式补充缺失语言，并把带后缀的闭合围栏规范为纯 ```。"""
    if language not in LEGAL_LANGS:
        raise ValueError(f'unsupported code language: {language}')

    lines = content.split('\n')
    in_block = False
    languages_added = 0
    closings_fixed = 0
    for i, line in enumerate(lines):
        match = FENCE.match(line)
        if not match:
            continue
        if not in_block:
            if not match.group(1):
                lines[i] = f'```{language}'
                languages_added += 1
            in_block = True
        else:
            if match.group(1):
                lines[i] = '```'
                closings_fixed += 1
            in_block = False
    return '\n'.join(lines), languages_added, closings_fixed


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


def update_h1_metadata(
    content: str,
    now: datetime.datetime = None,
    force: bool = False,
) -> tuple[str, int]:
    """
    紧跟 H1 添加/更新 `> Last Format Time：M/D/YYYY HH:MM:SS` 块。
    - 已存在且本次发生其他格式修改 → 更新时间戳
    - 已存在且没有其他格式修改 → 保持不变，确保幂等
    - 不存在 → 在 H1 下一行插入
    """
    if now is None:
        now = datetime.datetime.now()
    meta_line = f"> Last Format Time：{now.month}/{now.day}/{now.year} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"

    # 已存在且无需刷新则保持原样
    if H1_WITH_META.search(content) and not force:
        return content, 0

    # 已存在且发生了其他格式修改则更新时间
    if H1_WITH_META.search(content):
        return H1_WITH_META.sub(rf'\1\n{meta_line}', content), 1

    # 不存在则插入
    h1_match = re.search(r'^(# .+)$', content, re.MULTILINE)
    if not h1_match:
        return content, 0
    h1_end = h1_match.end()
    return content[:h1_end] + '\n' + meta_line + '\n' + content[h1_end:], 1


def normalize_h1_spacing(content: str) -> tuple[str, int]:
    """把 H1 元信息块后的连续空行规范为一行。"""
    lines = content.split('\n')
    for i, line in enumerate(lines[:-1]):
        if not H1.match(line):
            continue
        if i + 1 >= len(lines) or not META_LINE.match(lines[i + 1].strip()):
            return content, 0
        start = i + 2
        end = start
        while end < len(lines) and lines[end].strip() == '':
            end += 1
        if end == len(lines):
            desired = []
        else:
            desired = ['']
        current = lines[start:end]
        if current == desired:
            return content, 0
        lines[start:end] = desired
        return '\n'.join(lines), 1
    return content, 0


def wrap_bare_urls_under_h1(content: str) -> tuple[str, int]:
    """
    在 H1（和其 `> Last Format Time` 块）下方的"链接区域"内，把裸 URL 包成 `[URL](URL)`。
    链接区域 = 紧随 H1/meta 之后的连续行，直到遇到非链接内容为止。
    链接区域内的合法形式：
      - 裸 URL `https://...` → 包成 `[URL](URL)`
      - 已有 `[text](url)`  → 保留
    其他行（标题/列表/代码/正文/空行）→ 链接区域结束

    如果链接区域后面紧跟标题（非空行、非列表），补一个空行。
    """
    lines = content.split('\n')

    h1_idx = None
    for i, l in enumerate(lines):
        if H1.match(l):
            h1_idx = i
            break
    if h1_idx is None:
        return content, 0

    # 跳过 `> Last Format Time` 块 + 紧随的空行
    start = h1_idx + 1
    if start < len(lines) and META_LINE.match(lines[start].strip()):
        start += 1
    while start < len(lines) and lines[start].strip() == '':
        start += 1

    n_changes = 0
    saw_link = False
    i = start
    while i < len(lines):
        l = lines[i].strip()
        if not l:
            break
        if BARE_URL.match(l):
            lines[i] = f'[{l}]({l})'
            n_changes += 1
            saw_link = True
            i += 1
            continue
        if re.match(r'^\[.+\]\(.+\)$', l):
            saw_link = True
            i += 1
            continue
        break

    # 链接区域后紧跟标题则补空行
    if saw_link and i < len(lines):
        nxt = lines[i]
        if nxt.strip() != '' and re.match(r'^#{1,6}\s', nxt):
            lines.insert(i, '')
            n_changes += 1

    return '\n'.join(lines), n_changes


def ensure_h2_separators(content: str) -> tuple[str, int]:
    """
    确保每个 H2 紧上方有 `---` 分隔符。
    结构：content\n\n---\n## H2

    所有 H2 都必须有此分隔符，包括首个 H2（无论 H1 区域与首个 H2 之间
    是否有链接或引言段落）。
    """
    lines = content.split('\n')

    # 找所有 H2 的位置
    h2_indices = [i for i, l in enumerate(lines) if H2.match(l)]

    if not h2_indices:
        return content, 0

    n_changes = 0
    new_lines = list(lines)

    # 自底向上处理（避免插入影响前面的索引）
    for idx in reversed(h2_indices):
        # 检测 `---` 位置：idx-1（紧邻）或 idx-2（隔一空行）
        has_sep_direct = (
            idx - 1 >= 0 and new_lines[idx - 1].strip() == '---'
        )
        has_sep_with_blank = (
            idx - 2 >= 0
            and new_lines[idx - 1].strip() == ''
            and new_lines[idx - 2].strip() == '---'
        )

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


def remove_spurious_separators(content: str) -> tuple[str, int]:
    """
    删除不在 H2 紧上方（含隔一空行）的 `---` 行。
    `---` 是 H2 专用的章节分隔符，出现在 H3/H4/H5/H6/正文前均为误用。
    须跟踪代码块状态，避免触碰围栏内的 `---`。
    """
    lines = content.split('\n')
    in_code = False
    to_remove: set[int] = set()

    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.strip() != '---':
            continue

        # `---` 行在代码块外。跳过空行找下一个非空行
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1

        if j >= len(lines):
            # 文件末尾孤立的 ---
            to_remove.add(i)
            continue

        # 下一个非空行必须是 H2（紧邻或隔一空行均可），否则删 ---
        if not H2.match(lines[j]):
            to_remove.add(i)

    if not to_remove:
        return content, 0

    new_lines = [l for idx, l in enumerate(lines) if idx not in to_remove]
    return '\n'.join(new_lines), len(to_remove)


def remove_blank_after_headings(content: str) -> tuple[str, int]:
    """
    删除 H2-H6 标题后紧接的空行。
    规则：标题 → 正文/列表/代码块/下一级标题 均不空行。
    唯一例外：标题 → `> 引用块` 空一行（保留空行）。
    H1 跳过（其元信息块由 update_h1_metadata 处理）。
    须跟踪代码块状态。
    """
    lines = content.split('\n')
    in_code = False
    to_remove: set[int] = set()

    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not HEADING_H2_H6.match(line):
            continue

        # 下一行必须是空行才有得删
        if i + 1 >= len(lines):
            continue
        if lines[i + 1].strip() != '':
            continue  # 不空行，合规

        # 下一行是空行，看再下一行决定
        if i + 2 >= len(lines):
            # 标题后空行直达文件末尾 → 删空行
            to_remove.add(i + 1)
            continue

        next_content = lines[i + 2]
        if next_content.strip().startswith('> '):
            continue  # 引用块，保留空行

        to_remove.add(i + 1)

    if not to_remove:
        return content, 0

    new_lines = [l for idx, l in enumerate(lines) if idx not in to_remove]
    return '\n'.join(new_lines), len(to_remove)


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


def normalize_content(
    content: str,
    now: datetime.datetime = None,
    default_lang: str = None,
    expected_title: str = None,
) -> tuple[str, dict]:
    """规范化内容并返回统计；frontmatter 与 fenced code 内容保持不变。"""
    frontmatter, body = split_frontmatter(content)
    original_body = body

    body, n_h1_title = ensure_h1_title(body, expected_title)
    body, n_prefix = apply_outside_fenced_code(body, remove_number_prefixes)
    body, n_h4 = apply_outside_fenced_code(body, h4_to_h5)
    body, n_h6 = apply_outside_fenced_code(body, h6_to_h5)
    body, n_pseudo = apply_outside_fenced_code(body, bold_pseudo_headings_to_h3)
    body, n_h3 = apply_outside_fenced_code(body, h3_to_h2_if_loose)
    body, n_trailing_empty = remove_trailing_empty_heading(body)
    body, n_urls = wrap_bare_urls_under_h1(body)
    body, n_spur = remove_spurious_separators(body)
    body, n_sep = apply_outside_fenced_code(body, ensure_h2_separators)
    body, n_blank_after = remove_blank_after_headings(body)
    body, n_code_blanks = fix_code_block_blank_lines(body)
    body, n_punct = apply_outside_fenced_code(body, fix_punct_space)

    body, n_lang_added, n_closing_fixed = set_missing_code_languages(
        body,
        default_lang or 'text',
    )
    body, n_h1_spacing_before = normalize_h1_spacing(body)
    format_changed = body != original_body
    body, n_meta = update_h1_metadata(body, now=now, force=format_changed)
    body, n_h1_spacing_after = normalize_h1_spacing(body)
    n_h1_spacing = n_h1_spacing_before + n_h1_spacing_after
    normalized = frontmatter + body
    code_issues = check_code_blocks(normalized)
    manual_issues = check_manual_issues(normalized)

    stats = {
        'h1_title_fixed': n_h1_title,
        'number_prefixes_removed': n_prefix,
        'h4_to_h5': n_h4,
        'h6_to_h5': n_h6,
        'h3_to_h2': n_h3,
        'bold_pseudo_headings_to_h3': n_pseudo,
        'trailing_empty_headings_removed': n_trailing_empty,
        'h1_meta_updated': n_meta,
        'h1_spacing_fixed': n_h1_spacing,
        'h1_urls_wrapped': n_urls,
        'spurious_separators_removed': n_spur,
        'h2_separators_added': n_sep,
        'blank_after_heading_removed': n_blank_after,
        'code_block_blanks_fixed': n_code_blanks,
        'punct_space_fixed': n_punct,
        'code_languages_added': n_lang_added,
        'closing_fences_fixed': n_closing_fixed,
        'code_issues': code_issues,
        'manual_issues': manual_issues,
    }
    return normalized, stats


def process_file(
    path: Path,
    write: bool = False,
    now: datetime.datetime = None,
    default_lang: str = None,
) -> dict:
    """处理单个文件，返回报告；write=True 时写入同一次计算结果。"""
    original = path.read_text(encoding='utf-8')
    normalized, stats = normalize_content(
        original,
        now=now,
        default_lang=default_lang,
        expected_title=path.stem,
    )
    changed = normalized != original
    if write and changed:
        path.write_text(normalized, encoding='utf-8')
    return {
        'file': str(path),
        'changed': changed,
        **stats,
    }


def main() -> int:
    configure_console_output()
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('files', nargs='+', help='要处理的文件')
    parser.add_argument('--write', action='store_true', help='写回文件（默认只报告）')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    parser.add_argument(
        '--default-lang',
        choices=sorted(LEGAL_LANGS),
        help='为缺失标签的代码块指定统一语言（默认 text）',
    )
    args = parser.parse_args()

    results = []
    totals = {
        'h1_title_fixed': 0,
        'number_prefixes_removed': 0,
        'h4_to_h5': 0,
        'h6_to_h5': 0,
        'h3_to_h2': 0,
        'bold_pseudo_headings_to_h3': 0,
        'trailing_empty_headings_removed': 0,
        'h1_meta_updated': 0,
        'h1_spacing_fixed': 0,
        'h1_urls_wrapped': 0,
        'spurious_separators_removed': 0,
        'h2_separators_added': 0,
        'blank_after_heading_removed': 0,
        'code_block_blanks_fixed': 0,
        'punct_space_fixed': 0,
        'code_languages_added': 0,
        'closing_fences_fixed': 0,
        'code_issues': 0,
        'manual_issues': 0,
    }

    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f'[!] 跳过不存在的文件: {f}', file=sys.stderr)
            continue
        result = process_file(
            path,
            write=args.write,
            default_lang=args.default_lang,
        )
        results.append(result)

        for k in totals:
            if k in {'code_issues', 'manual_issues'}:
                totals[k] += len(result[k])
            else:
                totals[k] += result[k]

    if args.json:
        print(json.dumps({'results': results, 'totals': totals}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            status = '✓ 改动' if r['changed'] else '— 无变化'
            print(f'{r["file"]}: {status}')
            if r['h1_title_fixed']:
                print(f'  H1 标题修复: {r["h1_title_fixed"]}')
            if r['number_prefixes_removed']:
                print(f'  数字标号去除: {r["number_prefixes_removed"]}')
            if r['h4_to_h5']:
                print(f'  H4 → H5: {r["h4_to_h5"]}')
            if r['h6_to_h5']:
                print(f'  H6 → H5: {r["h6_to_h5"]}')
            if r['h3_to_h2']:
                print(f'  H3 → H2 (无 H2 时): {r["h3_to_h2"]}')
            if r['bold_pseudo_headings_to_h3']:
                print(f'  粗体伪标题 → H3: {r["bold_pseudo_headings_to_h3"]}')
            if r['trailing_empty_headings_removed']:
                print(f'  尾部空标题删除: {r["trailing_empty_headings_removed"]}')
            if r['h1_meta_updated']:
                print(f'  H1 元信息块: {r["h1_meta_updated"]}')
            if r['h1_spacing_fixed']:
                print(f'  H1 区域空行: {r["h1_spacing_fixed"]}')
            if r['h1_urls_wrapped']:
                print(f'  H1 裸 URL 包裹: {r["h1_urls_wrapped"]}')
            if r['spurious_separators_removed']:
                print(f'  误用 --- 删除: {r["spurious_separators_removed"]}')
            if r['h2_separators_added']:
                print(f'  H2 分隔符 ---: {r["h2_separators_added"]}')
            if r['blank_after_heading_removed']:
                print(f'  标题后空行删除: {r["blank_after_heading_removed"]}')
            if r['code_block_blanks_fixed']:
                print(f'  代码块空行: {r["code_block_blanks_fixed"]}')
            if r['punct_space_fixed']:
                print(f'  标点空格修复: {r["punct_space_fixed"]}')
            if r['code_languages_added']:
                print(f'  代码块语言补充: {r["code_languages_added"]}')
            if r['closing_fences_fixed']:
                print(f'  闭合围栏修复: {r["closing_fences_fixed"]}')
            for issue in r['code_issues']:
                if issue['kind'] == 'missing_lang':
                    msg = f'line {issue["line"]}: 缺语言标签'
                elif issue['kind'] == 'invalid_closing_fence':
                    msg = f'line {issue["line"]}: 闭合围栏带非法后缀 "{issue["lang"]}"'
                elif issue['kind'] == 'unclosed_fence':
                    msg = f'line {issue["line"]}: 代码块未闭合'
                else:
                    msg = f'line {issue["line"]}: 未知语言 "{issue["lang"]}"'
                print(f'  代码块: {msg}')
            for issue in r['manual_issues']:
                if issue['kind'] == 'empty_heading':
                    print(
                        f'  待确认: line {issue["line"]}: '
                        f'空 H{issue["level"]} 标题'
                    )
        print(
            f'\n合计: H1 标题 {totals["h1_title_fixed"]}, '
            f'数字标号 {totals["number_prefixes_removed"]}, '
            f'H4→H5 {totals["h4_to_h5"]}, '
            f'H6→H5 {totals["h6_to_h5"]}, '
            f'H3→H2 {totals["h3_to_h2"]}, '
            f'伪标题→H3 {totals["bold_pseudo_headings_to_h3"]}, '
            f'尾部空标题 {totals["trailing_empty_headings_removed"]}, '
            f'H1 元信息 {totals["h1_meta_updated"]}, '
            f'H1 空行 {totals["h1_spacing_fixed"]}, '
            f'H1 裸URL {totals["h1_urls_wrapped"]}, '
            f'误用--- {totals["spurious_separators_removed"]}, '
            f'H2 分隔符 {totals["h2_separators_added"]}, '
            f'标题后空行 {totals["blank_after_heading_removed"]}, '
            f'代码块空行 {totals["code_block_blanks_fixed"]}, '
            f'标点空格 {totals["punct_space_fixed"]}, '
            f'代码块语言 {totals["code_languages_added"]}, '
            f'闭合围栏 {totals["closing_fences_fixed"]}, '
            f'代码块问题 {totals["code_issues"]}, '
            f'待确认 {totals["manual_issues"]}'
        )

    return 0


if __name__ == '__main__':
    sys.exit(main())
