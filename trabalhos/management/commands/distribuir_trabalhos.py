from django.core.management.base import BaseCommand
from trabalhos.models import Trabalho, distribuir_trabalho


class Command(BaseCommand):
    help = 'Distribuir trabalhos sem avaliador'

    def handle(self, *args, **options):
        trabalhos = Trabalho.objects.filter(avaliador__isnull=True)
        self.stdout.write('Distribuindo %d trabalhos' % trabalhos.count())
        for trabalho in trabalhos:
            #distribuir_trabalho(Trabalho, trabalho)
            trabalho.save()
