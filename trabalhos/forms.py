from django import forms
from django_select2.forms import ModelSelect2Widget
from comum.forms import UsuarioSelectWidget, UsuariosSelectWidget
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


class TrabalhoChangeForm(forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ('area_tema',)
        widgets = {
            'area_tema': AreaTemaSelectWidget,
        }


class TrabalhoAddForm(forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = '__all__'
        widgets = {
            'area_tema': AreaTemaSelectWidget,
            'autor': UsuarioSelectWidget,
            'coautor1': UsuarioSelectWidget,
            'coautor2': UsuarioSelectWidget,
            'coautor3': UsuarioSelectWidget
        }
