from django.urls import path
from . import views

app_name = 'puzzles'

urlpatterns = [
    path('', views.index, name='index'),
]
