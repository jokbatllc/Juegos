from __future__ import annotations

import random

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from core.auth import require_group

from .forms import ColoringForm
from .services import generator, exporter
from puzzles.models import JuegoGenerado


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = ColoringForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            if not params.get("seed"):
                params["seed"] = random.randint(0, 1_000_000)
            drawings = generator.generate(params)
            resultado = [d["path"] for d in drawings]
            tipo = "coloring_kids" if params["tipo"] == "kids" else "coloring_adults"
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
    elif formato == "zip":
        file_obj = exporter.export_to_zip(juego)
        filename = f"coloring_{juego.id}.zip"
    else:
        raise Http404
    return FileResponse(file_obj, as_attachment=True, filename=filename)
