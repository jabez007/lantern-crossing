# Version and update policy

`pack.toml` owns the pack version. It must use
`26.2.<pack major>.<pack minor>.<pack patch>`. The initial version is
`26.2.0.1.0`, and its matching release tag is `v26.2.0.1.0`.
The current development baseline is `26.2.0.7.0`.

Increment major for intentional policy or selection changes that require users
to review their setup. Increment minor for compatible feature additions or
substantial sets of mod updates. Increment patch for scoped fixes, config
corrections, or small compatible updates. The Minecraft prefix stays 26.2.
A new Minecraft target requires a separately authorized version line.

## Version branches

`26.2` maintains the Minecraft 26.2 pack, including the audited 37-feature
baseline. `26.3` is the default development branch for work on Minecraft 26.3.
The former `main` branch is renamed to `26.2`; it is no longer an update target.

The 26.3 bootstrap still declares Minecraft 26.2 and pack version 26.2.0.3.0,
with 30 features. The maintained 26.2 line now has 37 features: the original 30,
Renice Shot, Sodium Extra, Reese's Sodium Options, Continuity, Cubes Without
Borders, More Chat History, and the Configured Defaults helper. Shared tooling fixes
are backported separately; target-specific pins are preserved.

[migration.toml](../migration.toml) tracks all 37 by stable project ID, including
the six additions after the original baseline and Configured Defaults. Discovery on
2026-11-19 found a release-designated Fabric 26.3 artifact for every feature.
These version IDs are discovery evidence, not installed pins or compatibility
audits. Every migration entry remains `deferred` and runtime `pending`.

Migration status distinguishes `static-verified`, `awaiting-upstream`,
`replacement-required`, `deferred`, and `manual-acceptance-required`; runtime
acceptance is recorded separately. Every entry needs a reason and evidence.
The source line must cover its entire active feature set; the bootstrap may have
only a subset. Validation rejects claims of migrated static checks while the
actual target remains 26.2. Refresh discovery explicitly; do not infer migration
from the existence of a newer upstream file.

To qualify 26.3: separately authorize migration; audit exact release artifacts,
client-only behavior, native ranges and complete dependency closure for all
intended selections; resolve each inventory entry; update manifests, target
validators and pack version together; repeat deterministic exports; then have
the owner complete runtime acceptance and record its exact pack hash. Missing
upstream versions require an explicit blocker or reviewed replacement decision.
No 26.3 compatibility or runtime result is claimed here.

Create topic branches from the intended version branch and target that branch
in pull requests. Backport shared fixes in separate reviewed changes. Do not
synchronize the two lines wholesale or merge target-specific dependency updates
across them. Keep each line's pack version and release tags aligned with its
actual Minecraft target.

`release-policy.toml` declares the intended version branch. Numeric branch names
(from Git locally or the PR base/push ref in CI) must agree with that declaration.
Topic branches inherit their intended line's policy. `pack.toml` always owns the
actual Minecraft target and its version prefix.

Normal exports use the development channel. Filenames include the actual pack
version and `-dev-<version branch>`; the archive's `versionId`, name and summary
also identify development status, actual target and branch. Thus the 26.3
bootstrap produces `lantern-crossing-26.2.0.3.0-dev-26.3.mrpack`. Renaming the
file does not change its internal identity, and archive validation checks both.
Release-channel naming is allowed only after the qualification checks below.

The workflow validates both version branches and PRs targeting them, compares
two exports byte for byte, and uploads the exact named archive and checksum.
Matching tags use the release channel, require tag ancestry on the policy's
remote version branch, and cannot bypass qualification by using a development
build. Index refresh is checked before export and source cleanliness afterward.

Discover availability for the next target without changing the pack:

```sh
python3 scripts/check_target_readiness.py --minecraft 26.3 --scope requested
```

This online discovery check does not audit dependency closure or prove runtime
compatibility. The offline snapshot remains evidence for its recorded target.

## Selection stability and upstream dependencies

Lantern Crossing selects release-designated feature versions. Upstream-declared
dependency closure may contain prerelease-versioned libraries when those exact
versions are required or bundled by the selected release.

The collection roles determine how validation applies:

| Kind | Policy |
| --- | --- |
| Selected feature | Require upstream `version_type = "release"`, Fabric, and Minecraft 26.2. |
| Selected platform or library | Require upstream release designation and the same target checks. |
| Resolved dependency | Require a legitimate, reachable dependency edge, exact lock, and client compatibility. A prerelease designation or identifier also requires exact upstream provenance. |
| Bundled implementation component | Audit the component inside the upstream artifact. The containing artifact's content hash pins it, including any prerelease-looking version name. Reject server-only modules. |

Upstream release designation governs intentional selections. An identifier
containing `pre`, `beta`, or `SNAPSHOT` in official dependency closure does not
change the feature artifact's release designation.

For a separately installed prerelease-versioned library, retain the original
upstream required-project declaration. An upstream exact version ID establishes
the pin directly. If upstream names only a project, record `audited_version` on
that parent's `client_required` edge, with `evidence` pointing to the parent's
exact Modrinth version API record. Record the exact declared version string in
`upstream_version` and the HTTPS source for that declaration in `audit_source`.
Validation requires both the version ID and version string to match the locked
dependency. Mod Menu's release-tagged `gradle.properties` provides that
evidence for Text Placeholder API.

A direct beta or alpha feature is ineligible. A manually added prerelease
library, a substituted version that does not match the audit pin, or an edge
without an upstream requirement is also ineligible. All dependencies must retain
`side = "client"`, exact hashes, and the strict server-independence audit.
Official provenance does not waive a server requirement.

## Update the pack

1. Create a topic branch from the intended version branch and inspect the
   current collection and audit. Target that version branch in the pull request.
2. Run `python3 scripts/check_target_readiness.py`. Query `--scope requested`
   when reviewing excluded requested features. This is availability discovery.
3. Inspect the exact project's Modrinth version metadata and release notes.
   Require Fabric and Minecraft 26.2 explicitly. Require `version_type = "release"`
   for intentional features and selected platform libraries. Apply the dependency
   provenance policy above to required and bundled libraries.
4. Recheck that the selected functionality works without a companion server.
   An optional server label does not establish eligibility. Document evidence
   and reject ambiguous requirements or material conflicts.
5. Install an exact version with
   `packwiz modrinth install --project-id PROJECT_ID --version-id VERSION_ID`.
   Let packwiz resolve dependencies, then inspect every result. Packwiz can pick
   a dependency that needs an exact upstream audit pin or miss a dependency
   absent from Modrinth metadata. Do not substitute arbitrary prereleases.
6. Set every active record to `side = "client"` and `pin = true`, including
   libraries. Keep normal Modrinth download and update fields. Do not commit JARs.
7. Inspect root and bundled `fabric.mod.json` files from the hash-verified
   artifacts. Record the client-required project edges and bundled modules in
   `docs/upstream-metadata.json`. Preserve Modrinth dependencies as evidence.
   Pin prerelease-versioned external dependencies on their upstream requirement
   edges. Any loader-specific exception needs an exact parent version, reason, and URL.
   Do not ignore dependency declarations merely because they are inconvenient.
8. Update `collection.toml`, the dated snapshot, the audit, configuration notes,
   README, release notes, and version. Exact pins remain authoritative in packwiz records. Update
   `required-by` for libraries from the resulting graph. Remove orphan libraries.
9. Run `make refresh`, `make test lint validate`, and `make checksum`. A second
   `make refresh` must leave `pack.toml` and `index.toml` unchanged. Compare two
   clean exports byte for byte and inspect the archive contents.
10. Complete the clean-client [acceptance checklist](acceptance-tests.md),
    particularly the vanilla-server join and affected interactions. Record the
    result in `docs/verification.md` with the tested version and environment.

## Promote a candidate

Add future proposals to `candidates.toml` with a project ID, slug, proposed
category, rationale, status, client-only verification state, target support
state, blockers, and promotion criteria. Candidate metadata or files stay outside
the active index. Never place a candidate lock in `mods/` as a staging shortcut.

Promotion is a deliberate change to the active collection and audit, followed by
exact pinning, dependency closure, and acceptance. Remove its candidate entry at
promotion. If it changes the original requested feature set, update the audited
intent list in the snapshot as part of that reviewed change.

## Publish a release

Complete review and owner-run runtime acceptance before publishing. In
`release-policy.toml`, record the accepted pack version, SHA-256 of `pack.toml`,
and the path of the owner-authored acceptance evidence under `docs/`. The pack
hash binds the loader and complete index, including mod locks and configuration.
Any subsequent pack/index change invalidates that acceptance. The fields remain
empty until the owner actually performs the checklist. Static tests never set them.

Check and build a qualified release with:

```sh
python3 scripts/release_metadata.py --channel release --tag v26.2.0.7.0
make release RELEASE_TAG=v26.2.0.7.0
```

Without qualification these commands intentionally fail. Development validation,
`make export`, and `make checksum` remain available. A qualified release retains
`lantern-crossing-<version>.mrpack` and `.sha256` names; release tag and pack
version must match, and the policy branch must equal the actual Minecraft target.
A migration-line release also requires the entire intended inventory migrated
and each feature's runtime acceptance recorded.
The 26.3 bootstrap therefore cannot publish a release in its current state.

Create and push a matching tag only with publication authorization. GitHub Actions
performs the same checks and confirms that the tag commit belongs to the remote
version branch before publishing through a draft release. It refuses to replace
published releases. Correct a published artifact with a new version and tag.

The release format is `.mrpack`. No CurseForge ZIP is produced. Adding another
format requires a concrete use case and review of its redistribution behavior
and the individual mod licenses.

## Native Fabric requirements

The offline checker also evaluates native `depends` and hard `breaks` against
pinned root modules, bundled modules, `provides` aliases, Minecraft, Fabric
Loader, and the declared minimum Java major in `collection.toml`. Optional
`recommends`, `suggests`, and soft `conflicts` do not become required edges.
Failures name the declaring module, requirement, and installed version.

This is a conservative partial implementation of
[Fabric Loader 0.20.1 predicates](https://github.com/FabricMC/fabric-loader/blob/0.20.1/src/main/java/net/fabricmc/loader/impl/util/version/VersionPredicateParser.java),
not ordinary npm SemVer or Python packaging versions. It supports exact and
ordered numeric bounds, arbitrary numeric component counts, prereleases, ignored
build metadata, space-separated AND, array OR, caret, tilde, trailing wildcards,
and Fabric's equality handling of opaque labels. In particular, Fabric's caret
behavior for major zero differs from npm. Python SemVer/PEP 440 libraries do not
provide these semantics directly; adding one would still require an adapter.

Unsupported syntax, non-ASCII version cores, opaque ordering, ambiguous bundled
alternatives, and duplicate mandatory IDs fail visibly. Root artifacts are
mandatory; among bundled copies the checker considers the newest version. A
constraint requiring selection of a different bundled copy requires Loader's
resolver and is reported as unevaluable. This does not implement Loader's full
SAT/backtracking selection algorithm or prove runtime compatibility. The Java
requirement checks the declared baseline, not the user's actual JVM.

Offline conformance fixtures record results from Loader's public API and the
exact Maven artifact SHA-256. The small Java adapter in `tests/fixtures/` allows
maintainers to regenerate that evidence outside Minecraft; normal tests require
neither Java, downloaded JARs, nor network access.
