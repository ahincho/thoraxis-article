# =============================================================================
# Recompila el informe al guardar cambios (latexmk -pvc).
# =============================================================================
# Uso (desde la raíz del repo):
#   .\scripts\watch.ps1
#
# latexmk detecta solo cuando hace falta biber. En Windows, el latexmk de
# MiKTeX necesita Perl instalado (por ejemplo Strawberry Perl, o el de Git for
# Windows en el PATH). Ctrl+C para salir.
# =============================================================================

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

foreach ($tool in "latexmk", "perl") {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Host "$tool no está en el PATH. latexmk necesita MiKTeX o TeX Live y Perl." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Modo watch sobre thoraxis-article: Ctrl+C para detener." -ForegroundColor Cyan
latexmk -pdf -pvc -outdir=build -jobname=thoraxis-article article.tex
