"""Validate complete source-artifact migration intent, pins and release acceptance."""

import json
import tomllib
from pathlib import Path

STATUSES = {
    "static-verified",
    "awaiting-upstream",
    "replacement-required",
    "deferred",
    "manual-acceptance-required",
}
QUALIFIED = {"static-verified", "manual-acceptance-required"}


def validate_migration(root: Path, branch: str, target: str, *, release: bool = False) -> None:
    data = tomllib.loads((root / "migration.toml").read_text())
    collection = tomllib.loads((root / "collection.toml").read_text())
    if data.get("schema") != 2 or branch not in {data["source"], data["target"]}:
        raise ValueError("migration inventory schema or version branch mismatch")
    active = {
        p["project-id"]: p
        for kind in ("selected", "resolved-dependency", "shader")
        for p in collection.get(kind, [])
    }
    entries = data["artifact"]
    recorded = {p["project-id"]: p for p in entries}
    if len(recorded) != len(entries) or not active.keys() <= recorded.keys():
        raise ValueError("migration inventory has duplicate IDs or omits active artifacts")
    if len(entries) != data["source-artifact-count"]:
        raise ValueError("migration inventory must account for every source artifact")
    evidence = json.loads((root / "docs/upstream-metadata.json").read_text())
    for entry in entries:
        check_entry(entry, active, evidence, target, data["target"])
    if release and branch == data["target"]:
        require_migrated(entries, active)


def require_migrated(entries: list[dict], active: dict) -> None:
    if {entry["project-id"] for entry in entries} != active.keys():
        raise ValueError("migration release must resolve the entire intended artifact inventory")
    for entry in entries:
        if entry["status"] not in QUALIFIED:
            raise ValueError(f"{entry['slug']}: migration release is blocked by {entry['status']}")
        if entry["runtime"] != "accepted":
            raise ValueError(f"{entry['slug']}: migration runtime acceptance remains pending")


def check_entry(entry: dict, active: dict, evidence: dict, target: str, migration_target: str):
    pid = entry["project-id"]
    if entry["status"] not in STATUSES or entry["runtime"] not in {"pending", "accepted"}:
        raise ValueError(f"{pid}: invalid migration status")
    if not entry.get("reason") or not entry.get("evidence", "").startswith("https://"):
        raise ValueError(f"{pid}: migration status needs reason and evidence")
    if pid in active and any(entry[key] != active[pid][key] for key in ("slug", "role")):
        raise ValueError(f"{pid}: migration project identity/role mismatch")
    qualified = entry["status"] in QUALIFIED
    if qualified:
        if target != migration_target or pid not in active:
            raise ValueError(
                f"{pid}: cannot claim migrated static checks before target/pin promotion"
            )
        kind = "shader_projects" if entry["role"] == "shader" else "projects"
        versions = evidence[kind][pid]["versions"]
        matches = [v for v in versions if v["id"] == entry["target-version-id"]]
        if len(matches) != 1 or matches[0]["version_number"] != entry["target-version"]:
            raise ValueError(f"{pid}: migration pin disagrees with audited artifact")
        dependencies = {d["project_id"] for d in matches[0].get("client_required", [])}
        if set(entry["dependencies"]) != dependencies:
            raise ValueError(f"{pid}: migration dependencies disagree with audited closure")
    if entry["runtime"] == "accepted" and not qualified:
        raise ValueError(f"{pid}: runtime acceptance cannot precede target migration")
