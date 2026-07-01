#!/usr/bin/env bash
# Локальный просмотр сайта
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

PORT="${1:-8099}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Ошибка: python3 не найден. Установите Python 3."
  exit 1
fi

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Порт $PORT уже занят. Сайт, возможно, уже запущен:"
  echo "  http://localhost:$PORT/"
  echo "  http://127.0.0.1:$PORT/"
  echo ""
  echo "Чтобы остановить: lsof -ti :$PORT | xargs kill"
  exit 0
fi

echo "Key Design Studio - локальный сервер"
echo "  http://localhost:$PORT/"
echo "  http://127.0.0.1:$PORT/privacy.html"
echo ""
echo "Остановка: Ctrl+C"
echo ""

python3 -m http.server "$PORT"
