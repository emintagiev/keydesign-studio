#!/usr/bin/env python3
"""Sync asset cache-bust query strings across all HTML pages."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_VERSION = "39"
CSS_VERSION = "79"


def bump_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = re.sub(r"app\.js\?v=\d+", f"app.js?v={APP_VERSION}", text)
    updated = re.sub(r"styles\.css\?v=\d+", f"styles.css?v={CSS_VERSION}", updated)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    changed = sum(1 for html in sorted(target.glob("*.html")) if bump_file(html))
    print(f"  → asset versions: app.js?v={APP_VERSION}, styles.css?v={CSS_VERSION} ({changed} pages)")


if __name__ == "__main__":
    main()
