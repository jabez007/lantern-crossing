# Verification record

Verified on 2026-11-18 for pack `26.2.0.4.0`. This record covers source metadata,
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
| Previous baseline | All 30 original features remain active. All 39 previous lock records are byte-identical to commit `3ed86e5`. This pass adds only Renice Shot and its documented keybinding override. |
| Current upstream recheck | Passed. Renice Shot `ZDCwiIc3` publishes release `roOTvshj`, version `1.2.1+mc26.2`, for Fabric 26.2. The exact artifact declares Minecraft 26.2, client environment, Java 25, and Fabric Loader >=0.19.5. |
| Exact active artifacts | Passed. The new Renice Shot artifact was SHA-512 verified and its native descriptor audited. All 40 exported downloads match their pins. Existing Fabric API satisfies its only required project dependency; optional Mod Menu and Cloth Config are already present. |
| `make test` | Passed, 51 offline tests. No network dependency. |
| `make lint` | Passed, Ruff lint and formatting. Complexity threshold is 10 in [pyproject.toml](../pyproject.toml). Highest function score is 8 for `check_dependencies`. |
| `make validate` | Passed, 31 features, nine libraries, zero exclusions, exact Fabric 26.2 target, client sides, dependency provenance, closure, and index. |
| `packwiz refresh` | Passed. A repeated refresh left `pack.toml` and `index.toml` byte-identical. |
| `make export` | Passed. Complete archive validation checked pins, project set, library closure, both hashes, sizes, environments, and config bytes. |
| Release checksum generation | Passed, `python3 scripts/release_metadata.py --checksum`. The archive was built with `make export`. |
| Repeated export comparison | Passed. The normalized `.mrpack` bytes matched exactly. Normalization idempotence and reordered-input behavior also pass unit tests. |
| SHA-256 verification | Passed, `sha256sum --check` reports the archive OK. |
| Offline readiness, requested scope | Passed for every requested feature using the corrected project identity. Availability discovery does not replace the dependency provenance audit. |
| Project identity regressions | Passed. Replacing the correct Light Overlay lock ID, or both collection and lock IDs, with the unrelated same-name project is rejected. The requested feature count is asserted once; the active set is compared with the authoritative requested IDs. |
| Exact OverlayLib dependency and rendering declarations | Passed. The exact upstream library version is enforced. Light Overlay and OverlayLib declare no conflicts against the selected Light Overlay/OverlayLib/Iris/Sodium stack. This does not establish runtime rendering compatibility. |
| Keybind audit | Passed statically. Renice Shot retains F9. The one-line `options.txt` moves Light Overlay to F7; inspection found no competing default F7 action. Runtime key loading remains a manual check. |
| GitHub Actions YAML and expressions | Passed, actionlint 1.7.12 including its shellcheck integration. |
| Hosted CI before this pass | Passed on `3ed86e5`, [26.2 run 44452238618](https://github.com/jabez007/lantern-crossing/actions/runs/44452238618). Current hosted results are tracked in [GitHub Actions](https://github.com/jabez007/lantern-crossing/actions). |
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

The `load_pack` interface and archive comparison remain intact. The existing
payload collector now includes the explicitly allowed root `options.txt` in its
override mapping. Packwiz indexing and exact archive-byte validation cover it
through the same path as the existing mod configs. Symlink rejection applies to
the new file. The new payload and symlink tests failed before that support was
added and pass afterward; a third regression rejects stale keybinding hashes.
The archive's missing-feature regression also removes Renice Shot explicitly.

No function exceeds the complexity limit. `payload_files` now scores 4 and
`check_dependencies` remains the maximum at 8. The Zoomify universal-build
NeoForge metadata exception is unchanged. Dependency provenance and strict
client-only enforcement have not been relaxed.

All 30 original features plus Renice Shot make 31 intentional features, with no
blocked features. Eight resolved libraries plus explicitly selected Fabric API
still make nine libraries. Renice Shot requires only that existing platform
library, and no other library or feature was introduced.

The validator checks native Fabric module presence and explicit Modrinth version
IDs. It does not evaluate every Fabric version-range expression. Iris' exact
Sodium dependency remains intact. Light Overlay and OverlayLib both require
Fabric Loader `>=0.19.3` and Fabric API `>=0.152.1+26.2`; the existing pins are
0.20.1 and 0.161.0+26.2. Light Overlay's YACL requirement is
`>=3.9.4+26.2-fabric`, satisfied by the unchanged 3.9.7+26.2-fabric pin.
The general runtime compatibility check remains part of manual acceptance.

## Exported artifact

`dist/lantern-crossing-26.2.0.4.0.mrpack` contains 40 download records and four
overrides: `config/MouseTweaks.cfg`, `config/clienttweaks-common.toml`,
`config/iris.properties`, and `options.txt`, all under `overrides/`. Every record has
`client = "required"` and `server = "unsupported"`. No JAR, staged file,
server payload, or repository tooling is embedded.

The archive is 23,243 bytes. Its SHA-256 is:

```text
b28f2a35797fa71a5aa98709a2036d1501a405932cf72d4cf171de64c1adf70d
```

The companion checksum is
`dist/lantern-crossing-26.2.0.4.0.sha256`. Generated artifacts stay ignored by Git.

## Runtime acceptance remains open

Test a new imported instance on Java 25 and a completely vanilla 26.2 server.
Record the client and hardware environment and complete every applicable item
in [acceptance-tests.md](acceptance-tests.md). Test startup, reconnect, culling
and lighting, inventory gestures, HUDs, maps, book editing, chat heads, and
resource behavior. Test Mod Menu's mod list and configuration screens, Sign
Tweaks' multiline editing and server acceptance, Iris with shaders disabled and
its shader-selection UI, and Client Tweaks' configured features and disabled
overlaps. Test Light Overlay's F7 toggle, config persistence, vanilla-server use,
and rendering with Sodium, Iris, and LambDynamicLights. Test F9 screenshot capture, F2 preservation, PNG dimensions, and resolution/HUD
restoration with Renice Shot. An optional known-good
shader pack test belongs in a separate profile and is not bundled here.

The client-only packaging policy is enforced statically. Successful runtime
operation and performance on particular hardware remain unverified.
