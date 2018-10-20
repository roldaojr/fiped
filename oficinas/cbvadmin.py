from django.urls import reverse
from menu import MenuItem
from dynamic_preferences.registries import global_preferences_registry
import cbvadmin
from comum.views import DetailView
from .forms import (OficinaSubmeterForm, OficinaChangeForm,
                    SubmeterMesaRedondaForm, ChangeMesaRedondaForm)
from .models import Oficina, MesaRedonda, Livro
from .views import (SubmeterAtividadeView, AvaliarAtividadeView,
                    InscricaoOficinaView)


@cbvadmin.register(Oficina)
class OficinaAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'situacao')
    filter_fields = ('nome', 'situacao')
    add_view_class = SubmeterAtividadeView
    detail_view_class = DetailView
    avaliar_view_class = AvaliarAtividadeView
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

    def get_view_kwargs(self, action):
        view_kwargs = super().get_view_kwargs(action)
        if action == 'add':
            view_kwargs['form_class'] = OficinaSubmeterForm
        elif action == 'change':
            view_kwargs['form_class'] = OficinaChangeForm
        return view_kwargs

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


@cbvadmin.register(MesaRedonda)
class MesaRedondaAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'situacao')
    filter_fields = ('nome', 'situacao')
    add_view_class = SubmeterAtividadeView
    detail_view_class = DetailView
    avaliar_view_class = AvaliarAtividadeView
    default_object_action = 'detail'

    def get_actions(self):
        actions = super().get_actions()
        actions.update({'detail': 'object',
                        'avaliar': 'object'})
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

    def get_form_class(self, request, obj=None):
        if obj:
            return ChangeMesaRedondaForm
        else:
            return SubmeterMesaRedondaForm

    def get_menu(self):
        menus = super().get_menu()
        menus[0].title = 'Avaliar'
        menus[0].submenu = 'Mesas-redondas'
        menus += [
            MenuItem('Submeter',
                     reverse(self.urls['add']),
                     weight=60, icon=self.menu_icon, submenu='Mesas-redondas',
                     check=lambda r: r.user.has_perm('oficinas.add_mesaredonda')),
        ]
        return menus


@cbvadmin.register(Livro)
class LivroAdmin(cbvadmin.ModelAdmin):
    list_display = ('titulo', 'nome', 'situacao')
    filter_fields = ('titulo', 'nome', 'situacao')
    detail_view_class = DetailView
    avaliar_view_class = AvaliarAtividadeView
    default_object_action = 'detail'

    def get_actions(self):
        actions = super().get_actions()
        actions.update({'detail': 'object',
                        'avaliar': 'object'})
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
        menus = super().get_menu()
        menus[0].title = 'Avaliar'
        menus[0].submenu = 'Livros'
        menus += [
            MenuItem('Submeter',
                     reverse(self.urls['add']),
                     weight=60, icon=self.menu_icon, submenu='Livros',
                     check=lambda r: r.user.has_perm('oficinas.add_livro')),
        ]
        return menus
