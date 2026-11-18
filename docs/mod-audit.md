# Client-only mod audit

Evidence checked on 2026-11-17 against the [Modrinth API](https://docs.modrinth.com/api/) and the exact downloaded Fabric artifacts. [The offline snapshot](upstream-metadata.json) records project/version identity, compatibility declarations, files, dependency edges, and recursive Fabric descriptors. Download hashes were checked during the audit and again by packwiz export.

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

## Dependency audit

Fabric API is an explicitly selected platform library. Eight projects are transitive libraries. All nine have exact Fabric 26.2 pins and `side = "client"`. The selected platform library is release-designated. Upstream dependency provenance permits the audited Placeholder API beta-versioned artifact. Their local APIs and configuration functions do not require any remote-server installation. They add no selected gameplay content. Exact parents appear in `collection.toml`; exact versions and hashes remain authoritative in `mods/*.pw.toml`.

| Library | Classification | Client purpose and dependency evidence |
| --- | --- | --- |
| [Fabric API](https://modrinth.com/mod/fabric-api) | selected-library | Required by Xaero's Minimap, YetAnotherConfigLib (YACL), Shulker Box Tooltip, Light Overlay, BetterF3, TCDCommons API, Dynamic FPS, OverlayLib, Balm, Entity Culling, Xaero's World Map, Inventory Profiles Next, Debugify, Mouse Tweaks, Sign Tweaks, Mod Menu, Better Statistics Screen, libIPN, Paginated Advancements & Custom Frames, Book Tweaks, Language Reload, Client Tweaks, Zoomify (Zoom), FastQuit, LambDynamicLights - Dynamic Lights. |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/mod/yacl) | dependency | Required by Light Overlay, Zoomify (Zoom). |
| [Cloth Config API](https://modrinth.com/mod/cloth-config) | dependency | Required by More Culling, BetterF3, Sign Tweaks, Paginated Advancements & Custom Frames, Status Effect Bars, FastQuit. |
| [TCDCommons API](https://modrinth.com/mod/tcdcommons) | dependency | Required by Better Statistics Screen. |
| [Fabric Language Kotlin](https://modrinth.com/mod/fabric-language-kotlin) | dependency | Required by Inventory Profiles Next, libIPN, Zoomify (Zoom). |
| [libIPN](https://modrinth.com/mod/libipn) | dependency | Required by Inventory Profiles Next. |
| [Balm](https://modrinth.com/mod/balm) | dependency | Required by Client Tweaks. |
| [Text Placeholder API](https://modrinth.com/mod/placeholder-api) | dependency | Required by Mod Menu. |
| [OverlayLib](https://modrinth.com/mod/overlaylib) | dependency | Required by Light Overlay. |

Fabric API supplies modules required by Debugify, Book Tweaks, Paginated Advancements, and other artifacts even where their Modrinth records omit that dependency. Sodium bundles the Fabric modules it requires. Cloth Config provides both `cloth-config` and `cloth-config2`. The client closure records these artifact-derived edges as well as upstream required-project edges.

Bundled libraries stay inside their upstream artifacts. They are not separately selected features or duplicate packwiz downloads. The snapshot includes recursive module descriptors for Fabric API, Kotlin, YACL, LambDynamicLights, and the other active artifacts. Both Xaero artifacts bundle XaeroLib 1.8.5. Fabric Loader resolves the duplicate module.

Zoomify version `D64cvU6G` is universal. Its Modrinth record lists KotlinLangForge `1vrSzlao` as required, although that is a NeoForge dependency and has no Fabric build. The Fabric descriptor requires YACL and Fabric Loader. Fabric Language Kotlin is already in the closure for IPN. This is the sole recorded loader-specific metadata exception, in `upstream-metadata.json`. The checker still requires the remaining Modrinth dependencies.

## Upstream release and dependency provenance

All 30 active features use upstream release-designated Fabric 26.2 versions.
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
identifiers, not its Modrinth project slug. All 30 requested features are active,
with zero blocked features.

## Intentional rejections

AppleSkin, Jade, Easy Shulker Boxes, Bookshelf Inspector, and Client Sort are rejected regardless of target availability. AppleSkin and the rejected inspector/container tools do not meet the selected strict server-independence policy. Jade is deliberately excluded. IPN owns sorting, so Client Sort is not selected. The source checker rejects their IDs or slugs, and an undeclared lock also fails the active-set check.

No substitute, shader pack, resource pack, gameplay content, or server companion has been added. See [configuration decisions](configuration.md) and [runtime acceptance](acceptance-tests.md).
