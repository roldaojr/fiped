# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.timezone import now
from .forms import PosterForm, MostraTecnologicaForm
from eventos.models import Evento


@login_required
def submeter(request):
    evento = Evento.objects.first()
    return render(request, 'trabalhos/index.html', {
        'pode_submeter': evento.def_trabalhos.prazo > now(),
        'def_trabalhos': evento.def_trabalhos
    })

@login_required
def submeter_poster(request):
    def_trabalhos = Evento.objects.first().def_trabalhos
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
    def_trabalhos = Evento.objects.first().def_trabalhos
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
