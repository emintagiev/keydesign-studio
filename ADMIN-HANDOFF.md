# Key Design Studio - админка для Кристины (Decap CMS)

> В новом чате напиши: **«Прочитай ADMIN-HANDOFF.md и HANDOFF.md, продолжай»**.

**Обновлено:** 8 июля 2026  
**Репозиторий:** https://github.com/emintagiev/keydesign-studio  
**Ветка:** `site-clean`  
**Прод:** https://www.keydesign.studio/  
**Админка:** https://www.keydesign.studio/admin/  
**Хостинг:** Timeweb (SFTP, `deploy.env`)

---

## Статус: MVP на проде, вход работает

| Что | Статус |
|-----|--------|
| Decap CMS на `/admin` | **На проде** |
| GitHub OAuth (вход) | **Работает** |
| Данные в YAML | **13 проектов** в `content/projects/` |
| Упрощённая форма (4 поля) | **На проде** |
| Дизайн админки под сайт | **На проде** (`admin/custom.css`) |
| Автодеплой после Publish | **Работает** - push в `site-clean` → GitHub Actions → SFTP (~2-5 мин) |
| Invite Кристины на GitHub | **Не сделано** |
| `docs/kristina-admin.md` | **Не создано** |

---

## Как Кристина работает (целевой flow)

1. Открывает https://www.keydesign.studio/admin/
2. **Войти через GitHub** → разрешить
3. Редактирует проект → **Publish**
4. Decap коммитит в GitHub (`content/*.yaml`, фото в `assets/projects/`)
5. CI собирает `dist/` и заливает на Timeweb (**автоматически**, ~2-5 мин)

**Не запускать два деплоя параллельно** - SFTP на Timeweb зависает. В workflow есть `concurrency: cancel-in-progress`.

---

## OAuth (реализовано через PHP на Timeweb, не Cloudflare)

Изначально планировали Cloudflare Worker. На практике сделали **PHP-прокси на том же хостинге**:

| Файл | Назначение |
|------|------------|
| `oauth/index.php` | OAuth proxy (`/auth`, `/callback`) |
| `oauth/oauth-secrets.php` | Client ID + Secret (**в .gitignore**, только на сервере) |
| `oauth/.htaccess` | Роутинг `/oauth/auth`, `/oauth/callback` |

**GitHub OAuth App:** `Key Design Studio CMS`  
**Callback URL:** `https://www.keydesign.studio/oauth/callback?provider=github`

**Decap config** (`admin/config.yml`):
```yaml
backend:
  base_url: https://www.keydesign.studio
  auth_endpoint: oauth/auth
```

**Важно:** `oauth/oauth-secrets.php` не в git. При переносе на новый сервер - скопировать вручную или пересоздать OAuth App.

Запасной вариант: `workers/decap-oauth/` (Cloudflare Worker) - подготовлен, **не задеплоен**.

Документация: `docs/oauth-setup.md` (частично устарела - описывает Cloudflare).

---

## Архитектура данных

Проекты больше **не** в `PROJECTS[]` внутри `build-projects.py`.

| Что | Где |
|-----|-----|
| Метаданные проектов | `content/projects/{slug}.yaml` |
| Featured + порядок | `content/site.yaml` |
| Сборка HTML | `build-projects.py` читает YAML |
| Автозаполнение полей | `enrich_project()` в `build-projects.py` |
| Синхронизация порядка | `sync_site_projects_order()` при сборке |
| Фото | `assets/projects/{slug}/{room}/` |
| i18n переводы | `app.js` - **не в админке** |

`prepare-deploy.sh` запускает `python3 build-projects.py --html-only` перед упаковкой `dist/`.

---

## Форма проекта в админке (4 поля для Кристины)

1. **Название проекта** - `title_plain` (как на сайте, одна строка)
2. **Порядок** - `sort_order` (1, 2, 3…)
3. **Главное фото** - `cover`
4. **Остальные фотографии** - `gallery` (список)

**Скрыто (hidden):** `slug`, `rooms`, `i18n_*`, `published`  
**Генерируется при сборке:** `title_html`, `description`, `carousel_*`, `meta`, `eyebrow` и т.д.

**Старые проекты с комнатами** (`kvartira-dubay`, `dom-sinegore` и др.): `rooms[]` сохранены в yaml, Кристина их не видит. Альбомы по комнатам на сайте работают как раньше.

**Настройки сайта:** только выбор **3 проектов на главную** (relation widget по названию).

---

## Брендинг админки

| Файл | Что |
|------|-----|
| `admin/index.html` | Decap CDN + `custom.css` |
| `admin/custom.css` | Стили сайта: `#f4efe7`, Jost, Cormorant, `#6e4844` |
| `admin/config.yml` | `logo: /assets/logo.png` |
| CSS | Скрыт нижний Decap credit на экране входа |

---

## GitHub Actions (активен)

`.github/workflows/deploy.yml` - push в `site-clean` → build → SFTP (lftp, parallel=4, timeout 30 min).

**Secrets в GitHub** (настроены): `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `DEPLOY_PASSWORD`, `DEPLOY_METHOD`, `DEPLOY_SSH_PORT`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

Локально дублируются в `deploy.env` (gitignored).

---

## Деплой вручную (как сейчас)

```bash
bash deploy-ru.sh          # prepare-deploy.sh + SFTP
# или
bash prepare-deploy.sh     # только dist/
```

`deploy.env` - локально, в `.gitignore`.

---

## Следующие шаги (приоритет)

### 1. Кристина
- [ ] GitHub username Кристины
- [ ] Invite **Write** на `emintagiev/keydesign-studio`
- [ ] `docs/kristina-admin.md` - инструкция на 1 страницу (RU)
- [ ] Убедиться, что написала `/start` боту @KeyDesignLeadsBot (chat_id `1459867475`)

### 2. Доработки по факту использования
- [ ] Новый проект: как задавать `slug` без латиницы (сейчас hidden, файл = slug)
- [ ] Загрузка фото в комнаты старых проектов - через «Медиафайлы» или упростить rooms
- [ ] Проверить relation widget `featured_slugs` после первого Publish Кристины

### 3. Прочее
- [ ] Удалить `workers/decap-oauth/node_modules` из репо / добавить в `.gitignore`
- [ ] Обновить `docs/oauth-setup.md` под PHP-прокси

---

## Файлы админки

| Файл | Назначение |
|------|------------|
| `admin/index.html` | Точка входа Decap |
| `admin/config.yml` | Коллекции и поля |
| `admin/custom.css` | Стили |
| `content/site.yaml` | Featured + projects_order |
| `content/projects/*.yaml` | 13 проектов |
| `oauth/` | GitHub OAuth proxy |
| `scripts/migrate-projects-to-yaml.py` | Одноразовая миграция (уже выполнена) |
| `requirements.txt` | PyYAML |
| `.github/workflows/deploy.yml` | CI (активен) |

---

## Принципы

- Только **короткое тире `-`**
- **Commit / deploy** - только по просьбе пользователя
- Версии `?v=` - только `bump-assets.py`
- i18n (`app.js`) - правит разработчик, не Кристина

---

## История

| Дата | Что |
|------|-----|
| 7 июля (утро) | План Decap, scope, OAuth |
| 7 июля (день) | YAML миграция, Decap, OAuth PHP, вход на проде |
| 7 июля (вечер) | Упрощение формы до 4 полей, дизайн админки, логотип KDS |
| 8 июля | GitHub Actions deploy, Telegram заявки, rename проектов, deploy queue fix |

Транскрипт: `~/.cursor/projects/Users-emin-key-design-studio/agent-transcripts/`
