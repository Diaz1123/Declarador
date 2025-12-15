# Guía de Implementación - Revisión de Pares Ciego

## Introducción

Este documento consolida todos los cambios derivados del diagnóstico de revisión de pares ciego. Cada sección corresponde a una observación crítica o mayor.

---

## PUNTO 1: Coherencia Interna del Modelo (CRÍTICO)

### 1.1 Escala de Revisión Humana

**PROBLEMA**: Conflicto entre constants.py (0-6) y JSON Schema (0-5).

**SOLUCIÓN**:
1. Actualizar `core/constants.py`: Eliminar nivel 6
2. Validar `core/models.py`: Agregar validadores MinValueValidator(0), MaxValueValidator(5)
3. JSON Schema en `core/schema.json` define: humanReview.level entre 0 y 5

✅ **IMPLEMENTADO**: core/schema.json

### 1.2 Formatos JSON (Español vs Inglés)

**PROBLEMA**: Duplicidad de claves (español en cuerpo, inglés en JSON).

**SOLUCIÓN**:
- **Formato CANÓNICO**: Inglés (keys en utils.py generate_declaration_json())
- **Estructura**: 
  - declarationType
  - version (payload: 1.0.0)
  - schemaVersion (schema: 1.0.0)
  - softwareVersion (software: 4.0.0)
  - usage.types, tool.*, humanReview.*

**CAMBIOS en core/utils.py** (línea ~170):
```python
# CAMBIAR:
'version': '4.0.0',

# POR:
'version': '1.0.0',  # Payload semantic version
'schemaVersion': '1.0.0',  # Schema specification version  
'softwareVersion': '4.0.0',  # Django release version
```

✅ **IMPLEMENTADO**: Documentado en schema.json

---

## PUNTO 2: Versionado Explícito

**PROBLEMA**: Ambigüedad entre versiones (whitepaper vs schema vs software).

**SOLUCIÓN**: Tres sistemas independientes con semantic versioning.

✅ **IMPLEMENTADO**: docs/VERSIONADO_Y_COMPATIBILIDAD.md

**Resumen**:
- **Whitepaper**: v1.0 (Preprint)
- **Schema JSON**: v1.0.0 (con breaking/non-breaking changes)
- **Software Django**: v4.0.0 (con MAJOR.MINOR.PATCH)

---

## PUNTO 3: Criptografía SHA-256

**PROBLEMA**: Especificación insuficiente de canonicalización y justificación.

**SOLUCIÓN**:
1. SHA-256 truncado a 16 caracteres hexadecimales en mayúsculas
2. Canonicalización: UTF-8, LF (no CRLF), orden de campos definido
3. Justificación: 64 bits suficiente para detección accidental; migración futura a 256 bits

**Verificación manual** (Linux/Mac):
```bash
msg="contenido canonizado"
printf "%s" "$msg" | sha256sum | cut -c1-16 | tr '[:lower:]' '[:upper:]'
```

**Ejemplo en Python**:
```python
import hashlib

def compute_hash(message):
    """SHA-256 truncado a 16 caracteres mayúsculas"""
    return hashlib.sha256(message.encode('utf-8')).hexdigest()[:16].upper()

# Ya implementado en core/utils.py línea 19
```

---

## PUNTO 4: Metodología Normativa

**PROBLEMA**: Falta de protocolo de revisión sistemática y matriz comparativa.

**SOLUCIÓN**:
Crear `docs/NORMATIVE_ANALYSIS.md` con:
- Bases consultadas (COPE, ICMJE, UNESCO, PubMed, SCOPUS)
- Período de revisión: 2020-2025
- Criterios inclusión/exclusión
- Matriz comparativa de políticas:

| Política | Exige Declaración | Prohíbe Autoría | Pide Prompts | Exige Revisión | Alcance |
|----------|-------------------|-----------------|--------------|----------------|----------|
| COPE | Sí | No | Opcional | Sí | Manuscritos |
| ICMJE | Sí | Limitado | No | Sí | Medios |
| UNESCO | Recomendado | Analizar | Sí | Sí | Educación |

**PENDIENTE**: Crear archivo NORMATIVE_ANALYSIS.md

---

## PUNTO 5: Adopción y Validez

**PROBLEMA**: Claims sin sustento de "recepción internacional favorable".

**SOLUCIÓN**:
1. Reescribir como "señales preliminares" en README
2. Documentar limitaciones: sesgo, auto-selección, ventana temporal
3. Crear `docs/ADOPTION_METRICS.md` con:
   - Fuente de datos (autodeclaración vs validado)
   - Deduplicación
   - Validación ROR/ORCID
   - Definición "instituciones distintas"

**PENDIENTE**: Crear archivo ADOPTION_METRICS.md

---

## PUNTO 6: Gobernanza y Privacidad

**PROBLEMA**: Insuficiente documentación de tratamiento de datos sensibles (prompts, ORCID, etc).

**SOLUCIÓN**:
Crear `docs/PRIVACY_GOVERNANCE.md` con:

### 6.1 Flujos de Datos

**Ruta 1: Descarga Local**
- JSON almacenado localmente
- Ningún envío a servidor
- Duración: indefinida

**Ruta 2: Registro Plataforma**
- BD PostgreSQL (TLS 1.3+)
- Retención: 7 años
- Campos opcionales: reviewer_name, reviewer_role, prompts

### 6.2 Tratamiento de Prompts

**Riesgos**: PII, datos confidenciales, IP

**Controles**:
- Checkbox "Guardar prompts" UNCHECKED por defecto
- Redacción automática de emails/SSN
- Campo "Prompts" con máximo 10 items
- Advertencia explícita antes de guardar

### 6.3 Minimización en Listados Públicos

```python
# En models.py Signer:
public_fields = {
    'full_name': True,
    'affiliation': True,  # Solo nombre
    'affiliation_ror_id': False,  # ROR opcional
    'orcid': False,  # Si verificado
    'email': False,  # Privado
    'declaration': False,  # Privado
}
```

**PENDIENTE**: Crear archivo PRIVACY_GOVERNANCE.md

---

## PUNTO 7: Interoperabilidad OJS/DSpace

**PROBLEMA**: Falta mapeo específico y ejemplos implementables.

**SOLUCIÓN**:
Crear `docs/OJS_DSPACE_INTEGRATION.md` con:

### 7.1 Mapeo Dublin Core

| Campo Django | Dublin Core | Valores |
|--------------|-------------|----------|
| ai_tool_name | dc.subject | Texto libre |
| human_review_level | dc.coverage.review | 0-5 |
| usage_types | dc.type.content | enum list |
| declaration_id | dc.identifier | unique |

### 7.2 Perfil Mínimo OJS

```xml
<dcterms:declaration>
  <dc:identifier>{declaration_id}</dc:identifier>
  <dc:type>academic-ai-transparency</dc:type>
  <dc:coverage>{human_review_level}</dc:coverage>
  <dc:subject>{usage_types}</dc:subject>
</dcterms:declaration>
```

**PENDIENTE**: Crear archivo OJS_DSPACE_INTEGRATION.md

---

## PUNTO 8: API Pública

**PROBLEMA**: Especificación incompleta de API REST.

**SOLUCIÓN**:
Crear `docs/API_SPECIFICATION.md` con:

### 8.1 Endpoints Mínimos

```
GET /api/v1/declarations/{id}.json
  - Retorna declaración en formato canónico
  - Rate limit: 100 req/min
  - CORS: *

GET /api/v1/verify/{hash}
  - Verifica integridad
  - Retorna {valid: bool, declaration_id, timestamp}

GET /api/v1/declarations/{id}.txt
  - Formato texto (compatibilidad)
```

**PENDIENTE**: Crear archivo API_SPECIFICATION.md

---

## Checklist de Implementación

### COMPLETADOS ✅
- [x] JSON Schema v1.0.0 con rango humanReview 0-5
- [x] Versionado y compatibilidad documentados
- [x] Estructura canónica JSON definida

### PENDIENTES ⏳
- [ ] Actualizar core/constants.py: Eliminar nivel 6
- [ ] Agregar validadores en core/models.py
- [ ] Actualizar core/utils.py: Agregar schemaVersion y softwareVersion
- [ ] Crear docs/NORMATIVE_ANALYSIS.md
- [ ] Crear docs/ADOPTION_METRICS.md
- [ ] Crear docs/PRIVACY_GOVERNANCE.md
- [ ] Crear docs/OJS_DSPACE_INTEGRATION.md
- [ ] Crear docs/API_SPECIFICATION.md
- [ ] Actualizar README.md: Reescribir claims de adopción
- [ ] Actualizar CHANGELOG.md: Documentar cambios

---

## Próximos Pasos

1. **Corto Plazo** (Esta semana):
   - Implementar cambios en models.py y utils.py
   - Actualizar README con versionado claro

2. **Mediano Plazo** (Este mes):
   - Crear documentación faltante
   - Validar con peers

3. **Largo Plazo** (Q1 2026):
   - Implementar API pública
   - Integración OJS/DSpace
   - Release v2.0.0 del schema

---

## Contacto y Preguntas

Para dudas sobre implementación, consultar:
- Issues de GitHub
- Diskusiones del proyecto
- Documentación en `/docs`
