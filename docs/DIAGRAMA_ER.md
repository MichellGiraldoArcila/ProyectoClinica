# Modelo Entidad-Relación — HCE Salud y Vida

Diagrama alineado con Resolución 866/2021 (alcance implementado).

```mermaid
erDiagram
    PAIS ||--o{ PACIENTE_NACIONALIDAD : tiene
    PACIENTE ||--o{ PACIENTE_NACIONALIDAD : tiene
    TIPO_DOCUMENTO ||--o{ PACIENTE : identifica
    MUNICIPIO ||--o{ PACIENTE : reside
    PAIS ||--o{ PACIENTE : residencia
    OCUPACION ||--o{ PACIENTE : ejerce
    ETNIA ||--o{ PACIENTE : pertenece
    PRESTADOR ||--o{ PACIENTE : afilia
    PACIENTE ||--o| OPOSICION_DONACION : registra
    PACIENTE ||--o{ VOLUNTAD_ANTICIPADA : documenta
    PACIENTE ||--o{ PACIENTE_DISCAPACIDAD : presenta
    DISCAPACIDAD ||--o{ PACIENTE_DISCAPACIDAD : cataloga

    PACIENTE ||--o{ CONTACTO_SALUD : atiende
    PRESTADOR ||--o{ CONTACTO_SALUD : presta
    MODALIDAD ||--o{ CONTACTO_SALUD : usa
    VIA_INGRESO ||--o{ CONTACTO_SALUD : ingresa
    CAUSA ||--o{ CONTACTO_SALUD : motiva
    DIAGNOSTICO ||--o{ CONTACTO_SALUD : diagnostica
    CONTACTO_SALUD ||--o{ TECNOLOGIA_SALUD : aplica
    CONTACTO_SALUD ||--o| RESULTADO_VALORACION : cierra
    TIPO_TECNOLOGIA ||--o{ TECNOLOGIA_SALUD : clasifica
```

## Entidades principales

- **PACIENTE**: núcleo de identificación y residencia.
- **PACIENTE_NACIONALIDAD**: cardinalidad N:M país–paciente.
- **OPOSICION_DONACION**: 1:1 con paciente (Ley 1805/2016).
- **CONTACTO_SALUD**: evento de atención (urgencias).
- **TECNOLOGIA_SALUD**: procedimientos, medicamentos, dispositivos, etc.
- **RESULTADO_VALORACION**: egreso, complicaciones, condición destino.

## Catálogos (tablas de referencia)

País, TipoDocumento, Municipio (DIVIPOLA), Diagnóstico (CIE-10), ModalidadTecnologia, ViaIngreso, CausaAtencion, TipoTecnologiaSalud, FinalidadTecnologia, PrestadorSalud, entre otros.
