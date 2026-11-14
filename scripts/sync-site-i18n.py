#!/usr/bin/env python3
"""Sync shared copy into both app.js dictionaries without reformatting other keys."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from site_i18n import RU, EN


def sync() -> None:
    path = ROOT / "app.js"
    text = path.read_text()
    pattern = r'(var i18n = \{\s*ru: )(\{.*?\})(,\s*en: )(\{.*?\})(\s*\};)'
    match = re.search(pattern, text, re.S)
    if not match:
        raise RuntimeError("Cannot find both app.js language dictionaries")

    def update(block, values):
        json.loads(block)  # Validate before editing.
        for key, value in values.items():
            encoded = json.dumps(value, ensure_ascii=False)
            key_pattern = r'("' + re.escape(key) + r'":\s*)"(?:[^"\\]|\\.)*"'
            if re.search(key_pattern, block):
                block = re.sub(key_pattern, lambda m: m[1] + encoded, block, count=1)
            else:
                block = block.rstrip()[:-1].rstrip() + ',\n          ' + json.dumps(key) + ': ' + encoded + '\n        }'
        json.loads(block)
        return block

    replacement = match[1] + update(match[2], RU) + match[3] + update(match[4], EN) + match[5]
    path.write_text(text[:match.start()] + replacement + text[match.end():])
    print("Shared RU/EN copy synced to app.js")


if __name__ == "__main__":
    sync()
