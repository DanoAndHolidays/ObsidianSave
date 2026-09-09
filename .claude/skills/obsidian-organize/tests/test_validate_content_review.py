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

    def test_inline_markers_are_valid(self):
        source = '# Note\n修正后的描述。 *已修改*\n新增重点。 *已补充*\n类型纠正。 *已纠正*\n'
        result = review.validate_content_review(source)
        self.assertEqual(result['entry_count'], 3)
        self.assertEqual(result['anchor_count'], 3)
        self.assertEqual(result['issues'], [])

    def test_legacy_protocol_is_rejected(self):
        source = '# Note\n修改一。〔CR-001〕\n## 内容审核变更记录\n### CR-001｜事实纠错\n'
        result = review.validate_content_review(source)
        kinds = {item['kind'] for item in result['issues']}
        self.assertIn('legacy_review_marker', kinds)
        self.assertIn('legacy_review_protocol', kinds)

    def test_marker_inside_code_is_rejected(self):
        source = '# Note\n```text\n*已修改*\n```\n'
        result = review.validate_content_review(source)
        self.assertEqual(result['issues'][0]['kind'], 'marker_in_code')


if __name__ == '__main__':
    unittest.main()
