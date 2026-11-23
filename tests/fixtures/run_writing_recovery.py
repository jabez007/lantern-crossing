"""Reproduce recorded candidate findings using exact JARs, without loading Minecraft."""

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
STUBS = {
    "ru/svyaton/bookpaste/BookPasteConfigManager.java": (
        "package ru.svyaton.bookpaste; public class BookPasteConfigManager {"
        "private static final BookPasteConfig CONFIG = new BookPasteConfig();"
        "public static BookPasteConfig getConfig() { return CONFIG; }}"
    ),
    "net/minecraft/client/Minecraft.java": (
        "package net.minecraft.client; public class Minecraft {}"
    ),
    "net/minecraft/client/gui/screens/inventory/BookEditScreen.java": (
        "package net.minecraft.client.gui.screens.inventory; public class BookEditScreen {}"
    ),
    "net/minecraft/client/gui/screens/inventory/PageButton.java": (
        "package net.minecraft.client.gui.screens.inventory;"
        "public class PageButton { public boolean visible; }"
    ),
    "net/minecraft/network/chat/Component.java": (
        "package net.minecraft.network.chat; public interface Component {}"
    ),
    "net/minecraft/world/entity/player/Player.java": (
        "package net.minecraft.world.entity.player; public class Player {}"
    ),
    "net/minecraft/client/player/LocalPlayer.java": (
        "package net.minecraft.client.player;"
        "public class LocalPlayer extends net.minecraft.world.entity.player.Player {}"
    ),
    "net/minecraft/network/protocol/Packet.java": (
        "package net.minecraft.network.protocol; public interface Packet<T> {}"
    ),
    "net/minecraft/network/protocol/game/ServerboundEditBookPacket.java": (
        "package net.minecraft.network.protocol.game; public class ServerboundEditBookPacket"
        " implements net.minecraft.network.protocol.Packet<Object> {}"
    ),
    "org/spongepowered/asm/mixin/injection/callback/CallbackInfo.java": (
        "package org.spongepowered.asm.mixin.injection.callback;"
        "public class CallbackInfo { public void cancel() {} }"
    ),
}


def check_digest(path: Path, algorithm: str, expected: str) -> None:
    if hashlib.new(algorithm, path.read_bytes()).hexdigest() != expected:
        raise ValueError(f"audit input hash mismatch: {path.name}")


def run_oracle(jdk: Path, artifacts: Path, gson: Path) -> dict:
    evidence = json.loads((FIXTURES / "writing-recovery.json").read_text())
    adapter = FIXTURES / "WritingRecoveryOracle.java"
    check_digest(adapter, "sha256", evidence["adapter-sha256"])
    check_digest(gson, "sha1", evidence["gson"]["sha1"])
    jars = []
    for slug in evidence["oracle-projects"]:
        entry = evidence["artifacts"][slug]
        path = artifacts / entry["filename"]
        check_digest(path, "sha512", entry["sha512"])
        jars.append(str(path.resolve()))
    classpath = ":".join([*jars, str(gson.resolve())])
    with tempfile.TemporaryDirectory(prefix="writing-recovery-") as temporary:
        work = Path(temporary)
        sources = []
        for name, content in STUBS.items():
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content + "\n")
            sources.append(str(path))
        classes = work / "classes"
        classes.mkdir()
        subprocess.run(
            [str(jdk / "bin/javac"), "-cp", classpath, "-d", str(classes), *sources, str(adapter)],
            check=True,
        )
        result = subprocess.run(
            [
                str(jdk / "bin/java"),
                "-cp",
                str(classes) + ":" + classpath,
                "me.devjg.booker.mixin.WritingRecoveryOracle",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    observed = json.loads(result.stdout)
    if observed != evidence["observations"]:
        raise ValueError("upstream findings changed; review before replacing recorded evidence")
    return observed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jdk", type=Path, required=True, help="JDK 25 or newer root")
    parser.add_argument(
        "--artifacts", type=Path, required=True, help="exact candidate JAR directory"
    )
    parser.add_argument("--gson", type=Path, required=True, help="official Gson 2.14.0 JAR")
    args = parser.parse_args()
    print(json.dumps(run_oracle(args.jdk, args.artifacts, args.gson), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
