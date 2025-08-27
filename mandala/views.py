<<<<<<< ours
from __future__ import annotations

import random
=======
from pathlib import Path
>>>>>>> theirs

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
<<<<<<< ours
from puzzles.models import JuegoGenerado

from .forms import MandalaForm
from .services import generator, exporter


def index(request):
    # Página de aterrizaje: redirige al formulario de creación
    return redirect("mandala:create")
=======
from puzzles.models import Exportacion, JuegoGenerado

from .forms import MandalaForm
from .services.generator import (
    MandalaParams,
    generate_mandala_svg,
    save_svg,
    svg_to_pdf,
    svg_to_png,
)


@require_group("generador")
def index(request):
    form = MandalaForm()
    return render(request, "mandala/index.html", {"form": form})
>>>>>>> theirs


@require_group("generador")
def create(request):
<<<<<<< ours
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
=======
    form = MandalaForm(request.POST)
    if not form.is_valid():
        return render(request, "mandala/index.html", {"form": form})
    params = MandalaParams(**form.to_params())
    svg = generate_mandala_svg(params)
    jg = JuegoGenerado.objects.create(
        tipo="mandala",
        parametros=form.cleaned_data,
        seed=form.cleaned_data.get("seed") or 0,
        creado_por=request.user if request.user.is_authenticated else None,
    )
    rel_path = save_svg(svg, f"{jg.id}.svg")
    jg.resultado = rel_path
    jg.save()
    return redirect("mandala:detail", pk=jg.pk)
>>>>>>> theirs


@login_required
def detail(request, pk):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="mandala")
<<<<<<< ours
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
=======
    svg_path = Path(settings.MEDIA_ROOT) / jg.resultado
    svg = svg_path.read_text(encoding="utf-8")
    return render(request, "mandala/detail.html", {"jg": jg, "svg": svg})


@login_required
def export(request, pk):
    fmt = request.GET.get("format", "svg")
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="mandala")
    base = Path(settings.MEDIA_ROOT) / "exports" / "mandala"
    svg_path = base / f"{jg.id}.svg"
    if not svg_path.exists():
        raise Http404
    svg_data = svg_path.read_text(encoding="utf-8")
    if fmt == "svg":
        export_path = svg_path
    elif fmt == "png":
        export_path = base / f"{jg.id}.png"
        svg_to_png(svg_data, export_path)
    elif fmt == "pdf":
        export_path = base / f"{jg.id}.pdf"
        svg_to_pdf(svg_data, export_path)
    else:
        raise Http404
    Exportacion.objects.create(
        juego=jg, formato=fmt, archivo=str(export_path.relative_to(settings.MEDIA_ROOT))
    )
    return FileResponse(
        open(export_path, "rb"), as_attachment=True, filename=export_path.name
    )
>>>>>>> theirs
