# Configuration decisions

## Safe defaults and existing instances

[Configured Defaults 26.2.0](https://modrinth.com/mod/configured-defaults/version/oM0C4RRZ)
replaces Default Options in pack 26.2.0.7.0. It is installed only on the client,
requires no additional library projects, and needs nothing on the server.

| Packaged template | Behavior on the client |
| --- | --- |
| `configureddefaults/options.txt` | Adds absent options only: target data version, Continuity selection, and Light Overlay F7. Existing values always win. |
| `configureddefaults/config/MouseTweaks.cfg` | Copies only if the entire live config file is missing. |
| `configureddefaults/config/clienttweaks-common.toml` | Copies only if the entire live config file is missing. |
| `configureddefaults/config/iris.properties` | Copies only if the entire live config file is missing. |

No live `options.txt`, mod config, server list, journal or forced-reset flag is
exported. The early Fabric language adapter calls the file handler before normal
mod initialization. It copies missing mod files and merges missing options keys,
not missing keys inside existing mod config files. Existing graphics, sound,
accessibility, keybindings and resource-pack lists remain authoritative.

A launcher-created file containing only version/fullscreen fields can receive
our absent resource-pack and F7 entries. A file already containing `resourcePacks`,
even `["vanilla"]`, keeps that exact value and order; enable Continuity manually
in that case. A saved F8/F9 overlay binding is preserved. Existing App-synced
preferences can take precedence over pack defaults.

The options template includes data version `4903`, read from `world_version` in
`version.json` inside the SHA-1-verified official Minecraft 26.2 client archive.
The [official version metadata](https://piston-meta.mojang.com/v1/packages/cf103b8fab4900562221bf7f23b72725dd9a914a/26.2.json)
and source hash are recorded in `docs/upstream-metadata.json`. This is format
metadata for modern key serialization, not a graphics preference. Existing
version fields are not overwritten. Inspecting the ZIP did not execute Minecraft.

Merging rewrites the options file only when adding keys. It preserves existing
parsed values, but malformed lines and duplicate keys are not preserved verbatim.
Use a copy of an existing profile when testing upgrades. Configured Defaults
uses no persistent first-run journal; its per-process guard prevents duplicate
initialization, and subsequent launches recheck for missing files/keys.

## Defaults manager evaluation, 2026-11-19

**Decision: select Configured Defaults 26.2.0 (`oM0C4RRZ`, project `SISoSFPP`).**

We retained the requested weights: preference preservation 25%, launcher
interoperability 25%, initial defaults 20%, update/reset experience 10%,
maintenance/compatibility 10%, and simplicity 10%. These guide engineering
judgment, not measured launcher scores. Configured Defaults wins the concrete
partial-options case while preserving existing values. That matters more under
the combined 45% interoperability/initial-default criteria than Default Options'
better native key-reset behavior. It has no extra dependency projects or
persistent journal and remains eligible under our strict client-only policy.

Current [Modrinth App launch code](https://github.com/modrinth/code/blob/a22ebc163b21bb266a58957338dd2d8789298b0d/packages/app-lib/src/api/instance/synced_options/game_options/launch_overrides.rs)
can create options before Minecraft, and
[its document initializer](https://github.com/modrinth/code/blob/a22ebc163b21bb266a58957338dd2d8789298b0d/packages/app-lib/src/api/instance/synced_options/game_options/options_file.rs)
starts with only the data version. Fullscreen overrides can therefore leave a
partial file. Configured Defaults fills our absent fields safely; Default Options'
non-key file handler skips the whole existing file. Neither can safely replace
an already populated resource-pack choice. App source is not a claim that a
particular installed version was runtime-tested.

Default Options remains a viable preference-preserving alternative, especially
for pack-defined Controls reset defaults. Config Manager has a useful UI, but
its environment metadata remains contradictory and its reset operations are too
broad for automatic upgrades. See the source evidence and tradeoffs below.

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
| Preserve existing valid option values and resource-pack order | V in normal copy mode | C: put-if-absent preserves values, but a merge rewrites parsed lines and drops malformed lines/duplicate keys | V: existing option values and saved keys respected; applying a new key can trigger Minecraft’s normal save |
| Automatically add Continuity when `resourcePacks` already exists | N in normal mode | N | N under a preservation policy; optional replacement handler would replace the list |
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
  targets. The previously used 26.2 release was published 2026-07-24; its 26.3 successor
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
application. Lantern Crossing therefore removes that manager and rejects packaged configs
that would activate its replacement handler. This is a deliberate
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
including an intentional F9 binding, win over our missing-key default. If that
conflicts with Renice Shot, deliberately bind Light Overlay to F7 and, where the
App supports it, exclude that setting from global synchronization for this
instance. Do not disable all user sync automatically or fight it every launch.
When a resource-pack field already exists, enable Continuity manually and keep
personal packs in the desired order. The App's resource-pack updater can defer
work when the field is absent; this also does not establish actual launcher
compatibility without the owner's tests.

A local `.mrpack` import does not itself establish an upstream project link for
automatic updates. Use a launcher-supported upgrade path if available for that
instance. Do not treat importing a second instance as an in-place upgrade.
The owner must record the actual upgrade path used. This evaluation does not
publish a Modrinth project or promise either launcher's automatic update UI.

### Deliberately adopt updated defaults

Configured Defaults has no in-game reset GUI. It does not change a mod's native
key reset default. Controls' reset for Light Overlay therefore returns its native
F9, not our initial F7; deliberately bind that action to F7 instead.

- To adopt an individual option or mod setting, use its normal UI or edit that
  one field with the game closed. Existing values are not replaced by updates.
- To enable Continuity, select both built-in packs in Resource Packs and preserve
  personal pack order. No file deletion is necessary.
- To reset an entire maintained mod config, close Minecraft, save a copy, and move
  only that live file aside. Next launch re-seeds it. This resets all settings in
  that file, not just fields changed by the pack. Do not remove the whole config
  directory or root options file.
- To reapply one packaged options key through merging, close the game and save a
  copy of `options.txt`, then remove only that key's line. The next launch adds
  it if the launcher has not already supplied it. App sync may require an explicit
  per-instance exception. Directly choosing the setting in-game is usually easier.

### Migrate existing installations

Use a launcher-supported update path or a disposable copy of the old profile.
Before launching the updated pack, verify that `defaultoptions-...jar` is removed
and `ConfiguredDefaults-...Fabric.jar` is installed. Do not run two defaults
managers. The pack contains only Configured Defaults; a launcher's failure to
remove old mod files cannot be repaired by source validation.

Existing options and mod configs win over templates. Configured Defaults ignores
`defaultoptions.journal.json` and `config/defaultoptions`, so leftover files from
26.2.0.6.0 do not execute after its old mod is removed. They need not be deleted
to migrate. After verifying the transition, the user may remove only that unused
template folder and journal with the game closed. Never delete live preferences
as a normal upgrade step. The repository rejects obsolete manager trees, but
ships no destructive cleanup script for player instances.

For older packs that distributed direct overrides, save options/configs and test
the launcher's removal behavior first. The defaults mod cannot restore previously
overwritten preferences or prevent a launcher removing formerly managed files.

### File-handler evidence and automation limits

Seven isolated fixtures execute the unmodified pinned upstream
`CopyDefaultsHandler` through `ConfiguredDefaultsFilesOracle.java`. Observations,
source/adapter/template hashes and the exact artifact SHA-512 are recorded in
`tests/fixtures/configured-defaults-files.json`. Cases cover fresh files,
launcher-created partial options, customized settings, repeat launch, an update
with new keys/files, a custom resource-pack list, and transition from a previous
manager followed by deliberate per-file re-seeding. The previous manager is not
executed concurrently in that transition fixture.

The audit compiles that source on JDK 17.0.21.1 outside the repository. Only its
logger/constants holder is stubbed. Each run uses a disposable game directory as
both its argument and working directory, matching the handler's path assumption.
No Fabric, Minecraft, resource repository or launcher runs. This verifies file
methods, not actual initialization order, key dispatch, resource rendering or
synchronization. Normal Python tests bind recorded observations to current pins
and templates; they do not download Java or invent a Python implementation.

Validators reject competing manager IDs, obsolete template trees, forced-reset
flags, unsupported template locations, root live preferences and resource-pack
replacement config. Exact pins, native dependency compatibility, client-only
policy, full exports and release gates remain enforced. The
[launcher acceptance matrix](acceptance-tests.md#launcher-configuration-acceptance-matrix)
leaves all runtime results open.

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

Iris 1.11.4 is active with Sodium 0.9.2. The Iris template sets
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
the Client Tweaks template:

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

Light Overlay retains its upstream behavior defaults. The
[release's key registrations](https://github.com/lugosieben/lightoverlay/blob/7e7647bb424ca8195329c889ce529c5974d11c21/src/main/java/net/lugo/lightoverlay/registration/KeyMappings.java)
bind overlay toggling to F9, which conflicts with Renice Shot. The options template seeds `key_key.light-overlay.toggle` as `key.keyboard.f7` only when absent.
F9 remains the high-resolution screenshot key familiar from FO.
Config opening and overlay-mode cycling are unbound.
The config screen is also available from Mod Menu or the client-local
`/lightoverlay config` command. No other Light Overlay setting is overridden.

Static inspection of the pinned artifacts found no competing F7 action in
Xaero's Minimap, Xaero's World Map, Zoomify, BetterF3, Iris, LambDynamicLights,
Renice Shot, or the other active utility mods. libIPN defines F7 in its key-code
catalog but does not assign it to an action by default. User-customized bindings can differ;
verify the new instance's Controls screen during acceptance.

The template paths and upgrade behavior are described above. Existing saved
keybindings retain priority over the pack default.

Light Overlay and OverlayLib declare no conflicts with the selected Iris/Sodium
stack. The overlay uses client-known world/light data and requires no server
component. This establishes static eligibility, not rendering acceptance.
Test toggling and persistence with Sodium, Iris, and LambDynamicLights installed,
starting with shaders disabled. Dynamic lighting does not change server-side
block light or spawn rules.

## Screenshots

[Renice Shot](https://modrinth.com/mod/renice-shot) is FO's screenshot mod for
Minecraft 26.2. Its exact release retains F9, a 3840 by 2160 PNG capture, and the
`huge_` filename prefix in the instance's `screenshots` directory.
The [release config defaults](https://github.com/wechirok/renice-shot/blob/bca7c14881a592ca3df2d309968cb29bdaa32728/src/main/java/me/wechirok/reniceshot/config/Config.java)
leave normal F2 screenshots and other mods' screenshot requests unchanged.
No Renice Shot properties file is shipped. Existing Mod Menu and Cloth Config
provide its optional local configuration screen.

Capture temporarily changes render resolution and restores it afterward. Test
that restoration with Sodium and Iris, initially with shaders disabled. Shader
capture behavior remains part of manual acceptance.

## FO graphics controls and window behavior

[Sodium Extra](https://modrinth.com/mod/sodium-extra) adds graphics controls to
the existing Sodium renderer. [Reese's Sodium Options](https://modrinth.com/mod/reeses-sodium-options)
supplies the alternative settings layout. Their exact native
descriptors require Sodium `0.9.2+mc26.2`, which remains pinned unchanged. Iris
also retains its existing compatible pin. No additional renderer is installed.

Sodium Extra retains its [release defaults](https://github.com/FlashyReese/sodium-extra-fabric/blob/6a1779fc751f27d91ee4387f5cf74e8cd7469bd3/common/src/main/java/me/flashyreese/mods/sodiumextra/client/config/SodiumExtraGameOptions.java).
Its FPS and coordinate overlays are
disabled by default, so they do not add another HUD over BetterF3 and the maps.
The release also leaves shader prevention, alternate projection, and optional
fog overrides disabled. No Sodium Extra or Reese's settings file is shipped.

[Cubes Without Borders](https://modrinth.com/mod/cubes-without-borders) retains
its defaults. It adds borderless/windowed
fullscreen choices and prefers borderless mode when fullscreen is toggled.
Test F11, Alt-Tab, resizing, multiple monitors, Renice Shot resolution restoration,
and Dynamic FPS focus detection together. No custom window settings are shipped.

[More Chat History](https://modrinth.com/mod/morechathistory) raises local
scrollback retention. It changes neither the
server's chat protocol nor server-side history. No custom chat config is needed.

## Default resource packs

The visible default resource-pack behavior selected from FO is Continuity's
connected textures and glass-pane culling fix. Both are already bundled inside
the exact Continuity mod artifact. Its hash-verified release sources register
them as optional built-in packs, so the first-install options template enables them:

```text
resourcePacks:["vanilla","continuity:glass_pane_culling_fix","continuity:default"]
```

This follows FO 14.1.2's ordering for those two packs. Connected glass,
sandstone, bookshelves, and stacked glass panes need visual acceptance with
Sodium, Iris, More Culling, and Light Overlay. Both packs can be disabled locally
from Minecraft's Resource Packs screen. No standalone textures or shaders are
downloaded for this choice.

FO also enables Sodium translation, chat-reporting, and Mod Menu helper packs.
Those helper packs are not included here. Animatica, Polytone, custom entity
models/textures, and custom sky support remain outside this addition.
Config Manager remains staged. Configured Defaults now supplies the selected
copy-if-missing behavior; do not install two default-setting managers together.
