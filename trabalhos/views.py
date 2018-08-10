# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.timezone import now
from eventos.models import Evento
from .forms import PosterForm, MostraTecnologicaForm
from .models import Definicoes


@login_required
def submeter(request):
    def_trabalhos = Definicoes.do_evento(Evento.objects.first())
    return render(request, 'trabalhos/index.html', {
        'pode_submeter': def_trabalhos.prazo > now(),
        'def_trabalhos': def_trabalhos
    })


@login_required
def submeter_poster(request):
    def_trabalhos = Definicoes.do_evento(Evento.objects.first())
    if not def_trabalhos.submeter_poster:
        raise Http404
    if request.method == 'POST':
        form = PosterForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            messages.success(request, 'Poster submetido com êxito!')
            return redirect(reverse('area_usuario'))
    else:
        form = PosterForm()
    return render(request, 'trabalhos/submeter_form.html', {'form': form})


@login_required
def submeter_mostra(request):
    def_trabalhos = Definicoes.do_evento(Evento.objects.first())
    if not def_trabalhos.submeter_mostra:
        raise Http404
    if request.method == 'POST':
        form = MostraTecnologicaForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            messages.success(request, 'Mostra tecnológica submetida com êxito!')
            return redirect(reverse('trabalhos:submeter'))
    else:
        form = MostraTecnologicaForm()
    return render(request, 'trabalhos/submeter_form.html', {'form': form})
