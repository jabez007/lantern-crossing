# Verification record

Verified on 2026-11-17 for pack `26.2.0.2.0`. This record covers source metadata,
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
| Current upstream recheck | Passed for the four promoted releases and their two new libraries. Light Overlay still has no Fabric 26.2 artifact. The original audit remains recorded for all 30 requested features. |
| Exact active artifacts | Passed. All 37 downloads match their pins. The six added artifacts were hash-verified and their Fabric descriptors and bundled modules audited. All 31 pre-existing lock files remain byte-identical. |
| `make test` | Passed, 44 offline tests. No network dependency. |
| `make lint` | Passed, Ruff lint and formatting. Complexity threshold is 10 in [pyproject.toml](../pyproject.toml). Highest function score is 8 for `check_dependencies`. |
| `make validate` | Passed, 29 features and eight libraries, exact Fabric 26.2 target, client sides, dependency provenance, closure, and index. |
| `packwiz refresh` | Passed. A repeated refresh left `pack.toml` and `index.toml` byte-identical. |
| `make export` | Passed. Complete archive validation checked pins, project set, library closure, both hashes, sizes, environments, and config bytes. |
| Release checksum generation | Passed, `python3 scripts/release_metadata.py --checksum`. The archive was built with `make export`. |
| Repeated export comparison | Passed. The normalized `.mrpack` bytes matched exactly. Normalization idempotence and reordered-input behavior also pass unit tests. |
| SHA-256 verification | Passed, `sha256sum --check` reports the archive OK. |
| Offline readiness, active scope | Passed for all 37 projects using the dated snapshot. Availability discovery does not replace the dependency provenance audit. |
| Offline readiness, requested scope | Expected nonzero result. Light Overlay is the only unavailable requested feature. |
| GitHub Actions YAML and expressions | Passed, actionlint 1.7.12 including its shellcheck integration. |
| Hosted GitHub Actions for this remediation | Not run. The unchanged workflow's local validation, refresh consistency, export, and reproducibility checks pass. No release was published. |
| Minecraft launch and vanilla-server join | Not run. All [manual acceptance tests](acceptance-tests.md) remain open. |

Regression coverage rejects missing features and libraries, undeclared projects,
duplicates, target changes, non-client sides, staged leakage, rejected projects,
stale hashes, local JARs, server config, malformed exports, and unexpected archive
contents. The policy regressions first failed against the old implementation:
it rejected both a release containing a bundled `pre3` library and an official,
exactly audited prerelease dependency. Both cases pass after the correction.

The suite now also rejects directly selected alpha or beta features, a beta
selected platform library, unaudited or substituted dependency pins, manually
introduced dependency edges without an upstream requirement, mismatched upstream
version declarations, mandatory server dependencies, and server-only bundled
modules. Client Tweaks' two disabled
overlap switches are checked as source invariants.

The `load_pack` interface and existing build architecture are unchanged.
No function exceeds the complexity limit. The one recorded loader-specific upstream
metadata exception is Zoomify's universal NeoForge dependency declaration.
Remove that exception if upstream corrects the exact version's metadata, and
recheck the Fabric closure before updating the pin.

This pass restores four upstream release-designated features, taking the active
baseline from 25 to 29 of 30. Resolved libraries grow from five to seven, plus
explicitly selected Fabric API. The new libraries are Balm and Text Placeholder
API. The Placeholder API edge records Mod Menu's exact release, required-project
declaration, audited version ID, and release-tagged build properties. Bundled
library identifiers are allowed under their containing release's hash pin.
Mandatory server requirements remain forbidden.

The validator checks native Fabric module presence and explicit Modrinth version
IDs. It does not evaluate every Fabric version-range expression. Iris' exact
Sodium dependency and relevant native constraints were inspected in this audit;
the general runtime compatibility check remains part of manual acceptance.

## Exported artifact

`dist/lantern-crossing-26.2.0.2.0.mrpack` contains 37 download records and three
overrides: `config/MouseTweaks.cfg`, `config/clienttweaks-common.toml`, and
`config/iris.properties`, all under `overrides/`. Every record has
`client = "required"` and `server = "unsupported"`. No JAR, staged file,
server payload, or repository tooling is embedded.

The archive is 21,467 bytes. Its SHA-256 is:

```text
52c46e67ab600d5f0d228447a44857ff7d46f761005be28a274a4dbb7f50ec39
```

The companion checksum is
`dist/lantern-crossing-26.2.0.2.0.sha256`. Generated artifacts stay ignored by Git.

## Runtime acceptance remains open

Test a new imported instance on Java 25 and a completely vanilla 26.2 server.
Record the client and hardware environment and complete every applicable item
in [acceptance-tests.md](acceptance-tests.md). Test startup, reconnect, culling
and lighting, inventory gestures, HUDs, maps, book editing, chat heads, and
resource behavior. Test Mod Menu's mod list and configuration screens, Sign
Tweaks' multiline editing and server acceptance, Iris with shaders disabled and
its shader-selection UI, and Client Tweaks' configured features and disabled
overlaps. Light Overlay remains the only blocked requested feature.

The client-only packaging policy is enforced statically. Successful runtime
operation and performance on particular hardware remain unverified.
