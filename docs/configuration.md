# Configuration decisions

The pack ships `config/MouseTweaks.cfg`, `config/clienttweaks-common.toml`, and
`config/iris.properties`, plus a single keybinding in `options.txt`. Other
settings retain upstream defaults. User-generated preferences, server addresses,
map caches, and waypoints do not belong in the repository or release archive.

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

Light Overlay retains its upstream behavior defaults. The
[release's key registrations](https://github.com/lugosieben/lightoverlay/blob/7e7647bb424ca8195329c889ce529c5974d11c21/src/main/java/net/lugo/lightoverlay/registration/KeyMappings.java)
bind overlay toggling to F9, which conflicts with Renice Shot. The pack's minimal
`options.txt` changes `key_key.light-overlay.toggle` to `key.keyboard.f7`.
F9 remains the high-resolution screenshot key familiar from FO.
Config opening and overlay-mode cycling are unbound.
The config screen is also available from Mod Menu or the client-local
`/lightoverlay config` command. No other Light Overlay setting is overridden.

Static inspection of the pinned artifacts found no competing F7 action in
Xaero's Minimap, Xaero's World Map, Zoomify, BetterF3, Iris, LambDynamicLights,
Renice Shot, or the other active utility mods. libIPN defines F7 in its key-code
catalog but does not assign it to an action by default. User-customized bindings can differ;
verify the new instance's Controls screen during acceptance.

Import into a clean launcher instance. The shipped `options.txt` contains only
that keybinding; it supplies no graphics, audio, accessibility, or personal
settings. Minecraft fills omitted settings with its defaults. Do not copy this
file over an existing instance's `options.txt`; change the binding in Controls
instead. The pack's key file is build input, not a place to save runtime options.

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
