from django.contrib import admin
from eventos.admin import HorarioInline, EventoAdmin
from .models import Minicurso, Ministrante, Definicoes


@admin.register(Ministrante)
class MinistranteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'bio')
    search_fields = ('nome',)


@admin.register(Minicurso)
class MinicursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ministrante', 'local', 'vagas', 'vagas_reserva')
    exclude = ('tipo',)
    inlines = [HorarioInline]
    search_fields = ('nome',)


class MinicursoDefinicaoInline(admin.StackedInline):
    model = Definicoes

EventoAdmin.inlines = list(getattr(EventoAdmin, 'inlines', [])) + \
                      [MinicursoDefinicaoInline]
