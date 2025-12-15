# Versionado y Compatibilidad - Declarador

## Resumen Ejecutivo

Este documento establece tres sistemas de versionado independientes para evitar ambigüedad y facilitar mantenimiento:

1. **Versión del Whitepaper/Documento**: 1.0 (Preprint)
2. **Versión del Schema JSON**: 1.0.0
3. **Versión del Software (Django)**: 4.0.0

---

## 1. Versión del Whitepaper/Documento

### Definición
Version del documento académico/especificación (manuscript/paper).

### Patrón
- Preprint (versión inicial)
- 1.0, 2.0, etc. (versiones después de peer review)

### Ubicación
- README.md: "Versión 1.0 – Preprint"
- Publicaciones académicas
- Header del documento

### Cambios que incrementan versión
- Nueva revisión sustancial del diseño del standard
- Incorporación de feedback de peer review
- Cambios en la filosofía o alcance del proyecto

---

## 2. Versión del Schema JSON

### Definición
Version de la especificación canónica de estructura de datos JSON.

### Ubicación
- `core/schema.json`: Campo `$id` = `https://declarador.io/schema/declaration/vX.Y.Z`
- `core/utils.py`: Campo `schemaVersion` en `generate_declaration_json()`

### Patrón Semántico
```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking change (cambio incompatible con versiones anteriores)
  - Ejemplo: Cambiar rango de `humanReview.level` de 0-6 a 0-5
  - Ejemplo: Hacer obligatorio un campo antes opcional
  - **Acción**: Todos los clientes DEBEN actualizar

- **MINOR**: Backward compatible (cambio no-breaking)
  - Ejemplo: Añadir campo opcional nuevo
  - Ejemplo: Aumentar límite de caracteres
  - **Acción**: Clientes pueden optar por actualizar

- **PATCH**: Bug fix
  - Ejemplo: Corregir descripción de campo
  - Ejemplo: Ajustar validación de regex
  - **Acción**: Recomendado actualizar

### Tabla de Compatibilidad

| Cambio | MAJOR | MINOR | PATCH | Ejemplo |
|--------|-------|-------|-------|----------|
| Nuevo campo requerido | ✓ | | | Cambiar `license` de opcional a requerido |
| Nuevo campo opcional | | ✓ | | Añadir `complianceNotes` |
| Cambiar tipo dato | ✓ | | | `level` de string a integer |
| Cambiar enum values | ✓ | | | Eliminar valor de humanReview level |
| Cambiar rango validación | ✓ | | | Cambiar minimum de 0 a 1 |
| Bug en schema | | | ✓ | Regex incorrecto en pattern |
| Nueva descripción | | | ✓ | Aclarar qué significa un campo |
| Deprecar campo | | ✓ | | Añadir nota pero mantener soporte |

---

## 3. Versión del Software (Django)

### Definición
Version del aplicativo Django (releases del proyecto).

### Ubicación
- `CHANGELOG.md`
- GitHub Releases / Tags (ej: `v4.0.0`)
- `package.json`: `"version"`

### Patrón Semántico
```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking change en código/API
  - Migraciones de BD incompatibles
  - Cambios en endpoints públicos

- **MINOR**: New features backward compatible
  - Nuevas vistas
  - Mejoras de rendimiento
  - Nuevas traducciones

- **PATCH**: Bug fixes
  - Correcciones de seguridad
  - Arreglos de UI

---

## Matriz de Relaciones

```
Whitepaper v1.0 (Preprint)
    ↓
Define specificación de
    ↓
Schema v1.0.0
    ↓
Implementada en
    ↓
Software v4.0.0
```

### Ejemplo de Evolución

**Iteración 1**
- Whitepaper: 1.0 (Preprint)
- Schema: 1.0.0
- Software: 4.0.0
- Estado: Inicial

**Iteración 2 (Bug en hash)**
- Whitepaper: 1.0 (Preprint) ← Sin cambios
- Schema: 1.0.0 ← Sin cambios
- Software: 4.0.1 ← PATCH
- Estado: Bug fix

**Iteración 3 (Feedback de peer review)**
- Whitepaper: 2.0 ← Cambio sustancial
- Schema: 2.0.0 ← MAJOR (humanReview level ahora 0-5)
- Software: 5.0.0 ← MAJOR
- Estado: Revisado y mejorado

**Iteración 4 (Nueva feature opcional)**
- Whitepaper: 2.0 ← Sin cambios
- Schema: 2.1.0 ← MINOR (campo new optional)
- Software: 5.1.0 ← MINOR
- Estado: Feature nueva

---

## Política de Deprecación

### Soporte de Versiones Previas

- **Actual**: Recibe todas las actualizaciones
- **N-1**: Recibe bug fixes de seguridad crítica
- **N-2 y anteriores**: Fin de soporte

### Anuncio de Deprecación

```markdown
## DEPRECATED (Schema v1.0.0)

Schema v1.0.0 deprecated desde [fecha].
Migra a v2.0.0: [enlace a guía de migración].
Soporte termina: [fecha].
```

---

## Roadmap Futuro

### Schema v2.0.0 (Próximo MAJOR)
- Humanize level scale: cambiar a 0-5 (eliminar nivel 6)
- Soporte multiidioma en metadata (i18n)
- Campo de conformidad normativa explícita

### Software v5.0.0 (Próximo MAJOR)
- Integración nativa OJS
- API REST con autenticación
- Interfaz web mejorada (frontend framework)

---

## Referencias

- [Semantic Versioning](https://semver.org/)
- [JSON Schema Versioning](https://json-schema.org/)
- [Django Release Cycle](https://docs.djangoproject.com/en/stable/releases/)
