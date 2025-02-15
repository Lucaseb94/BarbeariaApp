from django import forms
from .models import Agendamento, Barbeiro, Servico
from django.utils import timezone
from django.core.exceptions import ValidationError

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['barbeiro', 'data_agendamento', 'servicos']
        widgets = {
            'data_agendamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'servicos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove o usuário dos kwargs
        super().__init__(*args, **kwargs)
        
        # Filtra barbeiros ativos
        self.fields['barbeiro'].queryset = Barbeiro.objects.filter(status=True)
        
        # Filtra serviços ativos
        self.fields['servicos'].queryset = Servico.objects.all()

    def clean_data_agendamento(self):
        data_agendamento = self.cleaned_data.get('data_agendamento')
        if data_agendamento is None:
            return data_agendamento
        
        # Se a data informada for menor ou igual à hora atual, levanta o erro de validação
        if data_agendamento <= timezone.now():
            raise ValidationError('O horário deve ser no futuro.')
        return data_agendamento