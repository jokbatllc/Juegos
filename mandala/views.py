from __future__ import annotations

import random

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from core.auth import require_group

from .forms import MandalaForm
from .services import generator, exporter
from puzzles.models import JuegoGenerado


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = MandalaForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            if not params.get("semilla"):
                params["semilla"] = random.randint(0, 1_000_000)
            jg = JuegoGenerado.objects.create(
                tipo="mandala",
                parametros=params,
                seed=params["semilla"],
                creado_por=request.user if request.user.is_authenticated else None,
            )
            drawings = generator.generate(params, jg.id)
            jg.resultado = [d["path"] for d in drawings]
            jg.save()
            return redirect("mandala:detail", pk=jg.pk)
    else:
        form = MandalaForm()
    return render(request, "mandala/create.html", {"form": form})


@login_required
def detail(request, pk):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="mandala")
    images = [settings.MEDIA_URL + p for p in jg.resultado]
    return render(request, "mandala/detail.html", {"jg": jg, "images": images})


@login_required
def export(request, pk, formato):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="mandala")
    if formato == "pdf":
        file_obj = exporter.export_to_pdf(jg)
        filename = f"mandala_{jg.id}.pdf"
    elif formato == "zip":
        file_obj = exporter.export_to_zip(jg)
        filename = f"mandala_{jg.id}.zip"
    else:
        raise Http404
    return FileResponse(file_obj, as_attachment=True, filename=filename)
