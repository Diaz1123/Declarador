# API Pública REST - Especificación v1.0

## Endpoints Principales

### GET /api/v1/declarations/{id}

Obtiene una declaración por ID.

**Parámetros:**
- `id` (path, requerido): ID único de declaración
- `format` (query, opcional): json|xml|txt (default: json)

**Rate Limit:** 100 req/min

**Respuesta (200):**
```json
{
  "declaration_id": "ABC12345",
  "status": "published",
  "version": "1.0.0",
  "schemaVersion": "1.0.0",
  "softwareVersion": "4.0.0",
  "ai_tool_name": "ChatGPT",
  "human_review_level": 3,
  "usage_types": ["draft", "writing-support"],
  "created_at": "2025-12-15T10:30:00Z"
}
```

### GET /api/v1/verify/{hash}

Verifica integridad de declaración por hash SHA-256.

**Respuesta:**
```json
{
  "valid": true,
  "declaration_id": "ABC12345",
  "hash": "A1B2C3D4E5F6A7B8",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

### GET /api/v1/declarations

Búsqueda y listado de declaraciones.

**Parámetros Query:**
- `usage_type`: Filtrar por tipo de uso
- `review_level__gte`: Nivel de revisión mínimo
- `limit`: Resultados por página (default: 20, max: 100)
- `offset`: Paginación

## Códigos HTTP

| Código | Significado |
|---|---|
| 200 | OK |
| 400 | Solicitud inválida |
| 404 | No encontrado |
| 429 | Límite de rate exceed |
| 500 | Error servidor |

## Autenticación

Opcional con API Key:
```bash
curl -H "Authorization: Bearer {api_key}" \
  https://declarador.io/api/v1/declarations/{id}
```

---

**Versión API:** 1.0  
**Última actualización:** 2025-12-15
