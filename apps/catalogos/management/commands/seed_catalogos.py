"""
Carga catálogos base conforme Resolución 866/2021.
Ejecutar: python manage.py seed_catalogos
"""
from django.core.management.base import BaseCommand

from apps.catalogos.models import (
    CausaAtencion,
    CondicionEgreso,
    Diagnostico,
    Discapacidad,
    Etnia,
    FinalidadTecnologia,
    ModalidadTecnologia,
    Municipio,
    Ocupacion,
    Pais,
    PrestadorSalud,
    TipoDocumento,
    TipoTecnologiaSalud,
    UnidadTiempo,
    ViaIngreso,
)


class Command(BaseCommand):
    help = 'Carga datos iniciales de catálogos normativos'

    def handle(self, *args, **options):
        self._tipos_documento()
        self._paises()
        self._discapacidades()
        self._etnias()
        self._municipios()
        self._ocupaciones()
        self._prestadores()
        self._modalidades()
        self._vias_ingreso()
        self._causas()
        self._diagnosticos()
        self._tipos_tecnologia()
        self._finalidades()
        self._condiciones_egreso()
        self._unidades_tiempo()
        self.stdout.write(self.style.SUCCESS('Catálogos cargados correctamente.'))

    def _tipos_documento(self):
        datos = [
            ('CC', 'Cédula de ciudadanía'),
            ('CE', 'Cédula de extranjería'),
            ('TI', 'Tarjeta de identidad'),
            ('RC', 'Registro civil'),
            ('PA', 'Pasaporte'),
            ('PE', 'Permiso especial de permanencia'),
            ('CD', 'Carné diplomático'),
            ('SC', 'Salvoconducto'),
            ('PT', 'Permiso temporal'),
            ('DE', 'Documento extranjero'),
        ]
        for codigo, nombre in datos:
            TipoDocumento.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _paises(self):
        for codigo, nombre in [('170', 'Colombia'), ('840', 'Estados Unidos'), ('604', 'Perú')]:
            Pais.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _discapacidades(self):
        datos = [
            ('01', 'Discapacidad física'),
            ('02', 'Discapacidad visual'),
            ('03', 'Discapacidad auditiva'),
            ('04', 'Discapacidad intelectual'),
            ('05', 'Discapacidad psicosocial (mental)'),
            ('06', 'Sordoceguera'),
            ('07', 'Discapacidad múltiple'),
            ('08', 'Sin discapacidad'),
        ]
        for codigo, nombre in datos:
            Discapacidad.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _etnias(self):
        datos = [
            ('01', 'Indígena'),
            ('02', 'ROM (Gitanos)'),
            ('03', 'Raizal'),
            ('04', 'Palenquero'),
            ('05', 'Negro/Afrocolombiano'),
            ('06', 'Ninguna de las anteriores'),
        ]
        for codigo, nombre in datos:
            Etnia.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _municipios(self):
        datos = [
            ('05001', 'Medellín', 'Antioquia'),
            ('11001', 'Bogotá D.C.', 'Cundinamarca'),
            ('76001', 'Cali', 'Valle del Cauca'),
        ]
        for codigo, nombre, depto in datos:
            Municipio.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'departamento': depto},
            )

    def _ocupaciones(self):
        Ocupacion.objects.update_or_create(
            codigo='1111',
            defaults={'nombre': 'Miembros del poder ejecutivo'},
        )

    def _prestadores(self):
        PrestadorSalud.objects.update_or_create(
            codigo='123456789012',
            defaults={
                'nombre': 'IPS Salud y Vida',
                'es_administradora': False,
            },
        )
        PrestadorSalud.objects.update_or_create(
            codigo='987654321098',
            defaults={
                'nombre': 'EPS Salud Integral (ficticia)',
                'es_administradora': True,
            },
        )

    def _modalidades(self):
        datos = [
            ('01', 'Intramural'),
            ('02', 'Extramural unidad móvil'),
            ('03', 'Extramural domiciliaria'),
            ('04', 'Extramural jornada de salud'),
            ('05', 'Extramural atención prehospitalaria'),
            ('06', 'Telemedicina interactiva'),
            ('07', 'Telemedicina no interactiva'),
            ('08', 'Telemedicina telexperticia'),
            ('09', 'Telemedicina telemonitoreo'),
        ]
        for codigo, nombre in datos:
            ModalidadTecnologia.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _vias_ingreso(self):
        datos = [
            ('01', 'Demanda espontánea'),
            ('02', 'Derivado de consulta externa'),
            ('03', 'Derivado de urgencias'),
            ('04', 'Derivado de hospitalización'),
            ('07', 'Recién nacido en la institución'),
            ('13', 'Referido de otra institución'),
        ]
        for codigo, nombre in datos:
            ViaIngreso.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _causas(self):
        datos = [
            ('21', 'Accidente de trabajo'),
            ('23', 'Accidente de tránsito de origen común'),
            ('38', 'Enfermedad general'),
            ('39', 'Enfermedad laboral'),
            ('49', 'Riesgo ambiental'),
        ]
        for codigo, nombre in datos:
            CausaAtencion.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _diagnosticos(self):
        datos = [
            ('J069', 'Infección aguda de vías respiratorias superiores'),
            ('I10', 'Hipertensión esencial (primaria)'),
            ('S060', 'Conmoción cerebral'),
        ]
        for codigo, nombre in datos:
            Diagnostico.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _tipos_tecnologia(self):
        datos = [
            ('01', 'Procedimiento'),
            ('02', 'Medicamento con registro sanitario'),
            ('03', 'Medicamento vital no disponible'),
            ('04', 'Preparación magistral'),
            ('05', 'Medicamento sin registro (UNIRS)'),
            ('06', 'Dispositivo médico'),
            ('07', 'Componentes sanguíneos'),
            ('08', 'Fluidos orgánicos'),
            ('09', 'Órganos'),
            ('10', 'Tejidos'),
            ('11', 'Células'),
            ('12', 'Producto nutricional'),
            ('13', 'Servicio complementario'),
        ]
        for codigo, nombre in datos:
            TipoTecnologiaSalud.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _finalidades(self):
        for codigo, nombre in [
            ('15', 'Diagnóstico'),
            ('16', 'Tratamiento'),
            ('17', 'Rehabilitación'),
            ('18', 'Paliación'),
        ]:
            FinalidadTecnologia.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _condiciones_egreso(self):
        datos = [
            ('01', 'Paciente con destino a domicilio'),
            ('02', 'Paciente muerto'),
            ('03', 'Paciente hospitalizado'),
            ('04', 'Referido a otra institución'),
        ]
        for codigo, nombre in datos:
            CondicionEgreso.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})

    def _unidades_tiempo(self):
        for codigo, nombre in [
            ('1', 'Minutos'),
            ('2', 'Horas'),
            ('3', 'Día'),
            ('4', 'Semana'),
            ('5', 'Mes'),
            ('6', 'Año'),
        ]:
            UnidadTiempo.objects.update_or_create(codigo=codigo, defaults={'nombre': nombre})
