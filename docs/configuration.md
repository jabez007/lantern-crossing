# Configuration decisions

Only `config/MouseTweaks.cfg` is shipped. Every other active mod starts with its
upstream defaults. User-generated preferences, key bindings, server addresses,
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

Iris is excluded because its stable packages bundle a prerelease library.
Shaders remain unavailable in this baseline. A later promotion must check the
exact Sodium requirement, shader-disabled rendering, the shader UI, resizing,
and interactions with dynamic lighting. No shader pack is bundled.

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

## Excluded configuration

Client Tweaks is excluded, so its recipe-book, interaction, and HUD tweaks do
not overlap the dedicated QoL mods. Sign Tweaks and Mod Menu are also excluded.
Use existing mod-specific keys or configuration files for active projects that
normally expose configuration through Mod Menu. Book Tweaks keeps its defaults.

No speculative config file is shipped for an excluded mod. Promotion requires
a new audit and a deliberate configuration review.
