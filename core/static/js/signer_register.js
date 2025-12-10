// signer_register.js
// JavaScript para el formulario de registro de firmantes

// Constantes de Disciplinas (traducidas desde Django)
const Disciplines = {
    ACADEMICO: window.SIGNER_TRANSLATIONS?.academico || 'Académico',
    INVESTIGADOR: window.SIGNER_TRANSLATIONS?.investigador || 'Investigador',
    TECNICO: window.SIGNER_TRANSLATIONS?.tecnico || 'Técnico',
    GESTOR: window.SIGNER_TRANSLATIONS?.gestor || 'Gestor',
    ESTUDIANTE: window.SIGNER_TRANSLATIONS?.estudiante || 'Estudiante',
    OTRO: window.SIGNER_TRANSLATIONS?.otro || 'Otro'
};

const COUNTRIES = [
    'Alemania', 'Argentina', 'Bélgica', 'Bolivia', 'Brasil', 'Chile', 'Colombia',
    'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador', 'España', 'Francia', 'Guatemala',
    'Honduras', 'Italia', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú',
    'Polonia', 'Portugal', 'Puerto Rico', 'Reino Unido', 'República Dominicana',
    'Suiza', 'Uruguay', 'Venezuela', 'Otro'
];

// Mapeo de países a banderas (emojis)
const COUNTRY_FLAGS = {
    'Alemania': '🇩🇪',
    'Argentina': '🇦🇷',
    'Bélgica': '🇧🇪',
    'Bolivia': '🇧🇴',
    'Brasil': '🇧🇷',
    'Chile': '🇨🇱',
    'Colombia': '🇨🇴',
    'Costa Rica': '🇨🇷',
    'Cuba': '🇨🇺',
    'Ecuador': '🇪🇨',
    'El Salvador': '🇸🇻',
    'España': '🇪🇸',
    'Francia': '🇫🇷',
    'Guatemala': '🇬🇹',
    'Honduras': '🇭🇳',
    'Italia': '🇮🇹',
    'México': '🇲🇽',
    'Nicaragua': '🇳🇮',
    'Panamá': '🇵🇦',
    'Paraguay': '🇵🇾',
    'Perú': '🇵🇪',
    'Polonia': '🇵🇱',
    'Portugal': '🇵🇹',
    'Puerto Rico': '🇵🇷',
    'Reino Unido': '🇬🇧',
    'República Dominicana': '🇩🇴',
    'Suiza': '🇨🇭',
    'Uruguay': '🇺🇾',
    'Venezuela': '🇻🇪',
    'Otro': '🌍'
};

// Función para obtener la bandera de un país
function getCountryFlag(country) {
    return COUNTRY_FLAGS[country] || '🌍';
}

// Utilidades ORCID
function validateORCIDFormat(orcid) {
    const pattern = /^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$/;
    return pattern.test(orcid);
}

function formatORCID(value) {
    const clean = value.replace(/[^0-9X]/gi, '').toUpperCase().slice(0, 16);
    const parts = [];
    for (let i = 0; i < clean.length; i += 4) {
        parts.push(clean.slice(i, i + 4));
    }
    return parts.join('-');
}

async function fetchOrcidProfile(orcid) {
    try {
        const response = await fetch(`https://pub.orcid.org/v3.0/${orcid}`, {
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) throw new Error('ORCID no encontrado');

        const data = await response.json();
        const person = data.person || {};
        const name = person.name || {};
        const givenNames = name['given-names']?.value || '';
        const familyName = name['family-name']?.value || '';
        const fullName = `${givenNames} ${familyName}`.trim();

        return {
            name: fullName,
            isNamePublic: !!fullName,
            orcid: orcid,
            profileUrl: `https://orcid.org/${orcid}`
        };
    } catch (error) {
        throw new Error('No se pudo verificar el ORCID');
    }
}

async function searchRorOrganizations(query) {
    if (!query || query.length < 3) {
        appState.rorResults = [];
        appState.showRorDropdown = false;
        updateRorDropdown();
        return;
    }

    try {
        appState.rorStatus = 'searching';
        const encodedQuery = encodeURIComponent(query);
        const response = await fetch(`https://api.ror.org/v2/organizations?query=${encodedQuery}`);

        if (!response.ok) throw new Error('Error en búsqueda');

        const data = await response.json();
        appState.rorResults = (data.items || []).slice(0, 10).map(org => {
            const displayName = org.names?.find(n => n.types?.includes('ror_display'))?.value ||
                              org.names?.find(n => n.types?.includes('label'))?.value ||
                              org.names?.[0]?.value || 'Sin nombre';

            const country = org.locations?.[0]?.geonames_details?.country_name || '';
            const rorId = org.id || '';

            return {
                id: rorId,
                name: displayName,
                country: country,
                types: org.types || [],
                url: rorId
            };
        });

        appState.rorStatus = 'idle';
        appState.showRorDropdown = appState.rorResults.length > 0;
        updateRorDropdown();
    } catch (error) {
        appState.rorStatus = 'error';
        appState.rorResults = [];
        appState.showRorDropdown = false;
        updateRorDropdown();
    }
}

// Estado de la aplicación
const appState = {
    step: 0,
    isSubmitting: false,
    isComplete: false,
    orcidStatus: 'idle',
    orcidData: null,
    orcidTimeout: null,
    rorStatus: 'idle',
    rorResults: [],
    rorSelected: null,
    rorTimeout: null,
    showRorDropdown: false,
    form: {
        fullName: '', email: '', orcid: '', affiliation: '', affiliationRorId: '',
        discipline: '', country: '', profileUrl: '', declaration: '',
        agreedToTerms: false, publicListing: true
    },
    errors: {}
};

// Validación
function validate(step) {
    const e = {};
    if (step === 0) {
        if (!appState.form.fullName.trim()) e.fullName = 'Ingresa tu nombre completo';
        if (!appState.form.email.trim()) e.email = 'Ingresa tu correo';
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(appState.form.email)) e.email = 'Correo no válido';
        if (!appState.form.orcid.trim()) e.orcid = 'Ingresa tu ORCID';
        else if (!validateORCIDFormat(appState.form.orcid)) e.orcid = 'Formato: 0000-0000-0000-0000';
    }
    if (step === 1) {
        if (!appState.form.affiliation.trim()) e.affiliation = 'Ingresa tu institución';
        if (!appState.form.discipline) e.discipline = 'Selecciona una disciplina';
    }
    if (step === 3 && !appState.form.agreedToTerms) e.agreedToTerms = 'Debes aceptar para continuar';
    appState.errors = e;
    return Object.keys(e).length === 0;
}

function updateRorDropdown() {
    const dropdown = document.getElementById('rorDropdown');
    if (!dropdown) return;

    if (!appState.showRorDropdown || appState.rorResults.length === 0) {
        dropdown.classList.add('hidden');
        return;
    }

    dropdown.classList.remove('hidden');
    dropdown.innerHTML = appState.rorResults.map((org, idx) => `
        <div class="ror-result px-4 py-3 hover:bg-slate-50 cursor-pointer border-b border-slate-100 last:border-0 transition-colors"
             data-index="${idx}">
            <div class="flex items-start gap-3">
                <div class="flex-shrink-0 mt-1">
                    <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-slate-900 truncate">${org.name}</p>
                    <p class="text-xs text-slate-500 mt-0.5">${org.country || 'País desconocido'}</p>
                </div>
            </div>
        </div>
    `).join('');

    // Agregar event listeners
    dropdown.querySelectorAll('.ror-result').forEach((el) => {
        el.addEventListener('click', () => {
            const idx = parseInt(el.dataset.index);
            selectRorOrganization(appState.rorResults[idx]);
        });
    });
}

function selectRorOrganization(org) {
    appState.rorSelected = org;
    appState.form.affiliation = org.name;
    appState.form.affiliationRorId = org.id;
    appState.showRorDropdown = false;
    delete appState.errors.affiliation;

    // Actualizar input y dropdown
    const input = document.querySelector('input[name="affiliation"]');
    if (input) input.value = org.name;

    updateRorDropdown();
    updateRorFeedback();
    updateErrorDisplay('affiliation');
}

function updateRorFeedback() {
    const feedback = document.getElementById('rorFeedback');
    if (!feedback) return;

    if (appState.rorSelected) {
        feedback.innerHTML = `
            <div class="mt-2 p-3 bg-emerald-50 rounded-xl border border-emerald-100 text-sm">
                <div class="flex items-start gap-2">
                    <svg class="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <div class="flex-1">
                        <p class="font-medium text-emerald-800">Institución verificada en ROR</p>
                        <a href="${appState.rorSelected.url}" target="_blank" rel="noopener noreferrer"
                           class="text-xs text-emerald-600 hover:text-emerald-700 underline mt-1 inline-flex items-center gap-1">
                            Ver en ROR
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                            </svg>
                        </a>
                    </div>
                </div>
            </div>
        `;
    } else {
        feedback.innerHTML = '';
    }
}

// Actualizar campo
function updateField(field, value) {
    if (field === 'orcid') {
        value = formatORCID(value);
        appState.form[field] = value;
        delete appState.errors[field];

        // ORCID validation
        clearTimeout(appState.orcidTimeout);
        if (value.length === 19) {
            appState.orcidTimeout = setTimeout(() => {
                if (validateORCIDFormat(value)) {
                    validateORCIDReal(value);
                } else {
                    appState.orcidStatus = 'invalid';
                    appState.orcidData = { name: '', isNamePublic: false, orcid: value, profileUrl: '', error: 'Formato inválido' };
                    updateOrcidFeedback();
                }
            }, 600);
        } else {
            appState.orcidStatus = 'idle';
            appState.orcidData = null;
            updateOrcidFeedback();
        }
    } else if (field === 'affiliation') {
        appState.form[field] = value;
        delete appState.errors[field];

        // ROR search
        clearTimeout(appState.rorTimeout);
        if (value.length >= 3) {
            appState.rorTimeout = setTimeout(() => {
                searchRorOrganizations(value);
            }, 500);
        } else {
            appState.rorResults = [];
            appState.showRorDropdown = false;
            appState.rorSelected = null;
            appState.form.affiliationRorId = '';
            updateRorDropdown();
            updateRorFeedback();
        }
    } else {
        appState.form[field] = value;
        delete appState.errors[field];
    }

    updateErrorDisplay(field);
}

async function validateORCIDReal(orcid) {
    appState.orcidStatus = 'checking';
    updateOrcidFeedback();

    try {
        const profile = await fetchOrcidProfile(orcid);
        appState.orcidData = profile;
        appState.orcidStatus = 'valid';

        if (profile.name && !appState.form.fullName) {
            appState.form.fullName = profile.name;
            const nameInput = document.querySelector('input[name="fullName"]');
            if (nameInput) nameInput.value = profile.name;
        }
        updateOrcidFeedback();
    } catch (error) {
        appState.orcidStatus = 'error';
        appState.orcidData = {
            name: '', isNamePublic: false, orcid, profileUrl: '',
            error: error.message || 'Error desconocido'
        };
        updateOrcidFeedback();
    }
}

function updateOrcidFeedback() {
    const indicator = document.getElementById('orcidIndicator');
    const feedback = document.getElementById('orcidFeedback');
    const input = document.querySelector('input[name="orcid"]');

    if (!indicator || !feedback || !input) return;

    // Update indicator
    if (appState.orcidStatus === 'checking') {
        indicator.innerHTML = '⏳';
    } else if (appState.orcidStatus === 'valid') {
        indicator.innerHTML = '✓';
        input.classList.add('border-emerald-400', 'bg-emerald-50/30');
        input.classList.remove('border-rose-300');
    } else if (appState.orcidStatus === 'invalid' || appState.orcidStatus === 'error') {
        indicator.innerHTML = '⚠️';
        input.classList.remove('border-emerald-400', 'bg-emerald-50/30');
    } else {
        indicator.innerHTML = '';
        input.classList.remove('border-emerald-400', 'bg-emerald-50/30', 'border-rose-300');
    }

    // Update feedback message
    if (appState.orcidStatus === 'valid' && appState.orcidData) {
        feedback.innerHTML = `
            <div class="mt-2 p-3 bg-emerald-50 rounded-xl border border-emerald-100 text-sm text-emerald-800">
                <p class="font-medium">✓ Identidad verificada</p>
                ${appState.orcidData.name ? `<p class="text-emerald-600/80 text-xs mt-0.5">Registrado como: ${appState.orcidData.name}</p>` : ''}
            </div>
        `;
    } else {
        feedback.innerHTML = '';
    }
}

function updateErrorDisplay(field) {
    const errorEl = document.getElementById(`error-${field}`);
    if (errorEl) {
        if (appState.errors[field]) {
            errorEl.textContent = appState.errors[field];
            errorEl.classList.remove('hidden');
        } else {
            errorEl.classList.add('hidden');
        }
    }
}

// Renderizar pasos
function renderStepNav() {
    const nav = document.getElementById('stepNav');
    const steps = [0, 1, 2, 3];
    nav.innerHTML = `
        <div class="flex items-center justify-center gap-2">
            ${steps.map(i => `
                <div class="flex items-center">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-all ${
                        i === appState.step
                            ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-200'
                            : i < appState.step
                                ? 'bg-emerald-400 text-white'
                                : 'bg-slate-200 text-slate-400'
                    }">
                        ${i < appState.step ? '✓' : i + 1}
                    </div>
                    ${i < 3 ? `
                        <div class="w-8 h-0.5 ${i < appState.step ? 'bg-emerald-300' : 'bg-slate-200'}"></div>
                    ` : ''}
                </div>
            `).join('')}
        </div>
    `;
}

function renderStep() {
    const container = document.getElementById('formStepsContainer');
    let html = '';

    const t = window.SIGNER_TRANSLATIONS || {};

    switch(appState.step) {
        case 0:
            html = `
                <div class="space-y-6">
                    <div class="mb-8">
                        <h2 class="text-2xl font-bold text-slate-900">${t.tuIdentidad || 'Tu identidad'}</h2>
                        <p class="text-slate-500">${t.datosVerificables || 'Datos verificables para tu firma digital.'}</p>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">${t.nombreCompleto || 'Nombre completo'} <span class="text-rose-400">*</span></label>
                        <input type="text" name="fullName" value="${appState.form.fullName}"
                            class="w-full px-4 py-3.5 form-input rounded-xl ${appState.errors.fullName ? 'border-rose-300' : ''}"
                            placeholder="${t.placeholderNombre || 'Ej. Dra. María García'}">
                        <p id="error-fullName" class="text-rose-500 text-xs font-medium mt-1 ${appState.errors.fullName ? '' : 'hidden'}">${appState.errors.fullName || ''}</p>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">${t.correoElectronico || 'Correo electrónico'} <span class="text-rose-400">*</span></label>
                        <input type="email" name="email" value="${appState.form.email}"
                            class="w-full px-4 py-3.5 form-input rounded-xl ${appState.errors.email ? 'border-rose-300' : ''}"
                            placeholder="${t.placeholderEmail || 'nombre@institucion.edu'}">
                        <p id="error-email" class="text-rose-500 text-xs font-medium mt-1 ${appState.errors.email ? '' : 'hidden'}">${appState.errors.email || ''}</p>
                        <p class="text-xs text-slate-400 mt-1">${t.privadoValidacion || 'Privado. Solo para validación.'}</p>
                    </div>

                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <label class="text-sm font-semibold text-slate-700">ORCID <span class="text-rose-400">*</span></label>
                            <a href="https://orcid.org/register" target="_blank" class="text-xs font-medium text-cyan-600 hover:text-cyan-700">
                                ${t.obtenerOrcid || 'Obtener ORCID'} →
                            </a>
                        </div>
                        <div class="relative">
                            <input type="text" name="orcid" value="${appState.form.orcid}"
                                class="w-full px-4 py-3.5 form-input rounded-xl font-mono ${appState.errors.orcid ? 'border-rose-300' : ''}"
                                placeholder="0000-0000-0000-0000" maxlength="19">
                            <div id="orcidIndicator" class="absolute right-4 top-1/2 -translate-y-1/2"></div>
                        </div>
                        <p id="error-orcid" class="text-rose-500 text-xs font-medium mt-1 ${appState.errors.orcid ? '' : 'hidden'}">${appState.errors.orcid || ''}</p>
                        <div id="orcidFeedback"></div>
                    </div>
                </div>
            `;
            break;

        case 1:
            html = `
                <div class="space-y-6">
                    <div class="mb-8">
                        <h2 class="text-2xl font-bold text-slate-900">${t.contextoProfesional || 'Contexto profesional'}</h2>
                        <p class="text-slate-500">${t.desdeQueRol || '¿Desde qué rol firmas este compromiso?'}</p>
                    </div>

                    <div class="relative">
                        <label class="block text-sm font-semibold text-slate-700 mb-2">
                            <span class="inline-flex items-center gap-2">
                                ${t.institucionOrganizacion || 'Institución / Organización'} <span class="text-rose-400">*</span>
                                <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                                </svg>
                            </span>
                        </label>
                        <input type="text" name="affiliation" value="${appState.form.affiliation}"
                            class="w-full px-4 py-3.5 form-input rounded-xl ${appState.errors.affiliation ? 'border-rose-300' : ''}"
                            placeholder="${t.placeholderInstitucion || 'Ej. Universidad Nacional, Google, NASA...'}" autocomplete="off">
                        <p class="text-xs text-slate-500 mt-1.5">${t.rorSugerira || 'Escribe el nombre de tu institución. ROR sugerirá opciones verificadas (opcional).'}</p>
                        <p id="error-affiliation" class="text-rose-500 text-xs font-medium mt-1 ${appState.errors.affiliation ? '' : 'hidden'}">${appState.errors.affiliation || ''}</p>

                        <!-- ROR Dropdown -->
                        <div id="rorDropdown" class="hidden absolute z-10 w-full mt-1 bg-white border border-slate-200 rounded-xl shadow-xl max-h-80 overflow-y-auto"></div>

                        <!-- ROR Feedback -->
                        <div id="rorFeedback"></div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-2">${t.disciplinaRol || 'Disciplina / Rol'} <span class="text-rose-400">*</span></label>
                            <select name="discipline"
                                class="w-full px-4 py-3.5 form-select rounded-xl ${appState.errors.discipline ? 'border-rose-300' : ''}">
                                <option value="">${t.selecciona || 'Selecciona...'}</option>
                                ${Object.values(Disciplines).map(d => `<option value="${d}" ${appState.form.discipline === d ? 'selected' : ''}>${d}</option>`).join('')}
                            </select>
                            <p id="error-discipline" class="text-rose-500 text-xs font-medium mt-1 ${appState.errors.discipline ? '' : 'hidden'}">${appState.errors.discipline || ''}</p>
                        </div>

                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-2">${t.pais || 'País'}</label>
                            <select name="country" class="w-full px-4 py-3.5 form-select rounded-xl">
                                <option value="">${t.selecciona || 'Selecciona...'}</option>
                                ${COUNTRIES.map(c => `<option value="${c}" ${appState.form.country === c ? 'selected' : ''}>${c}</option>`).join('')}
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">${t.enlacePerfil || 'Enlace a perfil'} (${t.opcional || 'Opcional'})</label>
                        <input type="url" name="profileUrl" value="${appState.form.profileUrl}"
                            class="w-full px-4 py-3.5 form-input rounded-xl"
                            placeholder="https://linkedin.com/in/...">
                    </div>
                </div>
            `;
            break;

        case 2:
            html = `
                <div class="space-y-6">
                    <div class="mb-8">
                        <h2 class="text-2xl font-bold text-slate-900">${t.declaracion || 'Declaración'}</h2>
                        <p class="text-slate-500">${t.fraseBreveMotiviacion || 'Una frase breve sobre tu motivación'} (${t.opcional || 'Opcional'}).</p>
                    </div>

                    <div class="relative">
                        <label class="block text-sm font-semibold text-slate-700 mb-2">${t.mensajePersonal || 'Mensaje personal'}</label>
                        <textarea name="declaration"
                            class="w-full px-4 py-4 form-textarea rounded-2xl resize-none h-40"
                            placeholder="${t.placeholderDeclaracion || 'Escribe aquí tu compromiso...'}" maxlength="280">${appState.form.declaration}</textarea>
                        <div class="absolute bottom-4 right-4 text-xs text-slate-400 pointer-events-none">
                            <span id="charCount">${appState.form.declaration.length}</span>/280
                        </div>
                    </div>
                </div>
            `;
            break;

        case 3:
            html = `
                <div class="space-y-8">
                    <div class="mb-4">
                        <h2 class="text-2xl font-bold text-slate-900">${t.revisarYFirmar || 'Revisar y Firmar'}</h2>
                        <p class="text-slate-500">${t.confirmaDatos || 'Confirma que los datos son correctos.'}</p>
                    </div>

                    <div class="bg-slate-50 rounded-2xl p-6 border border-slate-100 space-y-4">
                        <div class="flex justify-between items-center py-2 border-b border-slate-200">
                            <span class="text-sm text-slate-500">${t.nombre || 'Nombre'}</span>
                            <span class="font-semibold text-slate-900">${appState.form.fullName}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-slate-200">
                            <span class="text-sm text-slate-500">ORCID</span>
                            <span class="font-mono text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded text-sm">${appState.form.orcid}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-slate-200">
                            <span class="text-sm text-slate-500">${t.afiliacion || 'Afiliación'}</span>
                            <span class="font-medium text-slate-900 text-right truncate max-w-[200px]">${appState.form.affiliation}</span>
                        </div>
                        ${appState.form.declaration ? `
                            <div class="pt-2">
                                <span class="text-sm text-slate-500 block mb-2">${t.declaracion || 'Declaración'}</span>
                                <p class="text-sm text-slate-700 italic border-l-2 border-slate-200 pl-3">"${appState.form.declaration}"</p>
                            </div>
                        ` : ''}
                    </div>

                    <div class="space-y-4">
                        <label class="flex items-start gap-3 cursor-pointer group p-3 hover:bg-slate-50 rounded-xl transition-colors -mx-3">
                            <input type="checkbox" name="agreedToTerms" ${appState.form.agreedToTerms ? 'checked' : ''}
                                class="mt-1">
                            <span class="text-sm text-slate-600 leading-relaxed">
                                ${t.aceptoPublicar || 'Acepto publicar esta firma bajo licencia abierta CC0. Entiendo que se generará un hash inmutable.'}
                            </span>
                        </label>
                        <p id="error-agreedToTerms" class="text-rose-500 text-xs font-medium ml-8 ${appState.errors.agreedToTerms ? '' : 'hidden'}">${appState.errors.agreedToTerms || ''}</p>
                    </div>
                </div>
            `;
            break;
    }

    container.innerHTML = html;
    attachInputListeners();
}

function attachInputListeners() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], textarea, select');
    inputs.forEach(input => {
        const field = input.getAttribute('name');
        input.addEventListener('input', (e) => {
            updateField(field, e.target.value);
            if (field === 'declaration') {
                const charCount = document.getElementById('charCount');
                if (charCount) charCount.textContent = e.target.value.length;
            }
        });
    });

    const checkbox = document.querySelector('input[type="checkbox"][name="agreedToTerms"]');
    if (checkbox) {
        checkbox.addEventListener('change', (e) => {
            updateField('agreedToTerms', e.target.checked);
        });
    }
}

function updateNavButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const prevPlaceholder = document.getElementById('prevPlaceholder');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const progressBar = document.getElementById('progressBar');
    const recaptchaContainer = document.getElementById('recaptcha-container-step0');

    // Progress bar
    progressBar.style.width = `${((appState.step + 1) / 4) * 100}%`;

    // Previous button
    if (appState.step > 0) {
        prevBtn.classList.remove('hidden');
        prevBtn.classList.add('flex');
        prevPlaceholder.style.display = 'none';
    } else {
        prevBtn.classList.add('hidden');
        prevBtn.classList.remove('flex');
        prevPlaceholder.style.display = 'block';
    }

    // Manejar visibilidad de reCAPTCHA
    if (recaptchaContainer) {
        if (appState.step === 0 && window.RECAPTCHA_ENABLED) {
            // Mostrar reCAPTCHA en paso 0
            recaptchaContainer.classList.remove('hidden');
            // Verificar si ya fue completado en esta sesión
            const verified = sessionStorage.getItem('recaptcha_verified_signer');
            if (verified === 'true') {
                nextBtn.disabled = false;
            } else {
                nextBtn.disabled = true;
            }
        } else {
            // Ocultar reCAPTCHA en otros pasos
            recaptchaContainer.classList.add('hidden');
            nextBtn.disabled = false;
        }
    }

    // Next/Submit button
    if (appState.step < 3) {
        nextBtn.classList.remove('hidden');
        nextBtn.classList.add('flex');
        submitBtn.classList.add('hidden');
        submitBtn.classList.remove('flex');
    } else {
        nextBtn.classList.add('hidden');
        nextBtn.classList.remove('flex');
        submitBtn.classList.remove('hidden');
        submitBtn.classList.add('flex');
    }
}

// Navegación
function nextStep() {
    if (validate(appState.step)) {
        appState.step = Math.min(appState.step + 1, 3);
        renderStepNav();
        renderStep();
        updateNavButtons();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        renderStep();
    }
}

function prevStep() {
    appState.step = Math.max(appState.step - 1, 0);
    renderStepNav();
    renderStep();
    updateNavButtons();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function submitForm() {
    if (!validate(3)) {
        renderStep();
        return;
    }

    appState.isSubmitting = true;
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Procesando...';

    try {
        // Preparar payload con datos del formulario
        const payload = {
            fullName: appState.form.fullName,
            email: appState.form.email,
            orcid: appState.form.orcid,
            affiliation: appState.form.affiliation,
            affiliationRorId: appState.form.affiliationRorId || '',
            discipline: appState.form.discipline,
            country: appState.form.country,
            profileUrl: appState.form.profileUrl,
            declaration: appState.form.declaration,
            agreedToTerms: appState.form.agreedToTerms,
            publicListing: appState.form.publicListing,
            orcidVerified: appState.orcidStatus === 'valid',
            orcidRegisteredName: appState.orcidData?.name || null
        };

        // Agregar token de reCAPTCHA si está habilitado
        if (window.RECAPTCHA_ENABLED) {
            const token = sessionStorage.getItem('recaptcha_token_signer');
            if (token) {
                payload.recaptchaToken = token;
            }
        }

        const response = await fetch(window.SIGNER_CONFIG.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.SIGNER_CONFIG.csrfToken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error || 'Error al registrar firmante');
            appState.isSubmitting = false;
            submitBtn.disabled = false;
            submitBtn.innerHTML = '✓ Firmar Ahora';
            return;
        }

        // Mostrar página de éxito
        showSuccessPage(data.signer);
    } catch (error) {
        alert('Error de conexión: ' + error.message);
        appState.isSubmitting = false;
        submitBtn.disabled = false;
        submitBtn.innerHTML = '✓ Firmar Ahora';
    }
}

function showSuccessPage(signer) {
    const app = document.getElementById('app');
    const t = window.SIGNER_TRANSLATIONS || {};
    
    app.innerHTML = `
        <div class="bg-white rounded-[2rem] shadow-2xl shadow-slate-200 p-8 md:p-12 overflow-hidden relative">
            <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-lime-400 via-cyan-400 to-violet-400"></div>

            <div class="text-center mb-10">
                <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-50 mb-6 border border-emerald-100">
                    <svg class="w-8 h-8 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                </div>
                <h1 class="text-3xl font-bold text-slate-900 mb-2">${t.compromisoRegistrado || '¡Compromiso registrado!'}</h1>
                <p class="text-slate-500">${t.firmaVerificada || 'Tu firma ha sido verificada criptográficamente.'}</p>
            </div>

            <div class="bg-slate-50 p-6 rounded-2xl mb-8 border border-slate-100">
                <div class="text-center mb-4">
                    <p class="font-semibold text-slate-900 text-lg">${signer.fullName}</p>
                    <p class="text-sm text-slate-600">${signer.affiliation}</p>
                    <p class="text-xs text-emerald-600 font-mono mt-2">${signer.orcid}</p>
                </div>

                <div class="flex items-center justify-between p-4 bg-white rounded-xl border border-slate-100">
                    <div>
                        <p class="font-semibold text-slate-900 text-sm">${t.hashVerificacion || 'Hash de verificación'}</p>
                        <p class="text-xs text-slate-500 font-mono">${signer.hashShort}</p>
                    </div>
                    <button onclick="copyToClipboard('${signer.verificationUrl}')" class="p-2 hover:bg-slate-50 rounded-lg transition-colors text-slate-400 hover:text-cyan-600">
                        📋
                    </button>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <a href="${signer.verificationUrl}" target="_blank" class="flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-slate-900 text-white font-medium hover:bg-slate-800 transition-colors">
                    ${t.verBadge || 'Ver Badge'}
                </a>
                <button onclick="location.reload()" class="flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-white border-2 border-slate-100 text-slate-700 font-medium hover:border-slate-200 transition-colors">
                    ${t.firmarOtro || 'Firmar otro'}
                </button>
            </div>
        </div>
    `;
}

function copyToClipboard(text) {
    const t = window.SIGNER_TRANSLATIONS || {};
    navigator.clipboard.writeText(text).then(() => {
        alert(t.enlaceCopiado || '¡Enlace copiado al portapeles!');
    });
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    renderStepNav();
    renderStep();
    updateNavButtons();

    document.getElementById('prevBtn').addEventListener('click', prevStep);
    document.getElementById('nextBtn').addEventListener('click', nextStep);
    document.getElementById('submitBtn').addEventListener('click', submitForm);
});

// Exponer funciones globales
window.copyToClipboard = copyToClipboard;
