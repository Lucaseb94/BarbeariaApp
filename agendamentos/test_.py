import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from agendamentos.models import Agendamento, Barbeiro, Servico, Clientes
from agendamentos.forms import AgendamentoForm
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.timezone import make_aware



@pytest.fixture
def cliente():
    """
    Fixture para criar um cliente (usuário) para os testes.
    """
    user = User.objects.create_user(username='cliente_teste', password='senha123')
    cliente = Clientes.objects.create(user=user)

    return cliente

@pytest.fixture
def barbeiro():
    """
    Fixture para criar um barbeiro para os testes.
    """
    return Barbeiro.objects.create(nome='Barbeiro Teste', status=True)

@pytest.fixture
def servico():
    """
    Fixture para criar um serviço para os testes.
    """
    return Servico.objects.create(nome='Corte de Cabelo', preco=50.00, tempo_estimado=timedelta(minutes=30))

@pytest.fixture
def agendamento(barbeiro, cliente):
    """
    Fixture para criar um agendamento existente para os testes.
    """
    data_agendamento = timezone.now() + timezone.timedelta(hours=1)
    return Agendamento.objects.create(
        cliente=cliente,
        barbeiro=barbeiro,
        data_agendamento=data_agendamento,
        status='pendente'
    )

@pytest.mark.django_db
class TestAgendarHorarioView:

    """
    Classe de teste para a view AgendarHorarioView.
    """

    def test_get(self, client, cliente, barbeiro, servico):
        """
        Testa se a view renderiza o formulário corretamente.
        """
        # Autentica o cliente
        client.force_login(cliente.user)

        # Acessa a view
        url = reverse('agendar_horario')
        response = client.get(url)

        # Verifica se a resposta foi bem-sucedida
        assert response.status_code == 200

        # Verifica se o formulário está no contexto
        assert isinstance(response.context['form'], AgendamentoForm)

        # Verifica se os serviços estão no contexto
        assert 'servicos' in response.context
        assert servico in response.context['servicos']

    def test_post_valido(self, client, cliente, barbeiro, servico):
        """
        Testa o envio de um formulário válido.
        """
        # Autentica o cliente
        client.force_login(cliente.user)

        # Dados do formulário
        data_agendamento = timezone.now() + timezone.timedelta(hours=2)
        data = {
            'barbeiro': barbeiro.id,
            'data_agendamento': data_agendamento.strftime('%Y-%m-%dT%H:%M'),
            'servicos': [servico.id],
        }

        # Acessa a view via POST
        url = reverse('agendar_horario')
        response = client.post(url, data)

        # Verifica se o agendamento foi criado
        assert Agendamento.objects.filter(cliente=cliente, barbeiro=barbeiro).exists()

        # Depuração: Imprimir URL esperada e URL retornada
        print("Reverse URL:", reverse('sucesso_agendamento'))
        print("Response URL:", response.url)

        # Verifica o redirecionamento para a página de sucesso
        assert response.status_code == 302
        assert response.url == reverse('sucesso_agendamento')  # Corrigido



    @pytest.mark.django_db
    def test_post_horario_indisponivel(self, client, cliente, barbeiro, servico):
        """
        Testa o envio de um formulário com horário indisponível.
        """
        # Define uma data futura relativa (por exemplo, amanhã às 18:00)
        data_futura = (timezone.now() + timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
        
        # Cria um agendamento no banco para simular um horário já ocupado
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            barbeiro=barbeiro,
            data_agendamento=data_futura,
            status='pendente',
        )

        # Faz login como cliente
        client.force_login(cliente.user)

        # Tenta agendar no mesmo horário do agendamento existente
        data = {
            'barbeiro': barbeiro.id,
            'data_agendamento': data_futura.strftime('%Y-%m-%dT%H:%M'),
            'servicos': [servico.id],
        }

        # Acessa a view via POST
        url = reverse('agendar_horario')
        response = client.post(url, data, follow=True)

        # Verifica se a mensagem esperada aparece na resposta
        assert response.status_code == 200  # O formulário é reexibido com erro
        assert "Horário indisponível" in response.content.decode()



    def test_sem_autenticacao(self, client):

        """
        Testa o acesso à view sem autenticação.
        """
        # Tenta acessar a view sem autenticação
        url = reverse('agendar_horario')
        response = client.get(url)

        # Verifica se o usuário foi redirecionado para a página de login
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))  # Supondo que a URL de login é 'login'

    @pytest.mark.django_db
    def test_data_agendamento_no_passado(self, barbeiro, servico):
        """
        Testa que o formulário não aceita agendamento no passado.
        """
        # Dados com data passada
        data_passada = (timezone.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        print(data_passada)
        form_data = {
            'barbeiro': barbeiro.id,
            'data_agendamento': data_passada,
            'sevicos': [servico.id]
        }

        form = AgendamentoForm(data=form_data)
        print(form)
        # O formulário não deve ser válido
        assert not form.is_valid()
        # Verifica se a mensagem de erro está presente
        assert "O horário deve ser no futuro." in form.errors.get('data_agendamento', [])

    @pytest.mark.django_db
    def test_data_agendamento_no_futuro(self, barbeiro, servico):
        """
        Testa que o formulário aceita agendamento no futuro.
        """

        # Dados com data futura
        data_futura = (timezone.now() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M')
        form_data = {
            'barbeiro': barbeiro.id,
            'data_agendamento': data_futura,
            'servicos': [servico.id],
        }

        form = AgendamentoForm(data=form_data)

        assert form.is_valid()














































