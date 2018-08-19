from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from comum.tests.factories import UsuarioFactory
from .factories import TrabalhoFactory, AreaTemaFactory, ModalidadeFactory
from ..models import Trabalho, AreaTema
import factory


class SubmeterTrabalhoTestCase(TestCase):
    def setUp(self):
        AreaTemaFactory.create()
        ModalidadeFactory.create()
        self.usuario = UsuarioFactory.create(perms=['trabalhos.add_trabalho'])
        self.client.force_login(self.usuario)

    def test_submeter(self):
        trabalho = TrabalhoFactory.build(
            autor=self.usuario, coautor1=None,
            coautor2=None, coautor3=None,
            arquivo__data=factory.Faker('binary', length=1024))
        trabalho_dict = model_to_dict(
            trabalho, exclude=('coautor1', 'coautor2', 'coautor3'))
        resp = self.client.post(reverse('cbvadmin:trabalhos_trabalho_add'),
                                trabalho_dict)
        self.assertEqual(resp.status_code, 302)

        trabalho = Trabalho.objects.last()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Pendente)


class AvaliarTrabalhoTestCase(TestCase):
    def setUp(self):
        AreaTemaFactory.create()
        ModalidadeFactory.create()
        self.usuario = UsuarioFactory.create(
            perms=['trabalhos.change_trabalho'])
        self.client.force_login(self.usuario)

    def test_aprovar(self):
        trabalho = TrabalhoFactory.create()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Pendente)
        self.client.post(
            reverse('cbvadmin:trabalhos_trabalho_avaliar', args=[trabalho.pk]),
            {'situacao': 1}
        )
        trabalho = Trabalho.objects.last()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Aprovado)

    def test_reprovar(self):
        trabalho = TrabalhoFactory.create()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Pendente)
        self.client.post(
            reverse('cbvadmin:trabalhos_trabalho_avaliar', args=[trabalho.pk]),
            {'situacao': 2}
        )
        trabalho = Trabalho.objects.last()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Reprovado)
