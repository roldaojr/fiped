import cbvadmin
from .models import Area, Poster, MostraTecnologica


@cbvadmin.register(Area)
class AreaAdmin(cbvadmin.ModelAdmin):
    list_display = ('nome',)
    menu_weight = 1


@cbvadmin.register(Poster)
class PosterAdmin(cbvadmin.ModelAdmin):
    list_display = ('titulo', 'nome_autor', 'area', 'aprovado')
    menu_weight = 2


@cbvadmin.register(MostraTecnologica)
class MostraTecnologicaAdmin(cbvadmin.ModelAdmin):
    list_display = ('titulo', 'nome_autor', 'area', 'aprovado')
    menu_weight = 3
