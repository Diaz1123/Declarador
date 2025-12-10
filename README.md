# Declarador

Sistema web para generar declaraciones de transparencia sobre el uso de Inteligencia Artificial Generativa en trabajos académicos.

## Descripción

Declarador es una herramienta que permite a estudiantes e investigadores documentar de manera transparente y estandarizada el uso de IA generativa en sus trabajos académicos, promoviendo la honestidad académica y la trazabilidad del contenido asistido por IA.

## Características principales

- Wizard guiado de 4 pasos para crear declaraciones completas
- Sistema de diagnóstico interactivo con 7 preguntas clave
- Clasificación en 9 categorías de uso académico de IA
- 7 niveles de revisión humana documentados
- Generación de hash de validación SHA-256 para integridad del documento
- Exportación en formatos TXT y JSON
- Interfaz moderna y responsive con Tailwind CSS
- Sistema de sesiones Django para persistencia de datos
- Preparado para integración con Google Gemini AI

## Stack tecnológico

**Backend:**
- Django 5.2.8
- Python 3.10+
- SQLite (desarrollo) / PostgreSQL (producción recomendado)

**Frontend:**
- Django Templates
- Tailwind CSS v4.1
- Vanilla JavaScript (sin dependencias externas)

**Herramientas:**
- Node.js + npm (para compilación de Tailwind CSS)
- Git para control de versiones

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.10 o superior
- Node.js 18 o superior
- npm (incluido con Node.js)
- Git (opcional, para control de versiones)

## Instalación Rápida

### Pasos Básicos

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio> declarador.io
cd declarador.io

# 2. Configurar variables de entorno (opcional)
cp env.example .env
# Edita .env si necesitas cambiar la configuración

# 3. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows

# 4. Instalar dependencias Python
pip install -r requirements.txt

# 5. Instalar dependencias Node.js
npm install

# 6. Compilar Tailwind CSS
npm run tailwind:build

# 7. Aplicar migraciones
python manage.py migrate

# 8. Iniciar servidor
python manage.py runserver
```

Accede a: **http://localhost:8000**

**Nota**: Por defecto usa SQLite. Para PostgreSQL, consulta [docs/POSTGRESQL.md](docs/POSTGRESQL.md)

Para una guía de instalación detallada con solución de problemas, consulta [docs/INSTALACION.md](docs/INSTALACION.md)

## Uso básico

1. Abre tu navegador y navega a `http://localhost:8000`
2. Serás redirigido automáticamente al Paso 1 del wizard
3. Completa los 4 pasos:
   - **Paso 1**: Diagnóstico - responde al checklist interactivo
   - **Paso 2**: Clasificación - selecciona tipos de uso de IA
   - **Paso 3**: Detalles - completa información de la herramienta, prompts y revisión
   - **Paso 4**: Resultado - visualiza, copia o descarga tu declaración
4. Descarga tu declaración en formato TXT o JSON
5. Incluye la declaración en tu trabajo académico

## Estructura del proyecto

```
declarador/
├── CHANGELOG.md
├── compile_messages.py
├── db.sqlite3
├── env.example
├── manage.py
├── package.json
├── README.md
├── requirements.txt
├── config/                  # Configuración principal de Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Configuración del proyecto
│   ├── urls.py              # Rutas principales
│   ├── wsgi.py              # WSGI
│   └── __pycache__/
├── core/                    # App principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── constants.py
│   ├── context_processors.py
│   ├── models.py
│   ├── tests.py
│   ├── translations.py
│   ├── utils.py             # Texto/JSON y hash de validación
│   ├── views_old.py.backup
│   ├── __pycache__/
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_signer_declaration_is_draft.py
│   │   └── 0003_signer_affiliation_ror_id.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── input.css
│   │   │   └── output.css
│   │   └── js/
│   │       ├── preview.js
│   │       ├── signer_register.js
│   │       ├── step1.js
│   │       ├── step2.js
│   │       ├── step3.js
│   │       └── step4.js
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── home.html
│           ├── not_found.html
│           ├── privacy.html
│           ├── search.html
│           ├── signer_register.html
│           ├── signer_verify.html
│           ├── signers_list.html
│           ├── step1_identification.html
│           ├── step2_usage_type.html
│           ├── step3_details.html
│           ├── step4_output.html
│           └── view_declaration.html
├── views/                   # Vistas modulares
│   ├── __init__.py
│   ├── declarations.py
│   ├── downloads.py
│   ├── README.md
│   ├── search.py
│   ├── signers.py
│   └── utils.py
├── docs/
│   ├── DEPLOY_UBUNTU.md
│   ├── INSTALACION.md
│   └── RECAPTCHA.md
├── locale/                  # i18n (es, en, pt, it)
│   ├── en/LC_MESSAGES/django.po|mo
│   ├── es/LC_MESSAGES/django.po|mo
│   ├── it/LC_MESSAGES/django.po|mo
│   └── pt/LC_MESSAGES/django.po|mo
└── scripts/
   ├── install_production.sh
   ├── manage_signers.py
   └── README.md
```

## Validador con hashing

Este proyecto genera un identificador de validación mediante hashing para asegurar la integridad de la declaración final.

- Algoritmo: SHA-256
- Formato mostrado: prefijo de 16 caracteres en mayúsculas
- Ubicación: se calcula en `core/utils.py` con `compute_hash(message)`
- Inclusión: el hash se agrega al texto y JSON finales si está disponible

Cómo se calcula:

```python
from core.utils import compute_hash

mensaje = "contenido canonizado de la declaración"
hash16 = compute_hash(mensaje)  # Ej.: 'A1B2C3D4E5F6A7B8'
print(hash16)
```

Verificación manual rápida (Linux, fish):

```fish
# Generar SHA-256 y comparar el prefijo (16 chars)
set msg "contenido canonizado de la declaración"
printf "%s" $msg | sha256sum | cut -c1-16 | tr '[:lower:]' '[:upper:]'
```

Notas:
- El mensaje que se hashea es la representación canónica del contenido de la declaración; cualquier cambio en el texto/JSON cambiará el hash.
- El hash se muestra junto al `declaration_id` en las salidas finales para facilitar su verificación.

## Comandos útiles

### Desarrollo

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Compilar CSS en modo watch (auto-recompilación)
npm run tailwind:watch

# Compilar CSS para producción
npm run tailwind:build
```

### Base de datos

```bash
# Crear migraciones después de cambios en models.py
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario para admin de Django
python manage.py createsuperuser

# Acceder a la shell de Django
python manage.py shell
```

### Utilidades

```bash
# Verificar configuración del proyecto
python manage.py check

# Limpiar sesiones expiradas
python manage.py clearsessions

# Recolectar archivos estáticos (producción)
python manage.py collectstatic
```

## Documentación

La documentación completa se encuentra en la carpeta [docs/](docs/):

- **[INSTALACION.md](docs/INSTALACION.md)** - Guía completa de instalación paso a paso
- **[INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)** - Guía rápida de uso
- **[POSTGRESQL.md](docs/POSTGRESQL.md)** - Configuración de PostgreSQL y búsqueda de declaraciones
- **[RESUMEN_PROYECTO.md](docs/RESUMEN_PROYECTO.md)** - Visión general técnica
- **[README_DECLARADOR.md](docs/README_DECLARADOR.md)** - Documentación técnica detallada
- **[GEMINI_INTEGRATION.md](docs/GEMINI_INTEGRATION.md)** - Integración con Google Gemini AI
- **[VERIFICACION.md](docs/VERIFICACION.md)** - Checklist de funcionalidades

Ver el [índice completo de documentación](docs/README.md)

## Configuración para producción

### Variables de entorno

El proyecto incluye un archivo `env.example` con todas las configuraciones disponibles. Para configurar:

```bash
# 1. Copiar archivo de ejemplo
cp env.example .env

# 2. Editar .env con tu configuración
nano .env  # o usa tu editor preferido
```

Configuración mínima para producción:

```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DB_ENGINE=postgresql
DB_NAME=declarador_db
DB_USER=usuario_db
DB_PASSWORD=password_segura
DB_HOST=localhost
DB_PORT=5432
```

### Cambios necesarios en settings.py

1. Configurar `DEBUG = False`
2. Generar una nueva `SECRET_KEY` segura
3. Configurar `ALLOWED_HOSTS` con tu dominio
4. Cambiar a PostgreSQL en lugar de SQLite
5. Configurar archivos estáticos: `python manage.py collectstatic`

### Despliegue en Producción

### Instalación Automática (Más Rápido)

```bash
# 1. Clonar el proyecto en el servidor
git clone <repo-url> /home/declarador/declarador.io

# 2. Ejecutar script de instalación
sudo bash /home/declarador/declarador.io/scripts/install_production.sh
```

El script configurará automáticamente: Ubuntu, Nginx, PostgreSQL, Gunicorn y SSL.

### Guía Manual Completa

Consulta la guía paso a paso: **[docs/DEPLOY_UBUNTU.md](docs/DEPLOY_UBUNTU.md)**

Incluye:
- Instalación manual paso a paso
- Configuración de PostgreSQL
- Configuración de Gunicorn
- Configuración de Nginx
- SSL con Let's Encrypt
- Systemd para inicio automático
- Comandos de mantenimiento

### Otras Opciones de Hosting

- **Heroku** - Platform as a Service, fácil configuración
- **Railway** - Alternativa moderna a Heroku
- **DigitalOcean** - VPS con control total (usa la guía de Ubuntu)
- **AWS / Google Cloud / Azure** - Soluciones empresariales

## Integración con Gemini AI (Opcional)

El proyecto incluye soporte para Google Gemini AI:

1. Obtén una API key en [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Configura en `config/settings.py`: `GEMINI_API_KEY = 'tu-api-key'`
3. Consulta [docs/GEMINI_INTEGRATION.md](docs/GEMINI_INTEGRATION.md) para implementación completa

Casos de uso disponibles: mejora de redacción, sugerencias de nivel de revisión, validación ética, generación de ejemplos, chatbot de ayuda.

## Solución de problemas

### El servidor no inicia

```bash
# Verificar que el puerto 8000 no esté en uso
lsof -i :8000

# Usar un puerto alternativo
python manage.py runserver 8080
```

### Los estilos no se muestran

```bash
# Verificar que el archivo CSS existe
ls core/static/css/output.css

# Recompilar Tailwind
npm run tailwind:build
```

### Error "No module named 'core'"

```bash
# Verificar que estás en el directorio correcto
pwd

# Verificar que el entorno virtual está activado
which python  # Debe mostrar la ruta al venv
```

### Errores de sesión

```bash
# Limpiar sesiones
python manage.py clearsessions

# O reiniciar la base de datos (solo en desarrollo)
rm db.sqlite3
python manage.py migrate
```

## Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

### Áreas de Contribución

- Tests unitarios y de integración
- Traducciones a otros idiomas (inglés, portugués)
- Mejoras de accesibilidad (WCAG 2.1)
- Integración completa con Gemini AI
- Exportación a formato PDF
- Mejoras de UI/UX
- Documentación adicional y tutoriales

## Licencia

Este proyecto es una migración del proyecto original usoeticoia.org (React + TypeScript) a Django, manteniendo el mismo propósito educativo de promover la transparencia en el uso académico de IA.

## Contacto y soporte

- Documentación: Ver carpeta `docs/`
- Issues: Reporta bugs o solicita features en GitHub Issues
- Discusiones: Participa en GitHub Discussions

## Reconocimientos

Proyecto creado para promover la transparencia académica en el uso de Inteligencia Artificial Generativa.

- Proyecto original: usoeticoia.org (React + TypeScript)
- Migración a Django: Diciembre 2025
- Estado actual: Producción ready

---

**Desarrollado para la transparencia académica en el uso de IA**
