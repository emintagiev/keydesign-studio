#!/usr/bin/env python3
"""Package generated static files for Firebase without rebuilding user images.

Usage: python3 scripts/package-firebase.py /absolute/new/output/directory
The destination must be empty. Never includes server secrets or source documents.
"""
from pathlib import Path
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def package(destination: Path) -> tuple[int, int]:
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit("Output directory must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    public = destination / "public"
    public.mkdir()
    count = skipped = 0
    for pattern in ("*.html", "*.css", "*.js", "robots.txt", "sitemap.xml"):
        for source in ROOT.glob(pattern):
            if " " in source.name:
                continue
            shutil.copy2(source, public / source.name)
            count += 1
    for folder in ("guides", "assets"):
        for source in sorted((ROOT / folder).rglob("*")):
            if not source.is_file() or source.name.startswith("."):
                continue
            if folder == "guides" and (source.suffix != ".html" or source.name.startswith("_") or " " in source.name):
                continue
            # Ignore Finder/iCloud copies only when the original sibling exists.
            match = re.match(r"^(.*) [2-9][0-9]*(\.[^.]+)$", source.name)
            if match and source.with_name(match[1] + match[2]).is_file():
                skipped += 1
                continue
            target = public / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            count += 1
    config = json.loads((ROOT / "firebase.json").read_text())
    config["hosting"]["public"] = "public"
    # Match the verified live rewrite. A function pinTag triggers a functions
    # deployment even with --only hosting; keep the existing Cloud Run service.
    for rewrite in config["hosting"].get("rewrites", []):
        if rewrite.get("source") == "/api/brief.php":
            rewrite.pop("function", None)
            rewrite["run"] = {"serviceId": "brief", "region": "us-central1"}
    # This release updates Hosting only; the existing brief function is preserved.
    config.pop("functions", None)
    (destination / "firebase.json").write_text(json.dumps(config, indent=2) + "\n")
    return count, skipped


if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_absolute():
        raise SystemExit("Pass one absolute output directory")
    count, skipped = package(Path(sys.argv[1]))
    print(f"Firebase bundle: {count} files; {skipped} duplicate copies omitted")
