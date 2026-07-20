# Key Design Studio - передача контекста

> В новом чате напиши: **«Прочитай HANDOFF.md»**.

**Обновлено:** 20 июля 2026  
**Прод (пока):** https://www.keydesign.studio/ (Timeweb)  
**Firebase (новый, работает везде):** https://keydesign-studio-xxxxx.web.app/  
**Репозиторий:** https://github.com/emintagiev/keydesign-studio (ветка `site-clean`)

---

## ТЕКУЩИЙ ШАГ (выдать пользователю сразу после прочтения HANDOFF)

### ✅ ПЕРЕЕЗД ДОМЕНА НА FIREBASE ЗАВЕРШЁН (20 июля)

- **`www.keydesign.studio`** → Firebase, **Connected**, сертификат `CN=www.keydesign.studio` активен. Проверено вживую: **работает везде (РФ без VPN + Instagram)** ✅
- **apex `keydesign.studio`** → Firebase, `HOST_ACTIVE`, сертификат `CN=keydesign.studio` выпущен (был `CERT_PROPAGATING` в конце сессии - к моменту чтения уже активен).
- **Timeweb НЕ трогали** - живой откат, TTL 1 мин. `admin.keydesign.studio` при необходимости оставить на Timeweb для CMS.

**Как чинили (важный урок):** для `www` Firebase хотел CNAME (не A-записи) - из-за двух A-записей был `HOST_CONFLICT`, висело ~2 часа. Диагностировали через **Hosting API** (`customDomains`, см. раздел «Диагностика подключения кастомного домена»). apex сделали сразу правильно по `requiredDnsUpdates.desired`: A `199.36.158.100` + TXT `hosting-site=...`.

**Текущее состояние DNS в Cloudflare (всё DNS only, серое облако):**
- `keydesign.studio` → A `199.36.158.100` (Firebase) + TXT `hosting-site=keydesign-studio-xxxxx`
- `www.keydesign.studio` → CNAME `keydesign-studio-xxxxx.web.app` (Firebase) + TXT `hosting-site=keydesign-studio-xxxxx`

**Осталось (после переезда, по приоритету):**
1. Проверить apex `https://keydesign.studio/` вживую; решить apex serve-контент vs 301→www (сейчас apex отдаёт тот же сайт, что и www; canonical у нас = www).
2. Закрыть от индексации зеркала `keydesign-studio-xxxxx.web.app` и Netlify (noindex/robots).
3. CI: добавить `firebase deploy` в GitHub Actions.
4. Живой тест формы в Telegram.

**Правило (усвоено дорогой ценой):** перед внесением DNS всегда сверяться с `requiredDnsUpdates.desired` из Hosting API. Поддомены - CNAME, apex - A-записи, всё DNS only. Verify не долбить (rate limit Let's Encrypt 5 фейлов/час).

---

## 🚧 В РАБОТЕ: новый проект «Облака (Орхан)» (не закоммичен, не задеплоен)

Задача пользователя: добавить проект **4-м по порядку**, обложка **cam_25**, и добавить cam_25 в hero-карусель на главной. Сначала проверяем на localhost.

**Что уже сделано (собрано локально, `python3 build-projects.py --html-only` отработал):**
- Слаг **`oblaka-orhan`**. Фото скопированы из `~/Desktop/key design/Облака (Орхан)/` в `assets/projects/oblaka-orhan/interior/` (9 шт: cam_12/24/25/27/31/32/33/34/37).
- `content/projects/oblaka-orhan.yaml` создан (single-gallery, room `interior`, cover `cam_25.jpg`, `sort_order: 4`, i18n `project.16`).
- **Порядок 4-м:** пересчитаны `sort_order` у 10 проектов (salok..little-classic сдвинуты 4→5 … 13→14); `content/site.yaml` `projects_order` - `oblaka-orhan` на 4-й позиции. Проверено в `projects.html` - стоит 4-м ✅
- **i18n** в `app.js`: добавлены `project.16.cat/name/desc` (RU: «Облака (Орхан)», EN: «Oblaka (Orhan)»).
- **Hero-карусель:** cam_25 → `assets/hero/7.jpg` (sips 1400px q68); добавлен 7-й `hero__slide data-hero-bg="assets/hero/7.jpg"` в `index.html` и `key-design-studio.html`; entry добавлен в `build-hero-images.py`.
- Локальный сервер: `python3 -m http.server 8099` (в корне репо). Страницы: `/oblaka-orhan.html`, `/projects.html`, `/` - отдают 200. (Локально clean URL без `.html` не работают - это норма для http.server, на проде ок.)

**❗ЧТО НУЖНО ОТ ПОЛЬЗОВАТЕЛЯ / ДОДЕЛАТЬ:**
- **Метаданные проекта пустые** - нужны: тип (квартира/дом/…), город, площадь (кв.м.), год. Сейчас в yaml `meta` пустые, `eyebrow: ''`, `title_plain: 'Облака (Орхан)'`. Заполнить `title_plain`, `meta`, `eyebrow`, и i18n `project.16.name` (RU/EN) под реальные данные, затем пересобрать.
- Уточнить порядок фото в галерее и правильную обложку (сейчас cover=cam_25, порядок - натуральная сортировка имён).
- Изображения НЕ оптимизированы (оригиналы 300-670 КБ) - прогнать `optimize-images.py` / пережать перед деплоем.
- После апрува: commit + deploy (Timeweb через `prepare-deploy.sh`/CI + Firebase `firebase deploy --only hosting`), не забыть `bump-assets.py` для версий `app.js`/`styles.css`.

---

## Как мы сюда пришли (контекст)

### Проблема
Сайт на Timeweb (российский IP `92.53.96.132`) отлично открывается в РФ без VPN, но **не грузится / душится** у зарубежных и VPN-пользователей (Instagram Stories - основной канал Кристины). Причина - троттлинг трансграничного трафика (ТСПУ/DPI РКН), не вина Timeweb.

### Прорыв (20 июля)
Пользователь нашёл работающий сайт конкурента - [shubochkini.com](https://www.shubochkini.com/) (студия интерьеров, открывается в РФ и через Instagram). Диагностика показала:
- Хостинг **Wix → Google Cloud (`34.149.87.45`) + Fastly CDN**, всё зарубежное, NS зарубежные.
- **Вывод:** сеть Google + Fastly **проходит через ТСПУ**, в отличие от Cloudflare (заблокирован/душат) и Netlify (душат в РФ).

Проверили гипотезу: развернули наш сайт на **Firebase Hosting** (это Google Cloud, IP `199.36.158.100`, фронт Fastly) → **работает везде: РФ без VPN, VPN, Instagram.** Подтверждено пользователем вживую.

### Архитектурное решение
- **Firebase = основной публичный сайт для всех** (бесплатно/копейки, работает везде).
- **Timeweb остаётся** под админку/CMS Кристины (ей в РФ удобно) + как **мгновенный откат** (TTL 1 мин). Год оплачен, не пропадает.
- **Форма заявки** - на Firebase Cloud Function (та же сеть, работает везде). Оставлять на Timeweb нельзя - у загранаудитории отваливалась бы.

### Тупики (НЕ повторять)
Cloudflare proxy (душат в РФ), Netlify (душат в РФ без VPN), Gcore (origin 504), AWS Route53 (домен в CF Registrar, NS не сменить), GeoDNS/CF Load Balancing (~$15/мес, не нужен раз Firebase и так везде работает).

---

## Firebase - что настроено (константы)

| Параметр | Значение |
|----------|----------|
| Google-аккаунт | `emintagiev90@gmail.com` |
| Firebase Project ID | `keydesign-studio-xxxxx` |
| Project number | `491997449676` |
| Hosting URL | `https://keydesign-studio-xxxxx.web.app` |
| План | **Blaze** (billing включён, budget alert $1) |
| Billing-нюанс | Страну в billing сменили с Indonesia (там требовало tax ID/NPWP) на подходящую под карту Visa ...8797 |
| Cloud Function | `brief` в регионе **us-central1** (2nd gen, Node 20) |
| Секреты функции | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (заданы из `deploy.env` через Secret Manager) |
| Cleanup policy | образы старше 1 дня удаляются (чтобы не копилась плата) |

### Firebase CLI
- Установлен глобально (`firebase --version` 15.x). Логин выполнен (`emintagiev90@gmail.com`).
- **Логин интерактивный** - через мой неинтерактивный терминал `firebase login` НЕ работает (`Error: Cannot run login in non-interactive mode`). Если разлогинится - пользователь логинится сам в своём Терминале.
- Деплой: `firebase deploy --only hosting --project keydesign-studio-xxxxx` (или `functions,hosting`).
- Деплой требует подтверждения пользователя (Auto-review) - повторять вызов с request_smart_mode_approval.

### Конфиг-файлы (локально, НЕ закоммичены)
- `firebase.json` - hosting: `public: dist`, `cleanUrls: true`, ignore `api/**` `admin/**` `oauth/**`, rewrite `/api/brief.php` → функция `brief` (с явным `region: us-central1`, `pinTag: true` - без региона rewrite давал 404!).
- `functions/index.js` - порт логики `api/brief.php` / `netlify/functions/brief.js` (honeypot `company`, валидация name+phone, отправка в Telegram всем chat_id). Node 20, глобальный `fetch`.
- `functions/package.json` - `firebase-functions` ^6.
- `.gitignore` - добавлены `functions/node_modules/`, `.firebase/`, `firebase-debug.log`, `*-debug.log`.
- Эти файлы можно коммитить (секретов в них нет), но пока не коммитили - **commit/deploy только по просьбе**.

### Статус формы
- Маршрут проверен: `POST /api/brief.php` без name/phone → `422 validation`; honeypot `company` → `200 ok` (без отправки). Функция напрямую (`https://us-central1-keydesign-studio-xxxxx.cloudfunctions.net/brief`) отвечает.
- **Живой тест доставки в Telegram НЕ делали** (пользователь отложил, чтобы не спамить Кристину). Сделать позже.
- `brief-config.js` endpoint остаётся `/api/brief.php` - менять не нужно, rewrite ловит.

### Диагностика подключения кастомного домена (Hosting API) - ВАЖНО

Если провижининг домена «висит» (статус `Needs setup` / `Minting certificate` долго) - НЕ гадать и НЕ ждать сутки вслепую. Firebase Hosting API отдаёт реальное внутреннее состояние и прямым текстом показывает причину.

Токен: один раз `gcloud auth login` (интерактивно, в Терминале пользователя, аккаунт `emintagiev90@gmail.com`). Дальше токен берётся `gcloud auth print-access-token` (в чат НЕ печатать). Обязателен заголовок `X-Goog-User-Project`, иначе 403 quota.

```bash
TOKEN=$(gcloud auth print-access-token)
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "X-Goog-User-Project: keydesign-studio-xxxxx" \
  "https://firebasehosting.googleapis.com/v1beta1/projects/keydesign-studio-xxxxx/sites/keydesign-studio-xxxxx/customDomains/<DOMAIN>" \
  | python3 -m json.tool
```

Что смотреть:
- `ownershipState`: `OWNERSHIP_ACTIVE` = владение подтверждено (TXT `hosting-site=...`).
- `hostState`: `HOST_ACTIVE` = DNS привязан верно; `HOST_CONFLICT` = конфликтующие/лишние записи; `HOST_UNHOSTED` = Firebase ещё не видит записи (перечитывает DNS периодически).
- `cert.state`: `CERT_VALIDATING` → `CERT_ACTIVE` (готово).
- `issues[]`: конкретные ошибки (напр. ACME challenge failed на IP).
- `requiredDnsUpdates.desired[]`: ЧТО Firebase хочет в DNS - доверять этому, а не своему плану.

**Урок 20 июля:** для `www` Firebase хотел CNAME → `keydesign-studio-xxxxx.web.app` (`certPreference: PROJECT_GROUPED`), а мы поставили две A-записи `199.36.158.100/101`. Из-за `.101` был `HOST_CONFLICT`, ACME падал `199.36.158.101: Request failed` - висело ~2 часа на «Needs setup». Как только заменили обе A-записи на **один CNAME `www → keydesign-studio-xxxxx.web.app` (DNS only)** - `hostState` → `HOST_ACTIVE`, `issues` пусто, пошёл выпуск («Minting certificate»).

Правило DNS для Firebase: **поддомены (`www`) - CNAME на `<site>.web.app`; apex (`keydesign.studio`) - A-записи Firebase** (на голом домене CNAME нельзя). Всё - **DNS only** (серое облако), никакого прокси. Перед переключением сверять с `requiredDnsUpdates.desired`.

---

## План после переключения домена (по приоритету)

1. **Домен** (текущий шаг, см. вверху) - `www` + apex на Firebase, `admin.` на Timeweb.
2. **Проверка** в РФ без VPN + Instagram.
3. **Закрыть от индексации** тестовый `keydesign-studio-xxxxx.web.app` и Netlify-зеркало `peppy-chimera-c97410.netlify.app` (SEO: чтобы не было дублей; canonical уже указывает на www, добавить noindex/robots на зеркалах).
4. **CI на Firebase** - добавить в `.github/workflows/deploy.yml` шаг `firebase deploy` (нужен CI-токен/service account в GitHub Secrets), чтобы push в `site-clean` деплоил и на Timeweb (админка), и на Firebase.
5. **Форма** - живой тест доставки в Telegram.
6. **HANDOFF/доки** обновить под финальную схему.

### SEO-замечание (на будущее, скоро займёмся)
Переезд на Firebase для Яндекса нейтрально-положителен: «российскость» задаётся регионом в Яндекс.Вебмастере, а не сервером; скорость (Fastly) выше Timeweb. Условия: держать один индексируемый URL (закрыть зеркала), выставить регион в Вебмастере, держать Timeweb-откат на случай будущей блокировки Google/Fastly.

---

## Инфраструктура

| Компонент | Значение |
|-----------|----------|
| Хостинг РФ (прод/откат/CMS) | **Timeweb**, shared, `vh464.timeweb.ru`, IP `92.53.96.132`, site ID `9198829`, аккаунт `ca794028` |
| Хостинг мир (новый основной) | **Firebase Hosting** (Google Cloud + Fastly) |
| DNS authority | **Cloudflare** (`anahi.ns.cloudflare.com`, `brett.ns.cloudflare.com`), серое облако (DNS only, orange нельзя) |
| DNS сейчас | `@` → A `199.36.158.100` (Firebase) + TXT `hosting-site=...`; `www` → CNAME `keydesign-studio-xxxxx.web.app` (Firebase) + TXT `hosting-site=...`. Всё **DNS only**, TTL 1 мин / Auto. Timeweb `92.53.96.132` больше не в DNS (только откат) |
| CF Zone ID | `3deda2169b93891d12e6fdf96463164d` |
| CF Account ID | `e67e23f319d133c4b26dd2f7deecf9db` |
| Домен | `keydesign.studio` (регистратор - Cloudflare Registrar, перенос заблокирован) |
| SSL Timeweb | Let's Encrypt, оба домена |
| Netlify-зеркало | `peppy-chimera-c97410.netlify.app` (душат в РФ - оставляем только как запас, потом закрыть от индексации) |

### DNS - как менять
Пользователь правит DNS в панели Cloudflare (dash.cloudflare.com) вручную или через browser MCP. API-токена Cloudflare у модели нет.

### Откат (на Timeweb)
Оба домена теперь на Firebase. Чтобы вернуть на Timeweb: в Cloudflare `www` - удалить CNAME, добавить A `www → 92.53.96.132`; apex - поменять A на `92.53.96.132` (удалить `199.36.158.100`). DNS only, TTL 1 мин → откат ~1-2 мин. Timeweb-сайт живой. Внимание: откат остановит SSL-провижининг на Firebase.

---

## Деплой (Timeweb - существующий)

Push в `site-clean` → `.github/workflows/deploy.yml`: `prepare-deploy.sh` (build `dist/`) → SFTP на Timeweb (`lftp`).
- Ручной: `bash prepare-deploy.sh && bash deploy-ru.sh` (SFTP из `deploy.env`).
- Скрыто на проде: `approach.html`, `partners.html`.
- **CI-флейк 9 июля:** «job was not acquired by Runner» - инфраструктурный сбой GitHub, перезапустить job (сайт мог уже быть выложен вручную).

### Сборка
```bash
python3 build-projects.py --html-only   # HTML из YAML
python3 build-hero-images.py            # hero + thumbs (macOS sips; mobile hero 1-m.jpg)
bash prepare-deploy.sh                  # dist/
python3 bump-assets.py                  # версии (сейчас app.js?v=38, styles.css?v=79)
```

---

## Форма заявки + Telegram

| Файл | Назначение |
|------|------------|
| `brief-config.js` | endpoint `/api/brief.php` |
| `api/brief.php` | Timeweb: POST → Telegram (secrets в `api/brief-secrets.php`, gitignore) |
| `netlify/functions/brief.js` | Netlify-зеркало |
| `functions/index.js` | **Firebase Cloud Function (новый основной)** |

**Бот:** @KeyDesignLeadsBot. **Получатели** (`TELEGRAM_CHAT_ID`): Emin `82721471`, Kristina `1459867475`. Токены в `deploy.env` (gitignore).

---

## Контент / проекты

- 13 проектов, источник правды - `content/projects/*.yaml`, порядок через `sort_order` → `content/site.yaml`.
- `python3 build-projects.py --html-only` пересобирает HTML + `projects.html` + сетку на главной.
- Featured на главной: `moscow-studio`, `kvartira-dubay`, `nevskaya-dom`.
- i18n названий дублировать в `app.js` (`project.N.name` RU + EN).
- Hero: 6 кадров `assets/hero/1-6.jpg`, мобильный LCP `assets/hero/1-m.jpg`. Preloader только desktop (≥981px).

**Контакты:** г. Новосибирск, ул. Инженерная 7, 3 этаж | `+7 (923) 000-00-36` | `key-des@mail.ru` | TG `@Kristina_Key_des` | IG `@key_design.studio`

---

## Админка / CMS

Decap CMS + OAuth (PHP) на Timeweb (`/admin/`, вход через GitHub). Остаётся на Timeweb. Детали - `ADMIN-HANDOFF.md`.

---

## Git

| Что | Значение |
|-----|----------|
| Ветка | `site-clean` |
| HEAD (prod) | `2752924` Improve mobile PageSpeed |
| Не коммитить | `deploy.env`, `api/brief-secrets.php`, `oauth/oauth-secrets.php` |
| Локально не закоммичено | `firebase.json`, `functions/`, обновлённый `.gitignore`, правки `build-projects.py`/`prepare-deploy.sh`, `scripts/setup-gcore-dns.py` (архив), `deploy.env.save`; **новый проект Облака (Орхан):** `content/projects/oblaka-orhan.yaml`, `assets/projects/oblaka-orhan/`, `assets/hero/7.jpg`, правки `sort_order` в 10 yaml, `content/site.yaml`, `app.js`, `index.html`, `key-design-studio.html`, `build-hero-images.py`, сгенерированные `*.html` |

---

## Принципы (не ломать)

- Только **короткое тире `-`**, не `—`/`–` (см. `.cursor/rules/copy-typography.mdc`)
- Названия вкладок меню - `.eyebrow`; «На главную →» на внутренних страницах
- **Commit / deploy - только по явной просьбе пользователя**
- Не слать тестовые заявки на prod без просьбы
- Пользователь любит **пошаговые инструкции блоками** со скринами, пишет «ок»/«готово» между шагами

---

## Проверки (копировать)

```bash
# DNS
dig @8.8.8.8 +short www.keydesign.studio
# Прод/Firebase заголовки (Fastly = Firebase, nginx = Timeweb)
curl -sI https://www.keydesign.studio/ | grep -iE 'HTTP|server|x-served-by'
# Firebase напрямую
curl -sI https://keydesign-studio-xxxxx.web.app/ | head -3
# Форма (маршрут)
curl -s -X POST https://keydesign-studio-xxxxx.web.app/api/brief.php -H 'Content-Type: application/json' -d '{"area":"x"}' -w ' HTTP %{http_code}\n'
```

---

## История чатов

Транскрипты: `~/.cursor/projects/Users-emin-key-design-studio/agent-transcripts/`

| Сессия | Тема |
|--------|------|
| 20 июля | **Прорыв Firebase**: анализ конкурента (Wix/Google/Fastly), деплой на Firebase (работает везде), форма на Cloud Function, Blaze, начали переезд домена |
| 15-20 июля | Ресёрч блокировок РКН 2026, цены Bunny CDN, Firebase-гипотеза |
| 9 июля | Mobile PageSpeed (84→86), deploy rerun, Timeweb тикет (закрыли) |
| 8-9 июля | Netlify зеркало, матрица доступности VPN |
| 7-8 июля | Telegram заявки, hero, deploy fix, Decap CMS, OAuth |

---

## Локальный запуск

```bash
cd /Users/emin/key-design-studio
python3 -m http.server 8099   # http://localhost:8099/
```
