"""Offline predicates, verified against Fabric Loader's actual API, plus graph checks."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from fabric_versions import UnsupportedPredicate, satisfies
from native_dependencies import validate_native_dependencies


def record(identifier, version="1.0", **fields):
    bundled = fields.pop("bundled", [])
    return [{"id": identifier, "version": version, **fields}, *bundled]


class FabricVersionTests(unittest.TestCase):
    def test_loader_conformance_vectors(self):
        data = json.loads((Path(__file__).parent / "fixtures/fabric-predicates.json").read_text())
        for case in data["cases"]:
            with self.subTest(case=case):
                self.assertEqual(satisfies(case["version"], case["predicate"]), case["matches"])

    def test_unsupported_is_not_silently_accepted(self):
        for expression in [
            ">nightly",
            "1 || 2",
            ">=1, <2",
            "[1,2)",
            "!=1",
            "1.x.2",
            ">=1.x",
            [],
            ["*", "!=1"],
            [1],
            "=１.２",
        ]:
            with self.subTest(expression=expression), self.assertRaises(UnsupportedPredicate):
                satisfies("1.2", expression)

    def test_builtin_and_alias_versions(self):
        versions = {
            "feature": record(
                "feature",
                depends={
                    "java": ">=25",
                    "minecraft": "~26.2-",
                    "fabricloader": ">=0.20",
                    "alias": "^2",
                },
            ),
            "library": record("library", "2.1.0+build", provides=["alias"]),
        }
        validate_native_dependencies(
            versions, {"java": "25", "minecraft": "26.2", "fabricloader": "0.20.1"}
        )

    def test_installed_but_incompatible_has_actionable_diagnostic(self):
        versions = {
            "feature": record("feature", depends={"library": ">=2"}),
            "library": record("library", "1.5"),
        }
        with self.assertRaisesRegex(
            ValueError, r"feature@1.0 requires library '>=2'; installed version: 1.5"
        ):
            validate_native_dependencies(versions, {})

    def test_missing_required_dependency(self):
        with self.assertRaisesRegex(ValueError, "library.*MISSING"):
            validate_native_dependencies(
                {"feature": record("feature", depends={"library": "*"})}, {}
            )

    def test_optional_dependencies_do_not_become_requirements(self):
        validate_native_dependencies(
            {
                "feature": record(
                    "feature",
                    recommends={"missing": ">2"},
                    suggests={"missing": "*"},
                    conflicts={"missing": "*"},
                )
            },
            {},
        )

    def test_hard_breaks_are_enforced(self):
        versions = {
            "feature": record("feature", breaks={"library": "<2"}),
            "library": record("library", "1.5"),
        }
        with self.assertRaisesRegex(ValueError, "feature@1.0 breaks library"):
            validate_native_dependencies(versions, {})

    def test_bundled_versions_use_newest_compatible_copy(self):
        versions = {
            "feature": record(
                "feature", depends={"library": ">=2"}, bundled=[{"id": "library", "version": "1.5"}]
            ),
            "other": record("other", bundled=[{"id": "library", "version": "2.1"}]),
        }
        validate_native_dependencies(versions, {})

    def test_alternative_bundled_resolution_is_explicitly_unsupported(self):
        versions = {
            "feature": record(
                "feature", depends={"library": "<2"}, bundled=[{"id": "library", "version": "1.5"}]
            ),
            "other": record("other", bundled=[{"id": "library", "version": "2.1"}]),
        }
        with self.assertRaisesRegex(
            UnsupportedPredicate, "bundled alternatives.*Loader resolution"
        ):
            validate_native_dependencies(versions, {})

    def test_bundled_copy_cannot_replace_a_mandatory_root(self):
        versions = {
            "feature": record(
                "feature", depends={"library": ">=2"}, bundled=[{"id": "library", "version": "2.1"}]
            ),
            "library": record("library", "1.5"),
        }
        with self.assertRaisesRegex(ValueError, "installed version: 1.5"):
            validate_native_dependencies(versions, {})

    def test_invalid_required_predicate_names_declaring_mod(self):
        versions = {
            "feature": record("feature", depends={"library": ">=1.x"}),
            "library": record("library"),
        }
        with self.assertRaisesRegex(
            UnsupportedPredicate, "feature@1.0 requires library.*unsupported"
        ):
            validate_native_dependencies(versions, {})

    def test_runtime_ids_cannot_be_spoofed(self):
        with self.assertRaisesRegex(ValueError, "reserved runtime ID"):
            validate_native_dependencies({"bad": record("bad", provides=["java"])}, {"java": "25"})
