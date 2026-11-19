# Verification record

QoL refinement completed on 2026-11-19 for development pack `26.2.0.8.0`,
Minecraft 26.2, Fabric Loader 0.20.1 and Java 25. Minecraft, Prism Launcher and
Modrinth App have not been run. Runtime acceptance remains uncompleted.
The preceding Configured Defaults evaluation is recorded in Git at `5577d19`.

## Selection and provenance

The [nine-candidate evaluation](mod-audit.md#qol-and-performance-refinement-2026-11-19)
adds BetterGrassify `r4yqxYQl`, Controlling `sZHXONgm`, Food Effect Tooltips
`aXyL1zFA`, and resolved Searchables `bvFby61J`. Exact URLs, filenames, SHA-512
hashes and stable project/version IDs are in the four new `mods/*.pw.toml`
records; the hash-verified metadata and recursive Fabric descriptors are in
`upstream-metadata.json`. All four artifacts are upstream releases with client
native environments. There are no new bundled JARs or server dependencies.

Packwiz resolved Searchables from Controlling. Food Effect Tooltips omits its
Fabric API and Cloth Config requirements from Modrinth metadata, so the exact
native descriptor supplies those two closure edges and artifact-field provenance.
Both libraries already exist. All 46 previous locks and their full upstream
project records are byte-identical to `5577d19`. The original four defaults
files, release policy, CI workflow, Minecraft/Loader and Java pins are unchanged.
The only added template is `configureddefaults/config/bettergrass.json`.

Enchantment Descriptions, Crash Assistant, Better Block Entities and Tooltip
Tweaks remain inactive for documented dependency, initialization or rendering/data
concerns. Ixeris and ModernFix-mVUS remain staged for owner benchmarking.
No performance measurements or upstream issue reproductions were attempted.
Native range checks against temporary candidate inventories pass for BBE,
Ixeris, ModernFix-mVUS and Tooltip Tweaks; that does not resolve their blockers.

## Observed automated results

Python 3.12.12, Ruff 0.16.4 and the CI-pinned packwiz commit
`170b22d785959dda5876b54b7f16e1b807a57fb6` were used. Actionlint is 1.7.12.
Candidate JAR/source downloads and logs remain outside the repository.

| Check | Observed result |
| --- | --- |
| Baseline `make test lint validate` before edits | Passed, 94 tests, 37 features and nine libraries. Prior hosted CI was green on both branch tips. |
| Four new focused tests before integration | Failed for absent selected identities, Searchables, food native edges and the BetterGrassify template. |
| Final `make test lint validate` on 26.2 | Passed, 98 offline tests, 40 features and ten libraries. |
| `make refresh` | Passed; repeated export refresh leaves pack/index contents unchanged. |
| `make checksum`, second `make export`, archive `cmp` | Passed, full archive validation and identical normalized bytes. |
| Generated `sha256sum --check` | Passed. |
| `check_target_readiness.py --offline` | Passed for all 40 active feature selections; discovery is not runtime proof. |
| Actionlint with shellcheck | Passed; workflow/release gates are unchanged. |
| Ruff complexity threshold 8 | Passed; configured maximum is 10. No production function was changed or broadened. |
| Prior lock/snapshot/template byte comparison | Passed for all 46 retained locks/project records and four templates. |
| `git ls-files '*.jar' '*.JAR'` | Empty. No downloaded binary is committed. |

Exact build commands:

```sh
make test lint validate
make refresh PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
python3 scripts/check_target_readiness.py --offline
make checksum PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cp dist/lantern-crossing-26.2.0.8.0-dev-26.2.mrpack /tmp/lantern-refinement/first.mrpack
make export PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'
cmp /tmp/lantern-refinement/first.mrpack dist/lantern-crossing-26.2.0.8.0-dev-26.2.mrpack
(cd dist && sha256sum --check lantern-crossing-26.2.0.8.0-dev-26.2.sha256)
/tmp/lantern-bin/actionlint .github/workflows/validate.yml
ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'
git diff --check
git ls-files '*.jar' '*.JAR'
```

The first uncached export was blocked by sandbox networking and correctly failed
archive validation for missing downloads. Retrying with network access populated
the external cache and passed. An old test hard-coded pack 0.7.0; it now derives
the version while retaining tag-mismatch rejection. No production check was
relaxed to accommodate an artifact or unsupported dependency.

The new tests verify active identities/library roles, incompatible Searchables,
Food Effect Tooltips' otherwise omitted native closure and restrained visual
defaults. Existing tests still cover exact pins, required-server rejection,
prerelease provenance, staged leaks, Configured Defaults isolation, root live
preferences, index/archives, branch labels and release eligibility.

The seven recorded Configured Defaults source-only file-handler cases remain
bound to the unchanged helper artifact and previous templates. They were not
rerun or extended into a Minecraft simulation. New JSON/template checks establish
packaging and intended settings, not actual in-game behavior. The native Fabric
predicate evaluator remains conservative and partial; unsupported semantics fail
explicitly. It does not replace Loader's complete SAT resolver or runtime mixins.

## Artifact and branch state

`dist/lantern-crossing-26.2.0.8.0-dev-26.2.mrpack` is 29,544 bytes, with 50 pinned
client downloads and five templates under `overrides/configureddefaults/`.
Every mod is client-required and server-unsupported in the archive. There are no
root live preferences, staged candidates, server data, embedded JARs or shaders.
SHA-256:

```text
768faa063f4bee5d111a6b2f8a42b15c731dbe5041209358f53885ebbe62ab0a
```

The 26.3 bootstrap retains pack 26.2.0.3.0, actual Minecraft 26.2, 30 features
and nine libraries. It receives only the reusable candidate evaluation and
40-feature migration inventory. All intended 26.3 selections remain deferred,
runtime pending. Neither its existing pins nor Configured Defaults installation
status changes. A 26.3 discovery artifact is not a compatibility qualification.
Publication continues to require matching tag, version branch/actual-target
agreement, remote ancestry and owner acceptance bound to the pack hash.
No tag or release is created by this milestone.

## Owner handoff

All runtime results remain uncompleted in the [launcher matrix](acceptance-tests.md#launcher-configuration-acceptance-matrix)
and [refinement checklist](acceptance-tests.md#qol-refinement-acceptance).
Test fresh imports, App sync choices, F7/F9, customized files, real upgrades,
terrain/culling/Iris interactions, food-effect probabilities, existing worlds
and a completely vanilla-server join. No launcher-specific override, automatic
update UI or newly installed crash-reporting interface is promised.
