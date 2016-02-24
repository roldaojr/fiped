from django.conf.urls import include, url
from .views import (minicurso_listar, minicurso_detalhes,
                    minicurso_inscricao)

urlpatterns = [
    url(r'^$', minicurso_listar, name='listar'),
    url(r'^detalhes/(\d+)$', minicurso_detalhes, name='detalhes'),
    url(r'^inscricao/(\d+)$', minicurso_inscricao, name='inscricao'),
]
