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

STATIC_PAGES: dict[str, dict[str, str]] = {
    "/": {
        "file": "index.html",
        "title": "Key Design Studio - студия интерьерного дизайна",
        "description": (
            "Key Design Studio - студия интерьерного дизайна в Новосибирске. "
            "Жилые и коммерческие интерьеры: от концепции до реализации. "
            "Проекты в Новосибирске, Москве и Дубае."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/about": {
        "file": "about.html",
        "title": "О студии",
        "description": (
            "Key Design Studio - студия интерьерного дизайна в Новосибирске. "
            "Авторские интерьеры квартир, домов и коммерческих пространств."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/projects": {
        "file": "projects.html",
        "title": "Проекты",
        "description": (
            "Проекты Key Design Studio - жилые и коммерческие интерьеры "
            "в Новосибирске, Москве и других городах."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/services": {
        "file": "services.html",
        "title": "Услуги",
        "description": (
            "Услуги Key Design Studio в Новосибирске: дизайн-проект интерьера, "
            "менеджмент, авторский надзор, архитектурное планирование."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/contacts": {
        "file": "contacts.html",
        "title": "Контакты",
        "description": (
            "Контакты Key Design Studio в Новосибирске - телефон, почта, "
            "Telegram, Instagram и адрес офиса на ул. Инженерная 7."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
    "/privacy": {
        "file": "privacy.html",
        "title": "Политика конфиденциальности",
        "description": (
            "Политика конфиденциальности Key Design Studio - обработка "
            "персональных данных на сайте."
        ),
        "og_image": DEFAULT_OG_IMAGE,
    },
}

PROD_HIDDEN = {"approach.html", "partners.html"}
NOINDEX_FILES = {"approach.html", "partners.html", "key-design-studio.html"}


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
    return (
        f'{robots}'
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
    r"\n?\s*(?:<link rel=\"canonical\"|<meta name=\"robots\"|<meta property=\"og:|<meta name=\"twitter:)[^\n]*\n?",
    re.IGNORECASE,
)


def strip_existing_seo(text: str) -> str:
    return SEO_TAG_RE.sub("\n", text)


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
