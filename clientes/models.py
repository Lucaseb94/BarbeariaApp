from django.db import models

# Create your models here.
class Clientes(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    endereco = models.TextField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], default='M')
    preferencias = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='clientes/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)  # True = Ativo, False = Inativo
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome