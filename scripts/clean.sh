#!/bin/bash
# =============================================================================
# clean.sh - Borra la carpeta build/ (PDF y archivos auxiliares)
# =============================================================================
# Todo lo que generan los scripts de compilación vive en build/, así que
# limpiar es borrar esa carpeta. En Windows: .\scripts\clean.ps1
# =============================================================================

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
rm -rf build
echo "Carpeta build/ eliminada."
