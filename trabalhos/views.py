from django.db.models import Q
from extra_views import InlineFormSet
from crispy_forms.helper import FormHelper
from comum.views import DetailView, AddWithInlinesView, EditWithInlinesView
from cbvadmin.views.list import TableListView
from .models import Avaliador_AreaTema


class TrabalhoDetalhes(DetailView):
    pass


class TrabalhoListView(TableListView):
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)

        if (user.is_authenticated and user.is_superuser):
            return qs

        if user.has_perm('trabalhos.change_trabalho'):
            return qs.filter(area_tema__avaliadores__id=user.pk)

        return qs.filter(
            Q(autor=user) | Q(coautor1=user) |
            Q(coautor2=user) | Q(coautor3=user)
        )


class Avaliador_AreaTemaesInline(InlineFormSet):
    model = Avaliador_AreaTema
    fields = ['usuario']
    factory_kwargs = {'extra': 1}


class AreaTemaAdd(AddWithInlinesView):
    inlines = [Avaliador_AreaTemaesInline]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        helper = FormHelper()
        helper.form_tag = False
        context.update({'formhelper': helper})
        return context


class AreaTemaEdit(EditWithInlinesView):
    inlines = [Avaliador_AreaTemaesInline]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        helper = FormHelper()
        helper.form_tag = False
        context.update({'formhelper': helper})
        return context
