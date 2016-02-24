# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('nome_completo', models.CharField(max_length=255)),
                ('cpf', models.CharField(unique=True, max_length=11, verbose_name='CPF')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='e-mail')),
                ('instituicao', models.CharField(max_length=255, verbose_name='institui\xe7\xe3o')),
                ('curso', models.CharField(max_length=255, verbose_name='curso')),
                ('ativo', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False, verbose_name='administrador')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
