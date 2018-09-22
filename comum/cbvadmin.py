from django.urls import reverse
from menu import MenuItem
from django.contrib.auth.models import Group
import cbvadmin
from cbvadmin.views.user import PasswordReset
from cbvadmin.cbvadmin import DefaultAdmin
from cbvadmin.options import GroupAdmin
from .models import Usuario
from .forms import UsuarioForm
from .views import Dashboard, MinhaInscricao


@cbvadmin.register('default')
class EventusDefaultAdmin(DefaultAdmin):
    dashboard_view_class = Dashboard
    minha_inscricao_view_class = MinhaInscricao

    def get_actions(self):
        actions = super().get_actions()
        actions.update({
            'minha_inscricao': 'collection',
        })
        return actions

    def get_menu(self):
        return [
            MenuItem('Painel', reverse('cbvadmin:dashboard'), weight=1),
            MenuItem('Minha inscrição', reverse('cbvadmin:minha_inscricao'),
                     weight=1),
            MenuItem('Configurações', reverse("dynamic_preferences:global"),
                     check=lambda r: r.user.has_perm('dynamic_preferences.change_globalpreferencemodel'),
                     weight=100)
        ]


@cbvadmin.register(Usuario)
class UsuarioAdmin(cbvadmin.ModelAdmin):
    passwordreset_view_class = PasswordReset
    list_display = ('nome_completo', 'nome_social', 'email', 'is_active')
    filter_fields = ('nome_completo', 'nome_social', 'email')
    form_class = UsuarioForm
    menu_weight = 10

    def get_actions(self):
        actions = super().get_actions()
        actions['passwordreset'] = 'object'
        return actions

    def has_permission(self, request, action, obj=None):
        if action == 'passwordreset':
            action = 'change'
        return super().has_permission(request, action, obj)

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus


@cbvadmin.register(Group)
class UsuarioGroupAdmin(GroupAdmin):
    menu_weight = 11

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus
