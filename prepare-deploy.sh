#!/usr/bin/env bash
# Собирает dist/ для Cloudflare Workers (prod-only правки в dist/, исходники не трогаем)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

python3 build-hero-images.py

rm -rf dist
mkdir -p dist

PROD_HIDDEN=(approach.html partners.html)

for f in *.html; do
  skip=0
  for hidden in "${PROD_HIDDEN[@]}"; do
    if [[ "$f" == "$hidden" ]]; then
      skip=1
      break
    fi
  done
  if [[ "$skip" -eq 0 ]]; then
    cp "$f" dist/
  fi
done

for f in *.css *.js; do
  if [[ -e "$f" ]]; then
    cp "$f" dist/
  fi
done

if [[ -f _redirects ]]; then
  cp _redirects dist/
fi

if [[ -f _headers ]]; then
  cp _headers dist/
fi

cp -R assets dist/

python3 strip-prod-nav.py dist/

echo "Deploy bundle ready: $(find dist -type f | wc -l | tr -d ' ') files"
echo "  hidden on prod: ${PROD_HIDDEN[*]}"
