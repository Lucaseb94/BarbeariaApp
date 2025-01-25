from django import forms
from .models import Agendamento
from clientes.models import Cliente
from barbeiros.models import Barbeiro
from .models import Servico

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'barbeiro', 'data_agendamento', 'status', 'servicos', 'observacoes']
        widgets = {
            'data_agendamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }