"""Keep rejected writing candidates out and retain reproducible text-safety evidence."""

import hashlib
import json
import unittest

import test_pack as fixtures
from pack_model import ROOT, load_pack, load_toml


RECOVERY_CANDIDATES = {
    "pfokf5Ct",
    "oUFjGUhJ",
    "DJVsjgm4",
    "P6TVpx0l",
    "yXAvIk0x",
    "fX4dIQCo",
    "Ss2JOg1D",
    "eKvNAquO",
}


class WritingRecoveryTests(unittest.TestCase):
    setUp = fixtures.PackTests.setUp
    invalid = fixtures.PackTests.invalid

    def test_readme_accounts_for_requests_without_claiming_feature_parity(self):
        text = (ROOT / "README.md").read_text()
        self.assertNotIn("All 30 originally requested features remain active", text)
        self.assertIn("Sign Tweaks and Book Tweaks", text)
        pack = load_pack(self.root)
        features = sum(p["role"] == "feature" for p in pack.projects.values())
        self.assertIn(f"{features} intentional Fabric mod", text)

    def test_recovery_candidates_require_a_new_audit_before_selection(self):
        staged = {p["project-id"] for p in load_toml(ROOT / "candidates.toml")["candidate"]}
        self.assertTrue(RECOVERY_CANDIDATES <= staged)
        collection = self.root / "collection.toml"
        snapshot = self.root / "docs/upstream-metadata.json"
        original_collection, original_snapshot = collection.read_text(), snapshot.read_text()
        for pid in sorted(RECOVERY_CANDIDATES):
            collection.write_text(
                original_collection
                + f'\n[[selected]]\nproject-id = "{pid}"\nslug = "candidate-{pid}"\nname = "candidate"\ncategory = "writing"\nrole = "feature"\n'
            )
            data = json.loads(original_snapshot)
            data["requested"].append(pid)
            snapshot.write_text(json.dumps(data))
            with self.subTest(candidate=pid):
                self.invalid("staged candidate leaks|writing editor conflict")
            collection.write_text(original_collection)
            snapshot.write_text(original_snapshot)

    def test_upstream_safety_observations_remain_bound_to_the_oracle(self):
        evidence = json.loads((ROOT / "tests/fixtures/writing-recovery.json").read_text())
        adapter = ROOT / "tests/fixtures/WritingRecoveryOracle.java"
        self.assertEqual(
            evidence["adapter-sha256"], hashlib.sha256(adapter.read_bytes()).hexdigest()
        )
        observed = evidence["observations"]
        paste = observed["bookpaste"]
        self.assertEqual(paste["long-word-remainder-units"], 76)
        self.assertTrue(paste["full-final-page-retains-text"])
        self.assertTrue(paste["surrogate-pair-preserved-at-capacity"])
        self.assertEqual(paste["combining-sequence-remainder"], "\u0301Z")
        for mode in ("SMART_FILL", "WHOLE_PARAGRAPHS"):
            self.assertEqual(paste[mode + "-whitespace-output"], "alpha")
        self.assertEqual(paste["boundary-remainder"], "next")
        self.assertEqual(paste["large-payload-remainder-after-100-helper-slices"], 397600)
        extractor = observed["book-extractor"]
        self.assertTrue(extractor["ordinary-roundtrip-equal"])
        self.assertFalse(extractor["marker-collision-preserved"])
        self.assertEqual(extractor["marker-collision-roundtrip"], ["before", "after"])
        self.assertTrue(extractor["101-pages-rejected"])
        self.assertTrue(extractor["1025-units-rejected"])
        self.assertEqual(observed["booker"]["zero-page-reader-exception"], "ArithmeticException")

    def test_existing_writing_pins_and_defaults_remain_unchanged(self):
        pack = load_pack(self.root)
        self.assertEqual(pack.versions["UCpxwAAu"]["id"], "ics7z6RR")
        self.assertEqual(pack.versions["NKvLVQMc"]["id"], "Y9zsgkwF")
        self.assertTrue(RECOVERY_CANDIDATES.isdisjoint(pack.projects))
        self.assertFalse(any("bookpaste" in p or "bookextractor" in p for p in pack.overrides))
        options = (ROOT / "configureddefaults/options.txt").read_text()
        self.assertNotIn("bookpaste", options)
        self.assertNotIn("bookextractor", options)
