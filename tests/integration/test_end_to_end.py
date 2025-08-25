import pytest
from django.contrib.auth.models import Group, User
from django.urls import reverse

from lexicon.models import Idioma, Palabra
from puzzles.models import Exportacion, JuegoGenerado


@pytest.mark.django_db
def test_wordsearch_end_to_end(client):
    lang = Idioma.objects.create(code="es", nombre="Español")
    words = [
        "uno",
        "dos",
        "tres",
        "cuatro",
        "cinco",
        "seis",
        "siete",
        "ocho",
        "nueve",
        "diez",
    ]
    for w in words:
        Palabra.objects.create(texto=w, idioma=lang)

    group = Group.objects.create(name="generador")
    user = User.objects.create_user(username="maker", password="maker123")
    user.groups.add(group)
    client.force_login(user)

    data = {
        "idioma": "es",
        "ancho": 10,
        "alto": 10,
        "num_palabras": 5,
        "permitir_diagonales": True,
        "permitir_invertidas": True,
        "caracteres_relleno": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "dificultad_min": 1,
        "dificultad_max": 5,
    }

    resp = client.post(reverse("wordsearch:create"), data)
    assert resp.status_code == 302
    jg = JuegoGenerado.objects.latest("id")
    detail = client.get(resp.headers["Location"])
    assert b"Palabras a encontrar" in detail.content
    grid = jg.resultado["grid"]
    assert len(grid) == 10
    assert all(len(row) == 10 for row in grid)

    client.get(reverse("wordsearch:export", args=[jg.id, "pdf"]))
    client.get(reverse("wordsearch:export", args=[jg.id, "png"]))
    assert Exportacion.objects.filter(juego=jg).count() == 2
