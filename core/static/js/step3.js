/**
 * JavaScript para Paso 3: Detalles
 * Contador de caracteres y manejo de prompts dinámicos
 */

document.addEventListener('DOMContentLoaded', function() {
    // Contador de caracteres para el propósito
    const purposeTextarea = document.querySelector('textarea[name="specific_purpose"]');
    if (purposeTextarea) {
        const maxLength = purposeTextarea.getAttribute('maxlength') || 600;
        const counter = document.createElement('div');
        counter.className = 'text-xs text-slate-400 mt-1 text-right';
        counter.textContent = `${purposeTextarea.value.length}/${maxLength}`;
        purposeTextarea.parentElement.appendChild(counter);

        purposeTextarea.addEventListener('input', function() {
            counter.textContent = `${this.value.length}/${maxLength}`;

            // Cambiar color si se acerca al límite
            if (this.value.length > maxLength * 0.9) {
                counter.classList.add('text-amber-600', 'font-semibold');
            } else {
                counter.classList.remove('text-amber-600', 'font-semibold');
            }
        });
    }

    // Función para agregar prompts dinámicamente
    let promptCount = document.querySelectorAll('[name^="prompt_"]').length;

    window.addPrompt = function() {
        const container = document.getElementById('promptsContainer');
        const div = document.createElement('div');
        div.className = 'flex gap-2 animate-in fade-in slide-in-from-left-2';
        div.innerHTML = `
            <input
                name="prompt_${promptCount}"
                class="flex-1 form-input rounded-lg border-slate-300 focus:border-primary-500 focus:ring-primary-500"
                placeholder="Copia aquí la instrucción principal...">
            <button
                type="button"
                onclick="this.parentElement.remove()"
                class="px-3 text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                ✕
            </button>
        `;
        container.appendChild(div);

        // Auto-focus en el nuevo campo
        div.querySelector('input').focus();

        promptCount++;
    };

    // Mejorar interactividad de los radio buttons de revisión
    document.querySelectorAll('input[name="human_review_level"]').forEach(radio => {
        radio.addEventListener('change', function() {
            // Scroll suave a los campos de revisor si el nivel > 0
            if (parseInt(this.value) > 0) {
                const reviewerFields = document.querySelector('input[name="reviewer_name"]');
                if (reviewerFields) {
                    setTimeout(() => {
                        reviewerFields.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        reviewerFields.focus();
                    }, 300);
                }
            }
        });
    });

    // Mejorar interactividad de checkboxes de integración
    document.querySelectorAll('input[name="content_use_modes"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.closest('label');
            if (this.checked) {
                label.classList.add('bg-primary-50');
            } else {
                label.classList.remove('bg-primary-50');
            }
        });
    });
});
