# Diagramas

El diagrama de arquitectura del artículo (Figura «Arquitectura de Thoraxis») está hecho con [Excalidraw](https://excalidraw.com), con los logos oficiales de cada tecnología incrustados.

| Archivo | Qué es |
|---|---|
| `thoraxis-architecture.excalidraw` | Fuente editable del diagrama, con los logos incrustados. Se abre en excalidraw.com (*Open*) o con la extensión de Excalidraw para VS Code. |
| `build_excalidraw.py` | Script que genera el `.excalidraw` desde cero: posiciones, colores, textos, flechas y logos. |
| `../figures/thoraxis-architecture.pdf` | Figura vectorial que usa el artículo, con la letra incrustada. |
| `../figures/thoraxis-architecture.svg` | La misma figura en SVG. Carga la letra Virgil desde excalidraw.com, así que necesita internet para verse igual. |

## Editar el diagrama

Hay dos caminos:

- **A mano:** abrir `thoraxis-architecture.excalidraw` en Excalidraw, editarlo y guardarlo en el mismo archivo. Luego exportar a SVG o PNG desde el menú (*Export image*), con fondo y en tema claro, y convertir a PDF (ver abajo). Si se edita a mano, ya no conviene regenerarlo con el script, porque se perderían los cambios.
- **Con el script:** cambiar `build_excalidraw.py` y regenerar:

  ```bash
  python diagrams/build_excalidraw.py <carpeta-de-logos>
  ```

## Logos

Los logos se bajaron con `fetch_icons.py` de [stack-diagram](https://github.com/caru-ini/stack-diagram) (licencia MIT, commit `1ed53e3`), que busca la marca oficial en svgl, devicon y gilbarbara/logos. Los que no estaban ahí se tomaron del repositorio oficial de cada proyecto:

| Logo | Origen |
|---|---|
| PyTorch, Kaggle, Colab, OpenTelemetry | devicon |
| Databricks, GitHub Actions | gilbarbara/logos |
| FastAPI, Grafana, Angular | svgl |
| MLflow | `mlflow/mlflow`, `assets/icon.svg` |
| ONNX | `onnx/onnx`, `docs/docsgen/source/_static/ONNX-Logo.svg` |
| MONAI | `Project-MONAI/MONAI`, `docs/images/MONAI-logo-color.png` |
| DVC | `treeverse/dvc.org`, `static/logos/dvc.svg` |
| Evidently | `evidentlyai/evidently`, `ui/service/src/assets/evidently-ai-logo.png` (recortado el margen transparente) |
| Datos, visor y revisión | íconos de Lucide |

NiiVue no publica un logo vectorial (su sitio solo tiene un favicon), así que el nodo del visor lleva el logo de Angular y el ícono genérico del visor.

Ningún logo está recoloreado. El de ONNX tiene letras blancas, así que va sobre un recuadro oscuro. Las marcas pertenecen a sus dueños y se usan solo para identificar cada tecnología.

## Exportar a PDF

El PDF del artículo se generó con el exportador oficial de Excalidraw (`exportToSvg` de `@excalidraw/utils` 0.1.2) y se imprimió a PDF desde Chrome, sin márgenes y con el tamaño de página del SVG. Desde Excalidraw basta con exportar a SVG y convertirlo a PDF con cualquier herramienta que respete el tamaño (por ejemplo, imprimirlo a PDF desde Chrome).
