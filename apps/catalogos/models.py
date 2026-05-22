"""
Catálogos de referencia - Resolución 866/2021.
Campos con más de 5 opciones se modelan como entidades independientes.
"""
from django.db import models

from core.validators import validar_codigo_iso_pais, validar_codigo_municipio, validar_codigo_prestador


class Pais(models.Model):
    codigo = models.CharField(
        'Código país (ISO 3166)',
        max_length=3,
        primary_key=True,
        validators=[validar_codigo_iso_pais],
    )
    nombre = models.CharField('Nombre del país', max_length=200)

    class Meta:
        db_table = 'cat_pais'
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class TipoDocumento(models.Model):
    codigo = models.CharField('Código', max_length=2, primary_key=True)
    nombre = models.CharField('Tipo de documento', max_length=100)

    class Meta:
        db_table = 'cat_tipo_documento'
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documento'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Ocupacion(models.Model):
    codigo = models.CharField('Código CIUO-88', max_length=4, primary_key=True)
    nombre = models.CharField('Nombre de la ocupación', max_length=250)

    class Meta:
        db_table = 'cat_ocupacion'
        verbose_name = 'Ocupación'
        verbose_name_plural = 'Ocupaciones (CIUO-88)'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Municipio(models.Model):
    codigo = models.CharField(
        'Código DIVIPOLA',
        max_length=5,
        primary_key=True,
        validators=[validar_codigo_municipio],
    )
    nombre = models.CharField('Nombre del municipio', max_length=200)
    departamento = models.CharField('Departamento', max_length=100, blank=True)

    class Meta:
        db_table = 'cat_municipio'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Etnia(models.Model):
    codigo = models.CharField('Código etnia', max_length=2, primary_key=True)
    nombre = models.CharField('Etnia', max_length=100)

    class Meta:
        db_table = 'cat_etnia'
        verbose_name = 'Etnia'
        verbose_name_plural = 'Etnias'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ComunidadEtnica(models.Model):
    codigo = models.CharField('Código comunidad', max_length=3, primary_key=True)
    nombre = models.CharField('Comunidad étnica', max_length=200)
    etnia = models.ForeignKey(
        Etnia,
        on_delete=models.PROTECT,
        related_name='comunidades',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'cat_comunidad_etnica'
        verbose_name = 'Comunidad étnica'
        verbose_name_plural = 'Comunidades étnicas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Discapacidad(models.Model):
    codigo = models.CharField('Código', max_length=2, primary_key=True)
    nombre = models.CharField('Categoría de discapacidad', max_length=100)

    class Meta:
        db_table = 'cat_discapacidad'
        verbose_name = 'Discapacidad'
        verbose_name_plural = 'Discapacidades'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class PrestadorSalud(models.Model):
    codigo = models.CharField(
        'Código prestador SGSSS',
        max_length=12,
        primary_key=True,
        validators=[validar_codigo_prestador],
    )
    nombre = models.CharField('Nombre de la entidad', max_length=300)
    es_administradora = models.BooleanField('Es administradora de plan de beneficios', default=False)

    class Meta:
        db_table = 'cat_prestador_salud'
        verbose_name = 'Prestador de salud'
        verbose_name_plural = 'Prestadores de salud'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ModalidadTecnologia(models.Model):
    codigo = models.CharField('Código modalidad', max_length=2, primary_key=True)
    nombre = models.CharField('Modalidad de realización', max_length=150)

    class Meta:
        db_table = 'cat_modalidad_tecnologia'
        verbose_name = 'Modalidad de tecnología'
        verbose_name_plural = 'Modalidades de tecnología'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ViaIngreso(models.Model):
    codigo = models.CharField('Código vía de ingreso', max_length=2, primary_key=True)
    nombre = models.CharField('Vía de ingreso', max_length=150)

    class Meta:
        db_table = 'cat_via_ingreso'
        verbose_name = 'Vía de ingreso'
        verbose_name_plural = 'Vías de ingreso'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class CausaAtencion(models.Model):
    codigo = models.CharField('Código causa', max_length=2, primary_key=True)
    nombre = models.CharField('Causa que motiva la atención', max_length=200)

    class Meta:
        db_table = 'cat_causa_atencion'
        verbose_name = 'Causa de atención'
        verbose_name_plural = 'Causas de atención'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class EnfermedadHuerfana(models.Model):
    codigo = models.CharField('Código enfermedad huérfana', max_length=4, primary_key=True)
    nombre = models.CharField('Nombre', max_length=300)

    class Meta:
        db_table = 'cat_enfermedad_huerfana'
        verbose_name = 'Enfermedad huérfana'
        verbose_name_plural = 'Enfermedades huérfanas'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Diagnostico(models.Model):
    codigo = models.CharField('Código CIE-10', max_length=4, primary_key=True)
    nombre = models.CharField('Nombre del diagnóstico', max_length=300)
    enfermedad_huerfana = models.ForeignKey(
        EnfermedadHuerfana,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='diagnosticos',
    )

    class Meta:
        db_table = 'cat_diagnostico'
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos (CIE-10)'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class TipoTecnologiaSalud(models.Model):
    codigo = models.CharField('Código tipo', max_length=2, primary_key=True)
    nombre = models.CharField('Tipo de tecnología en salud', max_length=100)

    class Meta:
        db_table = 'cat_tipo_tecnologia_salud'
        verbose_name = 'Tipo de tecnología en salud'
        verbose_name_plural = 'Tipos de tecnología en salud'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class FinalidadTecnologia(models.Model):
    codigo = models.CharField('Código finalidad', max_length=2, primary_key=True)
    nombre = models.CharField('Finalidad', max_length=200)

    class Meta:
        db_table = 'cat_finalidad_tecnologia'
        verbose_name = 'Finalidad de tecnología'
        verbose_name_plural = 'Finalidades de tecnología'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Procedimiento(models.Model):
    codigo = models.CharField('Código CUPS', max_length=6, primary_key=True)
    nombre = models.CharField('Procedimiento', max_length=300)

    class Meta:
        db_table = 'cat_procedimiento'
        verbose_name = 'Procedimiento (CUPS)'
        verbose_name_plural = 'Procedimientos'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class MedicamentoConRegistro(models.Model):
    codigo = models.CharField('Código IUM', max_length=15, primary_key=True)
    nombre = models.CharField('Medicamento', max_length=300)

    class Meta:
        db_table = 'cat_medicamento_registro'
        verbose_name = 'Medicamento con registro sanitario'
        verbose_name_plural = 'Medicamentos con registro'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class MedicamentoVital(models.Model):
    codigo = models.CharField('Código IUM', max_length=15, primary_key=True)
    nombre = models.CharField('Medicamento vital no disponible', max_length=300)

    class Meta:
        db_table = 'cat_medicamento_vital'
        verbose_name = 'Medicamento vital no disponible'
        verbose_name_plural = 'Medicamentos vitales no disponibles'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class PreparacionMagistral(models.Model):
    codigo = models.CharField('Código', max_length=15, primary_key=True)
    nombre = models.CharField('Preparación magistral', max_length=300)

    class Meta:
        db_table = 'cat_preparacion_magistral'
        verbose_name = 'Preparación magistral'
        verbose_name_plural = 'Preparaciones magistrales'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class MedicamentoSinRegistro(models.Model):
    codigo = models.CharField('Código UNIRS', max_length=15, primary_key=True)
    nombre = models.CharField('Medicamento sin registro (UNIRS)', max_length=300)

    class Meta:
        db_table = 'cat_medicamento_sin_registro'
        verbose_name = 'Medicamento sin registro'
        verbose_name_plural = 'Medicamentos sin registro'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class DispositivoMedico(models.Model):
    codigo = models.CharField('Código', max_length=25, primary_key=True)
    nombre = models.CharField('Dispositivo médico', max_length=300)

    class Meta:
        db_table = 'cat_dispositivo_medico'
        verbose_name = 'Dispositivo médico'
        verbose_name_plural = 'Dispositivos médicos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ComponenteSanguineo(models.Model):
    codigo = models.CharField('Código', max_length=19, primary_key=True)
    nombre = models.CharField('Componente sanguíneo', max_length=300)

    class Meta:
        db_table = 'cat_componente_sanguineo'
        verbose_name = 'Componente sanguíneo'
        verbose_name_plural = 'Componentes sanguíneos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class FluidoOrganico(models.Model):
    codigo = models.CharField('Código', max_length=19, primary_key=True)
    nombre = models.CharField('Fluido orgánico', max_length=300)

    class Meta:
        db_table = 'cat_fluido_organico'
        verbose_name = 'Fluido orgánico'
        verbose_name_plural = 'Fluidos orgánicos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Organo(models.Model):
    codigo = models.CharField('Código', max_length=19, primary_key=True)
    nombre = models.CharField('Órgano', max_length=300)

    class Meta:
        db_table = 'cat_organo'
        verbose_name = 'Órgano'
        verbose_name_plural = 'Órganos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Tejido(models.Model):
    codigo = models.CharField('Código', max_length=19, primary_key=True)
    nombre = models.CharField('Tejido', max_length=300)

    class Meta:
        db_table = 'cat_tejido'
        verbose_name = 'Tejido'
        verbose_name_plural = 'Tejidos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Celula(models.Model):
    codigo = models.CharField('Código', max_length=19, primary_key=True)
    nombre = models.CharField('Célula', max_length=300)

    class Meta:
        db_table = 'cat_celula'
        verbose_name = 'Célula'
        verbose_name_plural = 'Células'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ProductoNutricional(models.Model):
    codigo = models.CharField('Código', max_length=15, primary_key=True)
    nombre = models.CharField('Producto nutricional', max_length=300)

    class Meta:
        db_table = 'cat_producto_nutricional'
        verbose_name = 'Producto nutricional'
        verbose_name_plural = 'Productos nutricionales'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ServicioComplementario(models.Model):
    codigo = models.CharField('Código', max_length=15, primary_key=True)
    nombre = models.CharField('Servicio complementario', max_length=300)

    class Meta:
        db_table = 'cat_servicio_complementario'
        verbose_name = 'Servicio complementario'
        verbose_name_plural = 'Servicios complementarios'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class DescripcionMedicamento(models.Model):
    codigo = models.CharField('Código DCI', max_length=4, primary_key=True)
    descripcion = models.CharField('Denominación común internacional', max_length=300)

    class Meta:
        db_table = 'cat_descripcion_medicamento'
        verbose_name = 'Descripción medicamento (DCI)'
        verbose_name_plural = 'Descripciones de medicamentos'
        ordering = ['descripcion']

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'


class UnidadMedida(models.Model):
    codigo = models.CharField('Código UMM', max_length=4, primary_key=True)
    nombre = models.CharField('Unidad', max_length=100)
    tipo_unidad = models.CharField('Tipo de unidad', max_length=50, blank=True)

    class Meta:
        db_table = 'cat_unidad_medida'
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ViaAdministracion(models.Model):
    codigo = models.CharField('Código VAD', max_length=3, primary_key=True)
    nombre = models.CharField('Vía de administración', max_length=150)

    class Meta:
        db_table = 'cat_via_administracion'
        verbose_name = 'Vía de administración'
        verbose_name_plural = 'Vías de administración'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class UnidadTiempo(models.Model):
    codigo = models.CharField('Código', max_length=1, primary_key=True)
    nombre = models.CharField('Unidad de tiempo', max_length=50)

    class Meta:
        db_table = 'cat_unidad_tiempo'
        verbose_name = 'Unidad de tiempo'
        verbose_name_plural = 'Unidades de tiempo'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class InstrumentoMedicion(models.Model):
    codigo = models.CharField('Código', max_length=4, primary_key=True)
    nombre = models.CharField('Instrumento de medición', max_length=200)

    class Meta:
        db_table = 'cat_instrumento_medicion'
        verbose_name = 'Instrumento de medición'
        verbose_name_plural = 'Instrumentos de medición'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ParametroResultado(models.Model):
    codigo = models.CharField('Código parámetro', max_length=2, primary_key=True)
    nombre = models.CharField('Parámetro de resultado', max_length=200)

    class Meta:
        db_table = 'cat_parametro_resultado'
        verbose_name = 'Parámetro de resultado'
        verbose_name_plural = 'Parámetros de resultado'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class CondicionEgreso(models.Model):
    codigo = models.CharField('Código', max_length=2, primary_key=True)
    nombre = models.CharField('Condición de egreso', max_length=150)

    class Meta:
        db_table = 'cat_condicion_egreso'
        verbose_name = 'Condición de egreso'
        verbose_name_plural = 'Condiciones de egreso'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class TalentoHumano(models.Model):
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name='talentos_humanos',
    )
    numero_documento = models.CharField('Número de documento', max_length=20)
    nombres = models.CharField('Nombres', max_length=120, blank=True)
    apellidos = models.CharField('Apellidos', max_length=120, blank=True)
    registro_rethus = models.CharField('Registro ReTHUS', max_length=20, blank=True)

    class Meta:
        db_table = 'cat_talento_humano'
        verbose_name = 'Talento humano en salud'
        verbose_name_plural = 'Talento humano en salud'
        ordering = ['apellidos', 'nombres']
        unique_together = [('tipo_documento', 'numero_documento')]

    def __str__(self):
        return f'{self.tipo_documento_id} {self.numero_documento}'
