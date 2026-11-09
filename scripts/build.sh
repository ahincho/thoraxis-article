#!/bin/bash
# =============================================================================
# build.sh - Compila el informe de Thoraxis
# =============================================================================
# Uso (desde cualquier carpeta):
#   ./scripts/build.sh
#
# Salida: build/thoraxis-article.pdf
# Es el mismo script que ejecuta la CI de GitHub Actions.
#
# Secuencia completa: pdflatex (genera el .bcf), biber (resuelve las citas) y
# dos pasadas más de pdflatex (referencias cruzadas y bibliografía).
# Al final avisa si el resumen ejecutivo excede una página y cuántas marcas
# \pendiente{} quedan en el texto.
# =============================================================================

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

for tool in pdflatex biber; do
    if ! command -v "$tool" > /dev/null 2>&1; then
        echo "[ERROR] $tool no está en el PATH. Instala TeX Live o MiKTeX." >&2
        exit 1
    fi
done

name="thoraxis-article"
mkdir -p build

latex() {
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
        -output-directory=build -jobname="$name" article.tex > /dev/null
}

fail() {
    echo "FALLO en $1 (ver build/$name.$2)"
    grep -m 10 -E '^\./|^!|ERROR' "build/$name.$2" || true
    exit 1
}

printf 'Compilando %s ... ' "$name"
latex || fail pdflatex log
biber --quiet --input-directory=build --output-directory=build "$name" > /dev/null || fail biber blg
latex || fail pdflatex log
latex || fail pdflatex log
echo "OK"

if grep -q 'El resumen ejecutivo excede una hoja' "build/$name.log"; then
    echo "Aviso: el resumen ejecutivo excede una página (la guía pide como máximo una)."
fi

pending="$(grep -rhoF '\pendiente{' config sections | wc -l)"
pending=$((pending - 1)) # la definición de \pendiente en config/commands.tex
if [ "$pending" -gt 0 ]; then
    echo "Aviso: quedan $pending marcas \\pendiente{} en el texto."
fi
