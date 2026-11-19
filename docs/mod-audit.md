# Client-only mod audit

Evidence checked on 2026-11-17 against the [Modrinth API](https://docs.modrinth.com/api/) and the exact downloaded Fabric artifacts. [The offline snapshot](upstream-metadata.json) records project/version identity, compatibility declarations, files, dependency edges, and recursive Fabric descriptors. Download hashes were checked during the audit and again by packwiz export.

Renice Shot was added and audited on 2026-11-18. The prior 39 artifact pins are
unchanged. That addition completed the 30 original features plus Renice Shot.

Five FO-inspired additions were audited later on 2026-11-18. Default Options was added on 2026-11-19 to protect player preferences. All 40 prior pins
remain unchanged; the active baseline now has 37 intentional features.

The question for every row is whether the selected functionality works entirely on the client while connected to an unmodified vanilla 26.2 server. An optional server label alone is insufficient evidence. No runtime multiplayer acceptance has been performed.

## Requested features

| Project and upstream evidence | Fabric 26.2 evidence | Selected functionality | Server participation assessment | Decision |
| --- | --- | --- | --- | --- |
| [Sodium](https://modrinth.com/mod/sodium) | [mc26.2-0.9.2-fabric](https://modrinth.com/mod/sodium/version/xJZxADzI), release-designated | Client chunk rendering and render options. | No server build needed; all selected rendering is local. | Active |
| [Lithium](https://modrinth.com/mod/lithium) | [mc26.2-0.25.3-fabric](https://modrinth.com/mod/lithium/version/f7vZ0VWU), release-designated | Local simulation optimizations, including the integrated singleplayer server. | Independent installations are documented. No remote-server TPS benefit is claimed. | Active |
| [FerriteCore](https://modrinth.com/mod/ferrite-core) | [9.0.0-fabric](https://modrinth.com/mod/ferrite-core/version/d5ddUdiB), release-designated | Client memory optimizations. | Server optimizations are independent. Client memory savings do not depend on server installation. | Active |
| [ImmediatelyFast](https://modrinth.com/mod/immediatelyfast) | [1.16.5+26.2-fabric](https://modrinth.com/mod/immediatelyfast/version/pMWERcSu), release-designated | Immediate-mode client rendering. | No server component. All selected batching is local. | Active |
| [Entity Culling](https://modrinth.com/mod/entityculling) | [1.12.1](https://modrinth.com/mod/entityculling/version/kHxKicVG), release-designated | Local visibility and client tick culling. | Upstream explicitly says no server installation and no effect on server simulation. | Active |
| [More Culling](https://modrinth.com/mod/moreculling) | [1.8.2](https://modrinth.com/mod/moreculling/version/Qc7V2eKG), release-designated | Local block-face and model culling. | No server component. No world logic changes selected. | Active |
| [BadOptimizations](https://modrinth.com/mod/badoptimizations) | [2.4.1](https://modrinth.com/mod/badoptimizations/version/JmPs4Wie), release-designated | Local lightmap and rendering work reduction. | No server component. Standard vanilla world packets supply inputs. | Active |
| [Dynamic FPS](https://modrinth.com/mod/dynamic-fps) | [3.11.9](https://modrinth.com/mod/dynamic-fps/version/pC2JjFw1), release-designated | Unfocused and minimized client resource control. | No server component. Local client render loop only. | Active |
| [FastQuit](https://modrinth.com/mod/fastquit) | [3.1.5+mc26.2](https://modrinth.com/mod/fastquit/version/ZZ5dfboC), release-designated | Return to menu while a local singleplayer save finishes. | No remote-server component. Do not exit the process before saving finishes. | Active |
| [Debugify](https://modrinth.com/mod/debugify) | [26.2.0.1](https://modrinth.com/mod/debugify/version/p9lCmVmH), release-designated | Client bug fixes and fixes within the integrated singleplayer server. | Remote server fixes are independent. The selected local fixes need no remote cooperation. | Active |
| [Language Reload](https://modrinth.com/mod/language-reload) | [1.7.8+26.2](https://modrinth.com/mod/language-reload/version/doGx6rSt), release-designated | Language selection, multilingual search, and local reload. | No server component. Uses local translations. | Active |
| [Inventory Profiles Next](https://modrinth.com/mod/inventory-profiles-next) | [fabric-26.2-2.3.8](https://modrinth.com/mod/inventory-profiles-next/version/oQFRysLk), release-designated | Inventory sorting and local interaction assistance. | Upstream explicitly calls it pure client-side and usable everywhere. Uses vanilla inventory actions. | Active |
| [Mouse Tweaks](https://modrinth.com/mod/mouse-tweaks) | [26.2-2.31-fabric](https://modrinth.com/mod/mouse-tweaks/version/jOiTBIaB), release-designated | Right-button drag and left-button drag with a carried stack. | Upstream explicitly says there is no server component. Wheel and empty-cursor shift-drag are disabled here. | Active |
| [Shulker Box Tooltip](https://modrinth.com/mod/shulkerboxtooltip) | [5.4.3+26.2-fabric](https://modrinth.com/mod/shulkerboxtooltip/version/woHKruB1), release-designated | Shulker-item previews from contents already sent in vanilla item components. | No server assistance for this scope. Optional ender-chest preview requires server support and is excluded from pack intent. | Active |
| [Client Tweaks](https://modrinth.com/mod/client-tweaks) | [26.2.0.6+fabric-26.2](https://modrinth.com/mod/client-tweaks/version/klm9mkyw), release-designated | Local UI, rendering, targeting, and vanilla input conveniences. Two overlapping guards are pinned off. | Client initializer and enabled tweak implementations are local. No extra server data or installation. Requires Balm; the bundled shogi_api SNAPSHOT is hash-pinned inside this upstream release. | Active |
| [Status Effect Bars](https://modrinth.com/mod/status-effect-bars) | [1.0.12](https://modrinth.com/mod/status-effect-bars/version/aAXJqboy), release-designated | Render remaining durations from vanilla status-effect data. | No server component. No extra server-only information selected. | Active |
| [Light Overlay](https://modrinth.com/mod/lightoverlay), ID `8qVa1XCN` | [2.12.0+26.2](https://modrinth.com/mod/lightoverlay/version/AT01Q5uN), Fabric 26.2 release | Client-side light/spawnability overlay, local toggle, and local configuration. | Upstream is client-only. Release source uses client world data and client command callbacks. Requires OverlayLib 0.12.0+26.2, Fabric API, and YACL; no server counterpart. | Accepted, active |
| [BetterF3](https://modrinth.com/mod/betterf3) | [19.0.1](https://modrinth.com/mod/betterf3/version/TVXtAI9s), release-designated | Reformat local F3 debug information. | No server component. No added server information. | Active |
| [Better Mount HUD](https://modrinth.com/mod/better-mount-hud) | [1.3.1](https://modrinth.com/mod/better-mount-hud/version/M3Fe5t0L), release-designated | Mount and player HUD layout. | No server component. Uses ordinary vanilla mount state. | Active |
| [Paginated Advancements & Custom Frames](https://modrinth.com/mod/paginatedadvancements) | [2.8.0+26.2](https://modrinth.com/mod/paginatedadvancements/version/Ra3zz0eG), release-designated | Pagination and screen layout for vanilla advancements. | No server component. Custom advancement content is not selected or supplied. | Active |
| [Better Statistics Screen](https://modrinth.com/mod/better-stats) | [5.5.6+fn-26.2](https://modrinth.com/mod/better-stats/version/ga3HGfK0), release-designated | Search, filtering, sorting, and presentation of the player statistics supplied by vanilla. | No server assistance for this UI. Server statistics commands, sharing services, and extra server statistics are not selected. | Active |
| [Xaero's Minimap](https://modrinth.com/mod/xaeros-minimap) | [fabric-26.2-26.6.2](https://modrinth.com/mod/xaeros-minimap/version/kYWdcLLn), release-designated | Local terrain minimap and locally stored waypoints. | No server assistance for terrain or local waypoints. Server identification, enforced profiles, effects, and teleportation are not selected. | Active |
| [Xaero's World Map](https://modrinth.com/mod/xaeros-world-map) | [fabric-26.2-1.47.2](https://modrinth.com/mod/xaeros-world-map/version/W8qSt5Gs), release-designated | Locally recorded explored terrain and manual map selection. | No server assistance for recording or viewing terrain. Server-controlled world identification is not selected. Use Manual mode where world separation is ambiguous. | Active |
| [Zoomify (Zoom)](https://modrinth.com/mod/zoomify) | [2.17.0+mc26.2](https://modrinth.com/mod/zoomify/version/D64cvU6G), release-designated | Local camera zoom. | Client camera transforms and local configuration. Universal metadata also names a NeoForge-only library, not a Fabric requirement. | Active |
| [Sign Tweaks](https://modrinth.com/mod/signtweaks) | [2.103.0+26.2](https://modrinth.com/mod/signtweaks/version/piBkp75o), release-designated | Sign editor wrapping, multiline navigation, and copy/paste using vanilla sign editing. | Artifact has client entrypoints and no server entrypoint. Requires Mod Menu and Cloth Config; the full selected editor uses no companion server. | Active |
| [Book Tweaks](https://modrinth.com/mod/book-tweaks) | [1.2.0](https://modrinth.com/mod/book-tweaks/version/N3Xq3hFp), release-designated | Local book editor navigation, word wrapping, and multi-page paste. | Upstream describes a client-side editor. Vanilla book validation and limits remain authoritative. | Active |
| [LambDynamicLights - Dynamic Lights](https://modrinth.com/mod/lambdynamiclights) | [4.12.4+26.2](https://modrinth.com/mod/lambdynamiclights/version/XVsaQXSm), release-designated | Client-rendered held-item and entity lighting. | No server component. Does not change server block light, spawning, or game rules. | Active |
| [Chat Heads](https://modrinth.com/mod/chat-heads) | [1.3.2](https://modrinth.com/mod/chat-heads/version/rsO6BV1x), release-designated | Render player heads next to chat messages. | No server component. Uses player data already available on vanilla servers. | Active |
| [Iris Shaders](https://modrinth.com/mod/iris) | [1.11.4+26.2-fabric](https://modrinth.com/mod/iris/version/gxZWWnKH), release-designated | Local shader loading, shader selection, and rendering. Starts with shaders disabled. | Client rendering only. Exact upstream Sodium pin xJZxADzI is already selected. Bundled glsl-transformer 3.0.0-pre3 is part of this hash-pinned upstream release. | Active |
| [Mod Menu](https://modrinth.com/mod/modmenu) | [20.0.3](https://modrinth.com/mod/modmenu/version/iRo7AZXf), release-designated | Installed mod list and local configuration screens. | Client initializer only. Requires Fabric API and Text Placeholder API 3.1.0-beta.1+26.2, exactly as the release build declares. No server counterpart or server data needed. | Active |
| [Renice Shot](https://modrinth.com/mod/renice-shot), ID `ZDCwiIc3` | [1.2.1+mc26.2](https://modrinth.com/mod/renice-shot/version/roOTvshj), release-designated, Fabric 26.2 | Local high-resolution framebuffer capture and file saving. F9 captures at 3840 by 2160 by default. | Project is client required/server unsupported; the exact native descriptor is client-only. Requires existing Fabric API. Optional Mod Menu and Cloth Config are already present. No server counterpart or server data needed. | Active |
| [Sodium Extra](https://modrinth.com/mod/sodium-extra), ID `PtjYWJkn` | [mc26.2-0.9.5+fabric](https://modrinth.com/mod/sodium-extra/version/GJjGKm2A), release-designated, Fabric 26.2 | Local graphics controls and visual options. Extra HUD overlays remain disabled by default. | Project and native artifact are client-only. Requires the existing Sodium 0.9.2+mc26.2. Greenlight API 0.1.0+mc26.2 is bundled and hash-pinned. No server requirement. | Active |
| [Reese's Sodium Options](https://modrinth.com/mod/reeses-sodium-options), ID `Bh37bMuy` | [mc26.2-2.2.4+fabric](https://modrinth.com/mod/reeses-sodium-options/version/nnz8j4Hu), release-designated, Fabric 26.2 | Alternative Sodium options layout, search, and navigation. | Project and native artifact are client-only. Native Sodium requirement is exactly 0.9.2+mc26.2. Optional integrations do not require installation on the server. | Active |
| [Continuity](https://modrinth.com/mod/continuity), ID `1IjD5062` | [3.0.1+26.2](https://modrinth.com/mod/continuity/version/mgUN5Xz2), release-designated, Fabric 26.2 | Local connected textures and stacked glass-pane visual fix using its built-in packs. | Project and native artifact are client-only. Requires existing Fabric API; no server component or extra server data. Built-in texture assets are part of the pinned mod artifact. | Active |
| [Cubes Without Borders](https://modrinth.com/mod/cubes-without-borders), ID `ETlrkaYF` | [5.0.0+26.2](https://modrinth.com/mod/cubes-without-borders/version/ZM0HUAhK), release-designated, Fabric 26.2 | Borderless/windowed fullscreen and local window settings. | Project and native artifact are client-only. No required project dependency; optional config libraries are already present. None of its declared incompatible projects is active. No server component. | Active |
| [More Chat History](https://modrinth.com/mod/morechathistory), ID `8qkXwOnk` | [2.0.0](https://modrinth.com/mod/morechathistory/version/qpDhYv1Y), release-designated, Fabric 26.2 | Retain more already-received messages in local chat scrollback. | Project and native artifact are client-only, with no required project dependency. Does not add server-side history or require altered chat packets. | Active |
| [Default Options](https://modrinth.com/mod/default-options), ID `WEg59z5b` | [26.2.0.3+fabric-26.2](https://modrinth.com/mod/default-options/version/hS9ZtUOA), release-designated Fabric 26.2 | First-install settings and keybinding defaults with saved-preference preservation. | Project is client required/server unsupported. Native environment is universal, but initialization is client-only and local file/key handlers need no server. Requires existing Fabric API and Balm; native Balm minimum is 26.2.0.1, satisfied by 26.2.0.9. No server list is selected. | Active |

## Dependency audit

Fabric API is an explicitly selected platform library. Eight projects are transitive libraries. All nine have exact Fabric 26.2 pins and `side = "client"`. The selected platform library is release-designated. Upstream dependency provenance permits the audited Placeholder API beta-versioned artifact. Their local APIs and configuration functions do not require any remote-server installation. They add no selected gameplay content. Exact parents appear in `collection.toml`; exact versions and hashes remain authoritative in `mods/*.pw.toml`.

| Library | Classification | Client purpose and dependency evidence |
| --- | --- | --- |
| [Fabric API](https://modrinth.com/mod/fabric-api) | selected-library | Required by Renice Shot, Xaero's Minimap, YetAnotherConfigLib (YACL), Shulker Box Tooltip, Light Overlay, BetterF3, TCDCommons API, Dynamic FPS, OverlayLib, Balm, Entity Culling, Xaero's World Map, Inventory Profiles Next, Debugify, Mouse Tweaks, Sign Tweaks, Mod Menu, Better Statistics Screen, libIPN, Paginated Advancements & Custom Frames, Book Tweaks, Language Reload, Client Tweaks, Zoomify (Zoom), FastQuit, LambDynamicLights - Dynamic Lights. |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/mod/yacl) | dependency | Required by Light Overlay, Zoomify (Zoom). |
| [Cloth Config API](https://modrinth.com/mod/cloth-config) | dependency | Required by More Culling, BetterF3, Sign Tweaks, Paginated Advancements & Custom Frames, Status Effect Bars, FastQuit. |
| [TCDCommons API](https://modrinth.com/mod/tcdcommons) | dependency | Required by Better Statistics Screen. |
| [Fabric Language Kotlin](https://modrinth.com/mod/fabric-language-kotlin) | dependency | Required by Inventory Profiles Next, libIPN, Zoomify (Zoom). |
| [libIPN](https://modrinth.com/mod/libipn) | dependency | Required by Inventory Profiles Next. |
| [Balm](https://modrinth.com/mod/balm) | dependency | Required by Client Tweaks and Default Options. |
| [Text Placeholder API](https://modrinth.com/mod/placeholder-api) | dependency | Required by Mod Menu. |
| [OverlayLib](https://modrinth.com/mod/overlaylib) | dependency | Required by Light Overlay. |

Fabric API supplies modules required by Debugify, Book Tweaks, Paginated Advancements, and other artifacts even where their Modrinth records omit that dependency. Sodium bundles the Fabric modules it requires. Cloth Config provides both `cloth-config` and `cloth-config2`. The client closure records these artifact-derived edges as well as upstream required-project edges.

Bundled libraries stay inside their upstream artifacts. They are not separately selected features or duplicate packwiz downloads. The snapshot includes recursive module descriptors for Fabric API, Kotlin, YACL, LambDynamicLights, and the other active artifacts. Both Xaero artifacts bundle XaeroLib 1.8.5. Fabric Loader resolves the duplicate module.

Zoomify version `D64cvU6G` is universal. Its Modrinth record lists KotlinLangForge `1vrSzlao` as required, although that is a NeoForge dependency and has no Fabric build. The Fabric descriptor requires YACL and Fabric Loader. Fabric Language Kotlin is already in the closure for IPN. This is the sole recorded loader-specific metadata exception, in `upstream-metadata.json`. The checker still requires the remaining Modrinth dependencies.

## Upstream release and dependency provenance

All 37 active features use upstream release-designated Fabric 26.2 versions.
The same release requirement applies to explicitly selected Fabric API.
Resolved and bundled libraries remain part of the selected releases' official
closure, even when their version identifiers look like prereleases. This is not
permission to choose an unrelated prerelease or substitute an unaudited version.

- Mod Menu's [v20.0.3 build properties](https://github.com/TerraformersMC/ModMenu/blob/v20.0.3/gradle.properties) set `text_placeholder_api_version=3.1.0-beta.1+26.2` and declare Placeholder API required. The separately installed artifact is pinned to `NDqH16LT`. Its original upstream declaration and exact audited pin are recorded on Mod Menu's dependency edge in the snapshot.
- Sign Tweaks' release declares Mod Menu and Cloth Config required. Both are now active, so that dependency path is satisfied without a server companion.
- Iris' exact Sodium requirement is `xJZxADzI`, our existing Sodium 0.9.2 pin. Its native descriptor accepts Sodium `0.9.x` and Fabric Loader `>=0.12.3`. Sodium 0.9.2's exclusion of Iris `<=1.11.2` does not apply to Iris 1.11.4. Sodium and Fabric Loader 0.20.1 remain unchanged.
- Iris bundles `io_github_douira_glsl-transformer` version `3.0.0-pre3`. Client Tweaks bundles `shogi_api` version `26.2.0.1-SNAPSHOT`. The containing release hashes pin these components. Neither is an independent pack selection or separate download.
- Client Tweaks requires Balm. The resolved library pin is `26.2.0.9+fabric-26.2`. [Release-tagged client initialization](https://github.com/TwelveIterations/ClientTweaks/blob/v26.2.0.6/fabric/src/main/java/net/blay09/mods/clienttweaks/fabric/client/FabricClientTweaksClient.java) registers its config and tweaks on the client. Enabled defaults act on local UI, rendering, targeting, and ordinary inputs. The [configuration record](configuration.md#client-tweaks) lists the deliberately disabled overlaps.

The artifact audit verifies download hashes and recursive Fabric descriptors.
All newly installed records use `side = "client"`. An upstream-required library
would still be rejected if it introduced a mandatory server requirement or a
server-only module. Runtime verification remains open.

## Light Overlay identity correction

The accepted project is `8qVa1XCN`, slug `lightoverlay`, release `AT01Q5uN`
(`2.12.0+26.2`). Its [release metadata](https://api.modrinth.com/v2/version/AT01Q5uN)
requires OverlayLib `OQkmYeS8` (`0.12.0+26.2`) exactly. OverlayLib is a resolved
client-only library. Existing Fabric API and YACL pins satisfy the other required
projects. No existing mod pin changed. Both new artifacts declare a client
Fabric environment and no dependency conflicts with the selected rendering stack.
Upstream advertises Iris support; actual rendering remains a manual test.

The earlier exclusion queried the different Modrinth project `YfOlc91N`, slug
`light-overlay`, which shares the display name. That incorrect collection and
snapshot identity has been removed. Project-ID substitution regressions now
reject the similarly named project. The correct release's native Fabric module
ID and JAR filename still contain `light-overlay`; those are upstream artifact
identifiers, not its Modrinth project slug. All 30 original features remain active,
with zero blocked features.

## Screenshot selection

[FO's version-specific mod list](https://github.com/Fabulously-Optimized/fabulously-optimized/blob/main/INCLUDED-MODS.md)
uses Renice Shot for 26.2 and Fabrishot on older lines. The selected project is
Renice Shot `ZDCwiIc3`, version `roOTvshj`, the newest release-designated Fabric
26.2 artifact when checked. Native requirements are Minecraft `26.2`, Fabric
Loader `>=0.19.5`, Java `>=25`, and Fabric API. Existing pins satisfy them.
The artifact has no bundled modules or declared incompatible projects.

The [release source](https://github.com/wechirok/renice-shot/blob/bca7c14881a592ca3df2d309968cb29bdaa32728/src/main/java/me/wechirok/reniceshot/ReniceShot.java)
registers a local key mapping and captures the client framebuffer to a local
file. No server handshake, companion, or network data beyond vanilla rendering
is required. Existing Mod Menu and Cloth Config supply the optional config UI.
The F9 collision with Light Overlay is resolved by the documented F7 override.
Runtime screenshot capture and resolution restoration remain untested.

## Staged investigations

These projects are recorded only in `candidates.toml`. They have no active
packwiz records and are absent from exports. Downloaded artifacts were
SHA-512 verified outside the repository. Static findings do not establish
runtime compatibility or a performance benefit.

| Candidate and audited release | Findings | Decision and next gate |
| --- | --- | --- |
| [Config Manager](https://modrinth.com/mod/configmanager), `jlNms3Jp`, [1.1.4](https://api.modrinth.com/v2/version/okecULrz), release | Native Fabric environment is `*`, with a client initializer, local file-copy startup adapter, and optional native Mod Menu UI. The Modrinth version declares Mod Menu required, already available. However, [project API metadata](https://api.modrinth.com/v2/project/jlNms3Jp) declares client unsupported and server required, contradicting the client-facing description and native artifact. | Blocked. Do not bypass the client-only validator. Reconcile upstream metadata, then test first-install defaults, preservation of existing files, and explicit update/reset in a disposable profile. |
| [Ixeris](https://modrinth.com/mod/ixeris), `p8RJPJIC`, [4.6.11+26.2-fabric](https://api.modrinth.com/v2/version/qXHd9Vb4), release | Project and native artifact are client-only, Minecraft exactly 26.2, Loader >=0.16.0, and no required project dependencies. [Release-tagged source](https://github.com/decce6/ixeris/tree/124f06bd5a9530d9af9529d5af885275b8be77b1) changes local event polling and input. Buffered raw input is Windows-specific; benefit depends on OS and polling hardware. | Ready for review, inactive. Measure frame times/input behavior and test threading with Sodium, Iris, borderless mode, focus changes, and screenshots before promotion. |
| [ModernFix-mVUS](https://modrinth.com/mod/modernfix-mvus), `TjSm1wrD`, [5.27.19-build.2](https://api.modrinth.com/v2/version/50uUra83), release | Universal Fabric artifact has common/client initializers and bundled MixinExtras 0.5.4. Native Minecraft range is `~26.2-`; API lists Fabric 26.2 and requires existing Fabric API. Local startup/model/memory optimizations are the proposed selection; server fixes are outside it. | Under investigation, inactive. Complete exact-build client-function/range and overlap audits, then benchmark startup/memory and test resource reloads, rendering, and a vanilla-server join. No performance claim is established. |

Config Manager's current [source inspection](https://github.com/TheBossMagnus/Config-Manager/tree/adf332de967b8eef237fa5ffb0f020688548dcc0)
shows the usual copy path skips existing files. Startup also supports explicit
update/reset flags. This is promising for preserving personal preferences, but
it does not resolve the upstream environment disagreement. Defaults remain in
the current pack locations until an approved promotion and migration pass.
ModernFix's inspected source and native mixin lists include both client and
server work; finding a client initializer alone is insufficient for promotion.

## Intentional rejections

AppleSkin, Jade, Easy Shulker Boxes, Bookshelf Inspector, and Client Sort are rejected regardless of target availability. AppleSkin and the rejected inspector/container tools do not meet the selected strict server-independence policy. Jade is deliberately excluded. IPN owns sorting, so Client Sort is not selected. The source checker rejects their IDs or slugs, and an undeclared lock also fails the active-set check.

No substitute, shader pack, standalone resource pack, gameplay content, or server companion has been added. Continuity's two built-in visual packs are enabled. See [configuration decisions](configuration.md) and [runtime acceptance](acceptance-tests.md).
