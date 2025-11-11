```bash
#!/usr/bin/env bash
# combine.sh – führt automatisch alle erzeugten *_part_XXX.txt Dateien zusammen

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <prefix> [output_file]"
  echo "Example: $0 meinvideo meinvideo_complete.txt"
  exit 1
fi

PREFIX="$1"
OUTFILE="${2:-${PREFIX}_complete.txt}"

FILES=$(ls "${PREFIX}"_part_*.txt 2>/dev/null || true)

if [ -z "$FILES" ]; then
  echo "Fehler: Keine Dateien mit Präfix '${PREFIX}_part_*.txt' gefunden."
  exit 2
fi

# Sortiere die Teile numerisch und füge sie zusammen
cat $(ls "${PREFIX}"_part_*.txt | sort) > "$OUTFILE"

echo "✅ Dateien zusammengeführt → $OUTFILE"
```
