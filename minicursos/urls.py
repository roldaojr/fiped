from django.conf.urls import url
from .views import (minicurso_listar, minicurso_detalhes,
                    minicurso_inscricao)

app_name = 'minicursos'

urlpatterns = [
    url(r'^$', minicurso_listar, name='listar'),
    url(r'^detalhes/(\d+)$', minicurso_detalhes, name='detalhes'),
    url(r'^inscricao/(\d+)$', minicurso_inscricao, name='inscricao'),
]
