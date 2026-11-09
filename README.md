# thoraxis-article

Artículo en LaTeX, **a una sola columna**, del **Proyecto Integrador** del
**Programa en Deep Learning** (UTEC Posgrado): **Thoraxis**, segmentación de
estructuras del tórax en tomografía computarizada. Es el informe final que
pide la guía del proyecto.

> Thoraxis es una herramienta de investigación. No está destinada al
> diagnóstico clínico.

El PDF se llama siempre **`thoraxis-article.pdf`**.

**Obtener el informe:** lanza *Actions → CD - Build Article → Run workflow*
y, si quieres, indica una versión. El PDF queda como artefacto de esa
ejecución durante 90 días (GitHub lo entrega en un `.zip`). Los *Releases*
son solo versiones del repo (`vX.Y.Z`, con las notas): no llevan PDF. Para
revisar un cambio antes de versionarlo, el PDF de cada PR está en los
artefactos de la CI (ver [CI/CD](#cicd)).

Repositorios del proyecto:

| Repo | Contenido |
| --- | --- |
| [thoraxis-model](https://github.com/ahincho/thoraxis-model) | Entrenamiento, evaluación y exportación del modelo |
| [thoraxis-api](https://github.com/ahincho/thoraxis-api) | Servicio de inferencia |
| [thoraxis-web](https://github.com/ahincho/thoraxis-web) | Visor de cortes con la máscara de segmentación |
| **thoraxis-article** | Este informe |

---

## Origen del formato

| Qué | De dónde sale |
| --- | --- |
| Secciones y su contenido; solo el resumen ejecutivo tiene límite (una página como máximo) | Guía del proyecto integrador, sección 3 ("Estructura del Trabajo Final") |
| Artículo a una sola columna, sin límite de páginas, A4, márgenes de 2,5 cm | Decisión del equipo (la guía no fija formato) |
| Century Schoolbook, scripts y lint | Tesis del autor ([ahincho/thesis](https://github.com/ahincho/thesis)) |
| CI/CD y versionado por releases | CV del autor ([ahincho/curriculum-vitae](https://github.com/ahincho/curriculum-vitae)) |
| Citas y referencias | IEEE (`biblatex-ieee` + `biber`); la guía acepta APA o IEEE |

---

## Estructura

```
.
├── article.tex                   # Único punto de entrada: orden de las secciones
├── config/
│   ├── preamble.tex              # Clase, paquetes, márgenes, tipografía, títulos
│   ├── metadata.tex              # Título, integrantes, líder académico, fecha
│   └── commands.tex              # Macros propias (\pendiente, \articleSource...)
├── sections/
│   ├── 00-cover.tex              # 3.1 Portada
│   ├── 01-executive-summary.tex  # 3.2 Resumen ejecutivo (máximo una página)
│   ├── 02-introduction.tex       # 3.3 Introducción
│   ├── 03-data.tex               # 3.4 Datos y preparación
│   ├── 04-development.tex        # 3.5 Desarrollo de la solución
│   ├── 05-evaluation.tex         # 3.6 Evaluación de la solución
│   ├── 06-results-discussion.tex # 3.7 Resultados y discusión
│   └── 07-conclusions.tex        # 3.8 Conclusiones
├── bibliography/
│   └── references.bib            # 3.9 Referencias (IEEE)
├── figures/                      # Imágenes (\graphicspath apunta aquí)
├── scripts/
│   ├── build.sh / build.ps1      # Compilar (Linux/macOS/Git Bash y CI / Windows)
│   ├── watch.sh / watch.ps1      # Recompilar al guardar (latexmk -pvc)
│   └── clean.sh / clean.ps1      # Borrar build/
├── build/                        # Salida: PDF y auxiliares (ignorada por git)
├── .github/
│   ├── pull_request_template.md  # Plantilla de los PR (en español)
│   └── workflows/
│       ├── ci.yml                # Lint (chktex) y compilación en cada push y PR
│       ├── release.yml           # Versión del repo con release-please
│       └── cd.yml                # Compila el informe desde una versión (solo manual)
├── .vscode/                      # Receta de LaTeX Workshop y extensión recomendada
├── .chktexrc                     # Reglas del lint: avisos desactivados y por qué
├── .release-please-config.json   # Configuración de release-please
├── .release-please-manifest.json # Versión actual del repo (la mantiene release-please)
└── CHANGELOG.md                  # Lo genera release-please con la primera versión
```

Cada archivo de `sections/` empieza con un comentario que copia lo que la
guía pide para esa sección y en qué avance se revisa.

### Qué se revisa en cada avance

| Avance | Asesoría | Secciones |
| --- | --- | --- |
| 1. Definición del problema y alcance | 6–13 nov 2026 | Introducción, datos (fuente y acceso), propuesta inicial y dudas de viabilidad |
| 2. Desarrollo inicial y evaluación | 7–11 dic 2026 | Datos preparados, solución base, diseño, métricas y primeros resultados |
| 3. Resultados y preparación del cierre | 1–5 mar 2027 | Comparación con la solución base, análisis de errores y borrador completo |
| Entrega final | 20 mar 2027 | Informe completo, con el resumen ejecutivo al final |

---

## Compilar

Requiere MiKTeX o TeX Live con `pdflatex` y `biber` en el PATH. El PDF sale en
`build/thoraxis-article.pdf`.

La secuencia es `pdflatex` → `biber` → `pdflatex` → `pdflatex`. Los scripts
la ejecutan solos y al final avisan si el resumen ejecutivo pasa de una
página y cuántas marcas `\pendiente{...}` quedan.

Cada script existe en dos versiones con el mismo comportamiento: `.sh` para
Linux, macOS o Git Bash (es la que usa la CI) y `.ps1` para Windows
(PowerShell).

| Acción | Linux, macOS o Git Bash | Windows (PowerShell) |
| --- | --- | --- |
| Compilar | `./scripts/build.sh` | `.\scripts\build.ps1` |
| Recompilar al guardar | `./scripts/watch.sh` | `.\scripts\watch.ps1` |
| Borrar `build/` | `./scripts/clean.sh` | `.\scripts\clean.ps1` |

- **build** usa `pdflatex` y `biber` directamente. En Windows no usa
  `latexmk`, porque el `latexmk` de MiKTeX necesita Perl; MiKTeX instala solo
  los paquetes que falten (`--enable-installer`).
- **watch** usa `latexmk -pvc`, que sí necesita Perl (Git Bash ya lo trae; en
  PowerShell, Perl debe estar en el PATH). `Ctrl+C` para salir.
- **VS Code** con [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
  compila al guardar con la receta de `.vscode/settings.json` (pdflatex →
  biber → pdflatex × 2, sin `latexmk`) y deja `build/article.pdf`. Abre la
  carpeta `thoraxis-article` (*File → Open Folder*), no la carpeta padre: si
  no, VS Code usa tu receta global. Los archivos de `config/` y `sections/`
  empiezan con `% !TEX root = ../article.tex` para que siempre se compile
  `article.tex`.
- Si PowerShell bloquea los scripts por la política de ejecución, se pueden
  lanzar con `powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1`,
  sin cambiar la configuración del equipo.

---

## Escribir

| Qué quieres cambiar | Archivo |
| --- | --- |
| Título, integrantes, líder académico, fecha | `config/metadata.tex` |
| Márgenes, fuente, interlineado, estilo de títulos | `config/preamble.tex` |
| Texto de una sección | `sections/0N-*.tex` |
| Referencias | `bibliography/references.bib` |

### Convenciones

- **Citas (IEEE):** `\parencite{clave}` → [n], numeradas por orden de cita;
  `\textcite{clave}` → Autor et al. [n]. Claves `apellidoAÑO` en minúsculas.
- **Figuras y tablas:** título arriba (`\caption`) y fuente abajo
  (`\articleSource{Elaboración propia.}`). Referenciarlas con
  `Figura~\ref{fig:...}` y `Tabla~\ref{tab:...}`.
- **Pendientes:** `\pendiente{qué falta}` lo marca en rojo en el PDF. Antes de
  entregar no debe quedar ninguno.
- **Resumen ejecutivo:** máximo una página; los scripts lo comprueban.
- **Datos médicos:** nunca se suben a este repo (ni DICOM ni NIfTI). Las
  figuras con cortes deben salir de datos públicos y anonimizados.
- Archivos en **UTF-8 sin BOM** con fin de línea LF y **siempre con tildes**,
  también en comentarios, scripts y workflows. Excepción: los `.ps1` van en
  **UTF-8 con BOM** y fin de línea CRLF, porque sin BOM Windows PowerShell 5.1
  los lee como ANSI y muestra mal las tildes.
- Escapa `&`, `%`, `#` y `_`; usa ` ``comillas'' `, `\ldots` y `--` para rangos.
- Lint local: `chktex -q -I0 -l .chktexrc sections/02-introduction.tex`.

---

## CI/CD

El mismo modelo que el repo del CV, con las recetas de LaTeX de
[`nova-shared-02-pipelines`](https://github.com/ahincho/nova-shared-02-pipelines)
**fijadas a la rama `main`** (`@main`): una mejora en las recetas llega sola a
este repo, sin actualizar un SHA.

- **`ci.yml`**: en cada push y PR a `main`:
  - **Lint** (`reusable-latex-lint.yml`): pasa
    [chktex](https://www.nongnu.org/chktex/) por todos los `.tex`. Cada aviso
    aparece como anotación en la línea del PR y hace fallar la CI.
  - **Build** (`reusable-latex-build.yml`): ejecuta `scripts/build.sh` en la
    imagen completa de TeX Live y deja el PDF como artefacto
    `thoraxis-article` durante 30 días.
- **`release.yml`**: versiona el repo con
  [release-please](https://github.com/googleapis/release-please)
  (`reusable-release-please.yml`). No compila el informe.
- **`cd.yml`**: **solo se ejecuta a mano** y compila el informe desde una
  versión del repo. El PDF queda como artefacto `thoraxis-article-vX.Y.Z`
  durante 90 días; no crea releases.

El modelo tiene tres piezas:

1. **CI** valida cada cambio (lint y compilación).
2. **Release**: release-please crea **tags inmutables** `vX.Y.Z`. Un release
   es una versión de las fuentes, no un PDF.
3. **CD** compila **un tag** cuando necesitas el documento: para cada avance,
   para el asesor o para la entrega final. Como el tag no cambia, la misma
   versión se puede volver a generar en cualquier momento.

### Cómo se versiona el repo

1. Cada merge a `main` hace que release-please lea los commits y abra (o
   actualice) un **PR de release** con la próxima versión y el `CHANGELOG.md`.
   Ese PR se va acumulando: no hace falta versionar después de cada cambio.
2. Al mergear ese PR se crea el release del repo, `vX.Y.Z`, con las notas del
   CHANGELOG y sin PDF.

La versión sale de los commits, en formato
[Conventional Commits](https://www.conventionalcommits.org/es/). Con **squash
merge** el commit toma el **título del PR**, así que ese título debe ser un
commit convencional (`feat: ...`, `fix: ...`).

La primera versión es `0.1.0`. Mientras el repo esté en `0.x`, un cambio
mayor sube la versión menor en lugar de saltar a `1.0.0`
(`bump-minor-pre-major`):

| Commit | En `0.x` | Desde `1.0.0` |
| --- | --- | --- |
| `fix: ...` | `0.2.0` → `0.2.1` | `1.2.0` → `1.2.1` |
| `feat: ...` | `0.2.0` → `0.3.0` | `1.2.0` → `1.3.0` |
| `feat!: ...` o `BREAKING CHANGE:` en el cuerpo | `0.2.0` → `0.3.0` | `1.2.0` → `2.0.0` |
| `docs:`, `ci:`, `chore:`, ... | no cambian la versión | no cambian la versión |

Para el informe: una sección, un resultado o una figura nueva es `feat`;
corregir una cita, una cifra o la redacción es `fix`. Una buena convención es
sacar una versión por hito: cada avance (asesorías 1, 2 y 3) y la entrega
final.

**Pasar a `1.0.0`** (por ejemplo, la versión entregada el 20 de marzo de 2027)
es una decisión explícita: en un PR, escribe la línea `Release-As: 1.0.0` al
final de la descripción.

### Cómo se obtiene el informe

1. En *Actions → CD - Build Article → Run workflow*, indica la versión (por
   ejemplo `v0.1.0`) o déjala vacía para usar la última.
2. El workflow comprueba que el tag exista, compila el informe desde ese tag
   y lo sube como artefacto `thoraxis-article-vX.Y.Z`, con
   `thoraxis-article.pdf` dentro, durante 90 días.
3. Descárgalo desde la página de esa ejecución, en *Artifacts*.

### Flujo de un cambio

Los cambios entran a `main` solo mediante PR.

1. Crea una rama con nombre **en inglés** (`feat/...`, `fix/...`, `docs/...`;
   por ejemplo, `feat/data-section`), edita y compila en local.
2. Abre un PR a `main` con **título convencional en español** (por ejemplo,
   `feat: agrega la sección de datos`). La descripción también va en español
   y sigue la plantilla de `.github/pull_request_template.md`, que GitHub
   carga sola al abrir el PR. La CI pasa el lint y deja el PDF como artefacto
   para revisarlo.
3. Squash merge. release-please actualiza el PR de release.
4. Cuando quieras versionar, mergea el PR de release. Cuando necesites el PDF
   de esa versión, compílalo con `cd.yml`.

### Configuración del repositorio

Ajustes de GitHub de los que depende este flujo (se cambian en *Settings*):

| Ajuste | Valor | Por qué |
| --- | --- | --- |
| Tipos de merge | Solo **squash**, con el título del PR como mensaje | release-please lee un commit por PR; con merge commits duplica entradas |
| *Automatically delete head branches* | Activado | Las ramas mergeadas se borran solas |
| *Allow GitHub Actions to create and approve pull requests* | Activado | release-please abre su PR de release con `GITHUB_TOKEN`; sin esto `release.yml` falla |
| Permisos por defecto del `GITHUB_TOKEN` | Solo lectura | Cada workflow pide en `permissions` lo que necesita |
| *Immutable releases* | Activado | El tag y el release de una versión no se pueden mover ni borrar: el CD compila siempre lo mismo para la misma versión |

---

## Licencia

[Apache-2.0](LICENSE).
