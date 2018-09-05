from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import TemplateView
from paypal.standard.forms import PayPalPaymentsForm
from pagseguro.api import PagSeguroItem, PagSeguroApi
from dynamic_preferences.registries import global_preferences_registry
from cbvadmin.views.mixins import AdminMixin
from ..models import Inscricao


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
                'item_name': inscricao.valor,
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
                amount=self.object.valor,
                quantity=1
            ))
            data = api.checkout()
            if data['success']:
                return data['redirect_url']
            messages.error(self.request,
                           'Erro PagSeguro: %s' % data['message'])
        return reverse('cbvadmin:pagar')


@csrf_exempt
@require_http_methods(['POST'])
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    notification_type = request.POST.get('notificationType', None)

    if notification_code and notification_type == 'transaction':
        prefs = global_preferences_registry.manager()
        pagseguro_api = PagSeguroApi(
            pagseguro_email=prefs['pagamento__pagseguro_email'],
            pagseguro_token=prefs['pagamento__pagseguro_token'])
        response = pagseguro_api.get_notification(notification_code)

        if response.status_code == 200:
            return HttpResponse('Notificação recebida com sucesso.')

    return HttpResponse('Notificação inválida.', status=400)
