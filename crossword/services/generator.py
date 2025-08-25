import random
import unicodedata


def _normalize(word: str) -> str:
    nfkd = unicodedata.normalize('NFKD', word)
    only_ascii = nfkd.encode('ascii', 'ignore').decode('ascii')
    letters = [c for c in only_ascii if c.isalpha()]
    return ''.join(letters).upper()


def _try_place(grid, word, x, y, horizontal):
    width = len(grid[0])
    height = len(grid)
    for i, ch in enumerate(word):
        xi = x + i if horizontal else x
        yi = y if horizontal else y + i
        if xi < 0 or yi < 0 or xi >= width or yi >= height:
            return False
        cell = grid[yi][xi]
        if cell not in (None, ch):
            return False
    for i, ch in enumerate(word):
        xi = x + i if horizontal else x
        yi = y if horizontal else y + i
        grid[yi][xi] = ch
    return True


def generate(params: dict, palabras: list[dict]) -> dict:
    width = params['ancho']
    height = params['alto']
    seed = params.get('seed')
    rng = random.Random(seed)
    max_len = max(width, height)

    candidates = []
    for p in palabras:
        w = _normalize(p['texto'])
        if w and len(w) <= max_len:
            candidates.append({'word': w, 'definicion': p['definicion']})
    if len(candidates) < params['num_palabras']:
        raise ValueError('No hay suficientes palabras para generar el crucigrama')
    rng.shuffle(candidates)

    grid = [[None for _ in range(width)] for _ in range(height)]
    usados = []
    defs = []

    for entry in candidates:
        if len(usados) >= params['num_palabras']:
            break
        word = entry['word']
        definicion = entry['definicion']
        colocado = False
        for _ in range(200):
            horizontal = rng.choice([True, False])
            if horizontal:
                xs = list(range(0, width - len(word) + 1))
                ys = list(range(0, height))
            else:
                xs = list(range(0, width))
                ys = list(range(0, height - len(word) + 1))
            if not xs or not ys:
                continue
            x = rng.choice(xs)
            y = rng.choice(ys)
            if _try_place(grid, word, x, y, horizontal):
                usados.append(word)
                defs.append({
                    'palabra': word,
                    'pista': definicion,
                    'fila': y,
                    'col': x,
                    'orientacion': 'H' if horizontal else 'V',
                })
                colocado = True
                break
        if not colocado:
            continue
    if len(usados) < params['num_palabras']:
        raise ValueError('No se pudieron colocar todas las palabras')

    for y in range(height):
        for x in range(width):
            if grid[y][x] is None:
                grid[y][x] = '#'
    grid_strings = [''.join(row) for row in grid]
    return {
        'grid': grid_strings,
        'palabras': usados,
        'definiciones': defs,
        'ancho': width,
        'alto': height,
        'seed': seed,
    }
