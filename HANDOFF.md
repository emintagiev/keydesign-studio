# Key Design Studio - передача контекста

> В новом чате напиши: **«Прочитай HANDOFF.md»**.

**Обновлено:** 23 июля 2026  
**Прод:** https://www.keydesign.studio/ (Firebase Hosting + Fastly)  
**Firebase:** https://keydesign-studio-xxxxx.web.app/  
**Репозиторий:** https://github.com/emintagiev/keydesign-studio (ветка `site-clean`)

---

## ТЕКУЩИЙ ШАГ (выдать пользователю сразу после прочтения HANDOFF)

> **Сейчас: правки по сайту.** Работа по рекламе/SEO **на паузе** - зафиксирована ниже, вернёмся после правок.

Пользователь попросил внести изменения на сайте. Рекламу и Яндекс **не продолжаем**, пока не закончим правки. В новом чате: опиши правки по сайту; когда готов вернуться к рекламе - напиши **«продолжаем рекламу»** или **«прочитай HANDOFF, блок реклама»**.

**Правило работы с пользователем по рекламе:** только **step-by-step**, **один шаг за раз**, без длинных списков «сделайте всё сразу». Ждём «готово»/«ок» между шагами.

---

## 🚧 ПАУЗА: реклама и SEO (23 июля) - вернуться после правок сайта

### Стратегия (0 ₽ на старте)

- **Instagram** - основной канал (уже работает). Сайт = точка доверия + портфолио + форма.
- **SEO** - долгая база, бесплатный трафик через 2-6 мес.
- **Яндекс.Вебмастер + карты** - бесплатно, важнее Директа на старте.
- **Яндекс Директ** (30-80 тыс ₽/мес) - **отложен**, бюджета нет.
- **Регион в Вебмастере** - один на сайт (Новосибирская область); Москва идёт через **контент проектов**, не второй регион.

### ✅ Сделано на сайте (код, задеплоено)

Коммиты `2b2f35a`, `cf30200` (+ hero/обложки раньше).

| Что | Детали |
|-----|--------|
| `robots.txt` | https://www.keydesign.studio/robots.txt - Allow /, Disallow admin/oauth/api |
| `sitemap.xml` | 20 URL (главная, about/projects/services/contacts/privacy + 14 проектов) |
| `canonical` + **Open Graph** | на всех страницах через `seo.py` + `build-seo.py` |
| Meta **yandex-verification** | `b31dd3613bec3f68` на всех страницах (`seo.py` → `YANDEX_VERIFICATION`) |
| Тексты description | акцент **Новосибирск** (+ Москва, Дубай в проектах) |
| Редирект | `/key-design-studio` → `/` (301 в `firebase.json`) |
| noindex | `key-design-studio.html`, `approach.html`, `partners.html` |
| Сборка | `prepare-deploy.sh` вызывает `build-seo.py` после `build-projects.py` |

Файлы: `seo.py`, `build-seo.py`, `robots.txt`, `sitemap.xml`.

### ✅ Яндекс.Вебмастер (пользователь)

| Шаг | Статус |
|-----|--------|
| Сайт добавлен | `https://www.keydesign.studio` ✅ |
| Подтверждение прав | **Meta-тег** (DNS TXT на `www` **не работает** - см. урок ниже) ✅ |
| Регион | **Новосибирская область**, ссылка-подтверждение `https://www.keydesign.studio/contacts` - **заявка на модерации до 7 дней** (23 июля) ⏳ |
| Sitemap | добавить/проверить в Вебмастере: `https://www.keydesign.studio/sitemap.xml` |
| Главное зеркало | должно быть `https://www.keydesign.studio` |

**Урок: DNS-верификация на `www` не работает** при CNAME `www → *.web.app` (Firebase). Яндекс DNS резолвит CNAME и **не видит** TXT в Cloudflare на `www`. Решение: **meta-тег** (уже на сайте). TXT на `@` и `www` в Cloudflare можно оставить - не мешают.

### ⏸ Следующий шаг рекламы (когда вернёмся)

**Шаг 1 (текущий незавершённый):** Яндекс Бизнес / карточка организации - поле «Чем занимаетесь и чем выделяетесь». Черновик текста согласован частично, **ещё не вставлен**:

```
Key Design Studio - авторская студия интерьерного дизайна в Новосибирске. Проектируем квартиры, дома и коммерческие пространства: от планировки и 3D-визуализации до рабочих чертежей, комплектации и авторского надзора. Выверяем свет, материалы и каждую деталь - интерьер для жизни, а не только для фото. Слушаем задачу клиента и ведём проект до результата, близкого к визуализации. В портфолио - реализованные объекты в Новосибирске, Москве и других городах.
```

Короткий вариант (если лимит символов):

```
Авторский дизайн интерьера в Новосибирске: квартиры, дома, коммерция. Полный цикл - проект, 3D, чертежи, комплектация, надзор. Продуманный свет и материалы, сопровождение до готового интерьера.
```

**Дальше по очереди (не выдавать все сразу):** 2GIS → Google Search Console → Instagram-ссылки на проекты → тексты к проектам для SEO.

### Ожидания по срокам (0 ₽)

| Срок | Что |
|------|-----|
| 1-2 нед | индексация страниц после sitemap |
| до 7 дней | одобрение региона в Вебмастере |
| 2-4 нед | первые показы в «Поисковые запросы» |
| 3-6 мес | локальные запросы «дизайн интерьера новосибирск» |

---

## ✅ ПЕРЕЕЗД ДОМЕНА НА FIREBASE (20 июля)

- **`www.keydesign.studio`** → Firebase, **Connected**, сертификат `CN=www.keydesign.studio` активен. Проверено вживую: **работает везде (РФ без VPN + Instagram)** ✅
- **apex `keydesign.studio`** → Firebase, `HOST_ACTIVE`, сертификат `CN=keydesign.studio` выпущен (был `CERT_PROPAGATING` в конце сессии - к моменту чтения уже активен).
- **Timeweb НЕ трогали** - живой откат, TTL 1 мин. `admin.keydesign.studio` при необходимости оставить на Timeweb для CMS.

**Как чинили (важный урок):** для `www` Firebase хотел CNAME (не A-записи) - из-за двух A-записей был `HOST_CONFLICT`, висело ~2 часа. Диагностировали через **Hosting API** (`customDomains`, см. раздел «Диагностика подключения кастомного домена»). apex сделали сразу правильно по `requiredDnsUpdates.desired`: A `199.36.158.100` + TXT `hosting-site=...`.

**Текущее состояние DNS в Cloudflare (всё DNS only, серое облако):**
- `keydesign.studio` → A `199.36.158.100` (Firebase) + TXT `hosting-site=keydesign-studio-xxxxx`
- `www.keydesign.studio` → CNAME `keydesign-studio-xxxxx.web.app` (Firebase) + TXT `hosting-site=keydesign-studio-xxxxx`

## ✅ ГОТОВО: проект «г. Новосибирск, ЖК Облака, 80 кв.м.» + правки (20-22 июля)

- Слаг `oblaka-orhan`, 4-й в списке, обложка `cam_25`, hero `7.jpg` в карусели.
- Hero-карусель переставлена: 1-й - гостиная (kedrovy), 7-й - спальня с балдахином (moscow-studio). Маппинг в `build-hero-images.py`.
- ЖК Архитектор: обложка `IMG_4801.JPG` (зелёные диваны).
- Все задеплоено на Firebase.

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

### Конфиг-файлы (в репо)
- `firebase.json`, `functions/` - **закоммичены** (`62a12e1` и далее).
- `seo.py`, `build-seo.py`, `robots.txt`, `sitemap.xml` - **закоммичены** (`2b2f35a`, `cf30200`).

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

## План инфраструктуры (не срочно)

1. Закрыть от индексации зеркала `.web.app` и Netlify (canonical уже на www).
2. CI: `firebase deploy` в GitHub Actions.
3. Живой тест формы в Telegram.
4. Apex 301→www (опционально).

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
python3 build-seo.py                    # canonical, OG, yandex-verification; robots + sitemap
python3 build-hero-images.py            # hero + thumbs (macOS sips; mobile hero 1-m.jpg)
bash prepare-deploy.sh                  # dist/ (включает build-seo)
python3 bump-assets.py                  # версии (сейчас app.js?v=39, styles.css?v=79)
firebase deploy --only hosting --project keydesign-studio-xxxxx
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

- **14 проектов**, источник правды - `content/projects/*.yaml`, порядок через `sort_order` → `content/site.yaml`.
- `python3 build-projects.py --html-only` пересобирает HTML + `projects.html` + сетку на главной.
- Featured на главной: `moscow-studio`, `kvartira-dubay`, `nevskaya-dom`.
- i18n названий дублировать в `app.js` (`project.N.name` RU + EN).
- Hero: **7** кадров `assets/hero/1-7.jpg`, мобильный LCP `assets/hero/1-m.jpg`. Preloader только desktop (≥981px).

**Контакты:** г. Новосибирск, ул. Инженерная 7, 3 этаж | `+7 (923) 000-00-36` | `key-des@mail.ru` | TG `@Kristina_Key_des` | IG `@key_design.studio`

---

## Админка / CMS

Decap CMS + OAuth (PHP) на Timeweb (`/admin/`, вход через GitHub). Остаётся на Timeweb. Детали - `ADMIN-HANDOFF.md`.

---

## Git

| Что | Значение |
|-----|----------|
| Ветка | `site-clean` |
| HEAD (prod) | `cf30200` Yandex meta verification (+ SEO `2b2f35a`, hero/обложки раньше) |
| Не коммитить | `deploy.env`, **`deploy.env.save`**, `api/brief-secrets.php`, `oauth/oauth-secrets.php` |

---

## Принципы (не ломать)

- Только **короткое тире `-`**, не `—`/`–` (см. `.cursor/rules/copy-typography.mdc`)
- Названия вкладок меню - `.eyebrow`; «На главную →» на внутренних страницах
- **Commit / deploy - только по явной просьбе пользователя**
- Не слать тестовые заявки на prod без просьбы
- Пользователь любит **пошаговые инструкции блоками** - **один шаг**, ждём «ок»/«готово». **Не присылать много шагов сразу** (особенно по рекламе/SEO).

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
| 22-23 июля | **SEO старт (0 ₽)**: robots/sitemap/OG/canonical, Яндекс.Вебмастер (meta-тег), регион на модерации, черновик Яндекс Бизнес; **пауза** - правки сайта |
| 20-22 июля | Firebase prod, проект Облака, hero-карусель, обложка Архитектор |
| 20 июля | **Прорыв Firebase**: переезд домена, форма Cloud Function |
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
