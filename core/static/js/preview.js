/**
 * JavaScript para vista previa en tiempo real
 * Actualiza la vista previa conforme el usuario marca opciones
 */

let previewUpdateTimeout = null;
const PREVIEW_UPDATE_DELAY = 300; // ms de delay para evitar demasiadas peticiones

/**
 * Obtiene los datos actuales del formulario según el paso
 * Solo envía los datos del paso actual, el servidor usará la sesión para el resto
 */
function getFormData(step) {
    const data = {};

    // Paso 1: Checklist - solo si estamos en el paso 1
    if (step === 1) {
        const checkboxes = document.querySelectorAll('.checkbox-input:checked');
        const selectedIds = Array.from(checkboxes).map(cb => cb.value);
        if (selectedIds.length > 0) {
            data.selected_checklist_ids = selectedIds;
        }
    }

    // Paso 2: Tipos de uso - solo si estamos en el paso 2
    if (step === 2) {
        const usageCheckboxes = document.querySelectorAll('.usage-checkbox:checked');
        const usageTypes = Array.from(usageCheckboxes).map(cb => cb.value);
        if (usageTypes.length > 0) {
            data.usage_types = usageTypes;
        }
        
        const customUsageTextarea = document.querySelector('textarea[name="custom_usage_type"]');
        if (customUsageTextarea && customUsageTextarea.value.trim()) {
            data.custom_usage_type = customUsageTextarea.value;
        }
    }

    // Paso 3: Detalles - solo si estamos en el paso 3
    if (step === 3) {
        // AI Tool - solo enviar si hay valores
        const toolName = document.querySelector('input[name="ai_tool_name"]');
        const toolVersion = document.querySelector('input[name="ai_tool_version"]');
        const toolProvider = document.querySelector('input[name="ai_tool_provider"]');
        const toolMonth = document.querySelector('select[name="ai_tool_date_month"]');
        const toolYear = document.querySelector('select[name="ai_tool_date_year"]');
        
        if (toolName || toolVersion || toolProvider || toolMonth || toolYear) {
            data.ai_tool = {};
            if (toolName && toolName.value) data.ai_tool.name = toolName.value;
            if (toolVersion && toolVersion.value) data.ai_tool.version = toolVersion.value;
            if (toolProvider && toolProvider.value) data.ai_tool.provider = toolProvider.value;
            if (toolMonth) data.ai_tool.date_month = parseInt(toolMonth.value) || new Date().getMonth() + 1;
            if (toolYear) data.ai_tool.date_year = parseInt(toolYear.value) || new Date().getFullYear();
        }

        // Purpose
        const purpose = document.querySelector('textarea[name="specific_purpose"]');
        if (purpose && purpose.value.trim()) {
            data.specific_purpose = purpose.value;
        }

        // Prompts
        const promptInputs = document.querySelectorAll('input[name^="prompt_"]');
        const prompts = Array.from(promptInputs)
            .map(input => ({ id: input.name.replace('prompt_', ''), description: input.value }))
            .filter(p => p.description.trim());
        if (prompts.length > 0) {
            data.prompts = prompts;
        }

        // Content use modes
        const contentModes = document.querySelectorAll('input[name="content_use_modes"]:checked');
        const modes = Array.from(contentModes).map(cb => cb.value);
        if (modes.length > 0) {
            data.content_use_modes = modes;
        }
        
        const customContentMode = document.querySelector('input[name="custom_content_use_mode"]');
        if (customContentMode && customContentMode.value.trim()) {
            data.custom_content_use_mode = customContentMode.value;
        }
        
        const contentContext = document.querySelector('textarea[name="content_use_context"]');
        if (contentContext && contentContext.value.trim()) {
            data.content_use_context = contentContext.value;
        }

        // Human review
        const reviewLevel = document.querySelector('input[name="human_review_level"]:checked');
        if (reviewLevel) {
            data.human_review = {
                level: parseInt(reviewLevel.value) || 0
            };
            
            const reviewerName = document.querySelector('input[name="reviewer_name"]');
            if (reviewerName && reviewerName.value.trim()) {
                data.human_review.reviewer_name = reviewerName.value;
            }
            
            const reviewerRole = document.querySelector('input[name="reviewer_role"]');
            if (reviewerRole && reviewerRole.value.trim()) {
                data.human_review.reviewer_role = reviewerRole.value;
            }
        }

        // License
        const license = document.querySelector('select[name="license"]');
        if (license && license.value !== 'None') {
            data.license = license.value;
        }
    }

    // Solo enviamos los datos del paso actual
    // El servidor usará los datos de la sesión para los pasos que no están en el formulario actual
    return data;
}

/**
 * Actualiza la vista previa llamando al API
 */
function updatePreview(step) {
    // Limpiar timeout anterior
    if (previewUpdateTimeout) {
        clearTimeout(previewUpdateTimeout);
    }

    // Esperar un poco antes de actualizar para evitar demasiadas peticiones
    previewUpdateTimeout = setTimeout(() => {
        const previewContainer = document.getElementById('preview-container');
        const previewContent = document.getElementById('preview-content');
        
        if (!previewContainer || !previewContent) return;

        // Mostrar indicador de carga
        const updatingText = (window.PREVIEW_TRANSLATIONS && window.PREVIEW_TRANSLATIONS.updating) || 'Actualizando vista previa...';
        previewContent.innerHTML = `<div class="text-center py-8 text-slate-400">${updatingText}</div>`;

        const formData = getFormData(step);
        
        // Obtener la ruta base (puede incluir prefijo de idioma)
        // La URL actual puede ser /es/paso1/, /en/paso1/, etc.
        const pathParts = window.location.pathname.split('/').filter(p => p);
        let basePath = '';
        
        // Si hay un prefijo de idioma (es, en, pt, it), incluirlo
        if (pathParts.length > 0 && ['es', 'en', 'pt', 'it'].includes(pathParts[0])) {
            basePath = '/' + pathParts[0];
        }
        
        const apiUrl = basePath + '/api/preview/';
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Mostrar la vista previa formateada
                previewContent.innerHTML = `<pre class="p-4 text-sm font-mono leading-relaxed whitespace-pre-wrap text-slate-800">${escapeHtml(data.preview)}</pre>`;
            } else {
                const errorText = (window.PREVIEW_TRANSLATIONS && window.PREVIEW_TRANSLATIONS.error) || 'Error al generar vista previa';
                previewContent.innerHTML = `<div class="text-center py-8 text-red-500">${errorText}</div>`;
            }
        })
        .catch(error => {
            console.error('Error updating preview:', error);
            const unavailableText = (window.PREVIEW_TRANSLATIONS && window.PREVIEW_TRANSLATIONS.unavailable) || 'Vista previa no disponible';
            previewContent.innerHTML = `<div class="text-center py-8 text-slate-400">${unavailableText}</div>`;
        });
    }, PREVIEW_UPDATE_DELAY);
}

/**
 * Obtiene el valor de una cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Toggle del panel de vista previa (ocultar/mostrar)
 */
function togglePreviewPanel() {
    const previewPanel = document.getElementById('preview-panel');
    const previewContainer = document.getElementById('preview-container');
    const toggleIcon = document.getElementById('preview-toggle-icon');
    
    if (!previewPanel || !previewContainer) return;
    
    const isHidden = previewPanel.classList.contains('hidden');
    
    if (isHidden) {
        previewPanel.classList.remove('hidden');
        previewContainer.classList.remove('hidden');
        if (toggleIcon) {
            toggleIcon.classList.remove('rotate-180');
        }
        // Actualizar vista previa cuando se muestra (mostrará datos de todos los pasos)
        const step = getCurrentStep();
        updatePreview(step);
        
        // Hacer scroll suave hasta el panel de vista previa
        setTimeout(() => {
            previewPanel.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest'
            });
        }, 100);
    } else {
        previewPanel.classList.add('hidden');
        previewContainer.classList.add('hidden');
        if (toggleIcon) {
            toggleIcon.classList.add('rotate-180');
        }
    }
}

/**
 * Obtiene el paso actual basándose en la URL
 */
function getCurrentStep() {
    const path = window.location.pathname;
    if (path.includes('paso1')) return 1;
    if (path.includes('paso2')) return 2;
    if (path.includes('paso3')) return 3;
    return 0;
}

/**
 * Inicializa los listeners para actualizar la vista previa
 */
function initPreviewListeners(step) {
    // Paso 1: Listeners para checkboxes
    if (step === 1 || step === 0) {
        document.querySelectorAll('.checkbox-input').forEach(checkbox => {
            checkbox.addEventListener('change', () => updatePreview(1));
        });
    }

    // Paso 2: Listeners para tipos de uso
    if (step === 2 || step === 0 || step === 1) {
        document.querySelectorAll('.usage-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', () => updatePreview(2));
        });
        
        const customUsageTextarea = document.querySelector('textarea[name="custom_usage_type"]');
        if (customUsageTextarea) {
            customUsageTextarea.addEventListener('input', () => updatePreview(2));
        }
    }

    // Paso 3: Listeners para todos los campos
    if (step === 3 || step === 0 || step === 1 || step === 2) {
        // AI Tool
        ['ai_tool_name', 'ai_tool_version', 'ai_tool_provider'].forEach(name => {
            const input = document.querySelector(`input[name="${name}"]`);
            if (input) {
                input.addEventListener('input', () => updatePreview(3));
            }
        });
        
        ['ai_tool_date_month', 'ai_tool_date_year'].forEach(name => {
            const select = document.querySelector(`select[name="${name}"]`);
            if (select) {
                select.addEventListener('change', () => updatePreview(3));
            }
        });

        // Purpose
        const purpose = document.querySelector('textarea[name="specific_purpose"]');
        if (purpose) {
            purpose.addEventListener('input', () => updatePreview(3));
        }

        // Prompts
        document.querySelectorAll('input[name^="prompt_"]').forEach(input => {
            input.addEventListener('input', () => updatePreview(3));
        });

        // Content use modes
        document.querySelectorAll('input[name="content_use_modes"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => updatePreview(3));
        });
        
        const customContentMode = document.querySelector('input[name="custom_content_use_mode"]');
        if (customContentMode) {
            customContentMode.addEventListener('input', () => updatePreview(3));
        }
        
        const contentContext = document.querySelector('textarea[name="content_use_context"]');
        if (contentContext) {
            contentContext.addEventListener('input', () => updatePreview(3));
        }

        // Human review
        document.querySelectorAll('input[name="human_review_level"]').forEach(radio => {
            radio.addEventListener('change', () => updatePreview(3));
        });
        
        ['reviewer_name', 'reviewer_role'].forEach(name => {
            const input = document.querySelector(`input[name="${name}"]`);
            if (input) {
                input.addEventListener('input', () => updatePreview(3));
            }
        });

        // License
        const license = document.querySelector('select[name="license"]');
        if (license) {
            license.addEventListener('change', () => updatePreview(3));
        }
    }

    // Actualizar vista previa inicial
    updatePreview(step);
}

