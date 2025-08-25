from __future__ import annotations

import csv
import io
from typing import List

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.auth import require_group
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import (
    CategoriaForm,
    IdiomaForm,
    ImportCSVForm,
    ListaPalabrasForm,
    PalabraForm,
)
from .models import Categoria, Idioma, ListaPalabras, Palabra
from .utils import bulk_upsert_palabras, normalize_text


@login_required
def index(request):
    return render(request, "lexicon/index.html")


@login_required
def idioma_list(request):
    q = request.GET.get("q", "")
    qs = Idioma.objects.all()
    if q:
        qs = qs.filter(Q(code__icontains=q) | Q(nombre__icontains=q))
    paginator = Paginator(qs.order_by("code"), 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "lexicon/idioma_list.html", {"page_obj": page_obj, "q": q})


@require_group("editor_contenidos")
def idioma_create(request):
    form = IdiomaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Idioma creado")
        return redirect("lexicon:idioma_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Nuevo idioma"})


@require_group("editor_contenidos")
def idioma_edit(request, code: str):
    obj = get_object_or_404(Idioma, pk=code)
    form = IdiomaForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Idioma actualizado")
        return redirect("lexicon:idioma_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Editar idioma"})


@require_group("editor_contenidos")
def idioma_delete(request, code: str):
    obj = get_object_or_404(Idioma, pk=code)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Idioma eliminado")
        return redirect("lexicon:idioma_list")
    return render(request, "lexicon/confirm_delete.html", {"obj": obj})


@login_required
def categoria_list(request):
    q = request.GET.get("q", "")
    qs = Categoria.objects.all()
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(slug__icontains=q))
    paginator = Paginator(qs.order_by("nombre"), 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "lexicon/categoria_list.html", {"page_obj": page_obj, "q": q})


@require_group("editor_contenidos")
def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría creada")
        return redirect("lexicon:categoria_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Nueva categoría"})


@require_group("editor_contenidos")
def categoria_edit(request, pk: int):
    obj = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría actualizada")
        return redirect("lexicon:categoria_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Editar categoría"})


@require_group("editor_contenidos")
def categoria_delete(request, pk: int):
    obj = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Categoría eliminada")
        return redirect("lexicon:categoria_list")
    return render(request, "lexicon/confirm_delete.html", {"obj": obj})


@login_required
def palabra_list(request):
    q = request.GET.get("q", "")
    idioma_code = request.GET.get("idioma")
    categoria_id = request.GET.get("categoria")
    diff_min = request.GET.get("dificultad_min")
    diff_max = request.GET.get("dificultad_max")
    qs = Palabra.objects.all().select_related("idioma")
    if q:
        qs = qs.filter(texto__icontains=q)
    if idioma_code:
        qs = qs.filter(idioma__code=idioma_code)
    if categoria_id:
        qs = qs.filter(categorias__pk=categoria_id)
    if diff_min:
        qs = qs.filter(dificultad__gte=diff_min)
    if diff_max:
        qs = qs.filter(dificultad__lte=diff_max)
    paginator = Paginator(qs.order_by("texto").distinct(), 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "q": q,
        "idiomas": Idioma.objects.all(),
        "categorias": Categoria.objects.all(),
        "filtros": {
            "idioma": idioma_code,
            "categoria": categoria_id,
            "dificultad_min": diff_min,
            "dificultad_max": diff_max,
        },
    }
    return render(request, "lexicon/palabra_list.html", context)


@require_group("editor_contenidos")
def palabra_create(request):
    form = PalabraForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Palabra creada")
        return redirect("lexicon:palabra_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Nueva palabra"})


@require_group("editor_contenidos")
def palabra_edit(request, pk: int):
    obj = get_object_or_404(Palabra, pk=pk)
    form = PalabraForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Palabra actualizada")
        return redirect("lexicon:palabra_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Editar palabra"})


@require_group("editor_contenidos")
def palabra_delete(request, pk: int):
    obj = get_object_or_404(Palabra, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Palabra eliminada")
        return redirect("lexicon:palabra_list")
    return render(request, "lexicon/confirm_delete.html", {"obj": obj})


@login_required
def lista_list(request):
    q = request.GET.get("q", "")
    idioma_code = request.GET.get("idioma")
    qs = ListaPalabras.objects.all().select_related("idioma")
    if q:
        qs = qs.filter(nombre__icontains=q)
    if idioma_code:
        qs = qs.filter(idioma__code=idioma_code)
    paginator = Paginator(qs.order_by("nombre"), 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "lexicon/lista_list.html",
        {"page_obj": page_obj, "q": q, "idiomas": Idioma.objects.all(), "filtros": {"idioma": idioma_code}},
    )


@require_group("editor_contenidos")
def lista_create(request):
    form = ListaPalabrasForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Lista creada")
        return redirect("lexicon:lista_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Nueva lista"})


@require_group("editor_contenidos")
def lista_edit(request, pk: int):
    obj = get_object_or_404(ListaPalabras, pk=pk)
    form = ListaPalabrasForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Lista actualizada")
        return redirect("lexicon:lista_list")
    return render(request, "lexicon/form.html", {"form": form, "titulo": "Editar lista"})


@require_group("editor_contenidos")
def lista_delete(request, pk: int):
    obj = get_object_or_404(ListaPalabras, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Lista eliminada")
        return redirect("lexicon:lista_list")
    return render(request, "lexicon/confirm_delete.html", {"obj": obj})


@require_group("editor_contenidos")
def import_csv(request):
    form = ImportCSVForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        content = data["archivo"].read().decode("utf-8")
        sep = data["separador"]
        if data["tiene_encabezados"]:
            reader = csv.DictReader(io.StringIO(content), delimiter=sep)
        else:
            cols = [c.strip() for c in data.get("columnas", "").split(",") if c.strip()]
            reader = csv.DictReader(io.StringIO(content), fieldnames=cols, delimiter=sep)
        rows = list(reader)
        request.session["import_rows"] = rows
        request.session["import_meta"] = {
            "tipo": data["tipo"],
            "idioma": data["idioma"].code if data.get("idioma") else None,
        }
        return redirect("lexicon:import_preview")
    return render(request, "lexicon/import_csv.html", {"form": form})


@require_group("editor_contenidos")
def import_preview(request):
    rows: List[dict] = request.session.get("import_rows") or []
    meta = request.session.get("import_meta") or {}
    if not rows:
        return redirect("lexicon:import_csv")
    tipo = meta.get("tipo")
    idioma_code = meta.get("idioma")
    idioma = Idioma.objects.filter(code=idioma_code).first() if idioma_code else None
    if request.method == "POST":
        if tipo == "palabras" and idioma:
            stats = bulk_upsert_palabras(rows, idioma)
            messages.success(request, f"{stats['insertadas']} insertadas, {stats['duplicadas']} duplicadas")
        elif tipo == "categorias":
            for row in rows:
                nombre = normalize_text(row.get("nombre", ""))
                if not nombre:
                    continue
                slug = row.get("slug") or slugify(nombre)
                Categoria.objects.get_or_create(
                    nombre=nombre,
                    defaults={"slug": slug, "tipo_contenido": row.get("tipo_contenido", "wordsearch")},
                )
            messages.success(request, "Categorías importadas")
        request.session.pop("import_rows", None)
        request.session.pop("import_meta", None)
        return redirect("lexicon:index")
    return render(request, "lexicon/import_preview.html", {"rows": rows[:50], "meta": meta})
