from django import forms
from .models import ModeloBlog

class FormularioBlog(forms.ModelForm):
    content = forms.CharField(label="Contenido",required=True,widget=forms.Textarea)
    class Meta:
        model = ModeloBlog
        fields = [
            'title',
            'content',
            'image',
            ]