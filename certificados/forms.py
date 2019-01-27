from django import forms
from tablib import Dataset
from eventos.models import Inscricao
from cbvadmin.forms import FormHelper
from .models import Certificado, ModeloCertificado


class CertificadoForm(forms.ModelForm):
    inscricao = forms.CharField()

    def clean_inscricao(self, *args, **kwargs):
        return Inscricao(id=self.cleaned_data['inscricao'])

    class Meta:
        model = Certificado
        fields = ('nome', 'atividade', 'tipo_atividade', 'modelo', 'inscricao')


class CertificadoImportarForm(forms.Form):
    arquivo = forms.FileField(required=True)
    modelo = forms.ModelChoiceField(
        required=True, queryset=ModeloCertificado.objects.all())

    helper = FormHelper()
    helper.form_tag = False

    def clean_arquivo(self):
        arquivo = self.cleaned_data['arquivo'].read().decode("utf-8")
        return Dataset().load(arquivo, format='csv')
