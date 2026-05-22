from django import forms
from django.forms import inlineformset_factory

from apps.atencion.models import ContactoSalud, TecnologiaSalud


class ContactoSaludForm(forms.ModelForm):
    class Meta:
        model = ContactoSalud
        fields = [
            'paciente',
            'prestador',
            'fecha_inicio_atencion',
            'modalidad',
            'grupo_servicios',
            'entorno_atencion',
            'via_ingreso',
            'causa',
            'fecha_triage',
            'clasificacion_triage',
            'diagnostico_ingreso',
            'tipo_diagnostico_ingreso',
        ]
        widgets = {
            'fecha_inicio_atencion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_triage': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs.setdefault('class', css)


class TecnologiaSaludForm(forms.ModelForm):
    class Meta:
        model = TecnologiaSalud
        fields = [
            'tipo_tecnologia',
            'codigo_tecnologia',
            'nombre_tecnologia',
            'finalidad',
            'fecha_prescripcion',
            'talento_humano',
        ]
        widgets = {
            'fecha_prescripcion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


TecnologiaSaludFormSet = inlineformset_factory(
    ContactoSalud,
    TecnologiaSalud,
    form=TecnologiaSaludForm,
    extra=1,
    can_delete=True,
)
