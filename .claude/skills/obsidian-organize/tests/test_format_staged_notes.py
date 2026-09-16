import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))
SCRIPT = SCRIPT_DIR / 'format_staged_notes.py'
SPEC = importlib.util.spec_from_file_location('format_staged_notes', SCRIPT)
formatter = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(formatter)


class FormatStagedNotesTests(unittest.TestCase):
    def git(self, root, *args, text=False):
        result = subprocess.run(
            ['git', *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode('utf-8') if text else result.stdout

    def init_repo(self, root):
        self.git(root, 'init')
        self.git(root, 'config', 'user.name', 'Test')
        self.git(root, 'config', 'user.email', 'test@example.com')
        note = root / 'note.md'
        note.write_text(
            '# note\n'
            '> Last Format Time：7/14/2026 10:30:00\n\n'
            '---\n'
            '## Section\n'
            '正文\n',
            encoding='utf-8',
        )
        self.git(root, 'add', 'note.md')
        self.git(root, 'commit', '-m', 'initial')
        return note

    def test_formats_and_restages_fully_staged_note(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = self.init_repo(root)
            note.write_text(
                '# note\n'
                '> Last Format Time：7/14/2026 10:30:00\n\n'
                '## 1. Updated\n\n'
                '正文\n',
                encoding='utf-8',
            )
            self.git(root, 'add', 'note.md')

            report, exit_code = formatter.run(root)

            staged = self.git(root, 'show', ':note.md', text=True)
            self.assertEqual(exit_code, 0)
            self.assertEqual(report['formatted_files'], ['note.md'])
            self.assertIn('\n---\n## Updated\n正文\n', staged)
            self.assertEqual(self.git(root, 'diff', '--name-only', text=True), '')

    def test_rejects_partially_staged_note_without_rewriting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = self.init_repo(root)
            staged_content = note.read_text(encoding='utf-8') + '已暂存\n'
            note.write_text(staged_content, encoding='utf-8')
            self.git(root, 'add', 'note.md')
            worktree_content = staged_content + '未暂存\n'
            note.write_text(worktree_content, encoding='utf-8')

            report, exit_code = formatter.run(root)

            self.assertEqual(exit_code, 2)
            self.assertEqual(report['error'], 'partially_staged_notes')
            self.assertEqual(note.read_text(encoding='utf-8'), worktree_content)

    def test_unclosed_fence_blocks_without_rewriting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = self.init_repo(root)
            content = '# note\n```TypeScript\nconst value = 1\n'
            note.write_text(content, encoding='utf-8')
            self.git(root, 'add', 'note.md')

            report, exit_code = formatter.run(root)

            self.assertEqual(exit_code, 2)
            self.assertEqual(report['error'], 'unsafe_notes')
            self.assertEqual(note.read_text(encoding='utf-8'), content)


if __name__ == '__main__':
    unittest.main()
