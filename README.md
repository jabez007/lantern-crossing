# Lantern Crossing

A reproducible Fabric client pack for Minecraft Java 26.2 focused on performance,
navigation, quality-of-life improvements, and better interfaces while remaining
compatible with unmodified vanilla servers.

Server operators do not need to install anything. Every active packwiz record
uses `side = "client"`, and the exported pack marks every mod as required on the
client and unsupported on the server. Selected functionality must work entirely
from the client using vanilla server data. The [mod audit](docs/mod-audit.md)
documents that decision for all 30 requested projects. Static checks enforce the
packaging contract. A clean-client vanilla-server join still needs
[runtime acceptance](docs/acceptance-tests.md).

The target is Minecraft **26.2**, Fabric Loader **0.20.1**, and Java **25**.
The loader pin comes from Fabric's [26.2 compatibility
API](https://meta.fabricmc.net/v2/versions/loader/26.2), checked on 2026-11-17.
The checked evidence is in [upstream-metadata.json](docs/upstream-metadata.json).
Pack version `26.2.0.3.0` is a development baseline, not a runtime qualification.

## Version branches

- [`26.2`](https://github.com/jabez007/lantern-crossing/tree/26.2) maintains the
  Minecraft 26.2 pack and its audited 37-feature baseline.
- [`26.3`](https://github.com/jabez007/lantern-crossing/tree/26.3) is the default
  development branch for the next Minecraft version. This checkout still targets
  Minecraft 26.2 with the original 30 features. No 26.3 migration is qualified.

Use `26.2` for Minecraft 26.2 builds. Target pull requests at the intended version
branch and backport shared fixes deliberately. The branch name does not establish
Minecraft compatibility or runtime acceptance. `pack.toml` records the actual
target. See the [version-branch policy](docs/version-policy.md#version-branches).

The maintained line's six later feature additions and Default Options helper
are tracked by project ID in [migration.toml](migration.toml), not added to this
bootstrap. All 37 migration entries remain deferred, with runtime acceptance
pending. Discovery evidence is not an installed pin or compatibility audit.
The bootstrap retains older direct config overrides: use a disposable fresh
instance, not an existing player profile. The safe-defaults helper is part of
the future migration audit. The [configuration evaluation](docs/configuration.md#defaults-manager-evaluation-2026-11-19)
retains Default Options on the maintained line; shared checks now reject competing
managers, unsafe replacement/reset payloads and live root preference files.
No manager or target-specific default is promoted here.

## Pack philosophy

Lantern Crossing keeps vanilla progression, content, and server mechanics.
It supplies no blocks, items, mobs, dimensions, recipes, gameplay data packs,
server companions, shader packs, or resource packs. Upstream defaults apply
except for the documented [inventory, Client Tweaks, and Iris overrides](docs/configuration.md).

## Active selections

All 30 requested feature selections are active, with nine libraries in
[collection.toml](collection.toml).

| Category | Selected projects |
| --- | --- |
| Performance | Sodium, Lithium, FerriteCore, ImmediatelyFast, Entity Culling, More Culling, BadOptimizations, Dynamic FPS, FastQuit, Debugify, Language Reload |
| Inventory | Inventory Profiles Next, Mouse Tweaks, Shulker Box Tooltip, Client Tweaks |
| HUD and information | Status Effect Bars, Light Overlay, BetterF3, Better Mount HUD, Paginated Advancements, Better Statistics Screen |
| Navigation | Xaero's Minimap, Xaero's World Map, Zoomify |
| Writing | Sign Tweaks, Book Tweaks |
| Visual and social | LambDynamicLights, Chat Heads, Iris |
| Pack management | Mod Menu |

There are zero blocked requested features. Light Overlay uses the current
`lightoverlay` project, Modrinth ID `8qVa1XCN`; the audit records the identity
correction that completes this baseline.
Lantern Crossing selects release-designated feature versions. Upstream-declared
dependency closure may contain prerelease-versioned libraries when those exact
versions are required or bundled by the selected release. This does not permit
independently choosing arbitrary prerelease dependencies. See the
[audit](docs/mod-audit.md) for the exact provenance, including Mod Menu's
Placeholder API dependency and the libraries bundled with Iris and Client Tweaks.

Fabric API is an explicitly selected platform library. Cloth Config API,
Fabric Language Kotlin, libIPN, TCDCommons API, YACL, Balm, Text Placeholder API, and OverlayLib
are transitive dependencies. Libraries are separate from feature intent, and bundled libraries
remain inside upstream artifacts. The machine lock layer is `mods/*.pw.toml`.
It owns exact version IDs, URLs, and SHA-512 hashes. No mod JARs belong in Git.

## Install an exported pack

1. Obtain `lantern-crossing-26.2.0.3.0-dev-26.3.mrpack` and its `.sha256` file from a
   development build below. This is a Minecraft 26.2 development artifact.
2. Verify the download with `sha256sum --check lantern-crossing-26.2.0.3.0-dev-26.3.sha256`.
3. Import the `.mrpack` into a launcher that supports Modrinth packs. Use a new
   instance with Java 25 and let the launcher obtain the pinned upstream files.
4. Start the client and complete the [smoke tests](docs/acceptance-tests.md),
   including joining a completely vanilla 26.2 server.

Do not merge this pack into an existing instance's mod directory. A clean
instance avoids leftover mods and configuration. Server rules may restrict
minimaps or inventory assistance even though they require no server mods.

## Build and validate

The scripts use Python 3.11 or newer and its standard library. Unit tests and
repository validation work offline. Export needs access to the pinned mod URLs
unless packwiz's external download cache already contains them.

Install the exact development tools from the repository root:

```sh
python3 -m pip install -r requirements-dev.txt
go install github.com/packwiz/packwiz@170b22d785959dda5876b54b7f16e1b807a57fb6
export PATH="$(go env GOPATH)/bin:$PATH"
```

Use Go 1.24.6 for the same packwiz build environment as CI. Ruff 0.16.4 is pinned
in [requirements-dev.txt](requirements-dev.txt). Tool versions and checks are
also recorded in [verification.md](docs/verification.md).

| Command | Result |
| --- | --- |
| `make test` | Offline Python unit tests |
| `make lint` | Ruff lint, formatting, and complexity check |
| `make validate` | Exact pins, native dependency predicates, migration inventory, branch policy and index |
| `make refresh` | Regenerate packwiz index after an intentional payload edit |
| `make export` | Validate, export, normalize, and validate the complete `.mrpack` |
| `make checksum` | Development export and SHA-256 checksum |
| `make release RELEASE_TAG=v<version>` | Qualified release build; blocked on this bootstrap |
| `make clean` | Remove generated `build/` and `dist/` files |

`PACKWIZ`, `PYTHON`, and `RUFF` can name explicit local executables.
Export checks the existing index before packwiz's implicit refresh, so it cannot
hide stale source metadata. ZIP normalization fixes entry order, timestamps,
permissions, and JSON encoding. Stored entries avoid compression-version drift.

Development outputs are:

```text
dist/lantern-crossing-26.2.0.3.0-dev-26.3.mrpack
dist/lantern-crossing-26.2.0.3.0-dev-26.3.sha256
```

GitHub Actions validates pushes to `26.2` and `26.3` and pull requests targeting
either branch. It checks index consistency, builds twice to compare archive
bytes, and uploads version/branch/channel-labeled artifacts. The archive itself
also identifies development status and the actual Minecraft target.

[release-policy.toml](release-policy.toml) records the intended 26.3 line.
Numeric branch names must match it. Publishing requires a matching actual target,
tag ancestry on the version branch, and owner runtime acceptance bound to the
pack hash. This branch still targets 26.2 and cannot publish a release. No
acceptance result is recorded. Qualified 26.2 releases retain their existing
names on the maintained branch. See [version policy](docs/version-policy.md).

## Select and update deliberately

Version numbers follow `<Minecraft version>.<pack major>.<pack minor>.<pack patch>`.
`26.2.0.3.0` means Minecraft 26.2 and pack revision 0.3.0. Tags must match
`pack.toml` exactly with a `v` prefix.

Use exact upstream version IDs and repeat the client-only audit for updates.
Do not run a floating bulk update. All active records are pinned with packwiz's
`pin = true`. [version-policy.md](docs/version-policy.md) explains the update
procedure and [candidates.toml](candidates.toml) records future proposals without
including them in exports.

Discover current stable build availability with:

```sh
python3 scripts/check_target_readiness.py
python3 scripts/check_target_readiness.py --scope requested
python3 scripts/check_target_readiness.py --offline
```

The default checks active features and libraries. The requested scope covers
all 30 requested features. Both scopes currently report release availability for
the complete baseline.
Discovery does not qualify a dependency closure, audit a pinned artifact, or
replace runtime testing.

## Repository structure and licensing

[Cobbled Horizon](https://github.com/vice-magus-faolan/cobbled-horizon/tree/7850a25ebae704d5d07a91ed0c89c1e9be9e9e19)
provided the architectural reference for collection intent, candidates,
validation, and release naming. Lantern Crossing implements a smaller client
workflow. It contains no server deployment or runtime management system.

Repository-authored scripts and documentation use the [MIT license](LICENSE).
That license does not relicense Minecraft or any mod. Each mod retains its own
upstream license. Packwiz references upstream artifacts rather than vendoring
their JARs. The `.mrpack` contains download references and the documented config.
