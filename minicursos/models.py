from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from eventos.models import Atividade, Inscricao, Evento


class Definicoes(models.Model):
    evento = models.OneToOneField(Evento, primary_key=True,
                                  on_delete=models.CASCADE,
                                  related_name='def_minicursos')
    maximo = models.IntegerField('máximo de inscrições por pessoa', default=1)

    @classmethod
    def do_evento(cls, evento):
        if not hasattr(evento, 'def_minicursos'):
            evento.def_minicursos = cls.objects.create(evento=evento)
        return evento.def_minicursos

    class Meta:
        verbose_name = 'definição de minicurso'
        verbose_name_plural = 'definições de minicurso'


class Ministrante(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(blank=True, null=True,
                             upload_to="fotos/ministrante")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Minicurso(Atividade):
    ministrante = models.ForeignKey(Ministrante, on_delete=models.CASCADE)
    descricao = models.TextField('descrição', null=True, blank=True)
    pre_requisitos = models.TextField('pré-requisitos', null=True, blank=True)
    vagas = models.PositiveIntegerField(default=0)
    inscritos = models.PositiveIntegerField(
        'número de inscritos', default=0)
    vagas_reserva = models.PositiveIntegerField(default=0)
    inscritos_reserva = models.PositiveIntegerField(
        'número de inscritos na reserva', default=0)

    @property
    def vagas_disponiveis(self):
        return self.vagas - self.inscritos

    @property
    def tem_vagas_disponiveis(self):
        return self.inscritos < self.vagas

    @property
    def tem_vagas_espera(self):
        return self.inscritos_reserva < self.vagas_reserva

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.tipo = 'Minicurso'
        super(Minicurso, self).save(*args, **kwargs)

    class Meta:
        ordering = ('nome',)


@receiver(post_save, sender=Inscricao)
def minicurso_vagas_create(sender, instance, created, **kwargs):
    if type(instance.atividade) == Minicurso:
        if instance.espera:
            instance.atividade.inscritos_reserva += 1
        else:
            instance.atividade.inscritos += 1
        instance.atividade.save()


@receiver(post_delete, sender=Inscricao)
def minicurso_vagas_delete(sender, instance, **kwargs):
    if type(instance.atividade) == Minicurso:
        if instance.espera:
            instance.atividade.inscritos_reserva -= 1
        else:
            instance.atividade.inscritos -= 1
        instance.atividade.save()
