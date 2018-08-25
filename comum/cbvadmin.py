from django.urls import reverse
from menu import MenuItem
from django.contrib.auth.models import Group
import cbvadmin
from cbvadmin.cbvadmin import DefaultAdmin
from cbvadmin.options import GroupAdmin
from .models import Usuario
from .forms import UsuarioForm
from .views import Dashboard


@cbvadmin.register('default')
class EventusDefaultAdmin(DefaultAdmin):
    dashboard_view_class = Dashboard

    def get_menu(self):
        return [
            MenuItem('Painel', reverse('cbvadmin:dashboard')),
            MenuItem('Configurações', reverse("dynamic_preferences:global"),
                     weight=100)
        ]


@cbvadmin.register(Usuario)
class UsuarioAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome_completo', 'nome_social', 'email', 'is_active')
    filter_fields = ('nome_completo', 'nome_social', 'email')
    form_class = UsuarioForm
    menu_weight = 10

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
