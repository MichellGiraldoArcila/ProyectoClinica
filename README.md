# IPS Salud y Vida — Historia Clínica Electrónica (HCE)

Sistema de información para gestión de historia clínica electrónica, desarrollado con **Django 5+** y alineado con la **Resolución 866 de 2021** del Ministerio de Salud de Colombia (interoperabilidad de datos clínicos).

## Tecnologías

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.12+ |
| Framework | Django 5+ |
| Base de datos | MySQL (UTF8MB4) / SQLite (desarrollo) |
| Frontend | HTML, CSS, Bootstrap 5 |
| Configuración | python-decouple (.env) |
| Autenticación | Django Auth (sesiones) |

## Arquitectura del proyecto

```
ProyectoClinica/
├── manage.py
├── requirements.txt
├── .env.example
├── salud_vida/              # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── admin.py             # Personalización global del Admin
├── apps/
│   ├── catalogos/           # Tablas de referencia (>5 opciones → modelos)
│   ├── pacientes/           # CRUD pacientes + estructuras normativas
│   ├── atencion/            # Contacto servicio de salud (urgencias)
│   └── cuentas/             # Login, logout, dashboard
├── core/
│   ├── choices.py           # Choices normativos (≤5 opciones)
│   ├── validators.py
│   └── mixins.py            # Protección de rutas
├── templates/               # Plantillas Bootstrap 5
├── static/                  # CSS personalizado (portal + admin)
└── docs/
    └── DEFENSA_TECNICA.md   # Guía para sustentación
```

### Decisiones de modelado

- **Oposición a donación** y **voluntad anticipada**: tablas separadas (`OneToOne` / `ForeignKey`), no campos embebidos en paciente.
- **Nacionalidades** y **discapacidades**: relaciones **muchos a muchos** mediante tablas intermedias (`PacienteNacionalidad`, `PacienteDiscapacidad`).
- Campos con **más de 5 opciones** → modelos en `catalogos` (tipos documento, modalidad, vía ingreso, causa, finalidad, etc.).
- Campos con **5 o menos opciones** → `TextChoices` en `core/choices.py` (sexo, zona, triage, grupo servicios, etc.).

## Requisitos previos

- Python 3.12 o superior
- MySQL 8+ (producción) o SQLite (desarrollo local)
- Git

## Instalación

### 1. Clonar e instalar dependencias

```bash
git clone <url-repositorio>
cd ProyectoClinica
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Variables de entorno

```bash
cp .env.example .env
```

Editar `.env`. Para **MySQL**:

```env
DB_ENGINE=mysql
DB_NAME=salud_vida_hce
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Crear la base de datos en MySQL:

```sql
CREATE DATABASE salud_vida_hce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Para desarrollo rápido sin MySQL:

```env
DB_ENGINE=sqlite
```

### 3. Migraciones y datos iniciales

```bash
python manage.py migrate
python manage.py seed_catalogos
```

### 4. Superusuario

```bash
python manage.py createsuperuser
```

### 5. Ejecutar servidor

```bash
python manage.py runserver
```

- Portal: http://127.0.0.1:8000/
- Admin catálogos: http://127.0.0.1:8000/admin/

## Módulos funcionales

| Módulo | Rutas | Operaciones |
|--------|-------|-------------|
| Autenticación | `/login/`, `/registro/`, `/logout/` | Registro, inicio y cierre de sesión |
| Pacientes | `/pacientes/` | Crear, listar, consultar, actualizar |
| Atención urgencias | `/atencion/` | Crear, listar, consultar, actualizar contacto |
| Catálogos | `/admin/` | CRUD catálogos normativos (panel personalizado) |

> **Nota etapa 2:** Paciente y ContactoSalud no se registran en Django Admin; se gestionan por las vistas CRUD del portal (requisito académico etapa 3).

## Comandos útiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_catalogos
python manage.py collectstatic
python manage.py check
```

## Despliegue (recomendaciones)

1. `DEBUG=False`, `SECRET_KEY` segura, `ALLOWED_HOSTS` configurado.
2. MySQL con `utf8mb4` y usuario con permisos mínimos.
3. Servir estáticos con WhiteNoise o Nginx.
4. Gunicorn/uWSGI detrás de proxy inverso (Nginx).
5. HTTPS obligatorio en producción.
6. Respaldos automáticos de BD y rotación de logs.

## Equipo / IPS ficticia

**IPS Salud y Vida** — Proyecto académico Ingeniería de Software / Tendencias en Desarrollo de Software (2026-1).

## Licencia

Proyecto educativo. Datos de catálogo son referencias normativas del Ministerio de Salud (Res. 866/2021).
