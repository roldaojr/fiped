import six
from django.urls import reverse
from django.conf.urls import url
from django_tables2.columns import TemplateColumn
from menu import MenuItem
import cbvadmin
from cbvadmin.tables import table_factory
from .views import (CertificadosListView, CertificadoImprimirView,
                    MeusCertificadosListView, CertificadoImportarView)
from .forms import CertificadoForm
from .models import ModeloCertificado, Certificado


@cbvadmin.register(ModeloCertificado)
class ModeloCertificadoAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome',)


@cbvadmin.register(Certificado)
class CertificadoAdmin(cbvadmin.ModelAdmin):
    default_object_action = 'imprimir'
    list_display = ('nome', 'tipo_atividade', 'atividade')
    filter_fields = ('nome', 'tipo_atividade', 'atividade')
    form_class = CertificadoForm
    list_view_class = CertificadosListView
    meus_view_class = MeusCertificadosListView
    imprimir_view_class = CertificadoImprimirView
    importar_view_class = CertificadoImportarView

    def get_table_class(self):
        extra = {'Imprimir': TemplateColumn(
            template_name='certificados/tables_actions.html')}
        return table_factory(self.model_class, self.list_display,
                             action='edit', extra=extra)

    def get_actions(self):
        actions = super().get_actions()
        actions.update({
            'imprimir': 'object',
            'meus': 'collection',
            'importar': 'collection'
        })
        return actions

    def get_menu(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        code = '%s.edit_%s' % (app, model)
        return [
            MenuItem('Gerenciar',
                     reverse(self.urls['default']),
                     weight=self.menu_weight),
            MenuItem('Meus Certificados',
                     reverse(self.urls['meus']),
                     check=lambda request: request.user.has_perm(code),
                     weight=self.menu_weight + 1)
        ]

    def get_urls(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        urls = []
        # get valid actions
        actions = self.get_actions()

        for action, target in six.iteritems(actions):
            if action == self.default_action:
                pattern = r'^$'
            elif action == self.default_object_action:
                pattern = r'^(?P<pk>\w+)/$'
            elif target == 'object':
                pattern = r'^(?P<pk>\w+)/%s$' % action
            else:
                pattern = r'^%s$' % action

            view_class = self.get_view_class(action)
            view_kwargs = self.get_view_kwargs(action)
            view_kwargs.update({
                'model': self.model_class,
                'action': action,
                'admin': self,
            })
            urls.append(url(pattern, view_class.as_view(**view_kwargs),
                            name='%s_%s_%s' % (app, model, action)))
        return urls
