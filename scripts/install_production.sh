#!/bin/bash

# =================================================================
# Script de Instalación Automática - Declarador.io
# Para Ubuntu 20.04+ con Nginx y PostgreSQL
# =================================================================

set -e  # Salir si hay algún error

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

# Función para mostrar mensajes
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si se ejecuta como root
if [ "$EUID" -ne 0 ]; then 
    log_error "Este script debe ejecutarse como root (usa sudo)"
    exit 1
fi

echo "================================================================="
echo "   Instalación de Declarador.io en Producción"
echo "================================================================="
echo ""

# Solicitar información
read -p "Dominio (ejemplo: declarador.io): " DOMAIN
read -p "Email para SSL (ejemplo: admin@declarador.io): " EMAIL
read -sp "Password para PostgreSQL: " DB_PASSWORD
echo ""
read -sp "Django SECRET_KEY (deja en blanco para generar): " SECRET_KEY
echo ""

if [ -z "$SECRET_KEY" ]; then
    log_info "Generando SECRET_KEY..."
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
fi

# Paso 1: Actualizar sistema
log_info "Actualizando sistema..."
apt update
apt upgrade -y
log_success "Sistema actualizado"

# Paso 2: Instalar dependencias
log_info "Instalando dependencias..."
apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib curl ufw
log_success "Dependencias básicas instaladas"

# Instalar Node.js
log_info "Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs
log_success "Node.js instalado"

# Paso 3: Configurar PostgreSQL
log_info "Configurando PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE declarador_db;
CREATE USER declarador_user WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE declarador_user SET client_encoding TO 'utf8';
ALTER ROLE declarador_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE declarador_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE declarador_db TO declarador_user;
EOF
log_success "PostgreSQL configurado"

# Paso 4: Crear usuario
log_info "Creando usuario de aplicación..."
if id "declarador" &>/dev/null; then
    log_warning "Usuario declarador ya existe"
else
    useradd -m -s /bin/bash declarador
    log_success "Usuario declarador creado"
fi

# Paso 5: Clonar/preparar proyecto
log_info "Preparando directorio del proyecto..."
PROJECT_DIR="/home/declarador/declarador.io"

if [ -d "$PROJECT_DIR" ]; then
    log_warning "El directorio $PROJECT_DIR ya existe"
else
    log_info "Clona el proyecto manualmente en: $PROJECT_DIR"
    log_info "Ejecuta: git clone <repo-url> $PROJECT_DIR"
    log_error "Ejecuta primero el git clone y vuelve a correr este script"
    exit 1
fi

cd $PROJECT_DIR

# Paso 6: Configurar Python
log_info "Configurando entorno Python..."
sudo -u declarador python3 -m venv $PROJECT_DIR/venv
sudo -u declarador $PROJECT_DIR/venv/bin/pip install --upgrade pip
sudo -u declarador $PROJECT_DIR/venv/bin/pip install -r $PROJECT_DIR/requirements.txt
sudo -u declarador $PROJECT_DIR/venv/bin/pip install gunicorn psycopg2-binary
log_success "Entorno Python configurado"

# Paso 7: Configurar Node.js
log_info "Instalando dependencias Node.js..."
sudo -u declarador npm install
sudo -u declarador npm run tailwind:build
log_success "Dependencias Node.js instaladas"

# Paso 8: Crear archivo .env
log_info "Creando archivo de configuración..."
cat > $PROJECT_DIR/.env <<EOF
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN

DB_ENGINE=postgresql
DB_NAME=declarador_db
DB_USER=declarador_user
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
EOF
chown declarador:declarador $PROJECT_DIR/.env
chmod 600 $PROJECT_DIR/.env
log_success "Archivo .env creado"

# Paso 9: Migrar base de datos
log_info "Aplicando migraciones..."
sudo -u declarador $PROJECT_DIR/venv/bin/python manage.py migrate
log_success "Migraciones aplicadas"

# Paso 10: Recolectar archivos estáticos
log_info "Recolectando archivos estáticos..."
sudo -u declarador $PROJECT_DIR/venv/bin/python $PROJECT_DIR/manage.py collectstatic --noinput
log_success "Archivos estáticos recolectados"

# Paso 10.5: Configurar permisos correctos
log_info "Configurando permisos..."
chmod 755 /home/declarador
chown -R declarador:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 755 $PROJECT_DIR/staticfiles
log_success "Permisos configurados"

# Paso 11: Configurar Gunicorn
log_info "Configurando Gunicorn..."

cat > /etc/systemd/system/gunicorn.socket <<EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

cat > /etc/systemd/system/gunicorn.service <<EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=declarador
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          config.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl start gunicorn.socket
systemctl enable gunicorn.socket
log_success "Gunicorn configurado"

# Paso 12: Configurar Nginx
log_info "Configurando Nginx..."

cat > /etc/nginx/sites-available/declarador <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

ln -sf /etc/nginx/sites-available/declarador /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
log_success "Nginx configurado"

# Paso 13: Configurar Firewall
log_info "Configurando firewall..."
ufw allow 'Nginx Full'
ufw allow ssh
echo "y" | ufw enable
log_success "Firewall configurado"

# Paso 14: Configurar SSL
log_info "Instalando Certbot..."
apt install -y certbot python3-certbot-nginx

log_info "Obteniendo certificado SSL..."
certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive
log_success "SSL configurado"

# Resumen
echo ""
echo "================================================================="
echo "   Instalación Completada!"
echo "================================================================="
echo ""
echo -e "${GREEN}Tu aplicación está disponible en:${NC}"
echo "  https://$DOMAIN"
echo "  https://$DOMAIN/buscar/"
echo "  https://$DOMAIN/admin/"
echo ""
echo -e "${YELLOW}Información importante:${NC}"
echo "  - Usuario de la aplicación: declarador"
echo "  - Directorio del proyecto: $PROJECT_DIR"
echo "  - Base de datos: declarador_db"
echo "  - Usuario PostgreSQL: declarador_user"
echo ""
echo -e "${BLUE}Comandos útiles:${NC}"
echo "  - Ver logs: sudo journalctl -u gunicorn -f"
echo "  - Reiniciar: sudo systemctl restart gunicorn"
echo "  - Estado: sudo systemctl status gunicorn"
echo ""
echo -e "${GREEN}Próximos pasos:${NC}"
echo "  1. Crear superusuario: sudo -u declarador $PROJECT_DIR/venv/bin/python $PROJECT_DIR/manage.py createsuperuser"
echo "  2. Visitar: https://$DOMAIN"
echo "  3. Probar la búsqueda de declaraciones"
echo ""
echo "================================================================="

