import pytest
from django.contrib.auth.models import Group, User
from django.db import IntegrityError

from lexicon.models import Idioma, Palabra
from sudoku.forms import SudokuForm


@pytest.mark.django_db
def test_no_duplicate_words():
    lang = Idioma.objects.create(code="es", nombre="Español")
    Palabra.objects.create(texto="hola", idioma=lang)
    with pytest.raises(IntegrityError):
        Palabra.objects.create(texto="hola", idioma=lang)


@pytest.mark.django_db
def test_sudoku_form_sizes():
    assert SudokuForm({"tamaño": 9, "dificultad": "fácil"}).is_valid()
    assert not SudokuForm({"tamaño": 10, "dificultad": "fácil"}).is_valid()


@pytest.mark.django_db
def test_base_template_used(client):
    generador = Group.objects.create(name="generador")
    user = User.objects.create_user("tester", password="pass")
    user.groups.add(generador)
    client.force_login(user)
    urls = [
        "/wordsearch/",
        "/crossword/",
        "/sudoku/",
        "/coloring/",
        "/calligraphy/",
        "/mandala/",
        "/lexicon/",
    ]
    for url in urls:
        resp = client.get(url)
        assert any(t.name == "base.html" for t in resp.templates), url
