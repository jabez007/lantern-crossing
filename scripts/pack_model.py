"""The source contract shared by repository checks and archive validation."""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TARGET = "26.2"
REJECTED = {
    "appleskin",
    "jade",
    "easy-shulker-boxes",
    "easyshulkerboxes",
    "bookshelf-inspector",
    "bookshelfinspector",
    "client-sort",
    "clientsort",
    "EsAfCjCV",
    "nvQzSEkH",
}
PRERELEASE = re.compile(
    r"(?:alpha|beta|snapshot|preview|(?:^|[.+_-])(?:rc|pre|dev)(?:[.\d+_-]|$))", re.I
)


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(value: str) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and not any(c in value for c in "\\:\0")
        and all(part not in {"", ".", ".."} for part in value.split("/"))
    )


def stable(version: dict) -> bool:
    """Upstream release designation governs intentional selections."""
    return version.get("version_type") == "release"


def prerelease_dependency(version: dict) -> bool:
    """Prerelease-looking dependency artifacts need an exact upstream audit pin."""
    identifiers = [version.get("name", ""), version.get("version_number", "")]
    identifiers.extend(f["filename"] for f in version["files"] if f.get("primary"))
    identifiers.append(version["fabric_descriptor"]["version"])
    return not stable(version) or any(PRERELEASE.search(value) for value in identifiers)


@dataclass
class Pack:
    root: Path
    metadata: dict
    collection: dict
    evidence: dict
    projects: dict
    mods: dict
    versions: dict
    overrides: dict[str, bytes]


def entries_by_id(entries: list) -> dict:
    result = {}
    slugs = set()
    for entry in entries:
        for field in ("project-id", "slug", "name", "category", "role"):
            require(
                isinstance(entry.get(field), str) and entry[field], f"invalid collection {field}"
            )
        pid, slug = entry["project-id"], entry["slug"]
        require(pid not in result and slug not in slugs, f"duplicate project ID/slug: {pid}/{slug}")
        require(not ({pid, slug} & REJECTED), f"rejected project: {slug}")
        result[pid] = entry
        slugs.add(slug)
    return result


def check_collection(collection: dict, evidence: dict) -> dict:
    require(collection.get("schema") == 1, "collection schema must be 1")
    require(
        collection.get("minecraft") == TARGET and collection.get("loader") == "fabric",
        "collection target must be Fabric 26.2",
    )
    selected = collection.get("selected", [])
    dependencies = collection.get("resolved-dependency", [])
    excluded = collection.get("excluded", [])
    all_projects = entries_by_id(selected + dependencies + excluded)
    require(
        all(e["role"] in {"feature", "selected-library"} for e in selected), "invalid selected role"
    )
    require(all(e["role"] == "dependency" for e in dependencies), "invalid dependency role")
    require(
        all(e.get("reason") and e["role"] == "feature" for e in excluded),
        "excluded features need reasons",
    )
    requested = {e["project-id"] for e in selected + excluded if e["role"] == "feature"}
    require(
        requested == set(evidence["requested"]),
        "all requested features must be selected or explicitly excluded",
    )
    return {pid: e for pid, e in all_projects.items() if e not in excluded}


def check_candidates(root: Path, projects: dict) -> None:
    data = load_toml(root / "candidates.toml")
    require(data.get("schema") == 1, "candidates schema must be 1")
    ids, slugs = set(projects), {e["slug"] for e in projects.values()}
    for entry in data.get("candidate", []):
        for field in (
            "project-id",
            "slug",
            "category",
            "rationale",
            "status",
            "client-only",
            "target-support",
            "blockers",
            "promotion-criteria",
        ):
            require(entry.get(field), f"candidate missing {field}")
        require(
            entry["project-id"] not in ids and entry["slug"] not in slugs,
            "staged candidate leaks into active pack or repeats",
        )
        ids.add(entry["project-id"])
        slugs.add(entry["slug"])


def check_descriptor(descriptor: dict) -> None:
    require(descriptor.get("environment") != "server", "server-only Fabric module")
    # The containing artifact's hash pins bundled implementation components.
    for child in descriptor.get("bundled", []):
        check_descriptor(child)


def check_download(lock: dict, version: dict, pid: str) -> None:
    download = lock["download"]
    require(download.get("hash-format") == "sha512", "mod hashes must use SHA-512")
    require(bool(re.fullmatch(r"[0-9a-f]{128}", download["hash"])), "invalid mod SHA-512")
    url = urlsplit(download["url"])
    expected_path = f"/data/{pid}/versions/{version['id']}/{lock['filename']}"
    require(
        url.scheme == "https"
        and url.netloc == "cdn.modrinth.com"
        and unquote(url.path) == expected_path,
        "download URL must identify exact Modrinth project/version/file",
    )
    require(not url.query and not url.fragment, "download URL must not have a query or fragment")
    files = [f for f in version["files"] if f["filename"] == lock["filename"]]
    require(
        len(files) == 1 and files[0]["hashes"]["sha512"] == download["hash"],
        "pin hash/filename disagrees with upstream evidence",
    )


def check_mod(path: Path, projects: dict, evidence: dict) -> tuple[str, dict, dict]:
    lock = load_toml(path)
    pid = lock["update"]["modrinth"]["mod-id"]
    require(pid in projects, f"unexpected active project: {pid}")
    project = projects[pid]
    require(path.name == project["slug"] + ".pw.toml", f"lock slug disagrees: {path.name}")
    require(lock.get("side") == "client", f"{path.name}: side must be client")
    require(
        lock.get("pin") is True and not lock.get("option", {}).get("optional"),
        "all baseline mods must be pinned and required",
    )
    require(
        safe_path(lock["filename"])
        and "/" not in lock["filename"]
        and lock["filename"].endswith(".jar"),
        "unsafe mod filename",
    )
    upstream = evidence["projects"][pid]
    require(
        upstream.get("client_side") != "unsupported" and upstream.get("server_side") != "required",
        f"{project['slug']}: unsupported client or mandatory server requirement",
    )
    require(
        upstream["slug"] == project["slug"] and upstream["name"] == project["name"] == lock["name"],
        "collection/lock/upstream identity mismatch",
    )
    matches = [v for v in upstream["versions"] if v["id"] == lock["update"]["modrinth"]["version"]]
    require(len(matches) == 1, "pinned version missing from upstream evidence")
    version = matches[0]
    require(
        version["project_id"] == pid
        and TARGET in version["game_versions"]
        and "fabric" in version["loaders"],
        "pin must support Fabric 26.2",
    )
    if project["role"] != "dependency":
        require(stable(version), f"selected {project['slug']} must be release-designated")
    check_descriptor(version["fabric_descriptor"])
    check_download(lock, version, pid)
    return pid, lock, version


def check_dependencies(projects: dict, versions: dict, evidence: dict) -> None:
    check_dependency_stability(projects, versions)
    parents = {pid: set() for pid in projects}
    for pid, version in versions.items():
        requirements = {d["project_id"]: d.get("version_id") for d in version["client_required"]}
        check_upstream_requirements(pid, version, requirements, evidence)
        for dependency, exact in requirements.items():
            require(dependency in projects, f"required dependency missing: {dependency}")
            require(
                exact is None or versions[dependency]["id"] == exact,
                "exact dependency version mismatch",
            )
            parents[dependency].add(pid)
    for pid, project in projects.items():
        if project["role"] in {"dependency", "selected-library"}:
            require(
                set(project.get("required-by", [])) == parents[pid] and parents[pid],
                f"dependency parents disagree: {project['slug']}",
            )
    # No disconnected dependency cycle can disguise an unselected feature.
    reached = {pid for pid, p in projects.items() if p["role"] != "dependency"}
    pending = list(reached)
    while pending:
        for dep in versions[pending.pop()]["client_required"]:
            if dep["project_id"] not in reached:
                reached.add(dep["project_id"])
                pending.append(dep["project_id"])
    require(reached == set(projects), "orphan dependency outside selected closure")
    check_native_requirements(versions)


def upstream_dependency_pin(parent: dict, project_id: str, version: dict) -> bool:
    """Require the real upstream edge and its exact version declaration."""
    official = [
        d
        for d in parent["dependencies"]
        if d["dependency_type"] == "required" and d["project_id"] == project_id
    ]
    if any(d.get("version_id") == version["id"] for d in official):
        return True
    if not any(d.get("version_id") is None for d in official):
        return False
    return any(
        d["project_id"] == project_id
        and d.get("audited_version") == version["id"]
        and d.get("upstream_version") == version["version_number"]
        and urlsplit(d.get("audit_source", "")).scheme == "https"
        and bool(urlsplit(d.get("audit_source", "")).netloc)
        and d.get("evidence") == "https://api.modrinth.com/v2/version/" + parent["id"]
        for d in parent["client_required"]
    )


def check_dependency_stability(projects: dict, versions: dict) -> None:
    for pid, version in versions.items():
        if projects[pid]["role"] == "dependency" and prerelease_dependency(version):
            require(
                any(upstream_dependency_pin(parent, pid, version) for parent in versions.values()),
                f"prerelease dependency {projects[pid]['slug']} needs an exact upstream audit pin",
            )


def fabric_modules(descriptor: dict) -> list[dict]:
    return [descriptor] + [
        module for child in descriptor.get("bundled", []) for module in fabric_modules(child)
    ]


def check_native_requirements(versions: dict) -> None:
    """Also check dependencies omitted from the upstream project metadata."""
    modules = {pid: fabric_modules(v["fabric_descriptor"]) for pid, v in versions.items()}
    supplied = {
        pid: {mid for module in group for mid in [module["id"]] + module.get("provides", [])}
        for pid, group in modules.items()
    }
    for pid, group in modules.items():
        available = supplied[pid] | {"minecraft", "java", "fabricloader"}
        for dependency in versions[pid]["client_required"]:
            available |= supplied[dependency["project_id"]]
        for module in group:
            missing = set(module.get("depends", {})) - available
            require(
                not missing,
                f"Fabric module dependencies missing for {module['id']}: {sorted(missing)}",
            )


def check_upstream_requirements(
    pid: str, version: dict, requirements: dict, evidence: dict
) -> None:
    exceptions = {
        e["dependency"]
        for e in evidence.get("dependency_exceptions", [])
        if e["project_id"] == pid and e["version_id"] == version["id"]
    }
    for dependency in version["dependencies"]:
        if (
            dependency["dependency_type"] == "required"
            and dependency["project_id"] not in exceptions
        ):
            require(
                dependency["project_id"] in requirements,
                "upstream required dependency omitted from client closure",
            )
            require(
                dependency.get("version_id") is None
                or requirements[dependency["project_id"]] == dependency["version_id"],
                "upstream exact dependency constraint omitted",
            )
        if dependency["dependency_type"] == "incompatible":
            require(
                dependency["project_id"] not in evidence["active_ids"],
                "incompatible upstream projects selected together",
            )


def payload_files(root: Path) -> tuple[set[str], dict[str, bytes]]:
    require(
        not (root / "mods").is_symlink() and not (root / "config").is_symlink(),
        "payload directory symlink",
    )
    for name in ("options.txt", "servers.dat", "defaultoptions.journal.json"):
        path = root / name
        require(not path.is_symlink(), f"payload symlink: {path}")
        require(not path.exists(), f"runtime preferences must not be distributed: {name}")
    mods = {p.relative_to(root).as_posix() for p in (root / "mods").glob("*.pw.toml")}
    defaults = (root / "config/defaultoptions").exists()
    if defaults:
        require(
            "mods/default-options.pw.toml" in mods,
            "Default Options templates require the pinned helper",
        )
    configs = {}
    for path in (root / "config").rglob("*"):
        require(not path.is_symlink(), f"payload symlink: {path}")
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            require(
                not relative.lower().endswith((".jar", ".pw.toml")), "unexpected config artifact"
            )
            require(
                not set(path.relative_to(root).parts)
                & {
                    "staged",
                    "server-overrides",
                    "server.properties",
                    "eula.txt",
                    "servers.dat",
                    "defaultoptions.journal.json",
                },
                "staged or server-only config artifact",
            )
            require(
                not defaults or relative.startswith("config/defaultoptions/"),
                f"config must use copy-if-missing defaults, not direct overrides: {relative}",
            )
            configs[relative] = path.read_bytes()
    return mods, configs


def check_index(root: Path, pack: dict) -> dict[str, bytes]:
    require(
        pack["index"]["file"] == "index.toml" and pack["index"]["hash-format"] == "sha256",
        "unexpected index format",
    )
    require(digest(root / "index.toml") == pack["index"]["hash"], "stale pack index hash")
    index = load_toml(root / "index.toml")
    require(index.get("hash-format") == "sha256", "index must use SHA-256")
    mods, configs = payload_files(root)
    found = set()
    for entry in index.get("files", []):
        relative = entry["file"]
        require(safe_path(relative) and relative not in found, "unsafe or duplicate index path")
        require(relative in mods | configs.keys(), f"unexpected indexed file: {relative}")
        path = root / relative
        require(
            not path.is_symlink() and digest(path) == entry["hash"],
            f"stale index entry: {relative}",
        )
        require(bool(entry.get("metafile")) == (relative in mods), "index metafile flag disagrees")
        require(entry.get("alias") is None, "index aliases are not supported")
        found.add(relative)
    require(found == mods | configs.keys(), "index omits pack payload; run make refresh")
    return configs


def check_repository_files(root: Path) -> None:
    ignored = {".git", ".venv", ".agents", ".codex", ".aws", "build", "dist"}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if set(relative.parts) & ignored:
            continue
        require(path.suffix.lower() != ".jar", f"local JAR in source: {relative}")
        if relative.parts[0] == "mods" and len(relative.parts) > 1:
            require(
                path.is_file() and not path.is_symlink() and path.name.endswith(".pw.toml"),
                f"unexpected mod payload: {relative}",
            )


def load_pack(root: Path = ROOT) -> Pack:
    """Return a checked source contract, or raise ValueError with the failed invariant."""
    pack = load_toml(root / "pack.toml")
    require(pack.get("pack-format") == "packwiz:1.1.0", "unsupported pack format")
    require(
        set(pack["versions"]) == {"minecraft", "fabric"}
        and pack["versions"]["minecraft"] == TARGET,
        "target must be exactly Minecraft 26.2 + Fabric",
    )
    require(bool(re.fullmatch(r"26\.2\.\d+\.\d+\.\d+", pack["version"])), "invalid pack version")
    evidence = json.loads((root / "docs/upstream-metadata.json").read_text())
    require(evidence["schema"] == 1 and evidence["target"] == TARGET, "invalid upstream snapshot")
    require(
        evidence["fabric_loader"]["stable"]
        and pack["versions"]["fabric"] == evidence["fabric_loader"]["version"],
        "Fabric pin disagrees with stable compatibility evidence",
    )
    collection = load_toml(root / "collection.toml")
    projects = check_collection(collection, evidence)
    check_candidates(root, projects)
    mods, versions = {}, {}
    for path in sorted((root / "mods").glob("*.pw.toml")):
        pid, lock, version = check_mod(path, projects, evidence)
        require(pid not in mods, f"duplicate lock project ID: {pid}")
        mods[pid], versions[pid] = lock, version
    require(
        mods.keys() == projects.keys(), "selected project or dependency absent from active pack"
    )
    require(len({m["filename"] for m in mods.values()}) == len(mods), "duplicate mod filename")
    evidence["active_ids"] = list(mods)
    check_dependencies(projects, versions, evidence)
    check_repository_files(root)
    overrides = check_index(root, pack)
    return Pack(root, pack, collection, evidence, projects, mods, versions, overrides)
