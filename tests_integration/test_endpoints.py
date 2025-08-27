import pytest
from django.contrib.auth.models import Group, User


@pytest.mark.django_db
def test_main_endpoints(client):
    generador = Group.objects.create(name="generador")
    user = User.objects.create_user("tester", password="pass")
    user.groups.add(generador)
    client.force_login(user)

    urls = [
        "/",
        "/lexicon/",
        "/puzzles/",
        "/wordsearch/",
        "/crossword/",
        "/sudoku/",
        "/coloring/",
        "/calligraphy/",
        "/mandala/",
    ]
    for url in urls:
        resp = client.get(url)
        assert resp.status_code == 200, url

    home = client.get("/")
<<<<<<< ours
    assert "Wordsearch" in home.content.decode()
    assert "Crossword" in home.content.decode()
=======
    assert "Sopa de letras" in home.content.decode()
    assert "Crucigrama" in home.content.decode()
>>>>>>> theirs

    coloring = client.get("/coloring/")
    assert "static" in coloring.content.decode()
