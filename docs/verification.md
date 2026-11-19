# Verification record

Release hardening checked on 2026-11-19 for development pack `26.2.0.6.0`.
Minecraft has not been launched. All runtime acceptance remains open.
The preceding 26.2.0.5.0 record is preserved in Git history at `3fa2b8f`.

## Findings and disposition

| Finding | Disposition |
| --- | --- |
| Root `options.txt` could replace player preferences | Confirmed and corrected. Default Options uses copy-if-absent templates and preserves saved keys. Three direct mod overrides also became copy-if-missing templates. Source behavior is audited; launcher ordering and preservation still need manual acceptance. |
| 26.3 branch differs from maintained baseline | Confirmed. Its actual target remains 26.2 with 30 features. Shared tooling is backported without upgrading pins. The migration inventory tracks all 37 intended features, including the six post-baseline additions and Default Options. |
| Misleading development/release artifacts | Corrected. Filenames and internal identity encode actual target, version branch and development channel. Publication additionally requires matching target/tag, branch ancestry and owner-recorded acceptance bound to the pack hash. Neither branch is runtime-qualified. |
| Native dependency presence without version enforcement | Confirmed and materially strengthened. Required predicates and hard breaks are checked against native root/bundle/alias/runtime versions. Unsupported cases fail visibly; full Loader SAT resolution remains outside static validation. |
| Existing deterministic/client-only guarantees | Retained. The previous 45 lock records are byte-identical. No unrelated mod was added, updated or removed. All 46 records remain pinned client-side. |
| Previous CI failures | None found. Before this pass, both version-branch runs were green: [26.2](https://github.com/jabez007/lantern-crossing/actions/runs/44457005743), [26.3](https://github.com/jabez007/lantern-crossing/actions/runs/44452238087). Current results are in [Actions](https://github.com/jabez007/lantern-crossing/actions). |

## Tools and commands

Python 3.12.12, Go 1.24.6, Ruff 0.16.4 and packwiz commit
`170b22d785959dda5876b54b7f16e1b807a57fb6` match CI. Local actionlint is 1.7.12.
Local export commands use
`PACKWIZ='/tmp/lantern-bin/packwiz --cache /tmp/lantern-cache'`.
Audit downloads, compiler tools and cache remain outside the repository.

| Observed command/check | Result |
| --- | --- |
| `make test lint validate` | Passed: 85 offline tests, formatting/lint, complexity threshold 10, exact target/loader/pins, dependency closure and predicates, branch policy, migration inventory, client-only rules and index. |
| `make refresh` twice, then `cmp` on saved `pack.toml` and `index.toml` | Passed, no metadata drift. |
| `make checksum`, then a second `make export` and `cmp` | Passed, byte-identical normalized exports. |
| `python3 scripts/validate_mrpack.py dist/lantern-crossing-26.2.0.6.0-dev-26.2.mrpack` | Passed via export; checks complete mod set, exact downloads/hashes/sizes, environments, config bytes and artifact identity. |
| `sha256sum --check lantern-crossing-26.2.0.6.0-dev-26.2.sha256` from `dist/` | Passed. |
| `python3 scripts/check_target_readiness.py --offline --scope requested` | Passed for all 37 features; discovery only. |
| `python3 scripts/release_metadata.py --channel release --tag v26.2.0.6.0` | Rejected as intended: owner runtime qualification is absent. Synthetic unit fixtures prove qualified 26.2 release naming remains functional. |
| `/tmp/lantern-bin/actionlint .github/workflows/validate.yml` | Passed, including shellcheck integration. |
| `ruff check scripts tests --select C90 --config 'lint.mccabe.max-complexity=8'` | Passed. No changed function exceeds 8; configured maximum remains 10. |
| Prior lock-byte comparison against `3fa2b8f` | Passed for all 45 original mod records. |
| `git ls-files '*.jar' '*.JAR'` | Empty. No upstream binaries are committed. |

The incompatible-loader regression failed with the old presence-only checker,
then passed after native predicate integration. The root-preferences regression
likewise failed before the packaging fix. Existing server-required, server-only
bundle, arbitrary prerelease, staged leakage and project-identity tests remain.
Additional cases cover numeric boundaries, AND/OR, prereleases, opaque labels,
Fabric caret/tilde/wildcards, aliases, missing/incompatible requirements, soft
optional declarations, hard breaks, mandatory roots, and visible unsupported
resolution. Artifact tests reject incorrect branch/channel filenames and labels,
unqualified releases, target/version mismatches and stale acceptance hashes.

## Native predicate evidence and limits

51 committed conformance vectors were evaluated through Fabric Loader 0.20.1's
public `Version` and `VersionPredicate` APIs. Another 500 deterministic comparison
cases matched during implementation. This CLI-only audit did not launch Minecraft.
Loader's Maven JAR SHA-256 is
`d0c5a082e07410aaff9de7ab196aa6b4236002870f9ba3ad5c1260fcce5110ad`.
The source adapter and expected results are in `tests/fixtures/`; no Java runtime
or network is required by `make test`.

The evaluator implements a conservative subset of Loader semantics rather than
ordinary SemVer. It does not implement full SAT/backtracking, non-ASCII version
cores or ordering among different opaque bundled versions. Ambiguous alternative
bundle selection and unsupported expressions fail validation explicitly. Optional
soft declarations are not promoted into requirements. See the detailed
[version policy](version-policy.md#native-fabric-requirements).

## Dependency and artifact changes

Only Default Options was added: project `WEg59z5b`, version ID `hS9ZtUOA`,
release `26.2.0.3+fabric-26.2`. Its [lock](../mods/default-options.pw.toml)
contains the exact URL and SHA-512; its root/bundled metadata and SHA-1/size are
in the upstream snapshot. Existing Balm and Fabric API satisfy its requirements.
No resolved library pin changed. The [mod audit](mod-audit.md) and
[configuration notes](configuration.md#safe-defaults-and-existing-instances)
record the exact release-source evidence and resource-pack handler decision.

`dist/lantern-crossing-26.2.0.6.0-dev-26.2.mrpack` is 27,092 bytes with 46 downloads
and five templates under `overrides/config/defaultoptions/`. Every mod is
client-required and server-unsupported. No root options file, live mod config,
server list, journal, staged payload or JAR is embedded. Its SHA-256 is:

```text
6d38f68adec69416bafd56228380e371d0ca7b6edd7be9666d676a8aea95648e
```

Generated archives and checksums remain ignored. Release-channel artifacts are
not generated or published before owner acceptance.

## Manual acceptance handoff — all uncompleted

The owner must run [acceptance-tests.md](acceptance-tests.md). In particular:

- [ ] Fresh Prism import: determine whether options are pre-created; verify
  initial F7/F9, Continuity selection, inventory defaults and shaders disabled.
- [ ] Existing profile upgrade: distinctive graphics/audio/key/resource-pack/mod
  settings survive installation and two restarts, with and without a journal.
  Existing profiles may need F7/Continuity selected manually.
- [ ] Client reaches the menu with all mods initialized and no dependency warnings.
- [ ] Join and reconnect to an unmodified vanilla 26.2 server with nothing added
  server-side; verify no missing-server-component warnings.
- [ ] Smoke-test rendering with Sodium/Iris/Light Overlay/Continuity/dynamic lights,
  inventory interaction, maps, books/signs and F9 screenshot restoration.

Record actual results and the exact pack hash only after testing. Do not mark
26.3 qualified: availability discovery has not audited its artifacts, resolved
its dependency graph, or tested it at runtime. No additional staged feature is
promoted by this work.
