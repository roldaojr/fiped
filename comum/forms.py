from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from localflavor.br.forms import BRCPFField
from .models import Usuario


class UsuarioPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_completo', 'cpf', 'email', 'instituicao', 'curso')


class UsuarioForm(UsuarioPerfilForm):
    cpf = BRCPFField(label='CPF', max_length=11)
    password = forms.CharField(
        label='Senha',
        help_text='Use pelo menos 6 caracteres.',
        widget=forms.PasswordInput(),
        min_length=6)

    confirm_password = forms.CharField(
        label='Confirmar senha',
        help_text='Use pelo menos 6 caracteres.',
        min_length=6,
        widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('nome_completo', 'cpf', 'email', 'instituicao', 'curso')


class AlterarUsuarioForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Senha')

    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AlterarUsuarioForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']
