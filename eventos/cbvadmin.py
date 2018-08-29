from django.urls import reverse
from menu import MenuItem
from dynamic_preferences.registries import global_preferences_registry
import cbvadmin
from cbvadmin.options import SimpleAdmin
from comum.views import DetailView
from .models import Atividade, Inscricao, TipoInscricao
from .filters import InscricaoFilter
from .views import ImprimirLista, EscolherAtividade
from .views.pagamento import VisualizarPagamento, InscricaoPagarPagSeguro
from .forms import EditarInscricaoForm


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
        def pode_escolher_atividades(request):
            prefs = global_preferences_registry.manager()
            return (prefs['evento__inscricao_atividade'] and
                    hasattr(request.user, 'inscricao'))

        menus = super().get_menu()
        menus.append(
            MenuItem('Escolher atividades',
                     reverse(self.urls['escolher']),
                     weight=1, icon=self.menu_icon, submenu=False,
                     check=pode_escolher_atividades)
        )
        return menus


@cbvadmin.register(TipoInscricao)
class TipoInscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'preco', 'limite')
    menu_weight = 4


@cbvadmin.register(Inscricao)
class InscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'alojamento', 'deficiencia')
    filterset_class = InscricaoFilter
    imprimir_view_class = ImprimirLista
    detail_view_class = DetailView
    default_object_action = 'detail'
    pagar_pagseguro_view_class = InscricaoPagarPagSeguro
    form_class = EditarInscricaoForm
    menu_weight = 3

    def has_permission(self, request, action, obj=None):
        if action == 'imprimir':
            action = 'view'
        return super().has_permission(request, action, obj)

    def get_actions(self):
        actions = super().get_actions()
        del actions['add']
        actions.update({
            'detail': 'object',
            'imprimir': 'collection',
            'pagar_pagseguro': 'object'
        })
        return actions


@cbvadmin.register('pagamento')
class PagamentoAdmin(SimpleAdmin):
    pagar_view_class = VisualizarPagamento
    default_action = 'pagar'

    def get_actions(self):
        return {'pagar': 'collection'}

    def get_menu(self):
        return None
