from django import forms
from django.conf import settings
from django_select2.forms import ModelSelect2Widget
from comum.utils.file_upload import UploadMaxSizeMixin, humanbytes
from comum.forms import UsuarioSelectWidget, UsuariosSelectWidget
from comum.models import Usuario
from .models import Trabalho, AreaTema


class AreaTemaSelectWidget(ModelSelect2Widget):
    model = AreaTema
    search_fields = [
        'nome__icontains',
    ]


class AreaTemaForm(forms.ModelForm):
    class Meta:
        model = AreaTema
        exclude = []
        widgets = {
            'avaliadores': UsuariosSelectWidget,
        }


class TrabalhoChangeFormAdmin(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = '__all__'
        widgets = {
            'area_tema': AreaTemaSelectWidget,
            'avaliador': UsuarioSelectWidget
        }
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(
                settings.FILE_UPLOAD_MAX_SIZE)
        }


class TrabalhoChangeForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ('area_tema', 'carta_aceite')
        widgets = {
            'area_tema': AreaTemaSelectWidget,
        }
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(
                settings.FILE_UPLOAD_MAX_SIZE)
        }


class TrabalhoAddForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Trabalho
        exclude = ('observacoes', 'carta_aceite')
        widgets = {
            'area_tema': AreaTemaSelectWidget,
            'autor': UsuarioSelectWidget(attrs={'readonly': 'readonly'}),
            'coautor1': UsuarioSelectWidget,
            'coautor2': UsuarioSelectWidget,
            'coautor3': UsuarioSelectWidget
        }
        help_texts = {
            'coautor1': 'Necessário estar inscrito no evento',
            'coautor2': 'Necessário estar inscrito no evento',
            'coautor3': 'Necessário estar inscrito no evento',
            'arquivo': 'Tamanho maximo de %s' % humanbytes(
                settings.FILE_UPLOAD_MAX_SIZE)
        }


class TrabalhoReenviarForm(UploadMaxSizeMixin, forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ('arquivo',)
        help_texts = {
            'arquivo': 'Tamanho maximo de %s' % humanbytes(
                settings.FILE_UPLOAD_MAX_SIZE)
        }
