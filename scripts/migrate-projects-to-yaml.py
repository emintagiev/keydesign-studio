#!/usr/bin/env python3
"""One-time migration: build-projects.py PROJECTS -> content/*.yaml"""

import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PROJECTS_DIR = CONTENT / "projects"


def load_build_module():
    spec = importlib.util.spec_from_file_location("build_projects", ROOT / "build-projects.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def project_to_yaml(cfg: dict, sort_order: int) -> dict:
    data = {
        "slug": cfg["slug"],
        "title_plain": cfg["title_plain"],
        "title_html": cfg["title_html"],
        "eyebrow": cfg["eyebrow"],
        "lead": cfg.get("lead", ""),
        "meta": dict(cfg["meta"]),
        "description": cfg["description"],
        "cover": cfg["cover"],
        "grid_city": cfg["grid_city"],
        "carousel_cat": cfg["carousel_cat"],
        "carousel_name": cfg["carousel_name"],
        "i18n_cat": cfg["i18n_cat"],
        "i18n_name": cfg["i18n_name"],
        "published": True,
        "sort_order": sort_order,
        "rooms": [],
    }

    if "room_map" in cfg:
        for _folder, room_slug, name, cover in cfg["room_map"]:
            data["rooms"].append(
                {"slug": room_slug, "name": name, "cover_filename": cover}
            )
    elif "flat_room" in cfg:
        room_slug, name, cover = cfg["flat_room"]
        data["rooms"].append(
            {"slug": room_slug, "name": name, "cover_filename": cover}
        )

    return data


def main():
    mod = load_build_module()
    projects = mod.PROJECTS
    featured = mod.HOME_FEATURED_SLUGS

    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    site = {
        "featured_slugs": list(featured),
        "projects_order": [p["slug"] for p in projects],
    }
    (CONTENT / "site.yaml").write_text(
        yaml.dump(site, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"  -> content/site.yaml")

    for i, cfg in enumerate(projects, start=1):
        data = project_to_yaml(cfg, i)
        path = PROJECTS_DIR / f"{cfg['slug']}.yaml"
        path.write_text(
            yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        print(f"  -> {path.relative_to(ROOT)}")

    print(f"Migrated {len(projects)} projects.")


if __name__ == "__main__":
    main()
