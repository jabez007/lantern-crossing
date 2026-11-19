# Lantern Crossing

A reproducible Fabric client pack for Minecraft Java 26.2 focused on performance,
navigation, quality-of-life improvements, and better interfaces while remaining
compatible with unmodified vanilla servers.

Server operators do not need to install anything. Every active packwiz record
uses `side = "client"`, and the exported pack marks every mod as required on the
client and unsupported on the server. Selected functionality must work entirely
from the client using vanilla server data. The [mod audit](docs/mod-audit.md)
documents that decision for all 41 selected features. Static checks enforce the
packaging contract. A clean-client vanilla-server join still needs
[runtime acceptance](docs/acceptance-tests.md).

The target is Minecraft **26.2**, Fabric Loader **0.20.1**, and Java **25**.
The loader pin comes from Fabric's [26.2 compatibility
API](https://meta.fabricmc.net/v2/versions/loader/26.2), checked on 2026-11-17.
The checked evidence is in [upstream-metadata.json](docs/upstream-metadata.json).
Pack version `26.2.0.10.0` is a development baseline, not a runtime qualification.

## Version branches and feature freeze

[`26.2`](https://github.com/jabez007/lantern-crossing/tree/26.2) is the authoritative
baseline. Feature selection is frozen at 41 Fabric feature mods, eleven libraries
and two optional shader choices pending owner runtime acceptance and release
qualification. Follow-up work addresses bugs, compatibility, privacy/security,
dependencies, incorrect configuration, documentation, tests and acceptance findings.
Speculative feature additions wait until after the qualified 26.2 release.

[`26.3`](https://github.com/jabez007/lantern-crossing/tree/26.3) is a future forward
migration target, not a parallel release baseline. GitHub's default branch remains
26.3 at the owner's request; explicitly check out 26.2 for current work. The
older 26.3 bootstrap still targets Minecraft 26.2 with 30 features. It is not
qualified and receives no automatic synchronization or shader additions here.

After accepting and releasing 26.2, start migration from its accepted inventory.
Reevaluate every mod, shader and dependency for 26.3, resolve blockers, rerun
static/reproducibility checks and complete separate runtime qualification.
The earlier application of shared changes to 26.3 was forward preparation.
The [branch policy](docs/version-policy.md#version-branches) replaces the earlier
incorrect terminology. `pack.toml` always records the actual Minecraft target.

## Pack philosophy

[Fabulously Optimized](https://modrinth.com/modpack/fabulously-optimized) is the
reference for performance and visual conveniences.
Lantern Crossing combines those priorities with a pinned QoL selection and
documented defaults, so a new Prism Launcher instance starts with the tools you
normally add by hand. Two optional shaders are available through the existing Iris interface.

Lantern Crossing keeps vanilla progression, content, and server mechanics.
It supplies no blocks, items, mobs, dimensions, recipes, gameplay data packs,
server companions or standalone resource packs. Shaders are optional local visuals. Continuity's two
built-in visual packs are seeded when their options entry is absent. Upstream
defaults otherwise apply except for the documented [configuration and keybinding overrides](docs/configuration.md).

## Active selections

All 30 original features, Renice Shot, five FO-inspired additions, Configured Defaults,
three QoL refinements and Enchantment Descriptions are active: 41 intentional
Fabric mod features plus eleven libraries and two separate shader choices in
[collection.toml](collection.toml).

| Category | Selected projects |
| --- | --- |
| Performance | Sodium, Lithium, FerriteCore, ImmediatelyFast, Entity Culling, More Culling, BadOptimizations, Dynamic FPS, FastQuit, Debugify, Language Reload |
| Inventory | Inventory Profiles Next, Mouse Tweaks, Shulker Box Tooltip, Client Tweaks |
| HUD and information | Status Effect Bars, Light Overlay, BetterF3, Better Mount HUD, Paginated Advancements, Better Statistics Screen, Food Effect Tooltips, Enchantment Descriptions |
| Navigation | Xaero's Minimap, Xaero's World Map, Zoomify |
| Writing | Sign Tweaks, Book Tweaks |
| Visual and social | LambDynamicLights, Chat Heads, Iris, Renice Shot, Sodium Extra, Continuity, More Chat History, BetterGrassify |
| Interface and windows | Reese's Sodium Options, Cubes Without Borders, Controlling |
| Pack management | Mod Menu, Configured Defaults |

All 30 originally requested features remain active. New candidates and blockers
are documented in the refinement audit. Light Overlay uses the current
`lightoverlay` project, Modrinth ID `8qVa1XCN`; the audit records the identity
correction that completes this baseline.
Lantern Crossing selects release-designated feature versions. Upstream-declared
dependency closure may contain prerelease-versioned libraries when those exact
versions are required or bundled by the selected release. This does not permit
independently choosing arbitrary prerelease dependencies. See the
[audit](docs/mod-audit.md) for the exact provenance, including Mod Menu's
Placeholder API dependency and the libraries bundled with Iris and Client Tweaks.

Fabric API is an explicitly selected platform library. Cloth Config API,
Fabric Language Kotlin, libIPN, TCDCommons API, YACL, Balm, Text Placeholder API, OverlayLib, Searchables, and Prickle
are transitive dependencies. Libraries are separate from feature intent, and bundled libraries
remain inside upstream artifacts. The machine lock layer is `mods/*.pw.toml`.
It owns exact version IDs, URLs, and SHA-512 hashes. No mod JARs belong in Git.

BetterGrassify adds restrained terrain visuals, Controlling makes key conflicts
searchable, and Food Effect Tooltips explains vanilla item effects and their
probabilities. It does not display current player saturation or exhaustion.
Enchantment Descriptions adds shift-gated vanilla enchantment explanations. Its
Prickle dependency has an [exact environment classification audit](docs/mod-audit.md#prickle-environment-classification-review);
no server companion is required. Crash Assistant, BBE, Tooltip Tweaks, Ixeris and
ModernFix-mVUS remain inactive for the reasons in the
[refinement evaluation](docs/mod-audit.md#qol-and-performance-refinement-2026-11-19).
FO is a reference for performance decisions; these additions make no universal
FPS claim and do not imply FO endorsement.

Renice Shot remains the only screenshot mod: F2 takes normal captures, F9 takes
4K PNGs, and Light Overlay receives F7 when no binding exists. Revisit images in
the instance's `screenshots` folder. Both gallery candidates remain inactive after
[source, memory and privacy review](docs/mod-audit.md#screenshot-experience-evaluation-2026-11-19).
No screenshot metadata or gallery migration is introduced. See the
[storage and sharing guidance](docs/configuration.md#screenshots).

## Optional shader choices

Both shader ZIPs download from official Modrinth versions into `shaderpacks/`.
They are installed choices, not automatically enabled effects. A new instance
without saved Iris preferences starts with shaders disabled. Existing Iris preferences and per-shader presets
are not supplied or replaced by the pack.

| Choice | Release | Intended use |
| --- | --- | --- |
| [Complementary Reimagined](https://modrinth.com/shader/complementary-reimagined) | r5.10, `RKfUB9VC` | Featured atmospheric visuals that retain Minecraft's visual style. Try an appropriate Low or Medium preset before raising quality. |
| [MakeUp - Ultra Fast](https://modrinth.com/shader/makeup-ultra-fast-shaders) | 9.6, `t4YRxQug` | Adjustable alternative with shadowless and lower-effect profiles. Its name is not a measured speed guarantee. |
| Shaders disabled | Existing Iris option | Preserve the optimized vanilla rendering baseline and avoid shader rendering costs. |

Open **Options > Video Settings > Shader Packs**, choose a ZIP, adjust its
**Shader Pack Settings**, and apply. Use Iris's shader toggle to disable shaders.
Menu labels can vary by language. No shader-specific preset or new keybind is
shipped. Rendering, frame times and GPU memory still need owner acceptance on
your hardware in both launchers. See the [configuration guide](docs/configuration.md#optional-shaders)
and [source/license audit](docs/mod-audit.md#optional-shaders-and-distribution-2026-11-19).

Credits: Complementary Reimagined by EminGT / [Complementary Development](https://www.complementary.dev/),
under the release's Complementary License Agreement 1.8. MakeUp - Ultra Fast by
Javier Garduño / [javiergcim](https://github.com/javiergcim/MakeUpUltraFast), under
[LGPL-3.0-or-later](https://www.gnu.org/licenses/lgpl-3.0.html) as designated upstream.
Lantern Crossing is responsible for problems arising from its shader integration.
Both official ZIPs and their internal licenses/notices remain unmodified. We
reference Modrinth downloads, do not upload shader ZIPs ourselves, and do not
relicense either shader under the repository's MIT license. Retain these credits
on any future distribution description page.

## Install an exported pack

1. Obtain a reviewed release, or build the development artifact below. Current
   development output is `lantern-crossing-26.2.0.10.0-dev-26.2.mrpack` with its
   matching `.sha256`. A development build still requires manual acceptance.
2. Verify the download with `sha256sum --check lantern-crossing-26.2.0.10.0-dev-26.2.sha256`.
3. Import the `.mrpack` into a launcher that supports Modrinth packs. Use a new
   instance with Java 25 and let the launcher obtain the pinned upstream files.
4. Start the client and complete the [smoke tests](docs/acceptance-tests.md),
   including joining a completely vanilla 26.2 server.

Configured Defaults copies absent mod config files and merges missing options
keys. Existing values, including resource-pack order and custom keybindings,
remain authoritative. Launcher-created partial options files can receive F7 and
Continuity defaults; an existing resource-pack list still requires deliberate
manual activation. Modrinth App sync can supply values before launch.
See the [candidate evaluation and upgrade instructions](docs/configuration.md#defaults-manager-evaluation-2026-11-19)
and [owner acceptance matrix](docs/acceptance-tests.md#launcher-configuration-acceptance-matrix).
Neither launcher has been runtime-qualified. When upgrading from 26.2.0.6.0,
remove its old Default Options mod before launching; preserve live preferences.

Do not merge this pack into an existing instance's mod directory. A clean
instance avoids leftover mods and configuration. Server rules may restrict
minimaps or inventory assistance even though they require no server mods.

## Build and validate

The scripts use Python 3.11 or newer and its standard library. Unit tests and
repository validation work offline. Export needs access to the pinned artifact URLs
unless packwiz's external download cache already contains them.

For a fresh source checkout, select the authoritative branch explicitly because
GitHub's default remains the future migration branch:

```sh
git clone --branch 26.2 https://github.com/jabez007/lantern-crossing.git
cd lantern-crossing
```

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
| `make validate` | Source policy, exact pins, native dependency predicates, migration inventory, branch identity, and index hashes |
| `make refresh` | Regenerate packwiz index after an intentional payload edit |
| `make export` | Validate, export, normalize, and validate the complete `.mrpack` |
| `make checksum` | Development export and SHA-256 checksum |
| `make release RELEASE_TAG=v26.2.0.10.0` | Release build, requiring owner-recorded runtime qualification |
| `make clean` | Remove generated `build/` and `dist/` files |

`PACKWIZ`, `PYTHON`, and `RUFF` can name explicit local executables.
Export checks the existing index before packwiz's implicit refresh, so it cannot
hide stale source metadata. ZIP normalization fixes entry order, timestamps,
permissions, and JSON encoding. Stored entries avoid compression-version drift.

Default development outputs are:

```text
dist/lantern-crossing-26.2.0.10.0-dev-26.2.mrpack
dist/lantern-crossing-26.2.0.10.0-dev-26.2.sha256
```

GitHub Actions validates pushes to `26.2` and `26.3` and pull requests targeting
either branch. It checks index consistency, builds twice to compare archive
bytes, and uploads artifacts labeled with their version, branch and channel.
The archive itself also identifies development builds. The 26.3 bootstrap exports
its actual **26.2** target with `-dev-26.3`, never as a 26.3-compatible release.

Release publication requires a matching tag on the declared version branch,
agreement with the actual Minecraft target, and an owner acceptance record bound
to the exact `pack.toml` hash in [release-policy.toml](release-policy.toml).
Those acceptance fields are unset. Once qualified, releases retain the existing
`lantern-crossing-<version>.mrpack` and `.sha256` names. Published releases cannot
be replaced. See [release eligibility](docs/version-policy.md#publish-a-release).

## Select and update deliberately

Version numbers follow `<Minecraft version>.<pack major>.<pack minor>.<pack patch>`.
The final three components identify the pack revision. Tags must match
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

The default checks active Fabric features/libraries and the two Iris shader
choices. The requested scope covers 41 mod features plus both shaders, excluding
libraries. Both scopes report release availability for this recorded baseline.
Discovery does not qualify a dependency closure, audit a pinned artifact, or
replace runtime testing.

Config Manager and the five deferred refinement candidates remain outside the
active pack. Their [evaluation results](docs/mod-audit.md#qol-and-performance-refinement-2026-11-19)
and promotion gates are recorded in [candidates.toml](candidates.toml).

## Repository structure and licensing

[Cobbled Horizon](https://github.com/vice-magus-faolan/cobbled-horizon/tree/7850a25ebae704d5d07a91ed0c89c1e9be9e9e19)
provided the architectural reference for collection intent, candidates,
validation, and release naming. Lantern Crossing implements a smaller client
workflow. It contains no server deployment or runtime management system.

Repository-authored scripts and documentation use the [MIT license](LICENSE).
That license does not relicense Minecraft, mods or shaders. Each upstream artifact
retains its own license. Packwiz references official downloads rather than
vendoring JARs or shader ZIPs. The `.mrpack` contains download references and the documented config.
