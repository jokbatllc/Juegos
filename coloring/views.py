from __future__ import annotations

import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import ColoringForm
from .services import exporter, generator


def index(request):
    """Redirige al formulario de creación."""
    return redirect("coloring:create")


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = ColoringForm(request.POST)
        if form.is_valid():
            params = form.to_params()

            # Asegurar semilla
            if not params.get("seed"):
                params["seed"] = random.randint(0, 1_000_000)

            # Generar dibujos (lista de dicts con 'path')
            drawings = generator.generate(params)
            resultado = [d["path"] for d in drawings]

            # Tipo según público
            tipo = "coloring_kids" if params.get("tipo") == "kids" else "coloring_adults"

            juego = JuegoGenerado.objects.create(
                tipo=tipo,
                parametros=params,
                resultado=resultado,
                seed=params["seed"],
                creado_por=request.user if request.user.is_authenticated else None,
            )
            return redirect("coloring:detail", pk=juego.pk)
    else:
        initial = {"tipo": request.GET.get("tipo", "kids")}
        form = ColoringForm(initial=initial)

    return render(request, "coloring/create.html", {"form": form})


@login_required
def detail(request, pk):
    juego = get_object_or_404(
        JuegoGenerado, pk=pk, tipo__in=["coloring_kids", "coloring_adults"]
    )
    images = [settings.MEDIA_URL + p for p in juego.resultado]
    return render(request, "coloring/detail.html", {"jg": juego, "images": images})


@login_required
def export(request, pk, formato):
    juego = get_object_or_404(
        JuegoGenerado, pk=pk, tipo__in=["coloring_kids", "coloring_adults"]
    )

    if formato == "pdf":
        file_obj = exporter.export_to_pdf(juego)
        filename = f"coloring_{juego.id}.pdf"
    elif formato == "png":
        file_obj = exporter.export_to_png(juego)
        filename = f"coloring_{juego.id}.png"
    else:
        raise Http404("Formato no soportado")

    return FileResponse(file_obj, as_attachment=True, filename=filename)
