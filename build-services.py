#!/usr/bin/env python3
"""Собирает четыре страницы услуг: /uslugi-*.html (корень сайта)."""

from __future__ import annotations

import html
import sys
from pathlib import Path

from seo import SITE_ORIGIN, STATIC_PAGES
import site_i18n as t
from site_common import (
    SERVICES,
    app_ru,
    ld_script,
    page_shell,
    project_cards,
    provider_ld,
    published_guides,
)

ROOT = Path(__file__).resolve().parent
ESC = html.escape


def step_keys(n: int) -> list[int]:
    keys = []
    for k in range(1, 10):
        try:
            app_ru(f"svc.{n}.s{k}.title")
        except KeyError:
            continue
        keys.append(k)
    return keys


def arrow_link(attrs: str, key: str, text: str) -> str:
    return f'<a {attrs}><span data-i18n="{key}">{ESC(text)}</span> <span class="btn__arrow" aria-hidden="true">→</span></a>'


def build_page(service: dict) -> tuple[str, str]:
    n = service["n"]
    title_key = f"svc.{n}.pageTitle" if f"svc.{n}.pageTitle" in t.RU else f"svc.{n}.title"
    name = app_ru(title_key)
    design = service["key"] == "design"
    lead_key = "svc.1.pageLead" if design else f"svc.{n}.lead"
    lead = app_ru(lead_key)
    cost = t.RU[service["cost_key"]]
    price_actions = arrow_link('href="#brief" class="btn svc__cta" data-open-brief', "svc.cta", "Оставить заявку")
    if design:
        contact = arrow_link(
            'href="https://t.me/Kristina_Key_des" class="link-underline svc__cta" data-service-price-contact target="_blank" rel="noopener noreferrer"',
            "svc.askKristina", t.RU["svc.askKristina"],
        )
        price_actions += "\n        " + contact

    steps = []
    for k in step_keys(n):
        title = app_ru(f"svc.{n}.s{k}.title")
        text = app_ru(f"svc.{n}.s{k}.text")
        steps.append(
            f"""          <div class="svc__step">
            <h3 class="svc__step-title" data-i18n="svc.{n}.s{k}.title">{ESC(title)}</h3>
            <p class="svc__step-text" data-i18n="svc.{n}.s{k}.text">{ESC(text)}</p>
          </div>"""
        )

    faq = []
    for k in (1, 2, 3, 4):
        q = t.RU[f"svc.{n}.faq.{k}.q"]
        a = t.RU[f"svc.{n}.faq.{k}.a"]
        faq.append(
            f"""          <div class="faq__item">
            <dt data-i18n="svc.{n}.faq.{k}.q">{ESC(q)}</dt>
            <dd data-i18n="svc.{n}.faq.{k}.a">{ESC(a)}</dd>
          </div>"""
        )

    others = []
    for other in SERVICES:
        if other["n"] == n:
            continue
        o_n = other["n"]
        o_name = ESC(app_ru("svc.%d.title" % o_n))
        others.append(
            '          <li><a class="link-underline" href="/%s" data-i18n="svc.%d.title">%s</a></li>'
            % (other["slug"], o_n, o_name)
        )

    portfolio_key = "svc.1.portfolio" if design else "svc.portfolio"
    portfolio_note = "" if design else f'\n        <p class="svc__note" data-i18n="svc.portfolioNote">{ESC(t.RU["svc.portfolioNote"])}</p>'
    portfolio = f"""        <h2 class="svc-page__h" data-i18n="{portfolio_key}">{ESC(t.RU[portfolio_key])}</h2>{portfolio_note}
        <div class="proj-grid">
{project_cards(service["projects"])}
        </div>"""
    portfolio_after_price = "\n\n" + portfolio if design else ""
    portfolio_after_steps = "" if design else "\n\n" + portfolio

    main_html = f"""      <div class="section-head reveal">
        <div>
          <p class="eyebrow"><a href="/services" data-i18n="nav.services">Услуги</a></p>
          <h1 class="svc__title svc-page__title" data-i18n="{title_key}">{ESC(name)}</h1>
        </div>
        {arrow_link('href="/services" class="link-underline"', "svc.all", "Все услуги")}
      </div>

      <div class="svc-page reveal">
        <p class="svc__lead svc-page__lead" data-i18n="{lead_key}">{ESC(lead)}</p>
        <p class="svc__note" data-i18n="{service["cost_key"]}">{ESC(cost)}</p>
        {price_actions}{portfolio_after_price}

        <h2 class="svc-page__h" data-i18n="svc.conditions">Условия работы</h2>
        <ul class="svc-conditions">
          <li data-i18n="svc.{n}.condition.1">{ESC(t.RU[f"svc.{n}.condition.1"])}</li>
          <li data-i18n="svc.{n}.condition.2">{ESC(t.RU[f"svc.{n}.condition.2"])}</li>
        </ul>

        <h2 class="svc-page__h" data-i18n="svc.how">Как проходит работа</h2>
        <div class="svc__steps">
{chr(10).join(steps)}
        </div>
        {arrow_link('href="#brief" class="btn svc__cta" data-open-brief', "svc.cta", "Оставить заявку")}{portfolio_after_steps}

        <h2 class="svc-page__h" data-i18n="svc.faqTitle">Вопросы и ответы</h2>
        <dl class="faq">
{chr(10).join(faq)}
        </dl>

        <h2 class="svc-page__h" data-i18n="svc.others">Другие услуги</h2>
        <ul class="svc-others">
{chr(10).join(others)}
        </ul>
      </div>"""

    reading = [g for g in published_guides() if g.get("service") == service["key"]]
    if reading:
        links = ''.join(f'<li><a class="link-underline" href="/guides/{ESC(g["slug"])}">{ESC(g["title"])}</a></li>' for g in reading)
        main_html += f'<section class="svc-reading" lang="ru"><h2 class="svc-page__h">Перед началом работы</h2><ul class="svc-others">{links}</ul></section>'

    main_html += f'''<section class="svc-next">
      <h2 class="svc-page__h" data-i18n="svc.next">{ESC(t.RU['svc.next'])}</h2>
      <p data-i18n="svc.nextText">{ESC(t.RU['svc.nextText'])}</p>
      {arrow_link('href="#brief" class="btn" data-open-brief', 'svc.cta', 'Оставить заявку')}
    </section>'''

    path = f"/{service['slug']}"
    meta = STATIC_PAGES[path]
    title, description = meta["title"], meta["description"]
    url = f"{SITE_ORIGIN}{path}"
    ld = [
        ld_script(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": name,
                "serviceType": name,
                "description": lead,
                "url": url,
                "provider": provider_ld(),
                "areaServed": [{"@type": "City", "name": city} for city in ("Новосибирск", "Москва", "Дубай")],
            }
        ),
        ld_script(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE_ORIGIN}/"},
                    {"@type": "ListItem", "position": 2, "name": "Услуги", "item": f"{SITE_ORIGIN}/services"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": url},
                ],
            }
        ),
    ]
    page = page_shell(
        title=title,
        description=description,
        canonical_path=path,
        main_html=main_html,
        og_image=meta["og_image"],
        extra_head="\n".join(ld),
        active="services",
    )
    return f"{service['slug']}.html", page


def main() -> int:
    print("Service pages:")
    for service in SERVICES:
        name, page = build_page(service)
        meta = STATIC_PAGES[f"/{service['slug']}"]
        title, description = meta["title"], meta["description"]
        assert len(title) <= 65, (title, len(title))
        assert len(description) <= 160, (description, len(description))
        (ROOT / name).write_text(page, encoding="utf-8")
        print(f"  → {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
