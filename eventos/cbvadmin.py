import cbvadmin
from .models import Evento, Atividade, Inscricao


@cbvadmin.register(Evento)
class EventoAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'data_inicial', 'data_final')
    menu_weight = 1

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus


@cbvadmin.register(Atividade)
class AtividadeAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'tipo', 'local')
    menu_weight = 2

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus


@cbvadmin.register(Inscricao)
class InscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('atividade', 'usuario')
    menu_weight = 3

    def get_menu(self):
        menus = super().get_menu()
        menus[0].submenu = False
        return menus
