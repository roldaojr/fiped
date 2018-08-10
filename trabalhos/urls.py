# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import submeter, submeter_poster, submeter_mostra

app_name = 'trabalhos'

urlpatterns = [
    url(r'^$', submeter, name='index'),
    url(r'^submeter/poster/$', submeter_poster, name='submeter_poster'),
    url(r'^submeter/mostra/$', submeter_mostra, name='submeter_mostra'),
]
