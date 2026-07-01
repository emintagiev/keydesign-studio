# Перенос keydesign.studio на REG.RU

Сайт сейчас на **Cloudflare Workers**. В РФ провайдеры часто режут Cloudflare - без VPN сайт не открывается.

**Решение:** статика на **REG.RU** (тариф Host-Lite) + DNS домена на REG.RU, **без Cloudflare**.

После переключения сайт отдаётся с серверов REG.RU в России - **должен открываться без VPN** (МТС, Мегафон, Билайн, домашний интернет).

---

## Краткий ответ

| Вопрос | Ответ |
|--------|--------|
| Откроется в РФ? | **Да**, если DNS уйдёт с Cloudflare на REG.RU |
| Подходит наш сайт? | **Да** - статический HTML, ~110 МБ, Host-Lite заточен под это |
| SEO и реклама? | **Да** - хостинг не ограничивает Метрику, Директ, Вебmaster |

---

## Шаг 1. Заказать хостинг на REG.RU

1. Войти или зарегистрироваться: https://www.reg.ru/
2. Заказать **Host-Lite** (эконом, только HTML/CSS/JS) - от ~100-170 ₽/мес
3. Привязать домен **keydesign.studio** к услуге хостинга (если домен уже у REG.RU - в том же кабинете)

---

## Шаг 2. Добавить сайт в панели

1. Кабинет REG.RU → **Хостинг** → **Панель управления** (ISPmanager)
2. **Сайты** → добавить **keydesign.studio** и **www.keydesign.studio** (если www не создался сам)
3. Запомнить **корневую папку** сайта - колонка «Корневая директория», обычно:
   - `www/keydesign.studio`
   - полный путь: `/var/www/u1234567/data/www/keydesign.studio/`
   - `u1234567` - логин хостинга

---

## Шаг 3. Включить SSL

1. ISPmanager → **SSL-сертификаты** → Let's Encrypt
2. Выпустить для `keydesign.studio` и `www.keydesign.studio`
3. Включить редирект HTTP → HTTPS (или наш `.htaccess` сделает это сам)

Подождать 15-30 минут после выпуска.

---

## Шаг 4. Переключить DNS (главное)

Пока домен смотрит на Cloudflare - в РФ сайт может не открываться.

### Если домен на REG.RU

1. **Домены** → keydesign.studio → **DNS-серверы и управление зоной**
2. Убрать NS Cloudflare (если стоят)
3. Поставить **DNS-серверы REG.RU** (ns1.reg.ru, ns2.reg.ru - точные имена в кабинете)
4. В зоне DNS должны быть A/CNAME на ваш хостинг (часто создаются автоматически при привязке домена)

### Если домен у другого регистратора

1. У регистратора заменить NS с Cloudflare на NS REG.RU  
   **или**
2. Оставить NS у регистратора, но A-запись `@` и `www` → IP сервера из панели REG.RU (без прокси Cloudflare)

### Cloudflare

- Проект Workers можно **отключить** после успешного переключения
- В Cloudflare для домена больше ничего не нужно

Распространение DNS: от 15 минут до 24-48 часов. Проверка: https://dnschecker.org/#A/www.keydesign.studio

---

## Шаг 5. Загрузить файлы сайта

### Вариант A - FileZilla (проще всего)

1. Локально собрать сайт:

```bash
cd /Users/emin/key-design-studio
bash prepare-deploy.sh
```

2. ISPmanager → **FTP-пользователи** → данные для подключения (хост, логин, порт)
3. FileZilla → SFTP → подключиться
4. Открыть корневую папку сайта (`www/keydesign.studio`)
5. **Удалить** парковочные файлы REG.RU (кроме `webstat`, если есть)
6. Загрузить **содержимое** папки `dist/` (не саму папку `dist`, а файлы внутри: `index.html`, `assets/`, `.htaccess` и т.д.)

### Вариант B - архив через панель

1. `bash prepare-deploy.sh`
2. Запаковать **содержимое** `dist/` в `site.zip`
3. ISPmanager → **Сайты** → keydesign.studio → **Файлы сайта** → Загрузить → распаковать в корень

### Вариант C - deploy-ru.sh (если есть SSH)

```bash
cp deploy.env.example deploy.env
# заполнить DEPLOY_HOST, DEPLOY_USER, DEPLOY_PATH

chmod +x deploy-ru.sh
./deploy-ru.sh
```

`DEPLOY_PATH` - полный путь из панели, например `/var/www/u1234567/data/www/keydesign.studio`

---

## Шаг 6. Проверка

1. https://www.keydesign.studio/ - главная
2. https://www.keydesign.studio/projects.html - проекты
3. https://www.keydesign.studio/privacy.html - политика
4. Квиз «Обсудить проект»
5. **Без VPN** - телефон на мобильном интернете (не Wi-Fi с VPN)

Если по IP/временному URL REG.RU сайт открывается, а по домену нет - ждите DNS.

---

## Дальнейшие обновления сайта

```bash
bash prepare-deploy.sh
# затем снова FileZilla или ./deploy-ru.sh
```

GitHub и Cloudflare для прода больше не обязательны.

---

## Файлы в репозитории

| Файл | Назначение |
|------|------------|
| `prepare-deploy.sh` | Сборка `dist/` |
| `.htaccess` | HTTPS, www, редиректы, кэш, security-заголовки |
| `deploy-ru.sh` | Выкладка по SSH (rsync) |
| `deploy.env.example` | Шаблон доступов |

`_redirects` и `_headers` (Cloudflare) на REG.RU **не нужны**.

---

## Если что-то не работает

| Симптом | Что проверить |
|---------|----------------|
| Без VPN не открывается | DNS ещё на Cloudflare - dnschecker.org |
| Белая страница / 403 | `index.html` в корне сайта, не во вложенной `dist/` |
| Нет HTTPS | SSL в ISPmanager, подождать |
| 500 ошибка | временно переименовать `.htaccess` для теста |
