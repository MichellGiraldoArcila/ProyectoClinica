from django.contrib import admin

from apps.catalogos import models


class CatalogoAdmin(admin.ModelAdmin):
    list_per_page = 25


@admin.register(models.Pais)
class PaisAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')
    list_filter = ()
    fieldsets = ((None, {'fields': ('codigo', 'nombre')}),)


@admin.register(models.TipoDocumento)
class TipoDocumentoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.Ocupacion)
class OcupacionAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')
    list_filter = ()


@admin.register(models.Municipio)
class MunicipioAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre', 'departamento')
    search_fields = ('codigo', 'nombre', 'departamento')
    list_filter = ('departamento',)
    fieldsets = ((None, {'fields': ('codigo', 'nombre', 'departamento')}),)


@admin.register(models.Etnia)
class EtniaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.ComunidadEtnica)
class ComunidadEtnicaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre', 'etnia')
    search_fields = ('codigo', 'nombre')
    list_filter = ('etnia',)
    autocomplete_fields = ('etnia',)


@admin.register(models.Discapacidad)
class DiscapacidadAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.PrestadorSalud)
class PrestadorSaludAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre', 'es_administradora')
    search_fields = ('codigo', 'nombre')
    list_filter = ('es_administradora',)
    fieldsets = (
        ('Identificación', {'fields': ('codigo', 'nombre')}),
        ('Clasificación', {'fields': ('es_administradora',)}),
    )


@admin.register(models.ModalidadTecnologia)
class ModalidadTecnologiaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.ViaIngreso)
class ViaIngresoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.CausaAtencion)
class CausaAtencionAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.EnfermedadHuerfana)
class EnfermedadHuerfanaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.Diagnostico)
class DiagnosticoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre', 'enfermedad_huerfana')
    search_fields = ('codigo', 'nombre')
    list_filter = ('enfermedad_huerfana',)
    autocomplete_fields = ('enfermedad_huerfana',)
    fieldsets = (
        ('CIE-10', {'fields': ('codigo', 'nombre')}),
        ('Enfermedad huérfana', {'fields': ('enfermedad_huerfana',), 'classes': ('collapse',)}),
    )


@admin.register(models.TipoTecnologiaSalud)
class TipoTecnologiaSaludAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.FinalidadTecnologia)
class FinalidadTecnologiaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.Procedimiento)
class ProcedimientoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.MedicamentoConRegistro)
class MedicamentoConRegistroAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.MedicamentoVital)
class MedicamentoVitalAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.PreparacionMagistral)
class PreparacionMagistralAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.MedicamentoSinRegistro)
class MedicamentoSinRegistroAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.DispositivoMedico)
class DispositivoMedicoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.ComponenteSanguineo)
class ComponenteSanguineoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.FluidoOrganico)
class FluidoOrganicoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.Organo)
class OrganoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.Tejido)
class TejidoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.Celula)
class CelulaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.ProductoNutricional)
class ProductoNutricionalAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.ServicioComplementario)
class ServicioComplementarioAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.DescripcionMedicamento)
class DescripcionMedicamentoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')


@admin.register(models.UnidadMedida)
class UnidadMedidaAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre', 'tipo_unidad')
    search_fields = ('codigo', 'nombre')
    list_filter = ('tipo_unidad',)


@admin.register(models.ViaAdministracion)
class ViaAdministracionAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.UnidadTiempo)
class UnidadTiempoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.InstrumentoMedicion)
class InstrumentoMedicionAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.ParametroResultado)
class ParametroResultadoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.CondicionEgreso)
class CondicionEgresoAdmin(CatalogoAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(models.TalentoHumano)
class TalentoHumanoAdmin(CatalogoAdmin):
    list_display = ('tipo_documento', 'numero_documento', 'nombres', 'apellidos', 'registro_rethus')
    search_fields = ('numero_documento', 'nombres', 'apellidos', 'registro_rethus')
    list_filter = ('tipo_documento',)
    autocomplete_fields = ('tipo_documento',)
    fieldsets = (
        ('Identificación', {'fields': ('tipo_documento', 'numero_documento', 'registro_rethus')}),
        ('Datos personales', {'fields': ('nombres', 'apellidos')}),
    )
