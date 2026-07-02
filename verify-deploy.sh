#!/usr/bin/env bash
# Compare dist/ bundle with live production (https://www.keydesign.studio)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
BASE="${VERIFY_BASE:-https://www.keydesign.studio}"

bash prepare-deploy.sh >/dev/null

fail=0
check() {
  local path="$1"
  local local_md5 prod_md5
  local_md5=$(md5 -q "dist/$path")
  prod_md5=$(curl -fsSL "$BASE/$path" | md5 -q)
  if [[ "$local_md5" == "$prod_md5" ]]; then
    echo "OK   $path"
  else
    echo "FAIL $path"
    echo "     local: $local_md5"
    echo "     prod:  $prod_md5"
    fail=1
  fi
}

echo "Verify deploy: $BASE"
echo ""

for f in \
  index.html \
  projects.html \
  services.html \
  app.js \
  styles.css \
  kvartira-dubay.html \
  dom-sinegore.html \
  little-classic.html; do
  check "$f"
done

echo ""
echo "Homepage cards:"
curl -fsSL "$BASE/" | grep -o 'href="[^"]*\.html"' | grep -E 'kvartira-dubay|dom-sinegore|zhk-pulsar|dream-house' || true

echo ""
echo "Projects count:"
curl -fsSL "$BASE/projects.html" | grep -c 'class="proj-grid-card" href=' || true

if [[ "$fail" -ne 0 ]]; then
  echo ""
  echo "Production differs from dist/. Run ./deploy-ru.sh"
  exit 1
fi

echo ""
echo "Production matches dist/."
