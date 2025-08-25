import random
import unicodedata


def _normalize(word: str) -> str:
    nfkd = unicodedata.normalize('NFKD', word)
    only_ascii = nfkd.encode('ascii', 'ignore').decode('ascii')
    letters = [c for c in only_ascii if c.isalpha()]
    return ''.join(letters).upper()


def _try_place(grid, word, x, y, dx, dy):
    width = len(grid[0])
    height = len(grid)
    for i, ch in enumerate(word):
        xi = x + dx * i
        yi = y + dy * i
        if xi < 0 or yi < 0 or xi >= width or yi >= height:
            return False
        cell = grid[yi][xi]
        if cell is not None and cell != ch:
            return False
    for i, ch in enumerate(word):
        xi = x + dx * i
        yi = y + dy * i
        grid[yi][xi] = ch
    return True


def generate(params: dict, palabras: list[str]) -> dict:
    width = params['ancho']
    height = params['alto']
    seed = params.get('seed')
    rng = random.Random(seed)
    max_len = max(width, height)

    candidates = []
    for w in palabras:
        nw = _normalize(w)
        if nw and len(nw) <= max_len:
            candidates.append(nw)
    if len(candidates) < params['num_palabras']:
        raise ValueError('No hay suficientes palabras para generar la sopa')
    rng.shuffle(candidates)

    grid = [[None for _ in range(width)] for _ in range(height)]
    soluciones = []
    used = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if params['permitir_diagonales']:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if not params['permitir_invertidas']:
        directions = [d for d in directions if d[0] >= 0 and d[1] >= 0]

    for word in candidates:
        if len(used) >= params['num_palabras']:
            break
        placed = False
        for _ in range(200):
            dx, dy = rng.choice(directions)
            if dx == 0:
                xs = list(range(0, width))
            elif dx > 0:
                xs = list(range(0, width - len(word) + 1))
            else:
                xs = list(range(len(word) - 1, width))
            if dy == 0:
                ys = list(range(0, height))
            elif dy > 0:
                ys = list(range(0, height - len(word) + 1))
            else:
                ys = list(range(len(word) - 1, height))
            if not xs or not ys:
                continue
            x = rng.choice(xs)
            y = rng.choice(ys)
            if _try_place(grid, word, x, y, dx, dy):
                soluciones.append({
                    'palabra': word,
                    'fila_inicio': y,
                    'col_inicio': x,
                    'dx': dx,
                    'dy': dy,
                    'longitud': len(word),
                })
                used.append(word)
                placed = True
                break
        if not placed:
            continue
    if len(used) < params['num_palabras']:
        raise ValueError('No se pudieron colocar todas las palabras')

    fill_chars = params['caracteres_relleno']
    for y in range(height):
        for x in range(width):
            if grid[y][x] is None:
                grid[y][x] = rng.choice(fill_chars)
    grid_strings = [''.join(row) for row in grid]
    return {
        'grid': grid_strings,
        'soluciones': soluciones,
        'palabras': used,
        'ancho': width,
        'alto': height,
        'seed': seed,
    }
