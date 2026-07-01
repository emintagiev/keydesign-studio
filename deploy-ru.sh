#!/usr/bin/env bash
# Сборка dist/ и выкладка на российский хостинг по SSH (rsync)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

ENV_FILE="${DEPLOY_ENV:-$ROOT/deploy.env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  echo "Нет файла deploy.env"
  echo "  cp deploy.env.example deploy.env"
  echo "  # заполните DEPLOY_HOST, DEPLOY_USER, DEPLOY_PATH"
  exit 1
fi

: "${DEPLOY_HOST:?DEPLOY_HOST не задан в deploy.env}"
: "${DEPLOY_USER:?DEPLOY_USER не задан в deploy.env}"
: "${DEPLOY_PATH:?DEPLOY_PATH не задан в deploy.env}"

bash prepare-deploy.sh

DEPLOY_METHOD="${DEPLOY_METHOD:-ssh}"
SSH_PORT="${DEPLOY_SSH_PORT:-22}"

echo ""
echo "Deploy → ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH} (${DEPLOY_METHOD})"
echo ""

if [[ "$DEPLOY_METHOD" == "ftp" || "$DEPLOY_METHOD" == "sftp" ]]; then
  : "${DEPLOY_PASSWORD:?DEPLOY_PASSWORD не задан в deploy.env}"
  if ! command -v lftp >/dev/null 2>&1; then
    echo "Нужен lftp: brew install lftp"
    exit 1
  fi
  if [[ "$DEPLOY_METHOD" == "sftp" ]]; then
    LFTP_OPEN="open -u ${DEPLOY_USER},${DEPLOY_PASSWORD} sftp://${DEPLOY_HOST}:${SSH_PORT}"
  else
    LFTP_OPEN="open -u ${DEPLOY_USER},${DEPLOY_PASSWORD} ${DEPLOY_HOST}"
  fi
  lftp <<EOF
set cmd:fail-exit yes
set net:timeout 30
set net:max-retries 2
set sftp:auto-confirm yes
set ftp:use-feat no
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ftp:passive-mode true
set ssl:verify-certificate no
${LFTP_OPEN}
cd ${DEPLOY_PATH}
mirror -R --delete --verbose dist/ .
quit
EOF
else
  RSYNC_SSH="ssh -p ${SSH_PORT} -o StrictHostKeyChecking=accept-new"
  rsync -avz --delete --progress -e "$RSYNC_SSH" dist/ "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/"
fi

echo ""
echo "Готово. Проверьте: https://www.keydesign.studio/"
echo "Если DNS ещё на Cloudflare - сначала переключите NS (см. HOSTING-RU.md)"
