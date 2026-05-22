# Guía de defensa técnica — HCE Salud y Vida

Documento para sustentación individual (30 mayo 2026).

## 1. Propósito del sistema

Registrar y consultar datos clínicos interoperables según el anexo técnico de la **Resolución 866/2021**, en dos alcances:

1. **Información del paciente** (identificación, residencia, etnia, ocupación CIUO-88, estructuras especiales).
2. **Contacto con el servicio de salud** orientado a **urgencias** (triage, diagnóstico CIE-10, tecnologías en salud).

## 2. Correcciones respecto al diagrama inicial

| Aspecto | Diagrama inicial | Implementación |
|---------|------------------|----------------|
| Oposición donación | FK invertida (`id_oposicion` → paciente) | `OneToOneField` Paciente → OposicionDonacion |
| Nacionalidad | Campo único en paciente | Tabla `PacienteNacionalidad` (N:M) |
| Discapacidad | Tabla intermedia correcta | `PacienteDiscapacidad` con FK a catálogo |
| Voluntad anticipada | OK como tabla separada | `ForeignKey` (historial de documentos) |
| Tecnologías | Polimorfismo confuso en un solo código | `TecnologiaSalud` + catálogos por tipo (CUPS, IUM, etc.) |
| Resultados | Mezcla de IDs | `ResultadoValoracion` OneToOne con `ContactoSalud` |

## 3. Regla >5 opciones vs choices

**Ejemplos choices (≤5):** sexo biológico (3), identidad de género (5), zona residencia (2), grupo servicios (5), entorno (5), triage (5), tipo diagnóstico (3).

**Ejemplos modelos (>5):** tipo documento (10+), modalidad tecnología (9), vía ingreso (14+), causa atención (49+), finalidad tecnología (34+), tipo tecnología salud (13).

## 4. Normalización

- Catálogos en **3FN**: sin redundancia de nombres de país, diagnóstico, etc.
- Datos transaccionales en `pacientes` y `atencion` referencian catálogos por FK.
- Tablas intermedias solo con claves foráneas + metadatos mínimos.

## 5. Django Admin

- **Personalización:** `site_header`, `site_title`, `index_title`, plantilla `admin/base_site.html`, CSS `admin_custom.css`.
- **Cada catálogo:** `list_display`, `search_fields`, `list_filter`, `fieldsets` donde aplica.
- **Paciente y ContactoSalud:** gestionados en portal web (CRUD), no en Admin (cumple etapa 2 y separación de responsabilidades en etapa 3).

## 6. Autenticación

- `LoginView` + `logout` + `LoginRequiredMixin` en vistas de pacientes y atención.
- Sesiones Django estándar; redirección a dashboard tras login.

## 7. Demostración en vivo (orden sugerido)

1. Login con superusuario.
2. Dashboard → listar pacientes → crear paciente con **dos nacionalidades** y **dos discapacidades**.
3. Registrar **oposición a donación** y **voluntad anticipada**.
4. Ir a atención → crear contacto urgencias con triage, diagnóstico CIE-10, tecnología.
5. Admin → mostrar catálogo diagnósticos o prestadores editado.

## 8. Preguntas frecuentes del evaluador

**¿Por qué MySQL?**  
Requisito del proyecto y estándar en IPS; UTF8MB4 para caracteres clínicos y nombres con tildes.

**¿Por qué no registrar Paciente en Admin?**  
La rúbrica etapa 2 lo excluye; en etapa 3 el CRUD funcional está en vistas dedicadas con mejor UX para datos sensibles.

**¿Cómo cumple la Res. 866?**  
Cada elemento del anexo (país nacionalidad, documento, triage, tecnologías, resultados) tiene modelo o choice alineado al código normativo.

**¿ForeignKey vs ManyToMany?**  
M2M solo donde la norma permite múltiples (nacionalidad, discapacidad). Resto FK por cardinalidad 1:N o 1:1.

## 9. Archivos clave para explicar código

- `apps/catalogos/models.py` — catálogos normativos
- `apps/pacientes/models.py` — paciente y estructuras separadas
- `apps/atencion/models.py` — contacto urgencias y tecnologías
- `core/choices.py` — dominios ≤5 valores
- `apps/catalogos/admin.py` — personalización Admin por modelo
