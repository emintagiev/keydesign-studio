# Key Design Studio - передача контекста

> В новом чате напиши: **«Прочитай HANDOFF.md и продолжай»**.

**Обновлено:** 2 июля 2026  
**Прод:** https://www.keydesign.studio/  
**Локально:** `python3 -m http.server 8099` → http://localhost:8099/

---

## Быстрый старт для AI

1. Прочитать этот файл и `.cursor/rules/copy-typography.mdc`.
2. `git status` - много правок может быть **не закоммичено**, но уже **на проде** (деплой шёл через `./deploy-ru.sh` без commit).
3. Версии ассетов - только через `python3 bump-assets.py` (источник правды: `bump-assets.py`, не константы в `build-projects.py`).

---

## Деплой (актуально: Timeweb)

| Что | Как |
|-----|-----|
| Сборка | `bash prepare-deploy.sh` → папка `dist/` |
| Выкладка | `./deploy-ru.sh` (SFTP, creds в `deploy.env`, gitignored) |
| Проверка | `./verify-deploy.sh` - сравнивает prod с `dist/` по MD5 |
| Скрыто на проде | `approach.html`, `partners.html` (`PROD_HIDDEN` в `prepare-deploy.sh`, `strip-prod-nav.py`) |

**Важно:** `prepare-deploy.sh` перед копированием в `dist/` запускает `bump-assets.py` на **исходниках** - после деплоя локальные HTML могут чуть разъехаться по `?v=`. Коммитить лучше после деплоя или держать версии в `bump-assets.py`.

**GitHub:** `emintagiev/keydesign-studio`, ветка **`site-clean`**.  
Последний commit на ветке: `37058e9` (прелоадер), но **поверх него много uncommitted изменений** - about, команда, порядок проектов, прелоадер 0.8s, сетка projects 2 col и т.д.

Cloudflare (`wrangler.jsonc`, `master`) - legacy, основной прод сейчас Timeweb. См. `HOSTING-RU.md`.

---

## Версии кэша (сейчас)

| Файл | Версия |
|------|--------|
| `styles.css` | `?v=74` |
| `app.js` | `?v=35` |
| `project.js` | `?v=7` |
| `brief-config.js` | `?v=1` |
| логотипы | `?v=11` |

После правок CSS/JS: правка `bump-assets.py` → `python3 bump-assets.py`.

---

## Главная (`index.html`)

- Канон URL: `/`
- **Прелоадер** (только главная, `body.home`):
  - **0.8 с** минимум + **0.8 с** переход (desktop)
  - Desktop: логотип на месте hero, crossfade ч/б → светлый, затем контент
  - Mobile: простой центрированный прелоадер, без морфа
  - `prefers-reduced-motion`: почти без задержки
- Hero: 5 фото, crossfade
- Шапка nav-only (без логотипа в header), светлые элементы на hero
- **3 проекта в сетке** (featured):

| # | Проект | slug |
|---|--------|------|
| 1 | Москва Студия | `moscow-studio` |
| 2 | Дубай, апартаменты, 180 кв.м. | `kvartira-dubay` |
| 3 | Дом Синегорье | `dom-sinegore` |

Thumbs: `assets/thumbs/home/{moscow-studio,kvartira-dubay,dom-sinegore}.jpg` (генерит `build-hero-images.py`).

---

## Страница «Проекты» (`projects.html`)

- **Порядок** = массив `PROJECTS` в `build-projects.py` (пересборка: `python3 build-projects.py`):
  1. Москва Студия
  2. Дубай, апартаменты, 180 кв.м.
  3. Дом Синегорье
  4. г. Москва, ЖК Архитектор
  5. … далее остальные (всего **13** проектов, см. ниже)
- **Сетка: 2 колонки**, крупные карточки (`.projects-page .proj-grid`). На главной по-прежнему **3** в ряд.

---

## 13 проектов (порядок в `build-projects.py`)

| # | Название | slug / HTML |
|---|----------|-------------|
| 1 | Москва Студия | `moscow-studio` |
| 2 | Дубай, апартаменты, 180 кв.м. | `kvartira-dubay` |
| 3 | Дом Синегорье | `dom-sinegore` |
| 4 | г. Москва, ЖК Архитектор | `zhk-arkhitektor` |
| 5 | Салок красоты tati | `salok-krasoty-tati` |
| 6 | г. Новосибирск, Лаки Парк, Дом | `laki-park-dom` |
| 7 | Новосибирск, Академгородок, Жк Пульсар 1 | `ns-akadem-pulsar` |
| 8 | г. Новосибирск, Квартал Декабристов | `kvartal-dekabristov` |
| 9 | г. Новосибирск, Загородный дом, 160 кв.м. | `nevskaya-dom` |
| 10 | г. Новосибирск, Квартира с Восточным вайбом | `vostochny-vayb` |
| 11 | г. Новосибирск, Кедровый | `kedrovy-ns` |
| 12 | Кабинет-Оружейная Морозово | `kabinet-morozovo` |
| 13 | Little Classic | `little-classic` |

**Не путать:** `ns-akadem-pulsar` (Новосибирск, Академгородок) - отдельный проект.

---

## О студии (`about.html` - ручная страница)

- Фото Кристины: `assets/about-kristina.jpg?v=7`, max-width **480px**
- Блок **«Команда»**: Софья Вигель, Полина Трубина - фото `assets/team/`, 2 в ряд (max 400px как было у команды)
- Текст под командой: `about.team.note` в `app.js`
- `generate_info_pages()` в `build-projects.py` **отключён** - не затирает `about.html`

---

## Услуги (`services.html`)

- 2-я услуга: **«Проектное сопровождение»** (было «Менеджмент проектов»), ключ `svc.2.*` в `app.js`
- У «Дизайн-проект интерьера» убрана сноска про консультацию планировки (`svc.1.note` удалён)

---

## build-projects.py

```python
HOME_FEATURED_SLUGS = ["moscow-studio", "kvartira-dubay", "dom-sinegore"]
```

- Источники фото: `~/Desktop/key design/…`, `~/Desktop/…`
- `--html-only` - только HTML, без ingest с Desktop
- После полного прогона: `projects.html`, все `*.html` проектов, `update_homepage()` для `index.html` + `key-design-studio.html`
- `key-design-studio.html` - локально полная копия главной; на проде редирект на `/`

---

## Карта файлов

| Назначение | Файл |
|------------|------|
| Главная | `index.html` |
| i18n, hero, brief, preloader, services | `app.js` |
| Formspree | `brief-config.js` |
| Галерея проектов | `project.js` |
| Стили | `styles.css` |
| Генератор проектов | `build-projects.py` |
| Hero + thumbs главной | `build-hero-images.py` |
| Bump `?v=` | `bump-assets.py` |
| Prod bundle | `prepare-deploy.sh`, `strip-prod-nav.py` |
| Деплой RU | `deploy-ru.sh`, `deploy.env` |
| Оптимизация фото | `optimize-images.py` |
| Типографика (тире!) | `.cursor/rules/copy-typography.mdc` |

---

## Принципы (не ломать)

- Только **короткое тире `-`**, не `—` и не `–`.
- Названия вкладок страниц - **`.eyebrow`**, не крупный serif.
- «На главную →» на каждой внутренней (кроме главной).
- **Commit только по явной просьбе** пользователя. Деплой - по «задеплой» / «на прод».

---

## Открытые вопросы

1. Formspree в `brief-config.js` - проверить живой endpoint.
2. Подход / Партнёры - включить на прод, когда будут готовы.
3. **Git:** много uncommitted work - имеет смысл сделать commit на `site-clean` и push.
4. WebP / srcset - по желанию позже.

---

## Контакты на сайте

- `+7 (923) 000-00-36`
- `key-des@mail.ru`
- Telegram / WhatsApp / Instagram

---

## История чатов (если нужны детали)

Транскрипты Cursor: `~/.cursor/projects/Users-emin-key-design-studio/agent-transcripts/`  
Крупная сессия (прелоадер, mobile, команда, деплой): `38571574-ea1f-4e92-b50e-54d3c618934f`

---

## Локальный запуск

```bash
cd /Users/emin/key-design-studio
python3 -m http.server 8099
# или ./serve.sh
```
