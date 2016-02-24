from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Trabalhos",
                               reverse("trabalhos:index"),
                               check=lambda request: request.user.is_authenticated()))
