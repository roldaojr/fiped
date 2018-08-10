from django.urls import reverse
from menu import Menu, MenuItem


def usuario_autenticado(request):
    return lambda request: request.user.is_authenticated()


Menu.add_item("main", MenuItem("Trabalhos",
                               reverse("trabalhos:index"),
                               check=usuario_autenticado))
