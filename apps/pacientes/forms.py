from django import forms
from django.forms import inlineformset_factory

from apps.pacientes.models import (
    OposicionDonacion,
    Paciente,
    PacienteDiscapacidad,
    PacienteNacionalidad,
    VoluntadAnticipada,
)


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'tipo_documento',
            'numero_documento',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'fecha_nacimiento',
            'sexo_biologico',
            'identidad_genero',
            'ocupacion',
            'pais_residencia',
            'municipio_residencia',
            'zona_residencia',
            'etnia',
            'comunidad_etnica',
            'administradora_plan',
            'prestador_vinculacion',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
            ),
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in self.Meta.widgets:
                css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
                field.widget.attrs.setdefault('class', css)


class OposicionDonacionForm(forms.ModelForm):
    class Meta:
        model = OposicionDonacion
        fields = ['manifestacion', 'fecha_registro']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-select' if isinstance(
                    field.widget, forms.Select,
                ) else 'form-control'


class VoluntadAnticipadaForm(forms.ModelForm):
    class Meta:
        model = VoluntadAnticipada
        fields = [
            'tiene_documento',
            'fecha_documento',
            'prestador_documento',
            'observaciones',
        ]
        widgets = {
            'fecha_documento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


PacienteNacionalidadFormSet = inlineformset_factory(
    Paciente,
    PacienteNacionalidad,
    fields=('pais',),
    extra=1,
    can_delete=True,
)

PacienteDiscapacidadFormSet = inlineformset_factory(
    Paciente,
    PacienteDiscapacidad,
    fields=('discapacidad',),
    extra=1,
    can_delete=True,
)
