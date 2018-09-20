from djchoices import DjangoChoices, ChoiceItem
from django.db import models
from comum.models import Usuario
from eventos.models import Inscricao


class Oficina(models.Model):
    class Situacao(DjangoChoices):
        Pendente = ChoiceItem(0)
        Aprovado = ChoiceItem(1)
        Reprovado = ChoiceItem(2)

    nome = models.CharField(max_length=100)
    ministrante = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                    related_name='oficinas')
    arquivo = models.FileField(upload_to='oficinas', blank=False)
    situacao = models.IntegerField(choices=Situacao.choices,
                                   verbose_name='situação',
                                   default=0, editable=False)
    inscricoes = models.ManyToManyField(Inscricao, related_name='oficinas',
                                        blank=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class MesaRedonda(models.Model):
    class Situacao(DjangoChoices):
        Pendente = ChoiceItem(0)
        Aprovado = ChoiceItem(1)
        Reprovado = ChoiceItem(2)

    nome = models.CharField(max_length=100)
    ministrante = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                    related_name='mesasredondas')
    arquivo = models.FileField(upload_to='mesas_redondas', blank=False)
    situacao = models.IntegerField(choices=Situacao.choices,
                                   verbose_name='situação',
                                   default=0, editable=False)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'mesa-redonda'
        verbose_name_plural = 'mesas-redondas'

    def __str__(self):
        return self.nome
