from django.urls import path
from .views import AgendarHorarioView, catalogo_servicos, sucesso_agendamento, login

urlpatterns = [
    path('catalogo/', catalogo_servicos, name='catalogo_servicos'),
    path('agendar/', AgendarHorarioView.as_view(), name='agendar_horario'),
    path('sucesso-agendamento/', sucesso_agendamento, name='sucesso_agendamento'),
    path('login/', login, name='login'),
]