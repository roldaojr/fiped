from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import now
from django.contrib import messages
from dynamic_preferences.registries import global_preferences_registry
from cbvadmin.views.edit import AddView, EditView
from comum.views import BasicView
from cbvadmin.views.list import TableListView
from .forms import TrabalhoReenviarForm
from .models import Trabalho


class TrabalhoListView(TableListView):
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)

        if (user.is_authenticated and
                user.has_perm('trabalhos.change_areatema')):
            return qs

        if user.has_perm('trabalhos.change_trabalho'):
            return qs.filter(area_tema__avaliadores__id=user.pk)

        return qs.filter(
            Q(autor=user) | Q(coautor1=user) |
            Q(coautor2=user) | Q(coautor3=user)
        )


class SubmeterTrabalhoView(AddView):
    default_template = 'trabalhos/trabalho_submeter.html'

    def get_initial(self):
        return {'autor': self.request.user}

    def get_context_data(self, **kwargs):
        prefs = global_preferences_registry.manager()
        context = super().get_context_data(**kwargs)
        context.update({'pode_submeter': (
            prefs['trabalhos__prazo_submissao'] > now()
        )})
        return context


class AvaliarView(SingleObjectMixin, BasicView):
    def get(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        avaliacao = request.POST.get('situacao')
        observacoes = request.POST.get('observacoes')
        self.object.situacao = avaliacao
        self.object.observacoes = observacoes
        self.object.save()
        messages.success(request, 'Trabalho "%s" alterado avaliado' %
                         self.object.titulo)
        return HttpResponseRedirect(success_url)


class TrabalhoReenviarView(EditView):
    def get_form_class(self):
        return TrabalhoReenviarForm

    def form_valid(self, *args, **kwargs):
        self.object.situacao = Trabalho.Situacao.Reenviado
        return super().form_valid(*args, **kwargs)

    def get_success_url(self):
        return reverse(self.admin.urls['detail'], args=[self.object.pk])
