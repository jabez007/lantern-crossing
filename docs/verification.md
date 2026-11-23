# Verification record

## Writing gap recovery verification

Pack version `26.3.1.0.1` exports `lantern-crossing-26.3.1.0.1-dev.mrpack`.
The [recovery audit](mod-audit.md#writing-gap-recovery) retains the installed
BSW/Symbol Chat stack and records P2 as open and P3 as fixed. All subsequent
sections describe earlier milestone artifacts. Their archive hashes do not
identify this follow-up.

The baseline was remote commit `300837db7cd52275dcb128f3f1a0e5f95b5cd622`.
Its Actions run `45081176784` completed successfully. The results below record
local verification before this follow-up's commit and push; they do not report
a hosted CI result for the follow-up.

The diagnostic oracle executed unmodified BookPaste, Book Extractor and Booker
classes from their exact SHA-512-checked release JARs. Framework/config adapters
are stubbed; the fitter checks UTF-16 capacity, not actual Minecraft font layout.
There is no Minecraft JAR on its classpath and no Fabric/client/server/mod
initializer runs. Passing the diagnostic means the recorded failures reproduce;
it does not certify those candidates for installation.

The [adapter](../tests/fixtures/WritingRecoveryOracle.java),
[offline runner](../tests/fixtures/run_writing_recovery.py) and
[inputs/results](../tests/fixtures/writing-recovery.json) record:

- BookPaste preserves long-word/full-page remainders and a surrogate pair at a
  capacity boundary. A 500,000-unit string leaves 397,600 units after 100 helper
  slices. Both modes nevertheless turn `alpha\n\n` into `alpha` without a
  remainder. Boundary whitespace disappears, and a combining accent can start
  the next remainder separately from its base letter.
- Book Extractor round-trips a non-colliding Unicode/blank-page sample and rejects
  101 pages or 1025 units before mutation. Its accepted marker-collision sample
  loses an authored delimiter and splits one page into two.
- Booker wraps a five-page reader from index 0 to 4, but the same published
  handler throws `ArithmeticException` for a zero-page reader.

The record binds artifact identities, tested class hashes, fixture source,
Gson 2.14.0 and the downloaded Temurin 25.0.5.1+2 tool archive. Scribe's exact
CurseForge file and selected class hashes are recorded separately from its
not-fully-matched public source tree. All nine candidates' exclusions and current
issue states are in the [audit](mod-audit.md#writing-gap-recovery).

Reproduce the optional JAR diagnostic with local copies of the exact inputs
listed in the JSON record:

```sh
python3 tests/fixtures/run_writing_recovery.py \
	--jdk /tmp/lantern-writing-recovery/jdk25/jdk-25.0.5.1+2 \
	--artifacts /tmp/lantern-writing-recovery \
	--gson /tmp/lantern-writing/gson-2.14.0.jar
```

Observed command results:

| Command/check | Result |
| --- | --- |
| `make test lint validate` | PASS: 163 offline tests, Ruff lint/format, source/pins/index/native dependency/client-policy checks, migration and documentation/version consistency. |
| The JAR diagnostic command above | PASS: exact recorded observations reproduced against actual upstream class implementations, within the stubbed scope. |
| `ruff check --select C90 scripts tests` | PASS at the configured maximum 10, both before and after changes; no over-threshold functions. No separate type checker is configured. |
| `/tmp/lantern-bin/actionlint .github/workflows/validate.yml` | PASS; workflow unchanged. |
| `python3 scripts/check_target_readiness.py --offline` | PASS: recorded availability for all 54 active artifacts; candidates are not promoted. |
| `make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | PASS: index unchanged. |
| `make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | PASS from cache; exact complete archive, normalization, validation and checksum. |
| `make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | PASS repeated export. |
| `cmp /tmp/lantern-writing-recovery/first.mrpack dist/lantern-crossing-26.3.1.0.1-dev.mrpack` | PASS: byte-identical repeated builds. |
| `sha256sum --check lantern-crossing-26.3.1.0.1-dev.sha256` from `dist/` | PASS. |
| `python3 scripts/release_metadata.py --channel release --tag v26.3.1.0.1` | Expected refusal: `sodium: migration runtime acceptance remains pending`. No release/tag created. |
| `git diff --check` | PASS. |

The new README and candidate-admission regressions first failed against the old
parity text and unstaged recovery candidates, then passed after the corrections.
The first full run caught a missing literal "Pack version" prefix in this new
record; correcting the documentation satisfied the existing rule. No validation
policy was relaxed. There is no unresolved automated failure.

The eight Modrinth recovery candidates are staged in `candidates.toml`, alongside
eight existing entries. Tests show attempted active selection is rejected before
export. Scribe's official CurseForge identity is documented, without staging an
unrelated Modrinth project. No mod is added/removed/upgraded, and no defaults,
keybinding, player file or server channel is introduced.

Byte comparisons against the baseline confirmed that every mod/shader lock,
all seven defaults payloads, the active collection, index, migration inventory,
upstream metadata, validation modules, CI workflow and release-policy fields are
unchanged. The normalized previous/current archives differ only in manifest
`versionId`, from `26.3.1.0.0-dev` to `26.3.1.0.1-dev`. Both have 54 exact client
required/server unsupported downloads and seven defaults payloads.

Archive size: **32,231 bytes**. Archive SHA-256:
`40aa7eebd2cd245d345cf6e2b4decff615b3f1585de876082d1f811e13b5c1fb`.

`pack.toml` SHA-256 for any future owner acceptance:
`0c916c1b032c0296e79ec9707533bc53cb1ca2d9e80df3a48c41c0a83501e2a7`.

No Minecraft, Prism, Modrinth App, vanilla server or ordinary vanilla observer
acceptance ran. All [owner checks](acceptance-tests.md#gap-recovery-owner-checks)
remain uncompleted and all release-approval fields remain blank. P2 remains open,
with the unchanged BSW partial-row overflow and combined GUI/input acceptance
risks. P3 is fixed. No import, history, backup or cross-page recovery is promised.

The local `26.2` ref remains `6d7e73af2ab2c4835ac748be538d22abd9631ec7`.
No 26.2 checkout, backport, commit or push was performed. This follow-up's commit
and push target 26.3 only; no tag or release is created. Existing hard-coded
mod-count checks remain an optional cleanup;
no unrelated refactor or new over-threshold function is introduced.

## Writing refinement verification, 2026-11-22

Pack version `26.3.1.0.0` exports
`lantern-crossing-26.3.1.0.0-dev.mrpack`. The writing selection and pending owner
cases are recorded in the [audit](mod-audit.md#writing-refinement) and
[acceptance matrix](acceptance-tests.md#writing-owner-acceptance-matrix).
The records below this section describe older milestones, including the previous
pack version. Their hashes and smoke-test observations do not qualify this build.

The current archive has 54 exact downloads: 41 mod features, eleven libraries and
two optional shaders. It includes seven defaults payloads, no live config or
player content, and neither old editor download. BSW 3.1.1 (`ics7z6RR`) and
Symbol Chat 1.4.3 (`Y9zsgkwF`) replace Sign Tweaks and Book Tweaks.
Every original retained mod pin, shader audit and existing defaults template is
byte-identical to the prior checkout. Configured Defaults adds only the missing
Symbol Chat template. No environment/dependency exception or release-policy
approval field changed. The sole existing Prickle exception remains exact.

The major version increment follows the existing selection/setup-review policy.
Migration schema 3 retains all 54 source rows, records both retired editor pins
and replacement dispositions, and adds two target-only entries. Active, retired
and added artifact evidence remains checked; new entries and both retirements all
retain independent pending runtime states. No fictitious 26.2 artifacts are added.

| Command or check | Observed result |
| --- | --- |
| `make test lint validate` | PASS: 159 offline tests; Ruff lint/format, exact lock/index, native dependency closure, environment policy, documentation, migration and development identity checks. |
| `ruff check --select C90 scripts tests` | PASS before and after implementation, configured maximum 10; no over-threshold functions reported. No separate type checker is configured. |
| `/tmp/lantern-bin/actionlint .github/workflows/validate.yml` | PASS; unchanged workflow. Hosted GitHub Actions was not run during this local verification. |
| `python3 scripts/check_target_readiness.py --offline` | PASS: all 54 active artifacts have recorded target build availability; discovery is not runtime qualification. |
| `make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | PASS: repeated refresh leaves pack/index byte-identical. |
| `make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | PASS with network available for the two new pinned artifacts; full export, normalization, archive validation and checksum creation. |
| `make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` | PASS from cache; complete normalized archive. |
| `cmp /tmp/lantern-writing/first-complete.mrpack dist/lantern-crossing-26.3.1.0.0-dev.mrpack` | PASS: byte-identical repeated exports. |
| `sha256sum --check lantern-crossing-26.3.1.0.0-dev.sha256` from `dist/` | PASS. |
| `python3 scripts/release_metadata.py --channel release --tag v26.3.1.0.0` | Expected refusal: `sodium: migration runtime acceptance remains pending`. No release was created. Tests separately verify new-artifact and retirement acceptance cannot be skipped. |
| `git diff --check` | PASS; no staged changes. |

The first sandboxed export could not resolve/download the new files. Packwiz
omitted them, and our unchanged archive validator rejected the incomplete pack.
The network-enabled retry downloaded the exact SHA-512-checked files and passed.
There is no unresolved automated failure. No validator exception was added.
Conflict/selection regressions failed against the old selection before the
change. A retired-pin mutation test also failed before the corresponding gate
was added; it now rejects altered historical identity instead of bypassing it.

Book Tweaks was rejected after the exact JAR/source audit found legacy GLFW
key dispatch and clipboard consumption without confirmation of accepted text.
The final pack uses vanilla book page editing, without Book Tweaks page tools
or memory. The [input audit](upstream-metadata.json) binds artifact/class hashes
and the inspected vanilla SDL key values. No game execution or runtime data-loss
claim is involved. A future release needs a fresh input/paste audit before
Book Tweaks can be selected again.

Tooling observed: Python 3.12.12, Ruff 0.16.4, actionlint 1.7.12. Packwiz build
metadata identifies `170b22d78595` and Go 1.24.6, matching the pinned CI tooling.

The temporary audit command `python3 /tmp/lantern-writing/run-oracles.py` compiled
the unmodified Symbol Chat `FontProcessor`, `MappedFontProcessor` and `Util`
sources at `7da2d67e`, with the repository fixture
[`SymbolChatFontsOracle.java`](../tests/fixtures/SymbolChatFontsOracle.java).
Only Minecraft identifier/translation/GsonHelper adapters were stubbed. Actual
Gson 2.14.0, ICU 78.3 and the pinned JAR's font JSON were used. The recorded
[conversion results](../tests/fixtures/symbol-chat-fonts.json) bind source,
resource, library, adapter and artifact hashes. Mathematical bold, fullwidth and
circled conversions passed, including preservation of an unmapped supplementary
symbol. This executes source conversion code, not the compiled game or editor.
Fullwidth also changes spacing/punctuation; substitutions are not native styles.

The same audit command reran the existing unmodified Configured Defaults handler
with JDK 17.0.21.1 and logging/constants stubs. All seven file scenarios passed
with the additional writing template. Customized Symbol Chat settings/favorites
survived repeat launches and template updates. The
[file evidence](../tests/fixtures/configured-defaults-files.json) binds the new
complete template set. JDK 17 is only the isolated audit compiler; Minecraft
still requires Java 25. Neither oracle initializes Fabric or Minecraft.

Static font-resource inspection found all 478 distinct codepoints in the 35
bundled BSW definitions in vanilla 26.3's official glyph inventory. The three
Symbol Chat sample outputs also have vanilla glyph entries. The
[recorded metadata](upstream-metadata.json) binds the exact asset index, Unifont
ZIP, client and mod artifacts. Glyph presence does not prove rendering, layout,
server filtering or persistence. Arbitrary custom fonts are not qualified.

Archive size: **32,231 bytes**. Archive SHA-256:
`3bdc717c99090ca5f16c86a7d986d42266c96f2e0ef72e9ac632a2e8dc8da514`.

`pack.toml` SHA-256 for future owner acceptance:
`d045b32730bfbd2a84c54a8ebc7747ef57fa752e679a23ac2a58e9bf0b32d894`.

No Minecraft launch, Prism or Modrinth App acceptance, vanilla-server join,
vanilla-observer rendering or server restart test was performed. The earlier
owner smoke test stays attributed to its older, unidentified artifact. All
writing matrix boxes and final release approval fields remain pending.
Concrete risks are BSW's partial-row overflow behavior, combined widget/focus
interaction, unsupported/custom glyphs, server filtering and platform input.
Rich book file tools/native formatting remain deferred, as does the rejected
Scribble composition with its macOS file-dialog report.

The `26.2` ref remains `6d7e73af2ab2c4835ac748be538d22abd9631ec7`.
No checkout, backport, commit, push, tag or publication changed that branch.
The implementation targets only `26.3`.

A remaining cleanup candidate outside the edited code is the hard-coded mod
count in `tests/test_shaders.py`. Deriving it from the shared inventory would
avoid future count maintenance. That file remains unchanged; no unrelated
refactor is included.

## Initial Prism Launcher runtime smoke test

Source: the repository owner's initial runtime acceptance report for Minecraft
Java 26.3, recorded on 2026-11-19. The owner imported a GitHub Actions development
`.mrpack` into Prism Launcher, launched Minecraft and played/explored successfully.
The initial smoke test passed, with no significant issues reported.

| Observation | Owner-confirmed result |
| --- | --- |
| Prism import and startup | Development pack imported and Minecraft 26.3 launched successfully; no blocking startup issue reported. |
| Gameplay and exploration | Play and exploration worked; general feedback was positive. Individual mods were not comprehensively exercised. |
| IPN purple hotbar arrows | Expected auto-refill indicators. Owner chose to keep them enabled. |
| Mod Menu compact pause-menu icon | Mod Menu is present and accessible through the list icon in the pause-menu icon row. Owner chose to retain that style. |
| BetterGrassify green block sides | Expected FANCY-mode grass extending down block sides, rather than a rendering defect. Owner chose to retain the current configuration. |

The three unfamiliar behaviors are resolved observations, not bugs or outstanding
issues. No configuration changes are requested or made. This report does not
establish an absence of all dependency warnings or log errors.

The report does not identify the exact archive filename/SHA-256, test-session
date, Prism version, Java runtime details, OS, GPU or driver. Do not infer those
from the current build records below or bind this result to an unconfirmed hash.
This is preliminary owner evidence, not final release approval. The detailed
[acceptance checklist](acceptance-tests.md), migration runtime states and final
release-approval fields remain pending.

The following remain unconfirmed by this report:

- Modrinth App installation and startup.
- Both bundled shaders, shader switching and performance comparisons.
- The complete unmodified vanilla-server compatibility matrix.
- Every individual QoL mod's functionality.
- Configured Defaults on a completely fresh instance.
- Preference persistence after restarts and preservation through pack upgrades.
- Existing-world and configuration migration from 26.2 to 26.3.
- Platform compatibility beyond the owner's tested environment, whose details
  were not supplied.

The build records below describe automated work at their respective milestones.
Their statements that no runtime testing occurred apply to those earlier checks.

## Development artifact naming

Pack version `26.3.0.1.0` now exports
`lantern-crossing-26.3.0.1.0-dev.mrpack` with a matching
`lantern-crossing-26.3.0.1.0-dev.sha256` file. The generated manifest uses
`26.3.0.1.0-dev`. Qualified releases retain the unsuffixed pack version/name.
Only naming changes; pack/index, all artifact pins, configs and release acceptance
requirements remain unchanged. Historical artifacts/releases are not renamed.

Observed: `make test lint validate` passed 148 offline tests, lint/format and
all repository checks. `make refresh` left the pack/index/locks unchanged.
`make checksum` and repeated `make export` with
`PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'` passed;
`cmp` confirmed byte-identical outputs and `sha256sum --check` passed.
Actionlint and the configured complexity check passed. The archive is 31,987
bytes with 54 downloads and six defaults payloads. Its only internal difference
from the prior archive is the development manifest `versionId`.

SHA-256: `5a02ef6230042064afcb2736fe8efefa1d54ebaef6f1acac37ccbe9ecaa3cd31`.

Regression tests first failed with the old naming, then passed for development
and release identities on both Minecraft targets. They cover normalization,
checksum names, rejection of legacy filenames and all prior release gates.
Documentation now checks branch/target agreement explicitly because filenames
no longer contain the branch. Makefile and Actions already consume the shared
metadata outputs, so no duplicated naming logic or workflow edit is needed.
No Minecraft or launcher runtime acceptance was performed or marked complete.

The earlier records below describe builds produced before this naming cleanup.
Their old filenames, manifest versions, sizes and checksums remain historical
evidence, not current build instructions.

## Historical 26.3 migration verification

Pack version `26.3.0.1.0` is the primary Minecraft 26.3 migration baseline.
Development artifact: `lantern-crossing-26.3.0.1.0-dev-26.3.mrpack`.
All 41 feature mods, eleven libraries and two shaders from 26.2.0.10.0 are
accounted for, without replacements/exclusions. Every runtime state remains pending.

The existing 26.3 bootstrap was merged with the full 26.2 tree while retaining
both histories. The 26.2 P3 checklist regression reproduced four stale shader
claims; the focused fix passed 139 offline tests and source validation there.
No 26.3 locks are copied to 26.2. GitHub already defaults to 26.3; both branches
were unprotected and no rulesets existed when inspected. No force-push, branch
deletion, tag or release publication is part of this migration.

## Migration evidence and limits

The [complete artifact matrix](mod-audit.md#263-artifact-migration-matrix) and
`migration.toml` cover exact source/target identities and closure. All proposed
artifacts were downloaded to a temporary audit directory and SHA-512-checked.
Fabric root and nested descriptors, release notes, loader constraints and hard
incompatibilities were inspected. Current loader metadata returns0.20.1 stable;
Mojang26.3 metadata requires Java 25. The official client SHA-1 and options data
version 5023 were verified without executing the game.

Prickle and ED26.3 Maven binaries match Modrinth byte-for-byte. Their36 and7
published Java sources respectively match immutable26.3 source commits. The
new environment exception binds the exact artifact, descriptor, target and ED
parent. Unrelated server-required projects remain rejected. Prickle's disclosed
asynchronous HTTP update check remains; no companion protocol was found.

The existing Configured Defaults Java file-method oracle was rerun for all
seven cases using the unmodified26.3 source, actual JAR README resource and
logging/constants stubs. It covers fresh/partial/custom options, repeat launch,
updates, resource-pack order and old-manager/adoption behavior. It does not run
Fabric, Minecraft, Prism or the App, and does not prove Minecraft's later option
conversion. InputConstants bytecode retains symbolic `key.keyboard.f7` mapped
to SDL scancode 64; no GLFW numeric seed is distributed. The five mod templates
remain unchanged; only the options seed version changes.

Both official shader ZIP hashes and licenses remain unchanged; audits bind
Iris 1.11.7. New shader compilation, transparency, GPU support, frame times,
Wayland/windowing, input and actual vanilla26.3 server joins remain owner tests.
No Minecraft launch, GPU benchmark, launcher test or multiplayer acceptance was
performed. No acceptance record or runtime state has been marked complete.
MakeUp issue #208 is still open and now describes this exact 26.3 rendering
stack on Apple Silicon. The optional DoF feature is off upstream; owner checks
record this limitation separately. No shader ZIP is patched or preset forced.

## Automated migration checks

Observed: 146 offline tests passed; Ruff lint/format, pack/index/closure checks,
offline readiness and actionlint passed. Both complete normalized exports were
byte-identical. The archive is 31,992 bytes with 54 downloads and six defaults
payloads, all client required/server unsupported; two ZIP references are under
`shaderpacks/`, with no embedded mod/shader binary.

SHA-256: `14ef42ec1f28e62a6d1d1bb2f4d3fd5b27392529377bf2da0a5f4423af7abfcc`.

Commands executed on 26.3:

```sh
make test lint validate
make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cp dist/lantern-crossing-26.3.0.1.0-dev-26.3.mrpack /tmp/lantern-migration/first.mrpack
make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cmp /tmp/lantern-migration/first.mrpack dist/lantern-crossing-26.3.0.1.0-dev-26.3.mrpack
python3 scripts/validate_mrpack.py dist/lantern-crossing-26.3.0.1.0-dev-26.3.mrpack
python3 scripts/check_target_readiness.py --offline
/tmp/lantern-bin/actionlint .github/workflows/validate.yml
ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=10'
git diff --check
git ls-files '*.jar' '*.JAR' '*.zip' '*.ZIP'
```

The previous branch guard accepted a synthetic mismatch as
`lantern-crossing-26.3.0.1.0-dev-26.2.mrpack`. With the fix, the same fixture
fails: “version branch must target its own Minecraft release”. Release tests
also reject pending runtime acceptance, stale pin/role/closure records, missing
libraries/shaders and changed pack acceptance hashes.

New regression coverage includes Loader-provided library version incompatibility,
loader descriptor/pin changes and all-artifact migration completeness. Existing
server-required/prerelease/provenance/archive tests pass without weakened rules.
The configured complexity limit 10 passes; `check_entry` is 9, within that limit.
No new function exceeds the repository threshold. No unrelated refactor was needed.

Artifact Action updated from v5 to immutable v7.0.2 (Node 24), retaining the
existing workflow and release gates. Index drift checks now explicitly include
shaders and Configured Defaults. Both version branches still receive CI.
Repository description now names 26.3; default was already 26.3. Neither branch
protection nor rulesets were created or relaxed. No owner action is needed to
change the default. Requiring PR/validate checks in GitHub remains a separate
repository-settings choice.

The native validator now accounts for MixinExtras 0.5.5 supplied by the exact
Loader JAR, without adding a duplicate download. Migration validation covers
libraries and shaders as well as features, pin/role/closure consistency and
pending runtime gates. Version branches must match targets even for development
artifacts. Existing Fabric predicate limitations remain documented.

## Historical 26.2 verification

The records below describe earlier26.2 milestones and their then-current branches.
Their hashes, test counts and strategy statements are historical, not26.3 claims.

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
