from __future__ import annotations

import csv
import io
import json
import re
from typing import Iterable, List

from django.utils.text import slugify

from .models import Categoria, Idioma, Palabra


def normalize_text(s: str) -> str:
    return " ".join(s.strip().lower().split())


def parse_tags(s: str) -> dict:
    if not s:
        return {}
    if isinstance(s, dict):
        return s
    try:
        return json.loads(s)
    except Exception:
        return {}


def ensure_slug(nombre: str) -> str:
    base = slugify(nombre)
    slug = base
    i = 1
    while Categoria.objects.filter(slug=slug).exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


def split_categories(s: str) -> List[str]:
    if not s:
        return []
    parts = re.split(r"[|;]", s)
    return [normalize_text(p) for p in parts if p.strip()]


def bulk_upsert_palabras(rows: Iterable[dict], idioma: Idioma, batch_size: int = 500):
    inserted = duplicated = errors = 0
    cat_cache = {c.nombre: c for c in Categoria.objects.all()}
    buffer: List[Palabra] = []
    relations: List[List[str]] = []
    for row in rows:
        texto = normalize_text(row.get("texto", ""))
        if not texto:
            errors += 1
            continue
        dificultad = int(row.get("dificultad", 1))
        tags = parse_tags(row.get("tags", {}))
        cats = split_categories(row.get("categorias", ""))
        buffer.append(Palabra(texto=texto, idioma=idioma, dificultad=dificultad, tags=tags))
        relations.append(cats)
    for i in range(0, len(buffer), batch_size):
        batch = buffer[i : i + batch_size]
        rel = relations[i : i + batch_size]
        created = Palabra.objects.bulk_create(batch, ignore_conflicts=True)
        inserted += len(created)
        duplicated += len(batch) - len(created)
        for obj, cats in zip(created, rel):
            for cname in cats:
                cat = cat_cache.get(cname)
                if not cat:
                    cat = Categoria.objects.create(nombre=cname, slug=ensure_slug(cname), tipo_contenido="wordsearch")
                    cat_cache[cname] = cat
                obj.categorias.add(cat)
    return {"insertadas": inserted, "duplicadas": duplicated, "errores": errors}
