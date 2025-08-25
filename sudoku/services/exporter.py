from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from PIL import Image, ImageDraw, ImageFont

from puzzles.models import Exportacion, JuegoGenerado


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def export_to_pdf(juego: JuegoGenerado):
    grid = juego.resultado.get("grid", [])
    solution = juego.resultado.get("solution", [])
    html = render_to_string(
        "sudoku/export.html", {"jg": juego, "grid": grid, "solution": solution}
    )
    pdf_bytes = HTML(string=html).write_pdf()
    file_path = Path(settings.MEDIA_ROOT) / "exports" / "sudoku" / f"{juego.id}.pdf"
    _ensure_dir(file_path)
    file_path.write_bytes(pdf_bytes)
    Exportacion.objects.create(
        juego=juego, formato="pdf", archivo=f"exports/sudoku/{juego.id}.pdf"
    )
    return open(file_path, "rb")


def export_to_png(juego: JuegoGenerado, cell: int = 48, margin: int = 20):
    grid = juego.resultado.get("grid", [])
    if not grid:
        raise ValueError("No hay datos de grid para exportar")
    n = len(grid)
    width = margin * 2 + cell * n
    height = margin * 2 + cell * n
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", cell - 10)
    except OSError:
        font = ImageFont.load_default()

    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            x1 = margin + c * cell
            y1 = margin + r * cell
            x2 = x1 + cell
            y2 = y1 + cell
            draw.rectangle([x1, y1, x2, y2], outline="black")
            if val:
                w, h = draw.textsize(str(val), font=font)
                draw.text(
                    (x1 + (cell - w) / 2, y1 + (cell - h) / 2),
                    str(val),
                    fill="black",
                    font=font,
                )

    file_path = Path(settings.MEDIA_ROOT) / "exports" / "sudoku" / f"{juego.id}.png"
    _ensure_dir(file_path)
    img.save(file_path, "PNG")
    Exportacion.objects.create(
        juego=juego, formato="png", archivo=f"exports/sudoku/{juego.id}.png"
    )
    return open(file_path, "rb")
