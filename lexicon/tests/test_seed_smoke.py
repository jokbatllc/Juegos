import pytest
from django.core.management import call_command

from lexicon.models import Categoria, Idioma, Palabra


@pytest.mark.django_db
def test_seed_smoke():
    call_command("seed_lexicon", per_lang=50, langs="es,en")
    assert Palabra.objects.count() >= 100
    assert Idioma.objects.filter(code="es").exists()
    assert Idioma.objects.filter(code="en").exists()
    assert Categoria.objects.count() >= 10
    pairs = set(Palabra.objects.values_list("texto", "idioma__code"))
    assert len(pairs) == Palabra.objects.count()
