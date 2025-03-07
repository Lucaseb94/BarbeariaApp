# Generated by Django 5.0.7 on 2025-01-26 00:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Barbeiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=20)),
                ('especialidade', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='barbeiros/')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(blank=True, null=True)),
                ('nota', models.PositiveIntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('barbeiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbeiros.barbeiro')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioDisponivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('segunda', 'Segunda-feira'), ('terca', 'Terça-feira'), ('quarta', 'Quarta-feira'), ('quinta', 'Quinta-feira'), ('sexta', 'Sexta-feira'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], max_length=10)),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
                ('barbeiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbeiros.barbeiro')),
            ],
        ),
    ]
