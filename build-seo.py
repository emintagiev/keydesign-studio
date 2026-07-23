#!/usr/bin/env python3
"""Generate robots/sitemap and inject SEO tags into HTML pages."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from seo import (
    STATIC_PAGES,
    inject_seo,
    page_url,
    write_robots,
    write_sitemap,
)

ROOT = Path(__file__).resolve().parent
PROJECTS_DIR = ROOT / "content" / "projects"


def load_projects() -> list[dict]:
    site_path = ROOT / "content" / "site.yaml"
    site = yaml.safe_load(site_path.read_text(encoding="utf-8")) if site_path.exists() else {}
    order = site.get("projects_order") or []
    order_index = {slug: idx for idx, slug in enumerate(order)}

    projects = []
    for path in sorted(PROJECTS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not data.get("published", True):
            continue
        slug = data["slug"]
        projects.append(
            {
                "slug": slug,
                "file": f"{slug}.html",
                "path": f"/{slug}",
                "title": data["title_plain"],
                "description": data.get("description") or f'{data["title_plain"]} - проект Key Design Studio.',
                "cover": data.get("cover"),
                "sort_order": order_index.get(slug, data.get("sort_order", 9999)),
            }
        )
    projects.sort(key=lambda p: p["sort_order"])
    return projects


def patch_static_pages() -> int:
    changed = 0
    for path_key, meta in STATIC_PAGES.items():
        file_path = ROOT / meta["file"]
        if not file_path.exists():
            print(f"  skip missing: {meta['file']}")
            continue
        if path_key == "/":
            title = meta["title"]
        else:
            title = f"{meta['title']} - Key Design Studio"
        updated = inject_seo(
            file_path.read_text(encoding="utf-8"),
            canonical_path=path_key,
            title=title,
            description=meta["description"],
            og_image=meta.get("og_image"),
        )
        file_path.write_text(updated, encoding="utf-8")
        changed += 1
        print(f"  seo: {meta['file']}")
    return changed


def patch_key_design_studio() -> None:
    file_path = ROOT / "key-design-studio.html"
    if not file_path.exists():
        return
    updated = inject_seo(
        file_path.read_text(encoding="utf-8"),
        canonical_path="/",
        title="Key Design Studio - студия интерьерного дизайна",
        description=STATIC_PAGES["/"]["description"],
        og_image=STATIC_PAGES["/"]["og_image"],
        noindex=True,
    )
    file_path.write_text(updated, encoding="utf-8")
    print("  seo: key-design-studio.html (noindex, canonical /)")


def patch_project_pages(projects: list[dict]) -> int:
    changed = 0
    for project in projects:
        file_path = ROOT / project["file"]
        if not file_path.exists():
            print(f"  skip missing: {project['file']}")
            continue
        title = f'{project["title"]} - проект Key Design Studio'
        updated = inject_seo(
            file_path.read_text(encoding="utf-8"),
            canonical_path=project["path"],
            title=title,
            description=project["description"],
            og_image=project.get("cover"),
        )
        file_path.write_text(updated, encoding="utf-8")
        changed += 1
        print(f"  seo: {project['file']}")
    return changed


def collect_sitemap_urls(projects: list[dict]) -> list[str]:
    urls = [
        page_url(path)
        for path in STATIC_PAGES
        if STATIC_PAGES[path]["file"] != "key-design-studio.html"
    ]
    urls.extend(page_url(project["path"]) for project in projects)
    # Stable order: home first, then static, then projects
    home = page_url("/")
    static = [page_url(path) for path in ("/about", "/projects", "/services", "/contacts", "/privacy")]
    project_urls = [page_url(project["path"]) for project in projects]
    return [home, *static, *project_urls]


def main() -> int:
    print("SEO tags:")
    projects = load_projects()
    patch_static_pages()
    patch_key_design_studio()
    patch_project_pages(projects)

    print("SEO files:")
    write_robots(ROOT / "robots.txt")
    print("  robots.txt")
    urls = collect_sitemap_urls(projects)
    write_sitemap(ROOT / "sitemap.xml", urls)
    print(f"  sitemap.xml ({len(urls)} urls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
