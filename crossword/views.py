<<<<<<< ours
import random

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import CrosswordForm
from .services import repository, generator, exporter


def index(request):
    # Página de aterrizaje: llevar al formulario de creación
    return redirect("crossword:create")
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from core.auth import require_group
from .forms import CrosswordForm
from .services import repository, generator, exporter
from puzzles.models import JuegoGenerado
import random
>>>>>>> theirs


@require_group("generador")
def create(request):
<<<<<<< ours
    if request.method == "POST":
        form = CrosswordForm(request.POST)
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
=======
    if request.method == 'POST':
        form = CrosswordForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            if not params.get('seed'):
                params['seed'] = random.randint(0, 999999)
            palabras = repository.fetch_palabras(
                params['idioma'],
                params['categorias'],
                params['dificultad_min'],
                params['dificultad_max'],
                params['num_palabras'],
>>>>>>> theirs
            )
            try:
                resultado = generator.generate(params, palabras)
            except ValueError as e:
                form.add_error(None, str(e))
            else:
                juego = JuegoGenerado.objects.create(
<<<<<<< ours
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
=======
                    tipo='crossword',
                    parametros=params,
                    resultado=resultado,
                    seed=params['seed'],
                    creado_por=request.user if request.user.is_authenticated else None,
                )
                return redirect('crossword:detail', pk=juego.pk)
    else:
        form = CrosswordForm()
    return render(request, 'crossword/create.html', {'form': form})
>>>>>>> theirs


@login_required
def detail(request, pk):
<<<<<<< ours
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo="crossword")
    return render(request, "crossword/detail.html", {"juego": juego})
=======
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='crossword')
    return render(request, 'crossword/detail.html', {'juego': juego})
>>>>>>> theirs


@login_required
def export(request, pk, formato):
<<<<<<< ours
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo="crossword")
    if formato == "pdf":
        file_obj = exporter.export_to_pdf(juego)
        filename = f"crossword_{juego.id}.pdf"
    elif formato == "png":
=======
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='crossword')
    if formato == 'pdf':
        file_obj = exporter.export_to_pdf(juego)
        filename = f"crossword_{juego.id}.pdf"
    elif formato == 'png':
>>>>>>> theirs
        file_obj = exporter.export_to_png(juego)
        filename = f"crossword_{juego.id}.png"
    else:
        return HttpResponseBadRequest("Formato no soportado")
    return FileResponse(file_obj, as_attachment=True, filename=filename)
