# OAuth для админки Decap (GitHub + Cloudflare)

## Почему была ошибка Netlify

Decap с `backend: github` **по умолчанию** пытается авторизоваться через **Netlify** (`api.netlify.com`).  
У нас сайт на Timeweb, Netlify не настроен - поэтому появляется:

`bad_verification_code: The code passed is incorrect or expired`

**Важно:** OAuth-код одноразовый. Если обновить страницу с ошибкой или открыть старую ссылку callback - ошибка будет снова. Нужно начинать вход заново с `/admin`, после настройки своего OAuth-прокси.

---

## Шаг 1. GitHub OAuth App

1. Открой https://github.com/settings/developers
2. **OAuth Apps** -> **New OAuth App**
3. Заполни:
   - **Application name:** `Key Design Studio CMS`
   - **Homepage URL:** `https://www.keydesign.studio`
   - **Authorization callback URL:** `https://decap.keydesign.studio/callback`
4. Сохрани **Client ID** и сгенерируй **Client Secret**

---

## Шаг 2. Cloudflare Worker

В папке `workers/decap-oauth/`:

```bash
cd workers/decap-oauth
npm install
npx wrangler login
npx wrangler secret put GITHUB_OAUTH_ID      # вставь Client ID
npx wrangler secret put GITHUB_OAUTH_SECRET  # вставь Client Secret
npm run deploy
```

В Cloudflare Dashboard:

1. **Workers & Pages** -> `keydesign-decap-oauth`
2. **Settings** -> **Triggers** -> **Custom Domain**
3. Добавь: `decap.keydesign.studio` (зона `keydesign.studio` уже в Cloudflare)

Проверка: открой `https://decap.keydesign.studio` - должно быть `Key Design Decap OAuth proxy`.

---

## Шаг 3. Конфиг админки

В `admin/config.yml` уже указано:

```yaml
backend:
  name: github
  repo: emintagiev/keydesign-studio
  branch: site-clean
  base_url: https://decap.keydesign.studio
  auth_endpoint: auth
```

После деплоя сайта с этим конфигом вход идёт через Cloudflare, не через Netlify.

---

## Шаг 4. Вход в админку

1. Закрой все вкладки с `api.netlify.com` и старыми callback-URL
2. Открой **новую** вкладку: `https://www.keydesign.studio/admin/`
3. **Login with GitHub** -> разрешить доступ
4. Должна открыться панель Decap

Если снова ошибка - проверь, что callback URL в GitHub App **точно** `https://decap.keydesign.studio/callback` (без лишнего слэша в конце).

---

## Локальный тест без OAuth

Для разработки на своём компьютере:

1. В `admin/config.yml` раскомментируй `local_backend: true`
2. В одном терминале: `npx decap-server`
3. В другом: `python3 -m http.server 8099`
4. Открой `http://localhost:8099/admin/` - вход без GitHub

Перед продом снова закомментируй `local_backend`.
