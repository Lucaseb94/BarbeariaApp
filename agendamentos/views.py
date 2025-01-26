from django.shortcuts import render, redirect
from .models import Servico
from .forms import AgendamentoForm



def agendar_horario(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso_agendamento')
    else:
        form = AgendamentoForm()

    return render(request, 'agendar_horario.html', {'form': form})


def sucesso_agendamento(request):
    return render(request, 'sucesso_agendamento.html')


def catalogo_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'catalogo_servicos.html', {'servicos': servicos})