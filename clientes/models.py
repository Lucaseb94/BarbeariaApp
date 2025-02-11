from django.db import models
from django.contrib.auth.models import User

class Clientes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente', null=True)  # Relacionando ao User
    nome = models.CharField(max_length=255,null=True)
    email = models.EmailField(unique=True,null=True)
    telefone = models.CharField(max_length=20,null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], default='M')
    preferencias = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='clientes/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)  # True = Ativo, False = Inativo
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username  # Ou qualquer outro valor representativo
