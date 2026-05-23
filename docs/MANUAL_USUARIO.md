# Manual de Usuario
## Sistema de Historia Clínica Electrónica (HCE)
### IPS Salud y Vida — Resolución 866 de 2021

**Versión:** 1.0  
**Fecha:** Mayo 2026  
**Público:** Equipo de trabajo, docentes y evaluadores  

---

## Tabla de contenido

1. [Introducción](#1-introducción)
2. [Requisitos del sistema](#2-requisitos-del-sistema)
3. [Instalación paso a paso](#3-instalación-paso-a-paso)
4. [Primer acceso al sistema](#4-primer-acceso-al-sistema)
5. [Panel principal (Dashboard)](#5-panel-principal-dashboard)
6. [Módulo de pacientes](#6-módulo-de-pacientes)
7. [Módulo de contacto con el servicio de salud](#7-módulo-de-contacto-con-el-servicio-de-salud)
8. [Panel de administración (catálogos)](#8-panel-de-administración-catálogos)
9. [Guía para sustentación y explicación del proyecto](#9-guía-para-sustentación-y-explicación-del-proyecto)
10. [Preguntas frecuentes y solución de problemas](#10-preguntas-frecuentes-y-solución-de-problemas)
11. [Glosario de términos](#11-glosario-de-términos)

---

## 1. Introducción

### 1.1 ¿Qué es este sistema?

Es una aplicación web desarrollada con **Django** que permite a la **IPS Salud y Vida** gestionar información clínica de pacientes conforme a la **Resolución 866 de 2021** del Ministerio de Salud de Colombia.

El sistema cubre dos módulos principales exigidos en el proyecto académico:

| Módulo | Descripción |
|--------|-------------|
| **Gestión de pacientes** | Registrar, consultar y actualizar datos del paciente |
| **Contacto con el servicio de salud** | Registrar atenciones en urgencias (triage, diagnóstico, tecnologías) |

Además incluye:

- **Autenticación** (registro, inicio y cierre de sesión)
- **Catálogos normativos** administrables desde Django Admin
- **Interfaz web** con Bootstrap 5

### 1.2 ¿Para quién es este manual?

- Integrantes del equipo que van a **usar** el sistema
- Quienes van a **sustentar** el proyecto ante el docente
- Personas que necesitan **instalar** el proyecto en otro computador

### 1.3 Marco normativo

Los datos del sistema siguen el **anexo técnico** de la Resolución 866/2021, por ejemplo:

- Identificación del paciente (tipo y número de documento, nombres, sexo, identidad de género)
- Nacionalidades múltiples
- Discapacidades múltiples
- Oposición a donación (estructura separada)
- Voluntad anticipada (estructura separada)
- Contacto en urgencias: modalidad, vía de ingreso, causa, triage, diagnóstico CIE-10, tecnologías en salud

---

## 2. Requisitos del sistema

### 2.1 Software necesario

| Componente | Versión mínima |
|------------|----------------|
| Python | 3.12 o superior |
| Django | 5.0 o superior |
| Base de datos | MySQL 8+ (producción) o SQLite (pruebas locales) |
| Navegador | Chrome, Edge o Firefox actualizado |

### 2.2 Conocimientos recomendados

- Uso básico de navegador web
- Para instalación: línea de comandos (PowerShell o terminal)
- Para administración de catálogos: conceptos básicos de formularios web

### 2.3 Estructura del repositorio

```
ProyectoClinica/
├── apps/
│   ├── catalogos/    → Tablas de referencia (países, diagnósticos, etc.)
│   ├── pacientes/    → CRUD de pacientes
│   ├── atencion/     → CRUD de urgencias / contacto salud
│   └── cuentas/      → Login, registro, dashboard
├── templates/        → Pantallas HTML
├── static/           → Estilos CSS
├── docs/             → Documentación (este manual)
├── manage.py         → Comandos Django
└── requirements.txt  → Dependencias Python
```

---

## 3. Instalación paso a paso

### 3.1 Descargar el proyecto

```bash
git clone https://github.com/MichellGiraldoArcila/ProyectoClinica.git
cd ProyectoClinica
```

### 3.2 Crear entorno virtual (recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3.4 Configurar variables de entorno

1. Copie el archivo de ejemplo:
   ```bash
   copy .env.example .env
   ```
   (En Linux: `cp .env.example .env`)

2. Edite `.env` según su entorno.

**Opción A — Desarrollo rápido (SQLite, sin instalar MySQL):**
```env
SECRET_KEY=clave-secreta-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=sqlite
```

**Opción B — MySQL (entrega académica / producción):**
```env
DB_ENGINE=mysql
DB_NAME=salud_vida_hce
DB_USER=root
DB_PASSWORD=su_contraseña
DB_HOST=127.0.0.1
DB_PORT=3306
```

En MySQL, cree la base de datos:
```sql
CREATE DATABASE salud_vida_hce
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 3.5 Preparar la base de datos

```bash
python manage.py migrate
python manage.py seed_catalogos
```

El comando `seed_catalogos` carga los catálogos iniciales: países, tipos de documento, municipios, diagnósticos, prestadores (EPS e IPS de Colombia), modalidades, medicamentos, procedimientos y demás tablas del administrador.

### 3.6 Crear usuario administrador (opcional)

Para acceder al panel `/admin/`:

```bash
python manage.py createsuperuser
```

Siga las instrucciones en pantalla (usuario, correo, contraseña).

> **Nota:** También puede registrarse desde la web en `/registro/` sin ser administrador.

### 3.7 Iniciar el servidor

```bash
python manage.py runserver
```

Abra el navegador en: **http://127.0.0.1:8000/**

---

## 4. Primer acceso al sistema

### 4.1 Registro de nuevo usuario

Si nadie ha creado una cuenta aún:

1. Vaya a **http://127.0.0.1:8000/login/**
2. Clic en **Registrarse**
3. Complete el formulario:
   - Usuario (único, sin espacios)
   - Nombres y apellidos (opcional)
   - Correo electrónico
   - Contraseña (mínimo 8 caracteres; no puede ser muy común)
   - Confirmar contraseña
4. Clic en **Registrarse**

El sistema inicia sesión automáticamente y lo lleva al panel principal.

### 4.2 Iniciar sesión

1. URL: **http://127.0.0.1:8000/login/**
2. Ingrese usuario y contraseña
3. Clic en **Ingresar**

### 4.3 Cerrar sesión

En la barra superior, clic en **Cerrar sesión**.

### 4.4 Rutas protegidas

Las secciones de pacientes y atención **requieren** estar autenticado. Si intenta entrar sin sesión, el sistema lo redirige al login.

---

## 5. Panel principal (Dashboard)

**URL:** http://127.0.0.1:8000/

Después de iniciar sesión verá tres bloques:

| Bloque | Acción |
|--------|--------|
| **Gestión de pacientes** | Ir a listado o crear paciente nuevo |
| **Contacto con el servicio de salud** | Ir a atenciones o registrar urgencia |
| **Catálogos normativos** | Abrir Django Admin |

La barra de navegación superior permite moverse entre **Pacientes**, **Atención urgencias** y **Administración**.

---

## 6. Módulo de pacientes

### 6.1 Listar pacientes

**URL:** http://127.0.0.1:8000/pacientes/

- Tabla con documento, nombre y municipio
- **Buscar:** escriba documento o nombre y clic en Buscar
- Acciones: **Ver** (detalle) | **Editar**

### 6.2 Registrar un paciente nuevo

**URL:** http://127.0.0.1:8000/pacientes/nuevo/

Complete las secciones del formulario:

#### A) Datos del paciente
| Campo | Descripción |
|-------|-------------|
| Tipo de documento | CC, TI, CE, etc. (catálogo) |
| Número de documento | Único por tipo |
| Primer / segundo nombre | Según documento de identidad |
| Primer / segundo apellido | Según documento |
| Fecha y hora de nacimiento | Formato fecha-hora del navegador |
| Sexo biológico | 01 Hombre, 02 Mujer, 03 Indeterminado |
| Identidad de género | Masculino, Femenino, Transgénero, etc. |
| Ocupación | Código CIUO-88 (catálogo) |
| País de residencia | ISO 3166 |
| Municipio | Código DIVIPOLA (5 dígitos) |
| Zona | Urbana o Rural |
| Etnia / Comunidad étnica | Opcional |
| Administradora del plan | EPS o entidad responsable |
| Prestador de vinculación | Opcional |

#### B) Nacionalidades (múltiples)
- Puede agregar **más de un país** de nacionalidad
- Use el selector de país en cada fila
- Si necesita otra nacionalidad, agregue otra fila (formulario dinámico)

#### C) Discapacidades (múltiples)
- Seleccione una o más categorías: física, visual, auditiva, etc.
- Código 08 = Sin discapacidad (si aplica)

#### D) Oposición a donación (estructura separada — Res. 866)
| Campo | Valores |
|-------|---------|
| Manifestación | 01 = Sí se opone / 02 = No |
| Fecha de registro | Fecha del documento |

#### E) Voluntad anticipada (estructura separada)
| Campo | Descripción |
|-------|-------------|
| ¿Tiene documento? | Sí / No |
| Fecha del documento | Si aplica |
| Prestador donde reposa | Entidad de salud |
| Observaciones | Texto libre |

4. Clic en **Guardar**

### 6.3 Consultar detalle de paciente

**URL:** `/pacientes/<id>/`

Muestra en tarjetas:
- Identificación y residencia
- Lista de nacionalidades
- Lista de discapacidades
- Oposición a donación
- Voluntades anticipadas registradas

### 6.4 Actualizar paciente

**URL:** `/pacientes/<id>/editar/`

Mismos campos que el registro. Modifique lo necesario y **Guardar**.

---

## 7. Módulo de contacto con el servicio de salud

Este módulo representa la **atención en urgencias** cuando el paciente contacta el servicio de salud.

### 7.1 Listar atenciones

**URL:** http://127.0.0.1:8000/atencion/

Columnas: fecha inicio, paciente, prestador, diagnóstico ingreso, triage.

### 7.2 Registrar nueva atención

**URL:** http://127.0.0.1:8000/atencion/nuevo/

#### Datos del contacto

| Campo | Descripción |
|-------|-------------|
| Paciente | Debe existir previamente en el sistema |
| Prestador | IPS que realiza la atención (código SGSSS) |
| Fecha y hora inicio | Momento de inicio de la atención |
| Modalidad | Intramural, extramural, telemedicina, etc. |
| Grupo de servicios | Consulta externa, internación, atención inmediata… |
| Entorno | Hogar, institucional, laboral, etc. |
| Vía de ingreso | Demanda espontánea, derivado de urgencias, etc. |
| Causa | Accidente, enfermedad general, etc. |
| Fecha y hora triage | Opcional |
| Clasificación triage | I a V |
| Diagnóstico de ingreso | Código CIE-10 |
| Tipo diagnóstico | Impresión / Confirmado nuevo / Confirmado repetido |

#### Tecnologías en salud (opcional, una o más filas)

| Campo | Descripción |
|-------|-------------|
| Tipo de tecnología | Procedimiento, medicamento, dispositivo, etc. |
| Código de tecnología | CUPS, IUM u otro según tipo |
| Nombre | Descripción de la tecnología |
| Finalidad | Diagnóstico, tratamiento, rehabilitación… |
| Fecha prescripción | Si aplica |
| Talento humano | Profesional que prescribe o aplica |

Clic en **Guardar**.

### 7.3 Ver detalle de atención

**URL:** `/atencion/<id>/`

Muestra paciente, prestador, clasificación de urgencias y lista de tecnologías asociadas.

### 7.4 Actualizar atención

**URL:** `/atencion/<id>/editar/`

Modifique campos y guarde. Las tecnologías pueden editarse en el mismo formulario.

---

## 8. Panel de administración (catálogos)

**URL:** http://127.0.0.1:8000/admin/

Requiere usuario con permisos de **staff/superusuario** (`createsuperuser`).

### 8.1 ¿Qué se administra aquí?

Todos los **catálogos** con más de 5 opciones normativas, por ejemplo:

- Países, municipios, tipos de documento
- Diagnósticos CIE-10, enfermedades huérfanas
- Prestadores de salud, modalidades, vías de ingreso
- Causas de atención, tipos y finalidades de tecnología
- Medicamentos, procedimientos CUPS, etc.

### 8.2 ¿Qué NO se administra aquí?

Por diseño del proyecto académico:

- **Pacientes** → solo por el módulo web `/pacientes/`
- **Contactos de salud** → solo por `/atencion/`

### 8.3 Funciones del Admin

En cada catálogo puede:
- **Listar** con búsqueda y filtros
- **Crear** nuevo registro
- **Editar** o **eliminar** (con precaución en producción)

El encabezado del Admin está personalizado: *IPS Salud y Vida — Historia Clínica Electrónica*.

### 8.4 Cargar datos iniciales

Si los catálogos están vacíos:

```bash
python manage.py seed_catalogos
```

---

## 9. Guía para sustentación y explicación del proyecto

### 9.1 Guión de demostración (5–7 minutos)

1. **Contexto (30 s):** IPS Salud y Vida, Resolución 866/2021, interoperabilidad HCE.
2. **Login / registro (30 s):** Mostrar autenticación obligatoria.
3. **Paciente (2 min):** Crear paciente con 2 nacionalidades, 1 discapacidad, oposición a donación.
4. **Urgencias (2 min):** Registrar contacto con triage III, diagnóstico, una tecnología.
5. **Admin (1 min):** Mostrar catálogo de diagnósticos o prestadores.
6. **Cierre (30 s):** Mencionar Django, MySQL, modelo E-R, GitHub.

### 9.2 Preguntas que puede hacer el docente

| Pregunta | Respuesta sugerida |
|----------|-------------------|
| ¿Por qué nacionalidad es tabla aparte? | La norma permite **múltiples** nacionalidades por persona (N:M). |
| ¿Por qué oposición a donación es aparte? | La Res. 866 y la Ley 1805 exigen estructura **independiente**. |
| ¿ForeignKey o ManyToMany? | M2M solo donde hay cardinalidad múltiple; resto FK o OneToOne. |
| ¿Por qué choices y no tablas? | Campos con **5 o menos** opciones fijas usan `TextChoices`. |
| ¿Por qué más de 5 opciones son tablas? | Requisito del proyecto y facilita administración en Django Admin. |
| ¿Dónde está el modelo E-R? | En `docs/DIAGRAMA_ER.md` del repositorio. |

### 9.3 Tecnologías para mencionar

- **Backend:** Django 5+, Python 3.12+
- **BD:** MySQL UTF8MB4 (SQLite en desarrollo)
- **Frontend:** Templates Django + Bootstrap 5
- **Seguridad:** Autenticación por sesión, rutas protegidas
- **Repositorio:** GitHub con README y documentación

---

## 10. Preguntas frecuentes y solución de problemas

### No puedo iniciar sesión
- Verifique usuario y contraseña
- Si no tiene cuenta, use **Registrarse**
- Si olvidó la contraseña de admin: `python manage.py changepassword <usuario>`

### Error al conectar MySQL
- Verifique que MySQL esté encendido
- Revise `DB_USER`, `DB_PASSWORD`, `DB_NAME` en `.env`
- Confirme que la BD existe con charset `utf8mb4`
- Alternativa: use `DB_ENGINE=sqlite` para pruebas

### Lista de pacientes o municipios vacía
- Ejecute: `python manage.py seed_catalogos`

### Error 500 al entrar
- Revise que ejecutó `migrate`
- Vea el mensaje en la terminal donde corre `runserver`

### No aparece el Admin personalizado
- Entre a `/admin/` con superusuario
- Los estilos están en `static/css/admin_custom.css`

### Puerto 8000 ocupado
```bash
python manage.py runserver 8001
```
Luego abra http://127.0.0.1:8001/

### ¿Cómo agrega otro integrante del equipo?
1. Clonar el repo de GitHub
2. Seguir la sección 3 de este manual
3. Cada uno puede registrarse en `/registro/`

---

## 11. Glosario de términos

| Término | Significado |
|---------|-------------|
| **HCE** | Historia Clínica Electrónica |
| **IPS** | Institución Prestadora de Servicios de Salud |
| **CIE-10** | Clasificación Internacional de Enfermedades, décima revisión |
| **CIUO-88** | Clasificación Internacional Uniforme de Ocupaciones |
| **DIVIPOLA** | División político-administrativa de Colombia (DANE) |
| **Triage** | Clasificación de prioridad en urgencias (I a V) |
| **CUPS** | Clasificación Única de Procedimientos en Salud |
| **SGSSS** | Sistema General de Seguridad Social en Salud |
| **CRUD** | Crear, Leer, Actualizar (consultar/editar) |
| **Catálogo** | Tabla de referencia con códigos normativos |

---

## Contacto y repositorio

- **Repositorio:** https://github.com/MichellGiraldoArcila/ProyectoClinica  
- **Documentación técnica adicional:** `README.md`, `docs/DEFENSA_TECNICA.md`, `docs/DIAGRAMA_ER.md`

---

*Manual elaborado para el proyecto académico — Tendencias en Desarrollo de Software. IPS Salud y Vida.*
