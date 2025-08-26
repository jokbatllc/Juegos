import random

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import WordsearchForm
from .services import exporter, generator, repository


@require_group("generador")
def create(request):
    if request.method == 'POST':
        form = WordsearchForm(request.POST)
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
            )
            try:
                resultado = generator.generate(params, palabras)
            except ValueError as e:
                form.add_error(None, str(e))
            else:
                juego = JuegoGenerado.objects.create(
                    tipo='wordsearch',
                    parametros=params,
                    resultado=resultado,
                    seed=params['seed'],
                    creado_por=request.user if request.user.is_authenticated else None,
                )
                return redirect('wordsearch:detail', pk=juego.pk)
    else:
        form = WordsearchForm()
    return render(request, 'wordsearch/create.html', {'form': form})


@login_required
def detail(request, pk):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='wordsearch')
    palabras = juego.resultado.get('palabras', [])
    return render(
        request, 'wordsearch/detail.html', {'juego': juego, 'palabras': palabras}
    )


@login_required
def export(request, pk, formato):
    juego = get_object_or_404(JuegoGenerado, pk=pk, tipo='wordsearch')
    if formato == 'pdf':
        file_path = exporter.export_to_pdf(juego)
        filename = f"wordsearch_{juego.id}.pdf"
        content_type = 'application/pdf'
    elif formato == 'png':
        file_path = exporter.export_to_png(juego)
        filename = f"wordsearch_{juego.id}.png"
        content_type = 'image/png'
    else:
        raise Http404
    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=filename,
        content_type=content_type,
    )
