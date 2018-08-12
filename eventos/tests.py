from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from .models import TipoInscricao


class InscricaoParticipanteTestCase(TestCase):
    def setUp(self):
        TipoInscricao.objects.create(nome='Gratis', preco=0)
        self.pariticpante_data = {
            'nome_completo': 'nome de teste',
            'cpf': '12345678909',
            'email': 'null@mail.com',
            'deficiencia': '',
            'endereco': 'Rua 1',
            'numero': 'Rua 2',
            'cidade': 'Cidade Z',
            'uf': 'UF',
            'titulacao': 'Bacharel',
            'instituicao': 'UERN',
            'alojamento': False,
            'tipo': 1
        }

    def test_inscrever_se(self):
        resp = self.client.post(reverse('registration_register'),
                                self.pariticpante_data)
        self.assertEqual(resp.status_code, 302)
        # testar usuario
        usuario = resp.context['user']
        self.assertEqual(usuario.is_active, False)
        # testar inscricao
        inscricao_data = model_to_dict(usuario.inscricao)
        for k, v in inscricao_data.items():
            if k != 'id':
                self.assertEqual(v, self.pariticpante_data[k])
