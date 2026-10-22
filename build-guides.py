#!/usr/bin/env python3
"""Собирает раздел статей: guides/index.html и guides/<slug>.html.

Статьи лежат в content/guides/*.md (фронтматтер + текст).
Файлы, имя которых начинается с «_», в сборку, список и sitemap не попадают.
Посмотреть такой файл локально: python3 build-guides.py --preview
(страница появится только в dist/guides/, следующая сборка dist её сотрёт).
"""

from __future__ import annotations

import html
import re
import sys
from datetime import date
from pathlib import Path

from seo import SITE_ORIGIN, DEFAULT_OG_IMAGE
from site_common import (
    GUIDES_OUT,
    ROOT,
    SERVICE_BY_KEY,
    app_ru,
    guide_files,
    ld_script,
    page_shell,
    parse_guide,
    project_cards,
    provider_ld,
    published_guides,
)

ESC = html.escape
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
FORBIDDEN_MARKS = ("[НУЖНО УТОЧНИТЬ", "[ФОТО")


# ---------------------------------------------------------------- markdown

def _inline(text: str) -> str:
    text = ESC(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)

    def link(match):
        label, url = match.group(1), match.group(2).strip()
        if not (url.startswith("/") or url.startswith("https://") or url.startswith("http://")):
            return match.group(0)
        return f'<a href="{ESC(url, quote=True)}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)


def md_to_html(body: str) -> str:
    out: list[str] = []
    para: list[str] = []
    items: list[str] = []
    list_kind = ""

    def flush_para():
        nonlocal para
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para = []

    def flush_list():
        nonlocal items, list_kind
        if items:
            tag = list_kind or "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + f"</{tag}>")
            items, list_kind = [], ""

    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para()
            flush_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            flush_para()
            flush_list()
            level = 3 if len(heading.group(1)) >= 3 else 2
            out.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            continue
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        numbered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if bullet or numbered:
            flush_para()
            kind = "ul" if bullet else "ol"
            if list_kind and list_kind != kind:
                flush_list()
            list_kind = kind
            items.append((bullet or numbered).group(1))
            continue
        flush_list()
        para.append(line.strip())
    flush_para()
    flush_list()
    return "\n".join(out)


# ---------------------------------------------------------------- страницы

def human_date(value: str) -> str:
    try:
        d = date.fromisoformat(value)
    except ValueError:
        return value
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def check_guide(guide: dict) -> None:
    for mark in FORBIDDEN_MARKS:
        if mark in guide["body"] and not guide["draft"]:
            raise SystemExit(f"Статья {guide['slug']}: в тексте осталась метка {mark}… — публиковать нельзя")
    for key in ("title", "description", "date"):
        if not guide.get(key) and not guide["draft"]:
            raise SystemExit(f"Статья {guide['slug']}: в фронтматтере нет поля {key}")
    if not guide["draft"] and len(str(guide.get("description", ""))) > 160:
        raise SystemExit(f"Статья {guide['slug']}: description длиннее 160 знаков")


def arrow(attrs: str, key: str, text: str) -> str:
    return f'<a {attrs}><span data-i18n="{key}">{ESC(text)}</span> <span class="btn__arrow" aria-hidden="true">→</span></a>'


def article_page(guide: dict, by_slug: dict[str, dict], noindex: bool = False) -> str:
    slug = guide["slug"]
    title = str(guide.get("title") or "Тестовая страница")
    description = str(guide.get("description") or "Тестовая страница раздела статей.")
    path = f"/guides/{slug}"
    url = f"{SITE_ORIGIN}{path}"

    blocks = []
    projects = [p for p in (guide.get("projects") or []) if p]
    if projects:
        blocks.append(
            f"""        <section class="guide__block">
          <h2 class="svc-page__h" data-i18n="guides.project">Как это было в проекте</h2>
          <div class="proj-grid">
{project_cards(projects)}
          </div>
        </section>"""
        )
    service = SERVICE_BY_KEY.get(str(guide.get("service") or ""))
    if service:
        blocks.append(
            f"""        <section class="guide__block">
          <h2 class="svc-page__h" data-i18n="guides.service">Услуга</h2>
          <p><a class="link-underline" href="/{service['slug']}" data-i18n="svc.{service['n']}.title">{ESC(app_ru(f"svc.{service['n']}.title"))}</a></p>
        </section>"""
        )
    faq = [f for f in (guide.get("faq") or []) if isinstance(f, dict) and f.get("q") and f.get("a")]
    if faq:
        items = "\n".join(
            f"""            <div class="faq__item">
              <dt>{ESC(str(f['q']))}</dt>
              <dd>{ESC(str(f['a']))}</dd>
            </div>"""
            for f in faq
        )
        blocks.append(
            f"""        <section class="guide__block">
          <h2 class="svc-page__h" data-i18n="guides.faq">Вопросы и ответы</h2>
          <dl class="faq">
{items}
          </dl>
        </section>"""
        )
    related = [by_slug[s] for s in (guide.get("related") or []) if s in by_slug and s != slug][:2]
    if related:
        links = "\n".join(
            f'            <li><a class="link-underline" href="/guides/{ESC(r["slug"])}">{ESC(str(r["title"]))}</a></li>'
            for r in related
        )
        blocks.append(
            f"""        <section class="guide__block">
          <h2 class="svc-page__h" data-i18n="guides.related">Читайте также</h2>
          <ul class="svc-others">
{links}
          </ul>
        </section>"""
        )
    blocks.append(
        f"""        <section class="guide__block">
          <p class="svc__note" data-i18n="guides.cta">Расскажите метраж и когда планируете начать — заявка на сайте.</p>
          {arrow('href="#brief" class="btn svc__cta" data-open-brief', "svc.cta", "Оставить заявку")}
        </section>"""
    )

    main_html = f"""      <div class="section-head reveal">
        <div>
          <p class="eyebrow"><a href="/guides" data-i18n="nav.guides">Статьи</a></p>
          <h1 class="svc__title svc-page__title">{ESC(title)}</h1>
        </div>
        {arrow('href="/guides" class="link-underline"', "guides.back", "Все статьи")}
      </div>

      <article class="guide reveal">
        <p class="guide__date">{ESC(human_date(guide['date']))}</p>
        <div class="proj-story guide__body">
{md_to_html(guide['body'])}
        </div>
{chr(10).join(blocks)}
      </article>"""

    ld = [
        ld_script(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "description": description,
                "datePublished": guide["date"],
                "mainEntityOfPage": url,
                "image": DEFAULT_OG_IMAGE,
                "author": provider_ld(),
                "publisher": provider_ld(),
            }
        ),
        ld_script(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE_ORIGIN}/"},
                    {"@type": "ListItem", "position": 2, "name": "Статьи", "item": f"{SITE_ORIGIN}/guides"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": url},
                ],
            }
        ),
    ]
    return page_shell(
        title=f"{title} — Key Design Studio" if len(title) <= 40 else title,
        description=description,
        canonical_path=path,
        main_html=main_html,
        extra_head="\n".join(ld),
        noindex=noindex,
        nested=True,
    )


def list_page(guides: list[dict]) -> str:
    path = "/guides"
    title = "Статьи о дизайне интерьера — Key Design Studio"
    description = "Статьи Key Design Studio о том, как устроены дизайн-проект, комплектация и авторский надзор при ремонте."
    if guides:
        items = "\n".join(
            f"""          <li class="guides-list__item">
            <a href="/guides/{ESC(g['slug'])}">
              <span class="guides-list__title">{ESC(str(g['title']))}</span>
              <span class="guides-list__lead">{ESC(str(g['description']))}</span>
            </a>
          </li>"""
            for g in guides
        )
        body = f'      <ul class="guides-list reveal">\n{items}\n      </ul>'
    else:
        body = '      <p class="guides-soon reveal" data-i18n="guides.soon">Первые статьи скоро появятся</p>'
    main_html = f"""      <div class="section-head reveal">
        <div>
          <h1 class="eyebrow" data-i18n="guides.title">Статьи</h1>
        </div>
        {arrow('href="/" class="link-underline"', "nav.home", "На главную")}
      </div>
{body}"""
    return page_shell(
        title=title,
        description=description,
        canonical_path=path,
        main_html=main_html,
        noindex=not guides,
        nested=True,
    )


def main() -> int:
    preview = "--preview" in sys.argv
    guides = published_guides()
    for g in guides:
        check_guide(g)
    by_slug = {g["slug"]: g for g in guides}

    if preview:
        out_dir = ROOT / "dist" / "guides"
        out_dir.mkdir(parents=True, exist_ok=True)
        for path in guide_files(include_drafts=True):
            guide = parse_guide(path)
            if not guide["draft"]:
                continue
            by = dict(by_slug)
            (out_dir / f"{path.stem}.html").write_text(article_page(guide, by, noindex=True), encoding="utf-8")
            print(f"  preview → dist/guides/{path.stem}.html  (адрес /guides/{path.stem})")
        return 0

    GUIDES_OUT.mkdir(exist_ok=True)
    wanted = {"index.html"}
    (GUIDES_OUT / "index.html").write_text(list_page(guides), encoding="utf-8")
    print(f"Guides: index.html ({'заглушка, noindex' if not guides else str(len(guides)) + ' статей'})")
    for guide in guides:
        name = f"{guide['slug']}.html"
        wanted.add(name)
        (GUIDES_OUT / name).write_text(article_page(guide, by_slug), encoding="utf-8")
        print(f"  → guides/{name}")
    for old in GUIDES_OUT.glob("*.html"):
        if old.name not in wanted and " " not in old.name:
            try:
                old.unlink()
                print(f"  removed stale guides/{old.name}")
            except OSError:
                print(f"  ! не смог удалить guides/{old.name} — удалите вручную")
    return 0


if __name__ == "__main__":
    sys.exit(main())
