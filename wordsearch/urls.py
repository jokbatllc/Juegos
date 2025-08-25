from django.urls import path
from . import views

app_name = 'wordsearch'

urlpatterns = [
    path('', views.index, name='index'),
]
