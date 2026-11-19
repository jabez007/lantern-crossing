#!/usr/bin/env python3
"""Validate the complete .mrpack against the checked source contract."""

from __future__ import annotations

import argparse
import json
import stat
import sys
import zipfile
from pathlib import Path

from pack_model import ROOT, Pack, environment_notices, load_pack, require, safe_path
from release_metadata import add_context_arguments, context, metadata


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


def check_manifest(manifest: dict, pack: Pack, identity: dict, raw: bool) -> None:
    require(
        manifest.get("formatVersion") == 1 and manifest.get("game") == "minecraft",
        "invalid mrpack format/game",
    )
    expected_name = pack.metadata["name"] if raw else identity["name"]
    expected_version = pack.metadata["version"] if raw else identity["artifact-version"]
    require(manifest.get("name") == expected_name, "archive pack name/channel mismatch")
    require(manifest.get("versionId") == expected_version, "archive version/channel mismatch")
    if not raw:
        require(
            manifest.get("summary") == identity["summary"], "archive target/channel label mismatch"
        )
    require(
        manifest.get("dependencies")
        == {
            "minecraft": "26.2",
            "fabric-loader": pack.metadata["versions"]["fabric"],
        },
        "archive must target exact Minecraft 26.2 and Fabric loader pin",
    )


def check_downloads(files: list, pack: Pack) -> None:
    expected = {
        directory + "/" + lock["filename"]: (lock, versions[pid])
        for directory, locks, versions in (
            ("mods", pack.mods, pack.versions),
            ("shaderpacks", pack.shaders, pack.shader_versions),
        )
        for pid, lock in locks.items()
    }
    seen = set()
    for entry in files:
        path = entry["path"]
        require(
            path in expected and path not in seen,
            f"unexpected/duplicate exported mod/shader: {path}",
        )
        lock, version = expected[path]
        require(
            entry.get("env") == {"client": "required", "server": "unsupported"},
            f"{path}: expected client required, server unsupported",
        )
        require(entry.get("downloads") == [lock["download"]["url"]], f"{path}: pinned URL mismatch")
        upstream = next(f for f in version["files"] if f["filename"] == lock["filename"])
        require(entry.get("hashes") == upstream["hashes"], f"{path}: exact SHA-1/SHA-512 mismatch")
        require(entry.get("fileSize") == upstream["size"], f"{path}: file size mismatch")
        seen.add(path)
    require(
        seen == expected.keys(), "archive missing baseline project, shader or required dependency"
    )


def validate(path: Path, root: Path = ROOT, *, raw: bool = False, **build_context) -> Pack:
    """Return the checked source contract only after the complete archive passes."""
    pack = load_pack(root)
    identity = metadata(root, **build_context)
    require(path.name == identity["archive"], "archive filename/branch/channel mismatch")
    contents = read_archive(path)
    manifest = json.loads(contents.pop("modrinth.index.json"))
    check_manifest(manifest, pack, identity, raw)
    check_downloads(manifest["files"], pack)
    expected = {"overrides/" + name: data for name, data in pack.overrides.items()}
    # Packwiz emits one empty overrides directory, even when there are no configs.
    contents.pop("overrides/", None)
    require(
        contents == expected,
        "archive overrides missing, changed, staged, or server-only; only repository configs are allowed",
    )
    return pack


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    add_context_arguments(parser)
    args = parser.parse_args()
    try:
        pack = validate(args.archive, args.root, **context(args))
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    for notice in environment_notices(pack):
        print(notice)
    print(
        f"PASS: {args.archive.name}: exact client baseline, dependencies, hashes, environments, and config bytes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
