from django.urls import path
from . import views

app_name = 'coloring'

urlpatterns = [
    path('', views.index, name='index'),
]
