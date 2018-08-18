from django import forms
from django.forms import ValidationError
from crispy_forms.helper import FormHelper
from comum.models import Usuario
from .models import Inscricao, TipoInscricao


class InscricaoForm(forms.ModelForm):
    possui_deficiencia = forms.BooleanField(
        label='Possui deficiência ou outra necessidade educacional',
        required=False)
    deficiencia = forms.CharField(label='Especifique', required=False)
    alojamento = forms.BooleanField(
        label='Durante o evento irá necessitar de alojamento estudantil',
        required=False)
    endereco = forms.CharField(label='Endereço')
    numero = forms.CharField()
    cidade = forms.CharField()
    uf = forms.CharField(label='UF')
    titulacao = forms.CharField(label='Titulação')
    instituicao = forms.CharField(label='Filiação institucional')
    tipo = forms.ModelChoiceField(queryset=TipoInscricao.objects.all(),
                                  label='Categoria')
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    inscricao_fields = (
        'deficiencia', 'alojamento', 'endereco', 'numero', 'cidade', 'uf',
        'titulacao', 'instituicao', 'tipo')

    class Meta:
        model = Usuario
        fields = ('nome_completo', 'nome_social', 'cpf', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if cleaned_data.get('senha') != cleaned_data.get('confirmar_senha'):
            raise ValidationError('A senha e a confirmção devem ser iguais')

    def save(self, *args, **kwargs):
        usuario = super().save(*args, **kwargs)
        usuario.set_password(self.cleaned_data['senha'])
        inscricao_data = {
            f: self.cleaned_data[f] for f in self.inscricao_fields
        }
        inscricao = Inscricao(**inscricao_data)
        inscricao.usuario = usuario
        inscricao.save()
        return usuario
