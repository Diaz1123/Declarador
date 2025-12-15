"""
Constants for the AI Declaration application
Migrated from usoeticoia.org constants.ts
"""

USAGE_TYPES = [
    {
        'value': 'draft',
        'label': 'Generación de Borrador',
        'hint': 'La IA escribió una primera versión completa o secciones sustanciales que sirvieron de base.',
        'examples': ['Generación de introducción para un paper', 'Redacción de correos formales', 'Primer borrador de capítulos teóricos']
    },
    {
        'value': 'coauthor',
        'label': 'Co-creación Sustantiva',
        'hint': 'Colaboración iterativa donde la IA y el humano construyen argumentos o narrativas conjuntamente.',
        'examples': ['Diálogo socrático para refinar argumentos', 'Expansión de puntos clave definidos por el humano', 'Desarrollo de escenarios hipotéticos']
    },
    {
        'value': 'writing-support',
        'label': 'Asistencia de Estilo y Redacción',
        'hint': 'Mejora de la forma sin alterar el fondo o las ideas principales.',
        'examples': ['Parafraseo para mejorar fluidez (Tone adjustment)', 'Corrección gramatical y ortográfica', 'Adaptación de texto a formato académico estándar']
    },
    {
        'value': 'ideation',
        'label': 'Ideación y Estructura',
        'hint': 'Apoyo en la fase previa a la escritura (brainstorming, esquemas).',
        'examples': ['Generación de preguntas de investigación', 'Creación de esquemas (outlines) para tesis', 'Sugerencia de títulos o palabras clave']
    },
    {
        'value': 'analysis',
        'label': 'Análisis de Datos',
        'hint': 'Uso de capacidades computacionales para sintetizar o transformar información.',
        'examples': ['Resumen de papers o bibliografía', 'Extracción de entidades en textos', 'Análisis de sentimiento en corpus de datos']
    },
    {
        'value': 'coding',
        'label': 'Generación de Código',
        'hint': 'Creación de scripts, algoritmos o modelos matemáticos.',
        'examples': ['Scripts de Python/R para análisis estadístico', 'Consultas SQL complejas', 'Debugging de código de investigación']
    },
    {
        'value': 'translation',
        'label': 'Traducción Técnica',
        'hint': 'Traducción de textos académicos o técnicos entre idiomas.',
        'examples': ['Traducción de abstract al inglés', 'Comprensión de bibliografía en otro idioma']
    },
    {
        'value': 'review',
        'label': 'Simulación de Revisión (Feedback)',
        'hint': 'La IA actúa como "abogado del diablo" o revisor par simulado.',
        'examples': ['Detección de falacias lógicas', 'Crítica a la metodología propuesta', 'Búsqueda de lagunas en la argumentación']
    },
    {
        'value': 'other',
        'label': 'Otro uso no listado',
        'hint': 'Cualquier otro uso que no encaje en las categorías anteriores.',
        'examples': []
    }
]

CONTENT_USE_MODES = [
    'Incorporado tal cual (Verbatim)',
    'Editado parcialmente (ajustes menores)',
    'Reescrito sustancialmente',
    'Usado solo como inspiración/referencia',
    'Sintetizado con otras fuentes',
    'Otro'
]

HUMAN_REVIEW_LEVELS = [
    {'level': 0, 'label': 'Nivel 0: Sin Revisión', 'description': 'El contenido generado se utilizó directamente sin verificación humana (RIESGO ALTO).'},
    {'level': 1, 'label': 'Nivel 1: Revisión Superficial', 'description': 'Lectura rápida para verificar coherencia general, sin entrar en detalles de exactitud.'},
    {'level': 2, 'label': 'Nivel 2: Revisión Gramatical', 'description': 'Corrección de errores tipográficos, sintaxis y tono, asumiendo la veracidad del contenido.'},
    {'level': 3, 'label': 'Nivel 3: Verificación Selectiva', 'description': 'Comprobación aleatoria (spot-checking) de datos clave o afirmaciones dudosas.'},
    {'level': 4, 'label': 'Nivel 4: Contrastación Documental', 'description': 'Verificación de citas, referencias y datos contra fuentes primarias fiables.'},
    {'level': 5, 'label': 'Nivel 5: Validación Experta', 'description': 'Revisión profunda por un experto en la materia para asegurar integridad lógica y metodológica.'},
]

HELP_CHECKLIST = [
    {'id': 'q1', 'q': '¿Generó texto nuevo (párrafos, capítulos) que usaste como base?', 'suggests': 'draft', 'priority': 100},
    {'id': 'q2', 'q': '¿Te ayudó a escribir código, scripts o fórmulas matemáticas?', 'suggests': 'coding', 'priority': 90},
    {'id': 'q3', 'q': '¿Resumió artículos, extrajo datos o analizó documentos PDF?', 'suggests': 'analysis', 'priority': 80},
    {'id': 'q4', 'q': '¿Tradujo textos técnicos o abstracts a otro idioma?', 'suggests': 'translation', 'priority': 70},
    {'id': 'q5', 'q': '¿Sugirió estructuras, preguntas de investigación o ideas?', 'suggests': 'ideation', 'priority': 60},
    {'id': 'q6', 'q': '¿Solo mejoró la redacción, el vocabulario o la ortografía?', 'suggests': 'writing-support', 'priority': 40},
    {'id': 'q7', 'q': '¿Evaluó tu trabajo buscando errores o debilidades?', 'suggests': 'review', 'priority': 20}
]

CC_LICENSES = [
    {'value': 'CC BY 4.0', 'label': 'CC BY (Atribución)'},
    {'value': 'CC BY-SA 4.0', 'label': 'CC BY-SA (Atribución - Compartir Igual)'},
    {'value': 'CC BY-NC 4.0', 'label': 'CC BY-NC (Atribución - No Comercial)'},
    {'value': 'CC BY-ND 4.0', 'label': 'CC BY-ND (Atribución - Sin Derivadas)'},
    {'value': 'CC0 1.0', 'label': 'CC0 (Dominio Público)'},
    {'value': 'Copyright', 'label': 'Todos los derechos reservados (Copyright)'},
    {'value': 'None', 'label': 'No especificar / No aplica'}
]

PRESETS = [
    {
        'id': 'thesis-edit',
        'name': 'Corrección de Tesis',
        'description': 'Uso de IA solo para mejorar redacción y ortografía.',
        'data': {
            'usage_types': ['writing-support'],
            'specific_purpose': 'Mejorar la claridad, cohesión y ortografía de los capítulos de resultados y discusión, sin alterar los datos ni las conclusiones.',
            'content_use_modes': ['Editado parcialmente (ajustes menores)'],
            'human_review_level': 5,
            'reviewer_role': 'Autor Principal'
        }
    },
    {
        'id': 'coding-assist',
        'name': 'Análisis de Datos (R/Python)',
        'description': 'Generación de scripts para procesar datos.',
        'data': {
            'usage_types': ['coding', 'analysis'],
            'specific_purpose': 'Generación de scripts en Python para limpieza de dataset y visualización de gráficos exploratorios (Matplotlib).',
            'content_use_modes': ['Incorporado tal cual (Verbatim)', 'Editado parcialmente (ajustes menores)'],
            'human_review_level': 6,
            'reviewer_role': 'Investigador de Datos'
        }
    },
    {
        'id': 'translation',
        'name': 'Traducción de Abstract',
        'description': 'Traducción de resúmenes académicos.',
        'data': {
            'usage_types': ['translation'],
            'specific_purpose': 'Traducción del resumen ejecutivo del español al inglés para publicación internacional.',
            'content_use_modes': ['Editado parcialmente (ajustes menores)'],
            'human_review_level': 4,
            'reviewer_role': 'Autor / Traductor'
        }
    }
]

GLOSSARY_TERMS = [
    {'term': 'Prompt', 'definition': 'La instrucción o texto de entrada que se le da a la IA para generar una respuesta.'},
    {'term': 'Alucinación', 'definition': 'Fenómeno donde la IA genera información falsa o inventada con apariencia de ser real.'},
    {'term': 'Sesgo (Bias)', 'definition': 'Prejuicios o inclinaciones injustas presentes en los datos de entrenamiento de la IA que se reflejan en sus respuestas.'},
    {'term': 'Verbatim', 'definition': 'Copia textual, palabra por palabra, del contenido generado.'},
    {'term': 'LLM (Large Language Model)', 'definition': 'Modelo de lenguaje grande (como GPT, Claude, Gemini) entrenado con vastas cantidades de texto.'}
]

STEPS_LABELS = ['Diagnóstico', 'Clasificación', 'Detalles', 'Resultado']

MONTHS_ES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]

# Expanded AI Tools Catalog
AI_TOOLS_CATALOG = {
    'commercial': [
        {'name': 'ChatGPT', 'provider': 'OpenAI', 'versions': ['GPT-3.5', 'GPT-4', 'GPT-4 Turbo', 'GPT-4o', 'o1', 'o1-mini']},
        {'name': 'Claude', 'provider': 'Anthropic', 'versions': ['Claude 3 Haiku', 'Claude 3 Sonnet', 'Claude 3.5 Sonnet', 'Claude 3 Opus']},
        {'name': 'Gemini', 'provider': 'Google', 'versions': ['Gemini 1.0 Pro', 'Gemini 1.5 Pro', 'Gemini 1.5 Flash', 'Gemini 2.0 Flash']},
        {'name': 'Copilot', 'provider': 'Microsoft', 'versions': ['GPT-4 based', 'Copilot Pro']},
        {'name': 'Perplexity', 'provider': 'Perplexity AI', 'versions': ['Standard', 'Pro']},
        {'name': 'Grok', 'provider': 'xAI', 'versions': ['Grok-1', 'Grok-2']},
        {'name': 'DeepSeek', 'provider': 'DeepSeek', 'versions': ['DeepSeek-V2', 'DeepSeek-Coder']},
    ],
    'open_source': [
        {'name': 'Llama', 'provider': 'Meta', 'versions': ['Llama 2 7B', 'Llama 2 13B', 'Llama 2 70B', 'Llama 3 8B', 'Llama 3 70B', 'Llama 3.1 405B']},
        {'name': 'Mistral', 'provider': 'Mistral AI', 'versions': ['Mistral 7B', 'Mixtral 8x7B', 'Mixtral 8x22B']},
        {'name': 'Qwen', 'provider': 'Alibaba', 'versions': ['Qwen 7B', 'Qwen 14B', 'Qwen 72B']},
        {'name': 'Falcon', 'provider': 'TII', 'versions': ['Falcon 7B', 'Falcon 40B', 'Falcon 180B']},
        {'name': 'Phi', 'provider': 'Microsoft Research', 'versions': ['Phi-2', 'Phi-3 Mini', 'Phi-3 Medium']},
        {'name': 'Vicuna', 'provider': 'LMSYS', 'versions': ['Vicuna 7B', 'Vicuna 13B', 'Vicuna 33B']},
        {'name': 'MPT', 'provider': 'MosaicML', 'versions': ['MPT-7B', 'MPT-30B']},
    ],
    'local_platforms': [
        {'name': 'Ollama', 'provider': 'Ollama', 'versions': ['Llama 2', 'Mistral', 'Code Llama', 'Phi-2', 'Neural Chat']},
        {'name': 'LM Studio', 'provider': 'LM Studio', 'versions': ['Multi-model support']},
        {'name': 'GPT4All', 'provider': 'Nomic AI', 'versions': ['GPT4All-J', 'MPT-7B-Chat']},
        {'name': 'Jan', 'provider': 'Jan.ai', 'versions': ['Local LLM Runner']},
        {'name': 'LocalAI', 'provider': 'LocalAI', 'versions': ['Multi-model support']},
    ],
    'specialized': [
        {'name': 'GitHub Copilot', 'provider': 'GitHub/Microsoft', 'versions': ['GPT-4 based']},
        {'name': 'Tabnine', 'provider': 'Tabnine', 'versions': ['Pro', 'Enterprise']},
        {'name': 'Amazon CodeWhisperer', 'provider': 'AWS', 'versions': ['Standard', 'Professional']},
        {'name': 'Grammarly', 'provider': 'Grammarly', 'versions': ['Free', 'Premium', 'Business']},
        {'name': 'Wordtune', 'provider': 'AI21 Labs', 'versions': ['Free', 'Premium']},
        {'name': 'QuillBot', 'provider': 'QuillBot', 'versions': ['Free', 'Premium']},
        {'name': 'NotebookLM', 'provider': 'Google', 'versions': ['Standard']},
        {'name': 'Elicit', 'provider': 'Elicit', 'versions': ['Research Assistant']},
    ]
}

# Field validation limits
FIELD_LIMITS = {
    'specific_purpose': {'min': 20, 'max': 500, 'recommended': 100},
    'prompt_description': {'min': 10, 'max': 300, 'recommended': 50},
    'content_use_context': {'min': 10, 'max': 400, 'recommended': 100},
    'custom_usage_type': {'min': 10, 'max': 200, 'recommended': 50},
    'custom_content_use_mode': {'min': 10, 'max': 200, 'recommended': 50},
}
