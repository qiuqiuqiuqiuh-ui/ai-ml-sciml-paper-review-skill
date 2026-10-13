import json
import tempfile
import unittest
from pathlib import Path

from scripts.install_skill import differences, install


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "repo-checkout"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("---\nname: review-papers-rigorously\ndescription: Review papers.\n---\n# Version one\n", encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references" / "guide.md").write_text("# Guide", encoding="utf-8")
        (self.source / "README.md").write_text("Development docs", encoding="utf-8")
        self.target = self.base / "skills" / "review-papers-rigorously"

    def test_install_only_skill_files_and_verify(self):
        self.assertIsNone(install(self.source, self.target))
        self.assertFalse((self.target / "README.md").exists())
        self.assertEqual(differences(self.source, self.target), [])
        record = json.loads((self.target / "INSTALLATION.json").read_text(encoding="utf-8"))
        self.assertIn("references/guide.md", record["files"])

    def test_existing_installation_requires_explicit_update(self):
        install(self.source, self.target)
        with self.assertRaises(FileExistsError):
            install(self.source, self.target)

    def test_update_backs_up_and_preserves_local_files(self):
        install(self.source, self.target)
        original = (self.target / "SKILL.md").read_bytes()
        (self.target / "local-notes.txt").write_text("Keep this", encoding="utf-8")
        (self.source / "SKILL.md").write_text("---\nname: review-papers-rigorously\ndescription: Review papers.\n---\n# Version two\n", encoding="utf-8")
        self.assertTrue(differences(self.source, self.target))
        backup = install(self.source, self.target, update=True)
        self.assertEqual((backup / "SKILL.md").read_bytes(), original)
        self.assertEqual((self.target / "local-notes.txt").read_text(encoding="utf-8"), "Keep this")
        self.assertEqual(differences(self.source, self.target), [])

    def test_wrong_target_name_is_rejected(self):
        with self.assertRaises(ValueError):
            install(self.source, self.base / "wrong-name")

    def test_source_and_target_must_not_overlap(self):
        with self.assertRaises(ValueError):
            install(self.source, self.source / "review-papers-rigorously")
        self.assertFalse((self.source / "review-papers-rigorously").exists())

    def test_backup_must_not_be_inside_target(self):
        install(self.source, self.target)
        with self.assertRaises(ValueError):
            install(self.source, self.target, update=True, backup_dir=self.target / "backups")


if __name__ == "__main__":
    unittest.main()
