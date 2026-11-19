Lantern Crossing is a Minecraft Java 26.2 Fabric client pack. Server operators
do not need to install anything.

This development baseline contains the original 30 features plus Renice Shot,
for 31 intentional features and nine libraries.
Mod Menu, Sign Tweaks, Iris, and Client Tweaks are active upstream releases.
Their exact official dependency closure may include prerelease-versioned libraries.
Light Overlay 2.12.0+26.2 is active from project 8qVa1XCN, with its exact
OverlayLib 0.12.0+26.2 dependency. Renice Shot 1.2.1+mc26.2 supplies the F9
high-resolution screenshot workflow used by Fabulously Optimized for 26.2.
Light Overlay moves to F7 to avoid the collision. No existing mod pin changes
and no additional library is required.
See the repository's mod audit for evidence and limitations.

The .mrpack references pinned upstream artifacts and includes documented
Mouse Tweaks, Client Tweaks, Iris, and the single Light Overlay keybinding override.
Shaders start disabled and no shader pack is included. The .sha256 file verifies
the archive bytes.

Static CI checks do not replace the clean-client vanilla-server acceptance
checklist. Consult docs/verification.md for the recorded runtime test status.
