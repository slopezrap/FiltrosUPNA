from django import forms
from .models import ModeloFPBajo

filtros= [
    ('Butterworth', 'Butterworth'),
    ('Chebyshev', 'Chebyshev'),
    ]

class FormularioFPBajo(forms.ModelForm):
    tipoFiltro = forms.ChoiceField(choices=filtros, required=True, label="Seleccione el tipo de filtro que desea crear")
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