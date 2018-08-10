from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Programação",
                               reverse("eventos:programacao")))
