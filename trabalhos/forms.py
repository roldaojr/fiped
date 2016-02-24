# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from localflavor.br.forms import BRCPFField
from .models import Poster, MostraTecnologica


class TrabalhoForm(forms.ModelForm):
    cpf_autor = BRCPFField(
        label='CPF do autor principal',
        help_text='insira apenas números sem traços nem pontos',
        max_length=11)

    cpf_orientador = BRCPFField(
        label='CPF do orientador',
        help_text='insira apenas números sem traços nem pontos',
        max_length=11)


class PosterForm(TrabalhoForm):
    class Meta:
        model = Poster
        fields = '__all__'


LINK_PLANO_PESQUISA = 'http://febrace.org.br/arquivos/site/_conteudo/pdf/dicas-plano-de-pesquisa.pdf'
LINK_RESUMO_PROJETO = 'http://febrace.org.br/arquivos/site/_conteudo/pdf/dicas-resumo.pdf'
LINK_RELATORIO_PROJETO = 'http://febrace.org.br/arquivos/site/_conteudo/pdf/normas-relatorio.pdf'


class MostraTecnologicaForm(TrabalhoForm):
    plano_pesquisa = forms.FileField(
        help_text='<a href="{0}">Modelo Plano de Pesquisa</a>'.format(LINK_PLANO_PESQUISA))
    resumo_projeto = forms.FileField(
        help_text='<a href="{0}">Modelo Resumo</a>'.format(LINK_RESUMO_PROJETO))
    relatorio_projeto = forms.FileField(
        help_text='<a href="{0}">Modelo Relatório</a>'.format(LINK_RELATORIO_PROJETO))

    class Meta:
        model = MostraTecnologica
        fields = '__all__'
