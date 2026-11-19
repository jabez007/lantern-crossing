# Clean-client acceptance tests

Static CI validates metadata and packaging. It does not launch Minecraft, verify
rendering, or prove a vanilla-server join. No runtime test has been completed for
the initial baseline. Complete this checklist before accepting a release.

Use a fresh launcher instance imported from the built `.mrpack`, Minecraft 26.3,
Fabric Loader 0.20.1, and Java 25. Test against a completely unmodified vanilla
26.3 server. Record the pack version, archive SHA-256, date, Java version, launcher,
OS, GPU and driver, and results in `verification.md`. Keep addresses, player data,
and account information out of committed logs.

## Launcher configuration acceptance matrix

**All results below are uncompleted.** Expected behavior comes from source
inspection and isolated file-method fixtures, not launcher or Minecraft tests.
Run each column with disposable profiles. Record the launcher version, sync
controls actually available, pre-launch options contents, archive hash, upgrade
method and observed results. If the installed App has no sync control, mark that
column unavailable and record the version, rather than treating it as passed.

| Scenario | Prism | Modrinth App, sync disabled | Modrinth App, sync enabled | Expected result |
| --- | --- | --- | --- | --- |
| Fresh `.mrpack` import; inspect before launching | [ ] | [ ] | [ ] | Record whether root options, mod configs or a journal already exist, and which settings the launcher populated. No player options/journal should come from the archive. |
| First launch, no pre-existing options | [ ] | [ ] | [ ] | Continuity's two built-in packs are selected. Unseen Light Overlay binding becomes F7; Renice Shot remains F9. Mouse Tweaks, Client Tweaks and Iris receive their documented initial settings; shaders start disabled. |
| Launcher-created options containing only fullscreen/version | [ ] | [ ] | [ ] | Existing options remain authoritative. Absent resource-pack and F7 entries are merged while fullscreen survives. Existing resource-pack or key entries are preserved. |
| Existing graphics, sound, accessibility and interface preferences | [ ] | [ ] | [ ] | Distinctive values survive first launch and two restarts. App-synced values may take precedence; record that separately from mod behavior. |
| Existing overlay binding set to F8 or F9 | [ ] | [ ] | [ ] | Existing binding survives, even if it conflicts with screenshots. No repeated forced F7 reset. |
| Customized resource-pack selection and order, with/without a journal | [ ] | [ ] | [ ] | Defaults manager does not replace or reorder it. Record effects of App resource-pack sync separately. |
| Customized Mouse Tweaks, Client Tweaks and Iris files | [ ] | [ ] | [ ] | Existing files and unrelated settings survive; overlap switches are not silently reasserted. Review those switches manually if retaining old configs. |
| Repeat launch after changing defaults in-game | [ ] | [ ] | [ ] | Choices persist; no resource-pack or settings reset on every launch. |
| Upgrade through the actual supported launcher path | [ ] | [ ] | [ ] | Template updates do not reset live options/configs. Newly absent config files and missing option keys can receive defaults. Missing non-key options are merged; existing values and fields inside existing mod configs are not replaced or merged. |
| Intentional per-action default adoption | [ ] | [ ] | [ ] | Deliberately bind only Light Overlay to F7. Its native reset remains F9, so do not assume the reset button selects F7. If App sync reasserts a global value, test a deliberate per-instance exception. |
| Intentional Continuity activation | [ ] | [ ] | [ ] | Select both built-in packs manually and preserve personal pack order. Selection survives restart under the chosen sync policy. |
| Intentional adoption of one mod config | [ ] | [ ] | [ ] | With game closed, retain a copy and move only that live file aside. Next launch re-seeds it; every other custom file remains intact. This resets the entire selected file. |
| Existing 26.2.0.6.0 Default Options migration | [ ] | [ ] | [ ] | Old Default Options JAR is removed before launch; only Configured Defaults is active. Existing live preferences remain. Its old journal/templates may remain unused. |
| Upgrade from older direct-override pack | [ ] | [ ] | [ ] | Test a disposable copy with saved options/configs. Record whether the launcher removes previously managed overrides. The defaults manager cannot prevent launcher deletion. |

For the upgrade row, use a real supported pack update or a clearly labeled
private test export. A second fresh import is not an upgrade test. A local
`.mrpack` may not expose the same automatic update UI as a published linked
Modrinth pack; record any unavailable upgrade path as a limitation.

For App sync enabled, separately check game-option sync and resource-pack sync
where the installed version permits. Test a global custom overlay binding, a
per-instance override, and whether changes propagate to another disposable
instance. Do not use personal profiles as sync test fixtures.

Configured Defaults has no reset GUI and ignores the old Default Options journal.
Do not remove live preferences as a normal upgrade step. See [adoption instructions](configuration.md#deliberately-adopt-updated-defaults).

## Startup

- [ ] Fabric client starts and reaches the main menu without errors.
- [ ] No missing dependency warnings appear.
- [ ] No incompatible mod warnings appear.
- [ ] Logs contain no failed client entrypoints or unexpected server requirements.

## Vanilla-server compatibility

- [ ] Confirm the test server has no mods, plugins, proxy extensions, or companions.
- [ ] Join successfully without installing anything on the server.
- [ ] Disconnect and reconnect normally.
- [ ] No selected mod reports a missing server component.
- [ ] Local maps, shulker previews, and vanilla statistics work without extra data.

## Rendering and performance

- [ ] Sodium's video options load.
- [ ] World renders normally with shaders disabled.
- [ ] Held-item and entity dynamic lighting works and updates when the light moves.
- [ ] Weather, dimension changes, and status effects do not leave stale lighting.
- [ ] Entity and block culling produce no obvious corruption or missing geometry.
- [ ] Glass, foliage, signs, item frames, and block entities render from multiple angles.
- [ ] Fullscreen toggling and window resizing work.
- [ ] Iris UI opens without missing dependencies or server warnings.
- [ ] Shaders start disabled and ordinary world rendering has no corruption.
- [ ] Shader-selection UI works and Sodium's options remain functional.
Use the [shader owner acceptance matrix](#shader-owner-acceptance-matrix) below
for both bundled shader choices, lighting interactions and preference retention.

## Inventory

- [ ] IPN sorting works in the player inventory and vanilla containers.
- [ ] IPN scroll transfer and shift-drag act once per gesture.
- [ ] Mouse Tweaks right-drag and carried-stack left-drag work.
- [ ] Mouse Tweaks' disabled wheel and empty-cursor drag do not double-handle IPN.
- [ ] Shulker Box Tooltip displays vanilla item-contained contents.
- [ ] No inventory desync, accidental dropping, or slot interaction conflict occurs.
- [ ] Ender-chest remote preview is outside scope and does not prompt for a companion.

## HUD and interfaces

- [ ] Status Effect Bars reflect remaining vanilla effect durations.
- [ ] BetterF3 opens and displays current debug information.
- [ ] Better Mount HUD displays player and mount state correctly.
- [ ] Paginated Advancements navigates the server's ordinary advancement tabs.
- [ ] Better Statistics Screen searches and sorts the player's vanilla statistics.
- [ ] Mod Menu opens, lists installed configurable mods, and opens their config screens.
- [ ] Mod Menu reports no missing dependency warnings.
- [ ] Reese's Sodium Options opens, navigates, searches, and changes Sodium settings.
- [ ] Sodium Extra's graphics pages load; optional FPS/coordinate overlays stay off.
- [ ] More Chat History retains over 100 local messages without affecting vanilla chat.

## Default visuals and fullscreen

- [ ] Continuity's connected-texture and glass-pane packs are enabled after a fresh import.
- [ ] Connected glass, sandstone, bookshelves, and vertically stacked panes render correctly.
- [ ] Toggle each built-in pack in Resource Packs and reload without rendering corruption.
- [ ] With Sodium, Iris, More Culling, and Light Overlay active, repeat those visual checks
      with shaders disabled. No extra resource or shader pack is needed.
- [ ] Cubes Without Borders exposes its fullscreen choices through the settings UI.
- [ ] F11, Alt-Tab, window resizing, and multiple monitors work as expected.
- [ ] Dynamic FPS responds correctly to focus/minimize changes in borderless mode.
- [ ] Renice Shot restores the selected fullscreen mode and resolution after F9 capture.
- [ ] Connect to the unmodified vanilla 26.3 server and use these graphics and screenshot features
      without missing-server-component warnings.

## Client Tweaks

- [ ] Volume sliders, search retention, and recipe-book navigation work as configured.
- [ ] Enabled placement and offhand input conveniences behave normally on the vanilla server.
- [ ] On a fresh profile, `ui.alwaysPrioritizeExperienceBar=false` leaves the disabled HUD override inactive.
- [ ] On a fresh profile, `mining.doNotUseLastMending=false` leaves the disabled durability guard inactive.
- [ ] No inventory conflict occurs with IPN sorting, refill, or Mouse Tweaks gestures.
- [ ] No Client Tweaks or Balm warning requests server installation or server data.

## Navigation

- [ ] Xaero's Minimap renders local terrain.
- [ ] Xaero's World Map opens and records explored terrain.
- [ ] Local waypoints persist through disconnect, reconnect, and client restart.
- [ ] Verify Manual map selection and dimension separation without server identification.
- [ ] Zoomify zoom and reset behave normally.
- [ ] No server teleport permission or server identification extension is required.

## Building and writing

- [ ] Sign Tweaks edits a normal sign on the vanilla server.
- [ ] Multiline cursor navigation and text wrapping work.
- [ ] Multiline copy and paste work within vanilla sign limits.
- [ ] The vanilla server accepts the edited sign and its text persists after reopening.
- [ ] Vanilla sign placement and editing work with the active rendering stack.
- [ ] Book Tweaks navigation, page wrapping, multi-page paste, and page memory work.
- [ ] Edit, save, reopen, and sign a book without bypassing vanilla limits.

## Light Overlay

### Basic overlay

- [ ] Join a Minecraft 26.3 world and activate Light Overlay with F7.
- [ ] The overlay renders useful light and spawnability information.
- [ ] Deactivate it and confirm the overlay disappears cleanly.

### Vanilla server

- [ ] Connect to a completely unmodified vanilla Minecraft 26.3 server.
- [ ] No missing-server-mod or companion-library warning appears.
- [ ] Activate Light Overlay and verify useful light/spawn information is displayed.
- [ ] The server requires no mod or plugin for these features.

### Rendering stack

- [ ] With Sodium, Iris, Light Overlay, OverlayLib, and LambDynamicLights installed,
      the world and overlay render normally.
- [ ] Iris UI works and shaders-disabled rendering has no corruption.
- [ ] Enabling the overlay causes no obvious rendering corruption.
- [ ] Disabling it restores normal rendering without leftover overlay geometry.
- [ ] Repeat overlay toggling with both bundled shaders using the shader matrix below.

### Configuration

- [ ] Open Light Overlay's config through Mod Menu or `/lightoverlay config`.
- [ ] F7 toggles the overlay, and F9 captures a screenshot without toggling it.
- [ ] Controls shows no conflict between the two bindings.
- [ ] Configuration changes persist after restarting the client.

## Screenshots

- [ ] Renice Shot's local config opens through Mod Menu.
- [ ] On a completely vanilla 26.3 server, press F9 and save a 3840 by 2160 PNG
      under `screenshots` with the `huge_` prefix. No server installation is needed.
- [ ] F2 still takes a normal screenshot at the current window resolution.
- [ ] Resolution, fullscreen/windowed state, and HUD state restore after capture.
- [ ] Repeated captures work with Sodium and Iris installed and shaders disabled.
- [ ] The F7 overlay binding persists after restarting the client.
- [ ] Repeat capture with both bundled shaders using the shader matrix below.

## Screenshot owner acceptance matrix

All results below are uncompleted. Run on the maintained 26.3 artifact in both
launchers, with Modrinth App settings synchronization tested separately where
available. The expected architecture is Renice Shot alone. Neither evaluated
gallery is installed. Source inspection and archive validation are not observed
launcher or rendering results. Use copies of screenshots for destructive tests.

| Owner check | Prism | Modrinth App, sync off | Modrinth App, sync on | Expected result, not observed |
| --- | --- | --- | --- | --- |
| Fresh `.mrpack` import and first launch | [ ] | [ ] | [ ] | Renice Shot initializes; no gallery, new sharing prompt or missing-server-mod warning. Configured Defaults keeps its documented behavior. |
| Controls and configuration | [ ] | [ ] | [ ] | F2 remains normal capture, F9 is high resolution, an absent Light Overlay binding receives F7. Controlling finds no unexpected conflict; existing customized bindings survive. Mod Menu opens Renice Shot configuration. |
| F2 and repeated F9 captures | [ ] | [ ] | [ ] | Normal image has window dimensions; default F9 PNG has 3840x2160 pixels and a `huge_` time-based filename in this instance's screenshots folder. Existing names are not overwritten. |
| HUD, window and resolution restoration | [ ] | [ ] | [ ] | Test fullscreen/windowed capture and repeated captures. If opting into HUD hiding, it restores afterward. No persistent resize or hidden-HUD regression. |
| Existing screenshots and large collection | [ ] | [ ] | [ ] | Before installation, keep a backup and hash a representative selection. Old names, bytes, subfolders and custom formats survive launches/upgrades. Hundreds/thousands of controlled-copy images remain accessible through the launcher/OS folder. No in-game library is expected or benchmark claim made. |
| High-resolution/custom format files | [ ] | [ ] | [ ] | Open default 4K PNGs externally. Optionally test a safe larger size, JPG/TGA/BMP and HUD-hidden capture through Renice Shot. Check restoration and readability; respect hardware limits. |
| Gallery, sorting, favorites and deletion | [ ] | [ ] | [ ] | No gallery UI/key, favorites database, automatic sorting or in-game deletion is installed. Browse/copy/share deliberately with launcher/OS tools. Check any external deletion only on a disposable copy, then restore it. |
| Privacy before sharing | [ ] | [ ] | [ ] | Inspect a new original PNG's text metadata and default filename for unexpected coordinates, world/server identifiers or uploads. Review visible chat, maps and coordinates in the pixels. `%world%` naming, if personally enabled, exposes that name intentionally. |
| Xaero and panoramas | [ ] | [ ] | [ ] | Normal maps still work. No screenshot pins/map association, panorama capture or second F9 action is expected. |
| Sodium and Iris | [ ] | [ ] | [ ] | F2/F9 and restoration work with shaders disabled, without corrupted images or rendering. Repeat with both bundled shaders using the shader matrix below. |
| Vanilla server and existing world | [ ] | [ ] | [ ] | Capture after singleplayer load and on a completely unmodified vanilla 26.3 server; disconnect/rejoin normally. No server mod/plugin/protocol is needed. |
| Upgrade and repeat launch | [ ] | [ ] | [ ] | Upgrade an existing Lantern Crossing instance. Old screenshots, custom capture settings, keybindings and other preferences remain intact. New captures work and originals' hashes remain unchanged. Importing into a separate instance does not automatically move old screenshots. |

Future gallery promotion requires a separate disposable-profile evaluation of
old `huge_` images, custom/symlinked paths, arbitrary dimensions, bounded memory
with a large library, confirmation and cancellation of deletion, sorting and
favorites if offered, metadata privacy and exact Xaero world/dimension matching.
Neither candidate is installed merely to run that evaluation. These are open
promotion criteria, not claimed current features or completed acceptance.

## Social and resource behavior

- [ ] Chat Heads displays the correct head for ordinary vanilla player messages.
- [ ] Dynamic FPS reduces rendering while unfocused and minimized, then resumes.
- [ ] Memory, CPU, and GPU behavior show no obvious regression during a repeatable route.
- [ ] FastQuit returns to the menu while a singleplayer save finishes, and the
      completed save reopens correctly. Do not kill the process during saving.
- [ ] Language Reload switches and reloads local translations.

If a selected feature needs server installation or meaningful server-assisted
behavior to pass its test, exclude it and record the blocker. Do not fix a client
acceptance failure by modifying the vanilla test server.

## QoL refinement acceptance

All results are uncompleted. Run these on Prism and Modrinth App, with App sync
disabled and enabled where supported. Record each launcher version, pre-launch
file state, archive hash and actual upgrade method in the matrix above.

- [ ] Fresh import initializes BetterGrassify, Controlling, Searchables and Food
      Effect Tooltips without missing dependencies or server warnings.
- [ ] Controls search finds Light Overlay, Zoomify, Iris and Xaero bindings.
      Conflict-only and free-key views work. F7 overlay and F9 capture stay separate.
- [ ] A previously customized overlay binding and graphics/resource-pack order
      survive repeat launches and a real upgrade. Controlling does not rebind them.
- [ ] BetterGrassify's absent live config receives the documented fancy grass
      settings. Paths, farmland, Nether extensions and extra snow layers stay off.
- [ ] A pre-existing customized BetterGrassify config survives upgrade/restart.
      Disabling the effect in its UI persists without resetting other mod configs.
- [ ] Grass, slopes, podzol, mycelium, snowy grass and glass panes render correctly
      with Sodium, Continuity, More Culling, Entity Culling and dynamic lights.
      Resource reload, dimension changes and world reload leave no missing faces.
- [ ] Iris UI and Sodium settings work. With shaders disabled there is no visual
      corruption. Test both bundled shaders and switching them while viewing terrain
      and Xaero maps using the shader matrix below.
- [ ] Food-effect tooltips show vanilla golden-apple effects, rotten-flesh chance,
      milk clearing, honey poison removal, chorus teleport and totem effects.
      They remain readable with Shulker Box Tooltip and ordinary enchantment lines.
- [ ] Suspicious-stew information stays hidden under the retained default.
      No current saturation/exhaustion or plugin-only data is presented as known.
- [ ] Confirm ordinary enchanted items remain readable with Enchantment Descriptions
      collapsed; hold Shift to expand the locally supplied descriptions.
- [ ] Existing singleplayer worlds load and save normally. Join/rejoin a completely
      unmodified vanilla 26.3 server and exercise the new controls/rendering/tooltips
      without any server mod, plugin, protocol or companion.
- [ ] Launcher-local crash logs remain accessible. Before sharing any log, review
      paths, chat, server addresses and identifiers. Crash Assistant is not installed;
      no new crash UI or automatic upload is expected.

BBE, Ixeris, ModernFix-mVUS and Tooltip Tweaks are inactive. Their candidate
benchmarks and rendering gates in the audit apply only to a separately prepared
future evaluation profile, not to this milestone's acceptance result.

## Enchantment Descriptions acceptance

All results are uncompleted. Run each case in Prism Launcher and Modrinth App,
with App sync disabled and enabled where the installed version supports it.
Use disposable instances and record the pack version/hash, launcher, Java and
observed results. Static source inspection does not complete any row.

| Case | Prism | Modrinth App | Expected result |
| --- | --- | --- | --- |
| Fresh `.mrpack` import and launch | [ ] | [ ] | Enchantment Descriptions and Prickle initialize without missing dependencies or a server companion warning. |
| Enchanted book and vanilla enchanted tool/armor | [ ] | [ ] | A local prompt appears while collapsed; Shift reveals the relevant descriptions beside ordinary enchantment names/levels. Check common and stored enchantments. |
| Several enchantments and another supported language | [ ] | [ ] | Descriptions remain readable; scrolling/wrapping and translated text cause no tooltip errors. |
| Food/container/vanilla tooltips | [ ] | [ ] | Food Effect Tooltips and Shulker Box Tooltip keep their own information without duplicate enchantment explanations or missing ordinary lines. |
| Customized valid `enchdesc.json` | [ ] | [ ] | An existing `require_keybind.value = false` remains false through launch/restart/upgrade. Prickle may normalize formatting and add default metadata. Other mod configs, keybindings and resource-pack choices remain unchanged. |
| Real pack upgrade from 26.2.0.8.0 | [ ] | [ ] | The new template seeds only an absent file. Existing graphics, sound, accessibility, controls and mod preferences survive under the recorded App sync choices. |
| Deliberate adoption/reset of this file only | [ ] | [ ] | With the game closed and a backup retained, move only the live file aside. Next launch seeds Shift mode without resetting other settings. |
| Completely unmodified vanilla 26.3 server | [ ] | [ ] | Join/rejoin normally; ordinary enchanted item/book descriptions work with nothing installed server-side and no custom packet/companion warning. |
| Update host unavailable, optional disposable network test | [ ] | [ ] | Prickle may log its version-check warning; initialization/configuration/tooltips still work after the bounded asynchronous check. This is distinct from Minecraft server connectivity. |

No accurate custom server/plugin enchantment semantics are promised. Do not
install anything on the vanilla server to resolve a client acceptance failure.
Legacy config recovery and actual launcher upgrade/sync behavior require owner
observation, not a Python approximation.

## Shader owner acceptance matrix

Every result is uncompleted. Run against the final 26.3 archive in Prism Launcher
and Modrinth App, with sync enabled/disabled where supported. Record pack/hash,
launcher, Java, OS, GPU/driver, resolution, render distance, shader/version/profile
and actual observations. Test each shader separately and retain a no-shader
comparison. Do not infer GPU performance or visual compatibility from static CI.
Use disposable copies of existing instances for upgrade tests.

| Owner scenario | Prism | Modrinth App, sync off | Modrinth App, sync on | Expected result, not observed |
| --- | --- | --- | --- | --- |
| Fresh `.mrpack` import | [ ] | [ ] | [ ] | Exactly the two official shader ZIPs install under shaderpacks/. No supporting mods or copied ZIP override appears; no installation/dependency error. |
| First launch and Iris UI | [ ] | [ ] | [ ] | Without an existing/synced Iris config, shaders start disabled. Otherwise record and preserve the existing choice. The pack does not select a shader. Both named choices appear in Iris. Existing no-shader rendering and controls work; no new startup prompt/keybind is introduced by pack configuration. |
| Complementary Reimagined | [ ] | [ ] | [ ] | Select r5.10, choose a sensible Low/Medium profile for the hardware, apply, and inspect rendering. Record compile/log errors; increase quality only deliberately. |
| MakeUp alternative | [ ] | [ ] | [ ] | Select 9.6 and an appropriate low/shadowless profile; verify optional shadows, reflections, bloom and clouds respond to settings. Do not assume it is faster by name. |
| Terrain and transitions | [ ] | [ ] | [ ] | Grass/dirt paths, slopes, water edges and changing biomes render correctly. BetterGrassify's configured grass works; its snow mode remains OFF. Test snow visuals separately if enabled personally. |
| Continuity and culling | [ ] | [ ] | [ ] | Connected glass, bookshelves, sandstone, leaves, signs, chests, beds, item frames and entities/shadows stay correct from multiple angles. No missing faces or unexpected translucent surfaces. |
| Dynamic and shader lighting | [ ] | [ ] | [ ] | Held/dropped lights and other players render without doubled brightness. Compare LambDynamicLights behavior with shaders off and each shader on. Any local lighting adjustment preserves the useful no-shader behavior. |
| Weather, water and visibility | [ ] | [ ] | [ ] | Inspect clouds, rain, shadows, nighttime, caves, underwater and water transitions. Visibility remains usable; visual light is not mistaken for server spawn/light rules. |
| Dimensions and travel | [ ] | [ ] | [ ] | Overworld, Nether and End terrain, fog, portals and loading transitions remain correct. Existing worlds open normally. |
| Maps and overlays | [ ] | [ ] | [ ] | Xaero minimap/world map, waypoints and Light Overlay remain readable with each shader. Check overlay toggling, maps and water/sky interactions without promising screenshot-map integration. |
| Shader switching/reloading | [ ] | [ ] | [ ] | Switch off, to each shader and back repeatedly. Resource reloads, resizing, focus changes and fullscreen restore normally, with no persistent corruption or runaway memory growth. |
| Performance measurements | [ ] | [ ] | [ ] | Record a repeatable no-shader route, FPS/frame-time behavior and VRAM where available; repeat with both chosen profiles and high render distances. Choose acceptable settings from observed results, not upstream names or universal FPS claims. |
| Restart and preferences | [ ] | [ ] | [ ] | Active shader, custom preset and disabled state each persist across restarts when deliberately selected. Existing player settings/resource-pack ordering remain authoritative. |
| Upgrade from existing 26.2 pack | [ ] | [ ] | [ ] | Existing Iris config and per-shader .zip.txt preferences survive; active/disabled choice does not change unexpectedly. Both bundled choices remain available. Record launcher-specific behavior and any old ZIP filename migration. |
| Screenshots | [ ] | [ ] | [ ] | Renice Shot F9 and normal F2 captures are correct with each shader; resolution/HUD restore. Pre-existing screenshot names/bytes and worlds remain unchanged. Neither gallery is expected. |
| Unmodified vanilla server | [ ] | [ ] | [ ] | Join/rejoin a completely vanilla 26.3 server, switch visual choices locally, and use ordinary inventory/rendering features without server mods/plugins or missing-component warnings. |

Resolve runtime findings through scoped fixes during the feature freeze. Repeat
affected acceptance after any pack/index change. Record actual owner acceptance
and the final pack hash through the existing release policy before publishing.
No unchecked box is a pass, and 26.3 acceptance does not qualify the 26.2 maintenance pack.

## 26.3 migration acceptance

**Every result is uncompleted.** Use the existing matrices above in Prism and
Modrinth App, with App option/resource-pack synchronization disabled and enabled
where available. Record expected behavior separately from observed results.
Static success is not a completed Minecraft test.

| Migration scenario | Prism | App sync off | App sync on | Owner checks |
| --- | --- | --- | --- | --- |
| Fresh import | [ ] | [ ] | [ ] | Minecraft 26.3, Loader 0.20.1, Java 25; all 41 features and eleven libraries initialize; no missing/incompatible warning. Two shaders appear, neither selected automatically. |
| Real 26.2-to-26.3 upgrade of a disposable instance copy | [ ] | [ ] | [ ] | Record launcher upgrade path and old/new archive hashes. Original instance remains intact. Obsolete 26.2 JARs are removed, no duplicate mods. Retain preferences, screenshots, map data, worlds and shader sidecars where supported. A fresh import is not an upgrade test. |
| SDL3 controls and physical keys | [ ] | [ ] | [ ] | Review every binding after conversion. F7 overlay and F9 capture stay separate; F2/F3/F11, Zoomify, map keys, Controlling search/conflicts, IPN and extra mouse buttons work. Test non-US layouts, sign/book search and text input, wheel/drag actions and modifier keys. No numeric GLFW seed or raw-input option is expected. |
| Inventory and tooltips | [ ] | [ ] | [ ] | IPN/Mouse Tweaks actions run once without desync; Client Tweaks overlap switches stay off on fresh profiles; enchantment descriptions remain Shift-gated and food effects are readable without duplicates or invented server state. |
| SDL3 windows and Linux | [ ] | [ ] | [ ] | Cubes Without Borders fullscreen/windowed modes, resize, Alt-Tab, monitor/DPI changes and Dynamic FPS focus/minimize work. On Linux record Wayland versus XWayland/backend and test native Wayland where supported. Do not infer platform results from Windows. |
| Transparency and shader compilation | [ ] | [ ] | [ ] | Establish the no-shader baseline, then both shader choices. Check glass, water, particles, clouds, entities, block entities, grass/snow, Continuity textures, dynamic lights, dimensions, maps and overlays. Switch/reload repeatedly, inspect logs and frame times. Complete the shader matrix above. |
| Screenshot and local data preservation | [ ] | [ ] | [ ] | F2/F9 captures with and without each shader, correct HUD/resolution restoration. Existing screenshot bytes, worlds and map folders survive upgrade; maps retain correct server/dimension association or are deliberately reassigned manually. |
| Completely vanilla 26.3 server | [ ] | [ ] | [ ] | Join/rejoin with no companion mods/plugins. Inventory, navigation, vanilla enchantment/food tooltips, writing, chat, lighting and both shaders work without server-component warnings. Do not expect plugin-enchantment descriptions, ender-chest remote data or server teleport privileges. |
| Repeat launch and preferences | [ ] | [ ] | [ ] | Customized graphics, sound, accessibility, binds, resource packs and shader presets persist; deliberate shader-disable persists; no repeated default reset. Record launcher sync effects separately. |

Resolve defects before owner qualification. Set runtime acceptance only for the
actually tested 26.3 artifact and pack hash, never by copying the 26.2 record.
