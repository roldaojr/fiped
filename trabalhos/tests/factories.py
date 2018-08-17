import factory
from comum.tests.factories import UsuarioFactory
from ..models import Trabalho, AreaTema, Modalidade


class ModalidadeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Modalidade

    nome = factory.Faker('sentence', nb_words=3)


class AreaTemaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AreaTema

    nome = factory.Faker('sentence', nb_words=5)


class TrabalhoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trabalho

    modalidade = factory.Iterator(Modalidade.objects.all())
    titulo = factory.Faker('sentence', nb_words=10)
    autor = factory.SubFactory(UsuarioFactory)
    coautor1 = factory.SubFactory(UsuarioFactory)
    coautor2 = factory.SubFactory(UsuarioFactory)
    coautor3 = factory.SubFactory(UsuarioFactory)
    area_tema = factory.Iterator(AreaTema.objects.all())
    arquivo = factory.django.FileField()
