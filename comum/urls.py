from django.conf.urls import include, url
from django.contrib.auth  import views as auth
from .views import (usuario_perfil, usuario_registrar,
                    alterar_senha_concluido, home)

urlpatterns = [
    url(r'^usuario/', include([
            url(r'^login/$', auth.login, name='login'),
            url(r'^logout/$', auth.logout_then_login, name='logout'),
            url(r'^alterar_senha/$', auth.password_change, name='password_change',
                kwargs={'template_name':'comum/usuario/alterar_senha_form.html'}),
            url(r'^alterar_senha/feito/$', alterar_senha_concluido, name='password_change_done'),
            url(r'^redefinir_senha/$', auth.password_reset, name='password_reset'),
            url(r'^redefinir_senha/feito/$', auth.password_reset_done, name='password_reset_done'),
            url(r'^redefinir/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                auth.password_reset_confirm, name='password_reset_confirm'),
            url(r'^redefinir/feito/$', auth.password_reset_complete, name='password_reset_complete'),

            url(r'^perfil$', usuario_perfil, name='usuario_perfil'),
            url(r'^registrar$', usuario_registrar, name='usuario_registrar')
        ])),
    url(r'^$', home, name='home')
]
