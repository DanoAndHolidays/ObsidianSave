import datetime
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'normalize.py'
SPEC = importlib.util.spec_from_file_location('obsidian_normalize', SCRIPT)
normalize = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(normalize)


class NormalizeTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2026, 7, 14, 10, 30, 0)

    def test_preserves_frontmatter_exactly(self):
        source = (
            '---\n'
            'tags:\n'
            '  - 前端： Test\n'
            'aliases: ["---"]\n'
            '---\n'
            '# Note\n'
            '## Section\n'
            '正文\n'
        )
        result, _ = normalize.normalize_content(source, now=self.now)
        expected_frontmatter, _ = normalize.split_frontmatter(source)
        actual_frontmatter, _ = normalize.split_frontmatter(result)
        self.assertEqual(actual_frontmatter, expected_frontmatter)

    def test_preserves_fenced_code_content(self):
        source = (
            '# Note\n'
            '> Last Format Time：7/1/2026 09:00:00\n\n'
            '```markdown\n'
            '## 1. 代码里的标题\n'
            '中文： 空格必须保留\n'
            '---\n'
            '```\n'
        )
        result, _ = normalize.normalize_content(source, now=self.now)
        code = result.split('```markdown\n', 1)[1].split('\n```', 1)[0]
        self.assertEqual(code, '## 1. 代码里的标题\n中文： 空格必须保留\n---')

    def test_second_run_is_idempotent(self):
        source = '# Note\n## 1. Section\n正文\n'
        first, _ = normalize.normalize_content(source, now=self.now)
        later = datetime.datetime(2026, 7, 15, 11, 0, 0)
        second, stats = normalize.normalize_content(first, now=later)
        self.assertEqual(second, first)
        self.assertEqual(stats['h1_meta_updated'], 0)

    def test_refreshes_timestamp_when_format_changes(self):
        source = (
            '# Note\n'
            '> Last Format Time：7/1/2026 09:00:00\n\n'
            '## 1. Section\n'
            '正文\n'
        )
        result, stats = normalize.normalize_content(source, now=self.now)
        self.assertIn('> Last Format Time：7/14/2026 10:30:00', result)
        self.assertIn('\n---\n## Section\n', result)
        self.assertEqual(stats['h1_meta_updated'], 1)

    def test_write_uses_reported_result(self):
        source = '# Note\n## 1. Section\n正文\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'Note.md'
            path.write_text(source, encoding='utf-8')
            report = normalize.process_file(path, write=True, now=self.now)
            written = path.read_text(encoding='utf-8')
            expected, _ = normalize.normalize_content(source, now=self.now)
        self.assertTrue(report['changed'])
        self.assertEqual(written, expected)

    def test_explicit_default_language_and_invalid_closing_fence(self):
        source = '# Note\n```\n流程图\n```0\n'
        result, stats = normalize.normalize_content(
            source,
            now=self.now,
            default_lang='text',
        )
        self.assertIn('```text\n流程图\n```', result)
        self.assertEqual(stats['code_languages_added'], 1)
        self.assertEqual(stats['closing_fences_fixed'], 1)
        self.assertEqual(stats['code_issues'], [])

    def test_more_than_ten_code_blocks_restore_without_token_collisions(self):
        blocks = '\n\n'.join(
            f'```typescript\nconst value{i} = {i};\n```'
            for i in range(12)
        )
        source = f'# Note\n> Last Format Time：7/14/2026 10:30:00\n\n{blocks}\n'
        result, stats = normalize.normalize_content(source, now=self.now)
        self.assertEqual(result, source)
        self.assertEqual(stats['code_issues'], [])

    def test_wrapped_h1_link_is_idempotent_across_blank_line(self):
        source = (
            '# Note\n'
            '> Last Format Time：7/14/2026 10:30:00\n\n'
            '[https://example.com](https://example.com)\n\n'
            '---\n'
            '## Section\n'
            '正文\n'
        )
        result, stats = normalize.normalize_content(source, now=self.now)
        self.assertEqual(result, source)
        self.assertEqual(stats['h1_urls_wrapped'], 0)

    def test_process_file_uses_filename_for_missing_or_wrong_h1(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / '目标标题.md'
            missing.write_text('正文\n', encoding='utf-8')
            wrong = Path(directory) / '正确标题.md'
            wrong.write_text('# 错误标题\n正文\n', encoding='utf-8')
            normalize.process_file(missing, write=True, now=self.now)
            normalize.process_file(wrong, write=True, now=self.now)
            missing_result = missing.read_text(encoding='utf-8')
            wrong_result = wrong.read_text(encoding='utf-8')
        self.assertTrue(missing_result.startswith('# 目标标题\n'))
        self.assertTrue(wrong_result.startswith('# 正确标题\n'))

    def test_h1_numeric_prefix_is_preserved_when_it_is_in_filename(self):
        source = '# 1. Note\n正文\n'
        result, _ = normalize.normalize_content(
            source,
            now=self.now,
            expected_title='1. Note',
        )
        self.assertTrue(result.startswith('# 1. Note\n'))

    def test_scripted_heading_fixes_and_empty_heading_report(self):
        source = (
            '# Note\n'
            '> Last Format Time：7/1/2026 09:00:00\n\n\n'
            '---\n'
            '## Section\n'
            '**要点：**\n'
            '###### 深层标题\n'
            '## \n'
            '待确认正文\n'
        )
        result, stats = normalize.normalize_content(
            source,
            now=self.now,
            expected_title='Note',
        )
        self.assertIn('### 要点\n', result)
        self.assertIn('##### 深层标题\n', result)
        self.assertEqual(stats['h1_spacing_fixed'], 1)
        self.assertEqual(stats['bold_pseudo_headings_to_h3'], 1)
        self.assertEqual(stats['h6_to_h5'], 1)
        self.assertEqual(stats['manual_issues'][0]['kind'], 'empty_heading')

    def test_trailing_empty_heading_is_removed_without_manual_review(self):
        source = '# Note\n> Last Format Time：7/14/2026 10:30:00\n\n## \n'
        result, stats = normalize.normalize_content(
            source,
            now=self.now,
            expected_title='Note',
        )
        self.assertNotIn('## ', result)
        self.assertEqual(stats['trailing_empty_headings_removed'], 1)
        self.assertEqual(stats['manual_issues'], [])


if __name__ == '__main__':
    unittest.main()
