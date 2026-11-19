# Client-only mod audit

Evidence checked on 2026-11-17 against the [Modrinth API](https://docs.modrinth.com/api/) and the exact downloaded Fabric artifacts. [The offline snapshot](upstream-metadata.json) records project/version identity, compatibility declarations, files, dependency edges, and recursive Fabric descriptors. Download hashes were checked during the audit and again by packwiz export.

Renice Shot was added and audited on 2026-11-18. The prior 39 artifact pins are
unchanged. That addition completed the 30 original features plus Renice Shot.

Five FO-inspired additions were audited on 2026-11-18. On 2026-11-19, the
configuration evaluation selected Configured Defaults to replace Default Options.
The other 45 locks are unchanged from the preceding baseline. There are still
37 intentional features and nine libraries at that point.
The refinement below adds three features and Searchables, bringing the maintained
26.2 line to 40 features and ten libraries. The subsequent Prickle classification
review below adds Enchantment Descriptions, reaching 41 features and eleven libraries.

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
| [Configured Defaults](https://modrinth.com/mod/configured-defaults), ID `SISoSFPP` | [26.2.0](https://api.modrinth.com/v2/version/oM0C4RRZ), release-designated Fabric 26.2 | Early missing-file defaults and missing-options-key merging. | Client/server installations are independently optional; native environment `*` and the early Fabric adapter perform local file operations. No networking or server contribution is needed. Requires Minecraft `~26.2-` and Loader `>=0.19.0`, satisfied by 0.20.1. No required project dependencies or bundled JARs. | Active |

## Dependency audit

Fabric API is an explicitly selected platform library. Ten projects are transitive libraries. All eleven have exact Fabric 26.2 pins and `side = "client"`. The selected platform library is release-designated. Upstream dependency provenance permits the audited Placeholder API beta-versioned artifact. Their local APIs and configuration functions do not require any remote-server installation. They add no selected gameplay content. Exact parents appear in `collection.toml`; exact versions and hashes remain authoritative in `mods/*.pw.toml`.

| Library | Classification | Client purpose and dependency evidence |
| --- | --- | --- |
| [Fabric API](https://modrinth.com/mod/fabric-api) | selected-library | Required by Renice Shot, Xaero's Minimap, YetAnotherConfigLib (YACL), Shulker Box Tooltip, Light Overlay, BetterF3, TCDCommons API, Dynamic FPS, OverlayLib, Balm, Entity Culling, Xaero's World Map, Inventory Profiles Next, Debugify, Mouse Tweaks, Sign Tweaks, Mod Menu, Better Statistics Screen, libIPN, Paginated Advancements & Custom Frames, Book Tweaks, Language Reload, Client Tweaks, Zoomify (Zoom), FastQuit, LambDynamicLights - Dynamic Lights, BetterGrassify, Controlling, Searchables, Food Effect Tooltips, Prickle, Enchantment Descriptions. |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/mod/yacl) | dependency | Required by Light Overlay, Zoomify (Zoom). |
| [Cloth Config API](https://modrinth.com/mod/cloth-config) | dependency | Required by More Culling, BetterF3, Sign Tweaks, Paginated Advancements & Custom Frames, Status Effect Bars, FastQuit, Food Effect Tooltips. |
| [TCDCommons API](https://modrinth.com/mod/tcdcommons) | dependency | Required by Better Statistics Screen. |
| [Fabric Language Kotlin](https://modrinth.com/mod/fabric-language-kotlin) | dependency | Required by Inventory Profiles Next, libIPN, Zoomify (Zoom). |
| [libIPN](https://modrinth.com/mod/libipn) | dependency | Required by Inventory Profiles Next. |
| [Balm](https://modrinth.com/mod/balm) | dependency | Required by Client Tweaks. |
| [Text Placeholder API](https://modrinth.com/mod/placeholder-api) | dependency | Required by Mod Menu. |
| [OverlayLib](https://modrinth.com/mod/overlaylib) | dependency | Required by Light Overlay. |
| [Searchables](https://modrinth.com/mod/searchables) | dependency | Required by Controlling. |
| [Prickle](https://modrinth.com/mod/prickle) | dependency | Local Enchantment Descriptions config. Exact environment classification review below; no server companion. |

Fabric API supplies modules required by Debugify, Book Tweaks, Paginated Advancements, and other artifacts even where their Modrinth records omit that dependency. Sodium bundles the Fabric modules it requires. Cloth Config provides both `cloth-config` and `cloth-config2`. The client closure records these artifact-derived edges as well as upstream required-project edges.

Bundled libraries stay inside their upstream artifacts. They are not separately selected features or duplicate packwiz downloads. The snapshot includes recursive module descriptors for Fabric API, Kotlin, YACL, LambDynamicLights, and the other active artifacts. Both Xaero artifacts bundle XaeroLib 1.8.5. Fabric Loader resolves the duplicate module.

Zoomify version `D64cvU6G` is universal. Its Modrinth record lists KotlinLangForge `1vrSzlao` as required, although that is a NeoForge dependency and has no Fabric build. The Fabric descriptor requires YACL and Fabric Loader. Fabric Language Kotlin is already in the closure for IPN. This is the sole recorded loader-specific metadata exception, in `upstream-metadata.json`. The checker still requires the remaining Modrinth dependencies.

## Upstream release and dependency provenance

All 41 active features use upstream release-designated Fabric 26.2 versions.
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
| [Ixeris](https://modrinth.com/mod/ixeris), `p8RJPJIC`, [4.6.11+26.2-fabric](https://api.modrinth.com/v2/version/qXHd9Vb4), release | Project and native artifact are client-only, Minecraft exactly 26.2, Loader >=0.16.0, and no required project dependencies. [Release-tagged source](https://github.com/decce6/ixeris/tree/124f06bd5a9530d9af9529d5af885275b8be77b1) changes local event polling and input. Buffered raw input is Windows-specific; benefit depends on OS and polling hardware. | Staged pending benchmarking, inactive. Measure frame times/input behavior and test threading with Sodium, Iris, borderless mode, focus changes, and screenshots before promotion. |
| [ModernFix-mVUS](https://modrinth.com/mod/modernfix-mvus), `TjSm1wrD`, [5.27.19-build.2](https://api.modrinth.com/v2/version/50uUra83), release | Universal Fabric artifact has common/client initializers and bundled MixinExtras 0.5.4. Native Minecraft range is `~26.2-`; API lists Fabric 26.2 and requires existing Fabric API. Local startup/model/memory optimizations are the proposed selection; server fixes are outside it. | Staged pending benchmarking, inactive. Complete exact-build overlap audits, then benchmark startup/memory and test resource reloads, rendering, and a vanilla-server join. No performance claim is established. |

Config Manager's current [source inspection](https://github.com/TheBossMagnus/Config-Manager/tree/adf332de967b8eef237fa5ffb0f020688548dcc0)
shows the usual copy path skips existing files. Startup also supports explicit
update/reset flags. This is promising for preserving personal preferences, but
it does not resolve the upstream environment disagreement. The 2026-11-19 [configuration evaluation](configuration.md#defaults-manager-evaluation-2026-11-19)
rechecked that metadata. The final selection is Configured Defaults because it
can fill missing fields in launcher-created partial options files while
preserving existing values. It cannot replace a populated resource-pack list or
change native key reset defaults. Default Options is removed; no competing
manager is installed.
ModernFix's inspected source and native mixin lists include both client and
server work; finding a client initializer alone is insufficient for promotion.

## Intentional rejections

AppleSkin, Jade, Easy Shulker Boxes, Bookshelf Inspector, and Client Sort are rejected regardless of target availability. AppleSkin and the rejected inspector/container tools do not meet the selected strict server-independence policy. Jade is deliberately excluded. IPN owns sorting, so Client Sort is not selected. The source checker rejects their IDs or slugs, and an undeclared lock also fails the active-set check.

No substitute, shader pack, standalone resource pack, gameplay content, or server companion has been added. Continuity's two built-in visual packs are seeded when options are absent. Existing selections are preserved. See [configuration decisions](configuration.md) and [runtime acceptance](acceptance-tests.md).

## QoL and performance refinement, 2026-11-19

Only the maintained 26.2 branch installs the following three additions. The 26.3
bootstrap receives migration intent and this evaluation, not these artifacts.
At pack 26.2.0.8.0, the maintained baseline was 40 features and ten libraries. All 46 preceding
artifact locks and their upstream project records remain unchanged. No Minecraft,
Prism or Modrinth App runtime acceptance was performed.

| Candidate | Audited Fabric 26.2 release | Disposition | Evidence and scope |
| --- | --- | --- | --- |
| [BetterGrassify](https://modrinth.com/mod/bettergrassify), `m5T5xmUy` | [1.8.7+fabric.26.2, r4yqxYQl](https://api.modrinth.com/v2/version/r4yqxYQl) | Added on 26.2 | Client-only artifact. Local block-model/quad rendering needs no server installation or extra data. Requires existing Fabric API. Fancy grass, resource-pack compatibility mode, paths/farmland/Nether changes disabled, and extra snow layers disabled are initial defaults. |
| [Controlling](https://modrinth.com/mod/controlling), `xv94TkTM` | [26.2.4, sZHXONgm](https://api.modrinth.com/v2/version/sZHXONgm) | Added on 26.2 | Client-only keybinding screen search, free-key view and conflict filtering. Requires Fabric API and Searchables. Does not assign bindings or resolve conflicts automatically; F7 is unchanged. |
| [Enchantment Descriptions](https://modrinth.com/mod/enchantment-descriptions), `UVtY3ZAC` | [26.2.0.2, PTAK0HD2](https://api.modrinth.com/v2/version/PTAK0HD2) | Added after the classification review below | The initial deferral concerned metadata only. Client tooltip callback and vanilla translations are local. Required Prickle `aaRl8GiW`, release [26.2.0.3, XdvtdRYJ](https://api.modrinth.com/v2/version/XdvtdRYJ), declares server required in the [project API](https://api.modrinth.com/v2/project/aaRl8GiW). Its universal descriptor and local config implementation contradict that label. The exact-version exception below resolves this pairing. |
| [Crash Assistant](https://modrinth.com/mod/crash-assistant), `ix1qq8Ux` | [1.11.14, alR3tamq](https://api.modrinth.com/v2/version/alR3tamq) | Deferred due to compatibility | API is client-only; native universal language adapter starts a local child process early enough to diagnose many initialization failures. No required Modrinth projects; embedded application/libraries still need auditing. Launcher logs already provide the basic reporting path. Early privacy-default ordering with Configured Defaults is unresolved. |
| [Better Block Entities](https://modrinth.com/mod/better-block-entities), `ONZm0H7Y` | [1.3.9+mc26.2, n5mL5flA](https://api.modrinth.com/v2/version/n5mL5flA) | Deferred due to compatibility | Client-only; native Sodium `>=0.9.0`, release changelog supports 0.9.0 through 0.9.2, including our 0.9.2. Open Iris lighting report [#145](https://github.com/EdeenMC/betterblockentities/issues/145), Iris/Xaero shader-toggle map report [#156](https://github.com/EdeenMC/betterblockentities/issues/156), and acknowledged transition-lighting limitation [#7](https://github.com/EdeenMC/betterblockentities/issues/7) prevent promotion without resolving applicability to this stack. |
| [Ixeris](https://modrinth.com/mod/ixeris), `p8RJPJIC` | [4.6.11+26.2-fabric, qXHd9Vb4](https://api.modrinth.com/v2/version/qXHd9Vb4) | Staged pending benchmarking | Client event polling and Windows buffered raw input. The [upstream benchmarks](https://github.com/decce6/Ixeris/tree/124f06bd5a9530d9af9529d5af885275b8be77b1#benchmarks) are real workload-specific reports, not Lantern Crossing measurements. No required project dependency. |
| [ModernFix-mVUS](https://modrinth.com/mod/modernfix-mvus), `TjSm1wrD` | [5.27.19-build.2, 50uUra83](https://api.modrinth.com/v2/version/50uUra83) | Staged pending benchmarking | Independent local startup/model/memory fixes are eligible in principle; server fixes confer no remote benefit. Required Fabric API is present; native Minecraft `~26.2-` and Loader `>=0.16.10` fit. Broad patch interactions and benefit remain unqualified. |
| [Tooltip Tweaks](https://modrinth.com/mod/tooltiptweaks), `evJ7VC0w` | [3.0.1, mo7PzvJD](https://api.modrinth.com/v2/version/mo7PzvJD) | Deferred due to compatibility | Reads client FOOD/CONSUMABLE components, not authoritative current saturation/exhaustion. Fabric API `>=0.154.1` and YACL `>=3.9.5` are satisfied. Source has inconsistent cake saturation and truncated fractional icons; broad container/map/enchantment/effect rewrites also overlap dedicated tools. No 26.3 Fabric release found. |
| [Food Effect Tooltips](https://modrinth.com/mod/foodeffecttooltips), `GGfyJWnG` | [2.1.2+26.2, aXyL1zFA](https://api.modrinth.com/v2/version/aXyL1zFA) | Added on 26.2 | Client-only callback reads vanilla CONSUMABLE and DEATH_PROTECTION components, including effect duration, amplifier and probability. No player saturation/exhaustion estimate or extra server data. Suspicious-stew reveal stays off. No duplicate Tooltip Tweaks installation. |

### Source and dependency evidence

The hash-verified new artifact descriptors are in [upstream-metadata.json](upstream-metadata.json).
All new packwiz entries are pinned and `side = "client"`. Required libraries
remain separate from features. Searchables [1.0.1, bvFby61J](https://api.modrinth.com/v2/version/bvFby61J),
project `fuuu3xnx`, is the sole new library, with a client-only native descriptor
and no bundled JAR. Its Modrinth-required Fabric API edge is recorded even though
native metadata only recommends Fabric API. Controlling's native Searchables
`>=1.0.1`, Java `>=25`, Loader `>=0.19.3` and exact Minecraft `26.2` all pass.
No new selected artifact or dependency is a prerelease.

Food Effect Tooltips lists no dependencies in the Modrinth version response.
Its exact artifact's `fabric.mod.json` requires Fabric API and Cloth Config.
Those edges are recorded in `client_required` with artifact URL and native-field
provenance, and their reverse parents are reconciled in `collection.toml`.
Packwiz's native download metadata remains unchanged apart from required pinning.
No guessed or optional library is installed.

Source inspection used these revisions. A version-branch inspection is supporting
evidence; it is not a claim of a reproducible upstream source build.

- BetterGrassify [release tag 33df4f9](https://github.com/UltimatChamp/BetterGrassify/tree/33df4f9ef7f9bdbacb5b9fade4050542f7dcb2bf), `BetterGrassifyBlockStateModel`, `BetterGrassifyConfig` and Sodium meshing mixin. Client block/tint/light data supplies rendering. Compatibility mode limits replacement to full quads. Sodium, Iris, Continuity and More Culling have no declared hard conflict; visual interaction still needs owner acceptance.
- Controlling [26.2 source 3521164](https://github.com/jaredlll08/Controlling/tree/3521164fd53771ed95afe4868310ac0f88df8ceb), `NewKeyBindsScreen`, `NewKeyBindsList` and client mixins; Searchables [10cb075](https://github.com/jaredlll08/searchables/tree/10cb075ae5f3526bda799b9a37d8e2769a0277d6). Searches local registered mappings. No companion, handshake, protocol or new keybind is selected.
- Food Effect Tooltips [26.2 source 27b7894](https://github.com/DaFuqs/FoodEffectTooltips/tree/27b7894278716f5988f6a875bd80483e9e9f3316), `FoodeffecttooltipsClient`, `TooltipHelper` and `FoodEffectsConfig`. Probability is read from `ApplyStatusEffectsConsumeEffect`; no current-player food state is consulted. Vanilla item components support these tooltips on an unmodified server. Plugin behavior absent from those components is unknown and is not advertised.
- Enchantment Descriptions [df15f5b](https://github.com/Darkhax-Minecraft/Enchantment-Descriptions/tree/df15f5bc42a0d0b74356fec64dcfa4162701d149) loads Prickle config and resolves description translation keys. Prickle [19934df](https://github.com/Darkhax-Minecraft/PrickleMC/tree/19934df33b5f874d5849f272a663f0db97c4c099) uses local JSON file services; no required remote handshake was found. The later exact-artifact review below resolves this metadata-policy deferral. Vanilla translations are supplied, but plugin-defined enchantments need matching local descriptions; arbitrary plugin behavior cannot be inferred.
- Tooltip Tweaks [5a587ac](https://github.com/lunarbunten/tooltiptweaks-mod/tree/5a587ac31ae8c6f047ce234a52bdf7f4b9c0ae3e), `NutritionTooltips` hard-codes cake saturation `2.4F`; `FoodGuiTooltip` uses `2.8F` and casts saturation to `int`. Ordinary food values use local `FoodProperties`. It could supply hunger-only text, but that does not justify the broad rewrite set for this milestone. Food Effect Tooltips supplies the narrower effect use case with probabilities. No nutritional HUD or substitute is added.
- Crash Assistant [26.2 entrypoint dd39ca5](https://github.com/KostromDan/Crash-Assistant/tree/dd39ca5c8d2d292cc2c0f8c89123b7df1e3ffc4b) and [shared application 93fd896](https://github.com/KostromDan/Crash-Assistant/tree/93fd8960ed4f9e55a9f5c34ab2f8ce2c4308fc14). The inspected upload path calls `PrivacyPolicyDialog.ensurePrivacyPolicyAccepted`. Uploaded logs may contain file paths, chat, server addresses and account identifiers. `general.send_uploaded_logs_data_to_kostromdan_dev` defaults true and includes UUID metadata after an upload; it can be disabled. No automatic crash-log upload was found in the inspected path. `DefaultConfigModsCompatibility` seeds only YOSBR and Config Manager directories. Adding direct live overrides to force privacy defaults would violate Lantern Crossing's settings policy. Child-process/launcher interaction and exact embedded-code correspondence remain unaudited, so no diagnostics mod, telemetry, upload service or support link is installed. Use launcher-local logs and review/redact before deliberately sharing them.

### Performance mechanisms and selection

[FO at ef27a0b](https://github.com/Fabulously-Optimized/fabulously-optimized/tree/ef27a0ba425721fdaa8255251f01ed1301249cf4/Packwiz/26.2)
uses the same BetterGrassify, BBE, Ixeris, ModernFix-mVUS and Crash Assistant
artifacts audited here. Its BetterGrassify template sets `betterGrassMode` OFF;
Lantern Crossing deliberately selects restrained fancy grass instead. FO's
ModernFix template disables branding, measurement, telemetry-removal and snapshot
easter-egg patches. Those are FO choices, not measured compatibility fixes for
Lantern Crossing. We do not copy FO's `side = "both"` labels or its diagnostics
configuration. FO supplies comparison evidence and does not endorse this pack.
Controlling and Food Effect Tooltips are independent QoL selections.

| Performance candidate | Mechanism and bottleneck | Evidence quality | Overlap and risk | Measurable next gate |
| --- | --- | --- | --- | --- |
| Better Block Entities | Moves static chests, signs, beds and other supported block entities into terrain meshes; uses immediate rendering while animating. Reduces block-entity-heavy CPU submission/draw overhead. | Upstream shows a chest-heavy comparison; FO uses the exact release. No Lantern Crossing measurement. | Complements culling rather than replacing it; renderer, Iris, lighting, resource-pack models, visibility and animation transitions remain sensitive. Reports above are unresolved for our exact stack, not confirmed reproductions here. | Resolve relevant reports, then compare a fixed block-entity-heavy scene, transitions, resource reloads, maps and shader toggles. Deferred. |
| Ixeris | Polls events on the main thread, renders separately, and batches Windows raw mouse input. Targets high-polling input/JNI cost. | Upstream supplies OS/polling-rate benchmarks with large Windows gains and smaller Linux gains. These are conditional reports, not universal FPS promises. | Thread/context/focus handling touches Dynamic FPS, borderless fullscreen, Iris and screenshot capture. It does not replace Sodium's chunk renderer. | Owner compares frame-time distribution and input correctness with fixed OS, device polling rate, FPS cap and scene. Remains staged. |
| ModernFix-mVUS | Local startup, resource/model caches, memory use and bug fixes. Targets loading/allocation bottlenecks. | General upstream claims largely cover other versions and heavier packs. No controlled measurement for this restrained 26.2 pack. | Some scope overlaps FerriteCore memory, Lithium caches, Debugify bugs and ImmediatelyFast/BadOptimizations rendering work. [82fd9db](https://github.com/coredex-source/ModernFix---mVUS/tree/82fd9dbff079b58aeae447fefb3dbaac4e78dc68) disables its item-cache patch when Lithium is present; dynamic resources default off. That is not a complete conflict proof. | Owner compares cold/warm startup, heap after GC and resource reloads before considering a separate exact-build promotion. Keep experimental model loading off. Remains staged. |

AppleSkin, Jade, WTHIT, SimpleCoords, Overlay Stats and InventoryHUD+ are not
added or replaced in this milestone. No shaders, standalone resource packs,
server artifacts or content mods are introduced. All runtime results stay pending.

## Prickle environment classification review

The original deferral was overly conservative. It reproduced a metadata-policy
rejection, not a Fabric version incompatibility or demonstrated server companion
requirement. Exact artifact/source inspection supports independent client use
of the pair below. Runtime acceptance is still uncompleted.

| Artifact | Project/version IDs | Published release and environment | Selected use |
| --- | --- | --- | --- |
| [Enchantment Descriptions 26.2.0.2](https://api.modrinth.com/v2/version/PTAK0HD2) | `UVtY3ZAC` / `PTAK0HD2` | Fabric 26.2 release; API client required/server optional; native `client`. | Local descriptions of standard vanilla enchantments. Active feature. |
| [Prickle 26.2.0.3](https://api.modrinth.com/v2/version/XdvtdRYJ) | `aaRl8GiW` / `XdvtdRYJ` | Fabric 26.2 release; [project API](https://api.modrinth.com/v2/project/aaRl8GiW) client required/server required; native `*`. | Local configuration library. Active resolved dependency, not a feature or remote companion. |

Enchantment Descriptions' Modrinth edge and native `prickle: "*"` do not specify
an exact library version. Its build compiles against 26.2.0.2; Packwiz resolved
the newest stable Fabric 26.2 release, 26.2.0.3. The used configuration methods
exist in that artifact. Both JARs require Loader `>=0.19.3`, Java `>=25`,
Minecraft `>=26.2` and Fabric API. The pack's 0.20.1/25/26.2/existing Fabric API
pins satisfy the complete native graph. Neither artifact bundles libraries.
No earlier mod version changed. Every download/export remains client-only.

### Reproduced rejection and release correspondence

Before the change, isolated `check_mod()` fixtures accepted the Enchantment
Descriptions artifact and rejected Prickle with `unsupported client or mandatory
server requirement`. The same proposed artifacts passed native dependency
identity, version and hard-break checks alongside the maintained baseline.
The rejected field is project-level `server_side`; Modrinth v2 version responses
provide no separate environment override. No other dependency caused the rejection.

Both SHA-512-verified Modrinth binaries are byte-identical to their published
[Maven Prickle binary](https://maven.blamejared.com/net/darkhax/pricklemc/prickle-fabric-26.2/26.2.0.3/prickle-fabric-26.2-26.2.0.3.jar)
and [Maven Enchantment Descriptions binary](https://maven.blamejared.com/net/darkhax/enchdesc/enchdesc-fabric-26.2/26.2.0.2/enchdesc-fabric-26.2-26.2.0.2.jar).
Their versioned source JARs match the inspected immutable Git revisions:

- [Prickle fabric sources 26.2.0.3](https://maven.blamejared.com/net/darkhax/pricklemc/prickle-fabric-26.2/26.2.0.3/prickle-fabric-26.2-26.2.0.3-sources.jar): all 36 Java source files match [19934df](https://github.com/Darkhax-Minecraft/PrickleMC/tree/19934df33b5f874d5849f272a663f0db97c4c099). That commit precedes publication by 45 seconds and its change matches the release notes.
- [Enchantment Descriptions fabric sources 26.2.0.2](https://maven.blamejared.com/net/darkhax/enchdesc/enchdesc-fabric-26.2/26.2.0.2/enchdesc-fabric-26.2-26.2.0.2-sources.jar): all seven Java files match [df15f5b](https://github.com/Darkhax-Minecraft/Enchantment-Descriptions/tree/df15f5bc42a0d0b74356fec64dcfa4162701d149). Its translation fix precedes publication by 117 seconds. All 25 artifact language maps equal the source maps after JSON parsing.

`javap -p -c -verbose` inspected all 46 Prickle and seven Enchantment Descriptions
classes, including private methods and constant-pool references. The artifact
entrypoints/configuration/tooltip code agrees with the sources above. Binary
hashes, source URLs/SHA-256, class counts and source-match evidence are recorded
in [upstream-metadata.json](upstream-metadata.json). This is strong release
correspondence, not a claim of a signed or independently reproducible upstream
build. No Minecraft class was executed and neither launcher was run.

### Implementation findings

Prickle is a shared local configuration library. Its main initializer logs
initialization and schedules an update check; the client initializer is empty.
Both native mixin files have empty common, client and server lists. Its Fabric
service supplies `FabricLoader.getConfigDir()` to JSON configuration loading.
The other service supplies Minecraft value codecs. References under
`net.minecraft.network.chat` serialize text/style values; they register no packets.
There are no Minecraft networking registrations, server lifecycle hooks,
server-only mixins, companion handshakes or server-state reads in the inspected
artifact. Being usable in either environment does not require a paired install.

The library does make an asynchronous HTTP `HEAD` request to
`https://updates.blamejared.com/get?n=prickle&gv=<game-version>&ml=fabric`.
The daemon task has five-second connect/read timeouts and catches exceptions.
Its result is only logged; it does not gate configuration or tooltip display,
fetch executable code, or upload logs. The endpoint receives normal connection
metadata and game/mod-loader query values. No switch disabling this request was
found in this exact release. This external version check is disclosed, not
misrepresented as zero network activity or a Minecraft server protocol.

Enchantment Descriptions has a no-op common initializer and a logging client
initializer. Its three actual mixins are in the client-only list. They capture
the tooltip item and insert descriptions after vanilla enchantment lines.
`ENCHANTMENTS`/`STORED_ENCHANTMENTS` components and locally available registry
identifiers supply the input; local language keys supply the prose. The artifact
contains 43 vanilla enchantment description keys in English, with more languages
and optional mod translations. Unknown descriptions are skipped and logged,
not inferred from arbitrary server plugin behavior. There is no custom networking
or synchronized mod data. Only standard vanilla enchantments are selected here.

Prickle reads valid saved values and writes its canonical config, including
metadata/default fields. It may rewrite file formatting. Malformed files receive
an upstream backup/default recovery path. Configured Defaults seeds our minimal
shift-gated template only when `config/enchdesc.json` is absent; it does not
replace existing valid user choices. Food Effect Tooltips handles consumable and
death-protection effects, while Enchantment Descriptions handles enchantments.
Tooltip Tweaks remains inactive. No duplicate tooltip provider or key mapping is
introduced.

### Exact metadata exception

Option B is selected. `environment_exceptions` in the existing upstream snapshot
retains the original required/required labels and records the source evidence.
It authorizes only Prickle `aaRl8GiW`/`XdvtdRYJ` with its exact filename/SHA-512
and canonical stored Fabric-descriptor SHA-256, on Fabric 26.2, required by the
exact `UVtY3ZAC`/`PTAK0HD2` feature filename/SHA-512. Every incoming parent must
match that context and its real upstream dependency edge. No project-specific
parser condition or unbounded allowlist is added.

The only overridden interpretation is Modrinth's project-level server label.
Unsupported clients, native server-only modules, artifact identity/integrity,
release designation, dependency presence/ranges and client-only export remain
mandatory. Changed pins/descriptors/parents or corrected metadata fail pending
re-evaluation. Orphan/duplicate audits fail. Both validation CLIs print the audit
notice. This reviewed source finding is not a runtime compatibility proof.

### Upstream intent and clarification draft, not submitted

The README describes a reusable JSON configuration library. Its build marks the
mod as non-client-exclusive, consistent with universal native metadata. That
explains multi-environment publication but does not establish a companion-server
requirement. [Issue #6](https://github.com/Darkhax-Minecraft/PrickleMC/issues/6)
previously asked to mark the project optional; it is closed with no comments.
No maintainer confirmation of a publishing error or correction was found.
A project-label correction remains preferable. Nothing was posted or sent.

Proposed issue title: **Clarify independent client/server use and Modrinth environment labels**

> Modrinth project `aaRl8GiW` currently reports client and server required. For
> Fabric 26.2, version `XdvtdRYJ`, the published artifact has environment `*`,
> empty mixin lists and a local configuration service. Its initializer's HTTP
> update check is asynchronous and does not expect a Minecraft server companion.
> Enchantment Descriptions `PTAK0HD2` uses this library for local tooltip config.
> Could you confirm independent client-only use on vanilla servers and clarify
> whether the project labels can express that? The exact binaries match the
> versioned Maven artifacts; source revisions are `19934df` and `df15f5b`.
> The earlier optional-label question is #6. This request concerns environment
> classification, not removing the library dependency from Enchantment Descriptions.

### Simpler alternatives considered

| Option and exact Fabric 26.2 discovery | Assessment |
| --- | --- |
| Existing pack | Food Effect Tooltips supplies effect data; Shulker Box Tooltip supplies container previews. Neither explains enchantments. Tooltip Tweaks' enchantment layout is not a description provider. |
| [Enchantment Insights 26.2.3, P8CPaUO3](https://api.modrinth.com/v2/version/P8CPaUO3) | Client-only, maintained, but introduces Puzzles Lib, Forge Config API Port and bundled Tooltip Insights. Its larger UI/library scope is not a simpler replacement for one audited configuration library. Not installed or runtime-qualified. |
| [Item Tooltips 26.2-r1.1-fabric, E3Go08VW](https://api.modrinth.com/v2/version/E3Go08VW) | Adds Unified alongside existing Cloth Config/Fabric API and broader item/attribute/wrapping behavior. More overlap/configuration than the focused selected feature. Not installed or runtime-qualified. |
| [Enchant Description resource pack 0.3, Wo3GpQmN](https://api.modrinth.com/v2/version/Wo3GpQmN) | API lists 26.2, but its ZIP declares pack format 9, has only English, and replaces global enchantment names/level text. It lacks separate shift-gated description lines and requires resource-pack activation/order management. Not selected or runtime-qualified. |

No alternative is added. The 26.3 discovery entry is pending a separate exact
feature/library audit; this 26.2 exception cannot authorize different artifacts.
The [owner checklist](acceptance-tests.md#enchantment-descriptions-acceptance)
remains entirely uncompleted.

## Screenshot experience evaluation, 2026-11-19

Decision: retain Renice Shot alone. Neither gallery is installed. This review
changes no feature count, pin, defaults template, pack version or player file.
The maintained baseline remains 41 features and eleven libraries, pack
26.2.0.9.0. Both candidates remain outside the collection, index and export.

### Exact artifacts and source correspondence

| Project | Evaluated Fabric 26.2 artifact | Source and dependencies |
| --- | --- | --- |
| Renice Shot, `ZDCwiIc3` | Release `1.2.1+mc26.2`, version `roOTvshj`, retained | [Release tag](https://github.com/wechirok/renice-shot/tree/bca7c14881a592ca3df2d309968cb29bdaa32728). Required Fabric API and optional Mod Menu/Cloth Config are already installed. No bundled libraries. |
| Screenshot Viewer, `laNoi025` | Release `26.2-fabric-1`, native version `1.3.6-fabric-mc26.2`, version `id6Yni9S` | [Release commit](https://github.com/LGatodu47/ScreenshotViewer/tree/82dd0b8be130f5832badeeac9a9df74b2c4fd91a), committed 16 seconds before publication with matching version/changelog. Bundles CatConfigMC `0.2.1`, which bundles CatConfig `0.3.0`. No external API dependencies declared by Modrinth/native metadata; implementation uses the already installed Fabric API. |
| Screenshot Overhaul, `wYSKV506` | Alpha `0.2.3-26.2`, version `H592Npj8` | [26.2 release-time commit](https://github.com/Azz-9/Screenshot-Overhaul/tree/c1676036589ceccd6942d4b5449002baf036753c), matching version/changelog, committed 23 minutes before publication. Required Fabric API is already installed. No bundled libraries. The generic `v0.2.3` tag targets 26.3; it is not the source used for this 26.2 review. |

The [version API](https://api.modrinth.com/v2/version/id6Yni9S) and
[Overhaul version API](https://api.modrinth.com/v2/version/H592Npj8) identify the
exact files. `candidates.toml` records their URLs, SHA-512 hashes and immutable
source commits. Downloads matched these hashes. `javap -p -c -verbose` inspected
all 55 Viewer, 185 Overhaul and 17 Renice Shot top-level-JAR classes, including
private methods and constants. Published descriptors and the decision-relevant
methods/constants agree with the referenced sources. This is source/release
correspondence, not a reproducible upstream build or runtime proof. Current
Viewer master is unreleased 1.3.7 with additional options/fixes; those are not
attributed to the evaluated 1.3.6 artifact.

All three project labels are client required/server unsupported. All three
native root descriptors declare `environment = "client"`. Viewer has a client
entrypoint and client mixins; its bundled config libraries have no server
entrypoint/requirement. Overhaul's main entrypoint initializes client facilities.
No custom game packet protocol, remote sharing/upload client or mandatory
server companion was found in the reviewed implementation. Overhaul's Fabric
connection events refresh local state; they do not add a server protocol.
`net.minecraft.network.chat` references represent text, not a custom connection.
This audit covers these screenshot mods, not outbound behavior of unrelated
pack libraries such as the separately disclosed Prickle update check.

Isolated native graph checks passed for each candidate against all 52 existing
pins, including Java 25, Loader 0.20.1, Sodium 0.9.2 and Iris 1.11.4. Viewer also
passed the existing exact-feature check. Overhaul was rejected as an intentional
alpha selection. Its substantive privacy/deletion risks independently prevent
promotion; the alpha label alone did not decide the outcome. No policy or
metadata exception was added. Successful descriptor checks do not prove mixin
application, renderer compatibility or launcher behavior.

### Capabilities and limitations

V = verified supported by the exact source/artifact; C = supported with caveats;
N = not supported; U = unknown, requires runtime acceptance. V never means an
observed Minecraft result.

| Capability | Renice Shot | Screenshot Viewer | Screenshot Overhaul |
| --- | --- | --- | --- |
| Capture | V: normal F2 retained, separate F9 3840x2160 PNG; custom dimensions, optional HUD hiding/delay | N: no high-resolution capture of its own; modifies vanilla saved-message click behavior | V: normal capture, optional custom resolution/HUD/chat/hand hiding, previews and six-face panoramas; U: renderer restoration under failure |
| Files and naming | V: default `screenshots/huge_<time>.png`; custom `%time%` and `%world%`; PNG/JPG/TGA/BMP | C: existing lowercase `.png`, `.jpg`, `.jpeg`, including `huge_` names; not TGA/BMP | C: existing `.png` only, including `huge_`; custom token names/subdirectories and output root; no JPG/TGA/BMP capture selection found |
| Locations | V: instance screenshots directory | C: one configurable root, nonrecursive; release config UI expects absolute paths | C: recursive custom root and watch service; symlink traversal not guaranteed |
| Gallery and organization | N: use launcher/OS folder | V: title/pause buttons, enlargement/navigation, filename order forward/reverse, rename/open/copy; N: search, favorites or map integration | V: title/pause gallery, search, sort/filter/favorites and local `screenshot-states.json`; image metadata editing |
| Controls | V: F9 capture; Light Overlay seeded F7 | V: gallery shortcut initially unbound, menu buttons remain discoverable | C: F9 panorama collides with Renice Shot; no distinct bound gallery shortcut found |
| Large libraries | V: no library index/cache | C: eagerly creates a widget for every file; default `NONE` compression queues every full original decode when gallery opens and retains images until close | C: background recursive metadata scan/watchers; on-demand texture caches bounded by entry count, not image bytes |
| Images and thumbnails | C: capture limit depends on GPU/available memory | C: optional HALF/QUARTER/EIGHTH disk thumbnails; generation decodes full originals and queues the whole collection during initialization/config changes; no LRU or pixel budget | C: small/normal/full-view LRU limits 128/64/6, widths 128/512/1920; each load first decodes original; no disk thumbnail cache found |
| Arbitrary huge dimensions | U: hardware dependent | U: full native decode and GPU texture limits apply, not arbitrary-size support | U: downscaled presentation still needs original decode; full view is not a lossless 4K inspection tool |
| Deletion | N: no gallery delete operation | V: single/batch deletion confirmation enabled by default; disabling it changes safety | C: reviewed gallery and preview actions call deletion directly; no confirmation option found |
| Privacy | V: default time-only filename; no location metadata writer or automatic sharing found | V: no location metadata writer or automatic uploads found; explicit clipboard/open operations | C: capture unconditionally inserts location/server metadata into PNG; no capture-time opt-out found |
| Sodium/Iris | U: existing owner acceptance remains open | U: gallery plus capture/message/native-image mixins need runtime checks | C: built against Sodium 0.9.2 and Iris 1.11.4; local Iris shader-name lookup; U: actual capture/rendering compatibility |
| Prism and Modrinth App | C: ordinary client JAR/local instance paths; U: live launch/capture | C: ordinary client JAR, AWT and custom path behavior need acceptance | C: ordinary client JAR, AWT/path behavior need acceptance; existing symlink issue below |

Viewer's default full-image retention can be expensive even with background
loading. For scale only, 500 decoded 3840x2160 RGBA images require about 15.4 GiB
of pixel storage before other allocations. This is arithmetic, not a benchmark
or measured peak. Enabling EIGHTH thumbnails lowers retained preview size but
still queues the whole collection, decodes full images during generation, and
can fall back to original decoding while a thumbnail is pending. There is no
bounded visible-window image cache. It also globally redirects NativeImage's
PNG header validation and enables AWT on non-macOS systems. Neither can be
removed with an ordinary defaults template. Those costs are excessive for the
focused capture/gallery separation sought here, even though installation is
statically eligible. Revisit after bounded loading evidence or an upstream fix.

### Xaero integration and privacy

Overhaul places image thumbnails at stored X/Z coordinates and opens them from
the world map. It uses Xaero render interfaces plus mixins into
`MapElementRenderHandler.Builder.build`, `GuiMap` mouse/render methods and a
private `viewed` field accessor. Its Fabric plugin checks only whether
`xaeroworldmap` is installed. There is no declared version range protecting
these internal targets. No Minimap-specific integration was found.

The evaluated build compiles against World Map 1.46.1. Lantern Crossing pins
World Map 1.47.2 (`W8qSt5Gs`) and Minimap 26.6.2 (`kYWdcLLn`). Static inspection
of the hash-verified pinned map JAR found the named primary mixin targets and
field, but this does not prove all inherited interfaces, mixin application or
behavior. The integration is not qualified against our exact pins.

World matching uses a singleplayer save-folder ID or the literal multiplayer
server address, then filters dimension. It has no server-provided unique world
ID. It cannot reliably distinguish separate worlds behind one address or a
server reset, and different addresses can split one world. Old Renice Shot PNGs
can appear in the gallery but lack coordinates/world metadata and cannot acquire
accurate map positions retroactively.

[MetadataUtils](https://github.com/Azz-9/Screenshot-Overhaul/blob/c1676036589ceccd6942d4b5449002baf036753c/common/src/main/java/me/Azz_9/screenshot_overhaul/client/metadata/MetadataUtils.java)
collects X/Y/Z, dimension, biome, singleplayer seed/save identity/world name,
multiplayer server address, game version, resource-pack names, active shader and
timestamp. No player UUID/name or multiplayer seed fetch was found. The
[Screenshot mixin](https://github.com/Azz-9/Screenshot-Overhaul/blob/c1676036589ceccd6942d4b5449002baf036753c/common/src/main/java/me/Azz_9/screenshot_overhaul/mixin/ScreenshotMixin.java)
unconditionally writes these as PNG `tEXt` chunks. Sharing the original PNG
therefore shares the data even without any automatic upload. Hiding an image
from the map changes local state, not its embedded metadata. UI editing is not
a preventative default and metadata update strips all text chunks, including
unrelated existing text. No setting separates private local map association
from a shareable metadata-free original. Disabling the whole mod removes the
intended functionality. This fails the selected privacy requirement.

### Release maturity and architecture decision

Viewer's Fabric 26.2 release dates to June 26. Its July development fixes are
unreleased; requests for 26.3 remain open. [Issue 74](https://github.com/LGatodu47/ScreenshotViewer/issues/74)
requests subfolder support. [Issue 75](https://github.com/LGatodu47/ScreenshotViewer/issues/75)
reports custom click-event serialization with Chat Patches, which this pack does
not install. Do not generalize that report into a reproduced pack conflict.

Overhaul has five Fabric 26.2 alpha releases from July through October, most
recently October 20. Its optional photo-mode work remains experimental. No
runtime result or stable-API commitment was found. [Issue 2](https://github.com/Azz-9/Screenshot-Overhaul/issues/2)
reports an empty gallery with a symlinked screenshot root on Linux/Prism/26.3.
The reviewed 26.2 code also walks paths without following links; the 26.2 effect
is a source-based risk, not a reproduced bug. An open issue is not evidence that
it has been fixed. No upstream contact was made.

Weights remain the requested 25/15/20/15/10/10/5 percent. Scores below use 1 to 5
as engineering judgments about reviewed evidence, not runtime measurements.
A hard privacy/stability requirement cannot be traded for a higher total.

| Architecture | Stability 25 | Capture 15 | Gallery 20 | Exploration 15 | Privacy 10 | Memory 10 | Maintenance 5 | Weighted / 5 | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A: Renice Shot + Viewer | 3 | 5 | 3 | 1 | 5 | 1 | 3 | 3.00 | Defer: useful local gallery, but unbounded loading and broad image/AWT hooks are not justified for large high-resolution collections. |
| B: Renice Shot + Overhaul | 1 | 3 | 4 | 3 | 1 | 3 | 1 | 2.40 | Reject this combination: two F9 actions and overlapping capture/filename wrappers; metadata/deletion blockers persist. |
| C: Overhaul alone | 2 | 3 | 4 | 3 | 1 | 3 | 2 | 2.70 | Defer: useful gallery/map features, but privacy/deletion and maturity requirements unmet; loses Renice's separate F9 workflow, extra output formats and proven-in-source queue/error-restoration paths. |
| Retained: Renice Shot alone | 4 | 5 | 1 | 1 | 5 | 5 | 5 | 3.35 | Selected: established capture architecture; gallery, favorites, map pins and panoramas remain absent. Runtime qualification is still pending. |

A is the simpler future gallery direction if its memory behavior improves.
B does not become safe merely by rebinding panorama: both wrap
`Screenshot.grab` and `takeScreenshot` and control filenames. Renice Shot's
ordinary F9 task writes through its own framebuffer writer, so a directory
watcher can discover it but Overhaul's vanilla-save metadata hook cannot be
assumed to annotate it. No combined mixin test was performed and no crash is
claimed. C's custom-resolution path lacks the same explicit queued
capture/failure-restoration structure and does not establish a safer replacement.

No screenshot manager configuration, live preferences, screenshot folder,
metadata database or user image is packaged. Existing Configured Defaults
behavior remains unchanged. There is no gallery migration or user cleanup.
The 26.3 bootstrap receives shared documentation safeguards and candidate
findings only; its 30 installed features and 41 future identities stay unchanged.
Neither candidate is promoted there or claimed compatible with 26.3.
