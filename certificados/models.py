import os
from django.db import models
from django.utils.text import slugify
from shortuuidfield import ShortUUIDField
from eventos.models import Inscricao


def upload_imagem(instance, filename):
    ext = filename.split('.')[-1]
    name = slugify(instance.nome)
    filename = os.path.join('certificados', '.'.join([name, ext]))
    if os.path.exists(filename):
        os.remove(filename)
    return filename


class ModeloCertificado(models.Model):
    nome = models.CharField(max_length=300)
    paisagem = models.BooleanField(default=True)
    caixa_largura = models.FloatField()
    caixa_altura = models.FloatField()
    caixa_esquerda = models.FloatField()
    caixa_topo = models.FloatField()
    tamanho_fonte = models.IntegerField(default=18)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to=upload_imagem,
                               blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Modelo de Certificado'
        verbose_name_plural = 'Modelos de Certificado'


class Certificado(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    nome = models.CharField(max_length=300)
    atividade = models.CharField(max_length=300)
    tipo_atividade = models.CharField(max_length=30, blank=True, null=True)
    modelo = models.ForeignKey(ModeloCertificado, on_delete=models.CASCADE,
                               related_name='certificados')
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE,
                                  related_name='certificados')

    def __str__(self):
        return 'Certificado de %s (%s)' % (self.nome, self.tipo_atividade)

    class Meta:
        unique_together = ('atividade', 'tipo_atividade', 'inscricao')
