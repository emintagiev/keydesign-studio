#!/usr/bin/env python3
"""Reproduce measured image optimizations; retain all original PNG/JPEG files.

Requires Pillow with WebP support. If source images change after publication,
use a new version suffix and update HTML/cache rules (v1 URLs are immutable).
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]

for stem in ('logo', 'logo-light'):
    source = ROOT / 'assets' / (stem + '.png')
    with Image.open(source) as image:
        image.convert('RGBA').save(source.with_name(stem + '-v1.webp'),
                                   'WEBP', lossless=True, method=6, exact=True)

for stem in ('about-kristina', 'team/sofya-vigel', 'team/polina-trubina'):
    source = ROOT / 'assets' / (stem + '.jpg')
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        for width in (480, 960):
            resized = image.copy()
            resized.thumbnail((width, 10000), Image.Resampling.LANCZOS)
            resized.save(source.with_name(source.stem + f'-{width}-v1.webp'),
                         'WEBP', quality=88, method=6)
