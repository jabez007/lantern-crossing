# Verification record

The Prickle environment review completed on 2026-11-19 for development pack
`26.2.0.9.0`, Minecraft 26.2, Fabric Loader 0.20.1 and Java 25. No Minecraft,
Prism Launcher or Modrinth App runtime acceptance was performed. All owner
results remain uncompleted. Prior refinement evidence is in Git at `59373ad`.

## Verdict and artifact correspondence

The original Enchantment Descriptions deferral was overly conservative. An
isolated invocation of the original `check_mod()` accepted Enchantment
Descriptions but rejected Prickle because the project API says server required.
The pair passed the native dependency identities, ranges and hard-break checks
against the maintained baseline. No companion-server, extra server-data or
runtime incompatibility was demonstrated by that original rejection.

The [exact review](mod-audit.md#prickle-environment-classification-review) supports
independent client use for Enchantment Descriptions `PTAK0HD2`, version 26.2.0.2,
and Prickle `XdvtdRYJ`, version 26.2.0.3. Both remain pinned through packwiz.
The two Modrinth binaries match the published Maven binaries byte-for-byte.
All 36 Prickle and seven Enchantment Descriptions Java files in their versioned
Maven sources match the immutable Git revisions. All 25 enchantment language
maps match semantically. `javap -p -c -verbose` inspected every published class,
including private methods and constant-pool references, without executing mod
classes. This is release correspondence, not a signed/reproducible upstream
build attestation or Minecraft runtime qualification.

Prickle has no server-only mixins, Minecraft packet registrations, server hooks
or companion protocol. Its optional daemon HTTP HEAD version check catches
failures and does not gate local behavior. The endpoint and lack of a discovered
opt-out are disclosed in the audit. Enchantment Descriptions reads standard
client-visible components and local translations; plugin behavior is outside
selection. Food-effect/container tooltip providers remain separate.

## Implementation and policy

A generic `environment_exceptions` mechanism extends the existing evidence
snapshot. The one active audit retains Prickle's original labels and binds its
project/version, filename, SHA-512 and canonical stored descriptor SHA-256,
Fabric 26.2 context and the exact requiring feature artifact/version/hash.
All incoming parents and official required edges must match. Only a resolved
library's project-level server classification may be corrected.

Unrelated server-required projects, unsupported clients, actual server-only
modules, dependency presence/ranges, release designation, download integrity
and client-only exports remain enforced. Duplicate/orphan/stale audits fail.
A new parent or changed artifact/metadata requires re-evaluation, including
removing the exception after an upstream correction. Both repository and archive
CLIs print the audit notice. `validate_mrpack.validate()` returns the checked
`Pack` after complete archive validation so the CLI can report without a second
source load. Existing callers may continue to ignore its return value.

The [new minimal template](../configureddefaults/config/enchdesc.json) enables
Shift expansion using Prickle's property wrappers. Configured Defaults only
seeds a missing file. Prickle reads valid existing values and may normalize the
file or add metadata; malformed-file recovery belongs to the upstream library.
All five previous templates and 50 previous locks/project snapshot records are
byte-identical to `59373ad`. No existing mod, Loader or Java pin changed.
The release workflow and owner acceptance gates remain unchanged.

No upstream issue or comment was submitted. The existing optional-label issue
has no maintainer clarification; a concise draft is recorded in the audit.
Alternative mods/resource packs were compared and not installed.

## Observed automated checks

Tools match the established suite: Python 3.12.12, Ruff 0.16.4 and packwiz commit
`170b22d785959dda5876b54b7f16e1b807a57fb6`. Actionlint is 1.7.12.
Audit JARs, source archives, disassembly and temporary fixtures stay outside Git.

| Check | Observed result |
| --- | --- |
| Original baseline `make test lint validate` | Passed, 98 tests, 40 features and ten libraries; previous hosted branch CI was green. |
| Original isolated `check_mod()` reproduction | Prickle rejected with `unsupported client or mandatory server requirement`; Enchantment Descriptions accepted. Native graph compatibility passed independently. |
| New exact-library regression before implementation | Failed with the same metadata rejection. |
| Generic mechanism `make test lint validate` before activation | Passed, 114 tests, unchanged 40-feature baseline. |
| Integrated `make test lint validate` | Passed, 116 offline tests, 41 features and eleven libraries, with explicit Prickle AUDIT notice. |
| `make refresh` and subsequent exports | Passed, no pack/index drift. |
| `make checksum`, second `make export`, archive `cmp` | Passed, fully validated archive and byte-identical normalized output. |
| Generated checksum verification | Passed. |
| `check_target_readiness.py --offline` | Passed for the recorded active selections and libraries; discovery is not runtime proof. |
| Actionlint and Ruff complexity threshold 8 | Passed. Configured maximum remains 10; no changed function exceeds either threshold. |
| Old lock/snapshot/template and release-gate comparison | Passed, all 50 existing pins/project records, five templates and workflow/policy unchanged. |
| Tracked JAR scan | Empty. No mod/source binary is committed. |

Exact repository/build commands:

```sh
make test lint validate
make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
python3 scripts/check_target_readiness.py --offline
make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cp dist/lantern-crossing-26.2.0.9.0-dev-26.2.mrpack /tmp/lantern-enchantment/first.mrpack
make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cmp /tmp/lantern-enchantment/first.mrpack dist/lantern-crossing-26.2.0.9.0-dev-26.2.mrpack
(cd dist && sha256sum --check lantern-crossing-26.2.0.9.0-dev-26.2.sha256)
/tmp/lantern-bin/actionlint .github/workflows/validate.yml
ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'
git diff --check
git ls-files '*.jar' '*.JAR'
```

Packwiz resolved the expected Prickle 26.2.0.3 dependency. Its pinned executable
warned that Enchantment Descriptions' newer environment enum was unknown and
initially wrote both-side metadata. Both new lock records were deliberately set
to `side = "client"` and `pin = true` under the established pack contract.
No download or validation policy was relaxed.

Sixteen synthetic, project-independent policy tests cover exact audit acceptance,
removal, changed version/hash/descriptor/target/scope, corrected metadata,
unsupported clients, selected features, server-only roots/bundles, unrelated
required-server dependencies, native incompatibility, bad hashes, changed or
unofficial parents, orphan/duplicate audits and explicit notices. Two integration
tests bind the actual feature/library classification and minimal Prickle config.
Existing archive tests still enforce exact URLs/hashes, client environment,
complete closure and byte-identical repository overrides. Unit tests require no
network or Java runtime and do not imitate Minecraft behavior.

The Fabric predicate evaluator remains conservative and partial, with unsupported
or ambiguous semantics failing explicitly. Neither it nor source inspection
proves mixin application or a successful vanilla-server join on an owner's JVM.

## Artifact and branch state

`dist/lantern-crossing-26.2.0.9.0-dev-26.2.mrpack` is 30,899 bytes with 52 pinned
client downloads and six templates under `overrides/configureddefaults/`.
All downloads are client-required/server-unsupported. There are no root live
preferences, staged candidates, embedded JARs, shader packs or server payload.
SHA-256:

```text
3c3c1614b1f41e63f9a04121653c24c8c739705996c9634abdcf01b0cd2c27d8
```

The 26.3 bootstrap retains actual Minecraft 26.2, pack 26.2.0.3.0, 30 features
and nine libraries. Its shared tooling/migration intent may be updated; no
Prickle artifact or environment exception is installed there. All 41 intended
future features remain deferred/runtime pending. The 26.2 audit cannot qualify
26.3 artifacts. Release publication still requires target/branch agreement,
matching tag, ancestry and owner evidence bound to the exact pack hash.
No tag or release is created by this review.

## Owner handoff

Complete the [enchantment matrix](acceptance-tests.md#enchantment-descriptions-acceptance)
in both launchers, alongside the existing configuration/vanilla-server checklist.
Fresh initialization, Shift expansion, enchanted items/books, translations,
tooltip readability, existing valid settings, real upgrades and vanilla-server
connectivity all remain uncompleted. Treat custom server/plugin semantics,
legacy configuration formats and launcher/App sync behavior as limits requiring
separate observation. No runtime success is implied by the automated results.
