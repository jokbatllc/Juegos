import random

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import WordsearchForm
from .services import repository, generator, exporter


def index(request):
    # Aterriza en el formulario de creación
    return redirect("wordsearch:create")


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = WordsearchForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            if not params.get("seed"):
                params["seed"] = random.randint(0, 999999)

            palabras = repository.fetch_palabras(
                params["idioma"],
                params["categorias"],
                params["dificultad_min"],
                params["dificultad_max"],
                params["num_palabras"],
            )
            try:
                resultado = generator.generate(params, palabras)
            except ValueError as e:
                form.add_error(None, str(e))
            else:
                juego = JuegoGenerado.objects.create(
                    tipo="wordsearch",
                    parametros=params,
                    resultado=resultado,
                    seed=params["seed"],
                    creado_por=request.user if request.user.is_authenticated else None,
                )
                return redirect("wordsearch:detail", pk=juego.pk)
    else:
        form = WordsearchForm()

    return render(request, "wordsearch/create.html", {"form": form})


@login_required
def detail(request, pk):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo="wordsearch")
    return render(request, "wordsearch/detail.html", {"juego": juego})


@login_required
def export(request, pk, formato):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo="wordsearch")
    if formato == "pdf":
        file_obj = exporter.export_to_pdf(juego)
        filename = f"wordsearch_{juego.id}.pdf"
    elif formato == "png":
        file_obj = exporter.export_to_png(juego)
        filename = f"wordsearch_{juego.id}.png"
    else:
        raise Http404
    return FileResponse(file_obj, as_attachment=True, filename=filename)
