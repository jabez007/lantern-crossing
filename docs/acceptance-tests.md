# Clean-client acceptance tests

Static CI validates metadata and packaging. It does not launch Minecraft, verify
rendering, or prove a vanilla-server join. No runtime test has been completed for
the initial baseline. Complete this checklist before accepting a release.

Use a fresh launcher instance imported from the built `.mrpack`, Minecraft 26.2,
Fabric Loader 0.20.1, and Java 25. Test against a completely unmodified vanilla
26.2 server. Record the pack version, archive SHA-256, date, Java version, launcher,
OS, GPU and driver, and results in `verification.md`. Keep addresses, player data,
and account information out of committed logs.

## Launcher configuration acceptance matrix

**All results below are uncompleted.** This is the intended-baseline matrix
for a future migration after auditing/promoting the helper and later additions.
Those mods are not installed on this bootstrap, whose actual target is 26.2. Expected behavior comes from source
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
- [ ] World renders normally with shaders absent.
- [ ] Held-item and entity dynamic lighting works and updates when the light moves.
- [ ] Weather, dimension changes, and status effects do not leave stale lighting.
- [ ] Entity and block culling produce no obvious corruption or missing geometry.
- [ ] Glass, foliage, signs, item frames, and block entities render from multiple angles.
- [ ] Fullscreen toggling and window resizing work.
- [ ] Iris UI opens without missing dependencies or server warnings.
- [ ] Shaders start disabled and ordinary world rendering has no corruption.
- [ ] Shader-selection UI works and Sodium's options remain functional.
- [ ] Optionally test one known-good shader pack in a separate test profile,
      including dynamic lighting. No shader pack is supplied by the pack.

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

## Client Tweaks

- [ ] Volume sliders, search retention, and recipe-book navigation work as configured.
- [ ] Enabled placement and offhand input conveniences behave normally on the vanilla server.
- [ ] `ui.alwaysPrioritizeExperienceBar=false` leaves the disabled HUD override inactive.
- [ ] `mining.doNotUseLastMending=false` leaves the disabled durability guard inactive.
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

- [ ] Join a Minecraft 26.2 world and activate Light Overlay with F9.
- [ ] The overlay renders useful light and spawnability information.
- [ ] Deactivate it and confirm the overlay disappears cleanly.

### Vanilla server

- [ ] Connect to a completely unmodified vanilla Minecraft 26.2 server.
- [ ] No missing-server-mod or companion-library warning appears.
- [ ] Activate Light Overlay and verify useful light/spawn information is displayed.
- [ ] The server requires no mod or plugin for these features.

### Rendering stack

- [ ] With Sodium, Iris, Light Overlay, OverlayLib, and LambDynamicLights installed,
      the world and overlay render normally.
- [ ] Iris UI works and shaders-disabled rendering has no corruption.
- [ ] Enabling the overlay causes no obvious rendering corruption.
- [ ] Disabling it restores normal rendering without leftover overlay geometry.
- [ ] Optionally test one known-good shader pack separately. Do not add it to the pack.

### Configuration

- [ ] Open Light Overlay's config through Mod Menu or `/lightoverlay config`.
- [ ] F9 works, and the Controls screen shows no new default keybind conflict.
- [ ] Configuration changes persist after restarting the client.

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

Prospective checks only. The new QoL mods and Configured Defaults are not active
in this bootstrap. Run these after the separately authorized target migration
and dependency audit. No 26.3 or launcher compatibility is claimed.

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
      corruption. Optionally test one separately installed known-good shader and
      toggling it while viewing terrain and Xaero maps. No shader is supplied.
- [ ] Food-effect tooltips show vanilla golden-apple effects, rotten-flesh chance,
      milk clearing, honey poison removal, chorus teleport and totem effects.
      They remain readable with Shulker Box Tooltip and ordinary enchantment lines.
- [ ] Suspicious-stew information stays hidden under the retained default.
      No current saturation/exhaustion or plugin-only data is presented as known.
- [ ] Confirm ordinary enchanted items remain readable. Enchantment Descriptions
      is deferred, so descriptive enchantment text is not an expected pack feature.
- [ ] Existing singleplayer worlds load and save normally. Join/rejoin a completely
      unmodified vanilla 26.2 server and exercise the new controls/rendering/tooltips
      without any server mod, plugin, protocol or companion.
- [ ] Launcher-local crash logs remain accessible. Before sharing any log, review
      paths, chat, server addresses and identifiers. Crash Assistant is not installed;
      no new crash UI or automatic upload is expected.

BBE, Ixeris, ModernFix-mVUS and Tooltip Tweaks are inactive. Their candidate
benchmarks and rendering gates in the audit apply only to a separately prepared
future evaluation profile, not to this milestone's acceptance result.
