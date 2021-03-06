from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.formats import date_format, time_format, number_format
from djchoices import DjangoChoices, ChoiceItem
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from pagseguro.signals import notificacao_status_pago
from dynamic_preferences.registries import global_preferences_registry
from comum.models import Usuario


class Atividade(models.Model):
    nome = models.CharField(max_length=255)
    local = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.tipo:
            return '{0} {1}'.format(self.tipo, self.nome)
        else:
            return '{0}'.format(self.nome)


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
        return '{0}, de {1} às {2}'.format(data, hora_i, hora_f)

    class Meta:
        ordering = ('data', 'hora_inicial', 'hora_final')


class TipoInscricao(models.Model):
    nome = models.CharField('nome', max_length=200)
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='preço')
    validar = models.BooleanField(
        default=False, help_text='Validar inscrição desse tipo')
    limite = models.IntegerField(
        default=0, help_text='0 para ilimitado')

    class Meta:
        verbose_name = 'tipo de inscrição'
        verbose_name_plural = 'tipos de inscrição'
        ordering = ('nome',)

    def __str__(self):
        if self.preco > 0:
            return '%s (R$ %s)' % (self.nome,
                                   number_format(self.preco))
        return self.nome


class Inscricao(models.Model):
    class Pagamento(DjangoChoices):
        Pendente = ChoiceItem(0)
        Pago = ChoiceItem(1)
        Recusado = ChoiceItem(2)

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, editable=False,
        related_name='inscricao')
    # Inistituição
    instituicao = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name='instituição')
    titulacao = models.CharField(max_length=50, blank=True, null=True,
                                 verbose_name='titulação')
    deficiencia = models.CharField(max_length=300, blank=True, null=True,
                                   verbose_name='deficiência')
    # Endereço
    endereco = models.CharField(max_length=300, blank=True, null=True,
                                verbose_name='endereço')
    numero = models.CharField(max_length=10, blank=True, null=True,
                              verbose_name='número')
    cidade = models.CharField(max_length=50, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True,
                          verbose_name='UF')
    # relativo ao evento
    tipo = models.ForeignKey(TipoInscricao, on_delete=models.CASCADE,
                             related_name='inscricoes', blank=False, null=True)
    alojamento = models.BooleanField(default=False)
    atividades = models.ManyToManyField(Atividade, related_name='inscricoes',
                                        blank=True)
    validado = models.BooleanField(default=True)
    pagamento = models.IntegerField(choices=Pagamento.choices,
                                    default=Pagamento.Pendente)
    desconto = models.IntegerField(
        default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    class Meta:
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'
        ordering = ('usuario__nome_completo',)

    @property
    def valor(self):
        valor = (1 - self.desconto / 100) * float(self.tipo.preco)
        return Decimal(valor).quantize(Decimal('.01'))


def atualizar_pagamento_inscricao_paypal(sender, **kwargs):
    if sender.payment_status == ST_PP_COMPLETED:
        prefs = global_preferences_registry.manager()
        if sender.receiver_email != prefs['pagamento__paypal_email']:
            return
        inscricao = Inscricao.objects.get(pk=sender.invoice)
        inscricao.pagamento = Inscricao.Pagamento.Pago
        inscricao.save()


def atualizar_pagamento_insscricao_pagseguro(sender, transaction, **kwargs):
    if transaction['reference']:
        inscricao = Inscricao.objects.get(pk=transaction['reference'])
        inscricao.pagamento = Inscricao.Pagamento.Pago
        inscricao.save()


valid_ipn_received.connect(atualizar_pagamento_inscricao_paypal)
notificacao_status_pago.connect(atualizar_pagamento_insscricao_pagseguro)
