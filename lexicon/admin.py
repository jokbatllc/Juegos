from django.contrib import admin
from .models import Idioma, Categoria, Palabra, ListaPalabras


@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre")
    search_fields = ("code", "nombre")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "tipo_contenido")
    search_fields = ("nombre", "slug")
    list_filter = ("tipo_contenido",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Palabra)
class PalabraAdmin(admin.ModelAdmin):
    list_display = ("texto", "idioma", "dificultad")
    search_fields = ("texto",)
    list_filter = ("idioma", "categorias", "dificultad")
    filter_horizontal = ("categorias",)


@admin.register(ListaPalabras)
class ListaPalabrasAdmin(admin.ModelAdmin):
    list_display = ("nombre", "idioma")
    search_fields = ("nombre", "descripcion")
    list_filter = ("idioma", "categorias")
    filter_horizontal = ("categorias", "palabras")
