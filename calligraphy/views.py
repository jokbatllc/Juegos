from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from core.auth import require_group
from puzzles.models import JuegoGenerado

from .forms import CalligraphyForm
from .services import exporter, generator


def index(request):
    return render(request, "calligraphy/index.html")


@require_group("generador")
def create(request):
    if request.method == "POST":
        form = CalligraphyForm(request.POST)
        if form.is_valid():
            params = form.to_params()
            resultado = generator.generate(params)
            jg = JuegoGenerado.objects.create(
                tipo="calligraphy",
                parametros=params,
                resultado=resultado,
                seed=params.get("seed") or 0,
                creado_por=request.user if request.user.is_authenticated else None,
            )
            return redirect("calligraphy:detail", pk=jg.pk)
    else:
        form = CalligraphyForm(request.GET or None)
    return render(request, "calligraphy/create.html", {"form": form})


@login_required
def detail(request, pk):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="calligraphy")
    paginas = jg.resultado.get("paginas", [])[:2]
    return render(request, "calligraphy/detail.html", {"jg": jg, "paginas": paginas})


@login_required
def export(request, pk, formato):
    jg = get_object_or_404(JuegoGenerado, pk=pk, tipo="calligraphy")
    if formato == "pdf":
        exporter.export_to_pdf(jg)
    else:
        return HttpResponseBadRequest("Formato no soportado")
    return redirect("calligraphy:detail", pk=jg.pk)
