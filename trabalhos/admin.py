from django.contrib import admin
from eventos.admin import EventoAdmin
from .models import Area, Poster, MostraTecnologica, Definicoes


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering = ('nome',)


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'area', 'nome_autor', 'aprovado')
    ordering = ('area', 'titulo')
    list_filter = ('area',)
    search_fields = ('titulo', 'nome_autor')

    def has_add_permission(self, *args, **kwargs):
        return False


@admin.register(MostraTecnologica)
class MostraTecnologicaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'area', 'nome_autor', 'aprovado')
    ordering = ('area', 'titulo')
    list_filter = ('area',)
    search_fields = ('titulo', 'nome_autor')

    def has_add_permission(self, *args, **kwargs):
        return False


class EventoConfigInline(admin.StackedInline):
    model = Definicoes


EventoAdmin.inlines = list(getattr(EventoAdmin, 'inlines', [])) + [EventoConfigInline]
