"""Release-facing instructions must describe the actual branch's development build."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pack_model import ROOT, load_toml
from release_metadata import check_documentation


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        for name in (
            "pack.toml",
            "README.md",
            "docs/release-notes.md",
            "docs/verification.md",
            "docs/version-policy.md",
        ):
            shutil.copyfile(ROOT / name, self.root / name)
        self.line = load_toml(ROOT / "release-policy.toml")["version-branch"]

    def test_current_documentation(self):
        check_documentation(self.root, self.line)

    def test_old_version_or_branch_instructions_fail(self):
        version = load_toml(self.root / "pack.toml")["version"]
        for name in (
            "README.md",
            "docs/release-notes.md",
            "docs/verification.md",
            "docs/version-policy.md",
        ):
            path = self.root / name
            original = path.read_text()
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "documentation"):
                path.write_text(original.replace(version, "26.2.99.99.99"))
                check_documentation(self.root, self.line)
            path.write_text(original)
        wrong = "26.3" if self.line == "26.2" else "26.2"
        with self.assertRaisesRegex(ValueError, "documentation"):
            check_documentation(self.root, wrong)

    def test_pack_advance_requires_updated_documentation(self):
        path = self.root / "pack.toml"
        version = load_toml(path)["version"]
        path.write_text(path.read_text().replace(version, "26.2.99.99.99"))
        with self.assertRaisesRegex(ValueError, "documentation"):
            check_documentation(self.root, self.line)

    def test_release_example_tag_cannot_lag_the_current_version(self):
        path = self.root / "docs/version-policy.md"
        version = load_toml(self.root / "pack.toml")["version"]
        original = path.read_text()
        for command in (f"--tag v{version}", f"make release RELEASE_TAG=v{version}"):
            path.write_text(original.replace(command, command.replace(version, "26.2.99.99.99")))
            with self.subTest(command=command), self.assertRaisesRegex(ValueError, "documentation"):
                check_documentation(self.root, self.line)

    def test_shader_acceptance_matches_bundled_choices(self):
        acceptance = (ROOT / "docs/acceptance-tests.md").read_text().casefold()
        for obsolete in (
            "no shader pack is supplied",
            "no shader is supplied",
            "separately installed known-good shader",
            "shaders absent",
        ):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, acceptance)
        self.assertIn("shader owner acceptance matrix", acceptance)

    def test_owner_matrices_use_this_branchs_target(self):
        target = load_toml(ROOT / "pack.toml")["versions"]["minecraft"]
        content = (ROOT / "docs/acceptance-tests.md").read_text()
        self.assertIn(f"Run on the maintained {target} artifact", content)
        self.assertIn(f"Run against the final {target} archive", content)

    def test_current_renderer_configuration_statement_matches_the_pin(self):
        import json

        evidence = json.loads((ROOT / "docs/upstream-metadata.json").read_text())
        iris = evidence["projects"]["YL57xq9U"]["versions"][0]["version_number"].split("+")[0]
        self.assertIn(f"Iris {iris} is active", (ROOT / "docs/configuration.md").read_text())
