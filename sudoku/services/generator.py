from __future__ import annotations

import math
import random
from typing import List


def generate(params: dict) -> dict:
    size = params["tamaño"]
    dificultad = params["dificultad"]
    seed = params.get("seed")
    if seed is not None:
        random.seed(seed)
    root = int(math.sqrt(size))
    if size % root != 0:
        raise ValueError("Tamaño no soportado")
    block_rows = root
    block_cols = size // root

    solution = [[0] * size for _ in range(size)]
    numbers = list(range(1, size + 1))

    def _valid(grid: List[List[int]], r: int, c: int, val: int) -> bool:
        if val in grid[r]:
            return False
        if any(grid[i][c] == val for i in range(size)):
            return False
        br = r - r % block_rows
        bc = c - c % block_cols
        for i in range(br, br + block_rows):
            for j in range(bc, bc + block_cols):
                if grid[i][j] == val:
                    return False
        return True

    def _solve(grid: List[List[int]]) -> bool:
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    random.shuffle(numbers)
                    for val in numbers:
                        if _valid(grid, i, j, val):
                            grid[i][j] = val
                            if _solve(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    _solve(solution)

    grid = [row[:] for row in solution]
    diff_map = {
        "fácil": (0.4, 0.5),
        "medio": (0.55, 0.65),
        "difícil": (0.65, 0.75),
        "experto": (0.75, 0.85),
    }
    low, high = diff_map.get(dificultad, (0.55, 0.65))
    holes = int(size * size * random.uniform(low, high))
    positions = [(r, c) for r in range(size) for c in range(size)]
    random.shuffle(positions)
    for r, c in positions[:holes]:
        grid[r][c] = 0

    return {
        "grid": grid,
        "solution": solution,
        "tamaño": size,
        "dificultad": dificultad,
        "seed": seed,
    }
