#!/usr/bin/env python3
"""Build compressed hero slideshow and homepage grid thumbnails."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

HERO_SOURCES = [
    (
        "hero/1.jpg",
        "projects/kedrovy-ns/kitchen-living/005848974447_0000(3)-denoise-upscale-1.9x.jpeg",
        1400,
        68,
    ),
    (
        "hero/1-m.jpg",
        "projects/kedrovy-ns/kitchen-living/005848974447_0000(3)-denoise-upscale-1.9x.jpeg",
        820,
        60,
    ),
    ("hero/2.jpg", "projects/nevskaya-dom/guest-bedroom/2.jpg", 1400, 68),
    ("hero/3.jpg", "projects/kvartira-dubay/kitchen-living/01.jpg", 1400, 68),
    ("hero/4.jpg", "projects/oblaka-orhan/interior/cam_25.jpg", 1400, 68),
    ("hero/5.jpg", "projects/dom-sinegore/kitchen-living/1.jpg", 1400, 68),
    ("hero/6.jpg", "projects/zhk-arkhitektor/interior/IMG_4800.JPG", 1400, 68),
    ("hero/7.jpg", "projects/moscow-studio/interior/1.jpg", 1400, 68),
]

THUMB_SOURCES = [
    ("thumbs/home/moscow-studio.jpg", "projects/moscow-studio/interior/1.jpg", 900, 78),
    ("thumbs/home/kvartira-dubay.jpg", "projects/kvartira-dubay/kitchen-living/01.jpg", 900, 78),
    ("thumbs/home/dom-sinegore.jpg", "projects/dom-sinegore/kitchen-living/1.jpg", 900, 78),
    ("thumbs/home/nevskaya-dom.jpg", "projects/nevskaya-dom/kitchen-living/8.jpg", 900, 78),
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


def build_opening_image():
    """Keep the supplied opening photo separate from existing user image edits."""
    from PIL import Image, ImageOps

    source = ROOT / "content" / "hero" / "opening-curtains-20261115.jpg"
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        for name, width in (("opening-curtains-v1", 1600),
                            ("opening-curtains-mobile-v1", 820)):
            resized = image.copy()
            resized.thumbnail((width, 10000), Image.Resampling.LANCZOS)
            target = ASSETS / "hero" / (name + ".webp")
            resized.save(target, "WEBP", quality=84, method=6)
            print(f"  {target.relative_to(ASSETS)}: {target.stat().st_size // 1024}KB")
            if width == 1600:
                resized.save(target.with_suffix(".jpg"), "JPEG", quality=84, optimize=True)


def main():
    build_opening_image()
    if "--opening-only" in sys.argv:
        return
    print("Hero slides:")
    build(HERO_SOURCES)
    print("Homepage thumbs:")
    build(THUMB_SOURCES)
    print("Done.")


if __name__ == "__main__":
    main()
