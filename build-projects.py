#!/usr/bin/env python3
"""Copy original images and generate project pages from Desktop folders."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
PROJECTS_DIR = CONTENT_DIR / "projects"
DESKTOP = Path.home() / "Desktop"
KEY_DESIGN = DESKTOP / "key design"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
ASSET_JS_VERSION = "25"
ASSET_CSS_VERSION = "66"

HEADER = """  <header class="header" id="header">
    <div class="container header__inner">
      <a href="key-design-studio.html" class="brand" aria-label="Key Design Studio">
        <img class="brand__logo brand__logo--dark" src="assets/logo.png?v=11" alt="" width="859" height="722" />
        <img class="brand__logo brand__logo--light" src="assets/logo-light.png?v=11" alt="" width="859" height="722" />
      </a>

      <nav class="nav" id="nav" aria-label="Основная навигация">
        <a class="nav__link" href="about.html" data-i18n="nav.about">О студии</a>
        <a class="nav__link" href="projects.html" data-i18n="nav.projects">Проекты</a>
        <a class="nav__link" href="services.html" data-i18n="nav.services">Услуги</a>
        <a class="nav__link" href="approach.html" data-i18n="nav.approach">Подход</a>
        <a class="nav__link" href="partners.html" data-i18n="nav.partners">Партнёры</a>
        <a class="nav__link" href="contacts.html" data-i18n="nav.contact">Контакты</a>
      </nav>

      <div class="header__tools">
        <button class="nav-toggle" type="button" id="navToggle" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div class="header-social">
          <a class="header-social__link" href="https://t.me/Kristina_Key_des" target="_blank" rel="noopener noreferrer" aria-label="Telegram">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2 11 13"/><path d="m22 2-7 20-4-9-9-4 20-7z"/></svg>
          </a>
          <a class="header-social__link" href="https://instagram.com/key_design.studio" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          </a>
        </div>

        <div class="lang" role="group" aria-label="Выбор языка / Language">
          <button class="lang__btn" type="button" data-lang="ru" aria-pressed="true">RU</button>
          <button class="lang__btn" type="button" data-lang="en" aria-pressed="false">EN</button>
        </div>
      </div>
    </div>
  </header>"""

FOOTER = """  <footer class="footer">
    <div class="container footer__inner">
      <span class="footer__brand">Key Design Studio</span>
      <span class="footer__meta">
        © <span id="year"></span> Key Design Studio. <span data-i18n="footer.rights">Все права защищены.</span>
      </span>
      <a href="privacy.html" class="footer__link" data-i18n="footer.privacy">Политика конфиденциальности</a>
    </div>
  </footer>"""

JS_BOOTSTRAP = """  <script>document.documentElement.classList.add("js");</script>
"""

HOME_LINK = """        <a href="key-design-studio.html" class="link-underline" data-i18n="nav.home">
          На главную <span class="btn__arrow" aria-hidden="true">→</span>
        </a>"""

FAVICON_LINKS = """  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png?v=1" />
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png?v=1" />"""


def load_site_config() -> dict:
    path = CONTENT_DIR / "site.yaml"
    if not path.exists():
        return {"featured_slugs": [], "projects_order": []}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_projects() -> list[dict]:
    site = load_site_config()
    order = site.get("projects_order") or []
    order_index = {slug: i for i, slug in enumerate(order)}

    projects = []
    for path in sorted(PROJECTS_DIR.glob("*.yaml")):
        with path.open(encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        if not cfg.get("published", True):
            continue
        cfg.setdefault("slug", path.stem)
        cfg["html"] = f"{cfg['slug']}.html"
        projects.append(cfg)

    projects.sort(
        key=lambda p: (
            order_index.get(p["slug"], 9999),
            p.get("sort_order", 9999),
            p["slug"],
        )
    )
    for cfg in projects:
        enrich_project(cfg)
    return projects


def title_html_from_plain(title: str, existing=None) -> str:
    if existing and "<em>" in (existing or ""):
        return existing
    if ", " in title:
        head, tail = title.rsplit(", ", 1)
        return f"{head}, <em>{tail}</em>"
    words = title.split()
    if len(words) >= 2:
        return " ".join(words[:-1]) + f" <em>{words[-1]}</em>"
    return title


def enrich_project(cfg: dict) -> None:
    title = (cfg.get("title_plain") or "").strip()
    if not title:
        return

    meta = cfg.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        cfg["meta"] = meta

    meta.setdefault("type", "-")
    meta.setdefault("city", "-")
    meta.setdefault("area", "-")
    meta.setdefault("year", str(meta.get("year") or "2026"))

    year = meta.get("year", "2026")
    city = meta.get("city", "-")
    ptype = meta.get("type", "-")

    cfg["title_html"] = title_html_from_plain(title, cfg.get("title_html"))
    cfg["carousel_name"] = title
    cfg["description"] = f"{title} - проект Key Design Studio."
    cfg.setdefault("eyebrow", cfg.get("eyebrow") or "")
    cfg.setdefault("lead", cfg.get("lead") or "")
    cfg["grid_city"] = cfg.get("grid_city") or city
    if not cfg.get("carousel_cat"):
        parts = [p for p in (ptype, city, year) if p and p != "-"]
        cfg["carousel_cat"] = " · ".join(parts) if parts else title

    gallery = cfg.get("gallery") or []
    if gallery and not cfg.get("rooms"):
        paths = []
        for item in gallery:
            if isinstance(item, str):
                paths.append(item)
            elif isinstance(item, dict):
                paths.append(item.get("image") or item.get("path") or "")
        paths = [p for p in paths if p]
        if paths:
            cover_name = Path(paths[0]).name
            cfg["rooms"] = [{"slug": "photos", "name": "Фотографии", "cover_filename": cover_name}]
    elif not cfg.get("rooms") and cfg.get("cover"):
        cover_path = cfg["cover"]
        cover_name = Path(cover_path).name
        room_slug = Path(cover_path).parent.name
        if room_slug in ("projects", "assets", cfg.get("slug", "")):
            room_slug = "interior"
        cfg["rooms"] = [{"slug": room_slug, "name": "Интерьер", "cover_filename": cover_name}]


def gallery_image_paths(cfg: dict) -> list[str]:
    gallery = cfg.get("gallery") or []
    if not gallery:
        return []

    paths = []
    for item in gallery:
        if isinstance(item, str):
            paths.append(item)
        elif isinstance(item, dict):
            paths.append(item.get("image") or item.get("path") or "")
    paths = [p for p in paths if p]
    cover = cfg.get("cover")
    if cover and cover not in paths:
        paths.insert(0, cover)
    return paths

def sync_site_projects_order(projects: list[dict]) -> None:
    path = CONTENT_DIR / "site.yaml"
    site = load_site_config()
    ordered = sorted(projects, key=lambda p: p.get("sort_order", 9999))
    site["projects_order"] = [p["slug"] for p in ordered]
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(site, f, allow_unicode=True, sort_keys=False, default_flow_style=False)




def kadr(n: int) -> str:
    if 11 <= n % 100 <= 14:
        return "кадров"
    d = n % 10
    if d == 1:
        return "кадр"
    if 2 <= d <= 4:
        return "кадра"
    return "кадров"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-"))


def natural_sort_key(name: str):
    parts = re.split(r"(\d+)", name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


ROOT_ROOM = "__root__"


def copy_root_images(src_dir: Path, dest_dir: Path) -> list[str]:
    files = sorted(
        [f for f in src_dir.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTS],
        key=lambda p: natural_sort_key(p.name),
    )
    names = []
    for f in files:
        out = dest_dir / f.name
        copy_image_original(f, out)
        names.append(out.name)
    return names


def sync_rooms_from_config(cfg: dict):
    rooms = cfg.get("rooms")
    if rooms and isinstance(rooms[0], dict):
        cfg["rooms"] = [(r["slug"], r["name"], r["cover_filename"]) for r in rooms]
    elif "room_map" in cfg:
        cfg["rooms"] = [(room_slug, name, cover) for _, room_slug, name, cover in cfg["room_map"]]
    elif "flat_room" in cfg:
        room_slug, name, cover = cfg["flat_room"]
        cfg["rooms"] = [(room_slug, name, cover)]


def copy_image_original(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_room_folder(src_dir: Path, dest_dir: Path) -> list[str]:
    files = sorted(
        [f for f in src_dir.iterdir() if f.suffix.lower() in IMAGE_EXTS],
        key=lambda p: natural_sort_key(p.name),
    )
    names = []
    for f in files:
        out = dest_dir / f.name
        copy_image_original(f, out)
        names.append(out.name)
    return names


def copy_flat_folder(src_dir: Path, dest_slug: str, room_slug: str) -> list[str]:
    dest_dir = ROOT / "assets" / "projects" / dest_slug / room_slug
    files = sorted(
        [f for f in src_dir.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTS],
        key=lambda p: natural_sort_key(p.stem),
    )
    names = []
    for f in files:
        out = dest_dir / f.name
        copy_image_original(f, out)
        names.append(out.name)
    return names


def list_images(slug: str, room_slug: str) -> list[str]:
    d = ROOT / "assets" / "projects" / slug / room_slug
    if not d.exists():
        return []
    return sorted(
        [f.name for f in d.iterdir() if f.suffix.lower() in IMAGE_EXTS],
        key=natural_sort_key,
    )


def ingest_hero():
    src = DESKTOP / "фото главной.JPG"
    if not src.exists():
        print("  ! hero source not found, skipping")
        return
    dst = ROOT / "assets" / "hero-main.jpg"
    copy_image_original(src, dst)
    print(f"  → hero-main.jpg ({src.stat().st_size // 1024} KB original)")


def ingest_project(cfg: dict):
    if not cfg.get("source"):
        sync_rooms_from_config(cfg)
        return

    src = cfg["source"]
    slug = cfg["slug"]
    out_base = ROOT / "assets" / "projects" / slug

    if not src.exists():
        if out_base.exists():
            print(f"  ! source missing, keeping existing assets for {cfg['title_plain']}")
            sync_rooms_from_config(cfg)
            return
        raise FileNotFoundError(f"Source not found: {src}")

    if out_base.exists():
        shutil.rmtree(out_base)

    if "room_map" in cfg:
        cfg["rooms"] = []
        for folder, room_slug, name, cover in cfg["room_map"]:
            if folder == ROOT_ROOM:
                copy_root_images(src, out_base / room_slug)
            else:
                copy_room_folder(src / folder, out_base / room_slug)
            cfg["rooms"].append((room_slug, name, cover))
    elif "flat_room" in cfg:
        room_slug, name, cover = cfg["flat_room"]
        copy_flat_folder(src, slug, room_slug)
        cfg["rooms"] = [(room_slug, name, cover)]


def build_cards_and_views(cfg: dict) -> tuple[str, str]:
    slug = cfg["slug"]
    cards = []
    views = []

    for room_slug, name, cover in cfg["rooms"]:
        imgs = list_images(slug, room_slug)
        n = len(imgs)
        cover_path = f"assets/projects/{slug}/{room_slug}/{cover}"
        if cover not in imgs and imgs:
            cover_path = f"assets/projects/{slug}/{room_slug}/{imgs[0]}"

        cards.append(
            f'''          <button class="room-card" type="button" data-room="{room_slug}">
            <span class="room-card__media">
              <img src="{cover_path}" alt="{name}" loading="lazy" />
            </span>
            <span class="room-card__label">
              <span class="room-card__name">{name}</span>
              <span class="room-card__count">{n} {kadr(n)}</span>
            </span>
          </button>'''
        )

        figs = []
        for img in imgs:
            src = f"assets/projects/{slug}/{room_slug}/{img}"
            figs.append(
                f"              <figure>\n"
                f'                <img src="{src}" data-full="{src}" alt="{name} - Key Design Studio" loading="lazy" />\n'
                f"              </figure>"
            )

        views.append(
            f'''      <section class="room-view" id="view-{room_slug}" aria-label="{name}">
        <div class="room-view__head">
          <button class="room-back" type="button" data-back>← Все комнаты</button>
          <h2 class="room-view__title">{name}</h2>
          <span class="room-view__count">{n} {kadr(n)}</span>
        </div>
        <div class="room-stage">
          <button class="gallery-arrow gallery-arrow--prev" type="button" data-dir="prev" aria-label="Предыдущее фото">‹</button>
          <div class="proj-gallery">
{chr(10).join(figs)}
          </div>
          <button class="gallery-arrow gallery-arrow--next" type="button" data-dir="next" aria-label="Следующее фото">›</button>
        </div>
      </section>'''
        )

    return "\n".join(cards), "\n\n".join(views)


def build_single_gallery(cfg: dict) -> str:
    slug = cfg["slug"]
    room_slug, name, _cover = cfg["rooms"][0]
    figs = []
    yaml_paths = gallery_image_paths(cfg)
    if yaml_paths:
        for src in yaml_paths:
            figs.append(
                f"              <figure>\n"
                f'                <img src="{src}" data-full="{src}" alt="{name} - Key Design Studio" loading="lazy" />\n'
                f"              </figure>"
            )
        return "\n".join(figs)

    for img in list_images(slug, room_slug):
        src = f"assets/projects/{slug}/{room_slug}/{img}"
        figs.append(
            f"              <figure>\n"
            f'                <img src="{src}" data-full="{src}" alt="{name} - Key Design Studio" loading="lazy" />\n'
            f"              </figure>"
        )
    return "\n".join(figs)


def generate_html(cfg: dict):
    cards, views = build_cards_and_views(cfg)
    is_single = len(cfg["rooms"]) == 1

    if is_single:
        gallery = build_single_gallery(cfg)
        main_block = f'''  <main id="top" class="project-main project-single">
    <div class="container">
      <div class="proj-head">
        <div>
          <p class="eyebrow proj-head__eyebrow">{cfg["eyebrow"]}</p>
          <h1 class="proj-head__title">{cfg["title_html"]}</h1>
        </div>
{HOME_LINK}
      </div>

      <section class="project-gallery" aria-label="Фотографии проекта">
        <div class="room-stage">
          <button class="gallery-arrow gallery-arrow--prev" type="button" data-dir="prev" aria-label="Предыдущее фото">‹</button>
          <div class="proj-gallery">
{gallery}
          </div>
          <button class="gallery-arrow gallery-arrow--next" type="button" data-dir="next" aria-label="Следующее фото">›</button>
        </div>
      </section>

      <div class="proj-foot">
        <a class="proj-foot__cta" href="contacts.html">Обсудить <em>ваш проект</em></a>
        <a class="link-underline" href="projects.html">
          Все проекты <span class="btn__arrow" aria-hidden="true">→</span>
        </a>
      </div>
    </div>

    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Просмотр фотографии">
      <button class="lb-btn lightbox__close" type="button" aria-label="Закрыть">×</button>
      <button class="lb-btn lightbox__nav lightbox__nav--prev" type="button" aria-label="Предыдущее фото">←</button>
      <img class="lightbox__img" src="" alt="" />
      <button class="lb-btn lightbox__nav lightbox__nav--next" type="button" aria-label="Следующее фото">→</button>
      <span class="lightbox__counter"></span>
    </div>
  </main>'''
    else:
        main_block = f'''  <main id="top" class="project-main">
    <div class="container">
      <section class="project-rooms" id="rooms">
        <div class="proj-head">
          <div>
            <p class="eyebrow proj-head__eyebrow">{cfg["eyebrow"]}</p>
            <h1 class="proj-head__title">{cfg["title_html"]}</h1>
          </div>
{HOME_LINK}
        </div>

        <div class="rooms-rail-head">
          <h2 class="rooms-rail-title">Комнаты</h2>
          <div class="rail-nav">
            <button class="rail-nav__btn" type="button" data-dir="prev" aria-label="Прокрутить влево">←</button>
            <button class="rail-nav__btn" type="button" data-dir="next" aria-label="Прокрутить вправо">→</button>
          </div>
        </div>

        <div class="room-rail" id="roomRail">
{cards}
        </div>

        <div class="proj-foot">
          <a class="proj-foot__cta" href="contacts.html">Обсудить <em>ваш проект</em></a>
          <a class="link-underline" href="projects.html">
            Все проекты <span class="btn__arrow" aria-hidden="true">→</span>
          </a>
        </div>
      </section>

{views}
    </div>

    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Просмотр фотографии">
      <button class="lb-btn lightbox__close" type="button" aria-label="Закрыть">×</button>
      <button class="lb-btn lightbox__nav lightbox__nav--prev" type="button" aria-label="Предыдущее фото">←</button>
      <img class="lightbox__img" src="" alt="" />
      <button class="lb-btn lightbox__nav lightbox__nav--next" type="button" aria-label="Следующее фото">→</button>
      <span class="lightbox__counter"></span>
    </div>
  </main>'''

    return f'''<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
{JS_BOOTSTRAP}  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{cfg["description"]}" />
  <meta name="theme-color" content="#f4efe7" />
  <title>{cfg["title_plain"]} - проект Key Design Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
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
  </noscript>

{FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v={ASSET_CSS_VERSION}" />
</head>

<body>
{HEADER}

{main_block}

{FOOTER}

  <script src="app.js?v={ASSET_JS_VERSION}" defer></script>
  <script src="project.js?v=7" defer></script>
</body>
</html>
'''


def home_thumb(cfg: dict) -> str:
    thumb = ROOT / "assets" / "thumbs" / "home" / f"{cfg['slug']}.jpg"
    if thumb.exists():
        return f"assets/thumbs/home/{cfg['slug']}.jpg"
    return cfg["cover"]


def update_homepage(projects: list[dict], featured_slugs: list[str]):
    by_slug = {p["slug"]: p for p in projects}
    featured = [by_slug[slug] for slug in featured_slugs if slug in by_slug]
    cards = []
    for p in featured:
        img = home_thumb(p)
        cards.append(
            f'''          <a class="proj-grid-card" href="{p["html"]}">
            <span class="proj-grid-card__media">
              <img src="{img}" alt="{p["title_plain"]}" width="900" height="675" loading="lazy" decoding="async" />
            </span>
            <span class="proj-grid-card__info">
              <span class="proj-grid-card__name" data-i18n="{p["i18n_name"]}">{p["carousel_name"]}</span>
            </span>
          </a>'''
        )

    grid_html = "\n".join(cards)
    pattern = r'(<div class="proj-grid reveal">)(.*?)(</div>\s*\n\s*</div>\s*\n\s*</section>)'

    for page in ("key-design-studio.html", "index.html"):
        path = ROOT / page
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        replacement = r"\1\n" + grid_html + r"\n        \3"
        text = re.sub(pattern, replacement, text, count=1, flags=re.DOTALL)
        path.write_text(text, encoding="utf-8")


def generate_projects_page(projects: list[dict]):
    cards = []
    for p in projects:
        cards.append(
            f'''        <a class="proj-grid-card" href="{p["html"]}">
          <span class="proj-grid-card__media">
            <img src="{p["cover"]}" alt="{p["title_plain"]}" loading="lazy" />
          </span>
          <span class="proj-grid-card__info">
            <span class="proj-grid-card__name" data-i18n="{p["i18n_name"]}">{p["carousel_name"]}</span>
          </span>
        </a>'''
        )

    html = f'''<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
{JS_BOOTSTRAP}  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Проекты Key Design Studio - жилые и коммерческие интерьеры в Москве и Санкт-Петербурге." />
  <meta name="theme-color" content="#f4efe7" />
  <title>Проекты - Key Design Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
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
  </noscript>

{FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v={ASSET_CSS_VERSION}" />
</head>

<body>
{HEADER}

  <main id="top" class="projects-page">
    <div class="container">
      <div class="section-head reveal">
        <div>
          <h1 class="eyebrow" data-i18n="projects.label">Проекты</h1>
        </div>
        <a href="key-design-studio.html" class="link-underline" data-i18n="nav.home">
          На главную <span class="btn__arrow" aria-hidden="true">→</span>
        </a>
      </div>

      <div class="proj-grid reveal">
{chr(10).join(cards)}
      </div>
    </div>
  </main>

{FOOTER}

  <script src="app.js?v={ASSET_JS_VERSION}" defer></script>
</body>
</html>
'''
    (ROOT / "projects.html").write_text(html, encoding="utf-8")
    print("  → projects.html")


def _page_shell(title: str, description: str, main_content: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
{JS_BOOTSTRAP}  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{description}" />
  <meta name="theme-color" content="#f4efe7" />
  <title>{title} - Key Design Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
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
  </noscript>

{FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v={ASSET_CSS_VERSION}" />
</head>

<body>
{HEADER}

  <main id="top" class="projects-page">
    <div class="container">
{main_content}
    </div>
  </main>

{FOOTER}

  <script src="app.js?v={ASSET_JS_VERSION}" defer></script>
</body>
</html>
'''


def generate_info_pages():
    about = _page_shell(
        "О студии",
        "Key Design Studio - студия интерьерного дизайна в Москве и Санкт-Петербурге.",
        '''      <div class="about__grid reveal">
        <h1 class="about__title" data-i18n="about.title">
          Интерьеры, в которых хочется <em>жить и работать</em>
        </h1>
        <div class="about__body">
          <p class="eyebrow" data-i18n="about.label">О студии</p>
          <p class="about__text" data-i18n="about.text">
            Key Design Studio создаёт жилые и коммерческие пространства - квартиры,
            частные дома, офисы, рестораны и отели. Мы соединяем архитектурную
            ясность, благородные материалы и спокойную палитру, чтобы интерьер был
            одновременно функциональным и вне времени. Работаем в Москве и
            Санкт-Петербурге - от концепции до реализации под ключ.
          </p>
          <p class="about__signature">
            Кристина
            <span data-i18n="about.role">основатель и ведущий дизайнер</span>
          </p>
        </div>
      </div>''',
    )
    (ROOT / "about.html").write_text(about, encoding="utf-8")

    approach = _page_shell(
        "Подход",
        "Как мы работаем - Key Design Studio.",
        '''      <div class="section-head reveal">
        <div>
          <h1 class="eyebrow" data-i18n="nav.approach">Подход</h1>
          <h2 class="section-head__subtitle" data-i18n="approach.title">Как мы работаем</h2>
        </div>
''' + HOME_LINK + '''
      </div>
      <div class="approach__grid reveal">
        <div class="step">
          <span class="step__num">01</span>
          <h2 class="step__title" data-i18n="step.1.title">Знакомство и бриф</h2>
          <p class="step__text" data-i18n="step.1.text">
            Изучаем образ жизни, задачи и характер пространства, формируем общее видение.
          </p>
        </div>
        <div class="step">
          <span class="step__num">02</span>
          <h2 class="step__title" data-i18n="step.2.title">Концепция</h2>
          <p class="step__text" data-i18n="step.2.text">
            Предлагаем планировочные решения, палитру материалов и атмосферу интерьера.
          </p>
        </div>
        <div class="step">
          <span class="step__num">03</span>
          <h2 class="step__title" data-i18n="step.3.title">Проект и детали</h2>
          <p class="step__text" data-i18n="step.3.text">
            Разрабатываем рабочую документацию, подбираем мебель, свет и отделку.
          </p>
        </div>
        <div class="step">
          <span class="step__num">04</span>
          <h2 class="step__title" data-i18n="step.4.title">Реализация</h2>
          <p class="step__text" data-i18n="step.4.text">
            Ведём проект на площадке и контролируем качество вплоть до финального стайлинга.
          </p>
        </div>
      </div>''',
    )
    (ROOT / "approach.html").write_text(approach, encoding="utf-8")

    partners = _page_shell(
        "Партнёры",
        "Материалы и партнёры Key Design Studio.",
        '''      <div class="section-head reveal">
        <div>
          <h1 class="eyebrow" data-i18n="nav.partners">Партнёры</h1>
        </div>
''' + HOME_LINK + '''
      </div>
      <p class="lead reveal" style="max-width: 34ch; margin-bottom: var(--sp-5)" data-i18n="partners.text">
          Проверенные поставщики мебели, камня, света и отделочных материалов.
        </p>
      </div>
      <div class="partners__index reveal" aria-label="Партнёры и поставщики">
        <div class="pcat">
          <p class="pcat__label" data-i18n="partners.cat1">Мебель</p>
          <ul class="pcat__list">
            <li>Atelier</li><li>Forma</li><li>Casa</li><li>Lignum</li>
          </ul>
        </div>
        <div class="pcat">
          <p class="pcat__label" data-i18n="partners.cat2">Камень и поверхности</p>
          <ul class="pcat__list">
            <li>Pietra</li><li>Marmo</li><li>Terra</li>
          </ul>
        </div>
        <div class="pcat">
          <p class="pcat__label" data-i18n="partners.cat3">Свет</p>
          <ul class="pcat__list">
            <li>Lumen</li><li>Volta</li><li>Sole</li>
          </ul>
        </div>
        <div class="pcat">
          <p class="pcat__label" data-i18n="partners.cat4">Текстиль и декор</p>
          <ul class="pcat__list">
            <li>Norda</li><li>Studio Ferro</li>
          </ul>
        </div>
      </div>
      <p class="partners__note reveal" data-i18n="partners.note">
        Финальный список партнёров формируется индивидуально под задачи каждого проекта.
      </p>''',
    )
    (ROOT / "partners.html").write_text(partners, encoding="utf-8")
    print("  → about.html, approach.html, partners.html")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate project pages and optionally ingest Desktop photos.")
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Regenerate HTML only; do not copy images from Desktop",
    )
    args = parser.parse_args()

    site = load_site_config()
    projects = load_projects()
    featured_slugs = site.get("featured_slugs") or []

    did_ingest = False
    if not args.html_only:
        print("Copying hero image…")
        ingest_hero()

        for cfg in projects:
            if cfg.get("source"):
                print(f"Ingesting {cfg['title_plain']}…")
                ingest_project(cfg)
                did_ingest = True

        if did_ingest:
            opt = ROOT / "optimize-images.py"
            if opt.exists():
                print("Optimizing images…")
                subprocess.run([sys.executable, str(opt)], check=False)

    for cfg in projects:
        sync_rooms_from_config(cfg)
        html = generate_html(cfg)
        out = ROOT / cfg["html"]
        out.write_text(html, encoding="utf-8")
        print(f"  → {out.name} ({len(html)} bytes)")

    sync_site_projects_order(projects)
    update_homepage(projects, featured_slugs)
    generate_projects_page(projects)
    print("Updated projects.html")


if __name__ == "__main__":
    main()
