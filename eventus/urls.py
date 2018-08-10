from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
import cbvadmin

urlpatterns = [
    url(r'^admin2/', cbvadmin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^trabalhos/', include('trabalhos.urls', namespace='trabalhos')),
    url(r'^minicursos/', include('minicursos.urls', namespace='minicursos')),
    url(r'^eventos/', include('eventos.urls')),
    url(r'', include('comum.urls')),
]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
