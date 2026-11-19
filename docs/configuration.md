# Configuration decisions

This 26.3 development bootstrap still targets Minecraft 26.2 and retains its
original direct configuration overrides. Do not use it to upgrade an existing
player profile. The maintained 26.2 branch has the safe Default Options integration;
that helper and its templates await the separate 26.3 migration audit. See
[the migration inventory](../migration.toml) and [version policy](version-policy.md).

The pack ships `config/MouseTweaks.cfg`, `config/clienttweaks-common.toml`, and
`config/iris.properties`. Other settings retain upstream defaults.
User-generated preferences, key bindings, server addresses,
map caches, and waypoints do not belong in the repository or release archive.

## Defaults manager evaluation, 2026-11-19

**Maintained 26.2 decision: retain Default Options `26.2.0.3+fabric-26.2` (`hS9ZtUOA`).**
This 26.3 bootstrap has not installed that helper or the later features. The
comparison describes the maintained 26.2 implementation and the intended future
baseline. Do not assume the commands or defaults below apply to this bootstrap.

No mod, dependency, template, pack version or release-qualification field changes
in this evaluation. Preservation takes priority over automatically enabling
Continuity when a launcher or player already supplied an options file.

We retained the requested weights: preference preservation 25%, launcher
interoperability 25%, initial defaults 20%, update/reset experience 10%,
maintenance/compatibility 10%, and simplicity 10%. These weights guide judgment,
not measured launcher scores. The first 50% favors preserving existing data and
avoiding competing writers. Default Options supplies our specific defaults and
changes the Controls reset default to F7 without rewriting existing non-key
options. Its missing-file limitation is explicit. Configured Defaults improves
missing-key merging, but that does not solve an existing `resourcePacks` field.
Config Manager's useful UI does not resolve its eligibility blocker.
Our only maintained non-key vanilla default is `resourcePacks`. Configured
Defaults' merge cannot improve that already-present field, while our new key
already has a dedicated handler. Its broader merge capability therefore provides
little benefit for the defaults actually shipped here.

The comparison below uses **V** = Verified supported by metadata/source,
**C** = Supported with caveats, **N** = Not supported, and **U** = Unknown / requires
runtime testing. V is not a Minecraft or launcher acceptance result.

| Capability | Config Manager | Configured Defaults | Default Options |
| --- | --- | --- | --- |
| Release-designated Fabric 26.2 artifact | V: 1.1.4, `okecULrz` | V: 26.2.0, `oM0C4RRZ` | V: 26.2.0.3+fabric-26.2, `hS9ZtUOA` |
| Published Fabric 26.3 release prospect | V: same 1.1.4 | V: 26.3.0, `frAVVzBj` | V: 26.3.0.1+fabric-26.3, `YluujUg3` |
| Strict client-only eligibility today | U: native local behavior conflicts with API environment labels; blocked | V: independently optional client/server installation; local file handling | V: client required, server unsupported; local handlers |
| Copy entirely missing mod files | V: startup copy | V: early language adapter | V: extra-folder early-init handler |
| Preserve existing mod files on normal launch/update | V: existence check | V: existence check | V: existence check |
| Merge missing keys inside existing mod configs | N | N | N |
| Existing options file, even one launcher-created | C: normally skipped; narrow fullscreen workaround below | V: append only missing option keys | C: skip non-key options; separate key handler still applies unseen keys |
| Preserve existing valid option values and resource-pack order | V in normal copy mode | C: put-if-absent preserves values, but a merge rewrites parsed lines and drops malformed lines/duplicate keys | V: leave existing non-key file untouched; saved keys respected |
| Automatically add Continuity when `resourcePacks` already exists | N in normal mode | N | N under the selected safe policy; optional replacement handler is deliberately unused |
| F7 for unseen overlay binding; F7 as Controls reset default | C: missing whole options file only; no separate binding-default handler | C: absent key can be added; no native reset-default replacement | V: separate handler supplies both and respects seen bindings |
| Newly added defaults after a pack upgrade | C: new files only | C: new files and missing options keys | C: new files and unseen keys; no non-key options merge |
| Deliberate adoption/reset | C: GUI Update overwrites whole target files; Reset deletes config tree | C: manual file removal/edit; no reset GUI found | C: per-key Controls reset; manual edit or per-file re-seed for other settings |
| `.mrpack` template packaging | V: under overrides/config/modpack_defaults | V: under overrides/configureddefaults | V: under overrides/config/defaultoptions |
| Prism launch/import/upgrade behavior | U | U | U |
| Modrinth App with settings sync on/off | U; narrow fullscreen case is not general sync support | U; preserves fields already supplied by sync | U; respects saved fields/keys, cannot control App synchronization |

### Exact identities, dependencies and maintenance

- **Config Manager** is TheBossMagnus's `configmanager`, project `jlNms3Jp`,
  [source](https://github.com/TheBossMagnus/Config-Manager/tree/adf332de967b8eef237fa5ffb0f020688548dcc0),
  not the unrelated `config-manager` serializer. [Release 1.1.4](https://api.modrinth.com/v2/version/okecULrz)
  was published 2026-11-17 and lists Fabric 26.2/26.3. Native Minecraft range is
  `>=26.1`, with no declared Loader minimum. The API requires Mod Menu; its
  native descriptor suggests it instead. Our existing Mod Menu and official
  dependency closure would cover that requirement. No extra library was found
  in the audited JAR. The [project API](https://api.modrinth.com/v2/project/jlNms3Jp)
  still says client unsupported/server required. Source inspection suggests local
  operations, not a demonstrated server requirement, but the disagreement remains
  unresolved. Do not bypass the client-only checks or promote it from candidates.
- **Configured Defaults**, project `SISoSFPP`, is Fuzs's
  [source](https://github.com/Fuzss/configureddefaults/tree/1a10697acb2cc415c8f9293bae8d695634c12806).
  Its [release-designated Fabric 26.2 JAR](https://api.modrinth.com/v2/version/oM0C4RRZ) requires Minecraft `~26.2-` and Loader
  `>=0.19.0`, satisfied by 0.20.1. The API declares no required projects, and
  no bundled JARs were found. Client and server installations are independently
  optional; no companion or networking is selected. The tagged source's metadata
  file retains older version text, so the hash-verified release JAR's descriptor
  is authoritative for these target requirements. Its 26.3 release was published
  2026-09-22; an older-line update followed on 2026-09-26.
- **Default Options**, project `WEg59z5b`, has release-designated versions for both
  targets. The selected 26.2 release was published 2026-07-24; its 26.3 successor
  on 2026-09-16. Native Loader minimum is `>=0.19.3`, Java `>=25`, and Minecraft
  `~26.2-`. Required Fabric API and Balm are already pinned. Default Options requires
  `balm-fabric >=26.2.0.1`; our 26.2.0.9 pin remains unchanged. No additional dependency or
  bundled implementation is introduced by retaining it.

All three have maintained source and current target releases. No dedicated
upstream test source was found in the inspected candidate snapshots. Default
Options has the most detailed handler/command documentation; Configured Defaults
relies mainly on its project page, code and generated README. Config Manager's
code and guide make its reset flags explicit, but its README's description of
Update can sound like a per-setting merge. `OverwriteConfig` actually replaces
whole files; `ResetAndCopyConfig` removes the config directory's other contents.
Neither action is a safe automatic pack-update mechanism for Lantern Crossing.

### First-run state and update semantics

[Configured Defaults' file handler](https://github.com/Fuzss/configureddefaults/blob/1a10697acb2cc415c8f9293bae8d695634c12806/Common/src/main/java/fuzs/configureddefaults/common/handler/CopyDefaultsHandler.java)
uses a per-process initialization guard, not a persistent first-run journal. On
clients, its adapter enables options merging on each startup. Existing values win
through `putIfAbsent`; it writes only if new keys were added. Existing mod files
are still skipped in their entirety. Its copy targets use paths relative to the
process working directory, while option merging uses the provided game path.
Normal launcher working-directory behavior remains part of acceptance.

[Config Manager's normal copy](https://github.com/TheBossMagnus/Config-Manager/blob/adf332de967b8eef237fa5ffb0f020688548dcc0/common/src/main/java/io/github/thebossmagnus/mods/config_manager/common_coremod/CopyConfig.java)
checks files every startup. Update/reset are explicit flag-file operations invoked
by its GUI, not value-aware merge tracking. Its
[Modrinth workaround](https://github.com/TheBossMagnus/Config-Manager/blob/adf332de967b8eef237fa5ffb0f020688548dcc0/common/src/main/java/io/github/thebossmagnus/mods/config_manager/common_coremod/compat/ModrinthAppCompat.java)
handles only an options file with at most two nonblank lines and a fullscreen
setting. It temporarily removes that file, copies defaults, and restores the
fullscreen value. It does not recognize arbitrary synced settings or prove
compatibility with current Modrinth settings synchronization.

Default Options checks missing files on startup and tracks seen keys from saved
options. Its journal records the resource-pack handler separately; it is not a
record of which whole files or individual mod settings were customized. The
[new resource-pack mechanism](https://mods.twelveiterations.com/minecraft/default-options/config)
can operate despite a launcher-created options file, but its guard is the absence
of a journal entry. It cannot tell a fresh launcher file from a customized
existing resource-pack list. Missing/corrupt/deleted journals can allow another
application. Lantern Crossing therefore keeps `defaultResourcePacks` empty and
rejects packaged manager configs that would activate it. This is a deliberate
preservation decision, not an unsupported launcher workaround.

### What FO does, and what we reuse

At [FO commit ef27a0b](https://github.com/Fabulously-Optimized/fabulously-optimized/tree/ef27a0ba425721fdaa8255251f01ed1301249cf4),
its 26.2 and 26.3
[Config Manager locks](https://github.com/Fabulously-Optimized/fabulously-optimized/blob/ef27a0ba425721fdaa8255251f01ed1301249cf4/Packwiz/26.2/mods/config_manager.pw.toml)
still select 1.1.3 (`W4C08wBC`), with `side = "both"`. That is distinct from the
latest 1.1.4 candidate audited here and does not meet our packaging policy.

FO's [template tree](https://github.com/Fabulously-Optimized/fabulously-optimized/tree/ef27a0ba425721fdaa8255251f01ed1301249cf4/Packwiz/26.2/config/modpack_defaults)
mirrors the game directory, including graphics and UI preferences, mod configs,
and `options.txt`. Keybindings and the selected resource-pack list are together
in that options template, not managed through Default Options' separate key
handler. The list includes FO-specific helper/translation packs and Continuity.
Its [publish workflow](https://github.com/Fabulously-Optimized/fabulously-optimized/blob/ef27a0ba425721fdaa8255251f01ed1301249cf4/.github/workflows/auto-publish.yml)
runs Packwiz's Modrinth export, which carries those templates in `overrides/config/`.
We reuse the distinction between packaged defaults and live user files, not FO's
broader graphics choices, helper packs, side labels or reset operations.

FO's [changelog](https://github.com/Fabulously-Optimized/fabulously-optimized/blob/ef27a0ba425721fdaa8255251f01ed1301249cf4/CHANGELOG.md)
records the YOSBR replacement in 12.0.0-beta.3 on 2026-01-17 and 11.3.0 on
2026-01-31, citing reset options and improved compatibility. Its
[update guide](https://wiki.download.fo/update-instructions) explains that normal
upgrades preserve settings and deliberate resets adopt newer defaults. The
fullscreen workaround lives in Config Manager itself; no equivalent launcher
config workaround is added to Lantern Crossing. Current App synchronization is
a broader concern than the workaround described in that source.

### Prism and Modrinth App

[Prism documents `.mrpack` imports](https://prismlauncher.org/wiki/getting-started/download-modpacks/).
Our archive supplies templates instead of live preferences. The exact state of
`options.txt` before launch depends on the profile and launcher version. Record
it rather than assuming Prism always creates or always omits the file.

[Modrinth's synchronization documentation](https://modrinth.com/news/article/sync-settings/)
describes bidirectional per-setting sync, per-instance overrides, and custom mod
options synced by default. Synced values can take precedence over pack options.
Resource-pack sync is separately configurable; the App says modpack-included
packs are not propagated like user-added packs. Whether built-in Continuity IDs
and our key behave as expected in the installed App version still needs testing.

We ship no launcher settings or sync configuration. Existing saved/synced keys,
including an intentional F9 binding, win over our unseen-key default. If that
conflicts with Renice Shot, deliberately change Light Overlay to F7 and, where
the App supports it, exclude that setting from global synchronization for this
instance. Do not disable all user sync automatically or fight it on every launch.
When options already exist, enable Continuity manually in Resource Packs and
keep any personal packs in the desired order.

A local `.mrpack` import does not itself establish an upstream project link for
automatic updates. Use a launcher-supported upgrade path if available for that
instance. Do not treat importing a second instance as an in-place upgrade.
The owner must record the actual upgrade path used. This evaluation does not
publish a Modrinth project or promise either launcher's automatic update UI.

### Deliberately adopt updated defaults

Default Options' [save commands](https://mods.twelveiterations.com/minecraft/default-options/commands)
capture the current setup for pack authors. They are not reset commands.
Do not use `saveAll` to adopt the shipped defaults or delete the journal as a
routine update step.

- To reset only Light Overlay, use that action's reset control in Controls, then
  verify F7. Leave other keybindings alone. A global App preference may need a
  deliberate per-instance exception.
- To enable Continuity, select its two built-in packs in Resource Packs. Preserve
  the desired order of personal packs. No file deletion is necessary.
- To adopt an individual new mod setting, change that setting through its UI or
  edit that field with the game closed. Existing config files are not merged.
- To reset an entire maintained mod config, close Minecraft, save a copy of that
  specific live file, and move it out of the way. The next launch re-seeds the
  absent file. This resets all settings in that file, not just fields changed by
  the pack. Do not remove the entire config directory or root options file.

Existing 26.2.0.6.0 installations keep the same manager, templates and journal;
there is no defaults-manager migration or cleanup. For older installations that
received direct overrides, preserve options/configs before testing the launcher's
upgrade behavior in a disposable copy. The defaults mod cannot restore settings
an older installer already overwrote or prevent a launcher deleting old overrides.
Obsolete Config Manager/YOSBR/Configured Defaults trees are rejected in source,
not silently deleted from player instances. Remove another manager from a
personal profile before combining it with Lantern Crossing.

### File-handler evidence and automation limits

Seven isolated fixtures executed the unmodified pinned Default Options
`SimpleDefaultOptionsFileHandler` and `ExtraDefaultOptionsHandler`, context,
interfaces and exception source with `DefaultOptionsFilesOracle.java`. Observations
and source/template hashes are in `tests/fixtures/default-options-files.json`.
The fixtures cover absent options, launcher-created options, personalized files,
repeat application, added defaults during an update, custom resource packs with
no journal, and an existing journal followed by deliberate per-file re-seeding.

The audit compiled those source files on JDK 17.0.21.1 outside the repository.
Apache Commons IO 2.20.0 supplied real file copying and was checked against
Maven's published SHA-1; its SHA-512 is recorded in the fixture. Only logging,
a nullability annotation and a fail-on-use Minecraft type for deprecated API
methods were stubbed. No Minecraft initialization, keymapping, resource repository
or launcher ran. This verifies the isolated file methods, not startup ordering,
F7 application, actual rendering or launchers. Ordinary Python tests only bind
these recorded observations to the current artifact/template hashes; they do not
rerun Java or substitute a Python implementation of mod behavior.

Validators reject competing manager IDs, obsolete template trees, reset/update
flags, unsupported template locations, root live preferences and resource-pack
replacement configuration. Existing exact pin, native dependency, client-only,
export and release checks remain in force. The
[launcher acceptance matrix](acceptance-tests.md#launcher-configuration-acceptance-matrix)
contains every remaining runtime check.

## Inventory gestures

IPN owns sorting, scroll transfers, and shift-drag movement. Mouse Tweaks supplies
right-button dragging and left-button dragging with a carried stack.

| Mouse Tweaks key | Pack value | Reason |
| --- | --- | --- |
| `RMBTweak` | `1` | Keep its right-button drag behavior |
| `LMBTweakWithItem` | `1` | Keep its carried-stack drag behavior |
| `LMBTweakWithoutItem` | `0` | Avoid duplicate empty-cursor shift-drag handling with IPN's container swipe |
| `WheelTweak` | `0` | IPN owns scroll transfers |

The [Mouse Tweaks documentation](https://modrinth.com/mod/mouse-tweaks)
defines these keys and the configuration path. IPN's artifact describes
`container_swipe_moving_items` as movement while holding Shift and left click,
and exposes scroll-to-inventory and scroll-to-chest bindings. Verify all gestures
on a vanilla server, including container boundaries and creative inventory.
No second sorting mod is selected. Revisit the override if either project's
input handling changes.

## Rendering and lighting

Sodium owns chunk rendering. ImmediatelyFast batches immediate rendering.
Entity Culling skips locally occluded entity rendering, while More Culling
handles model and block-face culling. The [Entity Culling
FAQ](https://modrinth.com/mod/entityculling) explains how its visibility work
differs from Sodium's coarse checks. Their presence together does not establish
runtime compatibility. Check moving entities, signs, leaves, glass, item frames,
and block entities from several angles before accepting a build.

LambDynamicLights supplies local dynamic lighting. No second dynamic-lighting
implementation is included. Dynamic lights do not change server-side spawning
or block light levels. BadOptimizations' lightmap caching and the rendering stack
need visual testing when a held light, weather, or status effect changes.

Iris 1.11.4 is active with Sodium 0.9.2. `config/iris.properties` sets
`enableShaders=false` so the clean baseline starts with vanilla rendering.
The shader-selection UI remains available. No shader pack is bundled.
Check shader-disabled rendering, resizing, and interactions with dynamic lighting
before accepting the build. If a player adds a shader pack, review its own
dynamic-lighting behavior to avoid enabling the same effect twice.

## Maps and information

Xaero's Minimap uses World Map's map textures when both are installed, as
documented by [Xaero](https://modrinth.com/mod/xaeros-minimap). No second map cache
or external server map is supplied. Terrain recording and waypoints remain local.
Use the World Map's Manual selection mode when a server address can represent
multiple worlds. Server-controlled identification is outside the selected scope.
Teleport buttons require ordinary server command permission and are not a pack
travel feature.

Shulker Box Tooltip is selected for item-contained shulker data sent by vanilla.
Its optional server-assisted ender-chest preview is outside pack intent. Better
Statistics Screen is selected for presenting vanilla player statistics, not its
server commands or additional server-provided data. No config enables those
server integrations.

## Client Tweaks

The exact [26.2.0.6 configuration source](https://github.com/TwelveIterations/ClientTweaks/blob/v26.2.0.6/common/src/main/java/net/blay09/mods/clienttweaks/ClientTweaksConfig.java)
defines these options. The pack pins two existing upstream defaults off in
`config/clienttweaks-common.toml`:

| Key | Value | Reason |
| --- | --- | --- |
| `ui.alwaysPrioritizeExperienceBar` | `false` | Better Mount HUD owns the selected player/mount HUD presentation. Avoid an additional forced bar-priority rule. |
| `mining.doNotUseLastMending` | `false` | IPN owns refill and tool replacement assistance. Avoid a second last-durability input guard. |

Other options retain the release's defaults. Enabled behavior includes volume
sliders, creative and recipe-book search conveniences, ghost-ingredient
navigation, local shield visibility, placement targeting assistance, and local
guards against accidental offhand actions. These use client UI, rendering,
targeting, or suppression of ordinary vanilla inputs. They require no extra
server data or companion mod. No second sorting, wheel-transfer, or inventory
drag implementation is enabled by Client Tweaks.

Automatic ladder climbing, reactive sprinting, step-assist changes, and the other
opt-in tweaks remain at their disabled upstream defaults. Test enabled behavior
and the two explicitly disabled switches on the vanilla acceptance server.

The [Fabric client initializer](https://github.com/TwelveIterations/ClientTweaks/blob/v26.2.0.6/fabric/src/main/java/net/blay09/mods/clienttweaks/fabric/client/FabricClientTweaksClient.java)
registers Client Tweaks and its local config on the client. Balm's
[config interface](https://github.com/TwelveIterations/Balm/blob/v26.2.0.9/common/src/main/java/net/blay09/mods/balm/platform/config/BalmConfig.java)
maps the common config annotation to `config/clienttweaks-common.toml`.
Balm can populate omitted options from upstream defaults on first load.

Mod Menu exposes the active mods' configuration screens. Sign Tweaks and Book
Tweaks retain their upstream editing defaults.

## Light Overlay

Light Overlay retains its upstream defaults. The
[release's key registrations](https://github.com/lugosieben/lightoverlay/blob/7e7647bb424ca8195329c889ce529c5974d11c21/src/main/java/net/lugo/lightoverlay/registration/KeyMappings.java)
bind overlay toggling to F9. Config opening and overlay-mode cycling are unbound.
The config screen is also available from Mod Menu or the client-local
`/lightoverlay config` command. No Light Overlay config or keybind override is shipped.

Static inspection of the pinned artifacts found no competing F9 action in
Xaero's Minimap, Xaero's World Map, Zoomify, BetterF3, Iris, LambDynamicLights,
or the other active utility mods. libIPN defines F9 in its key-code catalog but
does not assign it to an action by default. User-customized bindings can differ;
verify the new instance's Controls screen during acceptance.

Light Overlay and OverlayLib declare no conflicts with the selected Iris/Sodium
stack. The overlay uses client-known world/light data and requires no server
component. This establishes static eligibility, not rendering acceptance.
Test toggling and persistence with Sodium, Iris, and LambDynamicLights installed,
starting with shaders disabled. Dynamic lighting does not change server-side
block light or spawn rules.
