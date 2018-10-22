from django.db import models
from django.dispatch import receiver
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
    carta_aceite = models.FileField(upload_to='cartas-de-aceite', blank=False,
                                    null=True, verbose_name='Carta de aceite')
    situacao = models.IntegerField(
        choices=Situacao.choices, verbose_name='situação', default=0,
        editable=False)
    avaliador = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                                  blank=True, null=True,
                                  related_name='trabalhos')
    observacoes = models.TextField(blank=True, null=True,
                                   verbose_name='observações')

    class Meta:
        ordering = ('titulo',)

    def __str__(self):
        return self.titulo


@receiver(models.signals.pre_save, sender=Trabalho)
def distribuir_trabalho(sender, instance, **kwargs):
    if instance.avaliador is None:
        avaliadores = instance.area_tema.avaliadores.annotate(
            total_trabalhos=models.Count('trabalhos')).order_by(
            'total_trabalhos')
        instance.avaliador = avaliadores.first()
