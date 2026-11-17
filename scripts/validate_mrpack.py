#!/usr/bin/env python3
"""Validate the complete .mrpack against the checked source contract."""

from __future__ import annotations

import argparse
import json
import stat
import sys
import zipfile
from pathlib import Path

from pack_model import ROOT, Pack, load_pack, require, safe_path


def read_archive(path: Path) -> dict[str, bytes]:
    require(path.suffix == ".mrpack", "validation requires a complete .mrpack archive")
    contents = {}
    with zipfile.ZipFile(path) as archive:
        require(
            sum(e.file_size for e in archive.infolist()) < 16 * 1024 * 1024,
            "unexpectedly large metadata archive",
        )
        for entry in archive.infolist():
            name = entry.filename
            require(safe_path(name.removesuffix("/")), f"unsafe archive path: {name}")
            require(name not in contents, f"duplicate archive path: {name}")
            kind = stat.S_IFMT(entry.external_attr >> 16)
            require(
                kind in {0, stat.S_IFDIR if entry.is_dir() else stat.S_IFREG},
                f"unsafe archive file type: {name}",
            )
            contents[name] = archive.read(entry)
    require("modrinth.index.json" in contents, "missing modrinth.index.json")
    return contents


def check_manifest(manifest: dict, pack: Pack) -> None:
    require(
        manifest.get("formatVersion") == 1 and manifest.get("game") == "minecraft",
        "invalid mrpack format/game",
    )
    require(manifest.get("name") == pack.metadata["name"], "archive pack name mismatch")
    require(manifest.get("versionId") == pack.metadata["version"], "archive version mismatch")
    require(
        manifest.get("dependencies")
        == {
            "minecraft": "26.2",
            "fabric-loader": pack.metadata["versions"]["fabric"],
        },
        "archive must target exact Minecraft 26.2 and Fabric loader pin",
    )


def check_mods(files: list, pack: Pack) -> None:
    expected = {"mods/" + m["filename"]: (pid, m) for pid, m in pack.mods.items()}
    seen = set()
    for entry in files:
        path = entry["path"]
        require(path in expected and path not in seen, f"unexpected/duplicate exported mod: {path}")
        pid, lock = expected[path]
        require(
            entry.get("env") == {"client": "required", "server": "unsupported"},
            f"{path}: expected client required, server unsupported",
        )
        require(entry.get("downloads") == [lock["download"]["url"]], f"{path}: pinned URL mismatch")
        upstream = next(f for f in pack.versions[pid]["files"] if f["filename"] == lock["filename"])
        require(entry.get("hashes") == upstream["hashes"], f"{path}: exact SHA-1/SHA-512 mismatch")
        require(entry.get("fileSize") == upstream["size"], f"{path}: file size mismatch")
        seen.add(path)
    require(seen == expected.keys(), "archive missing baseline project or required dependency")


def validate(path: Path, root: Path = ROOT) -> None:
    pack = load_pack(root)
    contents = read_archive(path)
    manifest = json.loads(contents.pop("modrinth.index.json"))
    check_manifest(manifest, pack)
    check_mods(manifest["files"], pack)
    expected = {"overrides/" + name: data for name, data in pack.overrides.items()}
    # Packwiz emits one empty overrides directory, even when there are no configs.
    contents.pop("overrides/", None)
    require(
        contents == expected,
        "archive overrides missing, changed, staged, or server-only; only repository configs are allowed",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate(args.archive, args.root)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        f"PASS: {args.archive.name}: exact client baseline, dependencies, hashes, environments, and config bytes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
