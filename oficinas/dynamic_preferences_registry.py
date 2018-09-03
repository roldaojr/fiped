from dynamic_preferences.types import BooleanPreference, IntegerPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


oficinas = Section('oficinas', verbose_name='Oficinas')


@global_preferences_registry.register
class InscricaoAtividadeAtivo(BooleanPreference):
    section = oficinas
    name = 'inscricao'
    verbose_name = 'Ativar inscrições em oficinas'
    default = False


@global_preferences_registry.register
class InscricaoAtividadeMax(IntegerPreference):
    section = oficinas
    name = 'inscricao_max'
    verbose_name = 'Número máximo de oficinas por participante'
    default = 1
