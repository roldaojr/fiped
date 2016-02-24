# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Definicoes',
            fields=[
                ('evento', models.OneToOneField(related_name='def_trabalhos', primary_key=True, serialize=False, to='eventos.Evento')),
                ('prazo', models.DateTimeField(verbose_name='prazo para submiss\xe3o')),
                ('submeter_poster', models.BooleanField(default=True, verbose_name='habilitar submiss\xe3o de poster')),
                ('modelo_poster', models.FileField(upload_to='modelos/poster', null=True, verbose_name='Modelo de Poster', blank=True)),
                ('submeter_mostra', models.BooleanField(default=True, verbose_name='habilitar submiss\xe3o de mostra tecnologica')),
                ('modelo_plano_pesquisa', models.FileField(upload_to='modelos/plano_pesquisa', null=True, verbose_name='Modelo de Plano de pesquisa', blank=True)),
                ('modelo_relatorio', models.FileField(upload_to='modelos/relatorio', null=True, verbose_name='Modelo de Relat\xf3rio', blank=True)),
                ('modelo_resumo', models.FileField(upload_to='modelos/resumo', null=True, verbose_name='Modelo de Resumo', blank=True)),
            ],
            options={
                'verbose_name': 'defini\xe7\xe3o de trabalhos',
                'verbose_name_plural': 'defini\xe7\xf5es de trabalhos',
            },
        ),
        migrations.CreateModel(
            name='MostraTecnologica',
            fields=[
                ('inscricao_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='eventos.Inscricao')),
                ('titulo', models.CharField(max_length=255, verbose_name='t\xedtulo')),
                ('nome_autor', models.CharField(max_length=255, verbose_name='nome completo do autor principal')),
                ('cpf_autor', models.CharField(max_length=11, verbose_name='CPF do autor principal')),
                ('nome_orientador', models.CharField(max_length=255, verbose_name='nome completo do orientador')),
                ('cpf_orientador', models.CharField(max_length=11, verbose_name='CPF do orientador')),
                ('aprovado', models.BooleanField(default=False, editable=False)),
                ('plano_pesquisa', models.FileField(upload_to='trabalhos/mostra_tecnologica', verbose_name='plano de pesquisa')),
                ('relatorio_projeto', models.FileField(upload_to='trabalhos/mostra_tecnologica', verbose_name='relat\xf3rio do projeto')),
                ('resumo_projeto', models.FileField(upload_to='trabalhos/mostra_tecnologica', verbose_name='resumo do projeto')),
                ('area', models.ForeignKey(verbose_name='\xe1rea de interesse', to='trabalhos.Area')),
            ],
            options={
                'abstract': False,
            },
            bases=('eventos.inscricao',),
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('inscricao_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='eventos.Inscricao')),
                ('titulo', models.CharField(max_length=255, verbose_name='t\xedtulo')),
                ('nome_autor', models.CharField(max_length=255, verbose_name='nome completo do autor principal')),
                ('cpf_autor', models.CharField(max_length=11, verbose_name='CPF do autor principal')),
                ('nome_orientador', models.CharField(max_length=255, verbose_name='nome completo do orientador')),
                ('cpf_orientador', models.CharField(max_length=11, verbose_name='CPF do orientador')),
                ('aprovado', models.BooleanField(default=False, editable=False)),
                ('resumo_expandido', models.FileField(upload_to='trabalhos/posters')),
                ('area', models.ForeignKey(verbose_name='\xe1rea de interesse', to='trabalhos.Area')),
            ],
            options={
                'abstract': False,
            },
            bases=('eventos.inscricao',),
        ),
    ]
