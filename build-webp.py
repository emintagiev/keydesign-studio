#!/usr/bin/env python3
"""Create WebP copies of project photos. Originals stay in place."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "assets" / "projects"
MANIFEST = ROOT / "content" / "image-manifest.json"
ORIGIN_EXTS = {".jpg", ".jpeg", ".png"}
FULL_WIDTH = 2000
PREVIEW_WIDTH = 800
QUALITY = 80


def natural_sort_key(name: str):
    import re
    parts = re.split(r"(\d+)", name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def list_originals(folder: Path) -> list[Path]:
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ORIGIN_EXTS]
    return sorted(files, key=lambda p: natural_sort_key(p.name))


def save_webp(src: Image.Image, dest: Path, max_width: int) -> tuple[int, int]:
    image = src
    if image.width > max_width:
        height = round(image.height * max_width / image.width)
        image = image.resize((max_width, height), Image.Resampling.LANCZOS)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, "WEBP", quality=QUALITY, method=4)
    return image.width, image.height


def main() -> None:
    manifest = {}
    count = 0
    for room_dir in sorted(p for p in PROJECTS.glob("*/*") if p.is_dir()):
        slug = room_dir.parent.name
        room = room_dir.name
        for index, src in enumerate(list_originals(room_dir), start=1):
            stem = f"{slug}-{room}-{index:02d}"
            full = room_dir / f"{stem}.webp"
            preview = room_dir / f"{stem}-800.webp"
            with Image.open(src) as image:
                image.load()
                width, height = save_webp(image, full, FULL_WIDTH)
                preview_width, preview_height = save_webp(image, preview, PREVIEW_WIDTH)
            rel = src.relative_to(ROOT).as_posix()
            manifest[rel] = {
                "webp": full.relative_to(ROOT).as_posix(),
                "webp800": preview.relative_to(ROOT).as_posix(),
                "width": width,
                "height": height,
                "preview_width": preview_width,
                "preview_height": preview_height,
            }
            count += 1
            if count % 25 == 0:
                print(f"  {count} photos")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WebP copies: {count}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
