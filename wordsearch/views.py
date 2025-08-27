import random

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import WordsearchForm
<<<<<<< ours
from .services import repository, generator, exporter


def index(request):
    # Aterriza en el formulario de creación
    return redirect("wordsearch:create")
=======
from .services import exporter, generator, repository
>>>>>>> theirs


@require_group("generador")
def create(request):
<<<<<<< ours
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
=======
    if request.method == 'POST':
        form = WordsearchForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            if not params.get('seed'):
                params['seed'] = random.randint(0, 999999)
            cantidad = form.cleaned_data['cantidad']
            juegos_ids = []
            for _ in range(cantidad):
                palabras = repository.fetch_palabras(
                    params['idioma'],
                    params['categorias'],
                    params['dificultad_min'],
                    params['dificultad_max'],
                    params['num_palabras'],
                )
                try:
                    resultado = generator.generate(params, palabras)
                except ValueError as e:
                    form.add_error(None, str(e))
                    break
                juego = JuegoGenerado.objects.create(
                    tipo='wordsearch',
                    parametros=params,
                    resultado=resultado,
                    seed=params['seed'],
                    creado_por=request.user if request.user.is_authenticated else None,
                )
                juegos_ids.append(juego.id)
            if juegos_ids and not form.errors:
                request.session['last_wordsearch_ids'] = juegos_ids
                return redirect('wordsearch:list')
    else:
        form = WordsearchForm()
    return render(request, 'wordsearch/create.html', {'form': form})
>>>>>>> theirs


@login_required
def detail(request, pk):
<<<<<<< ours
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
=======
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='wordsearch')
    palabras = juego.resultado.get('palabras', [])
    return render(
        request, 'wordsearch/detail.html', {'juego': juego, 'palabras': palabras}
    )


@login_required
def list(request):
    ids = request.session.get('last_wordsearch_ids', [])
    juegos = JuegoGenerado.objects.filter(id__in=ids, tipo='wordsearch')
    return render(request, 'wordsearch/list.html', {'juegos': juegos})


@login_required
def export_grid(request, pk, fmt):
    bg = request.GET.get('bg', 'white')
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='wordsearch')
    if fmt == 'pdf':
        file_path = exporter.export_grid_pdf(juego, bg=bg)
        content_type = 'application/pdf'
    elif fmt == 'png':
        file_path = exporter.export_grid_png(juego, bg=bg)
        content_type = 'image/png'
    else:
        raise Http404
    resp = FileResponse(open(file_path, 'rb'), content_type=content_type)
    resp['Content-Disposition'] = f'attachment; filename="wordsearch_{pk}_grid.{fmt}"'
    return resp


@login_required
def export_words(request, pk, fmt):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='wordsearch')
    if fmt == 'txt':
        file_path = exporter.export_words_txt(juego)
        content_type = 'text/plain'
    elif fmt == 'pdf':
        file_path = exporter.export_words_pdf(juego)
        content_type = 'application/pdf'
    else:
        raise Http404
    resp = FileResponse(open(file_path, 'rb'), content_type=content_type)
    resp['Content-Disposition'] = f'attachment; filename="wordsearch_{pk}_words.{fmt}"'
    return resp


@login_required
def export_solution(request, pk, fmt):
    bg = request.GET.get('bg', 'white')
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='wordsearch')
    if fmt == 'pdf':
        file_path = exporter.export_solution_pdf(juego, bg=bg)
        content_type = 'application/pdf'
    elif fmt == 'png':
        file_path = exporter.export_solution_png(juego, bg=bg)
        content_type = 'image/png'
    else:
        raise Http404
    resp = FileResponse(open(file_path, 'rb'), content_type=content_type)
    resp['Content-Disposition'] = (
        f'attachment; filename="wordsearch_{pk}_solution.{fmt}"'
    )
    return resp
>>>>>>> theirs
