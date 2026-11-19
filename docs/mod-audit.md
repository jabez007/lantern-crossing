# Client-only mod and shader audit

## Minecraft 26.3 migration review, 2026-11-19

The primary baseline is Minecraft 26.3, Fabric Loader 0.20.1, Java 25 and pack
26.3.0.1.0. All 41 feature mods, eleven libraries and both shader choices from
26.2.0.10.0 are accounted for. No replacement, exclusion or unrelated feature
was introduced. Every Packwiz record is pinned client-side. Static validation
checks exact Modrinth identity, release designation, hashes, target/loaders,
required closure, Fabric version predicates and incompatible declarations.
All Minecraft and launcher runtime acceptance remains **pending**.

[Official Minecraft 26.3 changes](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3)
and [Fabric's migration notes](https://fabricmc.net/2026/09/15/263.html) document
SDL3 physical-position keys, changed mouse constants and text-focus handling,
new transparency/core-shader compilation paths and Wayland behavior. Upstream
release support does not prove correct operation of this combined stack.

## 26.3 artifact migration matrix

Each target link is the exact Modrinth release used. Stable project IDs and full
source/target version IDs, role, dependency edges and independent runtime states
are in [migration.toml](../migration.toml). Raw release metadata and native
root/bundled descriptors are in [upstream-metadata.json](upstream-metadata.json).
All rows are statically verified; none is runtime accepted. Libraries are not
feature selections; bundled implementation libraries are not extra downloads.

| Project / role | 26.2 artifact | 26.3 artifact | Dependency/client scope and migration risks |
| --- | --- | --- | --- |
| Sodium (`AANobbMI`, feature) | mc26.2-0.9.2-fabric | [mc26.3-0.9.2-fabric](https://api.modrinth.com/v2/version/bAZQdGpg) | Local renderer; 0.9.2 port restores Linux fullscreen resolution control. Review new transparency, particles and falling blocks. |
| Lithium (`gvQqBUqZ`, feature) | mc26.2-0.25.3-fabric | [mc26.3-0.26.4-fabric](https://api.modrinth.com/v2/version/Lal8mJGR) | Independent local/integrated-server optimization; no remote TPS claim. MixinExtras >=0.5.5 supplied by Loader. |
| FerriteCore (`uXXizFIs`, feature) | 9.0.0-fabric | [9.0.0-fabric](https://api.modrinth.com/v2/version/d5ddUdiB) | Same multi-version artifact; native range >=26.1 <27. Independent client memory optimization. |
| ImmediatelyFast (`5ZwdcRci`, feature) | 1.16.5+26.2-fabric | [1.17.1+26.3-fabric](https://api.modrinth.com/v2/version/3MP9UR23) | Client rendering batches; 26.3 port. Shader and UI layering remain runtime checks. |
| Entity Culling (`NNAgCjsB`, feature) | 1.12.1 | [1.12.1](https://api.modrinth.com/v2/version/UWpkLRV5) | Client occlusion; new custom culling API. Inspect missing geometry and translucent entities. |
| More Culling (`51shyZVL`, feature) | 1.8.2 | [1.9.1](https://api.modrinth.com/v2/version/5jIORlSK) | Client face culling; 1.9.1 fixes fence-top rendering with candles. Check foliage and shader stack. |
| BadOptimizations (`g96Z4WVZ`, feature) | 2.4.1 | [2.4.1](https://api.modrinth.com/v2/version/Sp0ctspw) | Client-only 26.3 port; no extra optimizer selected. |
| Dynamic FPS (`LQ3K71Q1`, feature) | 3.11.9 | [3.11.10](https://api.modrinth.com/v2/version/Jwq069rR) | Same multi-version artifact, >=26.2.0-. SDL3 focus/minimize and Wayland need acceptance. |
| FastQuit (`x1hIzbuY`, feature) | 3.1.5+mc26.2 | [3.1.5+mc26.2](https://api.modrinth.com/v2/version/ZZ5dfboC) | Same artifact lists 26.3 and native >=26.2; local save behavior. Let background saves finish. |
| Debugify (`QwxR6Gcd`, feature) | 26.2.0.1 | [26.3.0.0](https://api.modrinth.com/v2/version/FMaS2nZn) | 26.3 removes fixes now implemented by Mojang. Selected client fixes need no remote companion. |
| Language Reload (`uLbm7CG6`, feature) | 1.7.8+26.2 | [1.7.8+26.3](https://api.modrinth.com/v2/version/QVn4cccd) | Client language/resource reload and text input; 26.3 Fabric key-mapping API. |
| Inventory Profiles Next (`O7RBXm3n`, feature) | fabric-26.2-2.3.8 | [fabric-26.3-2.3.8](https://api.modrinth.com/v2/version/y8vT21Sb) | Client sorting/refill via vanilla interactions; libIPN 6.9 required. Review new bundle/shulker swap-click options. |
| Mouse Tweaks (`aC3cM3Vq`, feature) | 26.2-2.31-fabric | [26.3-2.31-fabric](https://api.modrinth.com/v2/version/LeMuMhLv) | 26.3 client port; wheel/empty-cursor overlap switches unchanged. SDL3 gestures require acceptance. |
| Shulker Box Tooltip (`2M01OLQq`, feature) | 5.4.3+26.2-fabric | [5.4.3+26.3-fabric](https://api.modrinth.com/v2/version/60krd8u8) | Client-visible item contents only. Ender-chest server integration is outside selection; no remote preview claim. |
| Status Effect Bars (`x02cBj9Y`, feature) | 1.0.12 | [1.0.12](https://api.modrinth.com/v2/version/aAXJqboy) | Same client artifact lists 26.3; vanilla effect durations only. |
| BetterF3 (`8shC1gFX`, feature) | 19.0.1 | [20.0.0](https://api.modrinth.com/v2/version/XB7u4eSf) | 26.3 debug UI scale and shader-line fixes. Local diagnostic information. |
| Better Mount HUD (`kqJFAPU9`, feature) | 1.3.1 | [1.3.1](https://api.modrinth.com/v2/version/M3Fe5t0L) | Same multi-version client HUD artifact; no server counterpart. |
| Paginated Advancements & Custom Frames (`pJogNFap`, feature) | 2.8.0+26.2 | [2.9.0+26.3](https://api.modrinth.com/v2/version/coMs94me) | 26.3 client layout/pagination; vanilla advancements only, no new content. |
| Better Statistics Screen (`n6PXGAoM`, feature) | 5.5.6+fn-26.2 | [5.8.0+fn-26.3](https://api.modrinth.com/v2/version/GSF3fkG9) | Local statistics UI over vanilla statistics; exact TCDCommons GVSkIJY4. Server sharing/commands not selected. |
| Xaero's Minimap (`1bokaNcj`, feature) | fabric-26.2-26.6.2 | [fabric-26.3-26.6.2](https://api.modrinth.com/v2/version/MfxfgXaO) | Client mapping and local waypoints. Bundles XaeroLib 1.8.5; world map >=1.47.1; no server identification/teleport claim. |
| Xaero's World Map (`NcUtCpym`, feature) | fabric-26.2-1.47.2 | [fabric-26.3-1.47.2](https://api.modrinth.com/v2/version/VM8lNSSM) | Client explored terrain/manual map selection. Same bundled XaeroLib 1.8.5; minimap >=26.6.1; check world/dimension associations. |
| Zoomify (Zoom) (`w7ThoJFB`, feature) | 2.17.0+mc26.2 | [2.17.0+mc26.3](https://api.modrinth.com/v2/version/RUBpNu00) | Local camera zoom. Universal NeoForge Kotlin dependency still excluded by exact version audit; Fabric uses Kotlin. |
| Book Tweaks (`skd7t7zC`, feature) | 1.2.0 | [1.2.0-26.3](https://api.modrinth.com/v2/version/b2TIM6ZY) | 26.3 client editor; vanilla book packets only. SDL3 text focus/paste needs acceptance. |
| LambDynamicLights - Dynamic Lights (`yBW8D80W`, feature) | 4.12.4+26.2 | [4.13.0+26.3](https://api.modrinth.com/v2/version/rylKnJ4M) | 26.3 client lighting with bundled SpruceUI/Yumi. No server block-light/spawn changes. Compare doubled lighting with shaders. |
| Chat Heads (`Wb5oqrBJ`, feature) | 1.3.2 | [1.3.2](https://api.modrinth.com/v2/version/i3gcElvQ) | Client chat sprites; 1.3.1 stops recording heads as textual chat logs. No remote installation. |
| Fabric API (`P7dR8mSH`, selected-library) | 0.161.0+26.2 | [0.166.2+26.3](https://api.modrinth.com/v2/version/Zns5SSRA) | Explicit platform library installed on client; native Minecraft ~26.3-, Java >=25, Loader >=0.19.3. |
| Client Tweaks (`vPNqo58Q`, feature) | 26.2.0.6+fabric-26.2 | [26.3.0.1+fabric-26.3](https://api.modrinth.com/v2/version/7fKN7OpP) | Client entrypoint, no common initializer; local input/UI conveniences. Balm/Kuma bundled support; overlap switches retained. |
| Sign Tweaks (`c7xDMxha`, feature) | 2.103.0+26.2 | [2.104.0+26.3](https://api.modrinth.com/v2/version/bqVjibae) | Modrinth environment unknown; actual artifact environment client, empty main/server entrypoints. Local vanilla sign editor. |
| Iris Shaders (`YL57xq9U`, feature) | 1.11.4+26.2-fabric | [1.11.7+26.3-fabric](https://api.modrinth.com/v2/version/vTN4NRGW) | Client-only 1.11.7 fixes 26.3 bugs; exact Sodium bAZQdGpg required, native 0.9.x. Both shader audits renewed. |
| Mod Menu (`mOgUt4GM`, feature) | 20.0.3 | [21.0.1](https://api.modrinth.com/v2/version/xckkBHD5) | Client mod/config UI. Placeholder API is now release 3.2.0, so no prerelease dependency exemption needed. |
| Light Overlay (`8qVa1XCN`, feature) | 2.12.0+26.2 | [2.13.1+26.3](https://api.modrinth.com/v2/version/MBWYrOAD) | Correct project 8qVa1XCN; local light/spawn visualization. Exact OverlayLib iSTcauwL; YACL >=3.9.7. |
| Renice Shot (`ZDCwiIc3`, feature) | 1.2.1+mc26.2 | [1.2.1+mc26.3](https://api.modrinth.com/v2/version/cqRSJ7PC) | 26.3 capture artifact; symbolic F9 still 3840x2160 PNG. No gallery, automatic upload or filename change configured. |
| Sodium Extra (`PtjYWJkn`, feature) | mc26.2-0.9.5+fabric | [mc26.3-0.9.5+fabric](https://api.modrinth.com/v2/version/fs5l9Q1U) | Native requires Loader >=0.20.1 and exact Sodium 0.9.2+mc26.3. Client graphics controls, no additional HUD enabled. |
| Reese's Sodium Options (`Bh37bMuy`, feature) | mc26.2-2.2.4+fabric | [mc26.3-2.2.5+fabric](https://api.modrinth.com/v2/version/EfchygKx) | Client settings UI; exact Sodium 0.9.2+mc26.3. Do not upgrade renderer independently. |
| Continuity (`1IjD5062`, feature) | 3.0.1+26.2 | [3.0.1+26.3](https://api.modrinth.com/v2/version/Jt2sCWTQ) | 26.3 local connected textures; both built-in resource IDs still present. Existing resource-pack order wins. |
| Cubes Without Borders (`ETlrkaYF`, feature) | 5.0.0+26.2 | [5.0.0+26.3](https://api.modrinth.com/v2/version/26KCwNI9) | 26.3 SDL3 port; new Windowed/fullscreen choices. Upstream recommends reviewing old borderless-type customization. |
| More Chat History (`8qkXwOnk`, feature) | 2.0.0 | [2.0.0](https://api.modrinth.com/v2/version/qpDhYv1Y) | Same multi-version client artifact; local message history only. |
| Configured Defaults (`SISoSFPP`, feature) | 26.2.0 | [26.3.0](https://api.modrinth.com/v2/version/frAVVzBj) | 26.3 early file handler; missing files/options only. New README resource checked; no companion or extra library. |
| BetterGrassify (`m5T5xmUy`, feature) | 1.8.7+fabric.26.2 | [1.8.8+fabric.26.3](https://api.modrinth.com/v2/version/8qcmuwZa) | 26.3 local terrain port; config fields retained. Fancy grass, snow off; check culling/CTM/shaders. |
| Controlling (`xv94TkTM`, feature) | 26.2.4 | [26.3.4](https://api.modrinth.com/v2/version/V6AbRm67) | 26.3 controls search/conflicts with Searchables >=1.0.2; no server behavior. |
| Food Effect Tooltips [Fabric / NeoForge] (`GGfyJWnG`, feature) | 2.1.2+26.2 | [2.1.2+26.3](https://api.modrinth.com/v2/version/kbNgzPtF) | 26.3 client item-consumption data. Native-only Fabric/Cloth edges retained; no current saturation/exhaustion claim. |
| Enchantment Descriptions (`UVtY3ZAC`, feature) | 26.2.0.2 | [26.3.0.2](https://api.modrinth.com/v2/version/uZf2qbql) | 26.3 client tooltip mixins/local language resources. Renewed exact Prickle review; Shift gate retained, plugin descriptions not promised. |
| YetAnotherConfigLib (YACL) (`1eAoo2KR`, dependency) | 3.9.7+26.2-fabric | [3.9.7+26.3-fabric](https://api.modrinth.com/v2/version/s9SjoFu1) | Client configuration UI, required by Zoomify/Light Overlay; exact 3.9.7 target release. |
| Cloth Config API (`9s6osm5g`, dependency) | 26.2.155+fabric | [26.3.159+fabric](https://api.modrinth.com/v2/version/fg2uyxOW) | Client config UI; dependency aliases checked; optional server capability does not require remote installation. |
| TCDCommons API (`Eldc1g37`, dependency) | 5.5.6+fn-26.2 | [5.8.0+fn-26.3](https://api.modrinth.com/v2/version/GVSkIJY4) | UI/platform dependency; vanilla statistics UI needs no server services. Exact Better Statistics dependency. |
| Fabric Language Kotlin (`Ha28R6CL`, dependency) | 1.14.2+kotlin.2.4.21 | [1.14.2+kotlin.2.4.21](https://api.modrinth.com/v2/version/SKW1BTL3) | Fabric runtime library, client installation only. Release Kotlin 2.4.21; no server companion. |
| libIPN (`onSQdWhM`, dependency) | fabric-26.2-6.9.0 | [fabric-26.3-6.9.0](https://api.modrinth.com/v2/version/aKBFonyQ) | Client IPN library; >=6.9.0 <6.10 enforced by IPN, Kotlin >=1.13.10. |
| Balm (`MBAkmtvl`, dependency) | 26.2.0.9+fabric-26.2 | [26.3.0.3+fabric-26.3](https://api.modrinth.com/v2/version/MYj31XNG) | Client Tweaks config and input platform; capable of server use but no server install needed for selected client features. |
| Text Placeholder API (`eXts2L7r`, dependency) | 3.1.0-beta.1+26.2 | [3.2.0+26.3](https://api.modrinth.com/v2/version/lXytLqWj) | Release 3.2.0+26.3; local UI text library required by Mod Menu. |
| OverlayLib (`M1B8mLoH`, dependency) | 0.12.0+26.2 | [0.12.1+26.3](https://api.modrinth.com/v2/version/iSTcauwL) | Exact Light Overlay dependency 0.12.1+26.3; local renderer; native Fabric API >=0.160.5. |
| Searchables (`fuuu3xnx`, dependency) | 1.0.1 | [1.0.3](https://api.modrinth.com/v2/version/wV79bLRS) | Client search library for Controlling, native >=1.0.2 satisfied by 1.0.3. |
| Prickle (`aaRl8GiW`, dependency) | 26.2.0.3 | [26.3.0.2](https://api.modrinth.com/v2/version/aPdekuq6) | Exact 26.3 exception renewed below; local configuration, no companion protocol. HTTP update HEAD remains disclosed. |
| Complementary Shaders - Reimagined (`HVnmMxH1`, shader) | r5.10 | [r5.10](https://api.modrinth.com/v2/version/RKfUB9VC) | Same release ZIP explicitly lists 26.3/Iris. Optional features recognized in Iris 1.11.7; GLSL/GPU tests pending. |
| MakeUp - Ultra Fast (`izsIPI7a`, shader) | 9.6 | [9.6](https://api.modrinth.com/v2/version/t4YRxQug) | Same release ZIP explicitly lists 26.3/Iris; upstream minimum Iris 1.5.1 met. No performance benchmark claim. |

## Runtime foundation and closure

The [Fabric 26.3 loader endpoint](https://meta.fabricmc.net/v2/versions/loader/26.3)
currently returns stable 0.20.1. Mojang's [exact version manifest](https://piston-meta.mojang.com/v1/packages/ead839cbccf0ddf013c3f935f2840080b5cb0d26/26.3.json)
requires Java 25. Its SHA-1-verified client archive reports options data version 5023.
Fabric API is 0.166.2+26.3, Zns5SSRA. No server counterpart is selected.

Lithium's new native MixinExtras >=0.5.5 requirement is fulfilled by the library
inside the [exact Loader JAR](https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.20.1/fabric-loader-0.20.1.jar).
The audit records that JAR's SHA-512 and full root/nested descriptors. Native
validation now includes this real runtime provider, its alias, dependencies and
version. It does not install an independent extra MixinExtras artifact.
Xaero's two JARs both bundle XaeroLib 1.8.5; duplicate copies remain in upstream
JARs and the checker resolves their equal versions. No additional project is needed.

The 11 library projects are the same identities as on 26.2; their pins and reverse
parents are rebuilt from the new release graph and native Fabric requirements.
Text Placeholder API 3.2.0 is release-designated. Bundled prerelease-looking
implementation components remain bound to their containing release hash. The
existing general stability policy is unchanged. Zoomify's universal declaration
still includes NeoForge-only KotlinLangForge; its Fabric descriptor does not.
The exact RUBpNu00 dependency exception replaces the old D64cvU6G review.

## Prickle environment classification review

Modrinth still labels Prickle client required/server required. That label alone
would reject the new artifact. We repeated the implementation review for
**Prickle 26.3.0.2 / aPdekuq6** and its sole selected parent **Enchantment
Descriptions 26.3.0.2 / uZf2qbql**. The old 26.2 exception is not reused.

[Prickle source commit 24365236](https://github.com/Darkhax-Minecraft/PrickleMC/tree/24365236ad06e42d4ecf1e9043607948e998e11d)
corresponds to all 36 Java files in the published sources JAR. Its published
Maven binary is byte-identical to the Modrinth JAR. The exact Fabric descriptor
has environment `*`, a common initializer and a client initializer, empty
common/client/server mixin lists, no bundles and only Fabric API/runtime
requirements. The common path initializes local JSON config. There are no
Minecraft packet/payload registrations, server lifecycle hooks or companion
requirements. Server-capable configuration does not require a remote installation.

The initializer still makes an asynchronous HTTP HEAD request to
`updates.blamejared.com/get` with mod/game/loader identifiers. It is a daemon
update check, catches failures, and does not gate local functionality. It is
external traffic, not a vanilla-server handshake; no opt-out was found in this
release. No logs, screenshot uploads or automatic sharing are selected. This
existing limitation remains disclosed rather than hidden by the exception.

[Enchantment Descriptions source commit 9548950f](https://github.com/Darkhax-Minecraft/Enchantment-Descriptions/tree/9548950f455e134ee31ad239bc2fbfe1a341d580)
corresponds to all 7 published Java sources; its Maven binary also matches the
Modrinth artifact. Its Fabric environment is client, tooltip mixins are client
only, and vanilla description text comes from local language resources and
client-visible item enchantments. Prickle is used for local property config.
No custom Minecraft networking or server-provided description data is required.
Custom/plugin enchantment descriptions are not promised.

The renewed exception is only an environment-classification correction. It
binds project/version, filename/SHA-512, complete descriptor digest, Minecraft
26.3 and the exact ED parent artifact/required edge. Any changed pin or parent
requires renewed review. Dependency predicates, server-only Fabric module
rejection, artifact integrity and export side remain enforced. The validator
prints the exception. Unrelated server-required artifacts still fail. No issue
or maintainer message has been submitted.

## Shader migration and distribution

Both official ZIPs remain byte-identical to the audited 26.2 selection:
Complementary Reimagined r5.10 / RKfUB9VC and MakeUp - Ultra Fast 9.6 / t4YRxQug.
Current release metadata lists Minecraft 26.3 and Iris for both. No shader-code
change or reupload is made. Their distribution audits now bind the exact Iris
1.11.7 / vTN4NRGW filename and hash; old renderer approval cannot authorize it.
Iris's native Sodium requirement and exact Modrinth Sodium edge are satisfied.
Complementary's optional Iris feature names are present in the new Iris binary;
MakeUp's documented Iris minimum 1.5.1 is met. These are compatibility inputs,
not proof of GLSL compilation, GPU support, correct transparency or frame times.

Complementary is by **EminGT / Complementary Development**, under
[Complementary License Agreement 1.8](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/e10d27dec5acfb18509fdcc3cda704152dc2f7df/License.txt).
Its section 1.2 permits unmodified modpack inclusion using Modrinth/CurseForge
systems, without direct file uploads. The original license stays inside the
upstream ZIP. No shader is enabled by default; visible credit is supplied anyway.
Lantern Crossing accepts responsibility for integration problems. Do not modify
shader code or remove notices under this grant.

MakeUp is by **Javier Garduño / javiergcim**, designated LGPL-3.0-or-later with
its [included license/source](https://github.com/javiergcim/MakeUpUltraFast/tree/fed6d05f841389fb5981f078e2fcac8dfb9c0080)
and original notices. We reference the complete unmodified official release.
Attribution and official links remain in README. Neither shader is relicensed
under repository MIT. Exact license files/digests and immutable source commits
remain in the machine audit; artifact hashes did not change in this migration.

Complementary remains the atmospheric choice; MakeUp is the configurable
alternative with shadowless/low profiles. No unmeasured speed guarantee. Iris
starts disabled only when there is no saved/synced config. No selection, preset
or user screenshot is overwritten. Review dynamic-light overlap, transparent
surfaces, CTM/grass/culling, maps, dimensions and screenshots in both launchers.
The [owner checklist](acceptance-tests.md#263-migration-acceptance) is uncompleted.

[MakeUp issue #208](https://github.com/javiergcim/MakeUpUltraFast/issues/208)
remains open and reports depth-of-field focus-edge artifacts on Apple Silicon
with this exact Minecraft 26.3 / Loader 0.20.1 / Iris 1.11.7 / Sodium 0.9.2 /
MakeUp 9.6 combination. This is an upstream report, not our reproduced result.
DoF is off in the original release defaults. Leave it off if affected and record
any deliberate DoF test separately. Do not patch or reupload the shader ZIP as
an incidental workaround. This does not block the no-shader or default-profile
acceptance route, but it is a concrete opt-in rendering limitation.

## Historical 26.2 selection investigations

The following material records the original version-specific feature selection,
candidate deferrals, source evidence and shader licenses. Any old pin, count,
branch strategy or “active” label applies to that historical 26.2 snapshot only.
Use the current matrix above and lock files for the primary 26.3 baseline.
The general client-only/stability conclusions remain; exact exceptions do not
transfer automatically between versions.

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
At the screenshot review, the maintained baseline was 41 features and eleven
libraries, pack 26.2.0.9.0. Both candidates remain outside the collection, index
and export. The later shader milestone is recorded separately below.

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
The earlier screenshot review applied shared documentation guards and candidate
findings to the future 26.3 bootstrap as forward preparation. Its 30 installed
features and 41 future identities did not change. Current policy ends automatic
propagation; the shader milestone leaves 26.3 untouched. Neither screenshot
candidate is promoted there or claimed compatible with 26.3.

## Optional shaders and distribution, 2026-11-19

Decision: option A, Complementary Reimagined r5.10 plus MakeUp - Ultra Fast 9.6.
Both are installed choices and remain disabled in a clean instance. The pack
retains 41 Fabric feature mods and eleven libraries; the two shaders are visual
resources, recorded under `[[shader]]` separately from those mod selections.
There are 54 upstream downloads. No supporting mod or prior pin is changed.
The 26.2 inventory is frozen pending owner runtime acceptance and qualification.

### Selection and evidence matrix

V = supported by official metadata or inspected release source. C = supported
with caveats. U = unverified runtime/GPU behavior. No cell records an in-game
result or an independent performance measurement. Requested weights are retained.

| Criterion | Weight | Complementary Reimagined | MakeUp - Ultra Fast |
| --- | --- | --- | --- |
| Iris/rendering stack | 25% | V: release lists Iris/26.2. Optional CUSTOM_IMAGES, SSBO, BLOCK_EMISSION_ATTRIBUTE, FADE_VARIABLE and ENTITY_TRANSLUCENT flags exist in pinned Iris 1.11.4; no required flag list found. U: compilation/rendering on owner's GPU. | V: release lists Iris/26.2; included README requires Iris >=1.5.1, satisfied by 1.11.4. U: exact driver/rendering acceptance. |
| Visual style | 20% | Featured choice: upstream Reimagined defaults preserve blocky Minecraft styling with atmospheric lighting/clouds. Unbound differs mainly in defaults and would be redundant here. Appearance is owner-assessed, not observed in this audit. | Alternative color schemes and modular effects; vanilla-like restraint depends on chosen options. Not presented as identical to Reimagined or photorealism. |
| Performance accessibility | 20% | V: Potato/Very Low/Low/Medium/High/Very High/Ultra and additional high-end profiles. Higher colored-light/reflection settings use more resources. U: measured frame times/VRAM. | V: no-effects, three shadowless profiles, Low/Medium/High/Extreme+. Shadows, reflection, clouds, bloom and depth of field are configurable. U: faster than Complementary on the owner's hardware. |
| Stability/maintenance | 15% | Long-maintained project, current release dated November 18. New r5.10 lighting changes warrant acceptance. Open reports include water/weather artifacts and culling/skin/transparency scenarios. | Release 9.6 dated October 19; recent releases address Iris enchantment glint and End rendering. Open reports include translucency, fog compilation and optional DoF on Apple Silicon. None reproduced here. |
| Licensing/distribution | 10% | V: release's Complementary License Agreement 1.8 explicitly permits unmodified modpack use through platform systems; official Modrinth reference selected. | V: upstream LGPL-3.0-or-later designation, LGPL v3 text and copyright/source notices inside official ZIP. Unmodified official reference selected. |
| Distinct value | 10% | Main atmospheric, Minecraft-styled experience with integrated material/light effects. | Adjustable alternative emphasizing lower-effect/shadowless choices and its own color treatment; offers a different starting point without another renderer. |

A qualifies statically and gives a clear featured/adjustable choice. C would
omit that alternative without resolving a known hard compatibility problem.
Miniature is considered only as the fallback for an unsuitable or redundant
primary candidate. Neither condition was established, so B needs no deeper
artifact audit and Miniature is not installed. D is unnecessary because the two
selected releases have verifiable platform distribution grants and Iris support.
No controlled comparative benchmark was found in the reviewed release materials.
No benchmark ranks the shaders. Keep shaders disabled for the optimized vanilla
baseline; the word "Ultra Fast" is an upstream name, not a pack guarantee.

### Exact releases and source correspondence

| Project | Exact release | Official artifact and integrity |
| --- | --- | --- |
| [Complementary Reimagined](https://modrinth.com/shader/complementary-reimagined), `HVnmMxH1` | `r5.10`, `RKfUB9VC`, release, Iris, Minecraft 26.2 listed | [ComplementaryReimagined_r5.10.zip](https://cdn.modrinth.com/data/HVnmMxH1/versions/RKfUB9VC/ComplementaryReimagined_r5.10.zip), 567,387 bytes. SHA-512 `edced01fb330af215ac73b8d9d31011565089f971f87145b87f413f40ee2128b48970aed26f8e5e879899647ec847b3eefca64bfc013aabbcf25275a207f663d`. |
| [MakeUp - Ultra Fast](https://modrinth.com/shader/makeup-ultra-fast-shaders), `izsIPI7a` | `9.6`, `t4YRxQug`, release, Iris, Minecraft 26.2 listed | [MakeUp-UltraFast-9.6.zip](https://cdn.modrinth.com/data/izsIPI7a/versions/t4YRxQug/MakeUp-UltraFast-9.6.zip), 406,830 bytes. SHA-512 `fa7af14ac14bd77bc1c5d8abf5243e9f3dae08777272790de62b9f388db2f5383f8b00c61da358a356a43635afb7cab80ea7196ffd3a97e22d3184b76e9f3fd3`. |

Hashes matched the downloaded official ZIPs during inspection. Complementary's
447 archived files match [source revision e10d27d](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/tree/e10d27dec5acfb18509fdcc3cda704152dc2f7df)
after normalizing CRLF/LF for comparison only. MakeUp's 344 shader files, README
and LICENSE match [source revision fed6d05](https://github.com/javiergcim/MakeUpUltraFast/tree/fed6d05f841389fb5981f078e2fcac8dfb9c0080)
byte-for-byte. No downloaded file or ZIP was modified. No Fabric descriptor,
Java mod, installer or server companion was substituted for a shader resource.
Neither release declares required Modrinth dependency projects. Iris is the
already-selected renderer, not a new transitive mod. The native Fabric graph and
all 52 prior locks remain unchanged. Project environment labels are client
required/server unsupported, and every shader lock explicitly uses client side.

Iris `gxZWWnKH`, 1.11.4, and Sodium `xJZxADzI`, 0.9.2, remain pinned. The inspected
Iris binary contains Complementary's optional flags, but their usability also
depends on hardware. The exact shader/renderer artifacts are bound in the
snapshot's distribution audit; an Iris pin change requires re-review. Metadata
and recognized flags cannot prove GLSL compilation or GPU compatibility.
Packwiz's pinned executable reports the newer shader environment enum as unknown
and initially writes both-side records. The two generated records were set to
`side = "client"` and `pin = true`, consistent with the audited v2 labels and
existing export contract. No general environment or prerelease exception changed.

### Distribution gate and attribution

Complementary's [release license](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/e10d27dec5acfb18509fdcc3cda704152dc2f7df/License.txt)
is Agreement 1.8. ZIP member `License.txt` has SHA-256
`2d2f14f4e04e9a19ea11bb67c13cabe1ef458113320c02bbae87527b862266b6`.
Section 1.2 permits modpack inclusion through Modrinth/CurseForge systems,
requires unmodified contents and pack-author responsibility for integration
problems, and prohibits direct file uploads. Visible credit is mandatory when
enabled by default; Lantern Crossing credits EminGT / Complementary Development
with the official link even though it starts disabled. Lantern Crossing accepts
responsibility for problems arising from this integration. Changes to shader
code/variables or standalone redistribution are outside this chosen grant.
The license also restricts AI-training use; repository MIT terms do not override
any shader terms. No special installer, automatic patcher or modified shader is
included. The `.mrpack` contains official Modrinth download references only.

MakeUp's [release LICENSE](https://github.com/javiergcim/MakeUpUltraFast/blob/fed6d05f841389fb5981f078e2fcac8dfb9c0080/LICENSE)
is LGPL v3, with ZIP-member SHA-256
`e3a994d82e644b03a792a930f574002658412f62407f5fee083f2555c5f23118`.
Modrinth designates LGPL-3.0-or-later. The release includes readable shader source,
copyright notices and a README requesting credit and official links. README now
credits Javier Garduño / javiergcim and links the official project/source plus
[LGPL](https://www.gnu.org/licenses/lgpl-3.0.html); the incorporated
[GPL terms](https://www.gnu.org/licenses/gpl-3.0.html) remain applicable as upstream
specifies. We reference the complete unmodified upstream ZIP, retain its notices,
and distribute no compiled derivative or copied source tree. No further
release-specific modpack restriction was found in the exact ZIP/README. Automatic
launcher downloading uses Modrinth's ordinary modpack file mechanism.

No extra license notice payload is needed for this reference-only architecture;
original notices travel inside upstream ZIPs. Any future pack description page
must retain the credits/links and integration responsibility stated in README.
No modpack-level MIT permission is asserted over shaders. Each audit is tied to
its exact release ID, artifact SHA-512, release-license fingerprint and Iris pin.
Future changes require a fresh distribution/compatibility review.

### Rendering caveats and owner acceptance

Both packs operate on the client-visible world and need no vanilla-server mod,
plugin, custom protocol or unavailable server data. Their visuals are not
server-side light/spawn state. No network/upload feature or extra launcher
integration is selected. Ordinary Iris loading from `shaderpacks/` is the static
Prism/Modrinth interoperability basis, not an observed launcher result.

Continuity CTM and BetterGrassify remain unchanged; no custom textures/PBR pack
is installed. More Culling and Entity Culling can interact with shader shadows,
foliage and translucent surfaces. Check these with actual movement and lighting.
LambDynamicLights remains the no-shader light provider. Complementary has held
and optional colored dynamic lighting; MakeUp also shades held-light information.
Do not globally disable existing lighting or force a shader profile to avoid a
runtime interaction that has not been observed. The owner should check doubled
hand/entity brightness and preserve the useful no-shader behavior when adjusting.

Relevant reports are evidence for focused tests, not reproduced pack failures:
[MakeUp 208](https://github.com/javiergcim/MakeUpUltraFast/issues/208) describes
optional DoF edge artifacts on Apple Silicon with 26.3/Iris 1.11.7, not our exact
stack; DoF is off in the inspected ordinary defaults. [MakeUp 207](https://github.com/javiergcim/MakeUpUltraFast/issues/207)
reports a fog compile error without enough environment detail to establish its
scope. [LambDynamicLights 383](https://github.com/LambdAurora/LambDynamicLights/issues/383)
reports bright player models with Photon, not either selected shader. Review
water/rain, translucent player skins, signs, portals, leaves and all dimensions.
No source issue is silently treated as fixed by metadata compatibility.

Configured Defaults still seeds only `enableShaders=false` if the entire Iris
config is absent. It does not replace an existing active shader or user preset.
ZIP option sidecars are never shipped. Defaults, screenshots, worlds and existing
mod versions are unchanged. Complete the new owner matrix in both launchers;
no Minecraft, GPU benchmark, shader compilation or runtime acceptance was run.
This milestone leaves the 26.3 branch and hosting default untouched. Forward
migration begins from the accepted 26.2 inventory after its qualification/release.
