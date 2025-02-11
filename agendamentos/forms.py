from django import forms
from .models import Agendamento, Barbeiro, Servico

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