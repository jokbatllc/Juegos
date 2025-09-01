from __future__ import annotations

import random
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import MandalaForm
from .services import generator, exporter


def index(request):
    """Página de aterrizaje: redirige al formulario de creación."""
    return redirect("mandala:create")


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = MandalaForm(request.POST)
        if form.is_valid():
            params = form.to_params()

            # Semilla por defecto
            if not params.get("semilla"):
                params["semilla"] = random.randint(0, 1_000_000)

            # Creamos el registro primero para usar su id en paths
            jg = JuegoGenerado.objects.create(
                tipo="mandala",
                parametros=params,
                seed=params["semilla"],
                creado_por=request.user if request.user.is_authenticated else None,
            )

            # Generar dibujos; se espera una lista de dicts con 'path' relativo a MEDIA_ROOT
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
    # Construimos URLs públicas para las imágenes generadas
    images = [settings.MEDIA_URL + p for p in (jg.resultado or [])]
    return render(request, "mandala/detail.html", {"jg": jg, "images": images})


@login_required
def export(request, pk, formato):
    """
    Exporta el mandala a PDF o ZIP (con los recursos).
    El exporter devuelve un archivo-like (stream) listo para FileResponse.
    """
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="mandala")

    if formato == "pdf":
        file_obj = exporter.export_to_pdf(jg)
        filename = f"mandala_{jg.id}.pdf"
    elif formato == "zip":
        file_obj = exporter.export_to_zip(jg)
        filename = f"mandala_{jg.id}.zip"
    else:
        raise Http404("Formato no soportado")

    return FileResponse(file_obj, as_attachment=True, filename=filename)
