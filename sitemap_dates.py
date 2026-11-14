"""Track content changes independently of checkout/build file timestamps."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def normalize_head_spacing(text: str) -> str:
    # SEO injection may add blank lines in head; body/pre whitespace is retained.
    return re.sub(r'(<head\b[^>]*>)(.*?)(</head>)',
                  lambda m: m[1] + re.sub(r'\n[ \t]*\n(?:[ \t]*\n)*', '\n', m[2]) + m[3],
                  text, count=1, flags=re.S | re.I)


def fingerprint(path: Path) -> str:
    text = normalize_head_spacing(path.read_text(encoding="utf-8"))
    # Cache busting alone is not a content update.
    text = re.sub(r'(app\.js|styles\.css)\?v=\d+', r'\1', text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def content_dates(pages: dict[str, Path], state_path: Path, today=None) -> dict[str, str]:
    today = today or datetime.now(ZoneInfo("Asia/Novosibirsk")).date().isoformat()
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    state = {}
    for url, path in pages.items():
        digest = fingerprint(path)
        old = previous.get(url, {})
        stamp = old["lastmod"] if old.get("sha256") == digest else today
        state[url] = {"sha256": digest, "lastmod": stamp}
    rendered = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not state_path.exists() or state_path.read_text() != rendered:
        state_path.write_text(rendered, encoding="utf-8")
    return {url: item["lastmod"] for url, item in state.items()}
