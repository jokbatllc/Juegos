from __future__ import annotations

from pathlib import Path

import cairosvg
from django.conf import settings

from puzzles.models import Exportacion, JuegoGenerado


def export_svg(svg: str, path: Path):
    path.write_text(svg)
    return path


def export_to_pdf(juego: JuegoGenerado):
    base = Path(settings.MEDIA_ROOT) / "exports" / "maze"
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{juego.id}.pdf"
    svg = Path(settings.MEDIA_ROOT) / juego.resultado["svg"]
    cairosvg.svg2pdf(url=str(svg), write_to=str(path))
    Exportacion.objects.create(
        juego=juego, formato="pdf", archivo=f"exports/maze/{juego.id}.pdf"
    )
    return path


def export_to_png(juego: JuegoGenerado):
    base = Path(settings.MEDIA_ROOT) / "exports" / "maze"
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{juego.id}.png"
    svg = Path(settings.MEDIA_ROOT) / juego.resultado["svg"]
    cairosvg.svg2png(url=str(svg), write_to=str(path))
    Exportacion.objects.create(
        juego=juego, formato="png", archivo=f"exports/maze/{juego.id}.png"
    )
    return path
