from django.db.models import F, Q, Count
from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper
from dynamic_preferences.registries import global_preferences_registry
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
        if cleaned_data.get('senha') != cleaned_data.get('confirmar_senha'):
            raise ValidationError('A senha e a confirmção devem ser iguais')

    def save(self, *args, **kwargs):
        usuario = super().save(*args, **kwargs)
        usuario.set_password(self.cleaned_data['senha'])
        grupo, c = Group.objects.get_or_create(name='Participante')
        usuario.groups.add(grupo)
        usuario.save()
        inscricao_data = {
            f: self.cleaned_data[f] for f in self.inscricao_fields
        }
        inscricao = Inscricao(**inscricao_data)
        inscricao.usuario = usuario
        inscricao.save()
        return usuario


class EscolherAtividadesForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ('atividades',)

    def clean(self):
        cleaned_data = super().clean()
        prefs = global_preferences_registry.manager()

        if (len(cleaned_data['atividades']) >
                prefs['evento__inscricao_atividade_max']):
            raise ValidationError(
                'Você deve selecionar no máximo %d atividade(s)' %
                prefs['evento__inscricao_atividade_max'])
        return cleaned_data
