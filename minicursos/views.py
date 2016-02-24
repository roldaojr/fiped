# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models.query import Prefetch
from eventos.models import Inscricao, Evento
from eventos.decorators import evento_view
from .models import Minicurso


@login_required
def minicurso_listar(request):
    inscricoes = Inscricao.objects.filter(usuario=request.user)
    minicursos = Minicurso.objects.prefetch_related(
        Prefetch('inscricoes', queryset=inscricoes, to_attr='inscricoes_do_usuario')
    )
    return render(request, 'minicursos/listar.html', {
        'minicursos': minicursos,
    })


@login_required
def minicurso_detalhes(request, minicurso_id):
    minicurso = Minicurso.objects.get(pk=minicurso_id)
    def_minicursos = Evento.objects.first().def_minicursos
    qtd_inscricoes = request.user.inscricoes.filter(atividade__tipo='Minicurso').count()
    try:
        inscricao = minicurso.inscricoes.get(usuario=request.user)
    except:
        inscricao = None
    return render(request, 'minicursos/detalhes.html', {
        'minicurso': minicurso,
        'inscricao': inscricao,
        'pode_inscrever': qtd_inscricoes < def_minicursos.maximo,
        'inscricao_maximimo': def_minicursos.maximo
    })


@login_required
@transaction.atomic
def minicurso_inscricao(request, minicurso_id):
    def_minicursos = Evento.objects.first().def_minicursos
    if request.method == 'POST':
        minicurso = Minicurso.objects.get(pk=minicurso_id)
        cancelar = request.POST.get('cancelar', 'false') == 'true'
        espera   = request.POST.get('espera', 'false') == 'true'
        print cancelar
        print espera
        if cancelar: # cancelar inscrição
            minicurso.inscricoes.get(usuario=request.user).delete()
        else:
            if (minicurso.tem_vagas_disponiveis or
                (espera and minicurso.tem_vagas_espera)):
                minicurso.inscricoes.create(usuario=request.user, espera=espera)
                messages.success(request, 'Inscrito no minicurso {}.'.format(minicurso.nome))
            else:
                messages.warning(request, 'Não há vagas disponiveis')
        return redirect(reverse('minicursos:listar'))
    raise Http404
