"""Paciente inicial con nacionalidades múltiples. Ejecutar: python manage.py seed_pacientes_demo"""
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.catalogos.models import (
    Discapacidad,
    Municipio,
    NivelCIUO,
    Ocupacion,
    Pais,
    PrestadorSalud,
    TipoDocumento,
)
from apps.pacientes.models import (
    OposicionDonacion,
    Paciente,
    PacienteDiscapacidad,
    PacienteNacionalidad,
)
from core.choices import IdentidadGenero, SexoBiologico, SiNo, ZonaResidencia


class Command(BaseCommand):
    help = 'Crea un paciente de referencia con nacionalidades múltiples'

    def handle(self, *args, **options):
        cc = TipoDocumento.objects.get(codigo='CC')
        colombia = Pais.objects.get(codigo='170')
        peru = Pais.objects.get(codigo='604')
        medellin = Municipio.objects.get(codigo='05001')
        eps = PrestadorSalud.objects.filter(codigo='800088702002').first()
        ips = PrestadorSalud.objects.filter(codigo='890903211001').first()
        if not eps:
            eps = PrestadorSalud.objects.filter(es_administradora=True).first()
        if not ips:
            ips = PrestadorSalud.objects.filter(es_administradora=False).first()
        medico = Ocupacion.objects.filter(nivel=NivelCIUO.OCUPACION, codigo='2211').first()
        if not medico:
            medico = Ocupacion.objects.filter(nivel=NivelCIUO.OCUPACION).first()

        paciente, created = Paciente.objects.update_or_create(
            tipo_documento=cc,
            numero_documento='1009876543',
            defaults={
                'primer_nombre': 'Ana',
                'segundo_nombre': 'María',
                'primer_apellido': 'Giraldo',
                'segundo_apellido': 'Arcila',
                'fecha_nacimiento': timezone.make_aware(datetime(1995, 3, 15, 8, 30)),
                'sexo_biologico': SexoBiologico.MUJER,
                'identidad_genero': IdentidadGenero.FEMENINO,
                'ocupacion': medico,
                'pais_residencia': colombia,
                'municipio_residencia': medellin,
                'zona_residencia': ZonaResidencia.URBANA,
                'administradora_plan': eps,
                'prestador_vinculacion': ips,
            },
        )

        PacienteNacionalidad.objects.update_or_create(
            paciente=paciente, pais=colombia,
        )
        PacienteNacionalidad.objects.update_or_create(
            paciente=paciente, pais=peru,
        )

        disc = Discapacidad.objects.filter(codigo='08').first()
        if disc:
            PacienteDiscapacidad.objects.update_or_create(
                paciente=paciente, discapacidad=disc,
            )

        OposicionDonacion.objects.update_or_create(
            paciente=paciente,
            defaults={
                'manifestacion': SiNo.NO,
                'fecha_registro': datetime(2024, 1, 10).date(),
            },
        )

        accion = 'creado' if created else 'actualizado'
        self.stdout.write(
            self.style.SUCCESS(
                f'Paciente {accion}: {paciente} (nacionalidades Colombia y Perú).',
            ),
        )
