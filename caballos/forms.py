from django import forms
from .models import Caballo


class CaballoForm(forms.ModelForm):
    class Meta:
        model = Caballo
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dieta_detalles': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['fecha_nacimiento', 'dieta_detalles', 'observaciones']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['foto'].widget.attrs.update({'class': 'form-control'})
        self.fields['propietario'].widget.attrs.update({'class': 'form-select'})
        self.fields['box'].widget.attrs.update({'class': 'form-select'})
        self.fields['sexo'].widget.attrs.update({'class': 'form-select'})
        self.fields['tipo_pupilaje'].widget.attrs.update({'class': 'form-select'})
