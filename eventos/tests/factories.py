import factory
from comum.tests.factories import UsuarioFactory
from ..models import Inscricao, TipoInscricao


class TipoInscricaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TipoInscricao

    nome = factory.Faker('sentence', nb_words=4)
    preco = factory.Faker('pydecimal', left_digits=3, right_digits=0,
                          positive=True)


class InscricaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inscricao

    usuario = factory.SubFactory(UsuarioFactory)
    instituicao = factory.Faker('text', max_nb_chars=50)
    titulacao = factory.Faker('text', max_nb_chars=25)
    deficiencia = factory.Faker('text', max_nb_chars=50)
    endereco = factory.Faker('street_name')
    numero = factory.Faker('building_number')
    cidade = factory.Faker('city')
    uf = factory.Faker('estado_sigla', locale='pt_BR')
    tipo = factory.Iterator(TipoInscricao.objects.all())
    alojamento = factory.Faker('boolean', chance_of_getting_true=30)
