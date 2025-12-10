/**
 * JavaScript para Paso 1: Diagnóstico
 * Hace las casillas interactivas con feedback visual instantáneo
 */

document.addEventListener('DOMContentLoaded', function() {
    // Hacer las casillas interactivas
    document.querySelectorAll('.checklist-item').forEach(item => {
        const checkbox = item.querySelector('.checkbox-input');
        const icon = item.querySelector('.checkbox-icon');
        const text = item.querySelector('.checkbox-text');

        item.addEventListener('click', function(e) {
            // Toggle checkbox
            checkbox.checked = !checkbox.checked;

            // Update visual state
            if (checkbox.checked) {
                // Checked state
                item.classList.remove('border-slate-200', 'bg-white');
                item.classList.add('border-primary-500', 'bg-primary-50', 'ring-1', 'ring-primary-500', 'shadow-sm');

                icon.classList.remove('border-slate-300', 'bg-white');
                icon.classList.add('bg-primary-500', 'border-primary-500', 'text-white');

                if (!icon.querySelector('.checkmark')) {
                    const check = document.createElement('span');
                    check.className = 'checkmark';
                    check.textContent = '✓';
                    icon.appendChild(check);
                }

                text.classList.remove('text-slate-700');
                text.classList.add('text-primary-900');
            } else {
                // Unchecked state
                item.classList.remove('border-primary-500', 'bg-primary-50', 'ring-1', 'ring-primary-500', 'shadow-sm');
                item.classList.add('border-slate-200', 'bg-white');

                icon.classList.remove('bg-primary-500', 'border-primary-500', 'text-white');
                icon.classList.add('border-slate-300', 'bg-white');

                const checkmark = icon.querySelector('.checkmark');
                if (checkmark) {
                    checkmark.remove();
                }

                text.classList.remove('text-primary-900');
                text.classList.add('text-slate-700');
            }
            
            // Actualizar vista previa si está disponible
            if (typeof updatePreview === 'function') {
                updatePreview(1);
            }
        });
    });
});
