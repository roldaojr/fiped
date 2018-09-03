from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from cbvadmin.views.edit import AddView, EditView
from eventos.models import Inscricao
from .models import Oficina
from .forms import (OficinaSubmeterForm, OficinaChangeForm,
                    OficinaInscricaoForm)


class SubmeterOficinaView(AddView):
    form_class = OficinaSubmeterForm
    default_template = 'oficinas/oficina_submeter.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ministrante = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AlterarOficinaView(EditView):
    form_class = OficinaChangeForm


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
