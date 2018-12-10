from django import forms
from django.conf import settings
from django.forms import ValidationError
from comum.utils.file_upload import UploadMaxSizeMixin, humanbytes
from dynamic_preferences.registries import global_preferences_registry
from eventos.models import Inscricao
from .models import Oficina, MesaRedonda, Seminario


class OficinaSubmeterForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Oficina
        exclude = ('local', 'tipo', 'ministrante', 'inscricoes')
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(settings.FILE_UPLOAD_MAX_SIZE)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da oficina'


class OficinaChangeForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Oficina
        

class OficinaInscricaoForm(forms.ModelForm):
    atividades = forms.ModelMultipleChoiceField(
        queryset=Oficina.objects.filter(situacao=Oficina.Situacao.Aprovado),
        required=False)

    class Meta:
        model = Inscricao
        fields = ['atividades']

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            initial = kwargs.setdefault('initial', {})
            initial['atividades'] = instance.oficinas.values_list(
                'pk', flat=True)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        prefs = global_preferences_registry.manager()

        if ('atividades' in cleaned_data and
                len(cleaned_data['atividades']) >
                prefs['oficinas__inscricao_max']):
            raise ValidationError(
                'Você deve selecionar no máximo %d oficina(s)' %
                prefs['oficinas__inscricao_max'])
        return cleaned_data

    def save(self, *args, **kwargs):
        self.instance.oficinas.clear()
        for o in Oficina.objects.filter(
                pk__in=self.cleaned_data['atividades']):
            o.inscricoes.add(self.instance)


class SubmeterMesaRedondaForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = MesaRedonda
        exclude = ('local', 'tipo', 'ministrante', 'inscricoes')
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(settings.FILE_UPLOAD_MAX_SIZE)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da mesa redonda'


class ChangeMesaRedondaForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = MesaRedonda
        exclude = ('tipo', 'ministrante', 'arquivo', 'inscricoes')
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(settings.FILE_UPLOAD_MAX_SIZE)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da mesa redonda'


class MesaRedondaInscricaoForm(forms.ModelForm):
    atividades = forms.ModelMultipleChoiceField(
        queryset=MesaRedonda.objects.filter(
            situacao=MesaRedonda.Situacao.Aprovado), required=False)

    class Meta:
        model = Inscricao
        fields = ['atividades']

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            initial = kwargs.setdefault('initial', {})
            initial['atividades'] = instance.mesasredondas.values_list(
                'pk', flat=True)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.mesasredondas.clear()
        for o in MesaRedonda.objects.filter(
                pk__in=self.cleaned_data['atividades']):
            o.inscricoes.add(self.instance)


class SeminarioSubmeterForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Seminario
        exclude = ('local', 'tipo', 'ministrante', 'inscricoes')
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(settings.FILE_UPLOAD_MAX_SIZE)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome dó seminário temático'


class SeminarioChangeForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Seminario
        exclude = ('tipo', 'ministrante', 'arquivo', 'inscricoes')
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(settings.FILE_UPLOAD_MAX_SIZE)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da oficina'


class SeminarioInscricaoForm(forms.ModelForm):
    atividades = forms.ModelMultipleChoiceField(
        queryset=Seminario.objects.filter(
            situacao=Seminario.Situacao.Aprovado),
        required=False)

    class Meta:
        model = Inscricao
        fields = ['atividades']

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            initial = kwargs.setdefault('initial', {})
            initial['atividades'] = instance.seminarios.values_list(
                'pk', flat=True)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        prefs = global_preferences_registry.manager()

        if ('atividades' in cleaned_data and
                len(cleaned_data['atividades']) >
                prefs['seminarios__inscricao_max']):
            raise ValidationError(
                'Você deve selecionar no máximo %d seminários temáticos(s)' %
                prefs['seminarios__inscricao_max'])
        return cleaned_data

    def save(self, *args, **kwargs):
        self.instance.seminarios.clear()
        for o in Seminario.objects.filter(
                pk__in=self.cleaned_data['atividades']):
            o.inscricoes.add(self.instance)
