from django.forms.models import model_to_dict
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from comum.tests.factories import UsuarioFactory
from .factories import TipoInscricaoFactory, InscricaoFactory
from ..models import Inscricao
import factory


class InscricaoTestCase(TestCase):
    def test_inscrever_se(self):
        TipoInscricaoFactory.create()
        inscricao = InscricaoFactory.build()
        senha = factory.Faker('password')
        pariticpante_data = model_to_dict(inscricao)
        pariticpante_data.update({
            'nome_completo': inscricao.usuario.nome_completo,
            'cpf': inscricao.usuario.cpf,
            'email': inscricao.usuario.email,
            'senha': senha,
            'confirmar_senha': senha
        })
        resp = self.client.post(reverse('registration_register'),
                                pariticpante_data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('registration_complete'))
        # testar usuario
        usuario = resp.context['user']
        self.assertEqual(usuario.is_active, False)
        # testar inscricao
        inscricao_data = model_to_dict(usuario.inscricao)
        for k, v in inscricao_data.items():
            if k != 'id':
                self.assertEqual(v, pariticpante_data[k])
        # testar se é membro do grupo
        self.assertIn(
            Group.objects.get(name='Participante'),
            usuario.groups.all()
        )

    def test_inscrever_se_e_validar(self):
        TipoInscricaoFactory.create(validar=True)
        inscricao = InscricaoFactory.build()
        senha = factory.Faker('password')
        pariticpante_data = model_to_dict(inscricao)
        pariticpante_data.update({
            'nome_completo': inscricao.usuario.nome_completo,
            'cpf': inscricao.usuario.cpf,
            'email': inscricao.usuario.email,
            'senha': senha,
            'confirmar_senha': senha
        })
        resp = self.client.post(reverse('registration_register'),
                                pariticpante_data)
        # testar se inscrição não está validada
        usuario = resp.context['user']
        self.assertFalse(usuario.inscricao.validado)

    def test_validar_inscricao(self):
        usuario = UsuarioFactory.create(perms=['eventos.change_inscricao'])
        self.client.force_login(usuario)
        TipoInscricaoFactory.create(validar=True)
        inscricao = InscricaoFactory.create(validado=False)
        baseurl = reverse('cbvadmin:eventos_inscricao_validar',
                          args=[inscricao.pk])
        resp = self.client.get('%s?validado=1' % baseurl)
        self.assertEqual(resp.status_code, 302)
        inscricao = Inscricao.objects.get(pk=inscricao.pk)
        self.assertTrue(inscricao.validado)
