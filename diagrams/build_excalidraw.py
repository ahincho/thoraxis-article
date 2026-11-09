"""Genera diagrams/thoraxis-architecture.excalidraw con los logos incrustados.

Uso (desde la raíz del repositorio):
    python diagrams/build_excalidraw.py <carpeta-de-logos>

La carpeta de logos sale de fetch_icons.py de stack-diagram (licencia MIT), que
baja las marcas oficiales: svgl, devicon, gilbarbara/logos o el repositorio de
cada proyecto. Los logos no se guardan sueltos en el repositorio: quedan
incrustados en el archivo .excalidraw, que se abre y edita en Excalidraw (web o
extensión de VS Code).
"""
import base64
import json
import pathlib
import random
import re
import struct
import sys

LOGOS = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(__file__).with_name("thoraxis-architecture.excalidraw")
random.seed(7)

INK = "#1e1e1e"
MUTED = "#495057"
W, H = 290, 130            # tamaño de cada caja
COLS = [40, 470, 900, 1330]
ROW_CI, ROW_A, ROW_B, ROW_C = 40, 260, 500, 740
FONT = 1                   # Virgil, la letra a mano alzada de Excalidraw

elements, files = [], {}


def base(kind, eid, x, y, w, h, **kw):
    el = {
        "id": eid, "type": kind, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": INK, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1,
        "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False,
        "boundElements": [], "updated": 1, "link": None, "locked": False,
    }
    el.update(kw)
    elements.append(el)
    return el


def text(eid, cx, y, s, size, color=INK, width=None):
    lines = s.split("\n")
    w = width or max(len(line) for line in lines) * size * 0.6
    return base("text", eid, cx - w / 2, y, w, size * 1.25 * len(lines),
                strokeColor=color, text=s, originalText=s, fontSize=size,
                fontFamily=FONT, textAlign="center", verticalAlign="top",
                containerId=None, lineHeight=1.25, baseline=round(size * 0.9))


def logo_size(path):
    data = path.read_bytes()
    if path.suffix == ".png":
        w, h = struct.unpack(">II", data[16:24])
        return data, "image/png", w / h
    s = data.decode("utf-8", "ignore")
    vb = re.search(r'viewBox="([\d.\s-]+)"', s)
    if vb:
        _, _, w, h = map(float, vb.group(1).split())
    else:
        w = float(re.search(r'width="([\d.]+)', s).group(1))
        h = float(re.search(r'height="([\d.]+)', s).group(1))
    return data, "image/svg+xml", w / h


def image(eid, name, x, y, height, max_w=130):
    path = next(LOGOS.glob(f"{name}.*"))
    data, mime, ratio = logo_size(path)
    fid = f"logo-{name}"
    if fid not in files:
        files[fid] = {"mimeType": mime, "id": fid, "created": 1,
                      "dataURL": f"data:{mime};base64,{base64.b64encode(data).decode()}"}
    w = min(height * ratio, max_w)
    base("image", eid, x, y, w, w / ratio, fileId=fid, status="saved",
         scale=[1, 1], strokeColor="transparent")
    return w


def node(nid, col, row, title, subtitle, logos, fill, stroke, logo_h=34, dark=(), max_w=130):
    x, y = COLS[col], row
    # strokeSharpness es el campo de esquinas de las versiones anteriores de
    # Excalidraw (las que usa @excalidraw/utils); roundness, el de las actuales.
    base("rectangle", nid, x, y, W, H, backgroundColor=fill, strokeColor=stroke,
         roundness={"type": 3}, strokeSharpness="round")
    # Fila de logos centrada en la parte superior de la caja.
    widths = []
    for name in logos:
        _, _, ratio = logo_size(next(LOGOS.glob(f"{name}.*")))
        widths.append(min(logo_h * ratio, max_w))
    gap = 12
    total = sum(widths) + gap * (len(widths) - 1)
    cursor = x + (W - total) / 2
    for i, name in enumerate(logos):
        if name in dark:
            # Logo con letras blancas: va sobre un recuadro oscuro, sin recolorearlo.
            base("rectangle", f"{nid}-tile{i}", cursor - 8, y + 6, widths[i] + 16, logo_h + 12,
                 backgroundColor="#343a40", strokeColor="#343a40", strokeWidth=1,
                 roughness=0, roundness={"type": 3}, strokeSharpness="round")
        image(f"{nid}-logo{i}", name, cursor, y + 12, logo_h, max_w)
        cursor += widths[i] + gap
    text(f"{nid}-title", x + W / 2, y + 56, title, 20, width=W - 16)
    text(f"{nid}-sub", x + W / 2, y + 88, subtitle, 14, MUTED, width=W - 16)
    return {"x": x, "y": y, "cx": x + W / 2, "cy": y + H / 2}


def arrow(aid, pts, color=INK, dashed=False, label=None, label_at=None, width=2):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    base("arrow", aid, x0, y0, max(xs) - min(xs), max(ys) - min(ys),
         strokeColor=color, strokeWidth=width,
         strokeStyle="dashed" if dashed else "solid", points=rel,
         startBinding=None, endBinding=None, startArrowhead=None,
         endArrowhead="arrow", lastCommittedPoint=None, strokeSharpness="sharp")
    if label:
        lx, ly = label_at
        text(f"{aid}-label", lx, ly, label, 16, color)


# --- Cajas -------------------------------------------------------------------
datos = node("datos", 0, ROW_A, "Datos públicos de TC", "TotalSegmentator · COVID-19 · LCTSC",
             ["datos"], "#fff3bf", "#f59e0b")
dvc = node("dvc", 1, ROW_A, "Pipeline de DVC", "preparación y versionado",
           ["dvc"], "#c3fae8", "#0c8599")
train = node("train", 2, ROW_A, "Entrenamiento", "PyTorch y MONAI en Colab o Kaggle",
             ["pytorch", "monai", "colab", "kaggle"], "#b2f2bb", "#2f9e44", logo_h=30)
reg = node("reg", 3, ROW_A, "MLflow en Databricks", "corridas y registro de modelos",
           ["mlflow", "databricks"], "#d0bfff", "#7048e8")
ci = node("ci", 2, ROW_CI, "GitHub Actions", "CI/CD y reentrenamiento",
          ["githubactions"], "#eebefa", "#c2255c")
onnx = node("onnx", 3, ROW_B, "Modelo ONNX", "release de thoraxis-model",
            ["onnx"], "#d0bfff", "#7048e8", dark=("onnx",))
api = node("api", 2, ROW_B, "API de inferencia", "FastAPI y ONNX Runtime",
           ["fastapi"], "#a5d8ff", "#1971c2")
web = node("web", 1, ROW_B, "Visor web", "Angular y NiiVue",
           ["visor", "angular"], "#a5d8ff", "#1971c2")
rev = node("rev", 0, ROW_B, "Revisión humana", "MONAI Label o 3D Slicer",
           ["revisor", "monai"], "#ffd8a8", "#e8590c")
mon = node("mon", 2, ROW_C, "Deriva del modelo", "Evidently: entradas y salidas",
           ["evidently"], "#ffc9c9", "#e03131", logo_h=30, max_w=180)
obs = node("obs", 1, ROW_C, "Rendimiento de la API", "OpenTelemetry → Grafana: alertas",
           ["opentelemetry", "grafana"], "#ffec99", "#f08c00")

R, L = W, 0                 # bordes derecho e izquierdo relativos a x
FEED = "#7048e8"            # ciclos de retroalimentación
GRAY = "#868e96"

# --- Camino principal ----------------------------------------------------------
arrow("a1", [(datos["x"] + R, datos["cy"]), (dvc["x"], dvc["cy"])],
      label="descarga", label_at=((datos["x"] + R + dvc["x"]) / 2, datos["cy"] - 30))
arrow("a2", [(dvc["x"] + R, dvc["cy"]), (train["x"], train["cy"])],
      label="versiones", label_at=((dvc["x"] + R + train["x"]) / 2, dvc["cy"] - 30))
arrow("a3", [(train["x"] + R, train["cy"]), (reg["x"], reg["cy"])],
      label="métricas\ny modelos", label_at=((train["x"] + R + reg["x"]) / 2, train["cy"] - 50))
arrow("a4", [(reg["cx"], reg["y"] + H), (onnx["cx"], onnx["y"])],
      label="@champion", label_at=(reg["cx"] + 60, reg["y"] + H + 40))
arrow("a5", [(onnx["x"], onnx["cy"]), (api["x"] + R, api["cy"])],
      label="carga", label_at=((onnx["x"] + api["x"] + R) / 2, onnx["cy"] - 30))
arrow("a6", [(api["x"], api["cy"]), (web["x"] + R, web["cy"])],
      label="máscara\ny volumen", label_at=((api["x"] + web["x"] + R) / 2, api["cy"] - 50))

# --- Monitoreo y ciclos de retroalimentación -----------------------------------
arrow("a7", [(api["cx"], api["y"] + H), (mon["cx"], mon["y"])], GRAY,
      label="estadísticas", label_at=(api["cx"] + 70, api["y"] + H + 40))
# La telemetría de la API va a Grafana; sus alertas avisan al equipo y no
# disparan el reentrenamiento, por eso no tiene flecha hacia GitHub Actions.
x_tel = api["x"] + 50
y_tel = ROW_B + H + 55
arrow("a12", [(x_tel, api["y"] + H), (x_tel, y_tel), (obs["cx"], y_tel), (obs["cx"], obs["y"])], GRAY,
      label="telemetría", label_at=((x_tel + obs["cx"]) / 2 + 40, y_tel - 26))
x_out = reg["x"] + W + 90
arrow("a8", [(mon["x"] + R, mon["cy"]), (x_out, mon["cy"]), (x_out, ci["cy"]), (ci["x"] + R, ci["cy"])],
      FEED, dashed=True, label="alarma\nde deriva", label_at=(x_out + 55, (ci["cy"] + mon["cy"]) / 2))
arrow("a9", [(ci["cx"], ci["y"] + H), (train["cx"], train["y"])], FEED, dashed=True,
      label="lanza en Kaggle", label_at=(ci["cx"] + 85, ci["y"] + H + 25))
arrow("a10", [(web["x"], web["cy"]), (rev["x"] + R, rev["cy"])], FEED, dashed=True,
      label="caso\nmarcado", label_at=((web["x"] + rev["x"] + R) / 2, web["cy"] - 50))
y_mid = ROW_A + H + 55
arrow("a11", [(rev["cx"], rev["y"]), (rev["cx"], y_mid), (dvc["cx"], y_mid), (dvc["cx"], dvc["y"] + H)],
      FEED, dashed=True, label="máscara corregida", label_at=((rev["cx"] + dvc["cx"]) / 2, y_mid + 8))

doc = {
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": files,
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{OUT.name}: {len(elements)} elementos, {len(files)} logos")
