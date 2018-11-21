from dynamic_preferences.types import BooleanPreference, IntegerPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


oficinas = Section('oficinas', verbose_name='Oficinas')
mesasredondas = Section('mesasredondas', verbose_name='Mesas redondas')
semnarios = Section('seminarios', verbose_name='Semniários temáticos')


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


@global_preferences_registry.register
class InscricaoMesaRedondaAtivo(BooleanPreference):
    section = mesasredondas
    name = 'inscricao'
    verbose_name = 'Ativar inscrições mesas-redondas'
    default = False


@global_preferences_registry.register
class InscricaoMesaRedondaMax(IntegerPreference):
    section = mesasredondas
    name = 'inscricao_max'
    verbose_name = 'Número máximo de mesas-redondas por participante'
    default = 0


@global_preferences_registry.register
class InscricaoSeminarioAtivo(BooleanPreference):
    section = semnarios
    name = 'inscricao'
    verbose_name = 'Ativar inscrições semniários temáticos'
    default = False


@global_preferences_registry.register
class InscricaoSeminarioMax(IntegerPreference):
    section = semnarios
    name = 'inscricao_max'
    verbose_name = 'Número máximo de semniários temáticos por participante'
    default = 0
