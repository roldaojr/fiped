from django.conf.urls import include, url
from .views import programacao

urlpatterns = [
    url(r'^programacao$', programacao, name='programacao'),
]
