"""Validate the chosen defaults contract; these tests do not run Minecraft."""

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pack_model import ROOT, check_defaults_manager, load_toml


class DefaultsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        if (ROOT / "configureddefaults").exists():
            shutil.copytree(ROOT / "configureddefaults", self.root / "configureddefaults")
        self.managers = {"SISoSFPP": {}}
        # The 26.3 bootstrap has not adopted the maintained line's helper yet.
        (self.root / "configureddefaults/config").mkdir(parents=True, exist_ok=True)

    def test_competing_managers_are_rejected_by_project_identity(self):
        for pid in ("jlNms3Jp", "WEg59z5b", "WwbubTsV"):
            with (
                self.subTest(project=pid),
                self.assertRaisesRegex(ValueError, "competing defaults managers"),
            ):
                check_defaults_manager(self.root, self.managers | {pid: {}})

    def test_obsolete_manager_template_trees_are_rejected(self):
        for name in ("config/defaultoptions", "config/modpack_defaults", "config/yosbr"):
            path = self.root / name
            path.mkdir()
            with (
                self.subTest(path=name),
                self.assertRaisesRegex(ValueError, "unselected defaults layout"),
            ):
                check_defaults_manager(self.root, self.managers)
            path.rmdir()

    def test_selected_helper_requires_its_template_directory(self):
        shutil.rmtree(self.root / "configureddefaults")
        with self.assertRaisesRegex(ValueError, "requires its templates"):
            check_defaults_manager(self.root, self.managers)

    def test_bootstrap_without_manager_retains_its_existing_contract(self):
        shutil.rmtree(self.root / "configureddefaults")
        check_defaults_manager(self.root, {})

    def test_resource_pack_replacement_config_is_rejected(self):
        for name in ("defaultoptions-common.toml", "DefaultOptions-common.toml"):
            path = self.root / "configureddefaults/config" / name
            path.write_text('defaultResourcePacks = ["continuity:default"]\n')
            with (
                self.subTest(name=name),
                self.assertRaisesRegex(ValueError, "resource-pack replacement"),
            ):
                check_defaults_manager(self.root, self.managers)
            path.unlink()

    def test_extra_cannot_seed_root_player_preferences(self):
        (self.root / "configureddefaults/servers.dat").write_text("resourcePacks:[]\n")
        with self.assertRaisesRegex(ValueError, "unsupported Configured Defaults template"):
            check_defaults_manager(self.root, self.managers)

    def test_unsupported_handler_template_is_rejected(self):
        (self.root / "configureddefaults/unknown.txt").write_text("unused")
        with self.assertRaisesRegex(ValueError, "unsupported Configured Defaults template"):
            check_defaults_manager(self.root, self.managers)

    def test_forced_update_and_reset_flags_are_rejected(self):
        for name in ("CONFIG_MANAGER_UPDATE_FLAG", "CONFIG_MANAGER_RESET_FLAG"):
            path = self.root / "config" / name
            path.write_text("")
            with (
                self.subTest(flag=name),
                self.assertRaisesRegex(ValueError, "forced defaults reset/update"),
            ):
                check_defaults_manager(self.root, self.managers)
            path.unlink()

    def test_recorded_file_audit_matches_locked_artifact_and_templates(self):
        lock_path = ROOT / "mods/configured-defaults.pw.toml"
        if not lock_path.exists():
            self.skipTest("26.3 bootstrap tracks the helper as deferred, not installed")
        evidence = json.loads((ROOT / "tests/fixtures/configured-defaults-files.json").read_text())
        lock = load_toml(lock_path)
        self.assertEqual(evidence["artifact-sha512"], lock["download"]["hash"])
        self.assertEqual(evidence["version-id"], lock["update"]["modrinth"]["version"])
        self.assertEqual(
            evidence["adapter-sha256"],
            hashlib.sha256(
                (ROOT / "tests/fixtures/ConfiguredDefaultsFilesOracle.java").read_bytes()
            ).hexdigest(),
        )
        for name, digest in evidence["templates-sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(len(evidence["observations"]), 7)
        observations = {entry["scenario"]: entry for entry in evidence["observations"]}
        self.assertEqual(
            observations["fresh"]["after"]["options.txt"],
            (ROOT / "configureddefaults/options.txt").read_text(),
        )
        for name, entry in observations.items():
            if name not in {"fresh", "launcher-created-options", "pack-update"}:
                self.assertEqual(
                    entry["before"]["options.txt"], entry["after"]["options.txt"], name
                )
        launcher = observations["launcher-created-options"]["after"]["options.txt"]
        self.assertIn("fullscreen:true", launcher)
        self.assertIn("key_key.light-overlay.toggle:key.keyboard.f7", launcher)
        self.assertIn("continuity:default", launcher)
        update = observations["pack-update"]
        self.assertIn("viewBobbing:false", update["after"]["options.txt"])
        self.assertEqual(update["after"]["config/new-fixture.cfg"], "new-default=true\n")
        self.assertEqual(
            update["before"]["config/iris.properties"], update["after"]["config/iris.properties"]
        )
        adoption = observations["previous-manager-and-explicit-adoption"]
        self.assertEqual(
            adoption["after"]["config/iris.properties"],
            (ROOT / "configureddefaults/config/iris.properties").read_text(),
        )
        self.assertEqual(
            adoption["before"]["defaultoptions.journal.json"],
            adoption["after"]["defaultoptions.journal.json"],
        )
        self.assertEqual(
            evidence["scope"],
            "Unmodified upstream CopyDefaultsHandler only; logging/constants stubbed; no Fabric, Minecraft or launcher executed.",
        )
