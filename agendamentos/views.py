from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Servico, Agendamento
from .forms import AgendamentoForm
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class AgendarHorarioView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login') # Define a URL para onde os usuários não autenticados serão redirecionados
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendar_horario.html'
    success_url = reverse_lazy('sucesso_agendamento')

    def get_form_kwargs(self):
        """
        Passa o usuário logado para o formulário.
        Isso permite que o formulário acesse o usuário atual.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Valida o formulário e salva o agendamento.
        """
        # Define o status do agendamento como 'pendente'
        form.instance.status = 'pendente'

        # Vincula o cliente logado ao agendamento
        if self.request.user.is_authenticated:
            form.instance.cliente = self.request.user.cliente

        # Obtém a data e o barbeiro selecionados no formulário
        data_agendamento = form.cleaned_data['data_agendamento']
        barbeiro = form.cleaned_data['barbeiro']

        # Garantir que a data_agendamento está ciente do fuso horário
        if data_agendamento.tzinfo is None:
            data_agendamento = make_aware(data_agendamento)

        # Verifica se o horário já está ocupado para o barbeiro selecionado
        if Agendamento.objects.filter(barbeiro=barbeiro, data_agendamento=data_agendamento).exists():
            form.add_error('data_agendamento', 'Horário indisponível. Escolha outro horário.')
            return self.form_invalid(form)  # Não redireciona, retorna ao formulário com erro (status code 200)
        
        # Salva o agendamento no banco de dados
        return super().form_valid(form)  # Redireciona para a página de sucesso (status code 302)

    def get_context_data(self, **kwargs):
        """
        Adiciona dados extras ao contexto do template.
        """
        context = super().get_context_data(**kwargs)
        
        # Adiciona a lista de serviços ao contexto (para exibir no template)
        context['servicos'] = Servico.objects.all()
        
        return context

    def form_invalid(self, form):
        """
        Retorna apenas a mensagem de erro sem renderizar a página completa.
        """
        # Se houver erro no campo data_agendamento, retorna a mensagem
        if 'data_agendamento' in form.errors:
            error_message = form.errors['data_agendamento'][0]
            return HttpResponse(error_message, status=200)
        # Se não houver erro específico, retorna todos os erros como string
        return HttpResponse(str(form.errors), status=200)


def sucesso_agendamento(request):
    """
    Exibe a página de sucesso após o agendamento.
    """
    return render(request, 'sucesso_agendamento.html')


def login(request):
    return render(request, 'login.html')

def catalogo_servicos(request):
    """
    Exibe o catálogo de serviços disponíveis.
    """
    servicos = Servico.objects.all()
    return render(request, 'catalogo_servicos.html', {'servicos': servicos})