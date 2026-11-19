# Verification record — 26.3 development bootstrap

Shared hardening checked on 2026-11-19. This branch is not a Minecraft 26.3
release: `pack.toml` still declares Minecraft 26.2, Fabric Loader 0.20.1 and pack
26.2.0.3.0. It retains the original 30 features and nine libraries.
No Minecraft client has been launched. All runtime acceptance remains open.

## QoL refinement planning backport, 2026-11-19

The maintained 26.2 milestone `59373ad` has 40 features and ten libraries.
This branch receives its candidate evidence, explicit blockers and all 40 future
migration identities only. BetterGrassify, Controlling, Food Effect Tooltips and
Searchables are not installed here; all 39 bootstrap downloads and config bytes
remain unchanged. No 26.3 artifact is promoted or release-qualified.

Observed `make test lint validate` passed with 87 tests and the same single
intentional absent-helper skip. `make refresh`, `make checksum`, a second
`make export`, archive `cmp` and checksum verification passed using the Packwiz
override below. The archive remains byte-identical to the preceding bootstrap
hash. Actionlint, complexity threshold 8 and `git diff --check` pass. A byte diff
against `8463058` confirms unchanged locks, configs, collection, pack/index,
upstream snapshot, workflow and release policy.

The candidate-leakage test previously assumed an empty staging file. With actual
candidate tables now tracked, only that obsolete fixture edit was removed; the
same active-ID rejection remains asserted. The tag test now derives its pack
version while retaining mismatch rejection. All runtime results remain pending.
The appended refinement checklist is prospective until the migration audit.

## Configuration evaluation backport, 2026-11-19

The [final evaluation](configuration.md#defaults-manager-evaluation-2026-11-19)
selects Configured Defaults on the maintained 26.2 line. This bootstrap does not
install it, promote the later features or change target/version. The shared
validator and migration inventory reflect that future intended helper. The old
Default Options alternative is not a migration selection.

The manager's seven recorded source-only file cases and adapter are available as
reference evidence. Its active-artifact/template binding test is intentionally
skipped because the helper is absent. No Fabric, Minecraft or launcher is run.
All launcher matrix results remain uncompleted. The bootstrap retains its
original direct mod configs and cannot publish a release.

Final backport checks passed: `make test lint validate` ran 87 tests with one
intentional skip of the absent helper binding. `make refresh`, `make checksum`,
`make export`, repeated `cmp` and checksum verification passed with the external
Packwiz override recorded below. The archive still matches the prior green-CI
bootstrap bytes and hash exactly. Actionlint and Ruff including complexity <=8
passed. `git diff --exit-code -- mods config pack.toml index.toml collection.toml docs/upstream-metadata.json release-policy.toml`
confirmed that target, pins, payload and release qualification are unchanged.

## Scope and findings

Native Fabric predicate checks and release/artifact safeguards were backported
from the maintained 26.2 line. All 39 bootstrap locks and the configuration
payload remain unchanged from `3ed86e5`. No missing later feature was added to
this branch merely to match the maintained line's count.

The maintained line has 40 features. Its six post-baseline additions, Configured
Defaults helper and three QoL refinements are tracked in [migration.toml](../migration.toml). All entries
remain deferred with runtime pending. Discovery on 2026-11-19 found a Fabric
26.3 release for each feature, but did not audit those versions or their closure.
The older direct mod configuration overrides remain on this bootstrap; the
safe-defaults integration belongs to its separately authorized migration audit.
Do not use this development artifact to update an existing player profile.

## Automated verification

Use Python 3.12.12, Ruff 0.16.4, Go 1.24.6 and packwiz commit
`170b22d785959dda5876b54b7f16e1b807a57fb6`, as pinned in CI. Local commands use
`PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'`.

The shared suite checks required native `depends`, hard `breaks`, root/bundled
versions, aliases, Java/Minecraft/Loader requirements and actionable mismatches.
51 offline conformance vectors record Loader 0.20.1 API results; its JAR SHA-256
is `d0c5a082e07410aaff9de7ab196aa6b4236002870f9ba3ad5c1260fcce5110ad`.
No Java runtime or network is required by normal unit tests. Unsupported
expressions, opaque ordering and ambiguous bundled selection fail visibly.
This is a conservative partial evaluator, not Loader's full SAT resolver.
See [predicate capabilities](version-policy.md#native-fabric-requirements).

Release policy requires the intended version branch to match the numeric Git/CI
branch. Development filenames and internal archive identity name the actual
26.2 target and `dev-26.3` branch. Releases require target/branch agreement,
matching tag, remote ancestry and owner acceptance bound to the pack hash.
The current bootstrap fails release eligibility because its target is still 26.2.
Changing only a target declaration cannot qualify an unresolved migration.

Observed checks:

| Command/check | Result |
| --- | --- |
| `make test lint validate` | Passed: 76 offline tests; lint/format/complexity, exact pins, predicates, migration inventory, branch policy and index. |
| `make refresh` twice and `cmp` saved pack/index | Passed, no drift. |
| `make checksum`, second `make export`, `cmp` archives | Passed, byte-identical normalized output and complete archive validation. |
| `sha256sum --check lantern-crossing-26.2.0.3.0-dev-26.3.sha256` from `dist/` | Passed. |
| `/tmp/lantern-bin/actionlint .github/workflows/validate.yml` | Passed. |
| `ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'` | Passed; configured maximum remains 10. |
| Byte comparison of locks/configs/pack/index/upstream snapshot against `3ed86e5` | Passed, all bootstrap payload and pin evidence retained. |
| `python3 scripts/release_metadata.py --channel release --tag v26.2.0.3.0` | Rejected as intended: migration branch cannot publish a different Minecraft target. |

The development archive is 22,657 bytes, with 39 downloads and three unchanged
config overrides. Every mod is client-required and server-unsupported. Its name
is `lantern-crossing-26.2.0.3.0-dev-26.3.mrpack`; SHA-256:

```text
3e49157da527ed340c0f10c1367cdaae9cb02c1220376840086c588548b8ddff
```

Before this pass, [26.3 CI was green](https://github.com/jabez007/lantern-crossing/actions/runs/44452238087).
Current hosted results are available in [Actions](https://github.com/jabez007/lantern-crossing/actions).
No tag or release is created by this hardening work.

## Runtime handoff — all uncompleted

The owner must complete [acceptance-tests.md](acceptance-tests.md) after a future
26.3 migration. In particular, verify fresh defaults and upgrade preservation,
Light Overlay F7 and Continuity activation once those configuration choices are
migrated, client startup, vanilla-server join/reconnect, rendering and inventory
interaction. First audit and pin the 26.3 artifacts and full dependency closure;
current static checks establish only the retained 26.2 bootstrap contract.
