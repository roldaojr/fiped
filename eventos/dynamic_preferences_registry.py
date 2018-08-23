from django.utils.timezone import now
from dynamic_preferences.types import (
    BooleanPreference, IntegerPreference, StringPreference,
    DatePreference, FilePreference)
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


evento = Section('evento', verbose_name='Evento')
pagamento = Section('pagamento', verbose_name='Pagamento')


@global_preferences_registry.register
class NomeEvento(StringPreference):
    section = evento
    name = 'nome'
    verbose_name = 'Nome do evento'
    default = 'Eventus'


@global_preferences_registry.register
class LogoEvento(FilePreference):
    section = evento
    name = 'logo'
    verbose_name = 'Logotipo do evento'
    default = None


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


@global_preferences_registry.register
class DataInscricaoEvento(DatePreference):
    section = evento
    name = 'data_inscricao'
    verbose_name = 'Data de abertura das inscrições no evento'
    field_kwargs = {'required': False}

    @property
    def default(self):
        return now().date()


@global_preferences_registry.register
class InscricaoAtividadeMax(IntegerPreference):
    section = evento
    name = 'inscricao_atividade_max'
    verbose_name = 'Número máximo de atividades por participante'
    default = 1


@global_preferences_registry.register
class PaypalAtivo(BooleanPreference):
    section = pagamento
    name = 'paypal_ativo'
    verbose_name = 'Receber pagamento por PayPal'
    default = False


@global_preferences_registry.register
class PaypalEmail(StringPreference):
    section = pagamento
    name = 'paypal_email'
    verbose_name = 'E-mail da conta Paypal'
    default = ''
    field_kwargs = {'required': False}


@global_preferences_registry.register
class PagSeguroAtivo(BooleanPreference):
    section = pagamento
    name = 'pagseguro_ativo'
    verbose_name = 'Receber pagamentos por PagSeguro'
    default = False


@global_preferences_registry.register
class PagSeguroEmail(StringPreference):
    section = pagamento
    name = 'pagseguro_email'
    verbose_name = 'E-mail da conta PagSeguro'
    default = ''
    field_kwargs = {'required': False}


@global_preferences_registry.register
class PagSeguroToken(StringPreference):
    section = pagamento
    name = 'pagseguro_token'
    verbose_name = 'Token da conta PagSeguro'
    default = ''
    field_kwargs = {'required': False}
