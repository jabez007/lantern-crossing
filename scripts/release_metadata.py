#!/usr/bin/env python3
"""Read release names, check an optional tag, or write the artifact checksum."""

import argparse
import hashlib
from pathlib import Path

from pack_model import ROOT, TARGET, load_toml, require


def metadata(root: Path = ROOT, tag: str | None = None) -> dict[str, str]:
    pack = load_toml(root / "pack.toml")
    version = pack["version"]
    suffix = version.removeprefix(TARGET + ".").split(".")
    require(
        version.startswith(TARGET + ".")
        and len(suffix) == 3
        and all(p.isdecimal() for p in suffix),
        "version must be 26.2.<major>.<minor>.<patch>",
    )
    require(pack["versions"]["minecraft"] == TARGET, "release target must be 26.2")
    require(tag is None or tag == "v" + version, "release tag must agree with pack.toml")
    basename = "lantern-crossing-" + version
    return {
        "version": version,
        "minecraft": TARGET,
        "basename": basename,
        "archive": basename + ".mrpack",
        "checksum": basename + ".sha256",
    }


def write_checksum(root: Path = ROOT) -> Path:
    info = metadata(root)
    archive = root / "dist" / info["archive"]
    checksum = root / "dist" / info["checksum"]
    checksum.write_text(
        hashlib.sha256(archive.read_bytes()).hexdigest() + "  " + info["archive"] + "\n"
    )
    return checksum


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag")
    parser.add_argument(
        "--field", choices=("version", "minecraft", "basename", "archive", "checksum")
    )
    parser.add_argument("--checksum", action="store_true")
    args = parser.parse_args()
    try:
        info = metadata(tag=args.tag)
        if args.checksum:
            print(write_checksum())
        elif args.field:
            print(info[args.field])
        else:
            print(f"PASS: {info['version']}, Minecraft {TARGET}, tag v{info['version']}")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
