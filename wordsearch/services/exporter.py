from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML

from puzzles.models import Exportacion, JuegoGenerado


def export_to_pdf(juego: JuegoGenerado):
    """Render the puzzle to PDF and store it under MEDIA_ROOT/exports/wordsearch."""
    html = render_to_string("wordsearch/export.html", {"juego": juego})
    pdf_bytes = HTML(string=html).write_pdf()

    base_path = Path(settings.MEDIA_ROOT) / "exports" / "wordsearch"
    base_path.mkdir(parents=True, exist_ok=True)
    file_path = base_path / f"{juego.id}.pdf"
    file_path.write_bytes(pdf_bytes)

    Exportacion.objects.create(
        juego=juego, formato="pdf", archivo=f"exports/wordsearch/{juego.id}.pdf"
    )
    return file_path


def export_to_png(juego: JuegoGenerado, cell_size: int = 40):
    """Render the puzzle grid as a PNG image."""
    grid = juego.resultado["grid"]
    ancho = len(grid[0])
    alto = len(grid)
    img = Image.new("RGB", (ancho * cell_size, alto * cell_size), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", cell_size - 10)
    except OSError:
        font = ImageFont.load_default()

    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            bbox = draw.textbbox((0, 0), ch, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            tx = x * cell_size + (cell_size - w) / 2
            ty = y * cell_size + (cell_size - h) / 2
            draw.text((tx, ty), ch, fill="black", font=font)

    base_path = Path(settings.MEDIA_ROOT) / "exports" / "wordsearch"
    base_path.mkdir(parents=True, exist_ok=True)
    file_path = base_path / f"{juego.id}.png"
    img.save(file_path, "PNG")

    Exportacion.objects.create(
        juego=juego, formato="png", archivo=f"exports/wordsearch/{juego.id}.png"
    )
    return file_path
