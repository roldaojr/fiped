from django.shortcuts import redirect, Http404
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from cbvadmin.views.edit import AddView, EditView
from comum.views import BasicView
from eventos.models import Inscricao
from .forms import OficinaInscricaoForm


class SubmeterAtividadeView(AddView):
    default_template = 'oficinas/atividade_submeter.html'
    raise_exception = False

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ministrante = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class AvaliarAtividadeView(SingleObjectMixin, BasicView):
    def get(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        return redirect(success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        avaliacao = request.POST.get('situacao')
        self.object.situacao = avaliacao
        self.object.save()
        messages.success(request, 'Atividade "%s" avaliada' %
                         self.object.nome)
        return redirect(success_url)


class InscricaoOficinaView(EditView):
    form_class = OficinaInscricaoForm
    default_template = 'oficinas/oficina_inscricao.html'
    success_message = 'Inscrição na(s) oficina(s) salva'
    permission_required = []

    def get_object(self):
        try:
            return self.request.user.inscricao
        except Inscricao.DoesNotExist:
            raise Http404

    def get_success_url(self):
        return reverse(self.admin.urls['inscricao'])
