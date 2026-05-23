"""
Carga inicial de catálogos — Resolución 866/2021.
Uso: python manage.py seed_catalogos
"""
from django.core.management.base import BaseCommand

from apps.catalogos.models import (
    CausaAtencion,
    Celula,
    ComponenteSanguineo,
    ComunidadEtnica,
    CondicionEgreso,
    DescripcionMedicamento,
    Diagnostico,
    Discapacidad,
    DispositivoMedico,
    EnfermedadHuerfana,
    Etnia,
    FinalidadTecnologia,
    FluidoOrganico,
    InstrumentoMedicion,
    MedicamentoConRegistro,
    MedicamentoSinRegistro,
    MedicamentoVital,
    ModalidadTecnologia,
    Municipio,
    NivelCIUO,
    Ocupacion,
    Organo,
    Pais,
    ParametroResultado,
    PreparacionMagistral,
    PrestadorSalud,
    Procedimiento,
    ProductoNutricional,
    ServicioComplementario,
    TalentoHumano,
    Tejido,
    TipoDocumento,
    TipoTecnologiaSalud,
    UnidadMedida,
    UnidadTiempo,
    ViaAdministracion,
    ViaIngreso,
)


class Command(BaseCommand):
    help = 'Carga catálogos normativos y datos de referencia del sistema'

    def handle(self, *args, **options):
        self._tipos_documento()
        self._paises()
        self._discapacidades()
        self._etnias()
        self._comunidades()
        self._municipios()
        self._ocupaciones_ciuo88()
        self._prestadores()
        self._modalidades()
        self._vias_ingreso()
        self._causas()
        self._enfermedades_huerfanas()
        self._diagnosticos()
        self._tipos_tecnologia()
        self._finalidades()
        self._procedimientos()
        self._medicamentos()
        self._dispositivos_y_biologicos()
        self._descripciones_medicamento()
        self._unidades_y_vias()
        self._instrumentos_y_parametros()
        self._condiciones_egreso()
        self._unidades_tiempo()
        self._talento_humano()
        self.stdout.write(self.style.SUCCESS('Catálogos actualizados.'))

    def _cargar(self, modelo, datos, campo_codigo='codigo', campo_nombre='nombre'):
        for item in datos:
            codigo = item[0]
            nombre = item[1]
            extra = item[2] if len(item) > 2 else {}
            modelo.objects.update_or_create(
                **{campo_codigo: codigo},
                defaults={campo_nombre: nombre, **extra},
            )

    def _tipos_documento(self):
        self._cargar(TipoDocumento, [
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
        ])

    def _paises(self):
        self._cargar(Pais, [
            ('170', 'Colombia'),
            ('862', 'Venezuela'),
            ('604', 'Perú'),
            ('218', 'Ecuador'),
            ('152', 'Chile'),
            ('076', 'Brasil'),
            ('484', 'México'),
            ('840', 'Estados Unidos'),
            ('724', 'España'),
            ('032', 'Argentina'),
            ('591', 'Panamá'),
        ])

    def _discapacidades(self):
        self._cargar(Discapacidad, [
            ('01', 'Discapacidad física'),
            ('02', 'Discapacidad visual'),
            ('03', 'Discapacidad auditiva'),
            ('04', 'Discapacidad intelectual'),
            ('05', 'Discapacidad psicosocial (mental)'),
            ('06', 'Sordoceguera'),
            ('07', 'Discapacidad múltiple'),
            ('08', 'Sin discapacidad'),
        ])

    def _etnias(self):
        self._cargar(Etnia, [
            ('01', 'Indígena'),
            ('02', 'ROM (Gitanos)'),
            ('03', 'Raizal'),
            ('04', 'Palenquero'),
            ('05', 'Negro/Afrocolombiano'),
            ('06', 'Ninguna de las anteriores'),
        ])

    def _comunidades(self):
        etnia_indigena = Etnia.objects.filter(codigo='01').first()
        datos = [
            ('001', 'Comunidad Emberá', {'etnia': etnia_indigena}),
            ('002', 'Comunidad Wayuu', {'etnia': etnia_indigena}),
            ('003', 'Comunidad Nasa', {'etnia': etnia_indigena}),
            ('004', 'Comunidad ROM Bogotá', {'etnia': Etnia.objects.filter(codigo='02').first()}),
        ]
        for codigo, nombre, extra in datos:
            ComunidadEtnica.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, **extra},
            )

    def _municipios(self):
        self._cargar(Municipio, [
            ('05001', 'Medellín', {'departamento': 'Antioquia'}),
            ('11001', 'Bogotá D.C.', {'departamento': 'Cundinamarca'}),
            ('76001', 'Cali', {'departamento': 'Valle del Cauca'}),
            ('08001', 'Barranquilla', {'departamento': 'Atlántico'}),
            ('13001', 'Cartagena', {'departamento': 'Bolívar'}),
            ('68001', 'Bucaramanga', {'departamento': 'Santander'}),
            ('47001', 'Santa Marta', {'departamento': 'Magdalena'}),
            ('50001', 'Villavicencio', {'departamento': 'Meta'}),
        ])

    def _ocupaciones_ciuo88(self):
        gran_grupos = [
            ('0', 'Fuerzas militares'),
            ('1', 'Directores y gerentes'),
            ('2', 'Profesionales científicos e intelectuales'),
            ('3', 'Técnicos y profesionales de nivel medio'),
            ('4', 'Empleados de oficina'),
            ('5', 'Trabajadores de los servicios y vendedores'),
            ('6', 'Agricultores y trabajadores calificados agropecuarios'),
            ('7', 'Oficiales, operarios y artesanos'),
            ('8', 'Operadores de instalaciones y máquinas'),
            ('9', 'Ocupaciones elementales'),
        ]
        for codigo, nombre in gran_grupos:
            Ocupacion.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'nivel': NivelCIUO.GRAN_GRUPO, 'padre': None},
            )

        g2 = Ocupacion.objects.get(codigo='2')
        nodos = [
            ('22', g2, 'Profesionales de la salud', NivelCIUO.SUBGRUPO),
        ]
        for codigo, padre, nombre, nivel in nodos:
            Ocupacion.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'nivel': nivel, 'padre': padre},
            )
        p22 = Ocupacion.objects.get(codigo='22')
        for codigo, nombre, nivel in [
            ('221', 'Médicos', NivelCIUO.GRUPO_PRIMARIO),
            ('222', 'Profesionales de enfermería', NivelCIUO.GRUPO_PRIMARIO),
            ('226', 'Profesionales de la salud (otros)', NivelCIUO.GRUPO_PRIMARIO),
        ]:
            Ocupacion.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'nivel': nivel, 'padre': p22},
            )
        ocupaciones = [
            ('2211', '221', 'Médicos generales'),
            ('2212', '221', 'Médicos especialistas'),
            ('2221', '222', 'Profesionales de enfermería'),
            ('2261', '226', 'Odontólogos'),
            ('2262', '226', 'Farmacéuticos'),
            ('2264', '226', 'Fisioterapeutas'),
        ]
        for codigo, padre_codigo, nombre in ocupaciones:
            padre = Ocupacion.objects.get(codigo=padre_codigo)
            Ocupacion.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'nivel': NivelCIUO.OCUPACION, 'padre': padre},
            )

        Ocupacion.objects.update_or_create(
            codigo='9999',
            defaults={'nombre': 'Otra (especificar)', 'nivel': NivelCIUO.OCUPACION, 'padre': None},
        )

    def _prestadores(self):
        """EPS e IPS con códigos de 12 dígitos (formato SGSSS/REPS)."""
        prestadores = [
            ('800088702002', 'EPS SURA', True),
            ('800251440001', 'EPS Sanitas', True),
            ('900156264000', 'Nueva EPS', True),
            ('890303797001', 'EPS Compensar', True),
            ('890901826001', 'Hospital Pablo Tobón Uribe', False),
            ('890303842001', 'Fundación Valle del Lili', False),
            ('860015330001', 'Cruz Roja Seccional Bogotá', False),
            ('890102768001', 'Hospital San Vicente Fundación', False),
            ('890903211001', 'IPS Salud y Vida', False),
        ]
        for codigo, nombre, es_admin in prestadores:
            PrestadorSalud.objects.update_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'es_administradora': es_admin},
            )
        # Registro legado: se renombra sin borrar (puede estar referenciado por pacientes).
        PrestadorSalud.objects.filter(codigo='987654321098').update(
            nombre='Nueva EPS',
            es_administradora=True,
        )

    def _modalidades(self):
        self._cargar(ModalidadTecnologia, [
            ('01', 'Intramural'),
            ('02', 'Extramural unidad móvil'),
            ('03', 'Extramural domiciliaria'),
            ('04', 'Extramural jornada de salud'),
            ('05', 'Extramural atención prehospitalaria'),
            ('06', 'Telemedicina interactiva'),
            ('07', 'Telemedicina no interactiva'),
            ('08', 'Telemedicina telexperticia'),
            ('09', 'Telemedicina telemonitoreo'),
        ])

    def _vias_ingreso(self):
        self._cargar(ViaIngreso, [
            ('01', 'Demanda espontánea'),
            ('02', 'Derivado de consulta externa'),
            ('03', 'Derivado de urgencias'),
            ('04', 'Derivado de hospitalización'),
            ('07', 'Recién nacido en la institución'),
            ('13', 'Referido de otra institución'),
            ('14', 'Contra referido de otra institución'),
        ])

    def _causas(self):
        self._cargar(CausaAtencion, [
            ('21', 'Accidente de trabajo'),
            ('23', 'Accidente de tránsito de origen común'),
            ('38', 'Enfermedad general'),
            ('39', 'Enfermedad laboral'),
            ('26', 'Otro tipo de accidente'),
            ('28', 'Lesión por agresión'),
            ('49', 'Riesgo ambiental'),
        ])

    def _enfermedades_huerfanas(self):
        self._cargar(EnfermedadHuerfana, [
            ('E001', 'Fibrosis quística'),
            ('E002', 'Esclerosis lateral amiotrófica'),
            ('E003', 'Enfermedad de Gaucher'),
            ('E004', 'Histiocitosis'),
        ])

    def _diagnosticos(self):
        self._cargar(Diagnostico, [
            ('J069', 'Infección aguda de vías respiratorias superiores'),
            ('I10', 'Hipertensión esencial (primaria)'),
            ('E11', 'Diabetes mellitus tipo 2'),
            ('J189', 'Neumonía no especificada'),
            ('S060', 'Conmoción cerebral'),
            ('K029', 'Caries dental'),
            ('Z000', 'Examen médico general'),
            ('R509', 'Fiebre no especificada'),
        ])

    def _tipos_tecnologia(self):
        self._cargar(TipoTecnologiaSalud, [
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
        ])

    def _finalidades(self):
        self._cargar(FinalidadTecnologia, [
            ('11', 'Valoración integral promoción y mantenimiento'),
            ('15', 'Diagnóstico'),
            ('16', 'Tratamiento'),
            ('17', 'Rehabilitación'),
            ('18', 'Paliación'),
            ('19', 'Planificación familiar y anticoncepción'),
            ('21', 'Atención básica de orientación familiar'),
            ('38', 'Promoción del empoderamiento en salud'),
        ])

    def _procedimientos(self):
        self._cargar(Procedimiento, [
            ('890201', 'Consulta de primera vez por medicina general'),
            ('890266', 'Consulta de control o seguimiento'),
            ('902210', 'Radiografía de tórax PA'),
            ('902211', 'Radiografía de tórax (PA y lateral)'),
            ('930401', 'Terapia física integral'),
            ('911002', 'Hemograma IV (hemoglobina, hematocrito)'),
        ])

    def _medicamentos(self):
        self._cargar(MedicamentoConRegistro, [
            ('19961745-01', 'Acetaminofén 500 mg tableta'),
            ('19961829-01', 'Ibuprofeno 400 mg tableta'),
            ('19959310-01', 'Amoxicilina 500 mg cápsula'),
            ('19967794-01', 'Losartán 50 mg tableta'),
        ])
        self._cargar(MedicamentoVital, [
            ('19959310-02', 'Amoxicilina (vital no disponible)'),
            ('19967794-02', 'Losartán (vital no disponible)'),
            ('19961745-02', 'Acetaminofén (vital no disponible)'),
        ])
        self._cargar(PreparacionMagistral, [
            ('MAG001', 'Suspensión pediátrica magistral'),
            ('MAG002', 'Crema dermatológica magistral'),
            ('MAG003', 'Solución oral magistral'),
        ])
        self._cargar(MedicamentoSinRegistro, [
            ('UNIRS01', 'Medicamento UNIRS 01'),
            ('UNIRS02', 'Medicamento UNIRS 02'),
            ('UNIRS03', 'Medicamento UNIRS 03'),
        ])

    def _dispositivos_y_biologicos(self):
        self._cargar(DispositivoMedico, [
            ('DM001', 'Tensiómetro digital'),
            ('DM002', 'Glucometro'),
            ('DM003', 'Nebulizador'),
            ('DM004', 'Oxímetro de pulso'),
        ])
        self._cargar(ComponenteSanguineo, [
            ('CS001', 'Glóbulos rojos concentrados'),
            ('CS002', 'Plasma fresco congelado'),
            ('CS003', 'Plaquetas'),
        ])
        self._cargar(FluidoOrganico, [
            ('FO001', 'Sangre total'),
            ('FO002', 'Plasma'),
            ('FO003', 'Suero salino'),
        ])
        self._cargar(Organo, [
            ('OR001', 'Riñón'),
            ('OR002', 'Hígado'),
            ('OR003', 'Córnea'),
        ])
        self._cargar(Tejido, [
            ('TE001', 'Piel'),
            ('TE002', 'Cartílago'),
            ('TE003', 'Hueso'),
        ])
        self._cargar(Celula, [
            ('CE001', 'Células madre hematopoyéticas'),
            ('CE002', 'Linfocitos'),
            ('CE003', 'Células mesenquimales'),
        ])
        self._cargar(ProductoNutricional, [
            ('PN001', 'Fórmula enteral estándar'),
            ('PN002', 'Suplemento proteico'),
            ('PN003', 'Nutrición parenteral'),
        ])
        self._cargar(ServicioComplementario, [
            ('SC001', 'Transporte asistencial básico'),
            ('SC002', 'Acompañamiento hospitalario'),
            ('SC003', 'Terapia respiratoria domiciliaria'),
        ])

    def _descripciones_medicamento(self):
        self._cargar(DescripcionMedicamento, [
            ('N02B', 'Paracetamol'),
            ('M01A', 'Ibuprofeno'),
            ('J01C', 'Penicilinas'),
            ('C09C', 'Inhibidores de la enzima convertidora de angiotensina'),
        ], campo_nombre='descripcion')

    def _unidades_y_vias(self):
        self._cargar(UnidadMedida, [
            ('mg', 'Miligramo', {'tipo_unidad': 'Masa'}),
            ('mL', 'Mililitro', {'tipo_unidad': 'Volumen'}),
            ('UI', 'Unidad internacional', {'tipo_unidad': 'Biologica'}),
            ('tab', 'Tableta', {'tipo_unidad': 'Farmaceutica'}),
        ])
        self._cargar(ViaAdministracion, [
            ('VO', 'Vía oral'),
            ('IV', 'Vía intravenosa'),
            ('IM', 'Vía intramuscular'),
            ('SC', 'Vía subcutánea'),
        ])

    def _instrumentos_y_parametros(self):
        self._cargar(InstrumentoMedicion, [
            ('GLU', 'Glucometría'),
            ('TAM', 'Tensión arterial'),
            ('SAT', 'Saturación de oxígeno'),
            ('TAX', 'Triage de Manchester'),
        ])
        self._cargar(ParametroResultado, [
            ('01', 'Glucosa en sangre'),
            ('02', 'Presión arterial sistólica'),
            ('03', 'Presión arterial diastólica'),
            ('04', 'Frecuencia cardíaca'),
        ])

    def _condiciones_egreso(self):
        self._cargar(CondicionEgreso, [
            ('01', 'Paciente con destino a domicilio'),
            ('02', 'Paciente muerto'),
            ('03', 'Paciente hospitalizado'),
            ('04', 'Referido a otra institución'),
            ('05', 'Contra referido a otra institución'),
            ('06', 'Derivado a hospitalización domiciliaria'),
            ('07', 'Canalizado a servicio social'),
        ])

    def _unidades_tiempo(self):
        self._cargar(UnidadTiempo, [
            ('1', 'Minutos'),
            ('2', 'Horas'),
            ('3', 'Día'),
            ('4', 'Semana'),
            ('5', 'Mes'),
            ('6', 'Año'),
        ])

    def _talento_humano(self):
        cc = TipoDocumento.objects.get(codigo='CC')
        profesionales = [
            ('52345678', 'Laura', 'Gómez Pérez', 'RETHUS-10001'),
            ('98765432', 'Carlos', 'Rodríguez Mesa', 'RETHUS-10002'),
            ('43123456', 'Diana', 'Torres López', 'RETHUS-10003'),
            ('80234567', 'Andrés', 'Vélez García', 'RETHUS-10004'),
        ]
        for documento, nombres, apellidos, rethus in profesionales:
            TalentoHumano.objects.update_or_create(
                tipo_documento=cc,
                numero_documento=documento,
                defaults={
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'registro_rethus': rethus,
                },
            )
