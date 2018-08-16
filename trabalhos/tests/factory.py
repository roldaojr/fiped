import factory
from comum.models import Usuario
from ..models import Trabalho, AreaTema, Modalidade


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    nome_completo = factory.Faker('name')
    email = factory.Faker('email')


class ModalidadeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Modalidade

    nome = factory.Faker('sentence')


class AreaTemaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AreaTema

    nome = factory.Faker('sentence', nb_words=4)


class TrabalhoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trabalho

    modalidade = factory.SubFactory(ModalidadeFactory)
    titulo = factory.Faker('sentence', nb_words=6)
    autor = factory.SubFactory(UsuarioFactory)
    coautor1 = factory.SubFactory(UsuarioFactory)
    coautor2 = factory.SubFactory(UsuarioFactory)
    coautor3 = factory.SubFactory(UsuarioFactory)
    area_tema = factory.SubFactory(AreaTemaFactory)
    arquivo = factory.django.FileField()
