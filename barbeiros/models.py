from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Barbeiro(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=255)
    status = models.BooleanField(default=True)  # True = Ativo, False = Inativo
    foto = models.ImageField(upload_to='barbeiros/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Avaliacao(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionado ao cliente
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True, null=True)
    nota = models.PositiveIntegerField()  # Avaliação de 1 a 5

    def __str__(self):
        return f'{self.cliente.username} → {self.barbeiro.nome} ({self.nota}/5)'


class HorarioDisponivel(models.Model):
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    dia_semana = models.CharField(
        max_length=10,
        choices=[
            ('segunda', 'Segunda-feira'),
            ('terca', 'Terça-feira'),
            ('quarta', 'Quarta-feira'),
            ('quinta', 'Quinta-feira'),
            ('sexta', 'Sexta-feira'),
            ('sabado', 'Sábado'),
            ('domingo', 'Domingo'),
        ]
    )
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def __str__(self):
        return f'{self.barbeiro.nome} - {self.dia_semana}: {self.horario_inicio} às {self.horario_fim}'