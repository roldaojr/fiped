from django.test import TestCase
from django.urls import reverse
from .factories import UsuarioFactory


class PreferencesTestCase(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory.create(
            perms=['dynamic_preferences.change_globalpreferencemodel'])
        self.client.force_login(self.usuario)

    def test_view_prefs(self):
        resp = self.client.get(reverse('dynamic_preferences:global'))
        self.assertEqual(resp.status_code, 200)
