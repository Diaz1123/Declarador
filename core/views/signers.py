"""
Vistas del módulo de firmantes del compromiso ético de IA.
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import get_language
import json as json_lib
import traceback

from ..models import Signer
from ..translations import get_translated_glossary


@ensure_csrf_cookie
def signer_register(request):
    """Vista principal para registrarse como firmante del compromiso ético de IA"""
    current_lang = get_language()

    context = {
        'glossary': get_translated_glossary(current_lang),
    }
    return render(request, 'core/signer_register.html', context)


@require_http_methods(["POST"])
def signer_create(request):
    """API endpoint para crear un nuevo firmante"""
    try:
        # Obtener datos del cuerpo de la petición
        data = json_lib.loads(request.body)

        # Verificar reCAPTCHA si está habilitado
        from django.conf import settings
        from ..utils import verify_recaptcha

        if settings.RECAPTCHA_ENABLED:
            recaptcha_token = data.get('recaptchaToken')
            remote_ip = request.META.get('REMOTE_ADDR')

            verification = verify_recaptcha(recaptcha_token, remote_ip)

            if not verification['success']:
                error_msg = 'Verificación reCAPTCHA fallida. Por favor intenta de nuevo.'
                if verification.get('error_codes'):
                    error_msg += f" Códigos de error: {', '.join(verification['error_codes'])}"

                return JsonResponse({
                    'success': False,
                    'error': error_msg
                }, status=400)

        # Validaciones básicas
        required_fields = ['fullName', 'email', 'orcid', 'affiliation', 'discipline']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }, status=400)

        # Verificar si el email ya existe
        if Signer.objects.filter(email=data['email']).exists():
            return JsonResponse({
                'success': False,
                'error': 'Este correo electrónico ya está registrado'
            }, status=400)

        # Verificar si el ORCID ya existe
        if Signer.objects.filter(orcid=data['orcid']).exists():
            return JsonResponse({
                'success': False,
                'error': 'Este ORCID ya está registrado'
            }, status=400)

        # Crear nuevo firmante
        signer = Signer(
            full_name=data['fullName'],
            email=data['email'],
            orcid=data['orcid'],
            affiliation=data['affiliation'],
            affiliation_ror_id=data.get('affiliationRorId', ''),
            discipline=data['discipline'],
            country=data.get('country', ''),
            profile_url=data.get('profileUrl', ''),
            declaration=data.get('declaration', ''),
            orcid_verified=data.get('orcidVerified', False),
            orcid_registered_name=data.get('orcidRegisteredName', ''),
            agreed_to_terms=data.get('agreedToTerms', True),
            public_listing=data.get('publicListing', True)
        )

        signer.save()

        # Preparar respuesta con datos generados
        response_data = {
            'success': True,
            'signer': {
                'id': signer.signer_id,
                'fullName': signer.full_name,
                'orcid': signer.orcid,
                'affiliation': signer.affiliation,
                'hashShort': signer.hash_short,
                'validationHash': signer.validation_hash,
                'verificationUrl': signer.get_verification_url(request),
                'orcidVerified': signer.orcid_verified,
                'orcidRegisteredName': signer.orcid_registered_name,
                'timestamp': signer.created_at.isoformat()
            }
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


@require_http_methods(["GET"])
def signer_verify(request, hash_short):
    """Vista pública para verificar un firmante por su hash corto"""
    current_lang = get_language()

    try:
        signer = get_object_or_404(Signer, hash_short=hash_short)

        context = {
            'signer': signer,
            'glossary': get_translated_glossary(current_lang),
        }
        return render(request, 'core/signer_verify.html', context)

    except Exception:
        return render(request, 'core/not_found.html', {'query': hash_short})


@require_http_methods(["GET"])
def signers_list(request):
    """Lista pública de firmantes (solo los que aceptaron listado público)"""
    current_lang = get_language()

    # Obtener solo firmantes que aceptaron listado público
    signers = Signer.objects.filter(public_listing=True).order_by('-created_at')

    context = {
        'signers': signers,
        'total_signers': signers.count(),
        'glossary': get_translated_glossary(current_lang),
    }
    return render(request, 'core/signers_list.html', context)
