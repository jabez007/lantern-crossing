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
        for name in (
            "pack.toml",
            "index.toml",
            "collection.toml",
            "candidates.toml",
            "release-policy.toml",
            "migration.toml",
        ):
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
        features = {pid for pid, project in pack.projects.items() if project["role"] == "feature"}
        self.assertEqual(features, set(pack.evidence["requested"]))
        self.assertFalse(pack.collection.get("excluded"))

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

    def test_same_named_project_cannot_replace_light_overlay_lock(self):
        self.replace("mods/lightoverlay.pw.toml", 'mod-id = "8qVa1XCN"', 'mod-id = "YfOlc91N"')
        self.assertEqual(
            load_toml(self.root / "mods/lightoverlay.pw.toml")["name"], "Light Overlay"
        )
        self.invalid("unexpected active project")

    def test_same_named_project_cannot_replace_requested_identity(self):
        self.replace("collection.toml", 'project-id = "8qVa1XCN"', 'project-id = "YfOlc91N"')
        self.replace("mods/lightoverlay.pw.toml", 'mod-id = "8qVa1XCN"', 'mod-id = "YfOlc91N"')
        self.invalid("all requested features")

    def test_light_overlay_requires_exact_upstream_overlaylib_pin(self):
        def require_another_version(snapshot):
            parent = self.evidence_version(snapshot, "8qVa1XCN")
            for edge in parent["dependencies"] + parent["client_required"]:
                if edge["project_id"] == "M1B8mLoH":
                    edge["version_id"] = "different-version"

        self.edit_evidence(require_another_version)
        self.invalid("exact dependency version mismatch")

    def test_light_overlay_render_stack_has_no_new_declared_conflicts(self):
        pack = load_pack(self.root)
        stack = {"8qVa1XCN", "M1B8mLoH", "YL57xq9U", "AANobbMI"}
        module_ids = {pack.versions[pid]["fabric_descriptor"]["id"] for pid in stack}
        for pid in stack:
            self.assertEqual(pack.mods[pid]["side"], "client")
        for pid in ("8qVa1XCN", "M1B8mLoH"):
            descriptor = pack.versions[pid]["fabric_descriptor"]
            conflicts = set(descriptor.get("breaks", {})) | set(descriptor.get("conflicts", {}))
            self.assertFalse(module_ids & conflicts)

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

    def test_root_runtime_preferences_cannot_be_distributed(self):
        for name in ("options.txt", "servers.dat", "defaultoptions.journal.json"):
            path = self.root / name
            path.write_text("runtime")
            with self.subTest(name=name):
                self.invalid("runtime preferences")
            path.unlink()

    def test_helper_templates_require_the_selected_artifact(self):
        (self.root / "config/defaultoptions").mkdir()
        self.invalid("templates require the pinned helper")

    def test_new_config_requires_refresh(self):
        (self.root / "config/new.cfg").write_text("new")
        self.invalid("index omits")

    def test_required_native_version_range_is_enforced(self):
        def incompatible_loader(snapshot):
            self.evidence_version(snapshot, "AANobbMI")["fabric_descriptor"]["depends"][
                "fabricloader"
            ] = ">=999"

        self.edit_evidence(incompatible_loader)
        self.invalid(r"sodium@.*requires fabricloader '>=999'; installed version: 0.20.1")

    def test_symlink_payload_is_rejected(self):
        (self.root / "config/link.cfg").symlink_to(self.root / "pack.toml")
        self.invalid("symlink")

    def test_release_tag_must_match(self):
        self.assertEqual(
            metadata(self.root, "v26.2.0.3.0")["archive"],
            "lantern-crossing-26.2.0.3.0-dev-26.3.mrpack",
        )
        with self.assertRaisesRegex(ValueError, "tag must agree"):
            metadata(self.root, "v26.2.0.3.1")

    def test_release_checksum(self):
        (self.root / "dist").mkdir()
        name = metadata(self.root)["archive"]
        (self.root / "dist" / name).write_bytes(b"archive")
        result = write_checksum(self.root).read_text()
        self.assertEqual(result, hashlib.sha256(b"archive").hexdigest() + "  " + name + "\n")

    def test_stability_uses_upstream_release_designation(self):
        for name in ("1.0-beta.1", "1.0-SNAPSHOT", "3.0.0-pre3", "1.0-rc.1", "1.0-alpha1"):
            with self.subTest(name=name):
                self.assertTrue(stable({"version_type": "release", "version_number": name}))
        for kind in ("alpha", "beta"):
            self.assertFalse(stable({"version_type": kind, "version_number": "1.0"}))
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
        self.assertEqual(len(requested), len(snapshot["requested"]))
        self.assertTrue(all(r["ready"] for r in requested))

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
            "name": metadata(self.root)["name"],
            "versionId": metadata(self.root)["artifact-version"],
            "summary": metadata(self.root)["summary"],
            "dependencies": {"minecraft": "26.2", "fabric-loader": "0.20.1"},
            "files": files,
        }
        return manifest, {"overrides/" + n: data for n, data in pack.overrides.items()}

    def write_archive(self, manifest, overrides, extra=None):
        path = self.root / metadata(self.root)["archive"]
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("modrinth.index.json", json.dumps(manifest))
            for name, data in overrides.items():
                archive.writestr(name, data)
            if extra:
                archive.writestr(*extra)
        return path

    def test_complete_archive(self):
        validate(self.write_archive(*self.archive_data()), self.root)

    def test_archive_cannot_hide_its_development_identity(self):
        manifest, overrides = self.archive_data()
        manifest["versionId"] = load_toml(self.root / "pack.toml")["version"]
        with self.assertRaisesRegex(ValueError, "version/channel mismatch"):
            validate(self.write_archive(manifest, overrides), self.root)

    def test_archive_filename_must_match_version_line_and_channel(self):
        path = self.write_archive(*self.archive_data())
        wrong = path.with_name("lantern-crossing-26.3.0.1.0.mrpack")
        path.rename(wrong)
        with self.assertRaisesRegex(ValueError, "filename/branch/channel mismatch"):
            validate(wrong, self.root)

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

    def test_bundled_prerelease_is_allowed_in_release_parent(self):
        path = self.root / "docs/upstream-metadata.json"
        snapshot = json.loads(path.read_text())
        version = next(
            v for v in snapshot["projects"]["AANobbMI"]["versions"] if v["id"] == "xJZxADzI"
        )
        version["fabric_descriptor"]["bundled"][0]["version"] = "3.0.0-pre3"
        path.write_text(json.dumps(snapshot))
        load_pack(self.root)

    def edit_evidence(self, change):
        path = self.root / "docs/upstream-metadata.json"
        snapshot = json.loads(path.read_text())
        change(snapshot)
        path.write_text(json.dumps(snapshot))

    def evidence_version(self, snapshot, project_id):
        return next(
            v for v in snapshot["projects"][project_id]["versions"] if "client_required" in v
        )

    def prerelease_dependency(self, snapshot, audited=True):
        dependency = self.evidence_version(snapshot, "1eAoo2KR")
        dependency["version_type"] = "beta"
        dependency["version_number"] = "3.0.0-pre3"
        parent = self.evidence_version(snapshot, "w7ThoJFB")
        edge = next(d for d in parent["client_required"] if d["project_id"] == "1eAoo2KR")
        if audited:
            edge["audited_version"] = dependency["id"]
            edge["evidence"] = "https://api.modrinth.com/v2/version/" + parent["id"]
            edge["upstream_version"] = dependency["version_number"]
            edge["audit_source"] = "https://example.org/upstream/release/build.properties"
        return parent, dependency

    def test_official_exact_audited_prerelease_dependency_is_allowed(self):
        self.edit_evidence(self.prerelease_dependency)
        load_pack(self.root)

    def test_exact_upstream_version_dependency_is_allowed(self):
        def exact_requirement(snapshot):
            parent, dependency = self.prerelease_dependency(snapshot, audited=False)
            for edge in parent["dependencies"] + parent["client_required"]:
                if edge["project_id"] == "1eAoo2KR":
                    edge["version_id"] = dependency["id"]

        self.edit_evidence(exact_requirement)
        load_pack(self.root)

    def test_independently_selected_feature_must_be_a_release(self):
        for kind in ("alpha", "beta"):
            with self.subTest(kind=kind):
                self.edit_evidence(
                    lambda s: self.evidence_version(s, "AANobbMI").update(version_type=kind)
                )
                self.invalid("selected.*release-designated")

    def test_selected_platform_library_must_be_a_release(self):
        self.edit_evidence(
            lambda s: self.evidence_version(s, "P7dR8mSH").update(version_type="beta")
        )
        self.invalid("selected.*release-designated")

    def test_prerelease_dependency_requires_exact_audited_pin(self):
        self.edit_evidence(lambda s: self.prerelease_dependency(s, audited=False))
        self.invalid("prerelease dependency.*upstream.*pin")

    def test_prerelease_dependency_cannot_be_independently_substituted(self):
        def substitute(snapshot):
            parent, _ = self.prerelease_dependency(snapshot)
            edge = next(d for d in parent["client_required"] if d["project_id"] == "1eAoo2KR")
            edge["audited_version"] = "different-version"

        self.edit_evidence(substitute)
        self.invalid("prerelease dependency.*upstream.*pin")

    def test_prerelease_pin_must_match_upstream_version_declaration(self):
        def mismatched_declaration(snapshot):
            parent, _ = self.prerelease_dependency(snapshot)
            edge = next(d for d in parent["client_required"] if d["project_id"] == "1eAoo2KR")
            edge["upstream_version"] = "1.0"

        self.edit_evidence(mismatched_declaration)
        self.invalid("prerelease dependency.*upstream.*pin")

    def test_manually_added_prerelease_edge_is_not_upstream_provenance(self):
        def remove_upstream_declaration(snapshot):
            parent, _ = self.prerelease_dependency(snapshot)
            parent["dependencies"] = [
                d for d in parent["dependencies"] if d["project_id"] != "1eAoo2KR"
            ]
            del parent["fabric_descriptor"]["depends"]["yet_another_config_lib_v3"]

        self.edit_evidence(remove_upstream_declaration)
        self.invalid("prerelease dependency.*upstream.*pin")

    def test_server_required_dependency_is_rejected(self):
        self.edit_evidence(lambda s: s["projects"]["1eAoo2KR"].update(server_side="required"))
        self.invalid("server requirement")

    def test_server_only_bundled_module_is_still_rejected(self):
        def server_bundle(snapshot):
            version = self.evidence_version(snapshot, "AANobbMI")
            version["fabric_descriptor"]["bundled"][0]["environment"] = "server"

        self.edit_evidence(server_bundle)
        self.invalid("server-only Fabric module")

    def test_client_tweaks_overlap_switches_are_pinned_off(self):
        config = load_toml(self.root / "config/clienttweaks-common.toml")
        self.assertIs(config["ui"]["alwaysPrioritizeExperienceBar"], False)
        self.assertIs(config["mining"]["doNotUseLastMending"], False)

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
