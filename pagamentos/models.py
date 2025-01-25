from django.db import models
from agendamentos.models import Agendamento


# Create your models here.
class Pagamento(models.Model):
    METODO_PAGAMENTO_CHOICES = [
        ('cartao', 'Cartão'),
        ('dinheiro', 'Dinheiro'),
        ('pix', 'Pix'),
    ]

    STATUS_PAGAMENTO_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pagamento = models.CharField(max_length=20, choices=METODO_PAGAMENTO_CHOICES)
    status_pagamento = models.CharField(max_length=20, choices=STATUS_PAGAMENTO_CHOICES, default='pendente')
    data_pagamento = models.DateTimeField()

    def __str__(self):
        return f'Pagamento {self.id} - {self.valor}'
