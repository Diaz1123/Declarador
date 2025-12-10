# Guía de Instalación - Declarador.io

Esta guía te llevará paso a paso a través del proceso de instalación y configuración de Declarador.io en tu entorno local.

## Requisitos del Sistema

Antes de comenzar, verifica que tu sistema cumple con los siguientes requisitos:

### Software Requerido

- **Python**: Versión 3.10 o superior
- **Node.js**: Versión 18 o superior
- **npm**: Incluido con Node.js
- **Git**: Para control de versiones (opcional pero recomendado)

### Verificar Versiones Instaladas

```bash
# Verificar Python
python3 --version

# Verificar Node.js
node --version

# Verificar npm
npm --version

# Verificar Git
git --version
```

### Espacio en Disco

- Mínimo requerido: 500 MB
- Recomendado: 1 GB (incluye espacio para desarrollo)

## Instalación Paso a Paso

### 1. Obtener el Código Fuente

#### Opción A: Clonar desde Git

```bash
git clone <url-del-repositorio> declarador.io
cd declarador.io
```

#### Opción B: Descargar el archivo ZIP

1. Descarga el archivo ZIP del proyecto
2. Extrae el contenido
3. Navega al directorio extraído

```bash
cd declarador.io
```

### 2. Crear el Entorno Virtual de Python

El entorno virtual aísla las dependencias del proyecto de tu instalación global de Python.

#### En Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### En Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### En Windows (CMD):

```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Nota**: Una vez activado, verás `(venv)` al inicio de tu línea de comandos.

### 3. Instalar Dependencias de Python

Con el entorno virtual activado, instala las dependencias de Python:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará:
- Django 5.2.8
- google-generativeai (para integración opcional con Gemini AI)
- Otras dependencias necesarias

**Tiempo estimado**: 2-3 minutos

### 4. Instalar Dependencias de Node.js

Estas dependencias son necesarias para compilar Tailwind CSS:

```bash
npm install
```

Esto instalará:
- Tailwind CSS v4.1
- CLI de Tailwind
- Dependencias relacionadas

**Tiempo estimado**: 1-2 minutos

### 5. Compilar Tailwind CSS

Compila los estilos CSS necesarios para la interfaz:

```bash
npm run tailwind:build
```

Este comando genera el archivo `core/static/css/output.css` optimizado y minificado.

**Nota**: Si ves advertencias sobre PostCSS, puedes ignorarlas. El CSS se compilará correctamente.

### 6. Configurar la Base de Datos

Aplica las migraciones para crear la estructura de la base de datos SQLite:

```bash
python manage.py migrate
```

Este comando crea:
- El archivo `db.sqlite3` en la raíz del proyecto
- Todas las tablas necesarias para el modelo Declaration
- Tablas del sistema Django (sesiones, admin, etc.)

**Tiempo estimado**: 10-15 segundos

### 7. Crear un Superusuario (Opcional)

Si deseas acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Te pedirá:
- Nombre de usuario
- Dirección de email (opcional)
- Contraseña (mínimo 8 caracteres)

**Nota**: Puedes omitir este paso si solo quieres usar la aplicación web.

### 8. Verificar la Instalación

Ejecuta las verificaciones del sistema de Django:

```bash
python manage.py check
```

Si todo está correcto, verás:

```
System check identified no issues (0 silenced).
```

### 9. Iniciar el Servidor de Desarrollo

Inicia el servidor local de Django:

```bash
python manage.py runserver
```

Verás un mensaje similar a:

```
Django version 5.2.8, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 10. Acceder a la Aplicación

Abre tu navegador web y navega a:

```
http://localhost:8000
```

O también:

```
http://127.0.0.1:8000
```

Serás redirigido automáticamente al Paso 1 del wizard.

## Verificación de la Instalación

### Checklist de Verificación

- [ ] El servidor inicia sin errores
- [ ] La página principal carga correctamente
- [ ] Los estilos CSS se muestran correctamente
- [ ] Puedes navegar entre los pasos del wizard
- [ ] El archivo `db.sqlite3` existe en la raíz del proyecto
- [ ] El archivo `core/static/css/output.css` existe y tiene contenido

### Acceso al Panel de Administración

Si creaste un superusuario:

1. Navega a: `http://localhost:8000/admin/`
2. Ingresa con tu usuario y contraseña
3. Deberías ver el panel de administración de Django

## Configuración Adicional (Opcional)

### Variables de Entorno

Para configuración avanzada, puedes crear un archivo `.env` en la raíz del proyecto:

```bash
# .env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
GEMINI_API_KEY=tu-api-key-de-google
```

### Configurar Variables de Entorno (Opcional)

El proyecto incluye un archivo `env.example` con todas las configuraciones disponibles:

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar según tus necesidades
nano .env
```

Por defecto, el proyecto usa SQLite. No necesitas archivo `.env` para desarrollo básico.

### Configurar Integración con Gemini AI

Si deseas habilitar las funcionalidades de IA:

1. Obtén una API key de [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Agrega la clave a tu archivo `.env`:

```bash
GEMINI_API_KEY=tu-api-key-aqui
```

3. Consulta `docs/GEMINI_INTEGRATION.md` para más detalles

### Modo de Desarrollo CSS

Si vas a modificar estilos, usa el modo watch de Tailwind:

```bash
# En una terminal separada
npm run tailwind:watch
```

Esto recompilará automáticamente los estilos cuando modifiques `core/static/css/input.css`.

## Solución de Problemas

### Error: "No module named 'django'"

**Problema**: El entorno virtual no está activado o Django no se instaló.

**Solución**:
```bash
# Activar el entorno virtual
source venv/bin/activate  # Linux/Mac
# O
venv\Scripts\activate  # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Port 8000 is already in use"

**Problema**: Otro proceso está usando el puerto 8000.

**Solución 1** - Detener el proceso existente:
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Solución 2** - Usar otro puerto:
```bash
python manage.py runserver 8080
```

### Los estilos CSS no se muestran

**Problema**: El archivo CSS no se compiló correctamente.

**Solución**:
```bash
# Verificar que el archivo existe
ls -lh core/static/css/output.css

# Si no existe o está vacío, recompilar
npm run tailwind:build

# Si persiste el problema, reinstalar dependencias npm
rm -rf node_modules package-lock.json
npm install
npm run tailwind:build
```

### Error: "OperationalError: no such table"

**Problema**: Las migraciones no se aplicaron correctamente.

**Solución**:
```bash
# Eliminar la base de datos (solo en desarrollo)
rm db.sqlite3

# Aplicar migraciones nuevamente
python manage.py migrate
```

### Error: "ModuleNotFoundError: No module named 'core'"

**Problema**: Estás ejecutando comandos desde el directorio incorrecto.

**Solución**:
```bash
# Verificar que estás en el directorio correcto
pwd  # Debe mostrar: /ruta/a/declarador.io

# Verificar que existe manage.py
ls manage.py
```

### Errores de permisos en Linux/Mac

**Problema**: Permisos insuficientes para ejecutar scripts.

**Solución**:
```bash
# Dar permisos de ejecución
chmod +x manage.py

# Si el problema persiste con venv
chmod -R u+rwx venv/
```

## Comandos de Mantenimiento

### Limpiar sesiones expiradas

```bash
python manage.py clearsessions
```

### Actualizar dependencias de Python

```bash
pip install --upgrade -r requirements.txt
```

### Recolectar archivos estáticos (para producción)

```bash
python manage.py collectstatic
```

### Crear nuevas migraciones (después de cambios en models.py)

```bash
python manage.py makemigrations
python manage.py migrate
```

## Desinstalación

Si deseas eliminar completamente la instalación:

```bash
# 1. Desactivar el entorno virtual
deactivate

# 2. Eliminar el directorio del proyecto
cd ..
rm -rf declarador.io
```

## Próximos Pasos

Una vez completada la instalación:

1. Lee la documentación en `docs/INICIO_RAPIDO.md`
2. Prueba la aplicación creando una declaración completa
3. Revisa `docs/README_DECLARADOR.md` para entender la arquitectura
4. Explora las opciones de integración con IA en `docs/GEMINI_INTEGRATION.md`

## Soporte

Si encuentras problemas no cubiertos en esta guía:

1. Revisa `docs/README.md` para más documentación
2. Consulta el archivo `CHANGELOG.md` para cambios recientes
3. Abre un issue en el repositorio de GitHub

---

**Tiempo total de instalación**: 10-15 minutos

**Última actualización**: Diciembre 2025

