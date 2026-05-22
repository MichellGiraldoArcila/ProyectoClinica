"""
Contacto con el servicio de salud y tecnologías - Resolución 866/2021.
Atención en urgencias y resultados de valoración clínica.
"""
from django.db import models

from apps.catalogos.models import (
    CausaAtencion,
    Celula,
    ComponenteSanguineo,
    CondicionEgreso,
    DescripcionMedicamento,
    Diagnostico,
    DispositivoMedico,
    FinalidadTecnologia,
    FluidoOrganico,
    InstrumentoMedicion,
    MedicamentoConRegistro,
    MedicamentoSinRegistro,
    MedicamentoVital,
    ModalidadTecnologia,
    Organo,
    ParametroResultado,
    PreparacionMagistral,
    PrestadorSalud,
    Procedimiento,
    ProductoNutricional,
    ServicioComplementario,
    TalentoHumano,
    Tejido,
    TipoTecnologiaSalud,
    UnidadMedida,
    UnidadTiempo,
    ViaAdministracion,
    ViaIngreso,
)
from apps.pacientes.models import Paciente
from core.choices import (
    AlcanceIncapacidad,
    ClasificacionTriage,
    EntornoAtencion,
    GrupoServicios,
    Parentesco,
    TipoAlergia,
    TipoDiagnostico,
    TipoFactorRiesgo,
)


class ContactoSalud(models.Model):
    """Contacto con el servicio de salud - atención en urgencias."""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='contactos_salud',
    )
    prestador = models.ForeignKey(
        PrestadorSalud,
        on_delete=models.PROTECT,
        related_name='contactos_atencion',
        verbose_name='Prestador que realiza la atención',
    )
    fecha_inicio_atencion = models.DateTimeField('Fecha y hora inicio de atención')
    modalidad = models.ForeignKey(
        ModalidadTecnologia,
        on_delete=models.PROTECT,
        related_name='contactos',
    )
    grupo_servicios = models.CharField(
        'Grupo de servicios',
        max_length=2,
        choices=GrupoServicios.choices,
    )
    entorno_atencion = models.CharField(
        'Entorno de atención',
        max_length=2,
        choices=EntornoAtencion.choices,
    )
    via_ingreso = models.ForeignKey(
        ViaIngreso,
        on_delete=models.PROTECT,
        related_name='contactos',
    )
    causa = models.ForeignKey(
        CausaAtencion,
        on_delete=models.PROTECT,
        related_name='contactos',
        verbose_name='Causa que motiva la atención',
    )
    fecha_triage = models.DateTimeField('Fecha y hora del triage', null=True, blank=True)
    clasificacion_triage = models.CharField(
        'Clasificación triage',
        max_length=2,
        choices=ClasificacionTriage.choices,
        blank=True,
    )
    diagnostico_ingreso = models.ForeignKey(
        Diagnostico,
        on_delete=models.PROTECT,
        related_name='contactos_ingreso',
        verbose_name='Diagnóstico principal de ingreso',
    )
    tipo_diagnostico_ingreso = models.CharField(
        'Tipo diagnóstico de ingreso',
        max_length=2,
        choices=TipoDiagnostico.choices,
    )
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ate_contacto_salud'
        verbose_name = 'Contacto con el servicio de salud'
        verbose_name_plural = 'Contactos con el servicio de salud'
        ordering = ['-fecha_inicio_atencion']

    def __str__(self):
        return f'Contacto {self.pk} - {self.paciente} ({self.fecha_inicio_atencion:%Y-%m-%d})'


class TecnologiaSalud(models.Model):
    """Tecnologías en salud asociadas a un contacto."""
    contacto = models.ForeignKey(
        ContactoSalud,
        on_delete=models.CASCADE,
        related_name='tecnologias',
    )
    tipo_tecnologia = models.ForeignKey(
        TipoTecnologiaSalud,
        on_delete=models.PROTECT,
        related_name='tecnologias',
    )
    codigo_tecnologia = models.CharField('Código de la tecnología', max_length=25)
    nombre_tecnologia = models.CharField('Nombre de la tecnología', max_length=200)
    finalidad = models.ForeignKey(
        FinalidadTecnologia,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tecnologias',
    )
    descripcion_medicamento = models.ForeignKey(
        DescripcionMedicamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tecnologias',
    )
    fecha_prescripcion = models.DateTimeField(null=True, blank=True)
    dosis_prescrita = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
    )
    unidad_dosis_prescrita = models.ForeignKey(
        UnidadMedida,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dosis_prescritas',
    )
    via_administracion = models.ForeignKey(
        ViaAdministracion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tecnologias',
    )
    duracion_valor = models.PositiveIntegerField('Duración prescrita', null=True, blank=True)
    duracion_unidad = models.ForeignKey(
        UnidadTiempo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='duraciones',
    )
    frecuencia_cantidad = models.PositiveIntegerField(null=True, blank=True)
    frecuencia_unidad = models.ForeignKey(
        UnidadTiempo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='frecuencias',
    )
    dosis_administrada = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
    )
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    dosis_entregada = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
    )
    unidades_entregadas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    unidad_entregada = models.ForeignKey(
        UnidadMedida,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unidades_entregadas',
    )
    talento_humano = models.ForeignKey(
        TalentoHumano,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tecnologias_aplicadas',
    )

    class Meta:
        db_table = 'ate_tecnologia_salud'
        verbose_name = 'Tecnología en salud'
        verbose_name_plural = 'Tecnologías en salud'
        ordering = ['-fecha_prescripcion']

    def __str__(self):
        return f'{self.tipo_tecnologia_id} - {self.nombre_tecnologia}'


class ResultadoValoracion(models.Model):
    """Resultado de evaluación / valoración clínica del contacto."""
    contacto = models.OneToOneField(
        ContactoSalud,
        on_delete=models.CASCADE,
        related_name='resultado_valoracion',
    )
    fecha_resultado = models.DateTimeField('Fecha del resultado')
    instrumento = models.ForeignKey(
        InstrumentoMedicion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resultados',
    )
    parametro = models.ForeignKey(
        ParametroResultado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resultados',
    )
    valor_resultado = models.DecimalField(
        'Valor del resultado observado',
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
    )
    diagnostico_egreso = models.ForeignKey(
        Diagnostico,
        on_delete=models.PROTECT,
        related_name='egresos_principal',
        verbose_name='Diagnóstico principal de egreso',
    )
    tipo_diagnostico_egreso = models.CharField(
        max_length=2,
        choices=TipoDiagnostico.choices,
    )
    diagnostico_relacionado = models.ForeignKey(
        Diagnostico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='egresos_relacionados',
    )
    diagnostico_complicacion = models.ForeignKey(
        Diagnostico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='complicaciones',
    )
    condicion_egreso = models.ForeignKey(
        CondicionEgreso,
        on_delete=models.PROTECT,
        related_name='resultados',
    )
    diagnostico_muerte = models.ForeignKey(
        Diagnostico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='causas_muerte',
    )
    fecha_fin_atencion = models.DateTimeField('Fecha y hora fin de atención')
    prestador_referencia = models.ForeignKey(
        PrestadorSalud,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referencias_egreso',
    )
    dias_licencia_maternidad = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Días licencia maternidad',
    )
    talento_humano_egreso = models.ForeignKey(
        TalentoHumano,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='egresos_realizados',
    )

    class Meta:
        db_table = 'ate_resultado_valoracion'
        verbose_name = 'Resultado de valoración'
        verbose_name_plural = 'Resultados de valoración'
        ordering = ['-fecha_resultado']

    def __str__(self):
        return f'Resultado contacto {self.contacto_id}'


class Incapacidad(models.Model):
    resultado = models.OneToOneField(
        ResultadoValoracion,
        on_delete=models.CASCADE,
        related_name='incapacidad',
    )
    alcance = models.CharField(max_length=2, choices=AlcanceIncapacidad.choices)
    dias = models.PositiveSmallIntegerField('Días de incapacidad')

    class Meta:
        db_table = 'ate_incapacidad'
        verbose_name = 'Incapacidad'
        verbose_name_plural = 'Incapacidades'
        ordering = ['-dias']

    def __str__(self):
        return f'Incapacidad {self.dias} días ({self.get_alcance_display()})'


class AntecedenteSalud(models.Model):
    resultado = models.ForeignKey(
        ResultadoValoracion,
        on_delete=models.CASCADE,
        related_name='antecedentes',
    )
    tipo_alergia = models.CharField(
        'Tipo de antecedente/alergia',
        max_length=2,
        choices=TipoAlergia.choices,
        blank=True,
    )
    nombre_alergeno = models.CharField('Nombre del alérgeno', max_length=250, blank=True)
    diagnostico_familiar = models.ForeignKey(
        Diagnostico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='antecedentes_familiares',
    )
    parentesco = models.CharField(
        max_length=2,
        choices=Parentesco.choices,
        blank=True,
    )

    class Meta:
        db_table = 'ate_antecedente_salud'
        verbose_name = 'Antecedente de salud'
        verbose_name_plural = 'Antecedentes de salud'
        ordering = ['tipo_alergia']

    def __str__(self):
        return f'Antecedente {self.pk} - contacto {self.resultado.contacto_id}'


class FactorRiesgoExposicion(models.Model):
    resultado = models.ForeignKey(
        ResultadoValoracion,
        on_delete=models.CASCADE,
        related_name='factores_riesgo',
    )
    tipo_factor = models.CharField(
        max_length=2,
        choices=TipoFactorRiesgo.choices,
    )
    nombre_factor = models.CharField('Nombre del factor de riesgo', max_length=250)

    class Meta:
        db_table = 'ate_factor_riesgo'
        verbose_name = 'Exposición a factor de riesgo'
        verbose_name_plural = 'Exposiciones a factores de riesgo'
        ordering = ['tipo_factor']

    def __str__(self):
        return f'{self.get_tipo_factor_display()}: {self.nombre_factor}'
