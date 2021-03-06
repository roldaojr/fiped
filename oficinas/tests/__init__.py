from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from dynamic_preferences.registries import global_preferences_registry
from comum.tests.factories import UsuarioFactory
from eventos.tests.factories import InscricaoFactory, TipoInscricaoFactory
from .factories import OficinaFactory, MesaRedondaFactory
from ..models import Oficina, MesaRedonda
import factory


class SubmeterOficinaTestCase(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory.create(perms=['oficinas.add_oficina'])
        self.client.force_login(self.usuario)

    def test_submeter(self):
        oficina = OficinaFactory.build(
            ministrante=self.usuario,
            arquivo__data=factory.Faker(
                'binary', length=settings.FILE_UPLOAD_MAX_SIZE))
        oficina_dict = model_to_dict(oficina)
        resp = self.client.post(reverse('cbvadmin:oficinas_oficina_add'),
                                oficina_dict)
        self.assertEqual(resp.status_code, 302)

        oficina = Oficina.objects.last()
        self.assertEqual(oficina.situacao, Oficina.Situacao.Pendente)

        resp = self.client.get(resp.url)
        self.assertEqual(resp.status_code, 200)


class AvaliarOficinaTestCase(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory.create(perms=['oficinas.change_oficina'])
        self.client.force_login(self.usuario)

    def test_aprovar(self):
        oficina = OficinaFactory.create()
        self.assertEqual(oficina.situacao, Oficina.Situacao.Pendente)
        self.client.post(
            reverse('cbvadmin:oficinas_oficina_avaliar', args=[oficina.pk]),
            {'situacao': 1})
        oficina = Oficina.objects.last()
        self.assertEqual(oficina.situacao, Oficina.Situacao.Aprovado)

    def test_reprovar(self):
        oficina = OficinaFactory.create()
        self.assertEqual(oficina.situacao, Oficina.Situacao.Pendente)
        self.client.post(
            reverse('cbvadmin:oficinas_oficina_avaliar', args=[oficina.pk]),
            {'situacao': 2})
        oficina = Oficina.objects.last()
        self.assertEqual(oficina.situacao, Oficina.Situacao.Reprovado)


class InscreverOficinaTestCase(TestCase):
    def setUp(self):
        TipoInscricaoFactory.create()
        inscricao = InscricaoFactory.create()
        self.client.force_login(inscricao.usuario)
        prefs = global_preferences_registry.manager()
        prefs['oficinas__inscricao'] = True
        self.oficinas = OficinaFactory.create_batch(3)
        for o in self.oficinas:
            o.situacao = Oficina.Situacao.Aprovado
            o.save()

    def test_inscrever(self):
        resp = self.client.post(
            reverse('cbvadmin:oficinas_oficina_inscricao'),
            {'oficinas': [self.oficinas[0].pk]})
        self.assertEqual(resp.status_code, 302)


class SubmeterMesaRedondaTestCase(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory.create(
            perms=['oficinas.add_mesaredonda'])
        self.client.force_login(self.usuario)

    def test_submeter(self):
        mesaredonda = MesaRedondaFactory.build(
            ministrante=self.usuario,
            arquivo__data=factory.Faker('binary', length=1024))
        mesaredonda_dict = model_to_dict(mesaredonda)
        resp = self.client.post(reverse('cbvadmin:oficinas_mesaredonda_add'),
                                mesaredonda_dict)
        self.assertEqual(resp.status_code, 302)

        mesaredonda = MesaRedonda.objects.last()
        self.assertEqual(mesaredonda.situacao, MesaRedonda.Situacao.Pendente)

        resp = self.client.get(resp.url)
        self.assertEqual(resp.status_code, 200)


class AvaliarMesaRedondaTestCase(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory.create(
            perms=['oficinas.change_mesaredonda'])
        self.client.force_login(self.usuario)

    def test_aprovar(self):
        mesaredonda = MesaRedondaFactory.create()
        self.assertEqual(mesaredonda.situacao, MesaRedonda.Situacao.Pendente)
        self.client.post(reverse('cbvadmin:oficinas_mesaredonda_avaliar', args=[
                         mesaredonda.pk]), {'situacao': 1})
        mesaredonda = MesaRedonda.objects.last()
        self.assertEqual(mesaredonda.situacao, MesaRedonda.Situacao.Aprovado)

    def test_reprovar(self):
        mesaredonda = MesaRedondaFactory.create()
        self.assertEqual(mesaredonda.situacao, MesaRedonda.Situacao.Pendente)
        self.client.post(reverse('cbvadmin:oficinas_mesaredonda_avaliar', args=[
                         mesaredonda.pk]), {'situacao': 2})
        mesaredonda = MesaRedonda.objects.last()
        self.assertEqual(mesaredonda.situacao, MesaRedonda.Situacao.Reprovado)
