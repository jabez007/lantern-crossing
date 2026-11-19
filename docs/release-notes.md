Lantern Crossing 26.2.0.6.0 is a Minecraft Java 26.2 Fabric client pack.
Server operators do not need to install anything.

The baseline now contains 37 intentional features and nine libraries. This
revision adds Default Options for safer first-install settings. All 45 preceding
mod pins remain unchanged. No new library download is required. Sodium 0.9.2
and Iris 1.11.4 stay pinned.

Continuity's built-in connected-texture and glass-pane packs are seeded using
the same ordering as FO 14.1.2. No standalone resource pack or shader is added.
Other new mod settings retain upstream defaults. Light Overlay stays on F7 and
Renice Shot screenshots stay on F9; Iris starts with shaders disabled.

Config Manager, Ixeris, and ModernFix-mVUS were investigated and remain staged.
Config Manager has contradictory upstream environment metadata; the other two
still need the documented review, measurements, and runtime checks. None is
included in this release artifact.

The .mrpack contains pinned download references and documented configuration.
The .sha256 file verifies the archive bytes. Static CI does not replace the
clean-client and vanilla-server acceptance checklist. Runtime acceptance is
still outstanding; see docs/verification.md and docs/acceptance-tests.md.

Default Options now seeds first-install settings and missing mod config files.
Saved preferences are preserved. No root options.txt, server list or runtime
journal is distributed. Existing profiles may need F7 and Continuity selected
manually; the pack no longer replaces their preference files.

Exports default to a development channel labeled with actual target and version
branch. Release publication requires a matching target/tag and an owner acceptance
record bound to the pack hash. The 26.3 bootstrap still targets 26.2 and cannot
publish a 26.3 release. Its migration inventory tracks all intended features.
Native Fabric dependency predicates are now checked offline, with unsupported
semantics reported explicitly. This is not a substitute for Loader's full
resolver or runtime acceptance.
