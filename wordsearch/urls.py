from django.urls import path
<<<<<<< ours
from . import views

app_name = "wordsearch"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("export/<int:pk>/<str:formato>/", views.export, name="export"),
=======

from . import views

app_name = 'wordsearch'

urlpatterns = [
    path('', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('export/grid/<int:pk>.<str:fmt>', views.export_grid, name='export_grid'),
    path('export/words/<int:pk>.<str:fmt>', views.export_words, name='export_words'),
    path(
        'export/solution/<int:pk>.<str:fmt>',
        views.export_solution,
        name='export_solution',
    ),
>>>>>>> theirs
]
