from django.shortcuts import redirect
from django.forms import modelform_factory
from django.shortcuts import Http404, reverse
from django.views.generic.detail import SingleObjectMixin
from django_tables2.columns import Column
from extra_views.generic import GenericInlineFormSet
from attachments.models import Attachment
from cbvadmin.views.list import TableListView
from cbvadmin.tables import table_factory
from comum.views import EditWithInlinesView, BasicView
from ..models import Inscricao
from ..filters import InscricaoFilter


class ImprimirLista(TableListView):
    filterset_class = InscricaoFilter
    list_display = ('nome_completo', 'email', ' ')
    template_name_suffix = '_print_list'
    paginate_by = False

    def get_table_class(self):
        extra = {
            'nome_completo': Column(accessor='usuario.nome_completo'),
            'email': Column(accessor='usuario.email')
        }
        return table_factory(self.model, self.list_display, action=None,
                             extra=extra)


class AnexoInline(GenericInlineFormSet):
    model = Attachment
    fields = ['attachment_file']
    factory_kwargs = {'ct_field': 'content_type',
                      'fk_field': 'object_id', 'extra': 3}

    def get_form_class(self):
        form_class = modelform_factory(Attachment, exclude=[])
        form_class.Meta.labels = {'attachment_file': 'Anexo'}
        return form_class


class AnexarArquivoView(EditWithInlinesView):
    default_template = 'anexar_arquivos.html'
    model = Inscricao
    inlines = [AnexoInline]

    def get_object(self):
        if hasattr(self.request.user, 'inscricao'):
            return self.request.user.inscricao
        else:
            raise Http404

    def get_form_class(self, *args, **kwargs):
        return modelform_factory(Inscricao, fields=[])

    def get_success_url(self):
        return reverse('cbvadmin:minha_inscricao')

    def forms_valid(self, form, inlines):
        self.object = form.save()
        for formset in inlines:
            object_list = formset.save(commit=False)
            for obj in object_list:
                obj.creator = self.request.user
                obj.save()
            for form in formset.deleted_forms:
                form.instance.delete()
        return redirect(self.get_success_url())


class ValidarInscricaoView(SingleObjectMixin, BasicView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.validado = bool(request.GET.get('validado'))
        self.object.save()
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(self.admin.urls['detail'], args=[self.kwargs['pk']])
