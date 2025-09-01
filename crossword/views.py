import random

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import CrosswordForm
from .services import repository, generator, exporter


def index(request):
    """Página de aterrizaje: redirige al formulario de creación."""
    return redirect("crossword:create")


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = CrosswordForm(request.POST)
        if form.is_valid():
            params = form.to_params()

            # Asegurar semilla
            if not params.get("seed"):
                params["seed"] = random.randint(0, 999_999)

            # Obtener palabras según filtros
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
                    tipo="crossword",
                    parametros=params,
                    resultado=resultado,
                    seed=params["seed"],
                    creado_por=request.user if request.user.is_authenticated else None,
                )
                return redirect("crossword:detail", pk=juego.pk)
    else:
        form = CrosswordForm()

    return render(request, "crossword/create.html", {"form": form})


@login_required
def detail(request, pk):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo="crossword")
    return render(request, "crossword/detail.html", {"juego": juego})


@login_required
def export(request, pk, formato):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo="crossword")

    if formato == "pdf":
        file_obj = exporter.export_to_pdf(juego)
        filename = f"crossword_{juego.id}.pdf"
    elif formato == "png":
        file_obj = exporter.export_to_png(juego)
        filename = f"crossword_{juego.id}.png"
    else:
        return HttpResponseBadRequest("Formato no soportado")

    return FileResponse(file_obj, as_attachment=True, filename=filename)
