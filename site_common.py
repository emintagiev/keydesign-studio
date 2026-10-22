#!/usr/bin/env python3
"""Общие функции для генераторов страниц услуг и раздела статей."""

from __future__ import annotations

import html
import importlib.util
import json
import re
from pathlib import Path

import yaml

from seo import SITE_ORIGIN, inject_seo

ROOT = Path(__file__).resolve().parent
GUIDES_DIR = ROOT / "content" / "guides"
GUIDES_OUT = ROOT / "guides"

# Услуги: порядок и привязка проектов (Москва и Дубай в блоки услуг не ставим).
SERVICES = [
    {
        "n": 1,
        "key": "design",
        "slug": "uslugi-dizajn-proekt",
        "name": "Дизайн-проект интерьера",
        "orb": "assets/services/service-design.jpg",
        "projects": ["ns-akadem-pulsar", "oblaka-orhan", "kedrovy-ns"],
        "cost_key": "svc.cost.1",
    },
    {
        "n": 2,
        "key": "management",
        "slug": "uslugi-komplektaciya",
        "name": "Проектное сопровождение",
        "orb": "assets/services/service-management.jpg",
        "projects": ["kedrovy-ns", "kvartal-dekabristov"],
        "cost_key": "svc.cost.n",
    },
    {
        "n": 3,
        "key": "supervision",
        "slug": "uslugi-avtorskij-nadzor",
        "name": "Авторский надзор",
        "orb": "assets/services/service-supervision.jpg",
        "projects": ["kvartal-dekabristov", "nevskaya-dom"],
        "cost_key": "svc.cost.n",
    },
    {
        "n": 4,
        "key": "planning",
        "slug": "uslugi-arhitekturnoe-planirovanie",
        "name": "Архитектурное планирование",
        "orb": "assets/services/service-architecture.jpg",
        "projects": ["ns-akadem-pulsar", "little-classic"],
        "cost_key": "svc.cost.n",
    },
]

SERVICE_BY_KEY = {s["key"]: s for s in SERVICES}


def load_build_projects():
    spec = importlib.util.spec_from_file_location("build_projects", ROOT / "build-projects.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_BP = None


def bp():
    global _BP
    if _BP is None:
        _BP = load_build_projects()
    return _BP


# ---------------------------------------------------------------- статьи

def guide_files(include_drafts: bool = False) -> list[Path]:
    out = []
    if not GUIDES_DIR.exists():
        return out
    for path in sorted(GUIDES_DIR.glob("*.md")):
        if " " in path.name:
            continue
        if path.name.startswith("_") and not include_drafts:
            continue
        out.append(path)
    return out


def parse_guide(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    meta = (yaml.safe_load(match.group(1)) if match else {}) or {}
    body = match.group(2) if match else text
    meta["slug"] = str(meta.get("slug") or path.stem.lstrip("_"))
    meta["body"] = body
    meta["draft"] = path.name.startswith("_")
    meta["date"] = str(meta.get("date") or "")
    return meta


def published_guides() -> list[dict]:
    items = []
    for path in guide_files():
        guide = parse_guide(path)
        if guide.get("published", True) is False:
            continue
        items.append(guide)
    items.sort(key=lambda g: g["date"], reverse=True)
    return items


def has_published_guides() -> bool:
    return bool(published_guides())


# ---------------------------------------------------------------- меню

_SERVICES_LINK_RE = re.compile(
    r'(?P<indent>[ \t]*)<a class="nav__link(?: nav__link--active)?" href="/services"[^>]*>[^<]*</a>'
)
_GUIDES_LINK_RE = re.compile(
    r'\n?[ \t]*<a class="nav__link(?: nav__link--active)?" href="/guides"[^>]*>[^<]*</a>'
)


def sync_nav(text: str, enabled: bool, active: bool = False) -> str:
    """Пункт «Статьи» в меню: есть только когда опубликована хотя бы одна статья."""
    text = _GUIDES_LINK_RE.sub("", text)
    if not enabled:
        return text
    cls = "nav__link nav__link--active" if active else "nav__link"
    link = f'<a class="{cls}" href="/guides" data-i18n="nav.guides">Статьи</a>'
    return _SERVICES_LINK_RE.sub(lambda m: f"{m.group(0)}\n{m.group('indent')}{link}", text, count=1)


# ---------------------------------------------------------------- пути

def absolutize(text: str) -> str:
    """Для страниц во вложенных папках: относительные ссылки на ресурсы -> от корня."""
    skip = ("http://", "https://", "/", "#", "mailto:", "tel:", "data:", "javascript:")

    def fix_attr(match):
        value = match.group(2)
        if value.startswith(skip):
            return match.group(0)
        return f'{match.group(1)}/{value}"'

    text = re.sub(r'(\b(?:src|href|poster)=")([^"]*)"', fix_attr, text)

    def fix_srcset(match):
        parts = []
        for item in match.group(2).split(", "):
            item = item.strip()
            if item and not item.startswith(skip):
                item = "/" + item
            parts.append(item)
        return f'{match.group(1)}{", ".join(parts)}"'

    return re.sub(r'(\bsrcset=")([^"]*)"', fix_srcset, text)


# ---------------------------------------------------------------- блоки

def brief_block() -> str:
    text = (ROOT / "services.html").read_text(encoding="utf-8")
    match = re.search(r'(  <div class="brief" id="brief".*?)\n  <script src="brief-config\.js', text, re.S)
    if not match:
        raise RuntimeError("Не нашёл окно заявки в services.html")
    return match.group(1)


def project_cards(slugs: list[str]) -> str:
    text = (ROOT / "projects.html").read_text(encoding="utf-8")
    found = {}
    for match in re.finditer(r'<a class="proj-grid-card" href="/([^"]+)">.*?</a>', text, re.S):
        found[match.group(1)] = match.group(0)
    cards = []
    for slug in slugs:
        if slug not in found:
            raise RuntimeError(f"Нет карточки проекта {slug} в projects.html")
        cards.append("        " + found[slug])
    return "\n".join(cards)


def app_ru(key: str) -> str:
    """Русский текст из словаря app.js (первое вхождение ключа)."""
    text = (ROOT / "app.js").read_text(encoding="utf-8")
    match = re.search(r'"%s":\s*"((?:[^"\\]|\\.)*)"' % re.escape(key), text)
    if not match:
        raise KeyError(key)
    return json.loads('"' + match.group(1) + '"')


FONTS = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    rel="preload"
    as="style"
    href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500&display=swap"
    onload="this.onload=null;this.rel='stylesheet'"
  />
  <noscript>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500&display=swap"
    />
  </noscript>"""


def ld_script(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f'  <script type="application/ld+json">{payload}</script>'


def provider_ld() -> dict:
    return {"@type": "ProfessionalService", "name": "Key Design Studio", "url": f"{SITE_ORIGIN}/"}


def page_shell(
    *,
    title: str,
    description: str,
    canonical_path: str,
    main_html: str,
    og_image: str | None = None,
    extra_head: str = "",
    noindex: bool = False,
    nested: bool = False,
    active: str = "",
) -> str:
    b = bp()
    header = b.HEADER
    if active == "services":
        header = header.replace(
            '<a class="nav__link" href="/services"', '<a class="nav__link nav__link--active" href="/services"'
        )
    page = f"""<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
{b.JS_BOOTSTRAP}  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{html.escape(description, quote=True)}" />
  <meta name="theme-color" content="#f4efe7" />
  <title>{html.escape(title)}</title>
{FONTS}
{b.FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v={b.ASSET_CSS_VERSION}" />
{extra_head}
</head>
<body>
{header}

  <main id="top" class="services-page">
    <div class="container">
{main_html}
    </div>
  </main>

{b.FOOTER}

{brief_block()}
  <script src="brief-config.js?v=2" defer></script>
  <script src="app.js?v={b.ASSET_JS_VERSION}" defer></script>
</body>
</html>
"""
    page = inject_seo(
        page,
        canonical_path=canonical_path,
        title=title,
        description=description,
        og_image=og_image,
        noindex=noindex,
    )
    return absolutize(page) if nested else page
