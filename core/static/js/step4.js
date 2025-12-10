/**
 * JavaScript para Paso 4: Resultado
 * Tabs, copiar al portapapeles, y feedback visual
 */

document.addEventListener('DOMContentLoaded', function() {
    let currentTab = 'text';

    window.showTab = function(tab) {
        currentTab = tab;
        const textContent = document.getElementById('contentText');
        const jsonContent = document.getElementById('contentJson');
        const textBtn = document.getElementById('tabText');
        const jsonBtn = document.getElementById('tabJson');

        if (tab === 'text') {
            textContent.classList.remove('hidden');
            jsonContent.classList.add('hidden');
            textBtn.classList.add('text-primary-700', 'bg-white', 'border-b-2', 'border-primary-500');
            textBtn.classList.remove('text-slate-500');
            jsonBtn.classList.remove('text-primary-700', 'bg-white', 'border-b-2', 'border-primary-500');
            jsonBtn.classList.add('text-slate-500');
        } else {
            jsonContent.classList.remove('hidden');
            textContent.classList.add('hidden');
            jsonBtn.classList.add('text-primary-700', 'bg-white', 'border-b-2', 'border-primary-500');
            jsonBtn.classList.remove('text-slate-500');
            textBtn.classList.remove('text-primary-700', 'bg-white', 'border-b-2', 'border-primary-500');
            textBtn.classList.add('text-slate-500');
        }
    };

    window.copyContent = function() {
        const content = currentTab === 'text'
            ? document.getElementById('contentText').innerText
            : document.getElementById('contentJson').innerText;

        navigator.clipboard.writeText(content).then(() => {
            const copyIcon = document.getElementById('copyIcon');
            const copyText = document.getElementById('copyText');
            const copyBtn = document.getElementById('copyBtn');

            // Feedback visual
            copyIcon.innerText = '✓';
            copyText.innerText = 'Copiado';
            copyBtn.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');

            setTimeout(() => {
                copyIcon.innerText = '📋';
                copyText.innerText = 'Copiar';
                copyBtn.classList.remove('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
            }, 2000);
        }).catch(err => {
            console.error('Error al copiar:', err);
            alert('No se pudo copiar al portapapeles');
        });
    };

    // Guardar declaración en la base de datos
    window.saveDeclaration = async function() {
        const saveBtn = document.getElementById('saveBtn');
        const saveBtnText = document.getElementById('saveBtnText');
        const saveMessage = document.getElementById('saveMessage');

        // Deshabilitar botón mientras se procesa
        saveBtn.disabled = true;
        saveBtnText.innerText = 'Guardando...';
        saveBtn.classList.add('opacity-75', 'cursor-not-allowed');

        try {
            // Obtener el idioma actual de la URL
            const currentPath = window.location.pathname;
            const langMatch = currentPath.match(/^\/(es|en|pt|it)\//);
            const langPrefix = langMatch ? langMatch[0] : '/';

            // Intentar obtener el CSRF token de múltiples fuentes
            const csrfToken = window.CSRF_TOKEN || getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            const response = await fetch(langPrefix + 'api/guardar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({})
            });

            // Verificar si la respuesta es exitosa
            if (!response.ok) {
                const text = await response.text();
                console.error('Response error:', text);
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success) {
                // Mostrar mensaje de éxito
                saveMessage.querySelector('p').innerText = '✓ ' + data.message;
                saveMessage.classList.remove('hidden');
                saveMessage.classList.add('border-emerald-300', 'bg-emerald-50');

                // Cambiar el botón a estado de éxito
                saveBtnText.innerText = '¡Guardado!';
                saveBtn.classList.remove('bg-emerald-600', 'hover:bg-emerald-700');
                saveBtn.classList.add('bg-emerald-700');

                // Ocultar botón de "No guardar" después de guardar
                setTimeout(() => {
                    location.reload(); // Recargar para mostrar el estado guardado
                }, 1500);
            } else {
                throw new Error(data.error || 'Error al guardar');
            }
        } catch (error) {
            console.error('Error:', error);
            saveMessage.querySelector('p').innerText = '✗ Error al guardar: ' + error.message;
            saveMessage.classList.remove('hidden');
            saveMessage.classList.add('border-red-300', 'bg-red-50');
            saveMessage.querySelector('p').classList.add('text-red-700');
            saveMessage.querySelector('p').classList.remove('text-emerald-700');

            // Rehabilitar botón
            saveBtn.disabled = false;
            saveBtnText.innerText = 'Reintentar';
            saveBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        }
    };

    // Saltar el guardado y solo descargar
    window.skipSave = function() {
        const saveSection = document.getElementById('saveDeclarationSection');
        if (saveSection) {
            saveSection.style.transition = 'all 0.3s';
            saveSection.style.opacity = '0';
            saveSection.style.maxHeight = saveSection.offsetHeight + 'px';

            setTimeout(() => {
                saveSection.style.maxHeight = '0';
                saveSection.style.padding = '0';
                saveSection.style.margin = '0';
                saveSection.style.overflow = 'hidden';

                // Crear mensaje pequeño para cambiar de opinión
                setTimeout(() => {
                    const changeMindText = saveSection.getAttribute('data-change-mind-text') || '¿Cambiaste de opinión? Haz clic aquí para guardar la declaración';
                    const changeMindbtn = document.createElement('div');
                    changeMindbtn.id = 'changeMindBtn';
                    changeMindbtn.className = 'text-center py-2';
                    changeMindbtn.innerHTML = `
                        <button onclick="showSaveSection()" class="text-sm text-emerald-600 hover:text-emerald-700 underline">
                            ${changeMindText}
                        </button>
                    `;
                    saveSection.parentNode.insertBefore(changeMindbtn, saveSection.nextSibling);
                }, 300);
            }, 300);
        }
    };

    // Mostrar nuevamente la sección de guardado si cambia de opinión
    window.showSaveSection = function() {
        const saveSection = document.getElementById('saveDeclarationSection');
        const changeMindBtn = document.getElementById('changeMindBtn');

        if (saveSection) {
            // Remover el botón de cambiar de opinión
            if (changeMindBtn) {
                changeMindBtn.remove();
            }

            // Restaurar la sección
            saveSection.style.maxHeight = 'none';
            saveSection.style.padding = '';
            saveSection.style.margin = '';
            saveSection.style.overflow = '';
            saveSection.style.opacity = '1';
        }
    };

    // Función helper para obtener el CSRF token
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

    // Animar la aparición de los badges
    const badges = document.querySelectorAll('.bg-slate-800, .bg-white.border');
    badges.forEach((badge, index) => {
        setTimeout(() => {
            badge.classList.add('animate-in', 'fade-in', 'slide-in-from-bottom-2');
        }, index * 100);
    });
});
