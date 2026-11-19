"""Development names and release eligibility, without claiming runtime acceptance."""

import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from migration import validate_migration
from pack_model import ROOT, load_toml
from release_metadata import metadata


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("pack.toml", "collection.toml", "release-policy.toml", "migration.toml"):
            shutil.copyfile(ROOT / name, self.root / name)
        # Identity tests use the full intended inventory on either version branch.
        entries = load_toml(self.root / "migration.toml")["feature"]
        (self.root / "collection.toml").write_text(
            "\n".join(
                f'[[selected]]\nproject-id = "{p["project-id"]}"\n'
                f'slug = "{p["slug"]}"\nrole = "feature"\n'
                for p in entries
            )
        )
        self.version = load_toml(self.root / "pack.toml")["version"]
        self.line = load_toml(self.root / "release-policy.toml")["version-branch"]

    def replace(self, name, before, after):
        path = self.root / name
        self.assertIn(before, path.read_text())
        path.write_text(path.read_text().replace(before, after, 1))

    def qualify_fixture(self):
        # Synthetic acceptance is confined to a disposable test fixture.
        digest = hashlib.sha256((self.root / "pack.toml").read_bytes()).hexdigest()
        self.replace(
            "release-policy.toml",
            'runtime-accepted-version = ""',
            f'runtime-accepted-version = "{self.version}"',
        )
        self.replace(
            "release-policy.toml",
            'runtime-accepted-pack-sha256 = ""',
            f'runtime-accepted-pack-sha256 = "{digest}"',
        )
        self.replace(
            "release-policy.toml",
            'runtime-acceptance-record = ""',
            'runtime-acceptance-record = "docs/verification.md"',
        )
        (self.root / "docs").mkdir()
        (self.root / "docs/verification.md").write_text("Synthetic test fixture only.")

    def test_development_is_default_and_names_actual_target(self):
        info = metadata(self.root)
        self.assertEqual(info["channel"], "development")
        self.assertIn("Minecraft 26.2", info["summary"])
        self.assertEqual(info["archive"], f"lantern-crossing-{self.version}-dev-{self.line}.mrpack")
        self.assertIn("development", info["name"])

    def test_migration_branch_keeps_actual_target_in_development_name(self):
        self.replace(
            "release-policy.toml", f'version-branch = "{self.line}"', 'version-branch = "26.3"'
        )
        info = metadata(self.root, branch="26.3")
        self.assertEqual(info["minecraft"], "26.2")
        self.assertIn("26.2.", info["archive"])
        self.assertIn("dev-26.3", info["archive"])
        with self.assertRaisesRegex(ValueError, "migration branch cannot publish"):
            metadata(self.root, "v" + self.version, branch="26.3", channel="release")

    def test_numeric_branch_must_agree_with_policy(self):
        wrong = "26.3" if self.line == "26.2" else "26.2"
        with self.assertRaisesRegex(ValueError, "branch disagrees"):
            metadata(self.root, branch=wrong)

    def test_topic_branch_uses_its_declared_version_line(self):
        self.assertEqual(
            metadata(self.root, branch="fix/safer-defaults")["version-branch"], self.line
        )

    def test_pack_version_cannot_mislabel_target(self):
        self.replace("pack.toml", f'version = "{self.version}"', 'version = "26.3.0.6.0"')
        with self.assertRaisesRegex(ValueError, "version must be"):
            metadata(self.root)

    def test_release_requires_tag_and_owner_acceptance(self):
        with self.assertRaisesRegex(ValueError, "explicit matching tag"):
            metadata(self.root, channel="release")
        with self.assertRaisesRegex(ValueError, "not runtime-qualified|migration branch"):
            metadata(self.root, "v" + self.version, channel="release")

    def test_qualified_26_2_release_retains_existing_names(self):
        self.replace(
            "release-policy.toml", f'version-branch = "{self.line}"', 'version-branch = "26.2"'
        )
        self.qualify_fixture()
        info = metadata(self.root, "v" + self.version, channel="release")
        self.assertEqual(info["archive"], f"lantern-crossing-{self.version}.mrpack")
        self.assertEqual(info["artifact-version"], self.version)
        with self.assertRaisesRegex(ValueError, "tag must agree"):
            metadata(self.root, "v26.2.99.99.99", channel="release")

    def test_acceptance_is_invalidated_by_pack_or_index_changes(self):
        self.replace(
            "release-policy.toml", f'version-branch = "{self.line}"', 'version-branch = "26.2"'
        )
        self.qualify_fixture()
        self.replace("pack.toml", 'fabric = "0.20.1"', 'fabric = "0.20.2"')
        with self.assertRaisesRegex(ValueError, "current pack/index hash"):
            metadata(self.root, "v" + self.version, channel="release")

    def test_acceptance_needs_a_record(self):
        self.replace(
            "release-policy.toml", f'version-branch = "{self.line}"', 'version-branch = "26.2"'
        )
        self.qualify_fixture()
        (self.root / "docs/verification.md").unlink()
        with self.assertRaisesRegex(ValueError, "owner-authored acceptance record"):
            metadata(self.root, "v" + self.version, channel="release")

    def test_migration_inventory_cannot_omit_active_intent(self):
        self.replace("migration.toml", 'project-id = "AANobbMI"', 'project-id = "wrong"')
        with self.assertRaisesRegex(ValueError, "omits active features"):
            metadata(self.root)

    def test_migration_claim_cannot_precede_target_change(self):
        self.replace("migration.toml", 'status = "deferred"', 'status = "static-verified"')
        with self.assertRaisesRegex(ValueError, "cannot claim migrated"):
            validate_migration(self.root, self.line, "26.2")

    def test_migration_target_alone_is_not_release_qualification(self):
        with self.assertRaisesRegex(ValueError, "release is blocked by deferred"):
            validate_migration(self.root, "26.3", "26.3", release=True)

    def test_migration_release_requires_all_runtime_acceptance(self):
        path = self.root / "migration.toml"
        path.write_text(
            path.read_text().replace('status = "deferred"', 'status = "static-verified"')
        )
        with self.assertRaisesRegex(ValueError, "runtime acceptance remains pending"):
            validate_migration(self.root, "26.3", "26.3", release=True)
