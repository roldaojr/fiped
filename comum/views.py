from django.shortcuts import Http404
from django.urls import reverse
from django.db.models import Q
from datetime import date
from django.utils.translation import ugettext_lazy as _
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import DetailView as _DetailView
from django.views.generic import View
from registration.backends.simple.views import RegistrationView
from dynamic_preferences.registries import global_preferences_registry
from cbvadmin.views.mixins import (
    FormMixin, AdminMixin, PermissionRequiredMixin, SuccessMixin)
from cbvadmin.views.dashboard import Dashboard as DashboardView
from eventos.models import Inscricao
from trabalhos.models import Trabalho, AreaTema
from oficinas.models import Oficina, MesaRedonda, Seminario


class BasicView(PermissionRequiredMixin, AdminMixin, SuccessMixin, View):
    model = None


class DetailView(PermissionRequiredMixin, AdminMixin, _DetailView):
    pass


class InscreverView(RegistrationView):
    def registration_allowed(self):
        prefs = global_preferences_registry.manager()
        if date.today() > prefs['evento__data_fim'] or \
                date.today() < prefs['evento__data_inscricao']:
            return False
        else:
            return True

    def get_success_url(self, *args, **kwargs):
        return reverse('cbvadmin:dashboard')


class AddWithInlinesView(PermissionRequiredMixin, AdminMixin, FormMixin,
                         CreateWithInlinesView):
    default_template = 'change_form.html'
    success_message = _('The {name} \"{obj}\" was changed successfully.')


class EditWithInlinesView(PermissionRequiredMixin, AdminMixin, FormMixin,
                          UpdateWithInlinesView):
    default_template = 'change_form.html'
    success_message = _('The {name} \"{obj}\" was changed successfully.')


class MinhaInscricao(DetailView):
    template_name = 'comum/minha_inscricao.html'
    model = Inscricao

    def get_object(self):
        if hasattr(self.request.user, 'inscricao'):
            return self.request.user.inscricao
        else:
            raise Http404


class Dashboard(DashboardView):
    def trabalhos_counters(self, user=None):
        if user:
            trabalhos = Trabalho.objects.filter(
                area_tema__avaliadores__in=[user])
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

    def oficinas_counters(self):
        return [
            {
                'name': 'Oficinas submetidas',
                'value': Oficina.objects.count()
            },
            {
                'name': 'Oficinas aprovadas',
                'value': Oficina.objects.filter(
                    situacao=Oficina.Situacao.Aprovado).count()
            },
            {
                'name': 'Mesas redondas submetidas',
                'value': MesaRedonda.objects.count()
            },
            {
                'name': 'MMesa redondas aprovadas',
                'value': MesaRedonda.objects.filter(
                    situacao=MesaRedonda.Situacao.Aprovado).count()
            },
            {
                'name': 'Seminarios submetidos',
                'value': Seminario.objects.count()
            },
            {
                'name': 'Seminarios aprovados',
                'value': Seminario.objects.filter(
                    situacao=Seminario.Situacao.Aprovado).count()
            },
        ]

    def participante_trabalhos(self):
        user = self.request.user
        trabalhos = Trabalho.objects.filter(
            Q(autor=user) | Q(coautor1=user) |
            Q(coautor2=user) | Q(coautor3=user))
        return trabalhos

    def get_context_data(self, *args, **kwargs):
        context = {
            'trabalhos': self.participante_trabalhos(),
            'counters': [],
            'trabalhos_counters': []
        }
        user = self.request.user

        if user.has_perm('trabalhos.change_trabalho'):
            if user.has_perm('trabalhos.change_areatema'):
                context['trabalhos_counters'] += self.trabalhos_counters()
            else:
                context['trabalhos_counters'] += self.trabalhos_counters(user)

        if user.has_perm('oficinas.view_oficina'):
            context['counters'] += self.oficinas_counters()

        if user.has_perm('eventos.view_inscricao'):
            context['counters'] += self.organizador_counters()

        return context
