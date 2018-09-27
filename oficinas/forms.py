from django import forms
from django.conf import settings
from django.forms import ValidationError
from comum.utils.file_upload import UploadMaxSizeMixin, humanbytes
from dynamic_preferences.registries import global_preferences_registry
from eventos.models import Inscricao
from .models import Oficina, MesaRedonda


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
        exclude = ('tipo', 'ministrante', 'arquivo', 'inscricoes')
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(settings.FILE_UPLOAD_MAX_SIZE)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da oficina'


class OficinaInscricaoForm(forms.ModelForm):
    oficinas = forms.ModelMultipleChoiceField(
        queryset=Oficina.objects.filter(situacao=Oficina.Situacao.Aprovado),
        required=False)

    class Meta:
        model = Inscricao
        fields = ['oficinas']

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            initial = kwargs.setdefault('initial', {})
            initial['oficinas'] = instance.oficinas.values_list(
                'pk', flat=True)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        prefs = global_preferences_registry.manager()

        if ('oficinas' in cleaned_data and
                len(cleaned_data['oficinas']) >
                prefs['oficinas__inscricao_max']):
            raise ValidationError(
                'Você deve selecionar no máximo %d oficina(s)' %
                prefs['oficinas__inscricao_max'])
        return cleaned_data

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        instance.oficinas.clear()
        for o in Oficina.objects.filter(pk__in=self.cleaned_data['oficinas']):
            o.inscricoes.add(instance)


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
