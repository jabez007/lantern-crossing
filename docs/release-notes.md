Lantern Crossing 26.2.0.7.0 remains a Minecraft Java 26.2 Fabric client pack.
Server operators need nothing installed. Runtime acceptance is still pending.

Configured Defaults 26.2.0 replaces Default Options after evaluation of it,
Config Manager and Default Options. It copies missing mod files and adds only
absent keys to options.txt. This handles launcher-created partial files without
replacing saved preferences. A pre-existing resource-pack list, even vanilla
only, still requires manual Continuity activation.

Templates move to configureddefaults/; no live preferences, reset flags, journal,
shader pack or extra feature is distributed. The options data version is pinned
to Minecraft 26.2. Default key seeding is F7; Light Overlay's native Controls reset
is still F9. Deliberately rebind to F7 when adopting the pack default.

Before upgrading an existing instance, verify that the old Default Options JAR
was removed. Its journal and template folder can remain unused. Preserve options
and mod configs; test launcher removal behavior on a disposable copy. Details
and both launcher/sync acceptance cases are in configuration.md and
acceptance-tests.md.

All 45 other mod locks remain unchanged, including Balm and Fabric API.
Configured Defaults adds no required library. Counts remain 37 features and nine
libraries. No staged performance mod was promoted. The 26.3 bootstrap receives
shared tooling and inventory updates only; its actual target stays 26.2.
Development/release naming, reproducibility and owner acceptance gates remain.
