from __future__ import annotations

import random
from typing import List

from lexicon.models import Palabra


def generate(params: dict) -> dict:
    seed = params.get("seed")
    if seed is not None:
        random.seed(seed)

    idioma = params["idioma"]
    categorias = params.get("categorias") or []
    contenido = params["contenido"]
    num_paginas = params["num_paginas"]
    lineado = params["lineado"]
    fuente = params["fuente"]
    tamaño_letra = params["tamaño_letra"]

    qs = Palabra.objects.filter(idioma__code=idioma)
    if categorias:
        qs = qs.filter(categorias__id__in=categorias)
    palabras = list(qs.values_list("texto", flat=True))
    if not palabras:
        raise ValueError("No hay palabras disponibles para los parámetros dados")

    letras_pool = sorted({ch for w in palabras for ch in w.lower() if ch.isalpha()}) or list("abcdefghijklmnopqrstuvwxyz")

    paginas: List[dict] = []
    for _ in range(num_paginas):
        lineas: List[str] = []
        for _ in range(10):
            if contenido == "letras":
                letra = random.choice(letras_pool)
                linea = " ".join([letra] * 10)
            elif contenido == "palabras":
                palabra = random.choice(palabras)
                linea = " ".join([palabra] * 5)
            else:  # frases
                frase = " ".join(random.choice(palabras) for _ in range(3))
                linea = "  ".join([frase] * 2)
            lineas.append(linea)
        paginas.append(
            {
                "lineas": lineas,
                "lineado": lineado,
                "fuente": fuente,
                "tamaño_letra": tamaño_letra,
            }
        )

    return {
        "paginas": paginas,
        "seed": seed,
        "idioma": idioma,
        "categorias": categorias,
    }
