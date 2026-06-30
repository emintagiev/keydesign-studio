#!/usr/bin/env python3
"""Remove draft nav links from production dist/ bundle only."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAV_LINK = re.compile(
    r'^\s*<a class="nav__link" href="(?:approach|partners)\.html"[^>]*>.*?</a>\s*\n',
    re.MULTILINE,
)


def strip_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = NAV_LINK.sub("", text)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    dist = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    if not dist.is_dir():
        print(f"  ! dist not found: {dist}", file=sys.stderr)
        sys.exit(1)

    changed = sum(1 for html in dist.glob("*.html") if strip_file(html))
    print(f"  → prod nav: removed Подход/Партнёры from {changed} pages")


if __name__ == "__main__":
    main()
