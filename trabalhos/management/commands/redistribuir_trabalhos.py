from django.core.management.base import BaseCommand
from trabalhos.models import Trabalho, distribuir_trabalho


class Command(BaseCommand):
    help = 'Redistribuir trabalhos pendentes'

    def handle(self, *args, **options):
        trabalhos = Trabalho.objects.filter(situacao=Trabalho.Situacao.Pendente)
        self.stdout.write('Redistribuindo %d trabalhos' % trabalhos.count())
        trabalhos.update(avaliador=None)
        for trabalho in trabalhos:
            trabalho.save()
