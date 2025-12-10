# Configuración de reCAPTCHA v2

Este documento describe cómo configurar reCAPTCHA v2 en la aplicación Declarador.

## Obtener las keys de reCAPTCHA

1. Ve a [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en el botón "+" para crear un nuevo sitio
4. Configura tu sitio:
   - **Label**: Nombre descriptivo (ej: "Declarador - usoeticoia.org")
   - **reCAPTCHA type**: Selecciona "reCAPTCHA v2" → "I'm not a robot" Checkbox
   - **Domains**: Agrega tus dominios (ej: `usoeticoia.org`, `localhost` para desarrollo)
   - Acepta los términos de servicio
5. Haz clic en "Submit"
6. Copia tus keys:
   - **Site Key** (clave pública)
   - **Secret Key** (clave secreta)

## Configuración en la aplicación

### 1. Archivo `.env`

Crea o edita tu archivo `.env` en la raíz del proyecto:

```env
# reCAPTCHA v2 Configuration
RECAPTCHA_SITE_KEY=tu_site_key_aqui
RECAPTCHA_SECRET_KEY=tu_secret_key_aqui
RECAPTCHA_ENABLED=True
```

**Nota**: Para desarrollo local, puedes usar las keys de prueba de Google:
- Site Key: `6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI`
- Secret Key: `6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe`

Estas keys de prueba **siempre pasan** la validación en cualquier dominio.

### 2. Deshabilitar reCAPTCHA (opcional)

Si deseas deshabilitar reCAPTCHA temporalmente (por ejemplo, en desarrollo):

```env
RECAPTCHA_ENABLED=False
```

## Ubicación de reCAPTCHA en la aplicación

reCAPTCHA se muestra en los siguientes lugares:

### 1. Paso 1 del Declarador (`/paso1/`)
- Se muestra en la barra de acción inferior
- El botón "Siguiente" está deshabilitado hasta que se complete el desafío
- La verificación se guarda en la sesión para no volver a pedirla

### 2. Paso 1 del Registro de Firmantes (`/firmar/`)
- Se muestra en el paso 1 del formulario de registro
- El botón "Continuar" está deshabilitado hasta que se complete el desafío
- La verificación se guarda en sessionStorage del navegador

### 3. Validación en Backend
- El paso 1 de declaraciones valida el token en `core/views/declarations.py`
- El registro de firmantes valida el token en `core/views/signers.py`
- Si la validación falla, se retorna un error al usuario

## Comportamiento del reCAPTCHA

### Frontend
- El widget de reCAPTCHA se renderiza automáticamente si está habilitado
- Al completar el desafío, se ejecuta la función `onRecaptchaSuccess()`
- Esta función:
  - Habilita el botón de envío
  - Guarda el token en sessionStorage
  - Marca la verificación como completada

### Backend
- La función `verify_recaptcha()` en `core/utils.py` envía el token a la API de Google
- Google verifica:
  - Que el token sea válido
  - Que no haya expirado (2 minutos de validez)
  - Que provenga del dominio correcto
- Si `RECAPTCHA_ENABLED=False`, la verificación siempre pasa

## Códigos de error comunes

- `missing-input-response`: No se proporcionó el token de reCAPTCHA
- `invalid-input-response`: El token es inválido o ha expirado
- `timeout-or-duplicate`: El token ya fue usado o expiró
- `connection-error`: No se pudo conectar con la API de Google

## Testing

### Desarrollo Local
1. Usa las keys de prueba de Google (ver arriba)
2. O desactiva reCAPTCHA: `RECAPTCHA_ENABLED=False`

### Producción
1. Asegúrate de usar tus keys reales
2. Verifica que tu dominio esté configurado en la consola de reCAPTCHA
3. Monitorea los logs para detectar intentos de fraude

## Arquitectura

```
┌─────────────────┐
│   Frontend      │
│  (Template)     │
│                 │
│  1. Usuario     │
│     completa    │
│     reCAPTCHA   │
│                 │
│  2. Callback    │
│     guarda      │
│     token       │
└────────┬────────┘
         │
         │ Token
         ▼
┌─────────────────┐
│   Backend       │
│   (Django)      │
│                 │
│  3. Extrae      │
│     token del   │
│     request     │
│                 │
│  4. Llama       │
│     verify_     │
│     recaptcha() │
└────────┬────────┘
         │
         │ Token + IP
         ▼
┌─────────────────┐
│  Google API     │
│                 │
│  5. Verifica    │
│     token       │
│                 │
│  6. Retorna     │
│     success:    │
│     true/false  │
└────────┬────────┘
         │
         │ Resultado
         ▼
┌─────────────────┐
│   Backend       │
│                 │
│  7. Procesa     │
│     respuesta   │
│                 │
│  8. Continúa    │
│     o rechaza   │
└─────────────────┘
```

## Mantenimiento

- Las keys de reCAPTCHA no expiran
- Puedes regenerarlas desde la consola de Google si es necesario
- Monitorea el tráfico en la consola de reCAPTCHA para detectar patrones sospechosos
- Google proporciona análisis de uso y detección de bots

## Soporte

Si tienes problemas:
1. Verifica que las keys sean correctas
2. Confirma que el dominio esté autorizado
3. Revisa los logs de Django para errores específicos
4. Consulta la [documentación oficial de reCAPTCHA](https://developers.google.com/recaptcha/docs/display)
