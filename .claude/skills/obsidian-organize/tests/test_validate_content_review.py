import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'validate_content_review.py'
SPEC = importlib.util.spec_from_file_location('validate_content_review', SCRIPT)
review = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(review)


class ValidateContentReviewTests(unittest.TestCase):
    def test_note_without_semantic_changes_is_valid(self):
        result = review.validate_content_review('# Note\n正文\n')
        self.assertEqual(result['entry_count'], 0)
        self.assertEqual(result['issues'], [])

    def test_valid_marker_and_log(self):
        source = (
            '# Note\n'
            '修正后的描述。〔CR-001〕\n\n'
            '---\n'
            '## 内容审核变更记录\n'
            '### CR-001｜事实纠错\n'
            '- 日期：8/13/2026\n'
            '- 位置：第一段\n'
            '- 原内容：旧描述。\n'
            '- 调整后：修正后的描述。\n'
            '- 原因：旧描述不准确。\n'
            '- 依据：[官方文档](https://example.com/docs)\n'
        )
        result = review.validate_content_review(source)
        self.assertEqual(result['entry_count'], 1)
        self.assertEqual(result['anchor_count'], 1)
        self.assertEqual(result['issues'], [])

    def test_reports_orphans_missing_fields_and_invalid_evidence(self):
        source = (
            '# Note\n'
            '修改一。〔CR-001〕\n'
            '修改二。〔CR-002〕\n\n'
            '---\n'
            '## 内容审核变更记录\n'
            '### CR-001｜代码修正\n'
            '- 日期：2026-08-13\n'
            '- 位置：示例代码\n'
            '- 原内容：old()\n'
            '- 调整后：new()\n'
            '- 原因：旧调用无效。\n'
            '- 依据：无需外部依据（明显错误）\n'
            '### CR-003｜未知类型\n'
            '- 日期：8/13/2026\n'
        )
        result = review.validate_content_review(source)
        kinds = {item['kind'] for item in result['issues']}
        self.assertIn('invalid_date', kinds)
        self.assertIn('evidence_required', kinds)
        self.assertIn('orphan_anchor', kinds)
        self.assertIn('orphan_entry', kinds)
        self.assertIn('unsupported_type', kinds)
        self.assertIn('missing_field', kinds)

    def test_anchor_inside_code_is_rejected(self):
        source = '# Note\n```text\n〔CR-001〕\n```\n'
        result = review.validate_content_review(source)
        self.assertEqual(result['issues'][0]['kind'], 'anchor_in_code')


if __name__ == '__main__':
    unittest.main()
