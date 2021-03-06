from django.conf import settings
from django.conf.urls import url
from django.urls import include
from django.views.static import serve
from comum.views import InscreverView
from eventos.views.pagamento import pagseguro_notification
import cbvadmin


urlpatterns = [
    url(r'^admin/', cbvadmin.site.urls),
    url(r'^accounts/register/$', InscreverView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^preferences/', include('dynamic_preferences.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^attachments/', include('attachments.urls',
                                  namespace='attachments')),
    url(r'^pagamento/paypal/', include('paypal.standard.ipn.urls')),
    url(r'^pagamento/pagseguro/', pagseguro_notification),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            serve, {'document_root': settings.MEDIA_ROOT})
    ]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
