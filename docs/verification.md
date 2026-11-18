# Verification record

Verified on 2026-11-17 for pack `26.2.0.3.0`. This record covers source metadata,
upstream artifact inspection, and export behavior. Minecraft has not been launched.

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
| Previous remediation verification | Passed before adding Light Overlay. All four promoted projects are active release-designated Fabric 26.2 features with client-only records. The 29-feature source, index, 37-download archive, and all 44 existing tests passed. |
| Current upstream recheck | Passed. Project `8qVa1XCN`, slug `lightoverlay`, still publishes release `AT01Q5uN` for Fabric 26.2. The API's newer 26.3 artifacts were excluded from selection. |
| Exact active artifacts | Passed. The new Light Overlay and OverlayLib artifacts were hash-verified and audited. All 39 exported downloads match their pins. All 37 pre-existing mod records remain byte-identical. |
| `make test` | Passed, 48 offline tests. No network dependency. |
| `make lint` | Passed, Ruff lint and formatting. Complexity threshold is 10 in [pyproject.toml](../pyproject.toml). Highest function score is 8 for `check_dependencies`. |
| `make validate` | Passed, all 30 requested features, nine libraries, zero exclusions, exact Fabric 26.2 target, client sides, dependency provenance, closure, and index. |
| `packwiz refresh` | Passed. A repeated refresh left `pack.toml` and `index.toml` byte-identical. |
| `make export` | Passed. Complete archive validation checked pins, project set, library closure, both hashes, sizes, environments, and config bytes. |
| Release checksum generation | Passed, `python3 scripts/release_metadata.py --checksum`. The archive was built with `make export`. |
| Repeated export comparison | Passed. The normalized `.mrpack` bytes matched exactly. Normalization idempotence and reordered-input behavior also pass unit tests. |
| SHA-256 verification | Passed, `sha256sum --check` reports the archive OK. |
| Offline readiness, requested scope | Passed for every requested feature using the corrected project identity. Availability discovery does not replace the dependency provenance audit. |
| Project identity regressions | Passed. Replacing the correct Light Overlay lock ID, or both collection and lock IDs, with the unrelated same-name project is rejected. The requested feature count is asserted once; the active set is compared with the authoritative requested IDs. |
| Exact OverlayLib dependency and rendering declarations | Passed. The exact upstream library version is enforced. Light Overlay and OverlayLib declare no conflicts against the selected Light Overlay/OverlayLib/Iris/Sodium stack. This does not establish runtime rendering compatibility. |
| Keybind audit | Passed statically. Release source binds toggle to F9 and leaves config/mode-cycle keys unbound. Inspection of pinned artifacts found no competing default F9 action. No override was added. |
| GitHub Actions YAML and expressions | Passed, actionlint 1.7.12 including its shellcheck integration. |
| Hosted CI before this pass | Passed on commit `7136469`, [run 44234556018](https://github.com/jabez007/lantern-crossing/actions/runs/44234556018). The unchanged workflow's local validation, refresh consistency, export, and reproducibility steps also pass for this baseline. Hosted results are tracked in [GitHub Actions](https://github.com/jabez007/lantern-crossing/actions). |
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

The production validation model, `load_pack` interface, CI, and build architecture
are unchanged. The updated repository-contract test failed while the newly
installed Light Overlay ID was still absent from collection intent, and passes
after reconciliation. Two new same-name identity regressions exercise the
existing project-ID checks. Two more tests cover the exact OverlayLib pin and
absence of newly declared conflicts in the selected rendering stack.
No function exceeds the complexity limit. The one recorded loader-specific upstream
metadata exception is Zoomify's universal NeoForge dependency declaration.
Remove that exception if upstream corrects the exact version's metadata, and
recheck the Fabric closure before updating the pin.

This pass completes the baseline with all 30 intentional features and no blocked
features. The sole new resolved project is OverlayLib `0.12.0+26.2` (`OQkmYeS8`),
required exactly by Light Overlay `2.12.0+26.2` (`AT01Q5uN`). Eight resolved
libraries plus explicitly selected Fabric API make nine libraries. The previous
prerelease-dependency policy and its exact provenance records are preserved.
The incorrect similarly named Modrinth project has been removed from collection
intent and the snapshot. The [audit](mod-audit.md#light-overlay-identity-correction)
explains the identity correction.

The validator checks native Fabric module presence and explicit Modrinth version
IDs. It does not evaluate every Fabric version-range expression. Iris' exact
Sodium dependency remains intact. Light Overlay and OverlayLib both require
Fabric Loader `>=0.19.3` and Fabric API `>=0.152.1+26.2`; the existing pins are
0.20.1 and 0.161.0+26.2. Light Overlay's YACL requirement is
`>=3.9.4+26.2-fabric`, satisfied by the unchanged 3.9.7+26.2-fabric pin.
The general runtime compatibility check remains part of manual acceptance.

## Exported artifact

`dist/lantern-crossing-26.2.0.3.0.mrpack` contains 39 download records and three
overrides: `config/MouseTweaks.cfg`, `config/clienttweaks-common.toml`, and
`config/iris.properties`, all under `overrides/`. Every record has
`client = "required"` and `server = "unsupported"`. No JAR, staged file,
server payload, or repository tooling is embedded.

The archive is 22,542 bytes. Its SHA-256 is:

```text
1fb8d91acca8ec7b056ab9c18a157d80d981a21bb3283bdf2f365994cf294cdd
```

The companion checksum is
`dist/lantern-crossing-26.2.0.3.0.sha256`. Generated artifacts stay ignored by Git.

## Runtime acceptance remains open

Test a new imported instance on Java 25 and a completely vanilla 26.2 server.
Record the client and hardware environment and complete every applicable item
in [acceptance-tests.md](acceptance-tests.md). Test startup, reconnect, culling
and lighting, inventory gestures, HUDs, maps, book editing, chat heads, and
resource behavior. Test Mod Menu's mod list and configuration screens, Sign
Tweaks' multiline editing and server acceptance, Iris with shaders disabled and
its shader-selection UI, and Client Tweaks' configured features and disabled
overlaps. Test Light Overlay's F9 toggle, config persistence, vanilla-server use,
and rendering with Sodium, Iris, and LambDynamicLights. An optional known-good
shader pack test belongs in a separate profile and is not bundled here.

The client-only packaging policy is enforced statically. Successful runtime
operation and performance on particular hardware remain unverified.
