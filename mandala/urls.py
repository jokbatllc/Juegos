from django.urls import path
from . import views

app_name = "mandala"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("detail/<int:pk>/", views.detail, name="detail"),
      path("export/<int:pk>/<str:formato>/", views.export, name="export"),
       path("export/<int:pk>/", views.export, name="export"),
 
]
