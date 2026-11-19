#!/usr/bin/env python3
"""Canonicalize ZIP ordering, timestamps, permissions, and JSON for reproducible bytes."""

import argparse
import json
import os
import zipfile
from pathlib import Path

from release_metadata import add_context_arguments, context, metadata
from validate_mrpack import read_archive, validate


def normalize(path: Path, identity: dict | None = None) -> None:
    contents = read_archive(path)
    manifest = json.loads(contents["modrinth.index.json"])
    if identity is not None:
        manifest.update(
            name=identity["name"],
            versionId=identity["artifact-version"],
            summary=identity["summary"],
        )
    manifest["files"].sort(key=lambda entry: entry["path"])
    contents["modrinth.index.json"] = (
        json.dumps(manifest, sort_keys=True, indent=2) + "\n"
    ).encode()
    temporary = path.with_suffix(".tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, data in sorted(contents.items()):
                if name.endswith("/"):
                    continue
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    add_context_arguments(parser)
    args = parser.parse_args()
    validate(args.archive, raw=True, **context(args))
    normalize(args.archive, metadata(**context(args)))
    validate(args.archive, **context(args))


if __name__ == "__main__":
    main()
