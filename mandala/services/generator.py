from __future__ import annotations

import math
import random
from pathlib import Path

from django.conf import settings


SIZE_MAP = {"A4": 800, "A5": 600, "500": 500, "1000": 1000}
COMPLEXITY_MAP = {"simple": 5, "medio": 10, "detallado": 20, "extremo": 40}


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _draw_svg(size: int, segments: int, complexity: str, seed: int | None) -> str:
    rng = random.Random(seed)
    cx = cy = size / 2
    seg_angle = 2 * math.pi / segments
    lines = []
    count = COMPLEXITY_MAP.get(complexity, 10)
    for _ in range(count):
        angle = rng.random() * seg_angle
        radius = rng.random() * (size / 2)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        for k in range(segments):
            a = angle + k * seg_angle
            xk = cx + radius * math.cos(a)
            yk = cy + radius * math.sin(a)
            lines.append(
                f'<line x1="{cx}" y1="{cy}" x2="{xk:.2f}" y2="{yk:.2f}" stroke="black" stroke-width="1" />'
            )
    # add some circles
    for _ in range(count // 4):
        r = rng.random() * (size / 2)
        lines.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r:.2f}" stroke="black" stroke-width="1" fill="none" />'
        )
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">',
        *lines,
        "</svg>",
    ]
    return "".join(svg)


def generate(params: dict, base_id: int) -> list[dict]:
    size = SIZE_MAP.get(params["tamaño"], 800)
    segments = int(params["simetría"])
    complexity = params["complejidad"]
    cantidad = params["cantidad"]
    seed = params.get("semilla")

    base_path = Path(settings.MEDIA_ROOT) / "exports" / "mandala"
    _ensure_dir(base_path)

    results: list[dict] = []
    for i in range(cantidad):
        this_seed = None if seed is None else seed + i
        svg_data = _draw_svg(size, segments, complexity, this_seed)
        file_path = base_path / f"{base_id}_{i+1}.svg"
        file_path.write_text(svg_data, encoding="utf-8")
        results.append(
            {
                "path": f"exports/mandala/{file_path.name}",
                "tamaño": params["tamaño"],
                "complejidad": complexity,
                "simetría": params["simetría"],
            }
        )
    return results
