#!/bin/bash
# Rebuilds assets/fomantic from the config in _fomantic/. Requires Docker.
set -euo pipefail

FOMANTIC_VERSION=2.9.4
OPEN_SANS_VERSION=5.3.0

cd "$(dirname "$0")/.."
OUT=assets/fomantic
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

tar --no-xattrs -cf - -C _fomantic theme.config semantic.json site \
  | docker run --rm -i -e FOMANTIC_VERSION -e OPEN_SANS_VERSION node:22-bookworm-slim sh -c '
      set -e
      mkdir -p /cfg /w && tar -xf - -C /cfg
      cd /w && npm init -y >/dev/null
      npm install --no-audit --no-fund --ignore-scripts \
        fomantic-ui@$FOMANTIC_VERSION @fontsource/open-sans@$OPEN_SANS_VERSION >&2
      cd node_modules/fomantic-ui
      cp /cfg/semantic.json . && cp /cfg/theme.config src/ && cp -r /cfg/site src/site
      npx gulp build >/tmp/gulp.log 2>&1 || { tail -40 /tmp/gulp.log >&2; exit 1; }

      cd dist
      fonts=themes/default/assets/fonts
      open_sans=/w/node_modules/@fontsource/open-sans
      for subset in latin latin-ext; do
        for style in 400-normal 400-italic 700-normal 700-italic; do
          cp $open_sans/files/open-sans-$subset-$style.woff2 $fonts/
        done
      done
      cp $open_sans/LICENSE $fonts/LICENSE_OpenSans.txt

      assets=$(grep -o "url(themes/[^)]*" semantic.min.css | sed "s/^url(//" | sort -u)
      for file in $assets; do [ -f "$file" ] || { echo "missing $file" >&2; exit 1; }; done
      tar -cf - semantic.min.css semantic.min.js $fonts/LICENSE_icons.txt $fonts/LICENSE_OpenSans.txt $assets' > "$TMP"

rm -rf "$OUT" && mkdir -p "$OUT"
tar -xf "$TMP" -C "$OUT"
echo "Fomantic UI $FOMANTIC_VERSION built into $OUT"
