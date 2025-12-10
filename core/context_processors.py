"""
Context processors para templates
"""
from django.conf import settings


def recaptcha_keys(request):
    """
    Agrega las keys de reCAPTCHA al contexto de los templates
    """
    return {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        'RECAPTCHA_ENABLED': settings.RECAPTCHA_ENABLED,
    }
