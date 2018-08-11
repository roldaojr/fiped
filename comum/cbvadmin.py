import cbvadmin
from cbvadmin.options import GroupAdmin
from cbvadmin.views.user import PasswordReset
from .models import Usuario, Group


@cbvadmin.register(Usuario)
class UsuarioAdmin(cbvadmin.ModelAdmin):
    list_display = ('id', 'nome_completo', 'email', 'instituicao', 'ativo')
    passwordreset_view_class = PasswordReset
    menu_weight = 2

    def get_actions(self):
        actions = super().get_actions()
        actions['passwordreset'] = 'object'
        return actions

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus


@cbvadmin.register(Group)
class GroupAdmin(GroupAdmin):
    menu_weight = 3

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus
