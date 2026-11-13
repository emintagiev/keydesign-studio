#!/usr/bin/env python3
"""Собирает раздел статей: guides/index.html и guides/<slug>.html.

Статьи лежат в content/guides/*.md (фронтматтер + текст).
Файлы, имя которых начинается с «_», в сборку, список и sitemap не попадают.
Посмотреть такой файл локально: python3 build-guides.py --preview
(страница появится только в dist/guides/, следующая сборка dist её сотрёт).
"""

from __future__ import annotations

import html
import json
import math
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
    bp,
)

ESC = html.escape
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
FORBIDDEN_MARKS = ("[НУЖНО УТОЧНИТЬ", "[ФОТО", "[CHECK WITH KRISTINA")


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
    heading_number = 0

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
            heading_number += 1
            out.append(f'<h{level} id="part-{heading_number}">{_inline(heading.group(2))}</h{level}>')
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
        if mark in json.dumps(guide, ensure_ascii=False) and not guide["draft"]:
            raise SystemExit(f"Статья {guide['slug']}: в тексте осталась метка {mark}… — публиковать нельзя")
    for key in ("title", "description", "date"):
        if not guide.get(key) and not guide["draft"]:
            raise SystemExit(f"Статья {guide['slug']}: в фронтматтере нет поля {key}")
    if not guide["draft"] and len(str(guide.get("description", ""))) > 160:
        raise SystemExit(f"Статья {guide['slug']}: description длиннее 160 знаков")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", guide["slug"]):
        raise SystemExit(f"Некорректный адрес статьи: {guide['slug']}")
    if guide.get("date"):
        date.fromisoformat(guide["date"])
    if guide.get("service") and guide["service"] not in SERVICE_BY_KEY:
        raise SystemExit(f"Неизвестная услуга в статье {guide['slug']}")
    cover_data(guide)


def cover_data(guide: dict) -> dict:
    image = guide.get("cover_image")
    if image:
        for key in ("cover_image", "cover_thumbnail"):
            path = guide.get(key)
            if not isinstance(path, str) or not path.startswith("assets/guides/"):
                raise SystemExit(f"Статья {guide['slug']}: {key} должен быть файлом в assets/guides/")
            resolved = (ROOT / path).resolve()
            if not resolved.is_relative_to((ROOT / "assets" / "guides").resolve()) or not resolved.is_file():
                raise SystemExit(f"Статья {guide['slug']}: нет файла {key}")
        if not guide.get("cover_alt") or not guide.get("cover_caption"):
            raise SystemExit(f"Статья {guide['slug']}: отдельной обложке нужны alt и подпись")
        for key in ("cover_width", "cover_height"):
            if not isinstance(guide.get(key), int) or guide[key] <= 0:
                raise SystemExit(f"Статья {guide['slug']}: неверный размер {key}")
        return {"cover": image, "title_plain": guide["cover_alt"]}
    slug = guide.get("cover_project")
    if not slug:
        return {}
    project = next((p for p in bp().load_projects() if p["slug"] == slug), None)
    if not project or not (ROOT / project["cover"]).is_file():
        raise SystemExit(f"Нет обложки проекта {slug}")
    return project


def read_minutes(guide: dict) -> int:
    return max(1, math.ceil(len(guide["body"].split()) / 180))


def cover_picture(guide: dict, *, preview: bool = False) -> str:
    project = cover_data(guide)
    if not project:
        return ""
    if guide.get("cover_image"):
        full = "/" + ESC(guide["cover_image"], quote=True)
        thumb = "/" + ESC(guide["cover_thumbnail"], quote=True)
        alt = ESC(guide["cover_alt"], quote=True)
        width, height = guide["cover_width"], guide["cover_height"]
        loading = 'loading="lazy"' if preview else 'fetchpriority="high"'
        sizes = '(max-width: 640px) 100vw, (max-width: 960px) 50vw, 33vw' if preview else '(max-width: 960px) 100vw, 960px'
        webp_full = Path(guide["cover_image"]).with_suffix(".webp")
        webp_thumb = Path(guide["cover_thumbnail"]).with_suffix(".webp")
        source = ""
        if (ROOT / webp_full).is_file() and (ROOT / webp_thumb).is_file():
            source = (f'<source type="image/webp" srcset="/{ESC(str(webp_thumb))} 800w, '
                      f'/{ESC(str(webp_full))} {width}w" sizes="{sizes}" />')
        return (f'<picture>{source}<img src="{thumb if preview else full}" '
                f'srcset="{thumb} 800w, {full} {width}w" sizes="{sizes}" '
                f'alt="{alt}" width="{width}" height="{height}" {loading} decoding="async" /></picture>')
    return bp().render_picture(project["cover"], guide.get("cover_alt") or project["title_plain"],
                               preview=preview, lazy=preview)


def cards_html(guides: list[dict]) -> str:
    cards = []
    for g in guides:
        cards.append(f'''<li class="guide-card" lang="{ESC(g.get('lang', 'ru'))}">
          <a href="/guides/{ESC(g['slug'])}">
            <div class="guide-card__image">{cover_picture(g, preview=True)}</div>
            <span class="guide-card__meta">{ESC(g.get('category', 'Дизайн интерьера'))} · {read_minutes(g)} мин</span>
            <h2 class="guide-card__title">{ESC(g['title'])}</h2>
            <p>{ESC(g.get('lead') or g['description'])}</p>
            <span class="guide-card__link">Читать статью <span aria-hidden="true">→</span></span>
          </a>
        </li>''')
    return '<ul class="guide-cards">' + '\n'.join(cards) + '</ul>'


def update_home(guides: list[dict]) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    block = ""
    if guides:
        block = f'''<!-- GUIDES_HOME_START -->
    <section class="home-guides section" aria-labelledby="home-guides-title" lang="ru">
      <div class="container">
        <div class="section-head">
          <div><p class="eyebrow">Перед началом ремонта</p>
          <h2 class="section-head__subtitle" id="home-guides-title">От первых вопросов к своему интерьеру</h2></div>
          <a class="link-underline" href="/guides">Все статьи →</a>
        </div>
        {cards_html(guides[:3])}
      </div>
    </section>
    <!-- GUIDES_HOME_END -->'''
    pattern = r"<!-- GUIDES_HOME_START -->.*?<!-- GUIDES_HOME_END -->"
    updated = re.sub(pattern, lambda _: block, text, flags=re.S) if re.search(pattern, text, re.S) else text.replace("</main>", block + "\n  </main>", 1)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


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
          <h2 class="svc-page__h">Работы студии</h2>
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
          <p class="svc__note" data-i18n="guides.cta">Расскажите метраж и когда планируете начать - обсудим ваш проект.</p>
          {arrow('href="#brief" class="btn svc__cta" data-open-brief', "svc.cta", "Оставить заявку")}
        </section>"""
    )

    headings = re.findall(r"^#{1,3}\s+(.+)$", guide["body"], re.M)
    toc = '<nav class="guide-toc" aria-label="Содержание статьи"><p class="eyebrow">В этой статье</p><ol>' + ''.join(
        f'<li><a href="#part-{i}">{ESC(h)}</a></li>' for i, h in enumerate(headings, 1)
    ) + '</ol></nav>' if headings else ''
    project = cover_data(guide)
    caption = ESC(guide.get('cover_caption') or project.get('title_plain', ''))
    if project.get('slug'):
        caption = f'<a href="/{ESC(project["slug"])}">{caption} →</a>'
    photo = f'''<figure class="guide-cover">{cover_picture(guide)}
      <figcaption>{caption}</figcaption></figure>''' if project else ''
    lead = f'<p class="guide-lead">{ESC(guide["lead"])}</p>' if guide.get("lead") else ''
    main_html = f"""      <div class="section-head guide-heading reveal" lang="ru">
        <div>
          <p class="eyebrow"><a href="/guides" data-i18n="nav.guides">Статьи</a></p>
          <h1 class="svc__title svc-page__title">{ESC(title)}</h1>
        </div>
        {arrow('href="/guides" class="link-underline"', "guides.back", "Все статьи")}
      </div>

      <article class="guide reveal" lang="{ESC(guide.get('lang', 'ru'))}">
        <p class="guide__date"><time datetime="{ESC(guide['date'])}">{ESC(human_date(guide['date']))}</time> · {read_minutes(guide)} мин</p>
        {lead}
        <p class="guide-byline">Key Design Studio · По материалам Кристины Парыгиной, основателя студии</p>
        {photo}
        {toc}
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
                "image": f"{SITE_ORIGIN}/{project['cover']}" if project else DEFAULT_OG_IMAGE,
                "inLanguage": guide.get("lang", "ru"),
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
        og_image=project.get("cover") if project else None,
        noindex=noindex,
        nested=True,
    )


def list_page(guides: list[dict]) -> str:
    path = "/guides"
    title = "Статьи о дизайне интерьера — Key Design Studio"
    description = "Статьи Key Design Studio о том, как устроены дизайн-проект, комплектация и авторский надзор при ремонте."
    if guides:
        body = '<div class="guides-intro" lang="ru"><h2>Интерьер начинается<br>с понятных решений</h2><p>О проекте, бюджете и реализации. Объясняем, что предстоит выбрать и как устроена работа со студией.</p></div>' + cards_html(guides)
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
    if len(by_slug) != len(guides):
        raise SystemExit("Повторяющиеся адреса статей")
    for g in guides:
        for slug in g.get("related", []):
            if slug not in by_slug:
                raise SystemExit(f"Статья {g['slug']} ссылается на отсутствующую статью {slug}")

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
    update_home(guides)
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
