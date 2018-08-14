from django.utils.timezone import now
from dynamic_preferences.types import DateTimePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

trabalhos = Section('trabalhos', verbose_name='Trabalhos')


@global_preferences_registry.register
class PrazoSubmissao(DateTimePreference):
    section = trabalhos
    name = 'prazo_submissao'
    verbose_name = 'Prazo para submissão de trabalhos'

    @property
    def default(self):
        return now()
