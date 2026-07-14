import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / 'organize_changed_notes.py'
SPEC = importlib.util.spec_from_file_location('organize_changed_notes', SCRIPT)
organizer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(organizer)


class OrganizeChangedNotesTests(unittest.TestCase):
    def git(self, root, *args):
        subprocess.run(
            ['git', *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_preview_then_write_then_idempotent_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.git(root, 'init')
            (root / 'base.md').write_text('# base\n', encoding='utf-8')
            self.git(root, 'add', 'base.md')
            self.git(
                root,
                '-c', 'user.name=Test',
                '-c', 'user.email=test@example.com',
                'commit', '-m', 'initial',
            )
            self.git(root, 'tag', 'obsidian-organized-2026-07-14')
            note = root / '新笔记.md'
            note.write_text('正文\n```\n流程\n```0\n', encoding='utf-8')

            preview, preview_code = organizer.run(root)
            written, write_code = organizer.run(root, write=True)
            repeated, repeated_code = organizer.run(root)
            note_content = note.read_text(encoding='utf-8')

        self.assertEqual((preview_code, write_code, repeated_code), (0, 0, 0))
        self.assertEqual(preview['changed_count'], 1)
        self.assertEqual(written['changed_count'], 1)
        self.assertEqual(repeated['changed_count'], 0)
        self.assertEqual(repeated['code_issue_count'], 0)
        self.assertIn('```text\n流程\n```', note_content)


if __name__ == '__main__':
    unittest.main()
