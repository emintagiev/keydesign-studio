#!/usr/bin/env bash
# Собирает dist/ только с файлами сайта (без .git, скриптов и т.д.)
set -euo pipefail

rm -rf dist
mkdir -p dist

for f in *.html *.css *.js; do
  if [ -e "$f" ]; then
    cp "$f" dist/
  fi
done

if [ -f _redirects ]; then
  cp _redirects dist/
fi

cp -R assets dist/

echo "Deploy bundle ready: $(find dist -type f | wc -l | tr -d ' ') files"
