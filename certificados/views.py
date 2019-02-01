from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.template import Context, Template
from django.views.generic.edit import FormView
from django.forms.models import model_to_dict
from django.conf import settings
from import_export.results import RowResult
from trml2pdf import parseString
from cbvadmin.views.list import ListView
from cbvadmin.views.mixins import FormMixin, AdminMixin
from cbvadmin.tables import table_factory
from comum.views import DetailView
from .forms import CertificadoImportarForm
from .resources import CertificadoResource


class CertificadosListView(ListView):
    default_template = 'certificados/list.html'


class MeusCertificadosListView(ListView):
    def check_permissions(self, request):
        return True

    def get_table_class(self):
        return table_factory(
            self.model, ('atividade', 'tipo_atividade'), action='imprimir')

    def get_filter_fields(self):
        return None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(inscricao__usuario=self.request.user)


class CertificadoImprimirView(DetailView):
    def check_permissions(self, request):
        return True

    def get_template_names(self):
        return ['certificados/modelos/base.rml']

    def get_context_data(self, **kwargs):
        tpl = Template(self.object.modelo.conteudo)
        conteudo = tpl.render(Context(model_to_dict(self.object)))
        return {
            'modelo': self.object.modelo,
            'conteudo': conteudo,
            'MEDIA_ROOT': settings.MEDIA_ROOT,
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        if settings.DEBUG and request.GET.get('xml', ''):
            return response
        else:
            pdfData = parseString(response.rendered_content)
            return HttpResponse(pdfData, content_type='application/pdf')


class CertificadoImportarView(AdminMixin, FormMixin, FormView):
    model = None
    template_name = 'certificados/importar.html'
    permission_required = 'certificados.add_certificado'

    def get_form_class(self):
        return CertificadoImportarForm

    def form_valid(self, form):
        dataset = form.cleaned_data['arquivo']
        resource = CertificadoResource(form.cleaned_data['modelo'])
        result = resource.import_data(dataset)
        self.totals = result.totals
        for row_num, row in enumerate(result.rows):
            if row.import_type != RowResult.IMPORT_TYPE_SKIP:
                continue
            error = 'Linha %d: %s' % (row_num + 1, row.diff[-1])
            messages.info(self.request, error)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return 'Registros importados: ' \
            '%(new)d novos, %(skip)d ignorados ' \
            '%(invalid)s inválidos' % self.totals

    def get_success_url(self):
        return reverse(self.admin.urls['importar'])
