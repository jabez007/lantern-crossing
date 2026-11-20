# Version and update policy

`pack.toml` owns the version, using `<Minecraft>.<major>.<minor>.<patch>`.
The current development baseline is `26.3.0.1.0`.
Increment major for policy or selection changes requiring setup review, minor
for compatible additions or substantial updates, and patch for scoped fixes.
The Minecraft prefix must equal the actual target. The 26.2 maintenance line
keeps its own version sequence and release evidence.

## Version branches

**Primary branch: `26.3`. Maintenance branch: `26.2`.** GitHub defaults to 26.3.
Each numeric branch must target its own Minecraft release, for development and
release builds alike. Topic branches declare their destination version line in
`release-policy.toml`; target PRs at that line. Release tags must match the pack
version and their commit must belong to the appropriate remote version branch.

Migration moves the complete curated 26.2 inventory forward to 26.3, preserving
history. It does not imply that 26.2 passed runtime acceptance. The source is
41 feature mods, eleven libraries and two optional shaders at pack 26.2.0.10.0.
`migration.toml` schema 2 records every source artifact, exact source and target
versions, roles, dependencies, static status, evidence and separate runtime state.
The [human matrix](mod-audit.md#263-artifact-migration-matrix) covers the same set.
No source feature was dropped or replaced. All runtime states remain pending.

Changes flow primarily from 26.3 to 26.2. Backport important relevant bug,
security/privacy, configuration, installation, packaging, validation and
documentation fixes after reviewing 26.2 compatibility. Do not automatically
backport new mods, shaders or upstream upgrades. Never merge the 26.3 lock graph
wholesale. Run the maintenance branch's own tests, refresh, export and repeated
byte comparison; invalidate its acceptance if its pack/index changes.

## Feature freeze

Keep the accepted inventory frozen during migration and owner runtime acceptance.
Only compatibility fixes, broken dependencies, bugs, security/privacy issues,
incorrect defaults, test failures and release documentation should change now.
No speculative QoL or optimization additions. After qualification, new work
starts on 26.3; 26.2 remains selective maintenance.

The migration does not qualify either branch for release. Each branch requires
its own owner-led [acceptance checklist](acceptance-tests.md) and pack-hash-bound
record. Successful CI is a development-package check, not runtime acceptance.
Do not force-push, rewrite published history or delete either version branch.

## Artifacts and discovery

Development filenames append only `-dev` to the pack version:
`lantern-crossing-26.3.0.1.0-dev.mrpack` and `.sha256`.
The generated manifest version is `<pack-version>-dev`; a qualified release uses
`<pack-version>` with no development suffix. Checksums and GitHub Actions
artifact names use the same basename. Branch/target validation remains mandatory
independently of naming; the manifest retains its branch/target labels.
Qualified release names omit the development suffix. A tag alone cannot bypass
branch/target agreement, exact pins, full migration disposition or owner acceptance.

Shader resources are separate from Fabric mods. `shaderpacks/*.pw.toml` owns
exact ZIP versions, URLs and hashes. Their audits bind the exact reviewed Iris
artifact. Upstream license grants and credits remain mandatory; do not upload
ZIP overrides. Both download choices start disabled when Iris has no saved
preferences. Existing selections and presets remain authoritative.

```sh
python3 scripts/check_target_readiness.py --offline
python3 scripts/check_target_readiness.py --minecraft 26.3 --scope requested
```

Discovery reports availability only. It neither updates pins nor proves closure,
client independence, rendering correctness or runtime acceptance.

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
python3 scripts/release_metadata.py --channel release --tag v26.3.0.1.0
make release RELEASE_TAG=v26.3.0.1.0
```

Without qualification these commands intentionally fail. Development validation,
`make export`, and `make checksum` remain available. A qualified release retains
`lantern-crossing-<version>.mrpack` and `.sha256` names; release tag and pack
version must match, and the policy branch must equal the actual Minecraft target.
A migration-line release also requires the entire intended inventory migrated
and each artifact's runtime acceptance recorded.
The 26.3 migration cannot publish until all artifact runtime states and the
owner acceptance record are complete. Nothing is marked accepted by CI.

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

## Project environment metadata disagreements

A contradictory Modrinth server label can be corrected only by an explicit
`environment_exceptions` audit in the existing upstream snapshot. The audit must
name a resolved dependency, its exact project/version, filename, SHA-512,
canonical Fabric-descriptor SHA-256, Minecraft target, loader and observed labels.
It also binds every requiring feature's exact version and artifact identity and
requires the real upstream required-project edge. Evidence links, review reference
and a reason are mandatory. Repository and archive CLI checks print `AUDIT` notices.

The exception applies only to Modrinth's project-level `server_side` label.
Unsupported clients, native server-only modules, download integrity, required
version ranges, complete closure and client-only export rules remain enforced.
Changed pins, descriptors, parents or metadata require re-evaluation. Duplicate,
orphan and stale audits fail; a corrected upstream label requires removing the
obsolete exception. This is a human-reviewed source/artifact finding, not a
mechanical proof of runtime behavior or permission to allow other server mods.
