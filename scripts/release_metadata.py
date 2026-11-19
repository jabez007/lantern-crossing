#!/usr/bin/env python3
"""Name development artifacts and gate release publication on explicit qualification."""

import argparse
import hashlib
import os
import re
import subprocess
from pathlib import Path

from migration import validate_migration
from pack_model import ROOT, TARGET, load_toml, require, safe_path


def current_branch(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() or None


def check_qualification(root: Path, policy: dict, pack: dict, tag: str | None) -> None:
    require(tag is not None, "release channel requires an explicit matching tag")
    require(
        policy["version-branch"] == pack["versions"]["minecraft"],
        "migration branch cannot publish a release for a different Minecraft target",
    )
    validate_migration(root, policy["version-branch"], pack["versions"]["minecraft"], release=True)
    require(
        policy.get("runtime-accepted-version") == pack["version"],
        "release is not runtime-qualified: owner must record acceptance for this version",
    )
    require(
        policy.get("runtime-accepted-pack-sha256")
        == hashlib.sha256((root / "pack.toml").read_bytes()).hexdigest(),
        "runtime acceptance does not match the current pack/index hash",
    )
    record = policy.get("runtime-acceptance-record", "")
    require(
        safe_path(record) and record.startswith("docs/") and (root / record).is_file(),
        "release requires an owner-authored acceptance record under docs/",
    )


def metadata(
    root: Path = ROOT,
    tag: str | None = None,
    *,
    branch: str | None = None,
    channel: str = "development",
) -> dict[str, str]:
    pack = load_toml(root / "pack.toml")
    version = pack["version"]
    target = pack["versions"]["minecraft"]
    suffix = version.removeprefix(target + ".").split(".")
    require(
        version.startswith(target + ".")
        and len(suffix) == 3
        and all(p.isascii() and p.isdecimal() for p in suffix),
        "version must be <Minecraft>.<major>.<minor>.<patch>",
    )
    require(target == TARGET, f"validated Minecraft target must remain {TARGET}")
    require(tag is None or tag == "v" + version, "release tag must agree with pack.toml")
    policy = load_toml(root / "release-policy.toml")
    line = policy["version-branch"]
    require(
        policy.get("schema") == 1 and re.fullmatch(r"[0-9]+\.[0-9]+", line),
        "invalid version branch policy",
    )
    require(line == target, "version branch must target its own Minecraft release")
    actual_branch = branch or current_branch(root)
    require(
        not actual_branch
        or not re.fullmatch(r"[0-9]+\.[0-9]+", actual_branch)
        or actual_branch == line,
        "version branch disagrees with release-policy.toml",
    )
    require(channel in {"development", "release"}, "unknown artifact channel")
    validate_migration(root, line, target)
    if channel == "release":
        check_qualification(root, policy, pack, tag)
    return artifact_names(pack, line, channel)


def artifact_names(pack: dict, line: str, channel: str) -> dict[str, str]:
    version = pack["version"]
    target = pack["versions"]["minecraft"]
    development = channel == "development"
    artifact_version = version + (f"-dev.{line}" if development else "")
    basename = "lantern-crossing-" + version + (f"-dev-{line}" if development else "")
    return {
        "version": version,
        "minecraft": target,
        "version-branch": line,
        "channel": channel,
        "artifact-version": artifact_version,
        "artifact-name": basename,
        "name": pack["name"] + (f" (development, {line} branch)" if development else ""),
        "summary": f"Minecraft {target}; {channel} artifact from {line} version branch.",
        "basename": basename,
        "archive": basename + ".mrpack",
        "checksum": basename + ".sha256",
    }


def check_documentation(root: Path, version_branch: str) -> None:
    """Keep current install instructions tied to the development artifact identity.

    Check explicit current-version statements, leaving historical audit evidence
    alone. Release publication uses the same development instructions in Git.
    """
    pack = load_toml(root / "pack.toml")
    info = artifact_names(pack, version_branch, "development")
    for name in ("README.md", "docs/verification.md"):
        content = (root / name).read_text()
        require(
            f"Pack version `{info['version']}`" in content and info["archive"] in content,
            f"{name}: current-version/artifact documentation disagrees with pack.toml or branch",
        )
    require(
        (root / "docs/release-notes.md")
        .read_text()
        .startswith(f"Lantern Crossing {info['version']} "),
        "docs/release-notes.md: current-version documentation disagrees with pack.toml",
    )
    policy = (root / "docs/version-policy.md").read_text()
    require(
        all(
            statement in policy
            for statement in (
                f"The current development baseline is `{info['version']}`.",
                f"--tag v{info['version']}",
                f"make release RELEASE_TAG=v{info['version']}",
            )
        ),
        "docs/version-policy.md: current-version/release-example documentation disagrees with pack.toml",
    )


def write_checksum(root: Path = ROOT, **build_context) -> Path:
    info = metadata(root, **build_context)
    archive = root / "dist" / info["archive"]
    checksum = root / "dist" / info["checksum"]
    checksum.write_text(
        hashlib.sha256(archive.read_bytes()).hexdigest() + "  " + info["archive"] + "\n"
    )
    return checksum


def add_context_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tag", default=os.environ.get("RELEASE_TAG") or None)
    parser.add_argument("--branch", default=os.environ.get("PACK_BRANCH") or None)
    parser.add_argument(
        "--channel",
        choices=("development", "release"),
        default=os.environ.get("PACK_CHANNEL", "development"),
    )


def context(args: argparse.Namespace) -> dict:
    return {"tag": args.tag, "branch": args.branch, "channel": args.channel}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_context_arguments(parser)
    parser.add_argument("--field")
    parser.add_argument("--checksum", action="store_true")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        info = metadata(**context(args))
        check_documentation(ROOT, info["version-branch"])
        if args.github_output:
            with args.github_output.open("a") as output:
                output.write("".join(f"{key}={value}\n" for key, value in info.items()))
        if args.checksum:
            print(write_checksum(**context(args)))
        elif args.field:
            print(info[args.field])
        else:
            print(
                f"PASS: {info['archive']}, actual Minecraft {info['minecraft']}, {info['channel']}"
            )
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
