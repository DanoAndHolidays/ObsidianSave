import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'collect_changed_notes.py'
SPEC = importlib.util.spec_from_file_location('collect_changed_notes', SCRIPT)
collector = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(collector)


class CollectChangedNotesTests(unittest.TestCase):
    def git(self, root, *args):
        subprocess.run(
            ['git', *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_collects_committed_and_untracked_notes_but_excludes_skill_docs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.git(root, 'init')
            (root / 'tracked.md').write_text('# tracked\n', encoding='utf-8')
            self.git(root, 'add', 'tracked.md')
            self.git(
                root,
                '-c', 'user.name=Test',
                '-c', 'user.email=test@example.com',
                'commit', '-m', 'initial',
            )
            self.git(root, 'tag', 'obsidian-organized-2026-07-14')

            (root / 'tracked.md').write_text('# tracked\nchanged\n', encoding='utf-8')
            (root / '新笔记.md').write_text('# 新笔记\n', encoding='utf-8')
            skill_dir = root / '.claude' / 'skills' / 'demo'
            skill_dir.mkdir(parents=True)
            (skill_dir / 'SKILL.md').write_text('# skill\n', encoding='utf-8')

            result = collector.collect_changed_notes(root)

        self.assertEqual(result['baseline'], 'obsidian-organized-2026-07-14')
        self.assertEqual(result['files'], ['tracked.md', '新笔记.md'])


if __name__ == '__main__':
    unittest.main()
