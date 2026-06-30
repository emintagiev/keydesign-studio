#!/usr/bin/env python3
"""Copy original images and generate project pages from Desktop folders."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DESKTOP = Path.home() / "Desktop"
KEY_DESIGN = DESKTOP / "key design"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

HEADER = """  <header class="header" id="header">
    <div class="container header__inner">
      <a href="key-design-studio.html" class="brand" aria-label="Key Design Studio">
        <img class="brand__logo brand__logo--dark" src="assets/logo.png?v=11" alt="" width="859" height="722" />
        <img class="brand__logo brand__logo--light" src="assets/logo-light.png?v=11" alt="" width="859" height="722" />
      </a>

      <nav class="nav" id="nav" aria-label="Основная навигация">
        <a class="nav__link" href="about.html" data-i18n="nav.about">О студии</a>
        <a class="nav__link" href="projects.html" data-i18n="nav.projects">Проекты</a>
        <a class="nav__link" href="approach.html" data-i18n="nav.approach">Подход</a>
        <a class="nav__link" href="partners.html" data-i18n="nav.partners">Партнёры</a>
        <a class="nav__link" href="key-design-studio.html#contact" data-i18n="nav.contact">Контакты</a>
      </nav>

      <div class="header__tools">
        <button class="nav-toggle" type="button" id="navToggle" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">
          <span></span>
          <span></span>
        </button>

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
      <span class="footer__meta" data-i18n="footer.cities">Москва · Санкт-Петербург</span>
    </div>
  </footer>"""

HOME_LINK = """        <a href="key-design-studio.html" class="link-underline" data-i18n="nav.home">
          На главную <span class="btn__arrow" aria-hidden="true">→</span>
        </a>"""

FAVICON_LINKS = """  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png?v=1" />
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png?v=1" />"""

PROJECTS = [
    {
        "slug": "dream-house",
        "html": "dream-house.html",
        "source": KEY_DESIGN / "Dream House",
        "title_html": 'Dream <em>House</em>',
        "title_plain": "Dream House",
        "eyebrow": "Частный дом · Москва",
        "lead": (
            "Частный дом в тёплой нейтральной палитре: натуральное дерево, мягкие "
            "фактуры и спокойный свет. Выберите комнату, чтобы рассмотреть её детальнее."
        ),
        "meta": {"type": "Частный дом", "city": "Москва", "area": "240 м²", "year": "2025"},
        "description": "Dream House - частный дом в Москве. Проект Key Design Studio.",
        "cover": "assets/projects/dream-house/kitchen-living/8.jpg",
        "grid_city": "Москва",
        "carousel_cat": "Частный дом · Москва · 2025",
        "carousel_name": "Dream House",
        "i18n_cat": "project.1.cat",
        "i18n_name": "project.1.name",
        "room_map": [
            ("Кухня-гостиная", "kitchen-living", "Кухня-гостиная", "8.jpg"),
            ("Мастер- спальня", "master-bedroom", "Мастер-спальня", "1.jpg"),
            ("Кабинет", "study", "Кабинет", "1.jpg"),
            ("Гостевая спальня", "guest-bedroom", "Гостевая спальня", "1.jpg"),
            ("Ванная комната", "bathroom", "Ванная комната", "1.jpg"),
            ("Душевая", "shower", "Душевая", "1.jpg"),
            ("Гардеробная комната", "wardrobe", "Гардеробная", "1.jpg"),
            ("Гардеробная при входе", "entry-wardrobe", "Гардеробная при входе", "1.jpg"),
            ("Прачечная", "laundry", "Прачечная", "1.jpg"),
        ],
    },
    {
        "slug": "zhk-pulsar",
        "html": "zhk-pulsar.html",
        "source": KEY_DESIGN / "ЖК Пульсар",
        "title_html": 'ЖК <em>Пульсар</em>',
        "title_plain": "ЖК Пульсар",
        "eyebrow": "Жилой комплекс · Москва",
        "lead": (
            "Квартира в современном жилом комплексе: светлая палитра, "
            "функциональное зонирование и продуманные детали для комфортной жизни."
        ),
        "meta": {"type": "Квартира", "city": "Москва", "area": "-", "year": "2025"},
        "description": "ЖК Пульсар - квартира в Москве. Проект Key Design Studio.",
        "cover": "assets/projects/zhk-pulsar/kitchen-living/12.jpg",
        "grid_city": "Москва",
        "carousel_cat": "Квартира · Москва · 2025",
        "carousel_name": "ЖК Пульсар",
        "i18n_cat": "project.2.cat",
        "i18n_name": "project.2.name",
        "room_map": [
            ("Кухня- гостиная", "kitchen-living", "Кухня-гостиная", "12.jpg"),
            ("Спальня", "bedroom", "Спальня", "4.jpg"),
            ("Прихожая", "entry", "Прихожая", "21.jpg"),
            ("Ванная комната", "bathroom", "Ванная комната", "25.jpg"),
            ("Санузел", "wc", "Санузел", "1.jpg"),
        ],
    },
    {
        "slug": "moscow-studio",
        "html": "moscow-studio.html",
        "source": KEY_DESIGN / "Москва студия",
        "title_html": 'Москва <em>Студия</em>',
        "title_plain": "Москва Студия",
        "eyebrow": "Студия · Москва",
        "lead": (
            "Компактная студия с выверенной планировкой: каждый метр работает "
            "на комфорт, свет и ощущение простора."
        ),
        "meta": {"type": "Студия", "city": "Москва", "area": "-", "year": "2025"},
        "description": "Москва Студия - интерьер студии в Москве. Проект Key Design Studio.",
        "cover": "assets/projects/moscow-studio/interior/1.jpg",
        "grid_city": "Москва",
        "carousel_cat": "Студия · Москва · 2025",
        "carousel_name": "Москва Студия",
        "i18n_cat": "project.3.cat",
        "i18n_name": "project.3.name",
        "flat_room": ("interior", "Интерьер", "1.jpg"),
    },
    {
        "slug": "salok-krasoty-tati",
        "html": "salok-krasoty-tati.html",
        "source": KEY_DESIGN / "Салок красоты tati",
        "title_html": 'Салок красоты <em>tati</em>',
        "title_plain": "Салок красоты tati",
        "eyebrow": "Салок красоты tati",
        "lead": (
            "Интерьер салона красоты tati - мягкий свет, спокойная палитра "
            "и продуманная эргономика для комфорта гостей и команды."
        ),
        "meta": {"type": "Салок красоты", "city": "-", "area": "-", "year": "2026"},
        "description": "Салок красоты tati - проект Key Design Studio.",
        "cover": "assets/projects/salok-krasoty-tati/interior/08.04.2026 Кристина Key Design Tati DSCF2028.jpg",
        "grid_city": "-",
        "carousel_cat": "Салок красоты tati · 2026",
        "carousel_name": "Салок красоты tati",
        "i18n_cat": "project.4.cat",
        "i18n_name": "project.4.name",
        "flat_room": ("interior", "Интерьер", "08.04.2026 Кристина Key Design Tati DSCF2028.jpg"),
    },
    {
        "slug": "laki-park-dom",
        "html": "laki-park-dom.html",
        "source": DESKTOP / "г. Новосибирск, Лаки Парк, Дом",
        "title_html": 'г. Новосибирск, Лаки Парк, <em>Дом</em>',
        "title_plain": "г. Новосибирск, Лаки Парк, Дом",
        "eyebrow": "Частный дом · Новосибирск",
        "lead": "",
        "meta": {"type": "Частный дом", "city": "Новосибирск", "area": "-", "year": "2025"},
        "description": "г. Новосибирск, Лаки Парк, Дом - частный дом. Проект Key Design Studio.",
        "cover": "assets/projects/laki-park-dom/kitchen-living/001-denoise-upscale-1.7x.jpeg",
        "grid_city": "Новосибирск",
        "carousel_cat": "Частный дом · Новосибирск · 2025",
        "carousel_name": "г. Новосибирск, Лаки Парк, Дом",
        "i18n_cat": "project.5.cat",
        "i18n_name": "project.5.name",
        "room_map": [
            ("Кухня-гостиная", "kitchen-living", "Кухня-гостиная", "001-denoise-upscale-1.7x.jpeg"),
            ("Санузел 1", "wc-1", "Санузел 1", "005544777_0000(3)-denoise-upscale-1.9x.jpeg"),
            ("Санузел 2", "wc-2", "Санузел 2", "02354_0000(1)-denoise-upscale-2x.jpeg"),
        ],
    },
    {
        "slug": "zhk-arkhitektor",
        "html": "zhk-arkhitektor.html",
        "source": DESKTOP / "г. Москва, ЖК Архитектор",
        "title_html": 'г. Москва, ЖК <em>Архитектор</em>',
        "title_plain": "г. Москва, ЖК Архитектор",
        "eyebrow": "Жилой комплекс · Москва",
        "lead": "",
        "meta": {"type": "Квартира", "city": "Москва", "area": "-", "year": "2025"},
        "description": "г. Москва, ЖК Архитектор - квартира в Москве. Проект Key Design Studio.",
        "cover": "assets/projects/zhk-arkhitektor/interior/IMG_4796.JPG",
        "grid_city": "Москва",
        "carousel_cat": "Квартира · Москва · 2025",
        "carousel_name": "г. Москва, ЖК Архитектор",
        "i18n_cat": "project.6.cat",
        "i18n_name": "project.6.name",
        "flat_room": ("interior", "Интерьер", "IMG_4796.JPG"),
    },
    {
        "slug": "ns-akadem-pulsar",
        "html": "ns-akadem-pulsar.html",
        "source": DESKTOP / 'Новосибирск, Академгородок, Жк Пульсар 1',
        "title_html": 'Новосибирск, Академгородок, Жк <em>Пульсар 1</em>',
        "title_plain": 'Новосибирск, Академгородок, Жк Пульсар 1',
        "eyebrow": 'Жилой комплекс · Новосибирск',
        "lead": "",
        "meta": {"type": "Квартира", "city": "Новосибирск", "area": "-", "year": "2025"},
        "description": 'Новосибирск, Академгородок, Жк Пульсар 1 - проект Key Design Studio.',
        "cover": "assets/projects/ns-akadem-pulsar/kitchen-living/IMG_4822.JPG",
        "grid_city": "Новосибирск",
        "carousel_cat": 'Жилой комплекс · Новосибирск · 2025',
        "carousel_name": 'Новосибирск, Академгородок, Жк Пульсар 1',
        "i18n_cat": "project.7.cat",
        "i18n_name": "project.7.name",
        "room_map": [
            ('Кухня-гостиная', "kitchen-living", "Кухня-гостиная", 'IMG_4822.JPG'),
            ('Спальня', "bedroom", "Спальня", 'IMG_4831.JPG'),
            ('Прихожая', "entry", "Прихожая", 'IMG_4845.JPG'),
            ('мастер-санузел', "master-wc", "Мастер-санузел", 'IMG_4838.JPG'),
            ('Гостевой санузел', "guest-wc", "Гостевой санузел", 'IMG_4842.JPG'),
        ],
    },
    {
        "slug": "kvartal-dekabristov",
        "html": "kvartal-dekabristov.html",
        "source": DESKTOP / 'г. Новосибирск, Квартал Декабристов, Кухня - Гостиная',
        "title_html": 'г. Новосибирск, Квартал <em>Декабристов</em>',
        "title_plain": 'г. Новосибирск, Квартал Декабристов',
        "eyebrow": 'Квартира · Новосибирск',
        "lead": "",
        "meta": {"type": "Квартира", "city": "Новосибирск", "area": "-", "year": "2025"},
        "description": 'г. Новосибирск, Квартал Декабристов - проект Key Design Studio.',
        "cover": "assets/projects/kvartal-dekabristov/kitchen-living/6.jpg",
        "grid_city": "Новосибирск",
        "carousel_cat": 'Квартира · Новосибирск · 2025',
        "carousel_name": 'г. Новосибирск, Квартал Декабристов',
        "i18n_cat": "project.8.cat",
        "i18n_name": "project.8.name",
        "room_map": [
            ("__root__", "kitchen-living", "Кухня-гостиная", '6.jpg'),
            ('Ванная', "bathroom", "Ванная", '19.jpg'),
            ('Детская девочки', "girls-room", "Детская девочки", '25.jpg'),
            ('Прихожая', "entry", "Прихожая", '1.jpg'),
            ('Спальня', "bedroom", "Спальня", '9.jpeg'),
        ],
    },
    {
        "slug": "nevskaya-dom",
        "html": "nevskaya-dom.html",
        "source": DESKTOP / 'г. Новосибирск, ул. Невская дом',
        "title_html": 'г. Новосибирск, ул. Невская <em>дом</em>',
        "title_plain": 'г. Новосибирск, ул. Невская дом',
        "eyebrow": 'Частный дом · Новосибирск',
        "lead": "",
        "meta": {"type": "Частный дом", "city": "Новосибирск", "area": "-", "year": "2025"},
        "description": 'г. Новосибирск, ул. Невская дом - проект Key Design Studio.',
        "cover": "assets/projects/nevskaya-dom/kitchen-living/3.jpg",
        "grid_city": "Новосибирск",
        "carousel_cat": 'Частный дом · Новосибирск · 2025',
        "carousel_name": 'г. Новосибирск, ул. Невская дом',
        "i18n_cat": "project.9.cat",
        "i18n_name": "project.9.name",
        "room_map": [
            ("__root__", "kitchen-living", "Кухня-гостиная", '3.jpg'),
            ('Мастер-спальня', "master-bedroom", "Мастер-спальня", '1.jpg'),
            ('Гостевая спальня ', "guest-bedroom", "Гостевая спальня", '1.jpg'),
            ('Кабинет ', "study", "Кабинет", '1.jpg'),
            ('Ванная комната', "bathroom", "Ванная комната", '1.jpg'),
            ('Душевая', "shower", "Душевая", '1.jpg'),
            ('Мастер-гардеробная', "wardrobe", "Мастер-гардеробная", '1.jpg'),
        ],
    },
    {
        "slug": "vostochny-vayb",
        "html": "vostochny-vayb.html",
        "source": DESKTOP / 'г. Новосибирск, Квартира с Восточным вайбом',
        "title_html": 'г. Новосибирск, Квартира с Восточным <em>вайбом</em>',
        "title_plain": 'г. Новосибирск, Квартира с Восточным вайбом',
        "eyebrow": 'Квартира · Новосибирск',
        "lead": "",
        "meta": {"type": "Квартира", "city": "Новосибирск", "area": "-", "year": "2025"},
        "description": 'г. Новосибирск, Квартира с Восточным вайбом - проект Key Design Studio.',
        "cover": "assets/projects/vostochny-vayb/kitchen-living/IMG_4813.JPG",
        "grid_city": "Новосибирск",
        "carousel_cat": 'Квартира · Новосибирск · 2025',
        "carousel_name": 'г. Новосибирск, Квартира с Восточным вайбом',
        "i18n_cat": "project.10.cat",
        "i18n_name": "project.10.name",
        "room_map": [
            ('Кухня-гостиная ', "kitchen-living", "Кухня-гостиная", 'IMG_4813.JPG'),
            ('Спальня', "bedroom", "Спальня", 'IMG_4820.JPG'),
            ('Санузел ', "wc", "Санузел", 'IMG_4818.JPG'),
        ],
    },
    {
        "slug": "kedrovy-ns",
        "html": "kedrovy-ns.html",
        "source": DESKTOP / 'г. Новосибирск, Кедровый',
        "title_html": 'г. Новосибирск, <em>Кедровый</em>',
        "title_plain": 'г. Новосибирск, Кедровый',
        "eyebrow": 'Квартира · Новосибирск',
        "lead": "",
        "meta": {"type": "Квартира", "city": "Новосибирск", "area": "-", "year": "2025"},
        "description": 'г. Новосибирск, Кедровый - проект Key Design Studio.',
        "cover": "assets/projects/kedrovy-ns/kitchen-living/005848974447_0000(3)-denoise-upscale-1.9x.jpeg",
        "grid_city": "Новосибирск",
        "carousel_cat": 'Квартира · Новосибирск · 2025',
        "carousel_name": 'г. Новосибирск, Кедровый',
        "i18n_cat": "project.11.cat",
        "i18n_name": "project.11.name",
        "room_map": [
            ('Кухня -гостиная', "kitchen-living", "Кухня-гостиная", '005848974447_0000(3)-denoise-upscale-1.9x.jpeg'),
            ('Детская', "kids-room", "Детская", '1-denoise-upscale-1.9x.jpeg'),
            ('Санузел', "wc", "Санузел", '002-upscale-1.9x.jpeg'),
        ],
    },
    {
        "slug": "kabinet-morozovo",
        "html": "kabinet-morozovo.html",
        "source": DESKTOP / 'Кабинет-Оружейная Морозово',
        "title_html": 'Кабинет-Оружейная <em>Морозово</em>',
        "title_plain": 'Кабинет-Оружейная Морозово',
        "eyebrow": 'Кабинет · Морозово',
        "lead": "",
        "meta": {"type": "Кабинет", "city": "-", "area": "-", "year": "2025"},
        "description": 'Кабинет-Оружейная Морозово - проект Key Design Studio.',
        "cover": "assets/projects/kabinet-morozovo/interior/1.jpg",
        "grid_city": "-",
        "carousel_cat": 'Кабинет · 2025',
        "carousel_name": 'Кабинет-Оружейная Морозово',
        "i18n_cat": "project.12.cat",
        "i18n_name": "project.12.name",
        "flat_room": ("interior", "Интерьер", '1.jpg'),
    },
]


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
    if "room_map" in cfg:
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
        <a class="proj-foot__cta" href="key-design-studio.html#contact">Обсудить <em>ваш проект</em></a>
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
          <a class="proj-foot__cta" href="key-design-studio.html#contact">Обсудить <em>ваш проект</em></a>
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
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{cfg["description"]}" />
  <meta name="theme-color" content="#f4efe7" />
  <title>{cfg["title_plain"]} - проект Key Design Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&display=swap"
    rel="stylesheet"
  />

{FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v=53" />
</head>

<body>
{HEADER}

{main_block}

{FOOTER}

  <script src="app.js?v=10"></script>
  <script src="project.js?v=7"></script>
</body>
</html>
'''


def update_homepage(projects: list[dict]):
    slides = []
    for p in projects:
        slides.append(
            f'''        <a class="pcar-slide" href="{p["html"]}" aria-label="{p["title_plain"]}">
          <img src="{p["cover"]}" alt="{p["title_plain"]}" loading="lazy" />
          <span class="pcar-slide__shade" aria-hidden="true"></span>
          <span class="pcar-slide__caption">
            <span class="pcar-slide__name" data-i18n="{p["i18n_name"]}">{p["carousel_name"]}</span>
          </span>
        </a>'''
        )

    home = ROOT / "key-design-studio.html"
    text = home.read_text(encoding="utf-8")
    pattern = r'(<div class="pcar" id="projCar">)(.*?)(</div>\s*\n\s*</section>)'
    replacement = r'\1\n' + "\n".join(slides) + r'\n      \3'
    text = re.sub(pattern, replacement, text, count=1, flags=re.DOTALL)
    home.write_text(text, encoding="utf-8")


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
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Проекты Key Design Studio - жилые и коммерческие интерьеры в Москве и Санкт-Петербурге." />
  <meta name="theme-color" content="#f4efe7" />
  <title>Проекты - Key Design Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&display=swap"
    rel="stylesheet"
  />

{FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v=53" />
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

  <script src="app.js?v=10"></script>
</body>
</html>
'''
    (ROOT / "projects.html").write_text(html, encoding="utf-8")
    print("  → projects.html")


def _page_shell(title: str, description: str, main_content: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{description}" />
  <meta name="theme-color" content="#f4efe7" />
  <title>{title} - Key Design Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&display=swap"
    rel="stylesheet"
  />

{FAVICON_LINKS}
  <link rel="stylesheet" href="styles.css?v=53" />
</head>

<body>
{HEADER}

  <main id="top" class="projects-page">
    <div class="container">
{main_content}
    </div>
  </main>

{FOOTER}

  <script src="app.js?v=10"></script>
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

    did_ingest = False
    if not args.html_only:
        print("Copying hero image…")
        ingest_hero()

        for cfg in PROJECTS:
            if cfg.get("source"):
                print(f"Ingesting {cfg['title_plain']}…")
                ingest_project(cfg)
                did_ingest = True

        if did_ingest:
            opt = ROOT / "optimize-images.py"
            if opt.exists():
                print("Optimizing images…")
                subprocess.run([sys.executable, str(opt)], check=False)

    for cfg in PROJECTS:
        html = generate_html(cfg)
        out = ROOT / cfg["html"]
        out.write_text(html, encoding="utf-8")
        print(f"  → {out.name} ({len(html)} bytes)")

    update_homepage(PROJECTS)
    generate_projects_page(PROJECTS)
    print("Updated projects.html")


if __name__ == "__main__":
    main()
