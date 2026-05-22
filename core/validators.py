import re

from django.core.exceptions import ValidationError


def validar_codigo_iso_pais(value):
    if not re.fullmatch(r'[A-Z0-9]{3}', value or ''):
        raise ValidationError('El código de país debe tener 3 caracteres alfanuméricos (ISO 3166).')


def validar_codigo_municipio(value):
    if not re.fullmatch(r'\d{5}', value or ''):
        raise ValidationError('El código de municipio DIVIPOLA debe tener 5 dígitos.')


def validar_codigo_prestador(value):
    if value and not re.fullmatch(r'\d{12}', value):
        raise ValidationError('El código de prestador debe tener 12 dígitos numéricos.')
