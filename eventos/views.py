from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django_tables2.columns import Column
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import TemplateView
from paypal.standard.forms import PayPalPaymentsForm
from pagseguro.api import PagSeguroItem, PagSeguroApi
from dynamic_preferences.registries import global_preferences_registry
from cbvadmin.views.mixins import AdminMixin
from cbvadmin.views.list import TableListView
from cbvadmin.views.edit import EditView
from cbvadmin.tables import table_factory
from .filters import InscricaoFilter
from .forms import EscolherAtividadesForm
from .models import Inscricao


class ImprimirLista(TableListView):
    filterset_class = InscricaoFilter
    list_display = ('nome_completo', 'nome_social', 'cpf', 'email',
                    'tipo', 'alojamento', 'deficiencia')
    template_name_suffix = '_print_list'
    paginate_by = False

    def get_table_class(self):
        extra = {
            'nome_completo': Column(accessor='usuario.nome_completo'),
            'nome_social': Column(accessor='usuario.nome_social'),
            'cpf': Column(accessor='usuario.cpf'),
            'email': Column(accessor='usuario.email')
        }
        return table_factory(self.model, self.list_display, action=None,
                             extra=extra)


class EscolherAtividade(EditView):
    form_class = EscolherAtividadesForm
    default_template = 'eventos/atividade_escolher.html'
    permission_required = []

    def get_object(self):
        try:
            return self.request.user.inscricao
        except Inscricao.DoesNotExist:
            raise Http404

    def get_success_url(self):
        return reverse('cbvadmin:eventos_atividade_escolher')


class VisualizarPagamento(AdminMixin, TemplateView):
    template_name = 'eventos/pagamento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inscricao = self.request.user.inscricao
        prefs = global_preferences_registry.manager()
        if prefs['pagamento__paypal_ativo']:
            paypal_dict = {
                'currency_code': 'BRL',
                'business': prefs['pagamento__paypal_email'],
                'amount': inscricao.tipo.preco,
                'item_name': inscricao.tipo.nome,
                'invoice': inscricao.id,
                'notify_url': self.request.build_absolute_uri(
                    reverse('paypal-ipn')),
                'return': self.request.build_absolute_uri(
                    reverse('cbvadmin:pagar')),
                'cancel_return': self.request.build_absolute_uri(
                    reverse('cbvadmin:pagar')),
            }
            context['form'] = PayPalPaymentsForm(initial=paypal_dict)

        return context


class CheckoutException(Exception):
    pass


class InscricaoPagarPagSeguro(SingleObjectMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        self.object = self.get_object()
        if self.object.pagamento != Inscricao.Pagamento.Pago:
            prefs = global_preferences_registry.manager()
            api = PagSeguroApi(
                pagseguro_email=prefs['pagamento__pagseguro_email'],
                pagseguro_token=prefs['pagamento__pagseguro_token'],
                reference=str(self.object.pk)
            )
            api.add_item(PagSeguroItem(
                id='1',
                description=self.object.tipo.nome,
                amount=self.object.tipo.preco,
                quantity=1
            ))
            print(api.redirect_url)
            data = api.checkout()
            if data['success']:
                return data['redirect_url']
            messages.error(self.request,
                           'Erro PagSeguro: %s' % data['message'])
        return reverse('cbvadmin:pagar')
