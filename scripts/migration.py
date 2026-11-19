"""Validate the explicit migration inventory; availability is not qualification."""

import tomllib
from pathlib import Path

STATUSES = {
    "static-verified",
    "awaiting-upstream",
    "replacement-required",
    "deferred",
    "manual-acceptance-required",
}


def validate_migration(root: Path, branch: str, target: str, *, release: bool = False) -> None:
    data = tomllib.loads((root / "migration.toml").read_text())
    collection = tomllib.loads((root / "collection.toml").read_text())
    if data.get("schema") != 1 or branch not in {data["source"], data["target"]}:
        raise ValueError("migration inventory schema or version branch mismatch")
    features = {p["project-id"]: p for p in collection["selected"] if p["role"] == "feature"}
    entries = data["feature"]
    recorded = {p["project-id"]: p for p in entries}
    if len(recorded) != len(entries) or not features.keys() <= recorded.keys():
        raise ValueError("migration inventory has duplicate IDs or omits active features")
    if branch == data["source"] and features.keys() != recorded.keys():
        raise ValueError("migration inventory must cover the maintained source feature set exactly")
    for entry in entries:
        check_entry(entry, features, target, data["target"])
    if release and branch == data["target"]:
        require_migrated(entries, features)


def require_migrated(entries: list[dict], features: dict) -> None:
    if {entry["project-id"] for entry in entries} != features.keys():
        raise ValueError("migration release must resolve the entire intended feature inventory")
    for entry in entries:
        if entry["status"] not in {"static-verified", "manual-acceptance-required"}:
            raise ValueError(f"{entry['slug']}: migration release is blocked by {entry['status']}")
        if entry["runtime"] != "accepted":
            raise ValueError(f"{entry['slug']}: migration runtime acceptance remains pending")


def check_entry(entry: dict, features: dict, target: str, migration_target: str) -> None:
    pid = entry["project-id"]
    if entry["status"] not in STATUSES or entry["runtime"] not in {"pending", "accepted"}:
        raise ValueError(f"{pid}: invalid migration status")
    if not entry.get("reason") or not entry.get("evidence", "").startswith("https://"):
        raise ValueError(f"{pid}: migration status needs reason and evidence")
    if pid in features and entry["slug"] != features[pid]["slug"]:
        raise ValueError(f"{pid}: migration project identity/slug mismatch")
    qualified = entry["status"] in {"static-verified", "manual-acceptance-required"}
    if qualified and (target != migration_target or pid not in features):
        raise ValueError(f"{pid}: cannot claim migrated static checks before target/pin promotion")
    if entry["runtime"] == "accepted" and not qualified:
        raise ValueError(f"{pid}: runtime acceptance cannot precede target migration")
