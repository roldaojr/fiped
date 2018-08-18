from django.utils.translation import ugettext_lazy as _
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import DetailView as _DetailView
from django.views.generic import View
from cbvadmin.views.mixins import (
    FormMixin, AdminMixin, PermissionRequiredMixin, SuccessMixin)
from cbvadmin.views.dashboard import Dashboard as DashboardView
from eventos.models import Inscricao
from trabalhos.models import Trabalho, AreaTema


class BasicView(PermissionRequiredMixin, AdminMixin, SuccessMixin, View):
    model = None


class DetailView(PermissionRequiredMixin, AdminMixin, _DetailView):
    pass


class AddWithInlinesView(PermissionRequiredMixin, AdminMixin, FormMixin,
                         CreateWithInlinesView):
    default_template = 'change_form.html'
    success_message = _('The {name} \"{obj}\" was changed successfully.')


class EditWithInlinesView(PermissionRequiredMixin, AdminMixin, FormMixin,
                          UpdateWithInlinesView):
    default_template = 'change_form.html'
    success_message = _('The {name} \"{obj}\" was changed successfully.')


class Dashboard(DashboardView):
    def trabalhos_counters(self, user=None):
        if user:
            trabalhos = Trabalho.objects.filter(
                area_tematica__avaliadores__in=[user])
        else:
            trabalhos = Trabalho.objects.all()

        return [
            {
                'name': 'Trabalhos submetidos',
                'value': trabalhos.count()
            },
            {
                'name': 'Trabalhos avaliados',
                'value': trabalhos.exclude(
                        situacao=Trabalho.Situacao.Pendente).count()
            },
            {
                'name': 'Trabalhos aprovados',
                'value': trabalhos.filter(
                    situacao=Trabalho.Situacao.Aprovado).count(),
            }
        ]

    def organizador_counters(self):
        return [
            {
                'name': 'Inscrições',
                'value': Inscricao.objects.count(),
            },
            {
                'name': 'Avaliadores',
                'value': AreaTema.objects.values(
                    'avaliadores').distinct().count()
            },
        ]

    def get_context_data(self, *args, **kwargs):
        context = {'counters': []}
        user = self.request.user

        if user.has_perm('trabalhos.change_trabalho'):
            if user.has_perm('trabalhos.edit_area_tema'):
                context['counters'] += self.trabalhos_counters()
            else:
                context['counters'] += self.trabalhos_counters(user)

        if user.has_perm('trabalhos.view_inscricao'):
                context['counters'] += self.organizador_counters()

        return context
