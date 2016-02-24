# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsuarioForm, UsuarioPerfilForm

def home(request):
    return render(request, 'site/home.html')

def usuario_registrar(request):
    if request.method == 'POST':
        form = UsuarioForm(data=request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(user.password)
            usuario.save()
            return redirect(reverse('usuario_perfil'))
    else:
        form = UsuarioForm()
    return render(request, 'comum/usuario/registrar.html', {'form': form})


@login_required
def usuario_perfil(request):
    if request.method == 'POST':
        form = UsuarioPerfilForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com êxito.')
            return redirect(reverse('usuario_perfil'))
    else:
        form = UsuarioPerfilForm(instance=request.user)
        form.fields['cpf'].widget.attrs['readonly'] = "readonly"

    return render(request, 'comum/usuario/perfil.html', {'form': form})

@login_required
def alterar_senha_concluido(request):
    messages.success(request, 'Senha alterada com êxito.')
    return redirect(reverse('password_change'))
