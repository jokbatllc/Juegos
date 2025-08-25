from __future__ import annotations

from pathlib import Path
import zipfile

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML

from puzzles.models import Exportacion, JuegoGenerado


def export_to_pdf(juego: JuegoGenerado):
    img_paths = [Path(settings.MEDIA_ROOT) / p for p in juego.resultado]
    html = render_to_string(
        "mandala/export.html", {"images": [p.as_uri() for p in img_paths], "jg": juego}
    )
    pdf_bytes = HTML(string=html).write_pdf()
    base = Path(settings.MEDIA_ROOT) / "exports" / "mandala"
    base.mkdir(parents=True, exist_ok=True)
    file_path = base / f"{juego.id}.pdf"
    file_path.write_bytes(pdf_bytes)
    Exportacion.objects.create(
        juego=juego, formato="pdf", archivo=f"exports/mandala/{juego.id}.pdf"
    )
    return open(file_path, "rb")


def export_to_zip(juego: JuegoGenerado):
    img_paths = [Path(settings.MEDIA_ROOT) / p for p in juego.resultado]
    base = Path(settings.MEDIA_ROOT) / "exports" / "mandala"
    base.mkdir(parents=True, exist_ok=True)
    file_path = base / f"{juego.id}.zip"
    with zipfile.ZipFile(file_path, "w") as zf:
        for p in img_paths:
            zf.write(p, arcname=p.name)
    Exportacion.objects.create(
        juego=juego, formato="zip", archivo=f"exports/mandala/{juego.id}.zip"
    )
    return open(file_path, "rb")
