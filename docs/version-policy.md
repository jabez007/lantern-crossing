# Version and update policy

`pack.toml` owns the pack version. It must use
`26.2.<pack major>.<pack minor>.<pack patch>`. The initial version is
`26.2.0.1.0`, and its matching release tag is `v26.2.0.1.0`.
The current development baseline is `26.2.0.3.0`.

Increment major for intentional policy or selection changes that require users
to review their setup. Increment minor for compatible feature additions or
substantial sets of mod updates. Increment patch for scoped fixes, config
corrections, or small compatible updates. The Minecraft prefix stays 26.2.
A new Minecraft target requires a separately authorized version line.

## Version branches

`26.2` maintains the Minecraft 26.2 pack, including the audited 30-feature
baseline. `26.3` is the default development branch for work on Minecraft 26.3.
The former `main` branch is renamed to `26.2`; it is no longer an update target.

At branch creation, `26.3` inherits the verified 26.2 sources unchanged. Its
`pack.toml`, pins, validation target, and acceptance evidence still describe
Minecraft 26.2. Creating the branch does not complete or qualify a 26.3 upgrade.
Before claiming 26.3 support, audit exact upstream releases and dependencies,
update the target and its validation together, and repeat export and runtime
acceptance. Preserve the 26.2 pins on the retained line.

Create topic branches from the intended version branch and target that branch
in pull requests. Backport shared fixes in separate reviewed changes. Do not
synchronize the two lines wholesale or merge target-specific dependency updates
across them. Keep each line's pack version and release tags aligned with its
actual Minecraft target.

The existing `Validate and release` workflow runs the full validation and export
checks on pushes to either version branch and pull requests targeting them.
Topic pushes do not duplicate PR runs. Matching `v*` tags retain the release
workflow and tag-to-`pack.toml` checks.

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
9. Run `make refresh`, `make test lint validate`, and `make release`. A second
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

Complete review and runtime acceptance before tagging a build intended for
users. Validate the proposed tag with
`python3 scripts/release_metadata.py --tag v26.2.0.3.0`.
Create and push the matching tag only with publication authorization.
GitHub Actions then checks the same sources, builds the `.mrpack` and checksum,
and publishes both through a draft release. It refuses to overwrite a published
release. Correct a published artifact with a new version and tag.

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
