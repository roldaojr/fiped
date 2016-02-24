# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Evento, Inscricao, Atividade, Horario


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicial', 'data_final')
    ordering = ('nome',)

    def has_add_permission(self, *args, **kwargs):
        return Evento.objects.count() == 0


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'atividade', 'espera')
    ordering = ('atividade', 'usuario', 'espera')
    list_filter = ('atividade', 'espera')
    search_fields = ('atividade__nome', 'usuario__nome')

    def has_add_permission(self, *args, **kwargs):
        return False


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'local')
    list_filter = ('tipo',)
    inlines = [HorarioInline]
    ordering = ('nome',)
    search_fields = ('nome',)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('atividade', 'data', 'hora_inicial', 'hora_final')
    list_display_links = []
    list_filter = ('atividade__tipo',)

    def has_change_permission(self, request, obj=None, *args, **kwargs):
        if obj is None:
            return True
        else:
            return False
    
    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
