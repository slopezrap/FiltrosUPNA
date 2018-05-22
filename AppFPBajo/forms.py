from django import forms
from .models import ModeloFPBajo

class FormularioFPBajo(forms.ModelForm):
    class Meta:
        model = ModeloFPBajo
        fields = [
            'nameFilter',
            'Ap_db',
            'As_db',
            'Fp_Hz',
            'Fs_Hz',
            'Rg_Ohm',
            'Rl_Ohm',
            ]