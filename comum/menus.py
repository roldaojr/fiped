# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem


def usuario_autenticado(request):
    return request.user.is_authenticated()

def usuario_nao_autenticado(request):
    return not request.user.is_authenticated()

def nome_do_usuario(request):
    ''' Retorna o nome do perfil '''
    name = request.user.get_full_name() or request.user
    return name

menu_do_usuario = [
    MenuItem('Atualizar Perfil', reverse('usuario_perfil')),
    MenuItem('Alterar senha', reverse('password_change')),
    MenuItem('Administração', reverse("admin:index"), separator=True,
             check=lambda request: request.user.is_superuser),
    MenuItem("Sair", reverse('logout'), separator=True)
]

Menu.add_item('usuario', MenuItem('Inscrever-se', reverse('usuario_registrar'),
                                  check=usuario_nao_autenticado))
Menu.add_item('usuario', MenuItem('Entrar', reverse('login'),
                                  check=usuario_nao_autenticado))
Menu.add_item('usuario', MenuItem(nome_do_usuario, '#',
                                  children=menu_do_usuario,
                                  check=usuario_autenticado))
