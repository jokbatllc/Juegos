import os
import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from puzzles.models import JuegoGenerado, Exportacion


pytestmark = pytest.mark.django_db

def test_crea_juego_generado():
    juego = JuegoGenerado.objects.create(
        tipo="wordsearch",
        parametros={"size": 10},
        seed=123,
    )
    assert JuegoGenerado.objects.count() == 1
    assert juego.parametros["size"] == 10


def test_exportacion_filefield(tmp_media_dir):
    juego = JuegoGenerado.objects.create(tipo="wordsearch", parametros={"size": 5})
    uploaded = SimpleUploadedFile("test.pdf", b"contenido", content_type="application/pdf")
    export = Exportacion.objects.create(juego=juego, formato="pdf", archivo=uploaded)
    assert os.path.exists(export.archivo.path)
    assert export.archivo.path.startswith(str(settings.MEDIA_ROOT))


def test_parametros_y_resultado_json():
    juego = JuegoGenerado.objects.create(
        tipo="sudoku",
        parametros={"level": 1},
        resultado={"solved": False},
    )
    fetched = JuegoGenerado.objects.get(pk=juego.pk)
    assert fetched.parametros["level"] == 1
    assert fetched.resultado["solved"] is False
