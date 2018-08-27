from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import now
from dynamic_preferences.registries import global_preferences_registry
from cbvadmin.views.edit import AddView
from comum.views import DetailView, BasicView
from cbvadmin.views.list import TableListView


class TrabalhoDetalhes(DetailView):
    pass


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

    def get_context_data(self, **kwargs):
        prefs = global_preferences_registry.manager()
        context = super().get_context_data(**kwargs)
        context.update({'pode_submeter': (
            prefs['trabalhos__prazo_submissao'] > now()
        )})
        return context


class AvaliarTrabalhoView(SingleObjectMixin, BasicView):
    def get(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        avaliacao = request.POST.get('situacao')
        self.object.situacao = avaliacao
        self.object.save()
        return HttpResponseRedirect(success_url)
