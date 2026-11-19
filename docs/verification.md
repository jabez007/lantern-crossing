# Verification record

## Maintenance transition, 2026-11-19

26.2 is now legacy maintenance; 26.3 is primary development and GitHub default.
Only the P3 shader acceptance correction, branch/target guard, generic docs
regressions, Node 24 artifact Action and explicit shader/default index drift paths
are applied here. No mod/shader lock, pack/index, config template, library pin or
acceptance field changes. The 26.2 archive remains the same 54-download baseline.
The earlier records below retain their milestone-specific branch observations;
they are historical and do not override the current branch policy.

Observed maintenance checks: `make test lint validate` passed 141 offline tests,
Ruff and the 26.2 metadata checks. `make refresh`, `make checksum`, `make export`
(with the pinned Packwiz/cache arguments) passed. The two exports were
byte-identical, and the 54-download archive is unchanged from the previous
26.2 milestone: SHA-256
`fe76538fbf180eee4837cbebb44344792295992369ff26fb63b606fbfc30dea1`.
`git diff --exit-code a189c7a -- pack.toml index.toml mods shaderpacks configureddefaults docs/upstream-metadata.json release-policy.toml`
passed, confirming no dependency/payload/qualification drift. Actionlint and
`git diff --check` passed. All Minecraft/launcher acceptance remains pending.

## Historical 26.2 shader verification

Pack version `26.2.0.10.0` is the 26.2 feature-freeze baseline pending owner
runtime acceptance. Target: Minecraft 26.2, Fabric Loader 0.20.1, Java 25.
The baseline has 41 Fabric feature mods, eleven libraries and two optional shader
choices, 54 upstream downloads. Current development archive:
`lantern-crossing-26.2.0.10.0-dev-26.2.mrpack`.

No Minecraft, Prism Launcher, Modrinth App, GPU benchmark or shader runtime test
was performed. All results in the shader owner matrix remain uncompleted.
The preserved 26.3 branch is a future forward migration target, not a parallel
release baseline. GitHub's default remains unchanged by owner choice.

## Shader milestone checks

The [exact source/license audit](mod-audit.md#optional-shaders-and-distribution-2026-11-19)
selects Complementary Reimagined r5.10 / RKfUB9VC and MakeUp 9.6 / t4YRxQug.
Both official ZIPs matched SHA-512. Complementary source correspondence was
confirmed with line-ending normalization for comparison only; MakeUp shader
files and notices matched byte-for-byte. No upstream ZIP was altered. Iris's
pinned feature enum recognizes Complementary's optional flags. These observations
establish packaging/static eligibility, not GLSL compilation or GPU acceptance.

Shader locks/evidence are distinct from native Fabric mod metadata. Validation
requires exact official references and renderer-bound distribution audits, a
client-only shader destination and disabled-only Iris defaults. Required or incompatible shader
project dependencies fail explicitly for separate closure review. No such edge
exists in these releases. Existing Fabric native requirements, client-only
rules and the exact Prickle environment audit remain intact.

All 52 existing mod locks and their evidence dictionaries, six defaults, native
dependency inventory, Loader/Java versions, release policy and GitHub workflow
remain unchanged from 2add0bf. Only the two shader references are added to index.
The pack version advances by one minor step for the optional visual additions.
No actual shader presets or live settings are shipped. The 26.3 branch is not
modified or synchronized by this milestone; its tip remains b5b1262.

Observed automated checks:

| Command/check | Observed result |
| --- | --- |
| Baseline `make test lint validate` | Passed, 121 tests. Starting hosted CI at 2add0bf was green. |
| Pre-change validator against the new shader index | Rejected the shader metadata as an unexpected indexed file. Shader artifacts needed a separate typed path. |
| Extended model with no shader selections | All 121 prior tests passed before integration. |
| `make test lint validate` | Passed, 138 offline tests, including 16 focused shader tests and a release-example documentation regression; formatting/lint and all prior native/client-only regressions pass. |
| `make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | Passed; final manifest/index consistent. |
| First uncached export without network access | Packwiz omitted the two failed downloads but reported success. Archive validation rejected the missing shader set. Resolved by rerunning with network access; validation was not relaxed. |
| `make checksum` and repeated `make export` with the same Packwiz override | Passed; complete archive validation, byte comparison and checksum verification passed. |
| `python3 scripts/check_target_readiness.py --offline` | Passed for all 52 Fabric records and both Iris choices; discovery is not runtime proof. |
| `/tmp/lantern-bin/actionlint .github/workflows/validate.yml` | Passed; workflow/tool pins unchanged. |
| `ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'` | Passed; configured maximum stays 10. No changed function exceeds 8. |
| Old lock/default/evidence comparison | All 52 mod locks, six templates, prior project snapshots and both exception sets unchanged from 2add0bf. |
| Source review and `git diff --check` | Passed. No tracked JAR/ZIP, generated source junk, shader preset or unapproved payload. |
| Version-branch check | 26.3 remains at b5b12628561c2a4d78854b1244d58133dfad54aa; no commit or synchronization there. Hosting default remains 26.3. |

Exact final build commands:

```sh
make test lint validate
make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cp dist/lantern-crossing-26.2.0.10.0-dev-26.2.mrpack /tmp/lantern-shaders/first.mrpack
make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cmp /tmp/lantern-shaders/first.mrpack dist/lantern-crossing-26.2.0.10.0-dev-26.2.mrpack
(cd dist && sha256sum --check lantern-crossing-26.2.0.10.0-dev-26.2.sha256)
python3 scripts/check_target_readiness.py --offline
/tmp/lantern-bin/actionlint .github/workflows/validate.yml
ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'
git diff --check
git ls-files '*.jar' '*.JAR' '*.zip' '*.ZIP'
```

The normalized artifact is 31,990 bytes with 54 pinned client downloads and six
Configured Defaults overrides. Both shaders install through manifest entries
under `shaderpacks/`; no JAR/ZIP is embedded, and every download remains
client-required/server-unsupported. SHA-256:

```text
fe76538fbf180eee4837cbebb44344792295992369ff26fb63b606fbfc30dea1
```

Shader tests cover mod-declared shader incompatibility, exact identities/roles/paths, missing/duplicate/unapproved
records, side/pin/hash/URL enforcement, native metadata separation, release and
environment checks, stale distribution/renderer reviews, unreviewed dependency
edges, disabled-only defaults, no copied ZIP/preset payloads, complete exports
and Iris-aware discovery. Existing normalization tests now exercise the shader
entries too. They do not simulate Iris/GPU/launcher behavior. Native Fabric
predicate support remains conservative and partial as documented below; it is
not repurposed as a shader compiler.

A documentation regression exposed stale release-example tags in version policy.
The old guard accepted that file's stale baseline/examples; the new tests failed
before the fix. The existing release metadata check now also checks its current
baseline statement and both release-command examples. README and current release
records match pack.toml; historical verification versions remain dated evidence.

No release is runtime-qualified or published. Complete the
[shader owner matrix](acceptance-tests.md#shader-owner-acceptance-matrix), alongside
the existing full acceptance checklist in Prism and Modrinth App, then record
actual owner results and the final pack hash through the existing release gate.
Resolve failures through scoped fixes while feature additions remain frozen.

## Prior verification, pack 26.2.0.9.0

At that earlier review, pack version `26.2.0.9.0` was the current development baseline.

The Prickle environment review completed on 2026-11-19 for development pack
`26.2.0.9.0`, Minecraft 26.2, Fabric Loader 0.20.1 and Java 25. No Minecraft,
Prism Launcher or Modrinth App runtime acceptance was performed. All owner
results remain uncompleted. Prior refinement evidence is in Git at `59373ad`.

### Verdict and artifact correspondence

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

### Implementation and policy

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

### Observed automated checks

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

### Artifact and branch state

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

### Owner handoff

Complete the [enchantment matrix](acceptance-tests.md#enchantment-descriptions-acceptance)
in both launchers, alongside the existing configuration/vanilla-server checklist.
Fresh initialization, Shift expansion, enchanted items/books, translations,
tooltip readability, existing valid settings, real upgrades and vanilla-server
connectivity all remain uncompleted. Treat custom server/plugin semantics,
legacy configuration formats and launcher/App sync behavior as limits requiring
separate observation. No runtime success is implied by the automated results.

### Screenshot review, 2026-11-19

The [candidate and architecture matrix](mod-audit.md#screenshot-experience-evaluation-2026-11-19)
retains Renice Shot `roOTvshj` alone. Screenshot Viewer `id6Yni9S` is eligible
under the current artifact/environment rules but deferred for whole-library
image loading, missing memory bounds and broad image/AWT hooks. Screenshot
Overhaul `H592Npj8` passes native dependency-range checks but fails intentional
release designation and independently fails the selected metadata/deletion
safety requirements. No exception was created. Neither candidate is installed.

Exact SHA-512-verified candidate binaries and release-time source were inspected
outside Git. All top-level-JAR classes were disassembled without executing mod
code. The pinned Xaero World Map JAR was hash-verified and its primary mixin
signatures inspected. This does not qualify optional map integration or a
combined capture pipeline. No Minecraft, launcher, rendering, screenshot
capture, large-gallery benchmark or user-file migration was performed.

Observed checks for this pass:

| Command/check | Observed result |
| --- | --- |
| Baseline `make test lint validate` | Passed, 116 tests; both existing branch CI tips green. |
| Isolated candidate `check_mod()` and native graph checks | Viewer accepted; Overhaul rejected as selected alpha. Both native graphs passed with the existing 52 pins. No installation or general policy change. |
| New documentation regression before implementation | Failed because the checker was absent. Current-document check then failed until its explicit version statement was added. Stale version/branch and pack-advance fixtures are rejected. |
| `make test lint validate` | Passed, 121 offline tests, 41 features and eleven libraries; existing exact Prickle AUDIT notice unchanged. |
| `make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | Passed; index, manifest and payload unchanged. |
| `make checksum` followed by a second `make export`, using the same Packwiz override | Passed; archive validation and `cmp` passed. |
| `(cd dist && sha256sum --check lantern-crossing-26.2.0.9.0-dev-26.2.sha256)` | Passed. The complete archive still has the hash recorded above. |
| `python3 scripts/check_target_readiness.py --offline` | Passed. Discovery is not runtime proof. |
| `/tmp/lantern-bin/actionlint .github/workflows/validate.yml` | Passed; workflow unchanged. |
| `ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'` | Passed; configured threshold remains 10. No changed function exceeds 8, and no cleanup/refactor was required. |
| `git diff --check` and tracked JAR scan | Passed; no JARs in Git. |
| Baseline comparison | Pack/index, all 52 locks/project evidence records, six defaults, collection, migration inventory and release gates unchanged. |

`check_documentation()` reuses `artifact_names()` in the release metadata module.
The metadata CLI now checks explicit current-version statements in README and
this record, their development archive names, and the release-notes lead. It
checks development instructions even for a release-channel invocation. Historical
review versions remain valid evidence. Three tests cover current/stale identity
and a pack advance without matching docs. No extra maintenance command exists;
`make validate`, CI and the export workflow use the existing CLI.

Two additional pack tests bind the retained capture/staged-gallery selection
and verify that repository validation leaves a disposable existing screenshot
file byte-identical and outside overrides. Existing archive-negative tests now
also reject screenshots, screenshot state and unselected gallery configs.
Candidate export leakage was already checked generically and now covers both
new staging entries. These fixtures test repository packaging, not gallery
indexing, image decoding, launcher upgrade behavior or deletion inside Minecraft.

No payload changed in that screenshot review, so pack version 26.2.0.9.0 remained unchanged then.
The normalized archive remains 30,899 bytes, with 52 downloads and six templates,
SHA-256 `3c3c1614b1f41e63f9a04121653c24c8c739705996c9634abdcf01b0cd2c27d8`.
The 26.3 line remains a 30-feature Minecraft 26.2 bootstrap with 41 future feature
identities; no screenshot artifact is promoted there. Runtime acceptance and
release publication remain gated on the owner. Complete the new
[screenshot matrix](acceptance-tests.md#screenshot-owner-acceptance-matrix) in
both launchers. All results remain uncompleted.
