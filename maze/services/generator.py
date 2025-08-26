from __future__ import annotations

import random

CELL = 20


def generate_rect(width: int, height: int, seed: str | None = None) -> tuple[str, str]:
    rng = random.Random(seed)
    w, h = width // 2 * 2 + 1, height // 2 * 2 + 1
    grid = [[1] * w for _ in range(h)]

    def carve(x: int, y: int):
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        rng.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < w and 0 < ny < h and grid[ny][nx] == 1:
                grid[ny - dy // 2][nx - dx // 2] = 0
                grid[ny][nx] = 0
                carve(nx, ny)

    grid[1][1] = 0
    carve(1, 1)
    grid[h - 2][w - 2] = 0

    svg_lines = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 1:
                x0, y0 = x * CELL, y * CELL
                svg_lines.append(
                    f"<rect x='{x0}' y='{y0}' width='{CELL}' height='{CELL}' fill='black'/>"
                )
    svg_content = "".join(svg_lines)
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='{w*CELL}' height='{h*CELL}'>{svg_content}</svg>"

    sol = f"<svg xmlns='http://www.w3.org/2000/svg' width='{w*CELL}' height='{h*CELL}'>"
    sol += svg_content
    sol += f"<polyline points='10,10 {w*CELL-10},{h*CELL-10}' stroke='red' stroke-width='4' fill='none'/></svg>"

    return svg, sol


def generate(params: dict) -> dict:
    shape = params.get("shape")
    seed = params.get("seed")
    if shape != "rect":
        raise NotImplementedError("Solo rectangular implementado")
    svg, sol = generate_rect(params["width"], params["height"], seed)
    return {"svg": svg, "solution": sol}
