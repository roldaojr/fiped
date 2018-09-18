from django.db.models import F, Q, Count
from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper
from localflavor.br.forms import BRStateChoiceField
from comum.models import Usuario
from .models import Inscricao, TipoInscricao


class InscricaoForm(forms.ModelForm):
    possui_deficiencia = forms.BooleanField(
        label='Possui deficiência ou outra necessidade educacional',
        required=False)
    deficiencia = forms.CharField(
        label='Especifique', required=False, max_length=300)
    alojamento = forms.BooleanField(
        label='Durante o evento irá necessitar de alojamento estudantil',
        required=False)
    endereco = forms.CharField(label='Endereço', max_length=300)
    numero = forms.CharField(max_length=10)
    cidade = forms.CharField(max_length=50)
    uf = BRStateChoiceField(label='UF')
    titulacao = forms.CharField(label='Titulação', max_length=50)
    instituicao = forms.CharField(label='Filiação institucional',
                                  max_length=100)
    tipo = forms.ModelChoiceField(queryset=TipoInscricao.objects.all(),
                                  label='Categoria')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Confirmar senha')

    inscricao_fields = (
        'deficiencia', 'alojamento', 'endereco', 'numero', 'cidade', 'uf',
        'titulacao', 'instituicao', 'tipo')

    class Meta:
        model = Usuario
        fields = ('nome_completo', 'nome_social', 'cpf', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tipos = TipoInscricao.objects.annotate(
            Count('inscricoes')).filter(
                Q(limite=0) | Q(inscricoes__count__lt=F('limite')))
        self.fields['tipo'].queryset = tipos
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        tipo = cleaned_data['tipo']
        if tipo.limite > 0 and tipo.inscricoes.count() >= tipo.limite:
            raise ValidationError('Não há mais vagas para %s' % tipo.nome)
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError('A senha e a confirmção devem ser iguais')

    def save(self, *args, **kwargs):
        usuario = super().save(*args, **kwargs)
        usuario.set_password(self.cleaned_data['password1'])
        grupo, c = Group.objects.get_or_create(name='Participante')
        usuario.groups.add(grupo)
        usuario.save()
        inscricao_data = {
            f: self.cleaned_data[f] for f in self.inscricao_fields
        }
        inscricao = Inscricao(**inscricao_data)
        inscricao.usuario = usuario
        if self.cleaned_data['tipo'].validar:
            inscricao.validado = False
        else:
            inscricao.validado = True
        inscricao.save()
        return usuario


class EditarInscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        exclude = ('atividades',)
