"""Choices normativos Resolución 866/2021 (≤5 opciones)."""
from django.db import models


class SexoBiologico(models.TextChoices):
    HOMBRE = '01', 'Hombre'
    MUJER = '02', 'Mujer'
    INDETERMINADO = '03', 'Indeterminado o Intersexual'


class IdentidadGenero(models.TextChoices):
    MASCULINO = '01', 'Masculino'
    FEMENINO = '02', 'Femenino'
    TRANSGENERO = '03', 'Transgénero'
    NEUTRO = '04', 'Neutro'
    NO_DECLARA = '05', 'No lo declara'


class ZonaResidencia(models.TextChoices):
    URBANA = '01', 'Urbana'
    RURAL = '02', 'Rural'


class SiNo(models.TextChoices):
    SI = '01', 'Sí'
    NO = '02', 'No'


class GrupoServicios(models.TextChoices):
    CONSULTA_EXTERNA = '01', 'Consulta externa'
    APOYO = '02', 'Apoyo diagnóstico y complementación terapéutica'
    INTERNACION = '03', 'Internación'
    QUIRURGICO = '04', 'Quirúrgico'
    ATENCION_INMEDIATA = '05', 'Atención inmediata'


class EntornoAtencion(models.TextChoices):
    HOGAR = '01', 'Hogar'
    COMUNITARIO = '02', 'Comunitario'
    ESCOLAR = '03', 'Escolar'
    LABORAL = '04', 'Laboral'
    INSTITUCIONAL = '05', 'Institucional'


class ClasificacionTriage(models.TextChoices):
    TRIAGE_I = '01', 'Triage I'
    TRIAGE_II = '02', 'Triage II'
    TRIAGE_III = '03', 'Triage III'
    TRIAGE_IV = '04', 'Triage IV'
    TRIAGE_V = '05', 'Triage V'


class TipoDiagnostico(models.TextChoices):
    IMPRESION = '01', 'Impresión diagnóstica'
    CONFIRMADO_NUEVO = '02', 'Confirmado nuevo'
    CONFIRMADO_REPETIDO = '03', 'Confirmado repetido'


class AlcanceIncapacidad(models.TextChoices):
    NUEVA = '01', 'Nueva'
    PRORROGA = '02', 'Prórroga'


class Parentesco(models.TextChoices):
    PADRES = '01', 'Padres'
    HERMANOS = '02', 'Hermanos'
    TIOS = '03', 'Tíos'
    ABUELOS = '04', 'Abuelos'


class TipoAlergia(models.TextChoices):
    MEDICAMENTO = '01', 'Medicamento'
    ALIMENTO = '02', 'Alimento'
    SUSTANCIA_AMBIENTE = '03', 'Sustancia del ambiente'
    SUSTANCIA_PIEL = '04', 'Sustancia que entra en contacto con la piel'
    PICADURA = '05', 'Picadura de insectos'


class TipoFactorRiesgo(models.TextChoices):
    QUIMICOS = '01', 'Químicos'
    FISICOS = '02', 'Físicos'
    BIOMECANICOS = '03', 'Biomecánicos'
    PSICOSOCIALES = '04', 'Psicosociales'
    BIOLOGICOS = '05', 'Biológicos'
