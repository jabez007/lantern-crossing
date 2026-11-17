"""Exercise the repository contract with valid and deliberately damaged packs."""

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_target_readiness import compatible_versions, discover
from normalize_mrpack import normalize
from pack_model import ROOT, load_pack, load_toml, stable
from release_metadata import metadata, write_checksum
from validate_mrpack import validate


class PackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("pack.toml", "index.toml", "collection.toml", "candidates.toml"):
            shutil.copyfile(ROOT / name, self.root / name)
        for name in ("mods", "config"):
            shutil.copytree(ROOT / name, self.root / name)
        (self.root / "docs").mkdir()
        shutil.copyfile(
            ROOT / "docs/upstream-metadata.json", self.root / "docs/upstream-metadata.json"
        )

    def replace(self, name, before, after):
        path = self.root / name
        text = path.read_text()
        self.assertIn(before, text)
        path.write_text(text.replace(before, after, 1))

    def invalid(self, message):
        with self.assertRaisesRegex((ValueError, KeyError), message):
            load_pack(self.root)

    def test_repository_contract(self):
        pack = load_pack(self.root)
        self.assertEqual(len(pack.evidence["requested"]), 30)
        self.assertEqual(len(pack.collection["excluded"]), 5)
        self.assertEqual(len(pack.mods), 31)

    def test_side_is_always_explicitly_client(self):
        for side in ('"both"', '"server"', '""'):
            with self.subTest(side=side):
                path = self.root / "mods/sodium.pw.toml"
                original = path.read_text()
                path.write_text(original.replace('side = "client"', "side = " + side))
                self.invalid("side must be client")
                path.write_text(original)

    def test_missing_feature_and_dependency(self):
        for slug in ("sodium", "libipn"):
            with self.subTest(slug=slug):
                path = self.root / "mods" / (slug + ".pw.toml")
                original = path.read_bytes()
                path.unlink()
                self.invalid("absent")
                path.write_bytes(original)

    def test_unexpected_lock_project(self):
        self.replace("mods/sodium.pw.toml", 'mod-id = "AANobbMI"', 'mod-id = "unknown1"')
        self.invalid("unexpected active")

    def test_duplicate_project_and_slug(self):
        collection = (self.root / "collection.toml").read_text()
        first = collection.split("[[selected]]")[1].split("[[selected]]")[0]
        with (self.root / "collection.toml").open("a") as handle:
            handle.write("\n[[selected]]" + first)
        self.invalid("duplicate")

    def test_target_cannot_change_in_both_manifests(self):
        for name in ("pack.toml", "collection.toml"):
            self.replace(name, 'minecraft = "26.2"', 'minecraft = "26.3"')
        self.invalid("exactly Minecraft 26.2")

    def test_loader_cannot_change(self):
        self.replace("pack.toml", 'fabric = "0.20.1"', 'quilt = "0.20.1"')
        self.invalid("Fabric")

    def test_candidate_cannot_be_active(self):
        self.replace("candidates.toml", "candidate = []", "")
        with (self.root / "candidates.toml").open("a") as handle:
            handle.write(
                '\n[[candidate]]\nproject-id = "AANobbMI"\nslug = "sodium"\ncategory = "performance"\nrationale = "test"\nstatus = "proposed"\nclient-only = "verified"\ntarget-support = "ready"\nblockers = ["review"]\npromotion-criteria = "review"\n'
            )
        self.invalid("staged candidate leaks")

    def test_rejected_projects(self):
        for slug in (
            "appleskin",
            "jade",
            "easy-shulker-boxes",
            "bookshelf-inspector",
            "client-sort",
        ):
            with self.subTest(slug=slug):
                path = self.root / "collection.toml"
                original = path.read_text()
                path.write_text(original.replace('slug = "sodium"', 'slug = "' + slug + '"'))
                self.invalid("rejected project")
                path.write_text(original)

    def test_changed_lock_identity(self):
        self.replace("mods/sodium.pw.toml", 'name = "Sodium"', 'name = "Other"')
        self.invalid("identity mismatch")

    def test_wrong_hash_or_version(self):
        self.replace("mods/sodium.pw.toml", 'version = "xJZxADzI"', 'version = "unknown1"')
        self.invalid("pinned version missing")

    def test_required_by_cannot_hide_missing_edge(self):
        collection = load_toml(self.root / "collection.toml")
        dependency = collection["resolved-dependency"][0]
        parents = json.dumps(dependency["required-by"])
        self.replace("collection.toml", "required-by = " + parents, 'required-by = ["unknown1"]')
        self.invalid("dependency parents disagree")

    def test_jars_are_rejected_even_if_gitignored(self):
        (self.root / "accidental.jar").write_bytes(b"not a mod")
        self.invalid("local JAR")

    def test_stale_pack_index(self):
        with (self.root / "index.toml").open("a") as handle:
            handle.write("\n# stale\n")
        self.invalid("stale pack index hash")

    def test_changed_config_requires_refresh(self):
        with (self.root / "config/MouseTweaks.cfg").open("a") as handle:
            handle.write("\n# changed\n")
        self.invalid("stale index entry")

    def test_new_config_requires_refresh(self):
        (self.root / "config/new.cfg").write_text("new")
        self.invalid("index omits")

    def test_symlink_payload_is_rejected(self):
        (self.root / "config/link.cfg").symlink_to(self.root / "pack.toml")
        self.invalid("symlink")

    def test_release_tag_must_match(self):
        self.assertEqual(
            metadata(self.root, "v26.2.0.1.0")["archive"], "lantern-crossing-26.2.0.1.0.mrpack"
        )
        with self.assertRaisesRegex(ValueError, "tag must agree"):
            metadata(self.root, "v26.2.0.1.1")

    def test_release_checksum(self):
        (self.root / "dist").mkdir()
        name = metadata(self.root)["archive"]
        (self.root / "dist" / name).write_bytes(b"archive")
        result = write_checksum(self.root).read_text()
        self.assertEqual(result, hashlib.sha256(b"archive").hexdigest() + "  " + name + "\n")

    def test_stable_label_does_not_override_prerelease_name(self):
        for name in ("1.0-beta.1", "1.0-SNAPSHOT", "3.0.0-pre3", "1.0-rc.1", "1.0-alpha1"):
            with self.subTest(name=name):
                self.assertFalse(stable({"version_type": "release", "version_number": name}))
        self.assertFalse(stable({"version_type": "beta", "version_number": "1.0"}))
        self.assertTrue(stable({"version_type": "release", "version_number": "fabric-26.2-2.3.8"}))

    def test_readiness_filters_target_loader_and_stability(self):
        base = {
            "version_type": "release",
            "version_number": "1.0",
            "loaders": ["fabric"],
            "game_versions": ["26.2"],
        }
        variants = [
            base,
            base | {"loaders": ["neoforge"]},
            base | {"game_versions": ["26.1"]},
            base | {"version_type": "beta"},
        ]
        self.assertEqual(compatible_versions(variants, "26.2"), [base])

    def test_offline_readiness_never_fetches(self):
        snapshot = json.loads((self.root / "docs/upstream-metadata.json").read_text())
        with patch(
            "check_target_readiness.fetch_versions", side_effect=AssertionError("network forbidden")
        ):
            active = discover(self.root, "26.2", "active", snapshot)
            requested = discover(self.root, "26.2", "requested", snapshot)
        self.assertTrue(all(r["ready"] for r in active))
        self.assertEqual(len(requested), 30)
        self.assertEqual([r["name"] for r in requested if not r["ready"]], ["Light Overlay"])

    def archive_data(self):
        pack = load_pack(self.root)
        files = []
        for pid, lock in pack.mods.items():
            upstream = next(
                f for f in pack.versions[pid]["files"] if f["filename"] == lock["filename"]
            )
            files.append(
                {
                    "path": "mods/" + lock["filename"],
                    "hashes": upstream["hashes"],
                    "env": {"client": "required", "server": "unsupported"},
                    "downloads": [lock["download"]["url"]],
                    "fileSize": upstream["size"],
                }
            )
        manifest = {
            "formatVersion": 1,
            "game": "minecraft",
            "name": pack.metadata["name"],
            "versionId": pack.metadata["version"],
            "dependencies": {"minecraft": "26.2", "fabric-loader": "0.20.1"},
            "files": files,
        }
        return manifest, {"overrides/" + n: data for n, data in pack.overrides.items()}

    def write_archive(self, manifest, overrides, extra=None):
        path = self.root / "test.mrpack"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("modrinth.index.json", json.dumps(manifest))
            for name, data in overrides.items():
                archive.writestr(name, data)
            if extra:
                archive.writestr(*extra)
        return path

    def test_complete_archive(self):
        validate(self.write_archive(*self.archive_data()), self.root)

    def test_archive_missing_feature_or_dependency(self):
        manifest, overrides = self.archive_data()
        for needle in ("sodium-", "libIPN-"):
            changed = copy.deepcopy(manifest)
            changed["files"] = [f for f in manifest["files"] if needle not in f["path"]]
            with (
                self.subTest(needle=needle),
                self.assertRaisesRegex(ValueError, "missing baseline"),
            ):
                validate(self.write_archive(changed, overrides), self.root)

    def test_archive_rejects_wrong_environment_url_hash_size(self):
        manifest, overrides = self.archive_data()
        changes = {
            "env": {"client": "required", "server": "required"},
            "downloads": ["https://example.com/mod.jar"],
            "hashes": {"sha512": "0" * 128},
            "fileSize": 0,
        }
        for key, value in changes.items():
            changed = copy.deepcopy(manifest)
            changed["files"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(self.write_archive(changed, overrides), self.root)

    def test_archive_rejects_target_and_loader_changes(self):
        manifest, overrides = self.archive_data()
        for dependencies in (
            {"minecraft": "26.3", "fabric-loader": "0.20.1"},
            {"minecraft": "26.2", "quilt-loader": "0.20.1"},
        ):
            with (
                self.subTest(dependencies=dependencies),
                self.assertRaisesRegex(ValueError, "exact Minecraft"),
            ):
                validate(
                    self.write_archive(manifest | {"dependencies": dependencies}, overrides),
                    self.root,
                )

    def test_archive_rejects_extra_staged_server_or_jar_payload(self):
        manifest, overrides = self.archive_data()
        for name in (
            "overrides/staged/candidate.pw.toml",
            "overrides/server.properties",
            "server-overrides/config/a.cfg",
            "overrides/mods/a.jar",
            "../escape",
            "overrides/config/link",
        ):
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate(self.write_archive(manifest, overrides, (name, b"bad")), self.root)

    def test_archive_requires_exact_config_bytes(self):
        manifest, overrides = self.archive_data()
        for changed in ({}, {key: b"changed" for key in overrides}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "overrides"):
                validate(self.write_archive(manifest, changed), self.root)

    def test_archive_rejects_duplicate_entries(self):
        manifest, overrides = self.archive_data()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            path = self.write_archive(manifest, overrides, ("modrinth.index.json", b"{}"))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate(path, self.root)

    def test_normalization_is_reproducible_and_idempotent(self):
        manifest, overrides = self.archive_data()
        path = self.write_archive(manifest, overrides)
        normalize(path)
        first = path.read_bytes()
        # Reorder records, JSON keys, and ZIP entries and vary filesystem times.
        manifest["files"].reverse()
        path = self.write_archive(dict(reversed(list(manifest.items()))), overrides)
        normalize(path)
        self.assertEqual(first, path.read_bytes())
        normalize(path)
        self.assertEqual(first, path.read_bytes())
        validate(path, self.root)

    def test_bundled_prerelease_cannot_hide_in_stable_parent(self):
        path = self.root / "docs/upstream-metadata.json"
        snapshot = json.loads(path.read_text())
        version = next(
            v for v in snapshot["projects"]["AANobbMI"]["versions"] if v["id"] == "xJZxADzI"
        )
        version["fabric_descriptor"]["bundled"][0]["version"] = "1.0-SNAPSHOT"
        path.write_text(json.dumps(snapshot))
        self.invalid("bundled prerelease")

    def test_native_dependency_omission_is_detected(self):
        path = self.root / "docs/upstream-metadata.json"
        snapshot = json.loads(path.read_text())
        version = next(
            v for v in snapshot["projects"]["QwxR6Gcd"]["versions"] if "client_required" in v
        )
        version["fabric_descriptor"]["depends"]["missing_library"] = "*"
        path.write_text(json.dumps(snapshot))
        self.invalid("Fabric module dependencies missing")

    def test_server_config_cannot_be_shipped(self):
        (self.root / "config/server.properties").write_text("server-port=25565")
        self.invalid("server-only config")


if __name__ == "__main__":
    unittest.main()
