from django import forms
from django.contrib.auth.models import Group
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from .models import Usuario


class UsuarioSelectWidget(ModelSelect2Widget):
    model = Usuario
    search_fields = [
        'nome_completo__icontains',
    ]


class UsuariosSelectWidget(ModelSelect2MultipleWidget):
    model = Usuario
    search_fields = [
        'nome_completo__icontains',
    ]


class GroupsSelectWidget(ModelSelect2MultipleWidget):
    model = Group
    search_fields = [
        'name__icontains',
    ]


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_completo', 'nome_social', 'email', 'cpf',
                  'is_active', 'groups')
        widgets = {
            'groups': GroupsSelectWidget
        }
