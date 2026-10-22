#!/usr/bin/env bash
# Локальный просмотр сайта: собирает dist и открывает его с чистыми адресами,
# как на Firebase (/services вместо /services.html, /guides -> guides/index.html).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

PORT="${1:-8099}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Ошибка: python3 не найден. Установите Python 3."
  exit 1
fi

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Порт $PORT занят старым сервером — останавливаю его."
  lsof -ti :"$PORT" | xargs kill || true
  sleep 1
fi

echo "Собираю сайт…"
bash prepare-deploy.sh >/dev/null
python3 build-guides.py --preview >/dev/null || true

echo ""
echo "Key Design Studio — локальный сервер"
echo "  Главная:            http://localhost:$PORT/"
echo "  Услуги (оглавление): http://localhost:$PORT/services"
echo "  Дизайн-проект:      http://localhost:$PORT/uslugi-dizajn-proekt"
echo "  Проект с описанием: http://localhost:$PORT/ns-akadem-pulsar"
echo "  Пример статьи:      http://localhost:$PORT/guides/_example"
echo ""
echo "Остановка: Ctrl+C"
echo ""

cd dist
python3 - "$PORT" <<'PY'
import http.server, os, sys

class H(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        local = self.translate_path(path)
        if path != "/" and not os.path.exists(local) and os.path.exists(local + ".html"):
            self.path = path + ".html"
        return super().send_head()
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
PY
