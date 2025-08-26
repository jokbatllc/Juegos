from django.urls import path
from . import views

app_name = "lexicon"

urlpatterns = [
    path("", views.index, name="index"),
    # Idiomas
    path("idiomas/", views.idioma_list, name="idioma_list"),
    path("idiomas/create/", views.idioma_create, name="idioma_create"),
    path("idiomas/<str:code>/edit/", views.idioma_edit, name="idioma_edit"),
    path("idiomas/<str:code>/delete/", views.idioma_delete, name="idioma_delete"),
    # Categorías
    path("categorias/", views.categoria_list, name="categoria_list"),
    path("categorias/create/", views.categoria_create, name="categoria_create"),
    path("categorias/<int:pk>/edit/", views.categoria_edit, name="categoria_edit"),
    path("categorias/<int:pk>/delete/", views.categoria_delete, name="categoria_delete"),
    # Palabras
    path("palabras/", views.palabra_list, name="palabra_list"),
    path("palabras/create/", views.palabra_create, name="palabra_create"),
    path("palabras/<int:pk>/edit/", views.palabra_edit, name="palabra_edit"),
    path("palabras/<int:pk>/delete/", views.palabra_delete, name="palabra_delete"),
    # Listas
    path("listas/", views.lista_list, name="lista_list"),
    path("listas/create/", views.lista_create, name="lista_create"),
    path("listas/<int:pk>/edit/", views.lista_edit, name="lista_edit"),
    path("listas/<int:pk>/delete/", views.lista_delete, name="lista_delete"),
    # Importación CSV
    path("import/", views.import_csv, name="import_csv"),
    path("import/preview/", views.import_preview, name="import_preview"),
]
