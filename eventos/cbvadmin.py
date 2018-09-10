import cbvadmin
from cbvadmin.options import SimpleAdmin
from comum.views import DetailView
from .models import Inscricao, TipoInscricao
from .filters import InscricaoFilter
from .views import ImprimirLista, AnexarArquivoView, ValidarInscricaoView
from .views.pagamento import VisualizarPagamento, InscricaoPagarPagSeguro
from .forms import EditarInscricaoForm


@cbvadmin.register(TipoInscricao)
class TipoInscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'preco', 'validar', 'limite')
    menu_weight = 4


@cbvadmin.register(Inscricao)
class InscricaoAdmin(cbvadmin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'validado', 'alojamento')
    filterset_class = InscricaoFilter
    imprimir_view_class = ImprimirLista
    detail_view_class = DetailView
    anexar_view_class = AnexarArquivoView
    validar_view_class = ValidarInscricaoView
    default_object_action = 'detail'
    pagar_pagseguro_view_class = InscricaoPagarPagSeguro
    form_class = EditarInscricaoForm
    menu_weight = 3

    def has_permission(self, request, action, obj=None):
        if action == 'imprimir':
            action = 'view'
        if action == 'validar':
            action = 'change'
        return super().has_permission(request, action, obj)

    def get_actions(self):
        actions = super().get_actions()
        del actions['add']
        actions.update({
            'detail': 'object',
            'imprimir': 'collection',
            'anexar': 'collection',
            'pagar_pagseguro': 'object',
            'validar': 'object',
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
