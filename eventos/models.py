# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from comum.models import Usuario


@python_2_unicode_compatible
class Evento(models.Model):
    nome = models.CharField("nome", max_length=255, unique=True)
    data_inicial = models.DateField("data inicial")
    data_final = models.DateField("data final")

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Atividade(models.Model):
    nome = models.CharField("nome", max_length=255)
    local = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.tipo:
            return '{0} {1}'.format(self.tipo, self.nome)
        else:
            return '{0}'.format(self.nome)


@python_2_unicode_compatible
class Horario(models.Model):
    atividade = models.ForeignKey(Atividade, related_name='horarios')
    data = models.DateField()
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()

    def __str__(self):
        return '{0} das {1} ãs {2}'.format(self.data, self.hora_inicial, self.hora_final)

    class Meta:
        ordering = ('data', 'hora_inicial', 'hora_final')


class Inscricao(models.Model):
    atividade = models.ForeignKey(Atividade, related_name="inscricoes", editable=False)
    usuario = models.ForeignKey(Usuario, related_name="inscricoes", editable=False)
    espera = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'
        unique_together = ('atividade', 'usuario')
