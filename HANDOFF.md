# Key Design Studio - передача контекста

> В новом чате напиши: **«Прочитай HANDOFF.md и продолжай»**.

**Обновлено:** 7 июля 2026 (вечер)  
**Прод:** https://www.keydesign.studio/  
**Админка:** https://www.keydesign.studio/admin/  
**Локально:** `python3 -m http.server 8099`

---

## Активная задача

**Админка для Кристины** - MVP на проде, вход работает.  
Подробности: **`ADMIN-HANDOFF.md`**

**Главный блокер для полного flow:** Publish в админке коммитит в GitHub, но **автодеплой на Timeweb не настроен** (нет GitHub Actions secrets). Сейчас деплой вручную: `bash deploy-ru.sh`.

---

## Быстрый старт для AI

1. **`ADMIN-HANDOFF.md`** - админка, OAuth, YAML, форма, CI
2. **`HANDOFF.md`** (этот файл) - сайт, контакты, проекты
3. `.cursor/rules/copy-typography.mdc` - только короткое тире `-`
4. `git status` - **много uncommitted** (вся админка + content/ + oauth/)
5. Версии `?v=` - только `python3 bump-assets.py`

---

## Что сделано 7 июля 2026 (админка)

### Данные
- `content/projects/*.yaml` - 13 проектов (миграция из `PROJECTS[]`)
- `content/site.yaml` - featured + projects_order
- `build-projects.py` - читает YAML, `enrich_project()` автозаполняет поля для сайта

### Decap CMS (`/admin`)
- Вход через GitHub OAuth - **работает**
- OAuth proxy: PHP на Timeweb (`oauth/index.php`), не Cloudflare
- Форма проекта: **4 поля** (название, порядок, обложка, фотографии)
- Дизайн под сайт: `admin/custom.css` (бежевый фон, Jost, Cormorant)
- Логотип Key Design вместо Decap

### Деплой
- `prepare-deploy.sh` - build + копирует `admin/`, `oauth/`
- `.github/workflows/deploy.yml` - заготовка CI (secrets не добавлены)

---

## Git и прод

| Что | Статус |
|-----|--------|
| Ветка | `site-clean` |
| Последний коммит | `7fd23fb` - мобильная шапка |
| Uncommitted | **Вся админка**, `content/`, `oauth/`, `build-projects.py`, HTML проектов |
| Прод (сайт) | Админка + OAuth + упрощённая форма - **задеплоено через SFTP** |
| Прод (git) | Отстаёт от рабочей копии - **нужен commit + push** |

**Деплой:** `bash deploy-ru.sh` (SFTP, `deploy.env`)  
**Скрыто на проде:** `approach.html`, `partners.html`

---

## Сайт - структура

| Страница | Файл |
|----------|------|
| Главная | `index.html` - hero + 3 featured, **без контактов** |
| Проекты | `projects.html` - генерируется `build-projects.py` |
| Контакты | `contacts.html` - Яндекс.Карта iframe |
| Проект | `{slug}.html` - генерируется из YAML |

**Контакты:** г. Новосибирск, ул. Инженерная 7, 3 этаж  
**Координаты:** `54.8588216, 83.1087403`  
**Телефон:** `+7 (923) 000-00-36` | **Почта:** `key-des@mail.ru`  
**TG:** `https://t.me/Kristina_Key_des` | **IG:** `https://instagram.com/key_design.studio`

---

## 13 проектов

Данные в `content/projects/{slug}.yaml`. Порядок - `sort_order` в каждом yaml (синхронизируется в `site.yaml` при сборке).

| # | slug | Название |
|---|------|----------|
| 1 | moscow-studio | Москва Студия |
| 2 | kvartira-dubay | Дубай, апартаменты, 180 кв.м. |
| 3 | dom-sinegore | Дом Синегорье |
| 4 | zhk-arkhitektor | г. Москва, ЖК Архитектор |
| 5 | salok-krasoty-tati | Салок красоты tati |
| 6 | laki-park-dom | г. Новосибирск, Лаки Парк, Дом |
| 7 | ns-akadem-pulsar | Новосибирск, Академгородок, Жк Пульсар 1 |
| 8 | kvartal-dekabristov | г. Новосибирск, Квартал Декабристов |
| 9 | nevskaya-dom | г. Новосибирск, Загородный дом, 160 кв.м. |
| 10 | vostochny-vayb | г. Новосибирск, Квартира с Восточным вайбом |
| 11 | kedrovy-ns | г. Новосибирск, Кедровый |
| 12 | kabinet-morozovo | Кабинет-Оружейная Морозово |
| 13 | little-classic | Little Classic |

**Featured на главной** (`content/site.yaml`): `moscow-studio`, `kvartira-dubay`, `dom-sinegore`

**Не путать:** `ns-akadem-pulsar` (Новосибирск) - живой проект. `zhk-pulsar` / `dream-house` - удалены.

---

## Сборка и деплой

```bash
python3 build-projects.py --html-only   # пересобрать HTML из YAML
bash prepare-deploy.sh                  # dist/
bash deploy-ru.sh                         # dist/ → Timeweb SFTP
python3 bump-assets.py                    # после правок CSS/JS
```

---

## Принципы (не ломать)

- Только **короткое тире `-`**, не `—` / `–`
- Названия вкладок - **`.eyebrow`**
- «На главную →» на внутренних страницах
- Главная **без контактов**
- **Commit / deploy** - только по явной просьбе пользователя

---

## Следующие шаги

1. **Commit + push** всей работы по админке (по просьбе пользователя)
2. **GitHub Actions secrets** - автодеплой после Publish Кристины
3. **Invite Кристины** (Write) + `docs/kristina-admin.md`
4. Почистить `assets/contact/office-map.jpg`, мёртвый CSS `.contact-office__map-link`
5. `.gitignore` для `workers/decap-oauth/node_modules`

---

## История чатов

Транскрипты: `~/.cursor/projects/Users-emin-key-design-studio/agent-transcripts/`

| Сессия | Тема |
|--------|------|
| 3 июля | Контакты, Яндекс-карта, удаление проектов |
| 7 июля (утро) | План админки |
| 7 июля (день-вечер) | YAML, Decap, OAuth, упрощение формы, дизайн админки |

---

## Локальный запуск

```bash
cd /Users/emin/key-design-studio
python3 -m http.server 8099
```

- Главная: http://localhost:8099/
- Контакты: http://localhost:8099/contacts.html
- Админка (без OAuth): раскомментировать `local_backend: true` в `admin/config.yml`, `npx decap-server`
