"""
Multilingual translations for constants
This file provides translations for all the constants used in the application
"""

TRANSLATIONS = {
    'es': {
        # Help Checklist Questions (Step 1)
        'q1': '¿Generó texto nuevo (párrafos, capítulos) que usaste como base?',
        'q2': '¿Te ayudó a escribir código, scripts o fórmulas matemáticas?',
        'q3': '¿Resumió artículos, extrajo datos o analizó documentos PDF?',
        'q4': '¿Tradujo textos técnicos o abstracts a otro idioma?',
        'q5': '¿Sugirió estructuras, preguntas de investigación o ideas?',
        'q6': '¿Solo mejoró la redacción, el vocabulario o la ortografía?',
        'q7': '¿Evaluó tu trabajo buscando errores o debilidades?',

        # Content Use Modes
        'mode_verbatim': 'Incorporado tal cual (Verbatim)',
        'mode_partial': 'Editado parcialmente (ajustes menores)',
        'mode_substantial': 'Reescrito sustancialmente',
        'mode_inspiration': 'Usado solo como inspiración/referencia',
        'mode_synthesized': 'Sintetizado con otras fuentes',
        'mode_other': 'Otro',

        # Human Review Levels
        'review_0': 'Nivel 0: Sin Revisión',
        'review_0_desc': 'El contenido generado se utilizó directamente sin verificación humana (RIESGO ALTO).',
        'review_1': 'Nivel 1: Revisión Superficial',
        'review_1_desc': 'Lectura rápida para verificar coherencia general, sin entrar en detalles de exactitud.',
        'review_2': 'Nivel 2: Revisión Gramatical',
        'review_2_desc': 'Corrección de errores tipográficos, sintaxis y tono, asumiendo la veracidad del contenido.',
        'review_3': 'Nivel 3: Verificación Selectiva',
        'review_3_desc': 'Comprobación aleatoria (spot-checking) de datos clave o afirmaciones dudosas.',
        'review_4': 'Nivel 4: Contrastación Documental',
        'review_4_desc': 'Verificación de citas, referencias y datos contra fuentes primarias fiables.',
        'review_5': 'Nivel 5: Validación Experta',
        'review_5_desc': 'Revisión profunda por un experto en la materia para asegurar integridad lógica y metodológica.',
        'review_6': 'Nivel 6: Revisión Crítica y Ética',
        'review_6_desc': 'Análisis exhaustivo de sesgos, originalidad, ética y precisión técnica (Estándar "Gold").',
        # Usage Types
        'usage_draft': 'Generación de Borrador',
        'usage_draft_hint': 'La IA escribió una primera versión completa o secciones sustanciales que sirvieron de base.',
        'usage_draft_example_1': 'Generación de introducción para un paper',
        'usage_draft_example_2': 'Redacción de correos formales',
        'usage_draft_example_3': 'Primer borrador de capítulos teóricos',
        'usage_coauthor': 'Co-creación Sustantiva',
        'usage_coauthor_hint': 'Colaboración iterativa donde la IA y el humano construyen argumentos o narrativas conjuntamente.',
        'usage_coauthor_example_1': 'Diálogo socrático para refinar argumentos',
        'usage_coauthor_example_2': 'Expansión de puntos clave definidos por el humano',
        'usage_coauthor_example_3': 'Desarrollo de escenarios hipotéticos',
        'usage_writing': 'Asistencia de Estilo y Redacción',
        'usage_writing_hint': 'Mejora de la forma sin alterar el fondo o las ideas principales.',
        'usage_writing_example_1': 'Parafraseo para mejorar fluidez (Tone adjustment)',
        'usage_writing_example_2': 'Corrección gramatical y ortográfica',
        'usage_writing_example_3': 'Adaptación de texto a formato académico estándar',
        'usage_ideation': 'Ideación y Estructura',
        'usage_ideation_hint': 'Apoyo en la fase previa a la escritura (brainstorming, esquemas).',
        'usage_ideation_example_1': 'Generación de preguntas de investigación',
        'usage_ideation_example_2': 'Creación de esquemas (outlines) para tesis',
        'usage_ideation_example_3': 'Sugerencia de títulos o palabras clave',
        'usage_analysis': 'Análisis de Datos',
        'usage_analysis_hint': 'Uso de capacidades computacionales para sintetizar o transformar información.',
        'usage_analysis_example_1': 'Resumen de papers o bibliografía',
        'usage_analysis_example_2': 'Extracción de entidades en textos',
        'usage_analysis_example_3': 'Análisis de sentimiento en corpus de datos',
        'usage_coding': 'Generación de Código',
        'usage_coding_hint': 'Creación de scripts, algoritmos o modelos matemáticos.',
        'usage_coding_example_1': 'Scripts de Python/R para análisis estadístico',
        'usage_coding_example_2': 'Consultas SQL complejas',
        'usage_coding_example_3': 'Debugging de código de investigación',
        'usage_translation': 'Traducción Técnica',
        'usage_translation_hint': 'Traducción de textos académicos o técnicos entre idiomas.',
        'usage_translation_example_1': 'Traducción de abstract al inglés',
        'usage_translation_example_2': 'Comprensión de bibliografía en otro idioma',
        'usage_review': 'Simulación de Revisión (Feedback)',
        'usage_review_hint': 'La IA actúa como "abogado del diablo" o revisor par simulado.',
        'usage_review_example_1': 'Detección de falacias lógicas',
        'usage_review_example_2': 'Crítica a la metodología propuesta',
        'usage_review_example_3': 'Búsqueda de lagunas en la argumentación',
        'usage_other': 'Otro uso no listado',
        'usage_other_hint': 'Cualquier otro uso que no encaje en las categorías anteriores.',

        # Steps
        'step_diagnostic': 'Diagnóstico',
        'step_classification': 'Clasificación',
        'step_details': 'Detalles',
        'step_output': 'Resultado',
        
        # Declaration Text
        'decl_title': 'DECLARACIÓN DE TRANSPARENCIA ACADÉMICA: USO DE IA GENERATIVA',
        'decl_section_0': '0. DIAGNÓSTICO DE ORIGEN (TRAZABILIDAD)',
        'decl_section_1': '1. CLASIFICACIÓN DEL USO',
        'decl_section_2': '2. HERRAMIENTA UTILIZADA',
        'decl_section_3': '3. PROPÓSITO ESPECÍFICO',
        'decl_section_4': '4. PROMPTS (Instrucciones) PRINCIPALES',
        'decl_section_5': '5. INTEGRACIÓN EN EL PRODUCTO FINAL',
        'decl_section_6': '6. NIVEL DE REVISIÓN HUMANA Y ÉTICA',
        'decl_section_7': '7. LICENCIA DEL PRODUCTO FINAL',
        'decl_tool_name': '• Nombre',
        'decl_tool_version': '• Versión/Modelo',
        'decl_tool_provider': '• Proveedor',
        'decl_tool_date': '• Fecha de consulta',
        'decl_content_mode': '• Modo de uso',
        'decl_content_context': '• Contexto adicional',
        'decl_review_level': '• Nivel',
        'decl_review_description': '• Descripción',
        'decl_reviewed_by': '• Revisado por',
        'decl_reviewer_role': '• Rol/Cargo',
        'decl_id_registry': 'ID REGISTRO',
        'decl_hash_validation': 'HASH VALIDACIÓN',
        'decl_not_specified': 'No especificado',
        'decl_not_described': 'No descrito',
        'decl_manual_selection': 'Selección manual directa',
        'decl_author': 'Autor',
        'decl_author_email': 'Correo electrónico',

        # No AI Declaration
        'decl_title_no_ai': 'DECLARACIÓN DE NO USO DE INTELIGENCIA ARTIFICIAL GENERATIVA',
        'decl_no_ai_statement': 'CERTIFICO QUE NO SE UTILIZÓ INTELIGENCIA ARTIFICIAL GENERATIVA',
        'decl_no_ai_description': 'El autor declara que este trabajo académico fue realizado íntegramente sin el uso de herramientas de Inteligencia Artificial Generativa (IA). Todo el contenido, análisis, redacción y conclusiones son producto exclusivo del trabajo humano y de fuentes debidamente citadas.',

        # Step 1 - No AI Option
        'No utilicé Inteligencia Artificial': 'No utilicé Inteligencia Artificial',
        'Marca esta opción si NO usaste ninguna herramienta de IA en tu trabajo. Esto generará una declaración certificando la ausencia de uso de IA.': 'Marca esta opción si NO usaste ninguna herramienta de IA en tu trabajo. Esto generará una declaración certificando la ausencia de uso de IA.',

        # Step 4 - Save Modal
        'Datos del Autor': 'Datos del Autor',
        'Para guardar la declaración, necesitamos tus datos de contacto. Esta información solo se usará para identificar al autor de la declaración.': 'Para guardar la declaración, necesitamos tus datos de contacto. Esta información solo se usará para identificar al autor de la declaración.',
        'Nombre completo': 'Nombre completo',
        'Juan Pérez': 'Juan Pérez',
        'Correo electrónico': 'Correo electrónico',
        'correo@ejemplo.com': 'correo@ejemplo.com',
        'Guardar declaración': 'Guardar declaración',
        'Cancelar': 'Cancelar',

        # Preview Panel
        'preview_title': 'Vista Previa',
        'preview_description': 'Se actualiza automáticamente mientras completas el formulario',
        'preview_placeholder_step1': 'Marca opciones para ver la vista previa',
        'preview_placeholder_step2': 'Marca opciones para ver la vista previa',
        'preview_placeholder_step3': 'Completa los campos para ver la vista previa',
        'preview_updating': 'Actualizando vista previa...',
        'preview_error': 'Error al generar vista previa',
        'preview_unavailable': 'Vista previa no disponible',
        
        # Glossary Terms
        'Prompt': 'Prompt',
        'La instrucción o texto de entrada que se le da a la IA para generar una respuesta.': 'La instrucción o texto de entrada que se le da a la IA para generar una respuesta.',
        'Alucinación': 'Alucinación',
        'Fenómeno donde la IA genera información falsa o inventada con apariencia de ser real.': 'Fenómeno donde la IA genera información falsa o inventada con apariencia de ser real.',
        'Sesgo (Bias)': 'Sesgo (Bias)',
        'Prejuicios o inclinaciones injustas presentes en los datos de entrenamiento de la IA que se reflejan en sus respuestas.': 'Prejuicios o inclinaciones injustas presentes en los datos de entrenamiento de la IA que se reflejan en sus respuestas.',
        'Verbatim': 'Verbatim',
        'Copia textual, palabra por palabra, del contenido generado.': 'Copia textual, palabra por palabra, del contenido generado.',
        'LLM (Large Language Model)': 'LLM (Large Language Model)',
        'Modelo de lenguaje grande (como GPT, Claude, Gemini) entrenado con vastas cantidades de texto.': 'Modelo de lenguaje grande (como GPT, Claude, Gemini) entrenado con vastas cantidades de texto.',
    },
    'en': {
        # Help Checklist Questions (Step 1)
        'q1': 'Did it generate new text (paragraphs, chapters) that you used as a base?',
        'q2': 'Did it help you write code, scripts, or mathematical formulas?',
        'q3': 'Did it summarize articles, extract data, or analyze PDF documents?',
        'q4': 'Did it translate technical texts or abstracts to another language?',
        'q5': 'Did it suggest structures, research questions, or ideas?',
        'q6': 'Did it only improve writing, vocabulary, or spelling?',
        'q7': 'Did it evaluate your work looking for errors or weaknesses?',

        # Content Use Modes
        'mode_verbatim': 'Incorporated as is (Verbatim)',
        'mode_partial': 'Partially edited (minor adjustments)',
        'mode_substantial': 'Substantially rewritten',
        'mode_inspiration': 'Used only as inspiration/reference',
        'mode_synthesized': 'Synthesized with other sources',
        'mode_other': 'Other',

        # Human Review Levels
        'review_0': 'Level 0: No Review',
        'review_0_desc': 'Generated content was used directly without human verification (HIGH RISK).',
        'review_1': 'Level 1: Superficial Review',
        'review_1_desc': 'Quick reading to verify general coherence, without accuracy details.',
        'review_2': 'Level 2: Grammatical Review',
        'review_2_desc': 'Correction of typos, syntax, and tone, assuming content truthfulness.',
        'review_3': 'Level 3: Selective Verification',
        'review_3_desc': 'Random spot-checking of key data or doubtful claims.',
        'review_4': 'Level 4: Documentary Verification',
        'review_4_desc': 'Verification of citations, references, and data against reliable primary sources.',
        'review_5': 'Level 5: Expert Validation',
        'review_5_desc': 'Deep review by subject matter expert to ensure logical and methodological integrity.',
        'review_6': 'Level 6: Critical and Ethical Review',
        'review_6_desc': 'Exhaustive analysis of biases, originality, ethics, and technical accuracy (Gold Standard).',

        # Usage Types
        'usage_draft': 'Draft Generation',
        'usage_draft_hint': 'AI wrote a complete first version or substantial sections that served as the basis.',
        'usage_draft_example_1': 'Generation of introduction for a paper',
        'usage_draft_example_2': 'Writing formal emails',
        'usage_draft_example_3': 'First draft of theoretical chapters',
        'usage_coauthor': 'Substantive Co-creation',
        'usage_coauthor_hint': 'Iterative collaboration where AI and human jointly build arguments or narratives.',
        'usage_coauthor_example_1': 'Socratic dialogue to refine arguments',
        'usage_coauthor_example_2': 'Expansion of key points defined by the human',
        'usage_coauthor_example_3': 'Development of hypothetical scenarios',
        'usage_writing': 'Style and Writing Assistance',
        'usage_writing_hint': 'Improvement of form without altering substance or main ideas.',
        'usage_writing_example_1': 'Paraphrasing to improve fluency (Tone adjustment)',
        'usage_writing_example_2': 'Grammar and spelling correction',
        'usage_writing_example_3': 'Adaptation of text to standard academic format',
        'usage_ideation': 'Ideation and Structure',
        'usage_ideation_hint': 'Support in the pre-writing phase (brainstorming, outlines).',
        'usage_ideation_example_1': 'Generation of research questions',
        'usage_ideation_example_2': 'Creation of outlines for thesis',
        'usage_ideation_example_3': 'Suggestion of titles or keywords',
        'usage_analysis': 'Data Analysis',
        'usage_analysis_hint': 'Use of computational capabilities to synthesize or transform information.',
        'usage_analysis_example_1': 'Summary of papers or bibliography',
        'usage_analysis_example_2': 'Entity extraction in texts',
        'usage_analysis_example_3': 'Sentiment analysis in data corpus',
        'usage_coding': 'Code Generation',
        'usage_coding_hint': 'Creation of scripts, algorithms, or mathematical models.',
        'usage_coding_example_1': 'Python/R scripts for statistical analysis',
        'usage_coding_example_2': 'Complex SQL queries',
        'usage_coding_example_3': 'Debugging research code',
        'usage_translation': 'Technical Translation',
        'usage_translation_hint': 'Translation of academic or technical texts between languages.',
        'usage_translation_example_1': 'Translation of abstract to English',
        'usage_translation_example_2': 'Understanding bibliography in another language',
        'usage_review': 'Review Simulation (Feedback)',
        'usage_review_hint': 'AI acts as "devil\'s advocate" or simulated peer reviewer.',
        'usage_review_example_1': 'Detection of logical fallacies',
        'usage_review_example_2': 'Critique of proposed methodology',
        'usage_review_example_3': 'Search for gaps in argumentation',
        'usage_other': 'Other unlisted use',
        'usage_other_hint': 'Any other use that doesn\'t fit the above categories.',

        # Steps
        'step_diagnostic': 'Diagnostic',
        'step_classification': 'Classification',
        'step_details': 'Details',
        'step_output': 'Output',
        
        # Declaration Text
        'decl_title': 'ACADEMIC TRANSPARENCY DECLARATION: GENERATIVE AI USE',
        'decl_section_0': '0. ORIGIN DIAGNOSTIC (TRACEABILITY)',
        'decl_section_1': '1. USAGE CLASSIFICATION',
        'decl_section_2': '2. TOOL USED',
        'decl_section_3': '3. SPECIFIC PURPOSE',
        'decl_section_4': '4. MAIN PROMPTS (Instructions)',
        'decl_section_5': '5. INTEGRATION IN FINAL PRODUCT',
        'decl_section_6': '6. HUMAN AND ETHICAL REVIEW LEVEL',
        'decl_section_7': '7. FINAL PRODUCT LICENSE',
        'decl_tool_name': '• Name',
        'decl_tool_version': '• Version/Model',
        'decl_tool_provider': '• Provider',
        'decl_tool_date': '• Consultation Date',
        'decl_content_mode': '• Use Mode',
        'decl_content_context': '• Additional Context',
        'decl_review_level': '• Level',
        'decl_review_description': '• Description',
        'decl_reviewed_by': '• Reviewed by',
        'decl_reviewer_role': '• Role/Position',
        'decl_id_registry': 'REGISTRY ID',
        'decl_hash_validation': 'VALIDATION HASH',
        'decl_not_specified': 'Not specified',
        'decl_not_described': 'Not described',
        'decl_manual_selection': 'Direct manual selection',
        'decl_author': 'Author',
        'decl_author_email': 'Email',

        # No AI Declaration
        'decl_title_no_ai': 'DECLARATION OF NON-USE OF GENERATIVE ARTIFICIAL INTELLIGENCE',
        'decl_no_ai_statement': 'I CERTIFY THAT NO GENERATIVE ARTIFICIAL INTELLIGENCE WAS USED',
        'decl_no_ai_description': 'The author declares that this academic work was completed entirely without the use of Generative Artificial Intelligence (AI) tools. All content, analysis, writing, and conclusions are the exclusive product of human work and properly cited sources.',

        # Step 1 - No AI Option
        'No utilicé Inteligencia Artificial': 'I did not use Artificial Intelligence',
        'Marca esta opción si NO usaste ninguna herramienta de IA en tu trabajo. Esto generará una declaración certificando la ausencia de uso de IA.': 'Check this option if you did NOT use any AI tools in your work. This will generate a declaration certifying the absence of AI use.',

        # Step 4 - Save Modal
        'Datos del Autor': 'Author Information',
        'Para guardar la declaración, necesitamos tus datos de contacto. Esta información solo se usará para identificar al autor de la declaración.': 'To save the declaration, we need your contact information. This information will only be used to identify the author of the declaration.',
        'Nombre completo': 'Full name',
        'Juan Pérez': 'John Doe',
        'Correo electrónico': 'Email address',
        'correo@ejemplo.com': 'email@example.com',
        'Guardar declaración': 'Save declaration',
        'Cancelar': 'Cancel',

        # Glossary Terms
        'Prompt': 'Prompt',
        'La instrucción o texto de entrada que se le da a la IA para generar una respuesta.': 'The instruction or input text given to the AI to generate a response.',
        'Alucinación': 'Hallucination',
        'Fenómeno donde la IA genera información falsa o inventada con apariencia de ser real.': 'Phenomenon where AI generates false or made-up information with the appearance of being real.',
        'Sesgo (Bias)': 'Bias',
        'Prejuicios o inclinaciones injustas presentes en los datos de entrenamiento de la IA que se reflejan en sus respuestas.': 'Unfair prejudices or inclinations present in the AI\'s training data that are reflected in its responses.',
        'Verbatim': 'Verbatim',
        'Copia textual, palabra por palabra, del contenido generado.': 'Literal copy, word for word, of the generated content.',
        'LLM (Large Language Model)': 'LLM (Large Language Model)',
        'Modelo de lenguaje grande (como GPT, Claude, Gemini) entrenado con vastas cantidades de texto.': 'Large language model (such as GPT, Claude, Gemini) trained with vast amounts of text.',
    },
    'pt': {
        # Help Checklist Questions (Step 1)
        'q1': 'Gerou texto novo (parágrafos, capítulos) que você usou como base?',
        'q2': 'Ajudou você a escrever código, scripts ou fórmulas matemáticas?',
        'q3': 'Resumiu artigos, extraiu dados ou analisou documentos PDF?',
        'q4': 'Traduziu textos técnicos ou abstracts para outro idioma?',
        'q5': 'Sugeriu estruturas, questões de pesquisa ou ideias?',
        'q6': 'Apenas melhorou a redação, o vocabulário ou a ortografia?',
        'q7': 'Avaliou seu trabalho buscando erros ou fraquezas?',

        # Content Use Modes
        'mode_verbatim': 'Incorporado tal qual (Literal)',
        'mode_partial': 'Editado parcialmente (ajustes menores)',
        'mode_substantial': 'Reescrito substancialmente',
        'mode_inspiration': 'Usado apenas como inspiração/referência',
        'mode_synthesized': 'Sintetizado com outras fontes',
        'mode_other': 'Outro',

        # Human Review Levels
        'review_0': 'Nível 0: Sem Revisão',
        'review_0_desc': 'O conteúdo gerado foi usado diretamente sem verificação humana (RISCO ALTO).',
        'review_1': 'Nível 1: Revisão Superficial',
        'review_1_desc': 'Leitura rápida para verificar coerência geral, sem entrar em detalhes de precisão.',
        'review_2': 'Nível 2: Revisão Gramatical',
        'review_2_desc': 'Correção de erros tipográficos, sintaxe e tom, assumindo a veracidade do conteúdo.',
        'review_3': 'Nível 3: Verificação Seletiva',
        'review_3_desc': 'Verificação aleatória (spot-checking) de dados-chave ou afirmações duvidosas.',
        'review_4': 'Nível 4: Verificação Documental',
        'review_4_desc': 'Verificação de citações, referências e dados contra fontes primárias confiáveis.',
        'review_5': 'Nível 5: Validação Especializada',
        'review_5_desc': 'Revisão profunda por especialista na matéria para garantir integridade lógica e metodológica.',
        'review_6': 'Nível 6: Revisão Crítica e Ética',
        'review_6_desc': 'Análise exaustiva de vieses, originalidade, ética e precisão técnica (Padrão "Ouro").',

        # Usage Types
        'usage_draft': 'Geração de Rascunho',
        'usage_draft_hint': 'A IA escreveu uma primeira versão completa ou seções substanciais que serviram de base.',
        'usage_draft_example_1': 'Geração de introdução para um paper',
        'usage_draft_example_2': 'Redação de e-mails formais',
        'usage_draft_example_3': 'Primeiro rascunho de capítulos teóricos',
        'usage_coauthor': 'Co-criação Substantiva',
        'usage_coauthor_hint': 'Colaboração iterativa onde IA e humano constroem argumentos ou narrativas conjuntamente.',
        'usage_coauthor_example_1': 'Diálogo socrático para refinar argumentos',
        'usage_coauthor_example_2': 'Expansão de pontos-chave definidos pelo humano',
        'usage_coauthor_example_3': 'Desenvolvimento de cenários hipotéticos',
        'usage_writing': 'Assistência de Estilo e Redação',
        'usage_writing_hint': 'Melhora da forma sem alterar o conteúdo ou as ideias principais.',
        'usage_writing_example_1': 'Paráfrase para melhorar fluidez (Ajuste de tom)',
        'usage_writing_example_2': 'Correção gramatical e ortográfica',
        'usage_writing_example_3': 'Adaptação de texto ao formato acadêmico padrão',
        'usage_ideation': 'Ideação e Estrutura',
        'usage_ideation_hint': 'Apoio na fase de pré-escrita (brainstorming, esquemas).',
        'usage_ideation_example_1': 'Geração de questões de pesquisa',
        'usage_ideation_example_2': 'Criação de esquemas (outlines) para tese',
        'usage_ideation_example_3': 'Sugestão de títulos ou palavras-chave',
        'usage_analysis': 'Análise de Dados',
        'usage_analysis_hint': 'Uso de capacidades computacionais para sintetizar ou transformar informações.',
        'usage_analysis_example_1': 'Resumo de papers ou bibliografia',
        'usage_analysis_example_2': 'Extração de entidades em textos',
        'usage_analysis_example_3': 'Análise de sentimento em corpus de dados',
        'usage_coding': 'Geração de Código',
        'usage_coding_hint': 'Criação de scripts, algoritmos ou modelos matemáticos.',
        'usage_coding_example_1': 'Scripts de Python/R para análise estatística',
        'usage_coding_example_2': 'Consultas SQL complexas',
        'usage_coding_example_3': 'Debugging de código de pesquisa',
        'usage_translation': 'Tradução Técnica',
        'usage_translation_hint': 'Tradução de textos acadêmicos ou técnicos entre idiomas.',
        'usage_translation_example_1': 'Tradução de abstract para o inglês',
        'usage_translation_example_2': 'Compreensão de bibliografia em outro idioma',
        'usage_review': 'Simulação de Revisão (Feedback)',
        'usage_review_hint': 'A IA atua como "advogado do diabo" ou revisor par simulado.',
        'usage_review_example_1': 'Detecção de falácias lógicas',
        'usage_review_example_2': 'Crítica à metodologia proposta',
        'usage_review_example_3': 'Busca de lacunas na argumentação',
        'usage_other': 'Outro uso não listado',
        'usage_other_hint': 'Qualquer outro uso que não se encaixe nas categorias anteriores.',

        # Steps
        'step_diagnostic': 'Diagnóstico',
        'step_classification': 'Classificação',
        'step_details': 'Detalhes',
        'step_output': 'Resultado',
        
        # Declaration Text
        'decl_title': 'DECLARAÇÃO DE TRANSPARÊNCIA ACADÊMICA: USO DE IA GENERATIVA',
        'decl_section_0': '0. DIAGNÓSTICO DE ORIGEM (RASTREABILIDADE)',
        'decl_section_1': '1. CLASSIFICAÇÃO DO USO',
        'decl_section_2': '2. FERRAMENTA UTILIZADA',
        'decl_section_3': '3. PROPÓSITO ESPECÍFICO',
        'decl_section_4': '4. PROMPTS (Instruções) PRINCIPAIS',
        'decl_section_5': '5. INTEGRAÇÃO NO PRODUTO FINAL',
        'decl_section_6': '6. NÍVEL DE REVISÃO HUMANA E ÉTICA',
        'decl_section_7': '7. LICENÇA DO PRODUTO FINAL',
        'decl_tool_name': '• Nome',
        'decl_tool_version': '• Versão/Modelo',
        'decl_tool_provider': '• Provedor',
        'decl_tool_date': '• Data de consulta',
        'decl_content_mode': '• Modo de uso',
        'decl_content_context': '• Contexto adicional',
        'decl_review_level': '• Nível',
        'decl_review_description': '• Descrição',
        'decl_reviewed_by': '• Revisado por',
        'decl_reviewer_role': '• Função/Cargo',
        'decl_id_registry': 'ID REGISTRO',
        'decl_hash_validation': 'HASH VALIDAÇÃO',
        'decl_not_specified': 'Não especificado',
        'decl_not_described': 'Não descrito',
        'decl_manual_selection': 'Seleção manual direta',
        'decl_author': 'Autor',
        'decl_author_email': 'E-mail',

        # No AI Declaration
        'decl_title_no_ai': 'DECLARAÇÃO DE NÃO USO DE INTELIGÊNCIA ARTIFICIAL GENERATIVA',
        'decl_no_ai_statement': 'CERTIFICO QUE NÃO FOI UTILIZADA INTELIGÊNCIA ARTIFICIAL GENERATIVA',
        'decl_no_ai_description': 'O autor declara que este trabalho acadêmico foi realizado integralmente sem o uso de ferramentas de Inteligência Artificial Generativa (IA). Todo o conteúdo, análise, redação e conclusões são produto exclusivo do trabalho humano e de fontes devidamente citadas.',

        # Step 1 - No AI Option
        'No utilicé Inteligencia Artificial': 'Não utilizei Inteligência Artificial',
        'Marca esta opción si NO usaste ninguna herramienta de IA en tu trabajo. Esto generará una declaración certificando la ausencia de uso de IA.': 'Marque esta opção se você NÃO usou nenhuma ferramenta de IA em seu trabalho. Isso gerará uma declaração certificando a ausência de uso de IA.',

        # Step 4 - Save Modal
        'Datos del Autor': 'Dados do Autor',
        'Para guardar la declaración, necesitamos tus datos de contacto. Esta información solo se usará para identificar al autor de la declaración.': 'Para salvar a declaração, precisamos de suas informações de contato. Estas informações serão usadas apenas para identificar o autor da declaração.',
        'Nombre completo': 'Nome completo',
        'Juan Pérez': 'João Silva',
        'Correo electrónico': 'E-mail',
        'correo@ejemplo.com': 'email@exemplo.com',
        'Guardar declaración': 'Salvar declaração',
        'Cancelar': 'Cancelar',

        # Preview Panel
        'preview_title': 'Pré-visualização',
        'preview_description': 'Atualiza automaticamente enquanto você completa o formulário',
        'preview_placeholder_step1': 'Marque opções para ver a pré-visualização',
        'preview_placeholder_step2': 'Marque opções para ver a pré-visualização',
        'preview_placeholder_step3': 'Preencha os campos para ver a pré-visualização',
        'preview_updating': 'Atualizando pré-visualização...',
        'preview_error': 'Erro ao gerar pré-visualização',
        'preview_unavailable': 'Pré-visualização não disponível',
        
        # Glossary Terms
        'Prompt': 'Prompt',
        'La instrucción o texto de entrada que se le da a la IA para generar una respuesta.': 'A instrução ou texto de entrada dado à IA para gerar uma resposta.',
        'Alucinación': 'Alucinação',
        'Fenómeno donde la IA genera información falsa o inventada con apariencia de ser real.': 'Fenômeno onde a IA gera informações falsas ou inventadas com aparência de ser real.',
        'Sesgo (Bias)': 'Viés (Bias)',
        'Prejuicios o inclinaciones injustas presentes en los datos de entrenamiento de la IA que se reflejan en sus respuestas.': 'Preconceitos ou inclinações injustas presentes nos dados de treinamento da IA que se refletem em suas respostas.',
        'Verbatim': 'Literal',
        'Copia textual, palabra por palabra, del contenido generado.': 'Cópia textual, palavra por palavra, do conteúdo gerado.',
        'LLM (Large Language Model)': 'LLM (Modelo de Linguagem Grande)',
        'Modelo de lenguaje grande (como GPT, Claude, Gemini) entrenado con vastas cantidades de texto.': 'Modelo de linguagem grande (como GPT, Claude, Gemini) treinado com vastas quantidades de texto.',
    },
    'it': {
        # Help Checklist Questions (Step 1)
        'q1': 'Ha generato nuovo testo (paragrafi, capitoli) che hai usato come base?',
        'q2': 'Ti ha aiutato a scrivere codice, script o formule matematiche?',
        'q3': 'Ha riassunto articoli, estratto dati o analizzato documenti PDF?',
        'q4': 'Ha tradotto testi tecnici o abstract in un\'altra lingua?',
        'q5': 'Ha suggerito strutture, domande di ricerca o idee?',
        'q6': 'Ha solo migliorato la scrittura, il vocabolario o l\'ortografia?',
        'q7': 'Ha valutato il tuo lavoro cercando errori o debolezze?',

        # Content Use Modes
        'mode_verbatim': 'Incorporato così com\'è (Testuale)',
        'mode_partial': 'Modificato parzialmente (adattamenti minori)',
        'mode_substantial': 'Riscritto sostanzialmente',
        'mode_inspiration': 'Usato solo come ispirazione/riferimento',
        'mode_synthesized': 'Sintetizzato con altre fonti',
        'mode_other': 'Altro',

        # Human Review Levels
        'review_0': 'Livello 0: Nessuna Revisione',
        'review_0_desc': 'Il contenuto generato è stato utilizzato direttamente senza verifica umana (RISCHIO ALTO).',
        'review_1': 'Livello 1: Revisione Superficiale',
        'review_1_desc': 'Lettura rapida per verificare la coerenza generale, senza entrare nei dettagli di precisione.',
        'review_2': 'Livello 2: Revisione Grammaticale',
        'review_2_desc': 'Correzione di errori tipografici, sintassi e tono, assumendo la veridicità del contenuto.',
        'review_3': 'Livello 3: Verifica Selettiva',
        'review_3_desc': 'Controllo casuale (spot-checking) di dati chiave o affermazioni dubbie.',
        'review_4': 'Livello 4: Verifica Documentale',
        'review_4_desc': 'Verifica di citazioni, riferimenti e dati contro fonti primarie affidabili.',
        'review_5': 'Livello 5: Validazione Esperta',
        'review_5_desc': 'Revisione approfondita da parte di un esperto della materia per garantire l\'integrità logica e metodologica.',
        'review_6': 'Livello 6: Revisione Critica ed Etica',
        'review_6_desc': 'Analisi esaustiva di bias, originalità, etica e precisione tecnica (Standard "Oro").',

        # Usage Types
        'usage_draft': 'Generazione di Bozza',
        'usage_draft_hint': 'L\'IA ha scritto una prima versione completa o sezioni sostanziali che hanno servito da base.',
        'usage_draft_example_1': 'Generazione di introduzione per un paper',
        'usage_draft_example_2': 'Redazione di email formali',
        'usage_draft_example_3': 'Prima bozza di capitoli teorici',
        'usage_coauthor': 'Co-creazione Sostanziale',
        'usage_coauthor_hint': 'Collaborazione iterativa dove IA e umano costruiscono argomenti o narrative congiuntamente.',
        'usage_coauthor_example_1': 'Dialogo socratico per affinare gli argomenti',
        'usage_coauthor_example_2': 'Espansione di punti chiave definiti dall\'umano',
        'usage_coauthor_example_3': 'Sviluppo di scenari ipotetici',
        'usage_writing': 'Assistenza di Stile e Redazione',
        'usage_writing_hint': 'Miglioramento della forma senza alterare il contenuto o le idee principali.',
        'usage_writing_example_1': 'Parafrasi per migliorare la fluidità (Regolazione del tono)',
        'usage_writing_example_2': 'Correzione grammaticale e ortografica',
        'usage_writing_example_3': 'Adattamento del testo al formato accademico standard',
        'usage_ideation': 'Ideazione e Struttura',
        'usage_ideation_hint': 'Supporto nella fase di pre-scrittura (brainstorming, schemi).',
        'usage_ideation_example_1': 'Generazione di domande di ricerca',
        'usage_ideation_example_2': 'Creazione di schemi (outline) per tesi',
        'usage_ideation_example_3': 'Suggerimento di titoli o parole chiave',
        'usage_analysis': 'Analisi dei Dati',
        'usage_analysis_hint': 'Uso di capacità computazionali per sintetizzare o trasformare informazioni.',
        'usage_analysis_example_1': 'Riassunto di paper o bibliografia',
        'usage_analysis_example_2': 'Estrazione di entità nei testi',
        'usage_analysis_example_3': 'Analisi del sentiment in corpus di dati',
        'usage_coding': 'Generazione di Codice',
        'usage_coding_hint': 'Creazione di script, algoritmi o modelli matematici.',
        'usage_coding_example_1': 'Script Python/R per analisi statistica',
        'usage_coding_example_2': 'Query SQL complesse',
        'usage_coding_example_3': 'Debugging di codice di ricerca',
        'usage_translation': 'Traduzione Tecnica',
        'usage_translation_hint': 'Traduzione di testi accademici o tecnici tra lingue.',
        'usage_translation_example_1': 'Traduzione di abstract in inglese',
        'usage_translation_example_2': 'Comprensione di bibliografia in altra lingua',
        'usage_review': 'Simulazione di Revisione (Feedback)',
        'usage_review_hint': 'L\'IA agisce come "avvocato del diavolo" o revisore paritario simulato.',
        'usage_review_example_1': 'Rilevamento di fallacie logiche',
        'usage_review_example_2': 'Critica alla metodologia proposta',
        'usage_review_example_3': 'Ricerca di lacune nell\'argomentazione',
        'usage_other': 'Altro uso non elencato',
        'usage_other_hint': 'Qualsiasi altro uso che non rientri nelle categorie precedenti.',

        # Steps
        'step_diagnostic': 'Diagnostico',
        'step_classification': 'Classificazione',
        'step_details': 'Dettagli',
        'step_output': 'Risultato',
        
        # Declaration Text
        'decl_title': 'DICHIARAZIONE DI TRASPARENZA ACCADEMICA: USO DI IA GENERATIVA',
        'decl_section_0': '0. DIAGNOSTICO DI ORIGINE (TRACCIABILITÀ)',
        'decl_section_1': '1. CLASSIFICAZIONE DELL\'USO',
        'decl_section_2': '2. STRUMENTO UTILIZZATO',
        'decl_section_3': '3. SCOPO SPECIFICO',
        'decl_section_4': '4. PROMPT (Istruzioni) PRINCIPALI',
        'decl_section_5': '5. INTEGRAZIONE NEL PRODOTTO FINALE',
        'decl_section_6': '6. LIVELLO DI REVISIONE UMANA ED ETICA',
        'decl_section_7': '7. LICENZA DEL PRODOTTO FINALE',
        'decl_tool_name': '• Nome',
        'decl_tool_version': '• Versione/Modello',
        'decl_tool_provider': '• Fornitore',
        'decl_tool_date': '• Data di consultazione',
        'decl_content_mode': '• Modo di utilizzo',
        'decl_content_context': '• Contesto aggiuntivo',
        'decl_review_level': '• Livello',
        'decl_review_description': '• Descrizione',
        'decl_reviewed_by': '• Revisionato da',
        'decl_reviewer_role': '• Ruolo/Posizione',
        'decl_id_registry': 'ID REGISTRO',
        'decl_hash_validation': 'HASH VALIDAZIONE',
        'decl_not_specified': 'Non specificato',
        'decl_not_described': 'Non descritto',
        'decl_manual_selection': 'Selezione manuale diretta',
        'decl_author': 'Autore',
        'decl_author_email': 'Email',

        # No AI Declaration
        'decl_title_no_ai': 'DICHIARAZIONE DI NON UTILIZZO DI INTELLIGENZA ARTIFICIALE GENERATIVA',
        'decl_no_ai_statement': 'CERTIFICO CHE NON È STATA UTILIZZATA INTELLIGENZA ARTIFICIALE GENERATIVA',
        'decl_no_ai_description': 'L\'autore dichiara che questo lavoro accademico è stato realizzato interamente senza l\'uso di strumenti di Intelligenza Artificiale Generativa (IA). Tutti i contenuti, analisi, redazione e conclusioni sono prodotto esclusivo del lavoro umano e di fonti debitamente citate.',

        # Step 1 - No AI Option
        'No utilicé Inteligencia Artificial': 'Non ho utilizzato Intelligenza Artificiale',
        'Marca esta opción si NO usaste ninguna herramienta de IA en tu trabajo. Esto generará una declaración certificando la ausencia de uso de IA.': 'Seleziona questa opzione se NON hai utilizzato alcuno strumento di IA nel tuo lavoro. Questo genererà una dichiarazione che certifica l\'assenza di utilizzo di IA.',

        # Step 4 - Save Modal
        'Datos del Autor': 'Dati dell\'Autore',
        'Para guardar la declaración, necesitamos tus datos de contacto. Esta información solo se usará para identificar al autor de la declaración.': 'Per salvare la dichiarazione, abbiamo bisogno delle tue informazioni di contatto. Queste informazioni verranno utilizzate solo per identificare l\'autore della dichiarazione.',
        'Nombre completo': 'Nome completo',
        'Juan Pérez': 'Mario Rossi',
        'Correo electrónico': 'Indirizzo email',
        'correo@ejemplo.com': 'email@esempio.com',
        'Guardar declaración': 'Salva dichiarazione',
        'Cancelar': 'Annulla',

        # Preview Panel
        'preview_title': 'Anteprima',
        'preview_description': 'Si aggiorna automaticamente mentre completi il modulo',
        'preview_placeholder_step1': 'Seleziona opzioni per vedere l\'anteprima',
        'preview_placeholder_step2': 'Seleziona opzioni per vedere l\'anteprima',
        'preview_placeholder_step3': 'Completa i campi per vedere l\'anteprima',
        'preview_updating': 'Aggiornamento anteprima...',
        'preview_error': 'Errore nella generazione dell\'anteprima',
        'preview_unavailable': 'Anteprima non disponibile',
        
        # Glossary Terms
        'Prompt': 'Prompt',
        'La instrucción o texto de entrada que se le da a la IA para generar una respuesta.': 'L\'istruzione o testo di input dato all\'IA per generare una risposta.',
        'Alucinación': 'Allucinazione',
        'Fenómeno donde la IA genera información falsa o inventada con apariencia de ser real.': 'Fenomeno in cui l\'IA genera informazioni false o inventate con l\'apparenza di essere reali.',
        'Sesgo (Bias)': 'Bias (Pregiudizio)',
        'Prejuicios o inclinaciones injustas presentes en los datos de entrenamiento de la IA que se reflejan en sus respuestas.': 'Pregiudizi o inclinazioni ingiuste presenti nei dati di addestramento dell\'IA che si riflettono nelle sue risposte.',
        'Verbatim': 'Testuale',
        'Copia textual, palabra por palabra, del contenido generado.': 'Copia testuale, parola per parola, del contenuto generato.',
        'LLM (Large Language Model)': 'LLM (Modello di Linguaggio Grande)',
        'Modelo de lenguaje grande (como GPT, Claude, Gemini) entrenado con vastas cantidades de texto.': 'Modello di linguaggio grande (come GPT, Claude, Gemini) addestrato con vaste quantità di testo.',
    }
}


def get_translation(key, lang='es'):
    """Get translation for a key in the specified language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['es']).get(key, TRANSLATIONS['es'].get(key, key))


def get_translated_usage_types(lang='es'):
    """Get usage types translated to the specified language"""
    from .constants import USAGE_TYPES

    # Map usage type values to translation keys (handle 'writing-support' -> 'writing')
    value_to_key = {
        'draft': 'draft',
        'coauthor': 'coauthor',
        'writing-support': 'writing',
        'ideation': 'ideation',
        'analysis': 'analysis',
        'coding': 'coding',
        'translation': 'translation',
        'review': 'review',
        'other': 'other'
    }

    translated = []
    for usage_type in USAGE_TYPES:
        translated_item = usage_type.copy()
        usage_value = usage_type['value']
        translation_key = value_to_key.get(usage_value, usage_value)
        
        key_label = f"usage_{translation_key}"
        key_hint = f"usage_{translation_key}_hint"

        translated_item['label'] = get_translation(key_label, lang)
        translated_item['hint'] = get_translation(key_hint, lang)
        
        # Translate examples if available and not in Spanish
        if 'examples' in translated_item and translated_item['examples'] and lang != 'es':
            translated_examples = []
            num_examples = len(translated_item['examples'])
            
            for i in range(num_examples):
                example_key = f"usage_{translation_key}_example_{i+1}"
                translated_example = get_translation(example_key, lang)
                # Only add if translation exists (not the same as key)
                if translated_example != example_key:
                    translated_examples.append(translated_example)
            
            # Update examples only if we found translations
            if translated_examples:
                translated_item['examples'] = translated_examples
        
        translated.append(translated_item)

    return translated


def get_translated_steps_labels(lang='es'):
    """Get steps labels translated to the specified language"""
    return [
        get_translation('step_diagnostic', lang),
        get_translation('step_classification', lang),
        get_translation('step_details', lang),
        get_translation('step_output', lang),
    ]


def get_translated_checklist(lang='es'):
    """Get help checklist questions translated to the specified language"""
    from .constants import HELP_CHECKLIST

    translated = []
    for item in HELP_CHECKLIST:
        translated_item = item.copy()
        translated_item['q'] = get_translation(item['id'], lang)
        translated.append(translated_item)

    return translated


def get_translated_content_modes(lang='es'):
    """Get content use modes translated to the specified language"""
    modes = ['verbatim', 'partial', 'substantial', 'inspiration', 'synthesized', 'other']
    return [get_translation(f'mode_{mode}', lang) for mode in modes]


def get_translated_review_levels(lang='es'):
    """Get human review levels translated to the specified language"""
    from .constants import HUMAN_REVIEW_LEVELS

    translated = []
    for level in HUMAN_REVIEW_LEVELS:
        translated_item = level.copy()
        key = f"review_{level['level']}"
        translated_item['label'] = get_translation(key, lang)
        translated_item['description'] = get_translation(f"{key}_desc", lang)
        translated.append(translated_item)

    return translated


def get_translated_glossary(lang='es'):
    """Get glossary terms translated to the specified language"""
    from .constants import GLOSSARY_TERMS
    
    if lang == 'es':
        return GLOSSARY_TERMS
    
    translated = []
    for term in GLOSSARY_TERMS:
        translated_item = {
            'term': get_translation(term['term'], lang),
            'definition': get_translation(term['definition'], lang)
        }
        translated.append(translated_item)
    
    return translated
