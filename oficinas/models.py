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
    vagas = models.IntegerField(default=0)
    situacao = models.IntegerField(choices=Situacao.choices,
                                   verbose_name='situação',
                                   default=0, editable=False)
    inscricoes = models.ManyToManyField(Inscricao, related_name='oficinas',
                                        blank=True, editable=False)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def vagas_restantes(self):
        return self.vagas - self.inscricoes.count()


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
    inscricoes = models.ManyToManyField(Inscricao, blank=True, editable=False,
                                        related_name='mesasredondas')

    class Meta:
        ordering = ('nome',)
        verbose_name = 'mesa-redonda'
        verbose_name_plural = 'mesas-redondas'

    def __str__(self):
        return self.nome


class Seminario(models.Model):
    class Situacao(DjangoChoices):
        Pendente = ChoiceItem(0)
        Aprovado = ChoiceItem(1)
        Reprovado = ChoiceItem(2)

    nome = models.CharField(max_length=100)
    ministrante = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                    related_name='seminarios')
    arquivo = models.FileField(upload_to='seminarios', blank=False)
    vagas = models.IntegerField(default=0)
    situacao = models.IntegerField(choices=Situacao.choices,
                                   verbose_name='situação',
                                   default=0, editable=False)
    inscricoes = models.ManyToManyField(Inscricao, related_name='seminarios',
                                        blank=True, editable=False)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'seminário temático'
        verbose_name_plural = 'seminários temáticos'

    def __str__(self):
        return self.nome

    def vagas_restantes(self):
        return self.vagas - self.inscricoes.count()


class Livro(models.Model):
    class Situacao(DjangoChoices):
        Pendente = ChoiceItem(0)
        Aprovado = ChoiceItem(1)
        Reprovado = ChoiceItem(2)

    titulo = models.CharField(max_length=100)
    editora = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100, verbose_name='ISBN')
    ano = models.IntegerField()
    autores = models.CharField(max_length=100)
    biografia = models.TextField()
    resumo = models.TextField()
    palavras_chave = models.CharField(max_length=100)
    paginas = models.IntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2,
                                verbose_name='preço')
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    email = models.CharField(max_length=100, verbose_name='e-mail')
    capa = models.FileField(upload_to='livros', blank=False, null=False)
    situacao = models.IntegerField(choices=Situacao.choices,
                                   verbose_name='situação',
                                   default=0, editable=False)

    def __str__(self):
        return self.titulo
