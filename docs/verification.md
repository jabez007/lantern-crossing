# Verification record

Verified on 2026-11-18 for pack `26.2.0.5.0`. This record covers source metadata,
upstream artifact inspection, and export behavior. Minecraft has not been launched.

## Defaults hardening, 2026-11-19

The 26.2.0.6.0 defaults slice passes 57 offline tests, lint, source validation,
refresh and complete export validation. The original 45 mod records are retained;
Default Options is the only new artifact. File and key-handling behavior was
inspected in its exact release source. No Minecraft client was launched.
Root options and direct mod overrides have been replaced with first-install or
copy-if-missing templates; runtime journals and server lists are forbidden.
The earlier verification record below describes the preceding 26.2.0.5.0 build.

## Tool versions

| Tool | Version and source |
| --- | --- |
| Python | 3.12.12 locally and in [CI](../.github/workflows/validate.yml). Scripts require 3.11+ for `tomllib`. |
| packwiz | Commit `170b22d785959dda5876b54b7f16e1b807a57fb6`, module `v0.0.0-20261014010756-170b22d78595` |
| Go | 1.24.6, matching the unchanged CI configuration. |
| Ruff | 0.16.4, pinned in [requirements-dev.txt](../requirements-dev.txt) |
| actionlint | 1.7.12, checksum-verified upstream release binary, used for local workflow validation |

Local build commands used `PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'`.
The compiler, audit downloads, and packwiz cache are outside the repository.

## Observed results

| Check | Result |
| --- | --- |
| Previous baseline | All 31 existing features remain active. All 40 previous lock records are byte-identical to commit `8deae0e`. This pass adds five intentional features and enables Continuity's two built-in packs. |
| Current upstream recheck | Passed. Sodium Extra, Reese's Sodium Options, Continuity, Cubes Without Borders, and More Chat History all have exact release-designated Fabric 26.2 pins. Their project metadata and native descriptors are client-only. Exact versions and IDs are in the mod audit. |
| Exact active artifacts | Passed. All five new downloads were SHA-512 verified and their root/bundled descriptors audited. All 45 exported downloads match their pins. Existing Sodium and Fabric API close the new requirements. No library download was added. |
| `make test` | Passed, 54 offline tests. No network dependency. |
| `make lint` | Passed, Ruff lint and formatting. Complexity threshold is 10 in [pyproject.toml](../pyproject.toml). Highest function score is 8 for `check_dependencies`. |
| `make validate` | Passed, 36 features, nine libraries, zero excluded features, exact Fabric 26.2 target, client sides, dependency provenance, closure, and index. Three staged candidates remain inactive. |
| `packwiz refresh` | Passed. A repeated refresh left `pack.toml` and `index.toml` byte-identical. |
| `make export` | Passed. Complete archive validation checked pins, project set, library closure, both hashes, sizes, environments, and config bytes. |
| Release checksum generation | Passed, `python3 scripts/release_metadata.py --checksum`. The archive was built with `make export`. |
| Repeated export comparison | Passed. The normalized `.mrpack` bytes matched exactly. Normalization idempotence and reordered-input behavior also pass unit tests. |
| SHA-256 verification | Passed, `sha256sum --check` reports the archive OK. |
| Offline readiness, requested scope | Passed for every requested feature using the corrected project identity. Availability discovery does not replace the dependency provenance audit. |
| Project identity regressions | Passed. Replacing the correct Light Overlay lock ID, or both collection and lock IDs, with the unrelated same-name project is rejected. The requested feature count is asserted once; the active set is compared with the authoritative requested IDs. |
| Exact OverlayLib dependency and rendering declarations | Passed. The exact upstream library version is enforced. Light Overlay and OverlayLib declare no conflicts against the selected Light Overlay/OverlayLib/Iris/Sodium stack. This does not establish runtime rendering compatibility. |
| Keybind audit | Passed statically. Renice Shot retains F9 and Light Overlay retains F7. Inspection of the five new artifacts found no F7/F9 actions. Runtime key loading remains a manual check. |
| GitHub Actions YAML and expressions | Passed, actionlint 1.7.12 including its shellcheck integration. |
| Hosted CI before this pass | Passed on `8deae0e`, [26.2 run 44454029117](https://github.com/jabez007/lantern-crossing/actions/runs/44454029117). Current hosted results are tracked in [GitHub Actions](https://github.com/jabez007/lantern-crossing/actions). |
| Minecraft launch and vanilla-server join | Not run. All [manual acceptance tests](acceptance-tests.md) remain open. |

Regression coverage rejects missing features and libraries, undeclared projects,
duplicates, target changes, non-client sides, staged leakage, rejected projects,
stale hashes, local JARs, server config, malformed exports, and unexpected archive
contents. The earlier policy regressions still pass: official prerelease-looking
dependencies and bundled components are allowed, while independently selected
feature prereleases and mandatory server dependencies remain forbidden.

The suite now also rejects directly selected alpha or beta features, a beta
selected platform library, unaudited or substituted dependency pins, manually
introduced dependency edges without an upstream requirement, mismatched upstream
version declarations, mandatory server dependencies, and server-only bundled
modules. Client Tweaks' two disabled
overlap switches are checked as source invariants.

The production validation model, `load_pack` interface, archive comparison,
Makefile, and CI are unchanged. Three new regressions cover the Sodium add-ons'
exact native coupling to the retained Sodium pin, the two selected built-in
resource packs, and rejection of investigated candidates from the archive's mod
list. The resource-pack default test failed before the selection was added and
passes afterward. Existing candidate-leak coverage now appends to the populated
candidate list instead of assuming an empty manifest.

No function exceeds the complexity limit of 10. Existing `payload_files` scores
4, and `check_dependencies` remains the maximum at 8. The Zoomify universal-build
NeoForge metadata exception is unchanged. Dependency provenance and strict
client-only enforcement have not been relaxed.

The 31 prior features plus five additions make 36 intentional features.
Eight resolved libraries plus explicitly selected Fabric API still make nine
libraries. Sodium Extra and Reese's Sodium Options both accept exactly
Sodium `0.9.2+mc26.2`; no existing mod or loader pin changed.

Config Manager, Ixeris, and ModernFix-mVUS were inspected as staged candidates.
Their audited release artifacts remain outside the repository and exports.
Config Manager's v2 environment metadata conflicts with its native/client
behavior, Ixeris still needs hardware measurements, and ModernFix needs further
exact-build/default overlap review and measurements. The [investigation record](mod-audit.md#staged-investigations)
and `candidates.toml` state each promotion gate. No runtime result is claimed.

The validator checks native Fabric module presence and explicit Modrinth version
IDs. It does not evaluate every Fabric version-range expression. Iris' exact
Sodium dependency remains intact. Light Overlay and OverlayLib both require
Fabric Loader `>=0.19.3` and Fabric API `>=0.152.1+26.2`; the existing pins are
0.20.1 and 0.161.0+26.2. Light Overlay's YACL requirement is
`>=3.9.4+26.2-fabric`, satisfied by the unchanged 3.9.7+26.2-fabric pin.
The general runtime compatibility check remains part of manual acceptance.

## Exported artifact

`dist/lantern-crossing-26.2.0.5.0.mrpack` contains 45 download records and four
overrides: `config/MouseTweaks.cfg`, `config/clienttweaks-common.toml`,
`config/iris.properties`, and `options.txt`, all under `overrides/`. Every record has
`client = "required"` and `server = "unsupported"`. No JAR, staged file,
server payload, or repository tooling is embedded.

The archive is 26,035 bytes. Its SHA-256 is:

```text
6949319dc9d8ec9b2de212916bc03ef2ca453eea4d83a5b36abf25ac8be23b8f
```

The companion checksum is
`dist/lantern-crossing-26.2.0.5.0.sha256`. Generated artifacts stay ignored by Git.

## Runtime acceptance remains open

Test a new imported instance on Java 25 and a completely vanilla 26.2 server.
Record the client and hardware environment and complete every applicable item
in [acceptance-tests.md](acceptance-tests.md). Test startup, reconnect, culling
and lighting, inventory gestures, HUDs, maps, book editing, chat heads, and
resource behavior. Test Mod Menu's mod list and configuration screens, Sign
Tweaks' multiline editing and server acceptance, Iris with shaders disabled and
its shader-selection UI, and Client Tweaks' configured features and disabled
overlaps. Test the new graphics pages, connected textures, local chat scrollback,
borderless fullscreen, and focus behavior. Test Light Overlay's F7 toggle,
config persistence, vanilla-server use, and rendering with Sodium, Iris, and
LambDynamicLights. Test F9 screenshot capture, F2 preservation, PNG dimensions,
and resolution/HUD restoration with Renice Shot. An optional known-good shader
pack test belongs in a separate profile and is not bundled here.

The client-only packaging policy is enforced statically. Successful runtime
operation and performance on particular hardware remain unverified.
