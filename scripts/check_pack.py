#!/usr/bin/env python3
"""Validate collection intent, client policy, dependency closure, pins, and index."""

import argparse
import sys
from pathlib import Path

from pack_model import ROOT, environment_notices, load_pack


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        pack = load_pack(args.root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    features = sum(p["role"] == "feature" for p in pack.projects.values())
    for notice in environment_notices(pack):
        print(notice)
    print(
        f"PASS: {features} mod features, {len(pack.mods) - features} libraries, {len(pack.shaders)} optional shader choices, all client-only; exact Fabric 26.2 pins and index checked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
