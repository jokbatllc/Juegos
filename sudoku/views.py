from __future__ import annotations

<<<<<<< ours
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
=======
import math

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseBadRequest
>>>>>>> theirs
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import SudokuForm
<<<<<<< ours
from .services import generator, exporter


def index(request):
    # Página de aterrizaje: redirige al formulario de creación
    return redirect("sudoku:create")
=======
from .services import exporter, generator
>>>>>>> theirs


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = SudokuForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            resultado = generator.generate(params)
            jg = JuegoGenerado.objects.create(
                tipo="sudoku",
                parametros=params,
                resultado=resultado,
                seed=params.get("seed") or 0,
                creado_por=request.user if request.user.is_authenticated else None,
            )
            return redirect("sudoku:detail", pk=jg.pk)
    else:
        form = SudokuForm()
    return render(request, "sudoku/create.html", {"form": form})


@login_required
def detail(request, pk: int):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="sudoku")
<<<<<<< ours
    return render(
        request,
        "sudoku/detail.html",
        {"jg": jg, "grid": jg.resultado.get("grid"), "solution": jg.resultado.get("solution")},
=======
    size = jg.resultado.get("tamaño")
    sub = int(math.sqrt(size))
    grid = jg.resultado.get("grid")
    return render(
        request,
        "sudoku/detail.html",
        {
            "jg": jg,
            "grid": grid,
            "solution": jg.resultado.get("solution"),
            "size": size,
            "sub_rows": sub,
            "sub_cols": size // sub,
        },
>>>>>>> theirs
    )


@login_required
<<<<<<< ours
def export(request, pk: int, formato: str):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="sudoku")
    if formato == "pdf":
        exporter.export_to_pdf(jg)
    elif formato == "png":
        exporter.export_to_png(jg)
    else:
        return HttpResponseBadRequest("Formato no soportado")
    return redirect("sudoku:detail", pk=jg.pk)
=======
def index(request):
    juegos = JuegoGenerado.objects.filter(tipo="sudoku").order_by("-created_at")
    return render(request, "sudoku/index.html", {"juegos": juegos})


@login_required
def export(request, pk: int, formato: str):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="sudoku")
    if formato == "pdf":
        path = exporter.export_to_pdf(jg)
        return FileResponse(
            open(path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename=f"sudoku_{jg.id}.pdf",
        )
    if formato == "png":
        path = exporter.export_to_png(jg)
        return FileResponse(
            open(path, "rb"),
            content_type="image/png",
            as_attachment=True,
            filename=f"sudoku_{jg.id}.png",
        )
    return HttpResponseBadRequest("Formato no soportado")
>>>>>>> theirs
