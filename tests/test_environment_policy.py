"""Exact metadata audits cannot override artifact, native or dependency policy."""

import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_pack import main
from pack_model import ROOT, load_pack, load_toml


class EnvironmentPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        names = [
            "pack.toml",
            "index.toml",
            "collection.toml",
            "candidates.toml",
            "migration.toml",
            "release-policy.toml",
            "docs/upstream-metadata.json",
        ]
        names.extend(entry["file"] for entry in load_toml(ROOT / "index.toml")["files"])
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.snapshot = self.root / "docs/upstream-metadata.json"
        self.data = json.loads(self.snapshot.read_text())

    def save(self):
        self.snapshot.write_text(json.dumps(self.data))

    def authorize_fixture(self, pid="1eAoo2KR"):
        # Synthetic review of an existing library proves the parser is project-independent.
        project = self.data["projects"][pid]
        project["server_side"] = "required"
        version = project["versions"][0]
        artifact = next(f for f in version["files"] if f["primary"])
        parents = []
        for parent_id, upstream in self.data["projects"].items():
            parent = upstream["versions"][0]
            if any(d["project_id"] == pid for d in parent["client_required"]):
                file = next(f for f in parent["files"] if f["primary"])
                parents.append(
                    {
                        "project_id": parent_id,
                        "version_id": parent["id"],
                        "artifact": {
                            "filename": file["filename"],
                            "sha512": file["hashes"]["sha512"],
                        },
                    }
                )
        audit = {
            "scope": "modrinth-server-side",
            "project_id": pid,
            "version_id": version["id"],
            "minecraft": "26.2",
            "loader": "fabric",
            "artifact": {"filename": artifact["filename"], "sha512": artifact["hashes"]["sha512"]},
            "descriptor_sha256": hashlib.sha256(
                json.dumps(
                    version["fabric_descriptor"], sort_keys=True, separators=(",", ":")
                ).encode()
            ).hexdigest(),
            "observed": {"client_side": project["client_side"], "server_side": "required"},
            "required_by": parents,
            "reason": "Synthetic evidence used only in offline tests.",
            "evidence": ["https://example.invalid/immutable-artifact-audit"],
            "review": "docs/mod-audit.md#synthetic-test-only",
        }
        self.data.setdefault("environment_exceptions", []).append(audit)
        self.save()
        return audit

    def invalid(self, message):
        self.save()
        with self.assertRaisesRegex(ValueError, message):
            load_pack(self.root)

    def test_reviewed_exact_library_can_override_project_server_label(self):
        self.authorize_fixture()
        pack = load_pack(self.root)
        self.assertEqual(pack.evidence["projects"]["1eAoo2KR"]["server_side"], "required")
        self.assertEqual(pack.mods["1eAoo2KR"]["side"], "client")

    def test_removing_audit_reproduces_original_metadata_rejection(self):
        self.authorize_fixture()
        self.data["environment_exceptions"] = []
        self.invalid("mandatory server requirement")

    def test_audit_is_bound_to_version_file_hash_descriptor_and_target(self):
        audit = self.authorize_fixture()
        for key in ("version_id", "artifact", "descriptor_sha256", "minecraft", "loader", "scope"):
            original = audit[key]
            audit[key] = "changed"
            with self.subTest(field=key):
                self.invalid("environment audit.*re-evaluation")
            audit[key] = original

    def test_metadata_correction_requires_exception_removal(self):
        self.authorize_fixture()
        self.data["projects"]["1eAoo2KR"]["server_side"] = "optional"
        self.invalid("environment audit.*re-evaluation")

    def test_exception_does_not_authorize_unsupported_client(self):
        audit = self.authorize_fixture()
        self.data["projects"]["1eAoo2KR"]["client_side"] = "unsupported"
        audit["observed"]["client_side"] = "unsupported"
        self.invalid("unsupported client")

    def test_exception_cannot_authorize_intentional_feature(self):
        self.authorize_fixture("AANobbMI")
        self.invalid("environment audit.*resolved dependency")

    def test_exception_cannot_authorize_native_server_module(self):
        self.authorize_fixture()
        self.data["projects"]["1eAoo2KR"]["versions"][0]["fabric_descriptor"]["environment"] = (
            "server"
        )
        self.invalid("server-only Fabric module")

    def test_exception_cannot_authorize_bundled_server_module(self):
        self.authorize_fixture()
        descriptor = self.data["projects"]["1eAoo2KR"]["versions"][0]["fabric_descriptor"]
        descriptor["bundled"][0]["environment"] = "server"
        self.invalid("server-only Fabric module")

    def test_exception_cannot_change_install_side(self):
        self.authorize_fixture()
        path = self.root / "mods/yacl.pw.toml"
        path.write_text(path.read_text().replace('side = "client"', 'side = "both"'))
        self.invalid("side must be client")

    def test_unrelated_server_required_dependency_remains_rejected(self):
        self.authorize_fixture()
        self.data["projects"]["9s6osm5g"]["server_side"] = "required"
        self.invalid("mandatory server requirement")

    def test_audit_cannot_bypass_required_native_version_constraints(self):
        self.authorize_fixture()
        self.data["projects"]["AANobbMI"]["versions"][0]["fabric_descriptor"]["version"] = "0.8.0"
        self.invalid("requires sodium.*installed version: 0.8.0")

    def test_audit_cannot_bypass_download_integrity(self):
        self.authorize_fixture()
        path = self.root / "mods/yacl.pw.toml"
        original = load_toml(path)["download"]["hash"]
        path.write_text(path.read_text().replace(original, "0" * 128))
        self.invalid("pin hash/filename disagrees")

    def test_parent_context_cannot_change_silently(self):
        audit = self.authorize_fixture()
        for key in ("version_id", "artifact"):
            original = audit["required_by"][0][key]
            audit["required_by"][0][key] = "changed"
            with self.subTest(field=key):
                self.invalid("environment audit.*parent.*re-evaluation")
            audit["required_by"][0][key] = original
        audit["required_by"] = []
        self.invalid("environment audit.*parent.*re-evaluation")

    def test_synthetic_client_edge_cannot_replace_official_parent_requirement(self):
        audit = self.authorize_fixture()
        parent = self.data["projects"][audit["required_by"][0]["project_id"]]["versions"][0]
        parent["dependencies"] = [
            d for d in parent["dependencies"] if d["project_id"] != "1eAoo2KR"
        ]
        self.invalid("parent must officially require")

    def test_duplicate_and_orphan_audits_fail(self):
        audit = self.authorize_fixture()
        self.data["environment_exceptions"].append(dict(audit))
        self.invalid("duplicate environment audit")
        self.data["environment_exceptions"].pop()
        self.data["environment_exceptions"].append({"project_id": "missing"})
        self.invalid("orphan environment audit")

    def test_cli_explicitly_reports_environment_audit(self):
        self.authorize_fixture()
        stdout = io.StringIO()
        with (
            patch.object(sys, "argv", ["check_pack.py", "--root", str(self.root)]),
            redirect_stdout(stdout),
        ):
            result = main()
        self.assertEqual(result, 0)
        self.assertIn("AUDIT: environment classification", stdout.getvalue())
        self.assertIn("yacl", stdout.getvalue())
        self.assertIn("server_side=required", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
