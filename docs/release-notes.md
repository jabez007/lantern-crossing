Lantern Crossing is a Minecraft Java 26.2 Fabric client pack. Server operators
do not need to install anything.

This development baseline contains 29 of 30 requested features and eight libraries.
Mod Menu, Sign Tweaks, Iris, and Client Tweaks are active upstream releases.
Their exact official dependency closure may include prerelease-versioned libraries.
Light Overlay remains blocked because there is no Fabric 26.2 artifact.
See the repository's mod audit for evidence and limitations.

The .mrpack references pinned upstream artifacts and includes documented
Mouse Tweaks, Client Tweaks, and Iris configuration. Shaders start disabled and
no shader pack is included. The .sha256 file verifies the archive bytes.

Static CI checks do not replace the clean-client vanilla-server acceptance
checklist. Consult docs/verification.md for the recorded runtime test status.
