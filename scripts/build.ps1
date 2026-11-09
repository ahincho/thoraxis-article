# =============================================================================
# Compila el informe de Thoraxis: pdflatex, biber y dos pasadas más de pdflatex.
# =============================================================================
# Uso (desde la raíz del repo):
#   .\scripts\build.ps1
#
# Salida: build/thoraxis-article.pdf
#
# Usa pdflatex y biber directamente y no latexmk: en Windows, latexmk de
# MiKTeX necesita Perl instalado, y pdflatex no.
# =============================================================================

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

foreach ($tool in "pdflatex", "biber") {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Host "$tool no está en el PATH. Instala MiKTeX o TeX Live." -ForegroundColor Red
        exit 1
    }
}

$name = "thoraxis-article"
New-Item -ItemType Directory -Force build | Out-Null

$flags = "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-output-directory=build", "-jobname=$name", "--enable-installer"

function Invoke-Step([string]$label, [scriptblock]$step, [string]$log) {
    & $step | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host " FALLO en $label (ver build/$name.$log)" -ForegroundColor Red
        Select-String -Path "build/$name.$log" -Pattern '^\./|^!|ERROR' | Select-Object -First 10 | ForEach-Object Line
        exit 1
    }
}

Write-Host "Compilando $name" -ForegroundColor Cyan -NoNewline
Invoke-Step "pdflatex" { pdflatex @flags article.tex } "log"
Invoke-Step "biber" { biber --quiet --input-directory=build --output-directory=build $name } "blg"
Invoke-Step "pdflatex" { pdflatex @flags article.tex } "log"
Invoke-Step "pdflatex" { pdflatex @flags article.tex } "log"
Write-Host " OK" -ForegroundColor Green

if (Select-String -Path "build/$name.log" -Pattern 'El resumen ejecutivo excede una hoja' -Quiet) {
    Write-Host "Aviso: el resumen ejecutivo excede una página (la guía pide como máximo una)." -ForegroundColor Yellow
}

# Se resta 1 por la definición de \pendiente en config/commands.tex.
$pending = (Get-ChildItem -Recurse -Include *.tex config, sections |
    Select-String -Pattern '\\pendiente\{' -AllMatches | ForEach-Object { $_.Matches.Count } |
    Measure-Object -Sum).Sum - 1
if ($pending -gt 0) {
    Write-Host "Aviso: quedan $pending marcas \pendiente{} en el texto." -ForegroundColor Yellow
}
Write-Host "Listo: build/$name.pdf" -ForegroundColor Green
