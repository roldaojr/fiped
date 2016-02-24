from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Usuario
from .forms import AlterarUsuarioForm


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'cpf')
    list_display_links = ('nome_completo', 'email')
    ordering = ('nome_completo',)
    search_fields = ('nome_completo', 'email', 'cpf')
    exclude = ('password', 'last_login')
    #form = AlterarUsuarioForm

admin.site.unregister(Group)