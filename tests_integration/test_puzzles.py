import pytest
from django.contrib.auth.models import Group, User
from django.urls import reverse

from lexicon.models import Idioma, Palabra


@pytest.fixture
def generador_user(db):
    group = Group.objects.create(name="generador")
    user = User.objects.create_user(username="maker", password="maker123")
    user.groups.add(group)
    return user


@pytest.fixture
def lexicon_words(db):
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
    return lang


@pytest.mark.django_db
def test_generate_puzzles(client, generador_user, lexicon_words):
    client.force_login(generador_user)

    ws_data = {
        "idioma": "es",
        "ancho": 8,
        "alto": 8,
        "num_palabras": 5,
        "permitir_diagonales": True,
        "permitir_invertidas": True,
        "caracteres_relleno": "ABCDEFGHIJKLMN",
        "dificultad_min": 1,
        "dificultad_max": 5,
    }
    resp = client.post(reverse("wordsearch:create"), ws_data)
    assert resp.status_code == 302
    detail = client.get(resp.headers["Location"])
    assert "Palabras a buscar" in detail.content.decode()

    cw_data = {
        "idioma": "es",
        "ancho": 8,
        "alto": 8,
        "num_palabras": 5,
        "dificultad_min": 1,
        "dificultad_max": 5,
    }
    resp = client.post(reverse("crossword:create"), cw_data)
    assert resp.status_code == 302
    detail = client.get(resp.headers["Location"])
    assert "Definiciones" in detail.content.decode()

    resp = client.post(reverse("sudoku:create"), {"tamaño": 9, "dificultad": "fácil"})
    assert resp.status_code == 302
    detail = client.get(resp.headers["Location"])
    assert "Sudoku" in detail.content.decode()
