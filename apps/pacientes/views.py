from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.pacientes.forms import (
    OposicionDonacionForm,
    PacienteDiscapacidadFormSet,
    PacienteForm,
    PacienteNacionalidadFormSet,
    VoluntadAnticipadaForm,
)
from apps.pacientes.models import OposicionDonacion, Paciente, VoluntadAnticipada
from core.mixins import AuthRequiredMixin


class PacienteListView(AuthRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 15

    def get_queryset(self):
        qs = Paciente.objects.filter(activo=True).select_related(
            'tipo_documento',
            'municipio_residencia',
            'pais_residencia',
        )
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(numero_documento__icontains=q)
                | Q(primer_nombre__icontains=q)
                | Q(primer_apellido__icontains=q)
                | Q(segundo_apellido__icontains=q)
            )
        return qs


class PacienteDetailView(AuthRequiredMixin, DetailView):
    model = Paciente
    template_name = 'pacientes/paciente_detail.html'
    context_object_name = 'paciente'

    def get_queryset(self):
        return Paciente.objects.prefetch_related(
            'nacionalidades__pais',
            'discapacidades__discapacidad',
            'voluntades_anticipadas',
        ).select_related(
            'oposicion_donacion',
            'tipo_documento',
            'municipio_residencia',
            'ocupacion',
            'etnia',
            'administradora_plan',
        )


class PacienteCreateView(AuthRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['nacionalidad_formset'] = PacienteNacionalidadFormSet(self.request.POST)
            ctx['discapacidad_formset'] = PacienteDiscapacidadFormSet(self.request.POST)
            ctx['oposicion_form'] = OposicionDonacionForm(self.request.POST)
            ctx['voluntad_form'] = VoluntadAnticipadaForm(self.request.POST)
        else:
            ctx['nacionalidad_formset'] = PacienteNacionalidadFormSet()
            ctx['discapacidad_formset'] = PacienteDiscapacidadFormSet()
            ctx['oposicion_form'] = OposicionDonacionForm()
            ctx['voluntad_form'] = VoluntadAnticipadaForm()
        ctx['titulo'] = 'Registrar paciente'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        nacionalidad_fs = ctx['nacionalidad_formset']
        discapacidad_fs = ctx['discapacidad_formset']
        oposicion_form = ctx['oposicion_form']
        voluntad_form = ctx['voluntad_form']

        if not (nacionalidad_fs.is_valid() and discapacidad_fs.is_valid()):
            return self.render_to_response(ctx)

        self.object = form.save()
        nacionalidad_fs.instance = self.object
        discapacidad_fs.instance = self.object
        nacionalidad_fs.save()
        discapacidad_fs.save()

        if oposicion_form.is_valid() and oposicion_form.cleaned_data:
            if oposicion_form.cleaned_data.get('manifestacion'):
                OposicionDonacion.objects.create(
                    paciente=self.object,
                    **oposicion_form.cleaned_data,
                )

        if voluntad_form.is_valid() and voluntad_form.cleaned_data.get('tiene_documento'):
            VoluntadAnticipada.objects.create(
                paciente=self.object,
                **voluntad_form.cleaned_data,
            )

        messages.success(self.request, 'Paciente registrado correctamente.')
        return super().form_valid(form)


class PacienteUpdateView(AuthRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['nacionalidad_formset'] = PacienteNacionalidadFormSet(
                self.request.POST, instance=self.object,
            )
            ctx['discapacidad_formset'] = PacienteDiscapacidadFormSet(
                self.request.POST, instance=self.object,
            )
            try:
                ctx['oposicion_form'] = OposicionDonacionForm(
                    self.request.POST, instance=self.object.oposicion_donacion,
                )
            except OposicionDonacion.DoesNotExist:
                ctx['oposicion_form'] = OposicionDonacionForm(self.request.POST)
            ctx['voluntad_form'] = VoluntadAnticipadaForm(self.request.POST)
        else:
            ctx['nacionalidad_formset'] = PacienteNacionalidadFormSet(instance=self.object)
            ctx['discapacidad_formset'] = PacienteDiscapacidadFormSet(instance=self.object)
            try:
                ctx['oposicion_form'] = OposicionDonacionForm(instance=self.object.oposicion_donacion)
            except OposicionDonacion.DoesNotExist:
                ctx['oposicion_form'] = OposicionDonacionForm()
            ctx['voluntad_form'] = VoluntadAnticipadaForm()
        ctx['titulo'] = 'Actualizar paciente'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        nacionalidad_fs = ctx['nacionalidad_formset']
        discapacidad_fs = ctx['discapacidad_formset']

        if not (nacionalidad_fs.is_valid() and discapacidad_fs.is_valid()):
            return self.render_to_response(ctx)

        self.object = form.save()
        nacionalidad_fs.save()
        discapacidad_fs.save()

        oposicion_form = ctx['oposicion_form']
        if oposicion_form.is_valid() and oposicion_form.cleaned_data.get('manifestacion'):
            OposicionDonacion.objects.update_or_create(
                paciente=self.object,
                defaults=oposicion_form.cleaned_data,
            )

        messages.success(self.request, 'Paciente actualizado correctamente.')
        return super().form_valid(form)
