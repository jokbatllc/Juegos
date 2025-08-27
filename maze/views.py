from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import MazeForm
from .services import exporter, generator


@login_required
def index(request):
    juegos = JuegoGenerado.objects.filter(tipo="maze").order_by("-created_at")
    return render(request, "maze/index.html", {"juegos": juegos})


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = MazeForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            result = generator.generate(params)
            base = Path(settings.MEDIA_ROOT) / "exports" / "maze"
            base.mkdir(parents=True, exist_ok=True)
            count = len(list(base.glob("*.svg"))) + 1
            svg_path = base / f"maze_{count}.svg"
            svg_path.write_text(result["svg"])
            sol_path = base / f"maze_{count}_sol.svg"
            sol_path.write_text(result["solution"])
            result_paths = {
                "svg": str(svg_path.relative_to(settings.MEDIA_ROOT)),
                "solution": str(sol_path.relative_to(settings.MEDIA_ROOT)),
            }
            jg = JuegoGenerado.objects.create(
                tipo="maze", parametros=params, resultado=result_paths
            )
            return redirect("maze:detail", pk=jg.pk)
    else:
        form = MazeForm()
    return render(request, "maze/create.html", {"form": form})


@login_required
def detail(request, pk):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="maze")
    return render(request, "maze/detail.html", {"jg": jg})


@login_required
def export(request, pk, formato):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="maze")
    if formato == "pdf":
        path = exporter.export_to_pdf(jg)
        return FileResponse(
            open(path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename=f"maze_{jg.id}.pdf",
        )
    if formato == "png":
        path = exporter.export_to_png(jg)
        return FileResponse(
            open(path, "rb"),
            content_type="image/png",
            as_attachment=True,
            filename=f"maze_{jg.id}.png",
        )
    return HttpResponseBadRequest("Formato no soportado")
