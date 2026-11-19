#!/usr/bin/env python3
"""Discover Fabric mods and Iris shaders; this does not qualify runtime behavior."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path

from pack_model import ROOT, TARGET, load_toml, stable


def compatible_versions(
    versions: list[dict], target: str, release_only: bool = True, *, loader: str = "fabric"
) -> list[dict]:
    return [
        v
        for v in versions
        if target in v.get("game_versions", [])
        and loader in v.get("loaders", [])
        and (not release_only or stable(v))
    ]


def fetch_versions(project_id: str) -> list[dict]:
    request = urllib.request.Request(
        f"https://api.modrinth.com/v2/project/{project_id}/version",
        headers={"User-Agent": "lantern-crossing-readiness/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def discover(
    root: Path, target: str, scope: str, snapshot: dict | None, release_only: bool = True
) -> list[dict]:
    collection = load_toml(root / "collection.toml")
    projects = collection["selected"] + collection["resolved-dependency"]
    if scope == "requested":
        projects = [p for p in projects if p["role"] == "feature"] + collection["excluded"]
    projects += collection.get("shader", [])
    results = []
    for project in projects:
        pid = project["project-id"]
        loader = "iris" if project["role"] == "shader" else "fabric"
        try:
            versions = (
                snapshot["shader_projects" if loader == "iris" else "projects"][pid]["versions"]
                if snapshot is not None
                else fetch_versions(pid)
            )
            matches = compatible_versions(versions, target, release_only, loader=loader)
            results.append(
                {"name": project["name"], "loader": loader, "ready": bool(matches), "error": None}
            )
        except (OSError, urllib.error.URLError, KeyError, ValueError) as exc:
            results.append(
                {"name": project["name"], "loader": loader, "ready": False, "error": str(exc)}
            )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minecraft", default=TARGET)
    parser.add_argument("--scope", choices=("active", "requested"), default="active")
    parser.add_argument(
        "--offline", action="store_true", help="use the dated repository snapshot, limited to 26.2"
    )
    parser.add_argument(
        "--include-prereleases",
        action="store_true",
        help="discovery only; never permits activation",
    )
    args = parser.parse_args()
    snapshot = (
        json.loads((ROOT / "docs/upstream-metadata.json").read_text()) if args.offline else None
    )
    if snapshot and args.minecraft != snapshot["target"]:
        parser.error("offline snapshot covers only " + snapshot["target"])
    results = discover(ROOT, args.minecraft, args.scope, snapshot, not args.include_prereleases)
    print(
        "Discovery only: build availability does not prove dependency closure, client eligibility, or runtime acceptance."
    )
    if snapshot:
        print(
            "Offline snapshot base date "
            + snapshot["checked_at"]
            + "; later audits use per-project checked_at"
        )
    for result in results:
        detail = result["error"] or f"{result['loader']} {args.minecraft} build availability"
        print(f"{'READY' if result['ready'] else 'WAIT'}: {result['name']}: {detail}")
    return 0 if all(r["ready"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
