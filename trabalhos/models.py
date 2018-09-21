from django.db import models
from djchoices import DjangoChoices, ChoiceItem
from comum.models import Usuario


class AreaTema(models.Model):
    nome = models.CharField(max_length=300)
    avaliadores = models.ManyToManyField(Usuario)

    class Meta:
        verbose_name = 'área/tema'
        verbose_name_plural = 'áreas/temas'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Modalidade(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Trabalho(models.Model):
    class Situacao(DjangoChoices):
        Pendente = ChoiceItem(0)
        Aprovado = ChoiceItem(1)
        Reprovado = ChoiceItem(2)
        Corrigir = ChoiceItem(3, 'Necessita correção')
        Reenviado = ChoiceItem(4)

    modalidade = models.ForeignKey(Modalidade, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=300, verbose_name='título')
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='+')
    coautor1 = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, blank=True, null=True,
        related_name='+')
    coautor2 = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, blank=True, null=True,
        related_name='+')
    coautor3 = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, blank=True, null=True,
        related_name='+')
    area_tema = models.ForeignKey(
        AreaTema, on_delete=models.CASCADE, verbose_name='área/tema')
    arquivo = models.FileField(upload_to='trabalhos', blank=False)
    situacao = models.IntegerField(
        choices=Situacao.choices, verbose_name='situação', default=0,
        editable=False)

    class Meta:
        ordering = ('titulo',)

    def __str__(self):
        return self.titulo
