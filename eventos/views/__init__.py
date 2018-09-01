from django_tables2.columns import Column
from cbvadmin.views.list import TableListView
from cbvadmin.tables import table_factory
from ..filters import InscricaoFilter


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
