# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import date_format, time_format
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
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE,
                                  related_name='horarios')
    data = models.DateField()
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()

    def __str__(self):
        data = date_format(self.data)
        hora_i = time_format(self.hora_inicial)
        hora_f = time_format(self.hora_final)
        return '{0}, {1} às {2}'.format(data, hora_i, hora_f)

    class Meta:
        ordering = ('data', 'hora_inicial', 'hora_final')


class Inscricao(models.Model):
    atividade = models.ForeignKey(Atividade, editable=False, null=True,
                                  on_delete=models.CASCADE,
                                  related_name="inscricoes")
    usuario = models.ForeignKey(Usuario, editable=False,
                                on_delete=models.CASCADE,
                                related_name="inscricoes")
    espera = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'
        unique_together = ('atividade', 'usuario')
