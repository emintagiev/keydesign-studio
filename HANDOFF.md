# Key Design Studio - передача контекста

> Этот файл - «память» между чатами. В новом чате напиши: **«Прочитай HANDOFF.md и продолжай»**.

Дата: 30 июня 2026, поздний вечер.
**Прод:** https://www.keydesign.studio/
**Локально:** `http://localhost:8099/`

---

## ВАЖНО про откат

- Все файлы сайта под git.
- Перед крупной правкой: `git status` (чистое дерево).
- После логически законченного изменения: commit.
- Отменить незакоммиченное: `git restore .`

**GitHub:** `https://github.com/emintagiev/keydesign-studio`
**Ветка для работы:** `site-clean` (основная)
**Ветка деплоя Cloudflare:** `master` (fast-forward из site-clean)

```bash
git push origin site-clean
git push origin site-clean:master   # выкат на прод
```

Локальный `master` может расходиться с GitHub - работать на `site-clean`.

---

## Что на проде сейчас (коммит `92e2fc6` + следующий с шапкой)

### Главная
- URL: `https://www.keydesign.studio/` (`index.html`, чистый URL)
- Hero: 5 фото, crossfade 5 сек, lazy hero (только 1-й кадр сразу)
- Шапка без логотипа (nav-only), кремовые кнопки, квиз `#brief`
- Сетка 3 проектов, контакты внизу

### Услуги (`services.html` / `/services`)
- 4 услуги: дизайн-проект, менеджмент, авторский надзор, архитектурное планирование
- Круглое фото справа у каждой услуги, «Подробнее» раскрывает этапы
- «Оставить заявку» = тот же квиз, что «Обсудить проект»
- Тексты переписаны (референс buro11.ru, не копипаст)

### Скрыто на проде (есть только локально)
- **Подход** (`approach.html`) и **Партнёры** (`partners.html`)
- В `prepare-deploy.sh`: страницы не копируются в `dist/`, `strip-prod-nav.py` убирает ссылки из меню
- `_redirects`: `/approach.html` и `/partners.html` → `/` (302)

### Скорость
- Фото: ~176 МБ (было ~1 ГБ), `optimize-images.py` (2400px, q82)
- `_headers`: assets `max-age=31536000, immutable`; CSS/JS 7 дней; HTML 1 час
- Проверка: `curl -sI https://www.keydesign.studio/assets/projects/moscow-studio/interior/1.jpg | grep cache`

---

## Деплой (Cloudflare Workers + Assets)

| Параметр | Значение |
|----------|----------|
| Репозиторий | `emintagiev/keydesign-studio` |
| Ветка | `master` |
| Build command | `bash prepare-deploy.sh` |
| Output | `dist/` (в `.gitignore`) |
| Конфиг | `wrangler.jsonc` → `"assets": { "directory": "dist" }` |
| Домены | `www.keydesign.studio` (основной), apex → www |

Файлы деплоя: `prepare-deploy.sh`, `strip-prod-nav.py`, `_redirects`, `_headers`.

---

## Версии кэша (актуально)

| Файл | Версия |
|------|--------|
| `styles.css` | `?v=59` |
| `app.js` | `?v=18` |
| `brief-config.js` | `?v=1` |
| `project.js` | `?v=7` |
| логотипы | `?v=11` |

После правок CSS/JS: bump версии во **всех** `*.html` и в шаблонах `build-projects.py`.

---

## 12 проектов

| # | Название | HTML |
|---|----------|------|
| 1 | Dream House | `dream-house.html` |
| 2 | ЖК Пульсар (Москва) | `zhk-pulsar.html` |
| 3 | Москва Студия | `moscow-studio.html` |
| 4 | Салок красоты tati | `salok-krasoty-tati.html` |
| 5 | г. Новосибирск, Лаки Парк, Дом | `laki-park-dom.html` |
| 6 | г. Москва, ЖК Архитектор | `zhk-arkhitektor.html` |
| 7 | Новосибирск, Академгородок, Жк Пульсар 1 | `ns-akadem-pulsar.html` |
| 8 | г. Новосибирск, Квартал Декабристов | `kvartal-dekabristov.html` |
| 9 | г. Новосибирск, ул. Невская дом | `nevskaya-dom.html` |
| 10 | г. Новосибирск, Квартира с Восточным вайбом | `vostochny-vayb.html` |
| 11 | г. Новосибирск, Кедровый | `kedrovy-ns.html` |
| 12 | Кабинет-Оружейная Морозово | `kabinet-morozovo.html` |

---

## Карта файлов

| Назначение | Файл |
|------------|------|
| Главная | `index.html` (канон), `key-design-studio.html` (редирект на `/`) |
| Услуги | `services.html` |
| О студии | `about.html` (ручная, не build) |
| Подход / Партнёры | `approach.html`, `partners.html` (только локально) |
| Проекты | `projects.html` |
| i18n, hero, brief, services accordion | `app.js` |
| Formspree endpoint | `brief-config.js` |
| Галерея | `project.js` |
| Стили | `styles.css` |
| Генератор проектов | `build-projects.py` |
| Prod-сборка | `prepare-deploy.sh`, `strip-prod-nav.py` |
| Оптимизация фото | `optimize-images.py` |
| Правила AI | `.cursor/rules/copy-typography.mdc` |

---

## build-projects.py

- `HOME_LINK` - «На главную» в проектах.
- **`generate_info_pages()` отключён** - не затирать `about.html`.
- `--html-only` - только HTML, без копирования фото с Desktop.
- После ingest с Desktop автоматически запускается `optimize-images.py`.
- Пересборка: `python3 build-projects.py --html-only`

---

## Контакты

- Телефон: `+7 (923) 000-00-36`
- Почта: `key-des@mail.ru`
- Telegram / WhatsApp / Instagram (без ников в подписях)

---

## Открытые вопросы

1. **Formspree:** endpoint в `brief-config.js` (сейчас fallback mailto).
2. **Подход / Партнёры:** доработать локально, потом включить в prod (убрать из `PROD_HIDDEN` в `prepare-deploy.sh`).
3. EN-переводы длинных названий проектов.
4. WebP / srcset - долгосрочно.

---

## Принципы

- Только короткое тире `-` (см. `.cursor/rules/copy-typography.mdc`).
- Названия вкладок - `.eyebrow`, не `.section-head__title`.
- «На главную →» на каждой внутренней странице.
- Названия проектов = папке на Desktop, дословно.
- Commit только по запросу пользователя (или явная просьба «выкати»).

---

## Локальный запуск

```bash
cd /Users/emin/key-design-studio
python3 -m http.server 8099
```

Открыть: http://localhost:8099/

---

## Транскрипты

- `agent-transcripts/c99ba3ea-005b-40f7-8105-fbcc298fc982/` - оптимизация, услуги, деплой
