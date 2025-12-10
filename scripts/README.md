# Scripts de Instalación - Declarador.io

Esta carpeta contiene scripts de automatización para facilitar la instalación y mantenimiento del proyecto.

## Scripts Disponibles

### install_production.sh

Script de instalación automatizada para Ubuntu Server con Nginx y PostgreSQL.

**Uso**:

```bash
# 1. Clonar el proyecto primero
git clone <repo-url> /home/declarador/declarador.io

# 2. Ejecutar como root
sudo bash /home/declarador/declarador.io/scripts/install_production.sh
```

**Lo que hace**:
- Instala todas las dependencias necesarias
- Configura PostgreSQL con base de datos y usuario
- Crea entorno virtual Python
- Instala dependencias Python y Node.js
- Compila Tailwind CSS
- Crea archivo `.env` con configuración
- Aplica migraciones de Django
- Configura Gunicorn como servicio systemd
- Configura Nginx como proxy reverso
- Instala y configura SSL con Let's Encrypt
- Configura firewall UFW

**Requisitos**:
- Ubuntu 20.04 o superior
- Acceso root
- Dominio apuntando al servidor
- Proyecto ya clonado en `/home/declarador/declarador.io`

**Después de ejecutar**:
1. Crear superusuario: 
   ```bash
   sudo -u declarador /home/declarador/declarador.io/venv/bin/python /home/declarador/declarador.io/manage.py createsuperuser
   ```
2. Visitar tu dominio: `https://tudominio.com`

## Personalización

Si necesitas personalizar la instalación:

1. Copia el script
2. Modifica las variables según tus necesidades
3. Ejecuta tu versión personalizada

## Solución de Problemas

Si el script falla:

1. Lee el mensaje de error
2. Verifica los logs: `sudo journalctl -u gunicorn`
3. Consulta `docs/DEPLOY_UBUNTU.md` para instalación manual
4. Verifica que el proyecto esté clonado en `/home/declarador/declarador.io`

## Próximos Scripts (Planificados)

- `backup_database.sh` - Backup automático de PostgreSQL
- `update_app.sh` - Actualización automática de la aplicación
- `health_check.sh` - Verificación de estado del servidor

---

**Documentación Completa**: Ver `docs/DEPLOY_UBUNTU.md`

