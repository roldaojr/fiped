from django.conf.urls import url
from .views import programacao

app_name = 'eventos'

urlpatterns = [
    url(r'^programacao$', programacao, name='programacao'),
]
