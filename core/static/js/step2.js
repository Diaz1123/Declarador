/**
 * JavaScript para Paso 2: Clasificación de Uso
 * Hace los tipos de uso interactivos con feedback visual instantáneo
 */

document.addEventListener('DOMContentLoaded', function() {
    // Hacer los tipos de uso interactivos
    document.querySelectorAll('.usage-type-item').forEach(item => {
        const checkbox = item.querySelector('.usage-checkbox');
        const icon = item.querySelector('.usage-icon');
        const title = item.querySelector('h3');

        item.addEventListener('click', function(e) {
            // Si se hace click en el textarea del campo "otro", no hacer nada
            if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'LABEL') {
                return;
            }

            // Toggle checkbox
            checkbox.checked = !checkbox.checked;

            // Update visual state
            if (checkbox.checked) {
                // Checked state
                item.classList.remove('border-slate-200', 'bg-white');
                item.classList.add('border-primary-500', 'bg-primary-50/50', 'ring-1', 'ring-primary-500');

                icon.classList.remove('border-slate-300', 'bg-white');
                icon.classList.add('bg-primary-600', 'border-primary-600', 'text-white');

                if (!icon.querySelector('.checkmark')) {
                    const check = document.createElement('span');
                    check.className = 'checkmark';
                    check.textContent = '✓';
                    icon.appendChild(check);
                }

                title.classList.remove('text-slate-800');
                title.classList.add('text-primary-900');

                // Si es "other", mostrar el textarea
                if (item.dataset.value === 'other') {
                    const customField = item.querySelector('textarea');
                    if (customField) {
                        customField.parentElement.classList.remove('hidden');
                        customField.focus(); // Auto-focus en el campo
                    }
                }
            } else {
                // Unchecked state
                item.classList.remove('border-primary-500', 'bg-primary-50/50', 'ring-1', 'ring-primary-500');
                item.classList.add('border-slate-200', 'bg-white');

                icon.classList.remove('bg-primary-600', 'border-primary-600', 'text-white');
                icon.classList.add('border-slate-300', 'bg-white');

                const checkmark = icon.querySelector('.checkmark');
                if (checkmark) {
                    checkmark.remove();
                }

                title.classList.remove('text-primary-900');
                title.classList.add('text-slate-800');

                // Si es "other", ocultar el textarea
                if (item.dataset.value === 'other') {
                    const customField = item.querySelector('textarea');
                    if (customField) {
                        customField.parentElement.classList.add('hidden');
                    }
                }
            }
            
            // Actualizar vista previa si está disponible
            if (typeof updatePreview === 'function') {
                updatePreview(2);
            }
        });
    });
});
