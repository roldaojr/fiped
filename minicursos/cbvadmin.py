import cbvadmin
from .models import Minicurso, Ministrante


@cbvadmin.register(Minicurso)
class MinicursoAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome', 'local', 'ministrante', 'vagas', 'inscritos')
    menu_weight = 1


@cbvadmin.register(Ministrante)
class MinistranteAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome',)
    menu_weight = 2
