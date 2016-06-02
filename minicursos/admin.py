# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
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
    actions = ('lista_de_presenca',)

    def lista_de_presenca(self, request, queryset):
        return render(request, 'minicursos/lista_de_inscritos.html',
                      {'minicursos': queryset})
    lista_de_presenca.short_description = 'Lista de presença'

class MinicursoDefinicaoInline(admin.StackedInline):
    model = Definicoes

EventoAdmin.inlines = list(getattr(EventoAdmin, 'inlines', [])) + \
                      [MinicursoDefinicaoInline]
