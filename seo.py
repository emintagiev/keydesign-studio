#!/usr/bin/env python3
"""Shared SEO helpers for Key Design Studio."""

from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_ORIGIN = "https://www.keydesign.studio"
DEFAULT_OG_IMAGE = f"{SITE_ORIGIN}/assets/hero/1.jpg"
YANDEX_VERIFICATION = "b31dd3613bec3f68"

STATIC_PAGES: dict[str, dict[str, str]] = {
    "/": {
        "file": "index.html",
        "title": "Дизайн интерьера в Новосибирске — Key Design Studio",
        "description": (
            "Студия дизайна интерьера Кристины Парыгиной в Новосибирске: "
            "дизайн-проекты квартир, домов и коммерческих пространств. "
            "Проекты также в Москве и Дубае."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/about": {
        "file": "about.html",
        "title": "О студии — Кристина Парыгина и Key Design Studio",
        "description": (
            "Кристина Парыгина и команда Key Design Studio — "
            "студия дизайна интерьера в Новосибирске."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/projects": {
        "file": "projects.html",
        "title": "Проекты дизайна интерьера — Key Design Studio, Новосибирск",
        "description": (
            "Квартиры, загородные дома и салон красоты: проекты дизайна интерьера "
            "в Новосибирске, Москве и Дубае. Key Design Studio."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/services": {
        "file": "services.html",
        "title": "Услуги дизайнера интерьера в Новосибирске — Key Design Studio",
        "description": (
            "Дизайн-проект интерьера, проектное сопровождение и комплектация, "
            "авторский надзор, архитектурное планирование. Key Design Studio, Новосибирск."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/contacts": {
        "file": "contacts.html",
        "title": "Контакты — Key Design Studio, дизайн интерьера в Новосибирске",
        "description": (
            "Контакты Key Design Studio в Новосибирске — телефон, почта, "
            "Telegram, Instagram и адрес офиса на ул. Инженерная 7."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/privacy": {
        "file": "privacy.html",
        "title": "Политика конфиденциальности — Key Design Studio",
        "description": (
            "Политика конфиденциальности Key Design Studio — обработка "
            "персональных данных на сайте."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
}

NOINDEX_FILES = {"key-design-studio.html"}


TYPE_GENITIVE = {
    "Квартира": "квартиры",
    "Студия": "студии",
    "Частный дом": "дома",
    "Салон красоты": "салона красоты",
    "Кабинет": "кабинета",
    "Апартаменты": "апартаментов",
}

CITY_PREPOSITIONAL = {
    "Новосибирск": "Новосибирске",
    "Москва": "Москве",
    "Дубай": "Дубае",
    "Морозово": "Морозово",
}

# Место из уже опубликованного названия проекта. Пусто — отдельного ЖК в названии нет.
PROJECT_PLACE = {
    "moscow-studio": "ЖК Bauman Haus",
    "kvartira-dubay": "",
    "zhk-arkhitektor": "ЖК Архитектор",
    "oblaka-orhan": "ЖК Облака",
    "salon-krasoty-tati": "Tati",
    "laki-park-dom": "Лаки Парк",
    "ns-akadem-pulsar": "ЖК Пульсар",
    "kvartal-dekabristov": "ЖК Квартал Декабристов",
    "nevskaya-dom": "",
    "vostochny-vayb": "",
    "kedrovy-ns": "ЖК Кедровый",
    "dom-sinegore": "",
    "kabinet-morozovo": "с. Морозово",
    "little-classic": "ЖК Европейский берег",
}

# Падеж для фразы «в …», если именительный ЖК звучит криво.
PROJECT_LOC = {
    "salon-krasoty-tati": "салоне красоты Tati, Новосибирск",
}


def _area_m2(area: str) -> str:
    text = (area or "").replace("кв.м.", "").replace("кв. м.", "").strip()
    return text or area


def project_place(slug: str, city: str) -> str:
    place = PROJECT_PLACE.get(slug, "")
    if place and city and city not in place:
        return f"{place}, {city}"
    if place:
        return place
    return city


def project_seo(cfg: dict) -> tuple[str, str]:
    """Title and description from the published project name, area and rooms."""
    meta = cfg.get("meta") or {}
    ptype = meta.get("type") or ""
    gen = TYPE_GENITIVE.get(ptype, ptype.lower())
    area = _area_m2(str(meta.get("area") or ""))
    city = meta.get("city") or ""
    where = project_place(cfg.get("slug") or "", city)
    title = f"Дизайн {gen} {area} м² — {where} | Key Design Studio"
    if len(title) > 65:
        title = f"Дизайн {gen} {area} м² — {where}"

    slug = cfg.get("slug") or ""
    if slug in PROJECT_LOC:
        loc = PROJECT_LOC[slug]
    elif PROJECT_PLACE.get(slug):
        loc = where
    else:
        loc = CITY_PREPOSITIONAL.get(city, city)
    rooms = []
    for room in cfg.get("rooms") or []:
        if isinstance(room, dict) and room.get("name"):
            rooms.append(room["name"])
    room_list = ", ".join(rooms)
    tail = "Фото реализованного проекта Key Design Studio."
    if room_list:
        desc = f"Дизайн-проект {gen} {area} м² в {loc}: {room_list}. {tail}"
        while len(desc) > 160 and rooms:
            rooms = rooms[:-1]
            room_list = ", ".join(rooms)
            if room_list:
                desc = f"Дизайн-проект {gen} {area} м² в {loc}: {room_list}. {tail}"
            else:
                desc = f"Дизайн-проект {gen} {area} м² в {loc}. {tail}"
    else:
        desc = f"Дизайн-проект {gen} {area} м² в {loc}. {tail}"
    if len(desc) > 160:
        desc = desc[:157].rstrip() + "..."
    return title, desc




def page_url(path: str) -> str:
    if path == "/":
        return f"{SITE_ORIGIN}/"
    return f"{SITE_ORIGIN}{path}"


def absolute_asset(path: str) -> str:
    if path.startswith("http"):
        return path
    return f"{SITE_ORIGIN}/{path.lstrip('/')}"


def seo_block(
    *,
    canonical_path: str,
    title: str,
    description: str,
    og_image: str | None = None,
    noindex: bool = False,
) -> str:
    canonical = page_url(canonical_path)
    image = absolute_asset(og_image or DEFAULT_OG_IMAGE)
    robots = '  <meta name="robots" content="noindex, nofollow" />\n' if noindex else ""
    yandex = (
        f'  <meta name="yandex-verification" content="{html.escape(YANDEX_VERIFICATION, quote=True)}" />\n'
        if YANDEX_VERIFICATION
        else ""
    )
    return (
        f'{robots}'
        f'{yandex}'
        f'  <link rel="canonical" href="{html.escape(canonical, quote=True)}" />\n'
        f'  <meta property="og:type" content="website" />\n'
        f'  <meta property="og:site_name" content="Key Design Studio" />\n'
        f'  <meta property="og:title" content="{html.escape(title, quote=True)}" />\n'
        f'  <meta property="og:description" content="{html.escape(description, quote=True)}" />\n'
        f'  <meta property="og:url" content="{html.escape(canonical, quote=True)}" />\n'
        f'  <meta property="og:image" content="{html.escape(image, quote=True)}" />\n'
        f'  <meta property="og:locale" content="ru_RU" />\n'
        f'  <meta name="twitter:card" content="summary_large_image" />\n'
        f'  <meta name="twitter:title" content="{html.escape(title, quote=True)}" />\n'
        f'  <meta name="twitter:description" content="{html.escape(description, quote=True)}" />\n'
        f'  <meta name="twitter:image" content="{html.escape(image, quote=True)}" />\n'
    )


SEO_TAG_RE = re.compile(
    r"\n?\s*(?:<link rel=\"canonical\"|<meta name=\"robots\"|<meta name=\"yandex-verification\"|<meta property=\"og:|<meta name=\"twitter:)[^\n]*\n?",
    re.IGNORECASE,
)


def strip_existing_seo(text: str) -> str:
    return SEO_TAG_RE.sub("\n", text)



def upsert_title(text: str, title: str) -> str:
    escaped = html.escape(title)
    if re.search(r"<title>", text, re.IGNORECASE):
        return re.sub(
            r"<title>[^<]*</title>",
            f"<title>{escaped}</title>",
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    return text.replace("<head>", f"<head>\n  <title>{escaped}</title>", 1)


def upsert_description(text: str, description: str) -> str:
    escaped = html.escape(description, quote=True)
    if re.search(r'<meta name="description"', text, re.IGNORECASE):
        return re.sub(
            r'<meta name="description" content="[^"]*"\s*/?>',
            f'<meta name="description" content="{escaped}" />',
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    return text.replace(
        '<meta name="viewport"',
        f'<meta name="description" content="{escaped}" />\n  <meta name="viewport"',
        1,
    )


def inject_seo(
    text: str,
    *,
    canonical_path: str,
    title: str,
    description: str,
    og_image: str | None = None,
    noindex: bool = False,
) -> str:
    text = strip_existing_seo(text)
    text = upsert_title(text, title)
    text = upsert_description(text, description)
    block = seo_block(
        canonical_path=canonical_path,
        title=title,
        description=description,
        og_image=og_image,
        noindex=noindex,
    )
    return re.sub(
        r"(<title>[^<]*</title>)",
        r"\1\n" + block,
        text,
        count=1,
        flags=re.IGNORECASE,
    )


def write_robots(path: Path) -> None:
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /oauth/",
            "Disallow: /api/",
            "",
            f"Sitemap: {SITE_ORIGIN}/sitemap.xml",
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")


def write_sitemap(path: Path, urls: list[str]) -> None:
    today = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{html.escape(url, quote=True)}</loc>",
                f"    <lastmod>{today}</lastmod>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
