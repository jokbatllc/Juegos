from django.urls import path
from . import views

app_name = "coloring"

urlpatterns = [
    path("", views.create, name="create"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("export/<int:pk>/<str:formato>/", views.export, name="export"),
]
