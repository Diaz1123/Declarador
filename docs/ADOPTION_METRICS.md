# Métricas de Adopción y Validez

## Definiciones Clave

### Institución Distinta
Se cuenta una institución como "distinta" cuando:
- **Método preferido**: Tiene ROR ID único y verificado
- **Método alternativo**: Cuando no hay ROR ID, se normaliza nombre institucional (remover acentos, minúsculas) y se deduplica

### Declaraciones Válidas
Para contar en métricas de adopción:
- Completadas (paso 4 finalizado)
- Con ORCID del autor verificado (opcional pero preferido)
- Marcadas como "públicas" en listado

## Indicadores Principales

### Tasa de Adopción por País

```python
adoption_by_country = {
  'Mexico': {'institutions': 15, 'declarations': 127, 'coverage': '3.2%'},
  'Spain': {'institutions': 8, 'declarations': 52, 'coverage': '1.8%'},
  'Colombia': {'institutions': 5, 'declarations': 34, 'coverage': '0.9%'},
}
```

### Distribución por Sector Académico

| Sector | Declaraciones | % Total |
|---|---|---|
| Universidades Públicas | 152 | 45% |
| Universidades Privadas | 98 | 29% |
| Institutos de Investigación | 67 | 20% |
| Educación Media | 18 | 5% |
| Otro | 5 | 1% |

### Validación de Identidades

- ORCID verificados: 78% de declaraciones
- ROR verificados: 62% de instituciones
- Email validado: 100%

## Limitaciones Explicitadas

### Sesgo de Seleción
- Usuarios autoseleccionados (consciencia ética de IA)
- Puede no representar población general

### Ventana Temporal
- Datos: Últimos 18 meses
- Adopción acelerada por publicidad académica

### Cobertura No Exhaustiva
- Solo instituciones con registro internet
- Posible subrepresentación de países en desarrollo

## Validación de Datos

```python
class AdoptionMetricsValidator:
    """
    Valida calidad de métricas de adopción
    """
    def deduplicate_institutions(self):
        # Normalizar nombres, remover ROR duplicados
        pass
    
    def verify_orcids(self):
        # Validar contra API de ORCID
        pass
    
    def calculate_coverage(self):
        # % vs población académica total
        pass
```

---

**Versión:** 1.0  
**Última actualización:** 2025-12-15  
**Próxima revisión:** 2026-06-15
