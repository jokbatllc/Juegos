from __future__ import annotations

import math
import uuid
import random
from pathlib import Path

from django.conf import settings
from PIL import Image, ImageDraw

SIZE_MAP = {
    "A4": (595, 842),
    "A5": (420, 595),
    "Carta": (612, 792),
}


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _size_px(tamaño: str) -> tuple[int, int]:
    return SIZE_MAP.get(tamaño, (595, 842))


def _generate_kids(seed: int, complejidad: str, tamaño: str) -> str:
    rng = random.Random(seed)
    width, height = _size_px(tamaño)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    count = {"simple": 5, "medio": 10, "detallado": 20}[complejidad]
    for _ in range(count):
        x1, y1 = rng.randint(0, width - 50), rng.randint(0, height - 50)
        x2, y2 = x1 + rng.randint(30, 150), y1 + rng.randint(30, 150)
        if rng.random() < 0.5:
            draw.rectangle([x1, y1, x2, y2], outline="black", width=3)
        else:
            draw.ellipse([x1, y1, x2, y2], outline="black", width=3)
    file_id = uuid.uuid4().hex
    rel_path = Path("exports") / "coloring" / f"{file_id}.png"
    abs_path = Path(settings.MEDIA_ROOT) / rel_path
    _ensure_dir(abs_path)
    img.save(abs_path, "PNG")
    return str(rel_path)


def _generate_adults(seed: int, complejidad: str, tamaño: str) -> str:
    rng = random.Random(seed)
    width, height = _size_px(tamaño)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    cx, cy = width / 2, height / 2
    max_r = min(width, height) / 2 - 10
    rings = {"simple": 5, "medio": 10, "detallado": 20}[complejidad]
    for i in range(1, rings + 1):
        r = max_r * i / rings
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline="black", width=2)
    lines = {"simple": 8, "medio": 16, "detallado": 32}[complejidad]
    for i in range(lines):
        angle = 2 * math.pi * i / lines
        x = cx + max_r * math.cos(angle)
        y = cy + max_r * math.sin(angle)
        draw.line([cx, cy, x, y], fill="black", width=2)
    file_id = uuid.uuid4().hex
    rel_path = Path("exports") / "coloring" / f"{file_id}.png"
    abs_path = Path(settings.MEDIA_ROOT) / rel_path
    _ensure_dir(abs_path)
    img.save(abs_path, "PNG")
    return str(rel_path)


def generate(params: dict) -> list[dict]:
    rng = random.Random(params.get("seed"))
    cantidad = params.get("cantidad", 1)
    resultados = []
    for _ in range(cantidad):
        seed = rng.randint(0, 1_000_000)
        if params["tipo"] == "kids":
            path = _generate_kids(seed, params["complejidad"], params["tamaño"])
        else:
            path = _generate_adults(seed, params["complejidad"], params["tamaño"])
        resultados.append({"path": path, "tipo": params["tipo"], "complejidad": params["complejidad"]})
    return resultados
