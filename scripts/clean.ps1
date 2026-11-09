# =============================================================================
# Borra la carpeta build/ (PDF y archivos auxiliares).
# =============================================================================
# Uso (desde la raíz del repo):
#   .\scripts\clean.ps1
#
# Todo lo que generan los scripts de compilación vive en build/, así que
# limpiar es borrar esa carpeta.
# =============================================================================

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (Test-Path build) {
    Remove-Item -Recurse -Force build
}
Write-Host "Carpeta build/ eliminada." -ForegroundColor Green
