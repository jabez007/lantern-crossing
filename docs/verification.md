# Verification record

Configuration evaluation completed on 2026-11-19 for development pack
`26.2.0.7.0`, Minecraft 26.2, Fabric Loader 0.20.1 and Java 25.
Minecraft and both launchers have not been run. Runtime acceptance remains open.
Previous hardening/evaluation evidence remains in Git history at `4938e86`.

## Decision and provenance

The [three-candidate evaluation](configuration.md#defaults-manager-evaluation-2026-11-19)
selects Configured Defaults. It safely fills missing fields in launcher-created
partial options files, including the case supported by Modrinth App's current
pre-launch source. Existing values remain authoritative. Neither automatic
activation over a pre-existing resource-pack choice nor a pack-defined native
Controls reset is claimed.

The only artifact replacement is Default Options (`WEg59z5b`, `hS9ZtUOA`) with
Configured Defaults (`SISoSFPP`, `oM0C4RRZ`), release-designated Fabric 26.2 version
26.2.0. The [lock](../mods/configured-defaults.pw.toml) pins its exact URL and
SHA-512 `a8d3274943c67145722c1afe26ad39ba127ef2195c86f17bf4ade40205e571f0efae1db51368e83c31d88c9dafb22a4ff8846ff2e8969c3adbb4781989e78c4c`.
No required library projects or bundled JARs are introduced. All 45 other locks
are byte-identical to `4938e86`; Balm remains required by Client Tweaks. Fabric
API and Balm reverse edges no longer include the removed manager.

The three mod-config templates are byte-identical, now under
`configureddefaults/config/`. Resource-pack and F7 entries share the new options
template. Its data version 4903 was read from `version.json` in the official
SHA-1-verified client ZIP. No Minecraft code was executed. That provenance is in
the upstream snapshot. Root live preferences, obsolete managers/trees, journals,
reset flags and arbitrary template locations are rejected by validation.

## Observed automated results

Python 3.12.12, Ruff 0.16.4, Go 1.24.6, and packwiz commit
`170b22d785959dda5876b54b7f16e1b807a57fb6` match CI. Actionlint is 1.7.12.
Audit downloads and temporary compiler tools remain outside the repository.

| Check | Result |
| --- | --- |
| `make test lint validate` | Passed, 94 offline tests. Includes configuration policy, exact pins/closure, Fabric predicates, strict client-only rules, branch/release eligibility and index. |
| `make refresh` | Passed; subsequent export/refresh caused no further pack/index drift. |
| `make checksum`, second `make export`, archive `cmp` | Passed, complete archive validation and byte-identical normalized builds. |
| `sha256sum --check` | Passed for the generated checksum. |
| Actionlint with shellcheck | Passed; CI workflow and release gates are unchanged. |
| Ruff with complexity threshold 8 | Passed; configured maximum remains 10. |
| Prior pin/template byte comparison | Passed for 45 retained locks and all three mod-config templates. |
| Java file-handler oracle | Seven cases passed using unmodified upstream `CopyDefaultsHandler`, with only its logging/constants holder stubbed. No Fabric, Minecraft or launcher execution. |
| Committed JAR scan | Empty. Only metadata, templates, scripts, fixture data and source adapter are committed. |

Commands used for build validation:

```sh
make test lint validate
make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cmp /tmp/lantern-config-evaluation/configured-first.mrpack dist/lantern-crossing-26.2.0.7.0-dev-26.2.mrpack
(cd dist && sha256sum --check lantern-crossing-26.2.0.7.0-dev-26.2.sha256)
/tmp/lantern-bin/actionlint .github/workflows/validate.yml
ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'
git ls-files '*.jar' '*.JAR'
```

The first export encountered a sandbox-blocked uncached download and the archive
validator rejected the incomplete result. Retrying with network access populated
the external cache and passed complete validation. No check was relaxed.

Regression coverage includes missing dependency versions, server-required
artifacts, exact provenance, staged leakage, duplicate projects, competing
managers, old templates, root preferences, reset flags and archive content/identity.
The option-format regression checks the audited data version and normal F7 key
serialization. Recorded file cases cover absent/partial/custom options, repeat
launch, newly introduced options/files, custom resource packs, and a previous
manager's leftover files followed by deliberate per-file adoption. They are
pinned source observations, not a Python approximation or runtime acceptance.

The native predicate checker remains a conservative partial evaluator following
Fabric Loader 0.20.1, including its 51 offline conformance vectors. Unsupported
expressions and ambiguous bundled resolution fail explicitly. It does not
implement Loader's complete SAT resolver or prove behavior on a particular JVM.
See [version policy](version-policy.md#native-fabric-requirements).

## Artifact and release state

`dist/lantern-crossing-26.2.0.7.0-dev-26.2.mrpack` is 26,887 bytes: 46 pinned client
mod downloads and four templates under `overrides/configureddefaults/`. Every
mod is client-required and server-unsupported. It contains no root live settings,
staged data, JARs or server payload. SHA-256:

```text
fea1539fea89894596f754e33ff341d595a988204c9430f5f8a6de98d2204a2d
```

The 26.2 line has 37 features and nine libraries. No runtime acceptance is
recorded. Publication still requires a matching tag, version branch/actual-target
agreement, remote ancestry and owner evidence bound to the exact pack hash.
No tag or release is created by this work.

The 26.3 branch still targets actual Minecraft 26.2 at pack 26.2.0.3.0 with the
original 30 features and nine libraries. It receives shared checks/documentation
and updated migration intent, not Configured Defaults or a 26.3 upgrade. Its
migration entries remain deferred/runtime pending. Discovery of a 26.3 release
is not a compatibility audit.

## Owner handoff — all runtime results uncompleted

Complete the [launcher matrix](acceptance-tests.md#launcher-configuration-acceptance-matrix)
in Prism and Modrinth App with sync disabled/enabled where available. Verify
fresh/partial options, F7, Continuity, custom preferences, repeat launches,
actual upgrades, old-manager removal and deliberate adoption. Record launcher
versions, sync choices, upgrade path and exact archive hash. No automatic update
UI is promised for a local unlinked `.mrpack` import.

Then complete client initialization, vanilla-server join/reconnect, rendering
and inventory smoke tests. No server installation is required by the selected
functionality, but successful operation remains for the owner to verify.
