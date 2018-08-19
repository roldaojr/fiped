from django.urls import reverse
from menu import MenuItem
import cbvadmin
from comum.views import DetailView
from .models import Atividade, Inscricao, TipoInscricao
from .filters import InscricaoFilter
from .views import ImprimirLista, EscolherAtividade


@cbvadmin.register(Atividade)
class AtividadeAdmin(cbvadmin.ModelAdmin):
    escolher_view_class = EscolherAtividade
    list_display = ('nome', 'tipo', 'local')
    menu_weight = 2

    def has_permission(self, request, action, obj=None):
        if action == 'escolher':
            return True
        return super().has_permission(request, action, obj)

    def get_actions(self):
        actions = super().get_actions()
        actions.update({'escolher': 'collection'})
        return actions

    def get_menu(self):
        menus = super().get_menu()
        menus.append(
            MenuItem('Escolher atividades',
                     reverse(self.urls['escolher']),
                     weight=1, icon=self.menu_icon, submenu=False,
                     check=lambda r: bool(hasattr(r.user, 'inscricao')))
        )
        return menus


@cbvadmin.register(TipoInscricao)
class TipoInscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'preco')
    menu_weight = 4


@cbvadmin.register(Inscricao)
class InscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'alojamento', 'deficiencia')
    filterset_class = InscricaoFilter
    imprimir_view_class = ImprimirLista
    detail_view_class = DetailView
    default_object_action = 'detail'
    menu_weight = 3

    def get_actions(self):
        actions = super().get_actions()
        del actions['add']
        actions.update({'detail': 'object', 'imprimir': 'collection'})
        return actions
