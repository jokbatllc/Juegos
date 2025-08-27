from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML

from puzzles.models import Exportacion, JuegoGenerado


def export_to_pdf(juego: JuegoGenerado):
    html = render_to_string(
        "calligraphy/export.html",
        {"jg": juego, "paginas": juego.resultado.get("paginas", [])},
    )
    pdf_bytes = HTML(string=html).write_pdf()

    base = Path(settings.MEDIA_ROOT) / "exports" / "calligraphy"
    base.mkdir(parents=True, exist_ok=True)
    file_path = base / f"{juego.id}.pdf"
    file_path.write_bytes(pdf_bytes)

    Exportacion.objects.create(
        juego=juego, formato="pdf", archivo=f"exports/calligraphy/{juego.id}.pdf"
    )
    return open(file_path, "rb")
