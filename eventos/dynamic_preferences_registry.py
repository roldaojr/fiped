from django.utils.timezone import now
from dynamic_preferences.types import StringPreference, DatePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


evento = Section('evento', verbose_name='Evento')


@global_preferences_registry.register
class NomeEvento(StringPreference):
    section = evento
    name = 'nome'
    verbose_name = 'Nome do evento'
    default = 'Eventus'


@global_preferences_registry.register
class InicioEvento(DatePreference):
    section = evento
    name = 'data_inicio'
    verbose_name = 'Data de início do evento'

    @property
    def default(self):
        return now().date()


@global_preferences_registry.register
class FimEvento(DatePreference):
    section = evento
    name = 'data_fim'
    verbose_name = 'Data de termino do evento'

    @property
    def default(self):
        return now().date()
