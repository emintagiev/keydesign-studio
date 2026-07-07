#!/usr/bin/env bash
# Одноразовая настройка GitHub Actions secrets для автодеплоя.
# Запуск: bash scripts/setup-github-deploy-secrets.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${DEPLOY_ENV:-$ROOT/deploy.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Нет $ENV_FILE - скопируйте deploy.env.example → deploy.env"
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${DEPLOY_HOST:?DEPLOY_HOST не задан}"
: "${DEPLOY_USER:?DEPLOY_USER не задан}"
: "${DEPLOY_PATH:?DEPLOY_PATH не задан}"
: "${DEPLOY_PASSWORD:?DEPLOY_PASSWORD не задан}"

REPO="${GITHUB_REPO:-emintagiev/keydesign-studio}"
DEPLOY_METHOD="${DEPLOY_METHOD:-sftp}"
DEPLOY_SSH_PORT="${DEPLOY_SSH_PORT:-22}"

for name in DEPLOY_HOST DEPLOY_USER DEPLOY_PATH DEPLOY_PASSWORD DEPLOY_METHOD DEPLOY_SSH_PORT; do
  gh secret set "$name" --body "${!name}" --repo "$REPO"
done

echo "Secrets добавлены в $REPO:"
gh secret list --repo "$REPO"
