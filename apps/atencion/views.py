from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.atencion.forms import ContactoSaludForm, TecnologiaSaludFormSet
from apps.atencion.models import ContactoSalud
from core.mixins import AuthRequiredMixin


class ContactoListView(AuthRequiredMixin, ListView):
    model = ContactoSalud
    template_name = 'atencion/contacto_list.html'
    context_object_name = 'contactos'
    paginate_by = 15

    def get_queryset(self):
        qs = ContactoSalud.objects.filter(activo=True).select_related(
            'paciente',
            'prestador',
            'diagnostico_ingreso',
            'causa',
        )
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(paciente__numero_documento__icontains=q)
                | Q(paciente__primer_apellido__icontains=q)
                | Q(paciente__primer_nombre__icontains=q)
            )
        return qs


class ContactoDetailView(AuthRequiredMixin, DetailView):
    model = ContactoSalud
    template_name = 'atencion/contacto_detail.html'
    context_object_name = 'contacto'

    def get_queryset(self):
        return ContactoSalud.objects.select_related(
            'paciente',
            'prestador',
            'modalidad',
            'via_ingreso',
            'causa',
            'diagnostico_ingreso',
        ).prefetch_related('tecnologias')


class ContactoCreateView(AuthRequiredMixin, CreateView):
    model = ContactoSalud
    form_class = ContactoSaludForm
    template_name = 'atencion/contacto_form.html'
    success_url = reverse_lazy('atencion:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['tecnologia_formset'] = TecnologiaSaludFormSet(self.request.POST)
        else:
            ctx['tecnologia_formset'] = TecnologiaSaludFormSet()
        ctx['titulo'] = 'Registrar atención en urgencias'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        tecnologia_fs = ctx['tecnologia_formset']
        if not tecnologia_fs.is_valid():
            return self.render_to_response(ctx)
        self.object = form.save()
        tecnologia_fs.instance = self.object
        tecnologia_fs.save()
        messages.success(self.request, 'Contacto con el servicio de salud registrado.')
        return super().form_valid(form)


class ContactoUpdateView(AuthRequiredMixin, UpdateView):
    model = ContactoSalud
    form_class = ContactoSaludForm
    template_name = 'atencion/contacto_form.html'
    success_url = reverse_lazy('atencion:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['tecnologia_formset'] = TecnologiaSaludFormSet(
                self.request.POST, instance=self.object,
            )
        else:
            ctx['tecnologia_formset'] = TecnologiaSaludFormSet(instance=self.object)
        ctx['titulo'] = 'Actualizar atención'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        tecnologia_fs = ctx['tecnologia_formset']
        if not tecnologia_fs.is_valid():
            return self.render_to_response(ctx)
        self.object = form.save()
        tecnologia_fs.instance = self.object
        tecnologia_fs.save()
        messages.success(self.request, 'Contacto actualizado correctamente.')
        return super().form_valid(form)
