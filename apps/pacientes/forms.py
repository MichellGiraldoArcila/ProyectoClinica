from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils import timezone

from apps.catalogos.models import NivelCIUO, Ocupacion
from apps.pacientes.models import (
    OposicionDonacion,
    Paciente,
    PacienteDiscapacidad,
    PacienteNacionalidad,
    VoluntadAnticipada,
)

CODIGO_OCUPACION_OTRA = '9999'


class PacienteForm(forms.ModelForm):
    ocupacion_otra = forms.CharField(
        label='Especifique ocupación (si eligió Otra)',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_ocupacion_otra'}),
    )

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
                format='%Y-%m-%dT%H:%M',
            ),
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ocupacion'].queryset = Ocupacion.objects.filter(
            nivel=NivelCIUO.OCUPACION,
        ).order_by('nombre')
        self.fields['ocupacion'].label = 'Ocupación CIUO-88'
        self.fields['ocupacion'].required = False
        self.fields['ocupacion'].empty_label = '---------'
        if self.instance.pk and self.instance.ocupacion_id == CODIGO_OCUPACION_OTRA:
            self.fields['ocupacion_otra'].initial = self.instance.ocupacion_otra

        for name, field in self.fields.items():
            if name == 'ocupacion_otra':
                continue
            if name not in self.Meta.widgets:
                css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
                field.widget.attrs.setdefault('class', css)

    def clean_fecha_nacimiento(self):
        valor = self.cleaned_data.get('fecha_nacimiento')
        if valor and timezone.is_naive(valor):
            return timezone.make_aware(valor, timezone.get_current_timezone())
        return valor

    def clean(self):
        cleaned = super().clean()
        ocupacion = cleaned.get('ocupacion')
        ocupacion_otra = (cleaned.get('ocupacion_otra') or '').strip()

        if ocupacion and ocupacion.pk == CODIGO_OCUPACION_OTRA and not ocupacion_otra:
            self.add_error(
                'ocupacion_otra',
                'Indique cuál es la ocupación cuando selecciona Otra.',
            )
        if ocupacion and ocupacion.pk != CODIGO_OCUPACION_OTRA:
            cleaned['ocupacion_otra'] = ''
        return cleaned

    def save(self, commit=True):
        instancia = super().save(commit=False)
        instancia.ocupacion_otra = (self.cleaned_data.get('ocupacion_otra') or '').strip()
        if commit:
            instancia.save()
            self.save_m2m()
        return instancia


class PacienteNacionalidadForm(forms.ModelForm):
    class Meta:
        model = PacienteNacionalidad
        fields = ('pais',)
        labels = {'pais': 'País de nacionalidad (código ISO 3166)'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].required = False
        self.fields['pais'].widget.attrs.setdefault('class', 'form-select')

    def has_changed(self):
        if not self.instance.pk:
            pais = self.data.get(self.add_prefix('pais')) if self.data else None
            if not pais:
                return False
        return super().has_changed()


class NacionalidadFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        paises = []
        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or form.cleaned_data.get('DELETE'):
                continue
            pais = form.cleaned_data.get('pais')
            if pais:
                paises.append(pais)
        if not paises:
            raise ValidationError(
                'Debe registrar al menos un país de nacionalidad (Res. 866/2021).',
            )


class OposicionDonacionForm(forms.ModelForm):
    class Meta:
        model = OposicionDonacion
        fields = ['manifestacion', 'fecha_registro']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manifestacion'].required = False
        self.fields['fecha_registro'].required = False
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = (
                    'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
                )


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


PacienteNacionalidadFormSet = inlineformset_factory(
    Paciente,
    PacienteNacionalidad,
    form=PacienteNacionalidadForm,
    formset=NacionalidadFormSet,
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
