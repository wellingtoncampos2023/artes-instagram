#!/usr/bin/env bash
# Uso: tools/render.sh specs/AAAA-MM-DD-HHh.json  -> gera posts/AAAA-MM-DD/HHh-N.jpg
set -e
T="$(cd "$(dirname "$0")" && pwd)"; R="$(dirname "$T")"
[ -d "$T/node_modules" ] || (cd "$T" && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install --silent >/dev/null)
SPEC="$1"; ID=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['id'])" "$SPEC")
DAY=${ID:0:10}; SLOT=${ID:11}; TMP=$(mktemp -d)
python3 "$T/gen.py" "$SPEC" "$TMP" >/dev/null
mkdir -p "$R/posts/$DAY"
for h in "$TMP"/*.html; do n=${h##*-}; n=${n%.html}; (cd "$T" && node shot.mjs "$h" "$R/posts/$DAY/$SLOT-$n.jpg"); done
ls "$R/posts/$DAY/$SLOT"-*.jpg
