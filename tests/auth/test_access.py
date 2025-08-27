import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from lexicon.models import Idioma, Categoria, Palabra


@pytest.fixture
def setup_groups(db):
    for name in ["editor_contenidos", "generador", "visor"]:
        Group.objects.get_or_create(name=name)


@pytest.fixture
def editor(db, setup_groups):
    User = get_user_model()
    user = User.objects.create_user("editor", password="pass")
    user.groups.add(Group.objects.get(name="editor_contenidos"))
    return user


@pytest.fixture
def maker(db, setup_groups):
    User = get_user_model()
    user = User.objects.create_user("maker", password="pass")
    user.groups.add(Group.objects.get(name="generador"))
    return user


@pytest.fixture
def viewer(db, setup_groups):
    User = get_user_model()
    user = User.objects.create_user("viewer", password="pass")
    user.groups.add(Group.objects.get(name="visor"))
    return user


@pytest.fixture
def lexicon_data(db):
    es = Idioma.objects.create(code="es", nombre="Español")
    cat = Categoria.objects.create(nombre="animales", slug="animales", tipo_contenido="wordsearch")
    for t in ["gato", "perro", "oso"]:
        p = Palabra.objects.create(texto=t, idioma=es)
        p.categorias.add(cat)
    return es, cat


def test_viewer_cannot_import(client, viewer, lexicon_data):
    client.force_login(viewer)
    resp = client.get(reverse("lexicon:import_csv"))
    assert resp.status_code == 403


def test_maker_can_post_wordsearch(client, maker, lexicon_data):
    client.force_login(maker)
    data = {
        "idioma": "es",
        "ancho": 5,
        "alto": 5,
        "num_palabras": 3,
        "permitir_diagonales": "on",
        "permitir_invertidas": "on",
        "caracteres_relleno": "ABC",
        "dificultad_min": 1,
        "dificultad_max": 5,
    }
    resp = client.post(reverse("wordsearch:create"), data)
    assert resp.status_code in (302, 200)


def test_editor_can_access_categoria_create(client, editor):
    client.force_login(editor)
    resp = client.get(reverse("lexicon:categoria_create"))
    assert resp.status_code == 200


def test_anon_redirects_to_login(client):
    resp = client.get(reverse("lexicon:categoria_create"))
    assert resp.status_code == 302
    assert "/accounts/login/" in resp.headers.get("Location", "")
