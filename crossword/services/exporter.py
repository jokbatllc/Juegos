from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from PIL import Image, ImageDraw, ImageFont

from puzzles.models import Exportacion, JuegoGenerado


BLOCK_CHARS = {"#", ".", "", None}


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _is_block(cell: str | None) -> bool:
    return cell in BLOCK_CHARS


def export_to_pdf(juego: JuegoGenerado):
    grid = juego.resultado.get("grid", [])
    definiciones = juego.resultado.get("definiciones", [])
    html = render_to_string(
        "crossword/export.html",
        {"jg": juego, "grid": grid, "definiciones": definiciones},
    )
    pdf_bytes = HTML(string=html).write_pdf()

    file_path = Path(settings.MEDIA_ROOT) / "exports" / "crossword" / f"{juego.id}.pdf"
    _ensure_dir(file_path)
    file_path.write_bytes(pdf_bytes)

    Exportacion.objects.create(
        juego=juego,
        formato="pdf",
        archivo=f"exports/crossword/{juego.id}.pdf",
    )
    return open(file_path, "rb")


def export_to_png(juego: JuegoGenerado, cell: int = 48, margin: int = 20):
    grid = juego.resultado.get("grid", [])
    if not grid:
        raise ValueError("No hay datos de grid para exportar")
    ancho = len(grid[0])
    alto = len(grid)
    width = margin * 2 + cell * ancho
    height = margin * 2 + cell * alto
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", cell - 10)
    except OSError:
        font = ImageFont.load_default()

    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            x1 = margin + x * cell
            y1 = margin + y * cell
            x2 = x1 + cell
            y2 = y1 + cell
            if _is_block(ch):
                draw.rectangle([x1, y1, x2, y2], fill="black", outline="black")
            else:
                draw.rectangle([x1, y1, x2, y2], fill="white", outline="black")
                w, h = draw.textsize(ch, font=font)
                draw.text((x1 + (cell - w) / 2, y1 + (cell - h) / 2), ch, fill="black", font=font)

    file_path = Path(settings.MEDIA_ROOT) / "exports" / "crossword" / f"{juego.id}.png"
    _ensure_dir(file_path)
    img.save(file_path, "PNG")

    Exportacion.objects.create(
        juego=juego,
        formato="png",
        archivo=f"exports/crossword/{juego.id}.png",
    )
    return open(file_path, "rb")
