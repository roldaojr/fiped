from django import forms
from .models import Trabalho


class TrabalhoChangeForm(forms.ModelForm):
    class Meta:
        model = Trabalho
        fields = ('area_tema',)
