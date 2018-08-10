# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from eventos.models import Inscricao, Evento


class Definicoes(models.Model):
    evento = models.OneToOneField(Evento, primary_key=True,
                                  on_delete=models.CASCADE,
                                  related_name='def_trabalhos')
    prazo = models.DateTimeField('prazo para submissão', default=now)
    # poster
    submeter_poster = models.BooleanField(
        'habilitar submissão de poster', default=False)
    modelo_poster = models.FileField(
        'Modelo de Poster', null=True, blank=True,
        upload_to='modelos/poster')
    # mostra tecnologica
    submeter_mostra = models.BooleanField(
        'habilitar submissão de mostra tecnologica', default=False)
    modelo_plano_pesquisa = models.FileField(
        'Modelo de Plano de pesquisa', null=True, blank=True,
        upload_to='modelos/plano_pesquisa')
    modelo_relatorio = models.FileField(
        'Modelo de Relatório', null=True, blank=True,
        upload_to='modelos/relatorio')
    modelo_resumo = models.FileField(
        'Modelo de Resumo', null=True, blank=True,
        upload_to='modelos/resumo')

    @classmethod
    def do_evento(cls, evento):
        if not hasattr(evento, 'def_trabalhos'):
            evento.def_trabalhos = cls.objects.create(evento=evento)
        return evento.def_trabalhos

    class Meta:
        verbose_name = 'definição de trabalhos'
        verbose_name_plural = 'definições de trabalhos'


@python_2_unicode_compatible
class Area(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Trabalho(Inscricao):
    titulo = models.CharField('título', max_length=255)
    nome_autor = models.CharField('nome completo do autor principal',
                                  max_length=255)
    cpf_autor = models.CharField('CPF do autor principal', max_length=11)
    nome_orientador = models.CharField('nome completo do orientador',
                                       max_length=255)
    cpf_orientador = models.CharField('CPF do orientador', max_length=11)
    area = models.ForeignKey(Area, on_delete=models.CASCADE,
                             verbose_name="área de interesse")
    aprovado = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.titulo

    class Meta:
        abstract = True


class Poster(Trabalho):
    resumo_expandido = models.FileField(upload_to='trabalhos/posters')


class MostraTecnologica(Trabalho):
    plano_pesquisa = models.FileField(
        verbose_name='plano de pesquisa',
        upload_to='trabalhos/mostra_tecnologica')
    relatorio_projeto = models.FileField(
        verbose_name='relatório do projeto',
        upload_to='trabalhos/mostra_tecnologica')
    resumo_projeto = models.FileField(
        verbose_name='resumo do projeto',
        upload_to='trabalhos/mostra_tecnologica')
