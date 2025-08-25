from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
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


@require_group("generador")
def create(request):
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


@login_required
def detail(request, pk):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="mandala")
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
