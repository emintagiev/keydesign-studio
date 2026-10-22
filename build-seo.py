#!/usr/bin/env python3
"""Generate robots/sitemap and inject SEO tags into HTML pages."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from site_common import SERVICES, published_guides, sync_nav
from seo import (
    STATIC_PAGES,
    file_lastmod,
    inject_metrika,
    inject_seo,
    page_url,
    project_seo,
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
        if " " in path.name:
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not data.get("published", True):
            continue
        slug = data["slug"]
        data["slug"] = slug
        title, description = project_seo(data)
        projects.append(
            {
                "slug": slug,
                "file": f"{slug}.html",
                "path": f"/{slug}",
                "title": title,
                "description": description,
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
        title = meta["title"]
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
        title=STATIC_PAGES["/"]["title"],
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
        title = project["title"]
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


def collect_sitemap(projects: list[dict]) -> tuple[list[str], dict[str, str]]:
    home = page_url("/")
    service_paths = tuple(f"/{svc['slug']}" for svc in SERVICES)
    static_paths = ("/about", "/projects", "/services", *service_paths, "/contacts", "/privacy")
    urls = [home, *[page_url(path) for path in static_paths]]
    lastmods = {home: file_lastmod(ROOT / "index.html")}
    for path in static_paths:
        lastmods[page_url(path)] = file_lastmod(ROOT / STATIC_PAGES[path]["file"])
    for project in projects:
        url = page_url(project["path"])
        urls.append(url)
        html_path = ROOT / project["file"]
        yaml_path = ROOT / "content" / "projects" / f'{project["slug"]}.yaml'
        stamps = [file_lastmod(html_path)]
        if yaml_path.exists():
            stamps.append(file_lastmod(yaml_path))
        lastmods[url] = max(stamps)
    guides = published_guides()
    if guides:
        index_url = page_url("/guides")
        urls.append(index_url)
        lastmods[index_url] = file_lastmod(ROOT / "guides" / "index.html")
        for guide in guides:
            url = page_url(f"/guides/{guide['slug']}")
            urls.append(url)
            lastmods[url] = file_lastmod(ROOT / "guides" / f"{guide['slug']}.html")
    return urls, lastmods


def main() -> int:
    print("SEO tags:")
    projects = load_projects()
    patch_static_pages()
    patch_key_design_studio()
    patch_project_pages(projects)

    print("SEO files:")
    write_robots(ROOT / "robots.txt")
    print("  robots.txt")
    urls, lastmods = collect_sitemap(projects)
    write_sitemap(ROOT / "sitemap.xml", urls, lastmods)
    print(f"  sitemap.xml ({len(urls)} urls)")

    guides_on = bool(published_guides())
    metrika = 0
    nav = 0
    html_files = [p for p in sorted(ROOT.glob("*.html")) if " " not in p.name]
    html_files += [p for p in sorted((ROOT / "guides").glob("*.html")) if " " not in p.name]
    for html_path in html_files:
        original = html_path.read_text(encoding="utf-8")
        in_guides = html_path.parent.name == "guides"
        updated = inject_metrika(original)
        updated = sync_nav(updated, guides_on, active=in_guides)
        if updated != original:
            html_path.write_text(updated, encoding="utf-8")
            metrika += 1
        if guides_on and 'href="/guides"' in updated:
            nav += 1
    print(f"  metrika/nav: {metrika} pages changed; guides menu: {'on' if guides_on else 'off'} ({nav} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
