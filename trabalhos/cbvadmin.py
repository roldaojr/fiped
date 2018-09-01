from django.urls import reverse
from menu import MenuItem
import cbvadmin
from comum.views import DetailView
from .forms import TrabalhoChangeForm, TrabalhoAddForm, AreaTemaForm
from .models import Modalidade, AreaTema, Trabalho
from .views import TrabalhoListView, SubmeterTrabalhoView, AvaliarView


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
    filter_fields = ('titulo', 'modalidade', 'area_tema', 'situacao')
    list_view_class = TrabalhoListView
    add_view_class = SubmeterTrabalhoView
    detail_view_class = DetailView
    avaliar_view_class = AvaliarView
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

    def get_success_url(self, view=None):
        if not self.has_permission(view.request, self.default_action):
            return reverse('cbvadmin:dashboard')
        return super().get_success_url(view)

    def get_menu(self):
        menus = super().get_menu()
        menus[0].title = 'Avaliar trabalhos'
        menus.append(
            MenuItem('Submeter trabalho',
                     reverse(self.urls['add']),
                     weight=3, icon=self.menu_icon, submenu=False,
                     check=lambda r: r.user.has_perm('trabalhos.add_trabalho'))
        )
        return menus
