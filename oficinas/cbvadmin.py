from django.urls import reverse
from menu import MenuItem
from dynamic_preferences.registries import global_preferences_registry
import cbvadmin
from comum.views import DetailView
from trabalhos.views import AvaliarView
from .models import Oficina
from .views import (SubmeterOficinaView, AlterarOficinaView,
                    InscricaoOficinaView)


@cbvadmin.register(Oficina)
class OficinaAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'situacao')
    filter_fields = ('nome', 'situacao')
    add_view_class = SubmeterOficinaView
    edit_view_class = AlterarOficinaView
    detail_view_class = DetailView
    avaliar_view_class = AvaliarView
    inscricao_view_class = InscricaoOficinaView
    default_object_action = 'detail'

    def get_actions(self):
        actions = super().get_actions()
        actions.update({'detail': 'object',
                        'avaliar': 'object',
                        'inscricao': 'collection'})
        return actions

    def has_permission(self, request, action, obj=None):
        if action == 'inscricao':
            return True
        if action == 'avaliar':
            action = 'edit'
        return super().has_permission(request, action, obj)

    def get_success_url(self, view=None):
        if not self.has_permission(view.request, self.default_action):
            return reverse('cbvadmin:dashboard')
        return super().get_success_url(view)

    def get_menu(self):
        def pode_inscrever_se(request):
            prefs = global_preferences_registry.manager()
            return (prefs['oficinas__inscricao'] and
                    hasattr(request.user, 'inscricao'))

        menus = super().get_menu()
        menus[0].title = 'Avaliar'
        menus += [
            MenuItem('Submeter',
                     reverse(self.urls['add']),
                     weight=60, icon=self.menu_icon, submenu='Oficinas',
                     check=lambda r: r.user.has_perm('oficinas.add_oficina')),
            MenuItem('Inscrever-se',
                     reverse(self.urls['inscricao']),
                     weight=70, icon=self.menu_icon, submenu='Oficinas',
                     check=lambda r: pode_inscrever_se(r))
        ]
        return menus
