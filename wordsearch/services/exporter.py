from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML

from puzzles.models import Exportacion, JuegoGenerado


def _base_path() -> Path:
    path = Path(settings.MEDIA_ROOT) / "exports" / "wordsearch"
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_grid_pdf(juego: JuegoGenerado, bg: str = "white") -> Path:
    html = render_to_string("wordsearch/export_grid.html", {"juego": juego, "bg": bg})
    pdf_bytes = HTML(string=html).write_pdf()
    file_path = _base_path() / f"{juego.id}_grid.pdf"
    file_path.write_bytes(pdf_bytes)
    Exportacion.objects.create(
        juego=juego,
        formato="pdf",
        archivo=f"exports/wordsearch/{juego.id}_grid.pdf",
    )
    return file_path


def export_grid_png(
    juego: JuegoGenerado, cell_size: int = 40, bg: str = "white"
) -> Path:
    grid = juego.resultado["grid"]
    ancho = len(grid[0])
    alto = len(grid)
    mode = "RGBA" if bg == "transparent" else "RGB"
    bg_color = (255, 255, 255, 0) if bg == "transparent" else "white"
    img = Image.new(mode, (ancho * cell_size, alto * cell_size), bg_color)
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
    draw.rectangle([0, 0, ancho * cell_size - 1, alto * cell_size - 1], outline="black")
    file_path = _base_path() / f"{juego.id}_grid.png"
    img.save(file_path, "PNG")
    Exportacion.objects.create(
        juego=juego,
        formato="png",
        archivo=f"exports/wordsearch/{juego.id}_grid.png",
    )
    return file_path


def export_words_txt(juego: JuegoGenerado) -> Path:
    palabras = juego.resultado.get("palabras", [])
    file_path = _base_path() / f"{juego.id}_words.txt"
    file_path.write_text("\n".join(palabras), encoding="utf-8")
    Exportacion.objects.create(
        juego=juego,
        formato="txt",
        archivo=f"exports/wordsearch/{juego.id}_words.txt",
    )
    return file_path


def export_words_pdf(juego: JuegoGenerado) -> Path:
    palabras = juego.resultado.get("palabras", [])
    html = render_to_string("wordsearch/export_words.html", {"palabras": palabras})
    pdf_bytes = HTML(string=html).write_pdf()
    file_path = _base_path() / f"{juego.id}_words.pdf"
    file_path.write_bytes(pdf_bytes)
    Exportacion.objects.create(
        juego=juego,
        formato="pdf",
        archivo=f"exports/wordsearch/{juego.id}_words.pdf",
    )
    return file_path


def export_solution_pdf(juego: JuegoGenerado, bg: str = "white") -> Path:
    html = render_to_string(
        "wordsearch/export_solution.html", {"juego": juego, "bg": bg}
    )
    pdf_bytes = HTML(string=html).write_pdf()
    file_path = _base_path() / f"{juego.id}_solution.pdf"
    file_path.write_bytes(pdf_bytes)
    Exportacion.objects.create(
        juego=juego,
        formato="pdf",
        archivo=f"exports/wordsearch/{juego.id}_solution.pdf",
    )
    return file_path


def export_solution_png(
    juego: JuegoGenerado, cell_size: int = 40, bg: str = "white"
) -> Path:
    return export_grid_png(juego, cell_size=cell_size, bg=bg)
