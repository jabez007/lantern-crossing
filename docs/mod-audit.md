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

## QoL and performance refinement, 2026-11-19

Only the maintained 26.2 branch installs the following three additions. The 26.3
bootstrap receives migration intent and this evaluation, not these artifacts.
The maintained baseline is 40 features and ten libraries. All 46 preceding
artifact locks and their upstream project records remain unchanged. No Minecraft,
Prism or Modrinth App runtime acceptance was performed.

| Candidate | Audited Fabric 26.2 release | Disposition | Evidence and scope |
| --- | --- | --- | --- |
| [BetterGrassify](https://modrinth.com/mod/bettergrassify), `m5T5xmUy` | [1.8.7+fabric.26.2, r4yqxYQl](https://api.modrinth.com/v2/version/r4yqxYQl) | Added on 26.2 | Client-only artifact. Local block-model/quad rendering needs no server installation or extra data. Requires existing Fabric API. Fancy grass, resource-pack compatibility mode, paths/farmland/Nether changes disabled, and extra snow layers disabled are initial defaults. |
| [Controlling](https://modrinth.com/mod/controlling), `xv94TkTM` | [26.2.4, sZHXONgm](https://api.modrinth.com/v2/version/sZHXONgm) | Added on 26.2 | Client-only keybinding screen search, free-key view and conflict filtering. Requires Fabric API and Searchables. Does not assign bindings or resolve conflicts automatically; F7 is unchanged. |
| [Enchantment Descriptions](https://modrinth.com/mod/enchantment-descriptions), `UVtY3ZAC` | [26.2.0.2, PTAK0HD2](https://api.modrinth.com/v2/version/PTAK0HD2) | Deferred due to compatibility | Client tooltip callback and vanilla translations are local. Required Prickle `aaRl8GiW`, release [26.2.0.3, XdvtdRYJ](https://api.modrinth.com/v2/version/XdvtdRYJ), declares server required in the [project API](https://api.modrinth.com/v2/project/aaRl8GiW). Its universal descriptor and local config implementation contradict that label. No exception to the server-required rejection is added. |
| [Crash Assistant](https://modrinth.com/mod/crash-assistant), `ix1qq8Ux` | [1.11.14, alR3tamq](https://api.modrinth.com/v2/version/alR3tamq) | Deferred due to compatibility | API is client-only; native universal language adapter starts a local child process early enough to diagnose many initialization failures. No required Modrinth projects; embedded application/libraries still need auditing. Launcher logs already provide the basic reporting path. Early privacy-default ordering with Configured Defaults is unresolved. |
| [Better Block Entities](https://modrinth.com/mod/better-block-entities), `ONZm0H7Y` | [1.3.9+mc26.2, n5mL5flA](https://api.modrinth.com/v2/version/n5mL5flA) | Deferred due to compatibility | Client-only; native Sodium `>=0.9.0`, release changelog supports 0.9.0 through 0.9.2, including our 0.9.2. Open Iris lighting report [#145](https://github.com/EdeenMC/betterblockentities/issues/145), Iris/Xaero shader-toggle map report [#156](https://github.com/EdeenMC/betterblockentities/issues/156), and acknowledged transition-lighting limitation [#7](https://github.com/EdeenMC/betterblockentities/issues/7) prevent promotion without resolving applicability to this stack. |
| [Ixeris](https://modrinth.com/mod/ixeris), `p8RJPJIC` | [4.6.11+26.2-fabric, qXHd9Vb4](https://api.modrinth.com/v2/version/qXHd9Vb4) | Staged pending benchmarking | Client event polling and Windows buffered raw input. The [upstream benchmarks](https://github.com/decce6/Ixeris/tree/124f06bd5a9530d9af9529d5af885275b8be77b1#benchmarks) are real workload-specific reports, not Lantern Crossing measurements. No required project dependency. |
| [ModernFix-mVUS](https://modrinth.com/mod/modernfix-mvus), `TjSm1wrD` | [5.27.19-build.2, 50uUra83](https://api.modrinth.com/v2/version/50uUra83) | Staged pending benchmarking | Independent local startup/model/memory fixes are eligible in principle; server fixes confer no remote benefit. Required Fabric API is present; native Minecraft `~26.2-` and Loader `>=0.16.10` fit. Broad patch interactions and benefit remain unqualified. |
| [Tooltip Tweaks](https://modrinth.com/mod/tooltiptweaks), `evJ7VC0w` | [3.0.1, mo7PzvJD](https://api.modrinth.com/v2/version/mo7PzvJD) | Deferred due to compatibility | Reads client FOOD/CONSUMABLE components, not authoritative current saturation/exhaustion. Fabric API `>=0.154.1` and YACL `>=3.9.5` are satisfied. Source has inconsistent cake saturation and truncated fractional icons; broad container/map/enchantment/effect rewrites also overlap dedicated tools. No 26.3 Fabric release found. |
| [Food Effect Tooltips](https://modrinth.com/mod/foodeffecttooltips), `GGfyJWnG` | [2.1.2+26.2, aXyL1zFA](https://api.modrinth.com/v2/version/aXyL1zFA) | Added on 26.2 | Client-only callback reads vanilla CONSUMABLE and DEATH_PROTECTION components, including effect duration, amplifier and probability. No player saturation/exhaustion estimate or extra server data. Suspicious-stew reveal stays off. No duplicate Tooltip Tweaks installation. |

### Source and dependency evidence

The hash-verified new artifact descriptors are in [the maintained-line upstream snapshot](https://github.com/jabez007/lantern-crossing/blob/59373ad/docs/upstream-metadata.json).
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
- Enchantment Descriptions [df15f5b](https://github.com/Darkhax-Minecraft/Enchantment-Descriptions/tree/df15f5bc42a0d0b74356fec64dcfa4162701d149) loads Prickle config and resolves description translation keys. Prickle [19934df](https://github.com/Darkhax-Minecraft/PrickleMC/tree/19934df33b5f874d5849f272a663f0db97c4c099) uses local JSON file services; no required remote handshake was found. That evidence does not reconcile the API environment contradiction. Vanilla translations are supplied, but plugin-defined enchantments need matching local descriptions; arbitrary plugin behavior cannot be inferred.
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
