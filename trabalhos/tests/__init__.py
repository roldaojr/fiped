from faker import Faker
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from comum.models import Usuario
from .factory import TrabalhoFactory, AreaTemaFactory, ModalidadeFactory
from ..models import Trabalho


class SubmeterTrabalhoTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.area = AreaTemaFactory.create()
        self.modalidade = ModalidadeFactory.create()
        self.usuario = Usuario.objects.create_superuser(
            email=self.faker.email(),
            nome_completo=self.faker.name(),
            password='123456'
        )
        self.client.force_login(self.usuario)

    def test_submeter(self):
        trabalho_dict = {
            'modalidade': self.modalidade.pk,
            'titulo': self.faker.words(nb=8, ext_word_list=None),
            'autor': self.usuario.pk,
            'coautor1': '',
            'coautor2': '',
            'coautor3': '',
            'area_tema': self.area.pk,
            'arquivo': SimpleUploadedFile(
                self.faker.file_name(),
                self.faker.binary(length=10240),
                content_type="application/ms-word"
            )
        }
        resp = self.client.post(reverse('cbvadmin:trabalhos_trabalho_add'),
                                trabalho_dict)
        self.assertEqual(resp.status_code, 302)

        trabalho = Trabalho.objects.last()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Pendente)


class AvaliarTrabalhoTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.usuario = Usuario.objects.create_superuser(
            email=self.faker.email(),
            nome_completo=self.faker.name(),
            password=self.faker.password()
        )
        self.client.force_login(self.usuario)
        self.trabalho = TrabalhoFactory.create()

    def test_aprovar(self):
        trabalho = TrabalhoFactory()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Pendente)
        self.client.post(
            reverse('cbvadmin:trabalhos_trabalho_avaliar', args=[trabalho.pk]),
            {'situacao': 1}
        )
        trabalho = Trabalho.objects.last()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Aprovado)

    def test_reprovar(self):
        trabalho = TrabalhoFactory()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Pendente)
        self.client.post(
            reverse('cbvadmin:trabalhos_trabalho_avaliar', args=[trabalho.pk]),
            {'situacao': 2}
        )
        trabalho = Trabalho.objects.last()
        self.assertEqual(trabalho.situacao, Trabalho.Situacao.Reprovado)
