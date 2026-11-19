This is a development bootstrap for the 26.3 version branch, not a Minecraft
26.3-compatible release. Its actual target remains Minecraft 26.2, Fabric Loader
0.20.1, pack 26.2.0.3.0, with the original 30 features and nine libraries.

Shared native dependency checks, artifact naming and release safeguards have
been backported. No mod pins or configuration payload have changed. Development
exports are named lantern-crossing-26.2.0.3.0-dev-26.3.mrpack and carry the same
actual-target/development identity internally. Release publication is blocked.

The migration inventory tracks all 37 features intended from the maintained
26.2 line, including its six later additions and Default Options. Their 26.3
artifacts, dependencies and client-only behavior await a separate migration audit.
The bootstrap retains older direct config overrides; do not use it to update an
existing player profile. Use the maintained 26.2 line for its safer defaults.

No Minecraft runtime acceptance has been performed. See verification.md and
acceptance-tests.md for the remaining owner-run work.
