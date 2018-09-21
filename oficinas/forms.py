from django import forms
from django.forms import ValidationError
from dynamic_preferences.registries import global_preferences_registry
from eventos.models import Inscricao
from .models import Oficina, MesaRedonda


class OficinaSubmeterForm(forms.ModelForm):
    class Meta:
        model = Oficina
        exclude = ('local', 'tipo', 'ministrante', 'inscricoes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da oficina'


class OficinaChangeForm(forms.ModelForm):
    class Meta:
        model = Oficina
        exclude = ('tipo', 'ministrante', 'arquivo', 'inscricoes')

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


class SubmeterMesaRedondaForm(forms.ModelForm):
    class Meta:
        model = MesaRedonda
        exclude = ('local', 'tipo', 'ministrante', 'inscricoes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da mesa redonda'


class ChangeMesaRedondaForm(forms.ModelForm):
    class Meta:
        model = MesaRedonda
        exclude = ('tipo', 'ministrante', 'arquivo', 'inscricoes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Nome da mesa redonda'
