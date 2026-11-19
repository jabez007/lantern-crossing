"""Shader references preserve mod policy, download integrity, licensing and preferences."""

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_target_readiness import compatible_versions
from pack_model import load_pack
from validate_mrpack import validate
import test_pack as fixtures


class ShaderTests(unittest.TestCase):
    # Reuse the existing disposable repository/archive fixtures without inheriting tests.
    setUp = fixtures.PackTests.setUp
    replace = fixtures.PackTests.replace
    invalid = fixtures.PackTests.invalid
    archive_data = fixtures.PackTests.archive_data
    write_archive = fixtures.PackTests.write_archive

    def evidence_change(self, change, message):
        path = self.root / "docs/upstream-metadata.json"
        original = path.read_text()
        data = json.loads(original)
        change(data["shader_projects"]["HVnmMxH1"])
        path.write_text(json.dumps(data))
        try:
            self.invalid(message)
        finally:
            path.write_text(original)

    def test_exact_shader_choices_are_separate_from_mods(self):
        pack = load_pack(self.root)
        self.assertEqual(set(pack.shaders), {"HVnmMxH1", "izsIPI7a"})
        self.assertTrue(pack.shaders.keys().isdisjoint(pack.mods))
        self.assertEqual(len(pack.mods), 52)
        self.assertEqual(pack.shader_versions["HVnmMxH1"]["id"], "RKfUB9VC")
        self.assertEqual(pack.shader_versions["izsIPI7a"]["id"], "t4YRxQug")
        for version in pack.shader_versions.values():
            self.assertNotIn("fabric_descriptor", version)
            self.assertEqual(version["distribution_audit"]["mode"], "modrinth-reference")

    def test_missing_or_duplicate_shader_lock_is_rejected(self):
        path = self.root / "shaderpacks/complementary-reimagined.pw.toml"
        path.rename(path.with_suffix(".removed"))
        self.invalid("selected shader absent")
        path.with_suffix(".removed").rename(path)
        (path.parent / "other.pw.toml").write_bytes(path.read_bytes())
        self.invalid("identity mismatch")

    def test_same_named_unapproved_project_cannot_replace_shader(self):
        self.replace(
            "shaderpacks/complementary-reimagined.pw.toml",
            'mod-id = "HVnmMxH1"',
            'mod-id = "unrelated"',
        )
        self.invalid("unexpected shader project")

    def test_shader_identity_cannot_duplicate_a_mod(self):
        self.replace("collection.toml", 'project-id = "HVnmMxH1"', 'project-id = "AANobbMI"')
        self.invalid("duplicate project ID/slug")

    def test_shader_side_and_pin_are_required(self):
        path = self.root / "shaderpacks/complementary-reimagined.pw.toml"
        original = path.read_text()
        for before, after in [('side = "client"', 'side = "both"'), ("pin = true", "pin = false")]:
            with self.subTest(after=after):
                path.write_text(original.replace(before, after))
                self.invalid("pinned and client-only")
        path.write_text(original)

    def test_wrong_shader_hash_or_download_origin_is_rejected(self):
        path = self.root / "shaderpacks/complementary-reimagined.pw.toml"
        original = path.read_text()
        for changed in (
            original.replace('hash = "edced', 'hash = "00000'),
            original.replace("https://cdn.modrinth.com/", "https://example.com/"),
        ):
            with self.subTest(changed=changed[:40]):
                path.write_text(changed)
                self.invalid("hash/filename|download URL")
        path.write_text(original)

    def test_release_target_loader_and_environment_are_enforced(self):
        for field, value in (
            ("version_type", "beta"),
            ("game_versions", ["26.3"]),
            ("loaders", ["optifine"]),
        ):
            with self.subTest(field=field):
                self.evidence_change(
                    lambda p: p["versions"][0].__setitem__(field, value), "release-designated"
                )
        for field, value in (
            ("server_side", "required"),
            ("client_side", "unsupported"),
            ("project_type", "mod"),
        ):
            with self.subTest(field=field):
                self.evidence_change(lambda p: p.__setitem__(field, value), "client-only shader")

    def test_shader_cannot_have_fake_fabric_metadata_or_unreviewed_dependencies(self):
        self.evidence_change(
            lambda p: p["versions"][0].__setitem__("fabric_descriptor", {"id": "fabricated"}),
            "fabricated Fabric",
        )
        for kind in ("required", "incompatible"):
            with self.subTest(kind=kind):
                self.evidence_change(
                    lambda p: p["versions"][0].__setitem__(
                        "dependencies", [{"project_id": "unreviewed", "dependency_type": kind}]
                    ),
                    "explicit closure review",
                )

    def test_mod_declared_shader_incompatibility_is_rejected(self):
        path = self.root / "docs/upstream-metadata.json"
        data = json.loads(path.read_text())
        data["projects"]["AANobbMI"]["versions"][0]["dependencies"].append(
            {"project_id": "HVnmMxH1", "dependency_type": "incompatible"}
        )
        path.write_text(json.dumps(data))
        self.invalid("incompatible upstream projects selected together")

    def test_distribution_review_is_bound_to_the_exact_artifact_and_renderer(self):
        for field, value in (
            ("version_id", "changed"),
            ("artifact", {"filename": "other.zip", "sha512": "0" * 128}),
            ("mode", "direct-upload"),
            ("license_id", "unreviewed"),
            ("renderer", {"project_id": "YL57xq9U", "version_id": "new-iris"}),
        ):
            with self.subTest(field=field):
                self.evidence_change(
                    lambda p: p["versions"][0]["distribution_audit"].__setitem__(field, value),
                    "needs re-evaluation",
                )
        self.evidence_change(
            lambda p: p["versions"][0]["distribution_audit"].__setitem__("license_sha256", ""),
            "license fingerprint",
        )

    def test_automatic_shader_selection_or_enablement_is_rejected(self):
        path = self.root / "configureddefaults/config/iris.properties"
        original = path.read_text()
        for changed in (
            original.replace("enableShaders=false", "enableShaders=true"),
            original + "shaderPack=ComplementaryReimagined_r5.10.zip\n",
        ):
            with self.subTest(changed=changed):
                path.write_text(changed)
                self.invalid("only seed enableShaders=false")
        path.write_text(original)

    def test_direct_zip_and_player_presets_cannot_be_distributed(self):
        for relative in (
            "shaderpacks/unapproved.zip",
            "configureddefaults/config/copied-shader.zip",
            "configureddefaults/config/MakeUp-UltraFast-9.6.zip.txt",
        ):
            path = self.root / relative
            with self.subTest(relative=relative):
                path.write_bytes(b"isolated packaging fixture")
                self.invalid("local JAR/ZIP|unexpected.*payload|unexpected config artifact")
                path.unlink()

    def test_shader_cannot_be_installed_as_a_mod(self):
        path = self.root / "shaderpacks/complementary-reimagined.pw.toml"
        path.rename(self.root / "mods" / path.name)
        self.invalid("unexpected active project")

    def test_export_requires_exact_shader_paths_and_complete_set(self):
        manifest, overrides = self.archive_data()
        entries = [f for f in manifest["files"] if f["path"].startswith("shaderpacks/")]
        self.assertEqual(len(entries), 2)
        self.assertFalse(any("shaderpacks" in name for name in overrides))
        validate(self.write_archive(manifest, overrides), self.root)
        for remove in (True, False):
            changed = copy.deepcopy(manifest)
            target = next(f for f in changed["files"] if f["path"] == entries[0]["path"])
            if remove:
                changed["files"].remove(target)
            else:
                target["path"] = target["path"].replace("shaderpacks/", "mods/")
            with (
                self.subTest(remove=remove),
                self.assertRaisesRegex(ValueError, "missing baseline|unexpected/duplicate"),
            ):
                validate(self.write_archive(changed, overrides), self.root)

    def test_export_checks_shader_environment_hash_and_no_direct_override(self):
        manifest, overrides = self.archive_data()
        for field, value in (
            ("env", {"client": "required", "server": "required"}),
            ("hashes", {"sha512": "0" * 128}),
            ("downloads", ["https://example.com/shader.zip"]),
        ):
            changed = copy.deepcopy(manifest)
            entry = next(f for f in changed["files"] if f["path"].startswith("shaderpacks/"))
            entry[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(self.write_archive(changed, overrides), self.root)
        with self.assertRaisesRegex(ValueError, "archive overrides"):
            validate(
                self.write_archive(
                    manifest, overrides, ("overrides/shaderpacks/copied.zip", b"fixture")
                ),
                self.root,
            )

    def test_readiness_distinguishes_iris_from_fabric(self):
        versions = load_pack(self.root).shader_versions.values()
        self.assertEqual(len(compatible_versions(versions, "26.2", loader="iris")), 2)
        self.assertFalse(compatible_versions(versions, "26.2"))
