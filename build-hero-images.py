#!/usr/bin/env python3
"""Build compressed hero slideshow and homepage grid thumbnails."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

HERO_SOURCES = [
    ("hero/1.jpg", "projects/moscow-studio/interior/1.jpg", 1600, 75),
    ("hero/2.jpg", "projects/zhk-arkhitektor/interior/IMG_4800.JPG", 1600, 75),
    (
        "hero/3.jpg",
        "projects/kedrovy-ns/kitchen-living/005848974447_0000(3)-denoise-upscale-1.9x.jpeg",
        1600,
        75,
    ),
    ("hero/4.jpg", "projects/dream-house/kitchen-living/8.jpg", 1600, 75),
    ("hero/5.jpg", "projects/zhk-pulsar/kitchen-living/12.jpg", 1600, 75),
]

THUMB_SOURCES = [
    ("thumbs/home/dream-house.jpg", "projects/dream-house/kitchen-living/8.jpg", 900, 78),
    ("thumbs/home/zhk-pulsar.jpg", "projects/zhk-pulsar/kitchen-living/12.jpg", 900, 78),
    ("thumbs/home/moscow-studio.jpg", "projects/moscow-studio/interior/1.jpg", 900, 78),
]


def run_sips(src: Path, dst: Path, max_edge: int, quality: int):
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "sips",
        "-Z",
        str(max_edge),
        "-s",
        "format",
        "jpeg",
        "-s",
        "formatOptions",
        str(quality),
        str(src),
        "--out",
        str(dst),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"sips failed for {src}: {res.stderr.strip()}")


def build(entries):
    for rel_out, rel_src, max_edge, quality in entries:
        src = ASSETS / rel_src
        dst = ASSETS / rel_out
        if not src.exists():
            print(f"  skip missing source: {rel_src}")
            continue
        before = src.stat().st_size
        run_sips(src, dst, max_edge, quality)
        after = dst.stat().st_size
        print(f"  {rel_out}: {before // 1024}KB -> {after // 1024}KB")


def main():
    print("Hero slides:")
    build(HERO_SOURCES)
    print("Homepage thumbs:")
    build(THUMB_SOURCES)
    print("Done.")


if __name__ == "__main__":
    main()
