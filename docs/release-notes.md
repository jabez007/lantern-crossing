Lantern Crossing 26.2.0.6.0 is a Minecraft Java 26.2 Fabric client pack.
Server operators do not need to install anything.

The baseline now contains 37 intentional features and nine libraries. This
revision adds Sodium Extra, Reese's Sodium Options, Continuity, Cubes Without
Borders, and More Chat History. All five use exact upstream release-designated
Fabric 26.2 artifacts, and all 40 existing mod pins remain unchanged. No new
library download is required. Sodium 0.9.2 and Iris 1.11.4 stay pinned.

Continuity's built-in connected-texture and glass-pane packs are enabled using
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
