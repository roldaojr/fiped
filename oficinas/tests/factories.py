import factory
from comum.tests.factories import UsuarioFactory
from ..models import Oficina, MesaRedonda


class OficinaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Oficina

    nome = factory.Faker('sentence', nb_words=10)
    ministrante = factory.SubFactory(UsuarioFactory)
    arquivo = factory.django.FileField()


class MesaRedondaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MesaRedonda

    nome = factory.Faker('sentence', nb_words=10)
    ministrante = factory.SubFactory(UsuarioFactory)
    arquivo = factory.django.FileField()
