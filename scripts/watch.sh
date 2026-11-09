#!/bin/bash
# =============================================================================
# watch.sh - Recompila el informe al guardar cambios (latexmk -pvc)
# =============================================================================
# Uso:
#   ./scripts/watch.sh
#
# latexmk detecta solo cuando hace falta biber. Requiere Perl (Git Bash ya lo
# trae). Ctrl+C para salir.
# =============================================================================

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v latexmk > /dev/null 2>&1; then
    echo "[ERROR] latexmk no está en el PATH. Instala TeX Live o MiKTeX." >&2
    exit 1
fi

echo "Modo watch sobre thoraxis-article: Ctrl+C para detener."
latexmk -pdf -pvc -outdir=build -jobname=thoraxis-article article.tex
