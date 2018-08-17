from django.urls import reverse
from menu import MenuItem
import cbvadmin
from .forms import TrabalhoChangeForm, TrabalhoAddForm, AreaTemaForm
from .models import Modalidade, AreaTema, Trabalho
from .views import (TrabalhoDetalhes, TrabalhoListView,
                    AvaliarTrabalhoView)


@cbvadmin.register(Modalidade)
class ModalidadeAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome',)
    menu_weight = 1


@cbvadmin.register(AreaTema)
class AreaTemaAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome',)
    form_class = AreaTemaForm
    menu_weight = 1


@cbvadmin.register(Trabalho)
class TrabalhoAdmin(cbvadmin.ModelAdmin):
    list_display = ('titulo', 'autor', 'area_tema', 'modalidade',
                    'situacao')
    filter_fields = ('modalidade', 'area_tema', 'situacao')
    list_view_class = TrabalhoListView
    detail_view_class = TrabalhoDetalhes
    avaliar_view_class = AvaliarTrabalhoView
    form_class = TrabalhoAddForm
    default_object_action = 'detail'
    menu_weight = 2

    def get_actions(self):
        actions = super().get_actions()
        actions.update({'detail': 'object', 'avaliar': 'object'})
        return actions

    def has_permission(self, request, action, obj=None):
        if action == 'avaliar':
            action = 'edit'
        return super().has_permission(request, action, obj)

    def get_form_class(self, request, obj=None, **kwargs):
        if obj and not request.user.is_superuser:
            return TrabalhoChangeForm
        return super().get_form_class(request, obj=None, **kwargs)

    def get_menu(self):
        menus = super().get_menu()
        menus.append(
            MenuItem('Submeter trabalho',
                     reverse(self.urls['add']),
                     weight=self.menu_weight + 1, icon=self.menu_icon,
                     check=lambda r: r.user.has_perm('trabalhos.add_trabalho'))
        )
        return menus
