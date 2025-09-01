from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse

from core.auth import in_group
from puzzles.models import JuegoGenerado
from .utils import DETAIL_URLS


def home(request):
    cards = []

    # Bloque de generadores
    if in_group(request.user, "generador"):
        cards.extend(
            [
                {
                    "name": "Sopa de Letras",
                    "url": reverse("wordsearch:create"),
                    "desc": "Genera sopas parametrizables",
                    "icon": "bi-grid",
                },
                {
                    "name": "Crucigramas",
                    "url": reverse("crossword:create"),
                    "desc": "Rejillas con pistas",
                    "icon": "bi-table",
                },
                {
                    "name": "Sudoku",
                    "url": reverse("sudoku:create"),
                    "desc": "N×N y dificultad",
                    "icon": "bi-123",
                },
                {
                    "name": "Colorear (Niños)",
                    "url": reverse("coloring:create") + "?tipo=kids",
                    "desc": "Figuras simples",
                    "icon": "bi-brush",
                },
                {
                    "name": "Colorear (Adultos)",
                    "url": reverse("coloring:create") + "?tipo=adults",
                    "desc": "Mandalas/detalle",
                    "icon": "bi-flower3",
                },
                {
                    "name": "Caligrafía",
                    "url": reverse("calligraphy:create"),
                    "desc": "Cuadernos PDF",
                    "icon": "bi-pen",
                },
                {
                    "name": "Mandala",
                    "url": reverse("mandala:create"),
                    "desc": "Simetría radial",
                    "icon": "bi-sun",
                },
            ]
        )

    # Bloque de gestión de contenidos (Lexicon)
    if in_group(request.user, "editor_contenidos"):
        cards.append(
            {
                "name": "Léxico",
                "url": reverse("lexicon:index"),
                "desc": "Palabras y categorías",
                "icon": "bi-collection",
            }
        )

    # Búsqueda / recientes / totales
    q = request.GET.get("q")
    juegos = JuegoGenerado.objects.all()
    if request.user.is_authenticated:
        juegos = juegos.filter(creado_por=request.user)
    if q:
        juegos = juegos.filter(tipo__icontains=q)

    recientes_qs = juegos.order_by("-created_at")[:12]
    recientes = []
    for jg in recientes_qs:
        resolver = DETAIL_URLS.get(jg.tipo)
        url = resolver(jg.pk) if resolver else "#"
        recientes.append({"obj": jg, "url": url})

    total_por_tipo = (
        JuegoGenerado.objects.values("tipo").annotate(n=Count("id")).order_by()
    )

    context = {
        "cards": cards,
        "recientes": recientes,
        "total_por_tipo": total_por_tipo,
        "query": q or "",
    }
    return render(request, "core/home.html", context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="visor")
            user.groups.add(group)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "core/signup.html", {"form": form})


def handler403(request, exception=None):
    return render(request, "403.html", status=403)
