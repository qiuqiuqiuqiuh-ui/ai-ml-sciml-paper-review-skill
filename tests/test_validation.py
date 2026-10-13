import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_skill import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo-checkout"
        self.root.mkdir()
        self.skill = self.root / "SKILL.md"
        self.header = "---\nname: review-papers-rigorously\ndescription: Review research paper evidence.\n---\n"
        self.write_body("# Review\n")

    def write_body(self, body):
        self.skill.write_text(self.header + body, encoding="utf-8")

    def test_repository_name_can_differ(self):
        self.assertEqual(validate(self.root), [])

    def test_zip_directory_is_valid(self):
        renamed = self.root.with_name("repo-checkout-main")
        self.root.rename(renamed)
        self.assertEqual(validate(renamed), [])

    def test_installation_directory_must_match(self):
        self.assertTrue(validate(self.root, check_directory_name=True))
        installed = self.root.with_name("review-papers-rigorously")
        self.root.rename(installed)
        self.assertEqual(validate(installed, check_directory_name=True), [])

    def test_missing_resource_and_image_are_rejected(self):
        for body in ("[Guide](missing.md)", "![Icon](assets/icon.svg)"):
            with self.subTest(body=body):
                self.write_body(body)
                self.assertTrue(validate(self.root))

    def test_reference_links_and_spaces_are_checked(self):
        (self.root / "a guide.md").write_text("# Guide\n", encoding="utf-8")
        self.write_body("[Guide][guide]\n\n[guide]: <a guide.md#guide>\n")
        self.assertEqual(validate(self.root), [])
        (self.root / "a guide.md").unlink()
        self.assertTrue(validate(self.root))

    def test_unicode_and_duplicate_headings(self):
        self.write_body("# Review\n## 代码 `dtype` 检查\n## Repeat\n## Repeat\n[code](#代码-dtype-检查) [repeat](#repeat-1)\n")
        self.assertEqual(validate(self.root), [])
        self.write_body("# Review\n[Broken](#absent)\n")
        self.assertTrue(validate(self.root))

    def test_nested_documents_are_checked(self):
        nested = self.root / "references" / "nested"
        nested.mkdir(parents=True)
        (nested / "guide.md").write_text("[missing](missing.md)\n", encoding="utf-8")
        self.assertTrue(validate(self.root))

    def test_code_examples_are_not_links_or_scaffolds(self):
        self.write_body("# Review\n```md\n[missing](missing.md)\n[TODO: example]\n```\n`[missing](missing.md)`\n")
        self.assertEqual(validate(self.root), [])

    def test_body_and_description_scaffolds_are_rejected(self):
        self.write_body("# Review\n[TODO: write instructions]\n")
        self.assertTrue(validate(self.root))
        self.skill.write_text(self.header.replace("Review research paper evidence.", "'[TODO: describe]'"), encoding="utf-8")
        self.assertTrue(validate(self.root))

    def test_external_links_are_not_network_checked(self):
        self.write_body("[Source](https://example.invalid/paper#section)\n")
        self.assertEqual(validate(self.root), [])

    def test_path_cannot_escape_package(self):
        (self.root.parent / "outside.md").write_text("# Outside", encoding="utf-8")
        self.write_body("[Outside](../outside.md)\n")
        self.assertTrue(validate(self.root))

    def test_metadata_icon_and_policy(self):
        agent = self.root / "agents" / "openai.yaml"
        agent.parent.mkdir()
        data = {"interface": {"display_name": "Paper review", "short_description": "Review paper evidence and research claims", "default_prompt": "Use $review-papers-rigorously to review this paper."}, "policy": {"allow_implicit_invocation": True}}
        agent.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertEqual(validate(self.root), [])
        data["interface"]["icon_small"] = "assets/missing.svg"
        agent.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertTrue(validate(self.root))
        del data["interface"]["icon_small"]
        data["policy"]["allow_implicit_invocation"] = "false"
        agent.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertTrue(validate(self.root))


if __name__ == "__main__":
    unittest.main()
