# Clean-client acceptance tests

Static CI validates metadata and packaging. It does not launch Minecraft, verify
rendering, or prove a vanilla-server join. No runtime test has been completed for
the initial baseline. Complete this checklist before accepting a release.

Use a fresh launcher instance imported from the built `.mrpack`, Minecraft 26.2,
Fabric Loader 0.20.1, and Java 25. Test against a completely unmodified vanilla
26.2 server. Record the pack version, archive SHA-256, date, Java version, launcher,
OS, GPU and driver, and results in `verification.md`. Keep addresses, player data,
and account information out of committed logs.

## Defaults and upgrade acceptance, owner only

- [ ] Import a fresh pack in Prism without copying an old profile. Check whether
      the launcher creates `options.txt` before the first launch.
- [ ] With no prior options file, verify Continuity's two built-in packs are selected
      and Light Overlay uses F7. Confirm Renice Shot retains F9.
- [ ] Verify Mouse Tweaks, Client Tweaks and Iris receive their documented initial
      defaults early enough to affect the first launch. Shaders initially stay disabled.
- [ ] In a disposable existing profile, set distinctive graphics/audio preferences,
      another overlay key, resource-pack choices and Iris settings. Install/update
      the pack and confirm all existing settings remain intact after two restarts.
- [ ] Repeat the existing-profile check without a Default Options journal; saved
      options and mod configs must still be preserved.
- [ ] For existing profiles retaining F9 for Light Overlay, move it to F7 manually
      to resolve the screenshot collision. Do not reset unrelated settings.
- [ ] Confirm no server address list or runtime journal was supplied by the archive.

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
- [ ] Connect to the unmodified vanilla 26.2 server and use all five new features
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

- [ ] Join a Minecraft 26.2 world and activate Light Overlay with F7.
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
- [ ] F7 toggles the overlay, and F9 captures a screenshot without toggling it.
- [ ] Controls shows no conflict between the two bindings.
- [ ] Configuration changes persist after restarting the client.

## Screenshots

- [ ] Renice Shot's local config opens through Mod Menu.
- [ ] On a completely vanilla 26.2 server, press F9 and save a 3840 by 2160 PNG
      under `screenshots` with the `huge_` prefix. No server installation is needed.
- [ ] F2 still takes a normal screenshot at the current window resolution.
- [ ] Resolution, fullscreen/windowed state, and HUD state restore after capture.
- [ ] Repeated captures work with Sodium and Iris installed and shaders disabled.
- [ ] The F7 overlay binding persists after restarting the client.
- [ ] Optionally test capture with a separately installed known-good shader pack.

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
