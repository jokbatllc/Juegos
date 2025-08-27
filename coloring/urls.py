from django.urls import path
from . import views

app_name = "coloring"

urlpatterns = [
<<<<<<< ours
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
=======
    path("", views.create, name="create"),
>>>>>>> theirs
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("export/<int:pk>/<str:formato>/", views.export, name="export"),
]
