import pytest
from django.contrib.auth.models import Group
from django.urls import reverse

from puzzles.models import JuegoGenerado


@pytest.mark.django_db
def test_export_grid_png(client, tmp_media_dir, django_user_model):
    g = Group.objects.create(name="generador")
    user = django_user_model.objects.create_user("u", password="p")
    user.groups.add(g)
    jg = JuegoGenerado.objects.create(
        tipo="wordsearch",
        parametros={"ancho": 3, "alto": 3},
        resultado={"grid": ["ABC", "DEF", "GHI"], "palabras": ["ABC"]},
    )
    client.force_login(user)
    url = reverse("wordsearch:export_grid", args=[jg.id, "png"])
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp["Content-Type"] == "image/png"
    assert "attachment" in resp["Content-Disposition"]


@pytest.mark.django_db
def test_list_view_multiple(client, django_user_model):
    user = django_user_model.objects.create_user("u", password="p")
    client.force_login(user)
    j1 = JuegoGenerado.objects.create(
        tipo="wordsearch",
        parametros={},
        resultado={"grid": ["A"], "palabras": ["A"]},
    )
    j2 = JuegoGenerado.objects.create(
        tipo="wordsearch",
        parametros={},
        resultado={"grid": ["B"], "palabras": ["B"]},
    )
    session = client.session
    session['last_wordsearch_ids'] = [j1.id, j2.id]
    session.save()
    resp = client.get(reverse("wordsearch:list"))
    assert resp.status_code == 200
    assert len(resp.context["juegos"]) == 2
