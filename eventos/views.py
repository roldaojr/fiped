from django.urls import reverse
from django.http import Http404
from django_tables2.columns import Column
from cbvadmin.views.list import TableListView
from cbvadmin.views.edit import EditView
from cbvadmin.tables import table_factory
from .filters import InscricaoFilter
from .forms import EscolherAtividadesForm
from .models import Inscricao


class ImprimirLista(TableListView):
    filterset_class = InscricaoFilter
    list_display = ('nome_completo', 'nome_social', 'cpf', 'email',
                    'tipo', 'alojamento', 'deficiencia')
    template_name_suffix = '_print_list'
    paginate_by = False

    def get_table_class(self):
        extra = {
            'nome_completo': Column(accessor='usuario.nome_completo'),
            'nome_social': Column(accessor='usuario.nome_social'),
            'cpf': Column(accessor='usuario.cpf'),
            'email': Column(accessor='usuario.email')
        }
        return table_factory(self.model, self.list_display, action=None,
                             extra=extra)


class EscolherAtividade(EditView):
    form_class = EscolherAtividadesForm
    default_template = 'eventos/atividade_escolher.html'

    def get_object(self):
        try:
            return self.request.user.inscricao
        except Inscricao.DoesNotExist:
            raise Http404

    def get_success_url(self):
        return reverse('cbvadmin:eventos_atividade_escolher')
