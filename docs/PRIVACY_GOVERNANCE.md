# Gobernanza y Privacidad de Datos

## Introducción

Este documento especifica los protocolos de tratamiento de datos sensibles en Declarador, incluyendo:
- Flujos de datos según modo de uso (descarga local vs. registro en plataforma)
- Tratamiento de prompts y información identificable
- Minimización de datos en listados públicos
- Conformidad con RGPD, LGPD y normativas mexicanas de privacidad

---

## 1. Flujos de Datos

### Ruta 1: Descarga Local (Sin Conexión a Servidor)

**Características:**
- Declaración generada en navegador del usuario
- JSON exportado localmente a máquina del usuario
- Ningún envío de datos a servidores Declarador
- Duración de retención: Indefinida (bajo control del usuario)

**Datos incluidos:**
```json
{
  "declarationType": "academic-ai-transparency",
  "version": "1.0.0",
  "usage_types": [...],
  "ai_tool_name": "...",
  "ai_tool_version": "...",
  "specific_purpose": "...",
  "prompts": [...],
  "human_review_level": 0-5
}
```

**Responsabilidad:** Completamente del usuario (cifrado, almacenamiento, distribución)

---

### Ruta 2: Registro en Plataforma (Con Base de Datos)

**Infraestructura:**
- Base de Datos: PostgreSQL 13+ con TLS 1.3+
- Cifrado en tránsito: HTTPS obligatorio
- Cifrado en reposo: Recomendado (AES-256)
- Retención máxima: 7 años

**Campos opcionales enviados a servidor:**
```python
optional_fields = {
    'reviewer_name': String(200),      # Nombre revisor humano
    'reviewer_role': String(200),      # Rol (ej: "profesor", "asesor")
    'prompts': JSON,                   # Lista de prompts utilizados
    'public_listing': Boolean          # ¿Incluir en listado público?
}
```

**Acceso:**
- Propietario de la declaración: Acceso completo
- Administradores Declarador: Auditoría y mantenimiento
- Público: Solo si `public_listing = True` y datos redactados

---

## 2. Tratamiento de Prompts

### Riesgos Identificados

Los prompts pueden contener:
- **PII (Personally Identifiable Information)**: Nombres, emails, teléfono
- **Datos confidenciales**: Información de investigación no publicada
- **IP Comercial**: Detalles de productos/metodologías propietarias
- **Contexto sensible**: Identificación de individuos o grupos vulnerables

### Controles de Privacidad

**1. Checkbox "Guardar Prompts" (Descheckeado por defecto)**
```html
<input 
  type="checkbox" 
  name="save_prompts" 
  id="save_prompts"
  unchecked
  aria-label="Guardar prompts en servidor (requiere verificación de contenido)"
>
```

**2. Redacción Automática Pre-guardado**

Antes de enviar a base de datos, ejecutar automáticamente:
```python
def redact_sensitive_data(prompts_list):
    """
    Redacta información sensible de lista de prompts
    """
    patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'(?:\+34|0034|0)[6789]\d{8}|\+1[0-9]{10}',  # España, México, USA
        'ssn': r'\d{3}-\d{2}-\d{4}',  # US SSN format
        'rfc': r'[A-ZÑ]{3,4}\d{6}[HM][A-Z0-9]{3}',  # RFC México
        'orcid': r'\d{4}-\d{4}-\d{4}-\d{3}[0-9X]'
    }
    
    redacted = []
    for prompt in prompts_list:
        text = prompt['description']
        for pattern_type, regex in patterns.items():
            text = re.sub(regex, f'[REDACTED_{pattern_type.upper()}]', text)
        redacted.append({'description': text})
    
    return redacted
```

**3. Restricciones de Cantidad y Tamaño**
- Máximo 10 prompts por declaración
- Máximo 300 caracteres por prompt
- Máximo 10 KB total de prompts

**4. Advertencia Explícita Pre-Guardado**
```
⚠️ ADVERTENCIA DE PRIVACIDAD

Está a punto de guardar prompts en nuestros servidores.
Verifique que NO contenga:
  ✗ Nombres de personas reales
  ✗ Emails o teléfonos
  ✗ Números de identificación (RFC, CURP, SSN)
  ✗ Información confidencial de investigación
  ✗ Datos de terceros sin consentimiento

Una vez guardado, los prompts serán visibles en el listado
público SI marca "Incluir en listado público".

[Entiendo los riesgos - Continuar] [Cancelar]
```

**5. Auditoría Posterior a Guardado**
- Log automático de prompts guardados (sin mostrar contenido)
- Retención de auditoría: 12 meses
- Acceso solo para administradores

---

## 3. Minimización en Listados Públicos

### Campos Públicos vs. Privados

**Estructura Django (models.py):**
```python
class Signer(models.Model):
    # Campos SIEMPRE PÚBLICOS (si public_listing=True)
    full_name = models.CharField(max_length=200)                # Nombre completo
    affiliation = models.CharField(max_length=300)              # Institución
    
    # Campos PÚBLICOS SOLO SI VERIFICADOS
    affiliation_ror_id = models.CharField(max_length=200)       # ROR ID verificado
    orcid = models.CharField(max_length=19)                      # ORCID verificado
    orcid_verified = models.BooleanField(default=False)
    
    # Campos SIEMPRE PRIVADOS
    email = models.EmailField()                                  # Nunca público
    country = models.CharField(max_length=100, null=True)       # Nunca público
    
    # Configuración de privacidad
    public_listing = models.BooleanField(default=True)
    
    # Métodos de filtrado
    def get_public_profile(self):
        """Retorna solo campos públicos para listado"""
        if not self.public_listing:
            return None
        
        return {
            'full_name': self.full_name,
            'affiliation': self.affiliation,
            'affiliation_ror_id': self.affiliation_ror_id if self.affiliation_ror_id else None,
            'orcid': self.orcid if self.orcid_verified else None,
            'url': self.get_verification_url()
        }
```

### Listado Público - Ejemplo Renderizado

```html
<!-- VISIBLE -->
<div class="signer-card">
  <h4>Dr. Juan García López</h4>
  <p>Colegio de México</p>
  <p class="identifiers">
    <a href="https://ror.org/00pd74e60">ROR: 00pd74e60</a>
    <a href="https://orcid.org/0000-0001-2345-6789">ORCID: 0000-0001-2345-6789</a>
  </p>
</div>

<!-- OCULTO -->
juan.garcia@colmex.mx        <!-- Email: nunca visible -->
Mexico                         <!-- País: nunca visible -->
SSN/RFC: [privado]             <!-- Identificadores: nunca visibles -->
```

---

## 4. Período de Retención de Datos

### Timeline por Tipo de Dato

| Tipo de Dato | Retención | Justificación |
|---|---|---|
| Declaración completa | 7 años | Cumplimiento normativo académico |
| Prompts guardados | 5 años | Auditabilidad, análisis de tendencias |
| Logs de acceso | 12 meses | Seguridad, detección de anomalías |
| Datos de sesión | 30 días | Análisis de uso y UX |
| Cookies de seguimiento | 3 meses | Funcionalidad de sesión |

### Derecho al Olvido (RGPD Art. 17)

**Solicitud de eliminación:**
1. Usuario envía solicitud a: `privacy@declarador.io`
2. Equipo verifica identidad (último ORCID/email registrado)
3. Plazo de respuesta: 30 días
4. Alcance:
   - ✅ Eliminación de perfil (nombre, email, afiliación)
   - ✅ Eliminación de declaraciones no públicas
   - ❌ NO se eliminan declaraciones ya publicadas (responsabilidad autores)

---

## 5. Conformidad Normativa

### México - Ley Federal de Protección de Datos Personales (LFPDPP)
- ✅ Consentimiento expreso para recopilación
- ✅ Propósito específico (validación académica)
- ✅ Minimización de datos
- ✅ Derecho al acceso, rectificación y cancelación

### RGPD (Cuando aplique)
- ✅ Avisos de privacidad (Art. 13/14)
- ✅ Base legal de tratamiento (consentimiento)
- ✅ Derecho al olvido (Art. 17)
- ✅ Portabilidad de datos (Art. 20)

### LGPD Brasil (Si incluye usuários)
- ✅ Consentimiento explícito
- ✅ Propósito definido
- ✅ Retención determinada

---

## 6. Implementación Técnica

### Variables de Entorno (Django settings.py)

```python
# Privacy Settings
PRIVACY_RETENTION_DAYS = 2555  # 7 años
PROMPTS_RETENTION_DAYS = 1825  # 5 años
LOG_RETENTION_DAYS = 365

# TLS/Security
SSL_REDIRECT = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database Encryption
DB_ENCRYPTION_KEY = os.getenv('DB_ENCRYPTION_KEY')
DB_ENCRYPTION_ALGORITHM = 'AES-256-GCM'

# Data Anonymization Cron
ANONYMIZATION_CRON_ENABLED = True
ANONYMIZATION_CRON_HOUR = 2  # 2 AM UTC
```

### Tareas Programadas (Celery)

```python
from celery import shared_task
from datetime import timedelta
from django.utils import timezone

@shared_task
def anonymize_expired_data():
    """
    Anonimiza datos que superan período de retención
    Ejecuta diariamente a las 2 AM UTC
    """
    cutoff_date = timezone.now() - timedelta(
        days=settings.PRIVACY_RETENTION_DAYS
    )
    
    # Anonimizar declaraciones
    old_declarations = Declaration.objects.filter(
        created_at__lt=cutoff_date,
        is_anonymized=False
    )
    
    for declaration in old_declarations:
        declaration.anonymize()
        declaration.save()
    
    # Eliminar logs antiguos
    old_logs = AuditLog.objects.filter(
        created_at__lt=cutoff_date - timedelta(days=365)
    ).delete()
    
    return f"Anonimizadas {old_declarations.count()} declaraciones"
```

---

## 7. Contacto y Reportes

**Consultas de privacidad:** `privacy@declarador.io`
**Reportes de incidente:** `security@declarador.io`
**Tiempo de respuesta:** 48 horas máximo

---

## Historial de Cambios

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2025-12-15 | Documento inicial |
