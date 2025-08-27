from django.urls import path
from . import views

<<<<<<< ours
app_name = "crossword"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("export/<int:pk>/<str:formato>/", views.export, name="export"),
=======
app_name = 'crossword'

urlpatterns = [
    path('', views.create, name='create'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('export/<int:pk>/<str:formato>/', views.export, name='export'),
>>>>>>> theirs
]
