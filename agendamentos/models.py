from django.db import models
from clientes.models import Clientes
from barbeiros.models import Barbeiro
from django.core.exceptions import ValidationError

# Create your models here.
class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    servicos = models.ManyToManyField('Servico', blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.cliente.nome} - {self.data_agendamento}'

    def clean(self):
        # Validar se já existe um agendamento para o barbeiro no mesmo horário
        if Agendamento.objects.filter(barbeiro=self.barbeiro, data_agendamento=self.data_agendamento).exists():
            raise ValidationError("Horário indisponível. Escolha outro horário.")



class Servico(models.Model):
    nome = models.CharField(max_length=255)
    foto_servico = models.ImageField(blank=True, null=True, default='default.jpg')
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_estimado = models.DurationField()

    def __str__(self):
        return self.nome