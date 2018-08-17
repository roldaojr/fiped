from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from .factories import TipoInscricaoFactory, InscricaoFactory


class InscricaoParticipanteTestCase(TestCase):
    def test_inscrever_se(self):
        TipoInscricaoFactory.create()
        inscricao = InscricaoFactory.build()
        pariticpante_data = model_to_dict(inscricao)
        pariticpante_data.update({
            'nome_completo': inscricao.usuario.nome_completo,
            'cpf': inscricao.usuario.cpf,
            'email': inscricao.usuario.email
        })
        resp = self.client.post(reverse('registration_register'),
                                pariticpante_data)
        self.assertEqual(resp.status_code, 302)
        # testar usuario
        usuario = resp.context['user']
        self.assertEqual(usuario.is_active, False)
        # testar inscricao
        inscricao_data = model_to_dict(usuario.inscricao)
        for k, v in inscricao_data.items():
            if k != 'id':
                self.assertEqual(v, pariticpante_data[k])
