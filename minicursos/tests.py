# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from comum.models import Usuario
from eventos.models import Inscricao
from .models import Minicurso, Ministrante


class InscricaoTestCase(TestCase):
    def setUp(self):
        self.user1 = Usuario.objects.create(email='user1@dmain.com', cpf='97858138863')
        self.user2 = Usuario.objects.create(email='user2@dmain.com', cpf='37157945770')
        self.user3 = Usuario.objects.create(email='user3@dmain.com', cpf='71252368801')
        ministrante1 = Ministrante.objects.create(nome='ministrante1')
        self.minicurso1 = Minicurso.objects.create(
            nome='Minicurso1', vagas=2,
            ministrante=ministrante1)
        self.minicurso2 = Minicurso.objects.create(
            nome='Minicurso2', vagas=1, vagas_reserva=1,
            ministrante=ministrante1)
        Inscricao.objects.create(usuario=self.user1, atividade=self.minicurso1)

    def test_inscrever_usuario(self):
        '''Incrição de usuário em minicurso aumenta numero de inscritos'''
        Inscricao.objects.create(usuario=self.user2, atividade=self.minicurso1)
        self.assertEqual(self.minicurso1.inscritos, 2)
        self.assertEqual(self.minicurso1.vagas_disponiveis, 0)

    def test_desincrever_usuario(self):
        '''Remover incrição de usuário em minicurso diminui numero de inscritos'''
        Inscricao.objects.filter(usuario=self.user1, atividade=self.minicurso1).delete()
        self.assertEqual(self.minicurso1.inscritos, 1)
        self.assertEqual(self.minicurso1.vagas_disponiveis, 1)

    def test_inscrever_em_reserva(self):
        '''Incrição de usuário em reserva minicurso aumenta numero de inscritos'''
        Inscricao.objects.create(usuario=self.user1, atividade=self.minicurso2)
        Inscricao.objects.create(usuario=self.user2, atividade=self.minicurso2, espera=True)
        self.assertEqual(self.minicurso2.inscritos, 1)
        self.assertEqual(self.minicurso2.inscritos_reserva, 1)
