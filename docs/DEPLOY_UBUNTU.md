# Guía de Despliegue en Ubuntu con Nginx - Declarador.io

Esta guía te llevará paso a paso para desplegar Declarador.io en un servidor Ubuntu con Nginx y PostgreSQL.

## Requisitos

- Servidor Ubuntu 20.04 o superior
- Acceso root o sudo
- Dominio apuntando a tu servidor (opcional pero recomendado)

## Tiempo estimado: 30-40 minutos

---

## Opción A: Instalación Automática (Recomendado)

Si quieres una instalación rápida y automatizada, usa el script:

```bash
# 1. Clonar el proyecto
git clone https://github.com/tu-usuario/declarador.io.git /home/declarador/declarador.io

# 2. Ejecutar el script de instalación
sudo bash /home/declarador/declarador.io/scripts/install_production.sh
```

El script te pedirá:
- Dominio
- Email para SSL
- Password para PostgreSQL

Y configurará automáticamente:
- PostgreSQL
- Gunicorn
- Nginx
- SSL con Let's Encrypt
- Firewall

**Después de ejecutar el script, salta a la sección "Checklist Final".**

---

## Opción B: Instalación Manual (Paso a Paso)

Si prefieres instalar manualmente para entender el proceso:

---

## PARTE 1: Preparación del Servidor

### 1. Actualizar el Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalar Dependencias Básicas

```bash
sudo apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib curl
```

### 3. Instalar Node.js (para Tailwind CSS)

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

Verificar instalación:
```bash
python3 --version
node --version
npm --version
psql --version
nginx -v
```

---

## PARTE 2: Configurar PostgreSQL

### 1. Crear Base de Datos y Usuario

```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:
```sql
CREATE DATABASE declarador_db;
CREATE USER declarador_user WITH PASSWORD 'TU_PASSWORD_SEGURA_AQUI';
ALTER ROLE declarador_user SET client_encoding TO 'utf8';
ALTER ROLE declarador_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE declarador_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE declarador_db TO declarador_user;
\q
```

**Importante**: Cambia `TU_PASSWORD_SEGURA_AQUI` por una contraseña segura real.

---

## PARTE 3: Instalar el Proyecto

### 1. Crear Usuario para la Aplicación

```bash
sudo useradd -m -s /bin/bash declarador
sudo su - declarador
```

### 2. Clonar el Proyecto

```bash
cd /home/declarador
git clone https://github.com/tu-usuario/declarador.io.git
cd declarador.io
```

O si tienes los archivos:
```bash
# Sube los archivos a /home/declarador/declarador.io
```

### 3. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

**Importante**: Verifica que el venv se activó correctamente. Deberías ver `(venv)` al inicio de tu prompt.

### 4. Instalar Dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary  # Servidor WSGI y PostgreSQL
```

**Nota**: Si obtienes error de "externally-managed-environment", asegúrate de que el entorno virtual esté activado (`source venv/bin/activate`).

### 5. Instalar Dependencias Node.js

```bash
npm install
```

### 6. Compilar CSS

```bash
npm run tailwind:build
```

---

## PARTE 4: Configurar el Proyecto

### 1. Crear Archivo de Configuración

```bash
cp env.example .env
nano .env
```

Edita con tu configuración:

```bash
# Configuración de Producción
DEBUG=False
SECRET_KEY=GENERA_UNA_CLAVE_SUPER_SECRETA_AQUI
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de Datos PostgreSQL
DB_ENGINE=postgresql
DB_NAME=declarador_db
DB_USER=declarador_user
DB_PASSWORD=TU_PASSWORD_SEGURA_AQUI
DB_HOST=localhost
DB_PORT=5432
```

**Generar SECRET_KEY segura:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copia el resultado al archivo `.env`.

### 2. Aplicar Migraciones

```bash
python manage.py migrate
```

### 3. Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

Esto recopilará todos los archivos CSS, JS e imágenes en la carpeta `staticfiles/`.

### 4. Configurar Permisos Correctos

**IMPORTANTE**: Nginx necesita acceso a los archivos. Ejecuta:

```bash
# Sal del usuario declarador
exit

# Configura permisos del directorio home
sudo chmod 755 /home/declarador

# Configura permisos del proyecto
sudo chown -R declarador:www-data /home/declarador/declarador.io
sudo chmod -R 755 /home/declarador/declarador.io

# Permisos específicos para staticfiles
sudo chmod -R 755 /home/declarador/declarador.io/staticfiles
```

### 5. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 6. Probar el Servidor Localmente

```bash
python manage.py runserver 0.0.0.0:8000
```

Visita: `http://tu-ip:8000`

Si funciona, presiona Ctrl+C y sal del usuario:

```bash
exit
```

---

## PARTE 5: Configurar Gunicorn

### 1. Crear Archivo de Socket Systemd

Sal del usuario declarador:
```bash
exit
```

Como root/sudo:
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Contenido:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### 2. Crear Archivo de Servicio Systemd

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Contenido:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=declarador
Group=www-data
WorkingDirectory=/home/declarador/declarador.io
Environment="PATH=/home/declarador/declarador.io/venv/bin"
ExecStart=/home/declarador/declarador.io/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Iniciar y Habilitar Gunicorn

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

### 4. Verificar Estado

```bash
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn
```

### 5. Verificar Socket

```bash
sudo ls -la /run/gunicorn.sock
# Debería mostrar el archivo socket
```

---

## PARTE 6: Configurar Nginx

### 1. Crear Configuración del Sitio

```bash
sudo nano /etc/nginx/sites-available/declarador
```

Contenido básico (HTTP):
```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/declarador/declarador.io/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

**Nota**: Cambia `tudominio.com` por tu dominio real, o usa tu IP si no tienes dominio.

### 2. Activar el Sitio

```bash
sudo ln -s /etc/nginx/sites-available/declarador /etc/nginx/sites-enabled/
```

### 3. Verificar Configuración

```bash
sudo nginx -t
```

Si dice "syntax is ok" y "test is successful", continúa:

```bash
sudo systemctl restart nginx
```

### 4. Permitir Nginx en Firewall

```bash
sudo ufw allow 'Nginx Full'
```

---

## PARTE 7: Acceder a la Aplicación

Visita en tu navegador:
- `http://tudominio.com` (si configuraste dominio)
- `http://tu-ip-del-servidor` (si usas IP)

Deberías ver la aplicación funcionando.

---

## PARTE 8: Configurar SSL (HTTPS) - Recomendado

### 1. Instalar Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Obtener Certificado SSL

```bash
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

Sigue las instrucciones. Certbot configurará automáticamente Nginx para HTTPS.

### 3. Renovación Automática

```bash
sudo certbot renew --dry-run
```

El certificado se renovará automáticamente.

---

## PARTE 9: Mantenimiento

### Reiniciar Servicios

```bash
# Reiniciar Gunicorn
sudo systemctl restart gunicorn

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver logs de Gunicorn
sudo journalctl -u gunicorn

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Actualizar el Proyecto

```bash
sudo su - declarador
cd /home/declarador/declarador.io
source venv/bin/activate

# Obtener cambios
git pull

# Actualizar dependencias si es necesario
pip install -r requirements.txt
npm install

# Recompilar CSS
npm run tailwind:build

# Aplicar migraciones
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic --noinput

# Salir
exit

# Reiniciar Gunicorn
sudo systemctl restart gunicorn
```

### Backup de Base de Datos

```bash
# Crear backup
sudo -u postgres pg_dump declarador_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
sudo -u postgres psql declarador_db < backup_20251201.sql
```

---

## Solución de Problemas

### Error 502 Bad Gateway

```bash
# 1. Verificar estado
sudo systemctl status gunicorn

# 2. Ver logs detallados
sudo journalctl -u gunicorn -n 50 --no-pager

# 3. Si dice "No such file or directory" para gunicorn:
sudo su - declarador
cd ~/declarador.io
source venv/bin/activate
pip install gunicorn
which gunicorn  # Debe mostrar ruta en venv
exit

# 4. Recargar y reiniciar
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn

# 5. Verificar
sudo systemctl status gunicorn
```

### Error de Permisos en Archivos Estáticos

Si ves error 403 en los archivos CSS/JS:

```bash
# Permisos del directorio home (IMPORTANTE)
sudo chmod 755 /home/declarador

# Permisos del proyecto
sudo chown -R declarador:www-data /home/declarador/declarador.io
sudo chmod -R 755 /home/declarador/declarador.io

# Verificar
ls -la /home/ | grep declarador
ls -la /home/declarador/declarador.io/staticfiles/

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Base de Datos no Conecta

```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Verificar .env
sudo su - declarador
cd declarador.io
cat .env | grep DB_
```

### Cambios no se Reflejan

```bash
# Limpiar caché de Python
sudo su - declarador
cd declarador.io
find . -type d -name __pycache__ -exec rm -r {} +
exit

# Reiniciar todo
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## Configuración de Seguridad Adicional

### 1. Firewall UFW

```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### 2. Fail2Ban (Protección contra Ataques)

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Actualizar settings.py para Producción

```bash
sudo su - declarador
cd declarador.io
nano config/settings.py
```

Verificar/agregar:
```python
# Seguridad
SECURE_SSL_REDIRECT = True  # Solo si tienes SSL
SESSION_COOKIE_SECURE = True  # Solo si tienes SSL
CSRF_COOKIE_SECURE = True  # Solo si tienes SSL
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## Checklist Final

- [ ] PostgreSQL corriendo y base de datos creada
- [ ] Proyecto clonado en `/home/declarador/declarador.io`
- [ ] Entorno virtual creado y dependencias instaladas
- [ ] **Gunicorn instalado en el venv**: `which gunicorn` muestra ruta en venv
- [ ] Archivo `.env` configurado correctamente
- [ ] Migraciones aplicadas: `python manage.py migrate`
- [ ] Archivos estáticos recolectados: `python manage.py collectstatic`
- [ ] **Permisos configurados**: `/home/declarador` tiene permisos 755
- [ ] **Permisos de staticfiles**: Propiedad `declarador:www-data`
- [ ] Gunicorn configurado y corriendo: `sudo systemctl status gunicorn`
- [ ] Socket existe: `ls -la /run/gunicorn.sock`
- [ ] Nginx configurado y corriendo: `sudo nginx -t`
- [ ] Firewall configurado: `sudo ufw status`
- [ ] SSL configurado (si tienes dominio)
- [ ] **Aplicación accesible desde el navegador con estilos correctos**
- [ ] Sistema de búsqueda funciona correctamente

---

## Comandos Útiles de Referencia Rápida

```bash
# Estado de servicios
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status postgresql

# Reiniciar servicios
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Ver logs
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log

# Entrar al servidor como usuario de la app
sudo su - declarador

# Activar entorno virtual
source /home/declarador/declarador.io/venv/bin/activate

# Django management
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

---

## Recursos Adicionales

- **Documentación Django**: https://docs.djangoproject.com/
- **Guía Nginx**: https://nginx.org/en/docs/
- **Guía PostgreSQL**: https://www.postgresql.org/docs/
- **Certbot**: https://certbot.eff.org/

---

**¡Listo!** Tu aplicación Declarador.io está corriendo en producción.

**URL de Acceso**:
- Inicio: https://tudominio.com
- Búsqueda: https://tudominio.com/buscar/
- Admin: https://tudominio.com/admin/

---

**Última actualización**: Diciembre 2025

