# Clean-client acceptance tests

Static CI validates metadata and packaging. It does not launch Minecraft, verify
rendering, or prove a vanilla-server join. No runtime test has been completed for
the initial baseline. Complete this checklist before accepting a release.

Use a fresh launcher instance imported from the built `.mrpack`, Minecraft 26.2,
Fabric Loader 0.20.1, and Java 25. Test against a completely unmodified vanilla
26.2 server. Record the pack version, archive SHA-256, date, Java version, launcher,
OS, GPU and driver, and results in `verification.md`. Keep addresses, player data,
and account information out of committed logs.

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

- [ ] Light Overlay is absent as documented. If promoted, test overlay display and toggle.
- [ ] Sign Tweaks edits a normal sign on the vanilla server.
- [ ] Multiline cursor navigation and text wrapping work.
- [ ] Multiline copy and paste work within vanilla sign limits.
- [ ] The vanilla server accepts the edited sign and its text persists after reopening.
- [ ] Vanilla sign placement and editing work with the active rendering stack.
- [ ] Book Tweaks navigation, page wrapping, multi-page paste, and page memory work.
- [ ] Edit, save, reopen, and sign a book without bypassing vanilla limits.

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
