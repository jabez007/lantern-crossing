Lantern Crossing 26.3.1.0.0 refines sign and book authoring on Minecraft 26.3.
Big Sign Writer 3.1.1 and Symbol Chat 1.4.3 replace Sign Tweaks and Book Tweaks.
Books retain the vanilla editor with the shared Unicode palette. The pack has 41 feature mods, eleven libraries and two optional
shader choices. No 26.2 change or backport is part of this milestone.

Large lettering uses ordinary Unicode across existing sign rows. Symbol Chat
provides searchable symbols and Unicode variants across vanilla editors.
Vanilla clients need no companion mod for supported glyphs. Exact visual parity,
filtering, save/reconnect behavior and combined GUI usability remain owner tests.
Sign limits still apply; overflowing large-letter rows can be incomplete.
No book import/export, page reordering or native formatting toolbar is added.

Remove both old editor JARs when upgrading a disposable instance copy. Enhanced
sign wrapping/selection and quick actions, cross-page book tools and remembered
reading positions are gone. Book Tweaks has legacy GLFW dispatch under SDL3 and
a paste path that can consume text without confirming insertion.
Keep existing configs and player content. A missing Symbol Chat config receives
font-selection reset and missing-table-glyph hiding through Configured Defaults;
existing files remain authoritative. [Audit and restrictions](mod-audit.md#writing-refinement).

Minecraft 26.3, Fabric Loader 0.20.1, Java 25 and Fabric API 0.166.2+26.3 remain
the runtime foundation. Sodium 0.9.2 and Iris 1.11.7 remain paired exactly.
All unrelated pins and shader defaults stay unchanged.

Complementary Reimagined r5.10 and MakeUp - Ultra Fast 9.6 retain their official
ZIPs and license notices, with renewed Iris-bound reviews. Both remain disabled
on a clean instance. Existing shader settings and presets are not reset.
Complementary is by EminGT / Complementary Development under Complementary
License Agreement 1.8. MakeUp is by Javier Garduño / javiergcim under its upstream
LGPL-3.0-or-later designation. Official links and required credits remain in
README.md. Lantern Crossing is responsible for shader integration problems.

Configured Defaults 26.3.0 preserves existing files and option values. The existing
options data-version seed remains 5023; the five previous mod templates retain
their settings. The new writing template is also copy-if-missing. SDL3 uses physical-position inputs: inspect keybindings,
mouse gestures, text fields, fullscreen/window modes and Linux Wayland after
upgrade. Copy the old instance before testing; do not assume seamless format
conversion or map-directory reconciliation. Existing screenshots are untouched.

Prickle's contradictory server-required metadata is corrected only for the exact
reviewed26.3 artifact and ED parent, with renewed matching-source/binary evidence.
Its previously disclosed external HTTP update HEAD check remains. Environment
exceptions do not bypass integrity, dependency constraints or client export checks.
MixinExtras 0.5.5 comes from Fabric Loader itself, not a new independent download.

26.3 is the primary/default development and release-candidate branch. 26.2 retains
independent maintenance pins and acceptance records. Backport applicable fixes
selectively; never merge the new dependency graph wholesale. Feature selection
remains frozen during migration and acceptance except for this authorized
26.3-only writing refinement.

The owner reports a passed [initial Prism smoke test](verification.md#initial-prism-launcher-runtime-smoke-test)
for import, startup and gameplay. Full acceptance remains pending, including
Modrinth App, shaders, vanilla-server compatibility, preferences and upgrades.
Successful static CI and this initial smoke test do not qualify release
publication. No release tag or final release-approval record is created.
