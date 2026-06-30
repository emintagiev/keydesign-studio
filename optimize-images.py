#!/usr/bin/env python3
"""Resize and recompress site images for web (in place)."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
MAX_EDGE = 1920
JPEG_QUALITY = 76
SKIP_DIRS = {"logo-tmp", "hero", "thumbs"}
MIN_BYTES_TO_TOUCH = 180_000  # skip tiny files already web-sized
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path: Path):
    p = run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", "-g", "format", str(path)])
    if p.returncode != 0:
        return None
    data = {}
    for line in p.stdout.splitlines():
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    try:
        w = int(data.get("pixelWidth", 0))
        h = int(data.get("pixelHeight", 0))
    except ValueError:
        return None
    return w, h, data.get("format", "").lower()


def optimize_file(path: Path):
    size = path.stat().st_size
    info = probe(path)
    if not info:
        return "skip", size, size

    w, h, fmt = info
    max_dim = max(w, h)
    ext = path.suffix.lower()

    if size < MIN_BYTES_TO_TOUCH and max_dim <= MAX_EDGE:
        return "skip", size, size

    tmp = path.with_name(path.stem + ".__opt__" + path.suffix)
    try:
        if ext in {".jpg", ".jpeg"} or fmt == "jpeg":
            cmd = [
                "sips",
                "-Z",
                str(MAX_EDGE),
                "-s",
                "format",
                "jpeg",
                "-s",
                "formatOptions",
                str(JPEG_QUALITY),
                str(path),
                "--out",
                str(tmp),
            ]
        else:
            cmd = ["sips", "-Z", str(MAX_EDGE), str(path), "--out", str(tmp)]

        res = run(cmd)
        if res.returncode != 0 or not tmp.exists():
            return "fail", size, size

        new_size = tmp.stat().st_size
        tmp.replace(path)
        return "ok", size, new_size
    finally:
        if tmp.exists():
            tmp.unlink()


def main():
    files = []
    for path in ASSETS.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in IMAGE_EXT or path.suffix.lower() in {e.lower() for e in IMAGE_EXT}:
            files.append(path)

    files.sort()
    before = sum(f.stat().st_size for f in files)
    ok = skip = fail = 0
    saved = 0

    for i, path in enumerate(files, 1):
        status, old, new = optimize_file(path)
        if status == "ok":
            ok += 1
            saved += old - new
            if old > new * 1.15:
                print(f"  [{i}/{len(files)}] {path.relative_to(ROOT)}  {old // 1024}KB → {new // 1024}KB")
        elif status == "skip":
            skip += 1
        else:
            fail += 1
            print(f"  ! fail {path.relative_to(ROOT)}", file=sys.stderr)

    after = sum(f.stat().st_size for f in files)
    print(
        f"\nDone: {ok} optimized, {skip} skipped, {fail} failed\n"
        f"Before: {before / 1024 / 1024:.1f} MB\n"
        f"After:  {after / 1024 / 1024:.1f} MB\n"
        f"Saved:  {saved / 1024 / 1024:.1f} MB"
    )


if __name__ == "__main__":
    main()
