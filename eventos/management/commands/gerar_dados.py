from django.core.management.base import BaseCommand
from eventos.tests.factories import (InscricaoFactory, TipoInscricaoFactory,
                                     AtividadeFactory)
from trabalhos.tests.factories import (TrabalhoFactory, ModalidadeFactory,
                                       AreaTemaFactory)
from eventos.models import TipoInscricao, Inscricao, Atividade
from trabalhos.models import Trabalho, Modalidade, AreaTema


generate_models = [
    (TipoInscricao, TipoInscricaoFactory, 10),
    (Atividade, AtividadeFactory, 30)
    (Inscricao, InscricaoFactory, 500),
    (Modalidade, ModalidadeFactory, 5),
    (AreaTema, AreaTemaFactory, 30),
    (Trabalho, TrabalhoFactory, 100),
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, factory, size in generate_models:
            self.stdout.write('Gerando %d %s...' % (
                size, model._meta.verbose_name_plural))
            factory.create_batch(size)
