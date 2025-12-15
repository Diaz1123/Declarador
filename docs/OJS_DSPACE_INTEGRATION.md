# Interoperabilidad: OJS/DSpace Integration

## Mapeo Dublin Core

Declarador implementa el estándar Dublin Core para asegurar interoperabilidad con repositorios académicos.

### Campos Mapeados

| Campo Declarador | Dublin Core | Tipo | Obligatorio |
|---|---|---|---|
| declaration_id | dc:identifier | String | Sí |
| declaration_type | dc:type | academic-ai-transparency | Sí |
| ai_tool_name | dc:subject | String | Sí |
| human_review_level | dc:coverage.review | Integer (0-5) | Sí |
| usage_types | dc:type.content | Array (enum) | Sí |
| created_at | dc:issued | ISO8601 | Sí |
| reviewer_name | dc:contributor | String | No |
| license | dc:rights | String | No |

## Exportación XML (OJS)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<article>
  <metadata>
    <dc:identifier>{declaration_id}</dc:identifier>
    <dc:type>academic-ai-transparency</dc:type>
    <dc:coverage.review>{human_review_level}</dc:coverage.review>
    <dc:subject>{ai_tool_name}</dc:subject>
    <dc:subject>{usage_types_joined}</dc:subject>
    <dc:issued>{created_at_iso}</dc:issued>
    <dc:contributor>{reviewer_name}</dc:contributor>
    <dc:rights>{license}</dc:rights>
  </metadata>
</article>
```

## Integración DSpace

Declarador puede ser integrado como plugin de metadata extractor en DSpace.

### Configuración (dspace.cfg)

```properties
metadata.extractor.plugin.declarador.enabled = true
metadata.extractor.plugin.declarador.url = https://declarador.io/api/v1/declarations
metadata.extractor.plugin.declarador.timeout = 5000
metadata.extractor.plugin.declarador.cache_ttl = 3600
```

## API REST para Repositorios

### GET /api/v1/declarations/{id}.json

Retorna declaración en formato canónico JSON-LD.

```json
{
  "@context": "https://www.w3.org/2018/jsonld/context",
  "@id": "https://declarador.io/declarations/{id}",
  "@type": "academic-ai-transparency",
  "identifier": "{declaration_id}",
  "subject": "{ai_tool_name}",
  "coverage": {"review": {level: 0-5}},
  "created": "{created_at}"
}
```

### GET /api/v1/declarations/{id}.xml (Dublin Core)

Retorna metadata en formato OAI-PMH compatible.

## Referencias

- [Dublin Core Metadata Initiative](https://www.dublincore.org/)
- [OJS Plugin Architecture](https://docs.pkp.sfu.ca/dev/plugin-guide/)
- [DSpace Metadata Architecture](https://wiki.lyrasis.org/display/DSDOC7x/)

---

**Versión:** 1.0  
**Última actualización:** 2025-12-15
