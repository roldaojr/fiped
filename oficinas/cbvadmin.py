from django.urls import reverse
from menu import MenuItem
from dynamic_preferences.registries import global_preferences_registry
import cbvadmin
from comum.views import DetailView
from .forms import (
    OficinaSubmeterForm, OficinaChangeForm, OficinaInscricaoForm,
    SubmeterMesaRedondaForm, ChangeMesaRedondaForm, MesaRedondaInscricaoForm,
    SeminarioSubmeterForm, SeminarioChangeForm, SeminarioInscricaoForm)
from .models import Oficina, MesaRedonda, Seminario, Livro
from .views import (SubmeterAtividadeView, AvaliarAtividadeView,
                    InscricaoAtividadeView)


class AtividadeAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'situacao')
    filter_fields = ('nome', 'situacao')
    add_view_class = SubmeterAtividadeView
    detail_view_class = DetailView
    avaliar_view_class = AvaliarAtividadeView
    inscricao_view_class = InscricaoAtividadeView
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

    def pode_inscrever_se(self, request):
        return True

    def get_menu(self):
        submenu_label = self.model_class._meta.verbose_name_plural.title()
        perm_code = '%s.add_%s' % (self.model_class._meta.app_label,
                                   self.model_class._meta.model_name)
        menus = super().get_menu()
        menus[0].title = 'Avaliar'
        menus[0].submenu = submenu_label
        menus += [
            MenuItem('Submeter',
                     reverse(self.urls['add']),
                     weight=60, icon=self.menu_icon, submenu=submenu_label,
                     check=lambda r: r.user.has_perm(perm_code)),
            MenuItem('Inscrever-se',
                     reverse(self.urls['inscricao']),
                     weight=70, icon=self.menu_icon, submenu=submenu_label,
                     check=lambda r: self.pode_inscrever_se(r))
        ]
        return menus

    def max_inscricoes(self, request):
        return 0


@cbvadmin.register(Oficina)
class OficinaAdmin(AtividadeAdmin):
    inscricao_form_class = OficinaInscricaoForm
    limitar_vagas = True

    def pode_inscrever_se(self, request):
        prefs = global_preferences_registry.manager()
        return (prefs['oficinas__inscricao'] and
                hasattr(request.user, 'inscricao'))

    def get_form_class(self, request, obj=None):
        if obj:
            return OficinaChangeForm
        else:
            return OficinaSubmeterForm

    def max_inscriccoes(self):
        prefs = global_preferences_registry.manager()
        return prefs['oficinas__inscricao_max']


@cbvadmin.register(MesaRedonda)
class MesaRedondaAdmin(AtividadeAdmin):
    add_form_class = SubmeterMesaRedondaForm
    edit_form_class = ChangeMesaRedondaForm
    inscricao_form_class = MesaRedondaInscricaoForm

    def pode_inscrever_se(self, request):
        prefs = global_preferences_registry.manager()
        return (prefs['mesasredondas__inscricao'] and
                hasattr(request.user, 'inscricao'))

    def get_form_class(self, request, obj=None):
        if obj:
            return ChangeMesaRedondaForm
        else:
            return SubmeterMesaRedondaForm

    def max_inscriccoes(self):
        prefs = global_preferences_registry.manager()
        return prefs['mesasredondas__inscricao_max']


@cbvadmin.register(Seminario)
class SeminarioAdmin(AtividadeAdmin):
    inscricao_form_class = SeminarioInscricaoForm
    limitar_vagas = True

    def get_form_class(self, request, obj=None):
        if obj:
            return SeminarioChangeForm
        else:
            return SeminarioSubmeterForm

    def pode_inscrever_se(self, request):
        prefs = global_preferences_registry.manager()
        return (prefs['seminarios__inscricao'] and
                hasattr(request.user, 'inscricao'))

    def max_inscriccoes(self):
        prefs = global_preferences_registry.manager()
        return prefs['seminarios__inscricao_max']


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
