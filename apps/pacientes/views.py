from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
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


class PacienteFormMixin:
    """Valida y guarda paciente con formularios relacionados."""

    model = Paciente
    template_name = 'pacientes/paciente_form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('pacientes:lista')

    def _formularios_relacionados(self):
        kwargs = {'instance': self.object} if getattr(self, 'object', None) else {}
        nacionalidad = PacienteNacionalidadFormSet(
            self.request.POST or None,
            self.request.FILES or None,
            **kwargs,
        )
        discapacidad = PacienteDiscapacidadFormSet(
            self.request.POST or None,
            self.request.FILES or None,
            **kwargs,
        )
        oposicion_kwargs = {}
        if self.object:
            try:
                oposicion_kwargs['instance'] = self.object.oposicion_donacion
            except OposicionDonacion.DoesNotExist:
                pass
        oposicion = OposicionDonacionForm(
            self.request.POST or None,
            **oposicion_kwargs,
        )
        voluntad = VoluntadAnticipadaForm(self.request.POST or None)
        return nacionalidad, discapacidad, oposicion, voluntad

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            n, d, o, v = self._formularios_relacionados()
        else:
            inst = getattr(self, 'object', None)
            n = PacienteNacionalidadFormSet(instance=inst)
            d = PacienteDiscapacidadFormSet(instance=inst)
            try:
                o = OposicionDonacionForm(
                    instance=inst.oposicion_donacion if inst else None,
                )
            except (AttributeError, OposicionDonacion.DoesNotExist):
                o = OposicionDonacionForm()
            v = VoluntadAnticipadaForm()
        ctx['nacionalidad_formset'] = n
        ctx['discapacidad_formset'] = d
        ctx['oposicion_form'] = o
        ctx['voluntad_form'] = v
        return ctx

    def _guardar_relacionados(self, paciente, nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form):
        nacionalidad_fs.instance = paciente
        discapacidad_fs.instance = paciente
        nacionalidad_fs.save()
        discapacidad_fs.save()

        if oposicion_form.is_valid():
            datos = oposicion_form.cleaned_data
            if datos.get('manifestacion') and datos.get('fecha_registro'):
                OposicionDonacion.objects.update_or_create(
                    paciente=paciente,
                    defaults=datos,
                )

        if voluntad_form.is_valid() and voluntad_form.cleaned_data.get('tiene_documento'):
            VoluntadAnticipada.objects.create(
                paciente=paciente,
                **voluntad_form.cleaned_data,
            )

    def _respuesta_invalida(self, form, nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form):
        messages.error(
            self.request,
            'No se pudo guardar. Revise los campos marcados en rojo.',
        )
        return self.render_to_response({
            'form': form,
            'nacionalidad_formset': nacionalidad_fs,
            'discapacidad_formset': discapacidad_fs,
            'oposicion_form': oposicion_form,
            'voluntad_form': voluntad_form,
            'titulo': self.get_titulo(),
        })


class PacienteCreateView(AuthRequiredMixin, PacienteFormMixin, CreateView):
    def get_titulo(self):
        return 'Registrar paciente'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = self.get_titulo()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form = self._formularios_relacionados()

        if not all([
            form.is_valid(),
            nacionalidad_fs.is_valid(),
            discapacidad_fs.is_valid(),
            oposicion_form.is_valid(),
            voluntad_form.is_valid(),
        ]):
            return self._respuesta_invalida(
                form, nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form,
            )

        self.object = form.save()
        self._guardar_relacionados(
            self.object, nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form,
        )
        messages.success(request, 'Paciente registrado correctamente.')
        return redirect(self.success_url)


class PacienteUpdateView(AuthRequiredMixin, PacienteFormMixin, UpdateView):
    def get_queryset(self):
        return Paciente.objects.prefetch_related(
            'nacionalidades',
            'discapacidades',
        ).select_related('oposicion_donacion')

    def get_titulo(self):
        return 'Actualizar paciente'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = self.get_titulo()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form = self._formularios_relacionados()

        if not all([
            form.is_valid(),
            nacionalidad_fs.is_valid(),
            discapacidad_fs.is_valid(),
            oposicion_form.is_valid(),
            voluntad_form.is_valid(),
        ]):
            return self._respuesta_invalida(
                form, nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form,
            )

        self.object = form.save()
        self._guardar_relacionados(
            self.object, nacionalidad_fs, discapacidad_fs, oposicion_form, voluntad_form,
        )
        messages.success(request, 'Paciente actualizado correctamente.')
        return redirect(self.success_url)
