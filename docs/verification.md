# Verification record

Verified on 2026-11-17 for pack `26.2.0.1.0`. This record covers source metadata,
upstream artifact inspection, and export behavior. Minecraft has not been launched.

## Tool versions

| Tool | Version and source |
| --- | --- |
| Python | 3.12.12 locally and in [CI](../.github/workflows/validate.yml). Scripts require 3.11+ for `tomllib`. |
| packwiz | Commit `170b22d785959dda5876b54b7f16e1b807a57fb6`, module `v0.0.0-20261014010756-170b22d78595` |
| Go | Final packwiz build uses 1.24.6, matching CI. An earlier build used 1.24.4 and produced the same normalized archive. |
| Ruff | 0.16.4, pinned in [requirements-dev.txt](../requirements-dev.txt) |
| actionlint | 1.7.12, checksum-verified upstream release binary, used for local workflow validation |

Local build commands used `PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'`.
The compiler, audit downloads, and packwiz cache are outside the repository.

## Observed results

| Check | Result |
| --- | --- |
| All 30 requested project lookups and individual client-only audit | Passed. Evidence and decisions are in [mod-audit.md](mod-audit.md). |
| Exact active artifacts | Passed. All 31 downloads matched their pinned SHA-512. Fabric descriptors and recursive bundled module versions were inspected. |
| `make test` | Passed, 33 offline tests. No network dependency. |
| `make lint` | Passed, Ruff lint and formatting. Complexity threshold is 10 in [pyproject.toml](../pyproject.toml). Highest function score is 8 for `check_dependencies`. |
| `make validate` | Passed, 25 features and six libraries, exact Fabric 26.2 target, client sides, closure, and index. |
| `packwiz refresh` | Passed. A repeated refresh left `pack.toml` and `index.toml` byte-identical. |
| `make export` | Passed. Complete archive validation checked pins, project set, library closure, both hashes, sizes, environments, and config bytes. |
| `make release` | Passed, archive and SHA-256 file produced. |
| Repeated export comparison | Passed. The normalized `.mrpack` bytes matched exactly. Normalization idempotence and reordered-input behavior also pass unit tests. |
| SHA-256 verification | Passed, `sha256sum --check` reports the archive OK. |
| Live readiness, active scope | Passed, all 31 projects have release-designated Fabric 26.2 builds. |
| Live readiness, requested scope | Expected nonzero result. Light Overlay has no Fabric 26.2 artifact. Available parent builds do not override the other four exclusions. |
| Offline readiness | Passed for active scope using the dated snapshot. |
| GitHub Actions YAML and expressions | Passed, actionlint 1.7.12 including its shellcheck integration. |
| Hosted GitHub Actions run and release publication | Not run locally. The workflow is configured for pushes, pull requests, and matching release tags. |
| Minecraft launch and vanilla-server join | Not run. All [manual acceptance tests](acceptance-tests.md) remain open. |

Regression coverage rejects missing features and libraries, undeclared projects,
duplicates, target changes, non-client sides, staged leakage, rejected projects,
stale hashes, local JARs, server config, malformed exports, and unexpected archive
contents. During implementation, the valid-source test failed on directory
handling before that validator defect was corrected. The final suite passes.

There were no pre-existing functions or unrelated source files in this new
workspace. No function exceeds the complexity limit. The one recorded upstream
metadata exception is Zoomify's universal NeoForge dependency declaration.
Remove that exception if upstream corrects the exact version's metadata, and
recheck the Fabric closure before updating the pin.

## Exported artifact

`dist/lantern-crossing-26.2.0.1.0.mrpack` contains 31 download records and one
override, `overrides/config/MouseTweaks.cfg`. Every record has
`client = "required"` and `server = "unsupported"`. No JAR, staged file,
server payload, or repository tooling is embedded.

The archive is 17,611 bytes. Its SHA-256 is:

```text
93aeb09a531c971b25b8e977887bd8cb9631cb03d77730b0db8f4aceb1db8868
```

The companion checksum is
`dist/lantern-crossing-26.2.0.1.0.sha256`. Generated artifacts stay ignored by Git.

## Runtime acceptance remains open

Test a new imported instance on Java 25 and a completely vanilla 26.2 server.
Record the client and hardware environment and complete every applicable item
in [acceptance-tests.md](acceptance-tests.md). Test startup, reconnect, culling
and lighting, inventory gestures, HUDs, maps, book editing, chat heads, and
resource behavior. Light Overlay, Client Tweaks, Sign Tweaks, Iris, and Mod Menu
remain excluded and have explicit promotion gates.

The client-only packaging policy is enforced statically. Successful runtime
operation and performance on particular hardware remain unverified.
