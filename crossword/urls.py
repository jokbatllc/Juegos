from django.urls import path
from . import views

app_name = "crossword"

urlpatterns = [
    path("", views.index, name="index"),                     # página inicial (ajústala si no existe)
    path("create/", views.create, name="create"),            # crear crucigrama
    path("detail/<int:pk>/", views.detail, name="detail"),   # ver detalle
    path("export/<int:pk>/<str:formato>/", views.export, name="export"),  # exportar
]
