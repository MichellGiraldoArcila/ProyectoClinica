from django.contrib import admin

from apps.pacientes.models import PacienteDiscapacidad, PacienteNacionalidad


@admin.register(PacienteNacionalidad)
class PacienteNacionalidadAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'pais', 'codigo_pais', 'nombre_pais')
    list_filter = ('pais',)
    search_fields = (
        'paciente__numero_documento',
        'paciente__primer_nombre',
        'paciente__primer_apellido',
        'pais__nombre',
        'pais__codigo',
    )
    raw_id_fields = ('paciente',)
    autocomplete_fields = ('pais',)
    fieldsets = (
        (
            'País de la nacionalidad (Res. 866/2021)',
            {
                'fields': ('paciente', 'pais'),
                'description': (
                    'Estructura para múltiples países de nacionalidad por paciente. '
                    'Código ISO 3166 y nombre del país según catálogo País.'
                ),
            },
        ),
    )

    @admin.display(description='Código país (ISO 3166)')
    def codigo_pais(self, obj):
        return obj.pais_id

    @admin.display(description='Nombre del país de nacionalidad')
    def nombre_pais(self, obj):
        return obj.pais.nombre


@admin.register(PacienteDiscapacidad)
class PacienteDiscapacidadAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'discapacidad')
    search_fields = ('paciente__numero_documento',)
    raw_id_fields = ('paciente',)
    autocomplete_fields = ('discapacidad',)
