# Registro de Cambios - Declarador.io

Todos los cambios notables del proyecto serán documentados en este archivo.

## [Correcciones en Guía de Despliegue] - 2025-12-01

### Corregido
- **Guía de despliegue actualizada** con soluciones a problemas comunes:
  - Agregada instalación explícita de gunicorn en requirements
  - Agregada sección de configuración de permisos para `/home/declarador`
  - Agregada verificación de permisos de staticfiles
  - Mejorada sección de troubleshooting para error 502
  - Agregado checklist más detallado con verificaciones de permisos
  - Documentado problema de "externally-managed-environment"
  - Agregadas instrucciones para verificar instalación de gunicorn

### Mejorado
- Documentación de `DEPLOY_UBUNTU.md` con casos reales de producción
- Checklist final más completo con verificaciones críticas

## [Optimización de Archivos Estáticos] - 2025-12-01

### Cambiado
- **Configuración de archivos estáticos optimizada** en `config/settings.py`
  - Removido `STATICFILES_DIRS` para evitar duplicados
  - Agregado `STATIC_ROOT` para recolección en producción
  - Django ahora busca automáticamente en `core/static/`
  - Elimina advertencias de archivos duplicados en `collectstatic`

### Actualizado
- `docs/DEPLOY_UBUNTU.md` - Simplificada sección de archivos estáticos
- `requirements.txt` - Agregado gunicorn explícitamente

## [Guía de Despliegue en Producción] - 2025-12-01

### Agregado
- **Guía completa de despliegue** en `docs/DEPLOY_UBUNTU.md`
  - Instalación paso a paso en Ubuntu Server
  - Configuración de Nginx como proxy reverso
  - Configuración de Gunicorn como servidor WSGI
  - Configuración de PostgreSQL en producción
  - Configuración de SSL con Let's Encrypt
  - Systemd para inicio automático de servicios
  - Comandos de mantenimiento y actualización
  - Solución de problemas comunes
  - Checklist de seguridad
- **Script de instalación automática** en `scripts/install_production.sh`
  - Instalación completamente automatizada
  - Configuración interactiva (dominio, email, passwords)
  - Instala y configura todos los servicios
  - Obtiene certificado SSL automáticamente
  - Tiempo de instalación: ~10 minutos
- Carpeta `scripts/` con documentación de scripts
- Referencias actualizadas en README.md y docs/README.md

## [Integración de PostgreSQL y Sistema de Búsqueda] - 2025-12-01

### Agregado
- **Soporte completo para PostgreSQL** como base de datos principal
- **Guardado automático** de todas las declaraciones generadas
- **Sistema de búsqueda** por Hash de Validación o ID de Declaración
- **Página de verificación** pública de declaraciones en `/buscar/`
- **Vista individual** de declaraciones en `/declaracion/<ID>/`
- Botón "Verificar" en el header para acceso rápido a búsqueda
- Template `search.html` para búsqueda de declaraciones
- Template `view_declaration.html` para visualización completa
- Template `not_found.html` para declaraciones no encontradas
- Documentación completa en `docs/POSTGRESQL.md`
- Soporte para variables de entorno con `python-decouple`
- **Archivo `env.example`** con configuración completa comentada
  - Ejemplos para SQLite y PostgreSQL
  - Configuraciones para desarrollo y producción
  - Instrucciones de uso incluidas

### Cambiado
- `config/settings.py` ahora soporta PostgreSQL y SQLite dinámicamente
- Las declaraciones se guardan automáticamente en base de datos
- Header actualizado con enlace de verificación
- `requirements.txt` incluye `psycopg2-binary` y `python-decouple`

### Técnico
- Nuevas vistas: `search_declaration()` y `view_declaration()`
- Nuevas URLs: `/buscar/` y `/declaracion/<ID>/`
- Configuración de base de datos por variables de entorno
- Índices automáticos en `declaration_id` y `validation_hash`

## [Reorganización de Documentación] - 2025-12-01

### Cambiado
- README.md principal completamente reescrito como punto de entrada conciso
- Toda la documentación reformateada sin emojis para mayor profesionalismo
- INICIO_RAPIDO.md actualizado sin emojis
- RESUMEN_PROYECTO.md completamente reescrito sin emojis
- docs/README.md actualizado con nueva estructura

### Agregado
- **docs/INSTALACION.md** - Guía completa de instalación paso a paso con:
  - Requisitos del sistema detallados
  - Instalación paso a paso para Linux/Mac/Windows
  - Sección completa de solución de problemas
  - Comandos de mantenimiento
  - Configuración adicional opcional
- Sección de instalación rápida en README.md principal
- Referencias cruzadas mejoradas entre documentos
- Convenciones de documentación actualizadas

### Mejorado
- Estructura de carpeta `docs/` mejor organizada
- Índice de documentación más claro en docs/README.md
- Orden de lectura recomendado mejorado
- Enlaces entre documentos actualizados

### Estructura actual de documentación
```
declarador.io/
├── README.md                    # Punto de entrada principal (conciso)
├── CHANGELOG.md                 # Este archivo - registro de cambios
├── docs/                        # Toda la documentación del proyecto
│   ├── README.md               # Índice completo de documentación
│   ├── INSTALACION.md          # Guía completa de instalación (NUEVO)
│   ├── INICIO_RAPIDO.md        # Guía rápida de uso
│   ├── RESUMEN_PROYECTO.md     # Visión general técnica
│   ├── README_DECLARADOR.md    # Documentación técnica detallada
│   ├── GEMINI_INTEGRATION.md   # Guía de integración con IA
│   ├── VERIFICACION.md         # Checklist de verificación
│   └── LEEME_PRIMERO.txt       # Archivo histórico
├── config/                      # Configuración Django
├── core/                        # Aplicación principal
├── requirements.txt             # Dependencias Python
├── package.json                 # Dependencias Node.js
└── manage.py                    # CLI Django
```

## [Versión Inicial] - 2025-11-XX

### Agregado
- Migración completa de usoeticoia.org (React) a Django
- Wizard de 4 pasos completamente funcional
- Sistema de sesiones Django
- Modelo Declaration con 21 campos
- 9 tipos de uso de IA académico
- 7 niveles de revisión humana
- Generación de hash SHA-256
- Exportación TXT y JSON
- Integración preparada con Google Gemini AI
- Interfaz responsive con Tailwind CSS
- Documentación completa del proyecto

---

## Formato

Este changelog sigue las convenciones de [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

### Tipos de cambios
- **Agregado** - para funcionalidades nuevas
- **Cambiado** - para cambios en funcionalidades existentes
- **Obsoleto** - para funcionalidades que serán removidas
- **Removido** - para funcionalidades removidas
- **Corregido** - para corrección de bugs
- **Seguridad** - para vulnerabilidades corregidas

