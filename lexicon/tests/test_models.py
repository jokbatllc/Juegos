import pytest
from django.db import IntegrityError

from lexicon.models import Idioma, Categoria, Palabra


pytestmark = pytest.mark.django_db

@pytest.fixture
def idioma_es():
    return Idioma.objects.create(code="es", nombre="Español")


@pytest.fixture
def idioma_en():
    return Idioma.objects.create(code="en", nombre="English")


@pytest.fixture
def categoria_animales():
    return Categoria.objects.create(nombre="Animales", slug="animales", tipo_contenido="wordsearch")


@pytest.fixture
def categoria_tecnologia():
    return Categoria.objects.create(nombre="Tecnología", slug="tecnologia", tipo_contenido="crossword")


@pytest.fixture
def palabra_factory():
    def create_palabra(idioma, texto="palabra"):
        return Palabra.objects.create(texto=texto, idioma=idioma)
    return create_palabra


def test_crea_idiomas_y_categorias(idioma_es, idioma_en, categoria_animales, categoria_tecnologia):
    assert Idioma.objects.count() == 2
    assert Categoria.objects.count() == 2
    assert str(idioma_es) == "Español"
    assert str(categoria_animales) == "Animales"


def test_unique_palabra_por_idioma(idioma_es, palabra_factory):
    palabra_factory(idioma_es, texto="hola")
    with pytest.raises(IntegrityError):
        palabra_factory(idioma_es, texto="hola")


def test_palabra_m2m_categorias(idioma_es, categoria_animales, categoria_tecnologia, palabra_factory):
    palabra = palabra_factory(idioma_es, texto="lobo")
    palabra.categorias.add(categoria_animales, categoria_tecnologia)
    assert palabra.categorias.count() == 2


def test_filtrado_por_idioma_y_categoria(idioma_es, idioma_en, categoria_animales, categoria_tecnologia, palabra_factory):
    palabra_es = palabra_factory(idioma_es, texto="gato")
    palabra_es.categorias.add(categoria_animales)
    palabra_en = palabra_factory(idioma_en, texto="cat")
    palabra_en.categorias.add(categoria_animales)
    palabra_es_tech = palabra_factory(idioma_es, texto="chip")
    palabra_es_tech.categorias.add(categoria_tecnologia)

    qs = Palabra.objects.filter(idioma=idioma_es, categorias=categoria_animales)
    assert list(qs) == [palabra_es]
