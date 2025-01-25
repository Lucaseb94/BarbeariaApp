from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalogo_servicos, name='catalogo_servicos'),
    path('agendar/', views.agendar_horario, name='agendar_horario'),
]