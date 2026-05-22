"""
Información del paciente - Resolución 866/2021.
Estructuras separadas: oposición donación, voluntad anticipada.
Relaciones múltiples: discapacidades, nacionalidades.
"""
from django.db import models

from apps.catalogos.models import (
    ComunidadEtnica,
    Discapacidad,
    Etnia,
    Municipio,
    Ocupacion,
    Pais,
    PrestadorSalud,
    TipoDocumento,
)
from core.choices import IdentidadGenero, SexoBiologico, SiNo, ZonaResidencia


class Paciente(models.Model):
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name='pacientes',
        verbose_name='Tipo de documento',
    )
    numero_documento = models.CharField('Número de documento', max_length=20)
    primer_nombre = models.CharField('Primer nombre', max_length=60)
    segundo_nombre = models.CharField('Segundo nombre', max_length=60, blank=True)
    primer_apellido = models.CharField('Primer apellido', max_length=60)
    segundo_apellido = models.CharField('Segundo apellido', max_length=60, blank=True)
    fecha_nacimiento = models.DateTimeField('Fecha y hora de nacimiento')
    sexo_biologico = models.CharField(
        'Sexo biológico',
        max_length=2,
        choices=SexoBiologico.choices,
    )
    identidad_genero = models.CharField(
        'Identidad de género',
        max_length=2,
        choices=IdentidadGenero.choices,
    )
    ocupacion = models.ForeignKey(
        Ocupacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes',
        verbose_name='Ocupación (CIUO-88)',
    )
    pais_residencia = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        related_name='residentes',
        verbose_name='País de residencia habitual',
    )
    municipio_residencia = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        related_name='pacientes',
        verbose_name='Municipio de residencia',
    )
    zona_residencia = models.CharField(
        'Zona de residencia',
        max_length=2,
        choices=ZonaResidencia.choices,
    )
    etnia = models.ForeignKey(
        Etnia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes',
    )
    comunidad_etnica = models.ForeignKey(
        ComunidadEtnica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes',
    )
    administradora_plan = models.ForeignKey(
        PrestadorSalud,
        on_delete=models.PROTECT,
        related_name='pacientes_afiliados',
        verbose_name='Administradora del plan de beneficios',
    )
    prestador_vinculacion = models.ForeignKey(
        PrestadorSalud,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes_vinculados',
        verbose_name='Prestador de vinculación',
    )
    activo = models.BooleanField('Activo', default=True)
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        db_table = 'pac_paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['primer_apellido', 'primer_nombre']
        unique_together = [('tipo_documento', 'numero_documento')]

    def __str__(self):
        return (
            f'{self.tipo_documento_id} {self.numero_documento} - '
            f'{self.primer_nombre} {self.primer_apellido}'
        )

    @property
    def nombre_completo(self):
        partes = [
            self.primer_nombre,
            self.segundo_nombre,
            self.primer_apellido,
            self.segundo_apellido,
        ]
        return ' '.join(p for p in partes if p).strip()


class PacienteNacionalidad(models.Model):
    """Múltiples nacionalidades por paciente (Res. 866)."""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='nacionalidades',
    )
    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        related_name='nacionalidades_paciente',
    )

    class Meta:
        db_table = 'pac_nacionalidad'
        verbose_name = 'Nacionalidad del paciente'
        verbose_name_plural = 'Nacionalidades del paciente'
        ordering = ['pais__nombre']
        unique_together = [('paciente', 'pais')]

    def __str__(self):
        return f'{self.paciente} - {self.pais}'


class PacienteDiscapacidad(models.Model):
    """Múltiples discapacidades por paciente."""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='discapacidades',
    )
    discapacidad = models.ForeignKey(
        Discapacidad,
        on_delete=models.PROTECT,
        related_name='pacientes',
    )

    class Meta:
        db_table = 'pac_discapacidad'
        verbose_name = 'Discapacidad del paciente'
        verbose_name_plural = 'Discapacidades del paciente'
        ordering = ['discapacidad__codigo']
        unique_together = [('paciente', 'discapacidad')]

    def __str__(self):
        return f'{self.paciente} - {self.discapacidad}'


class OposicionDonacion(models.Model):
    """Estructura separada - oposición a presunción legal de donación (Ley 1805/2016)."""
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='oposicion_donacion',
    )
    manifestacion = models.CharField(
        'Manifestación de oposición',
        max_length=2,
        choices=SiNo.choices,
        help_text='01=Sí se opone, 02=No',
    )
    fecha_registro = models.DateField('Fecha de registro del documento')

    class Meta:
        db_table = 'pac_oposicion_donacion'
        verbose_name = 'Oposición a donación'
        verbose_name_plural = 'Oposiciones a donación'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'Oposición {self.paciente} - {self.get_manifestacion_display()}'


class VoluntadAnticipada(models.Model):
    """Estructura separada - documento de voluntad anticipada."""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='voluntades_anticipadas',
    )
    tiene_documento = models.CharField(
        '¿Tiene documento de voluntad anticipada?',
        max_length=2,
        choices=SiNo.choices,
    )
    fecha_documento = models.DateField(
        'Fecha de suscripción, modificación o revocación',
        null=True,
        blank=True,
    )
    prestador_documento = models.ForeignKey(
        PrestadorSalud,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voluntades_anticipadas',
        verbose_name='Prestador donde reposa el documento',
    )
    observaciones = models.TextField('Observaciones', blank=True)

    class Meta:
        db_table = 'pac_voluntad_anticipada'
        verbose_name = 'Voluntad anticipada'
        verbose_name_plural = 'Voluntades anticipadas'
        ordering = ['-fecha_documento']

    def __str__(self):
        return f'Voluntad anticipada - {self.paciente}'
