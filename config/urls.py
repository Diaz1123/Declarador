"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from core.views import (
    # Wizard
    home, step1_identification, step2_usage_type, step3_details, step4_output,
    # Downloads
    download_text, download_json,
    # Search
    search_declaration, view_declaration,
    # Signers
    signer_register, signer_create, signer_verify, signers_list,
    # Utils
    load_preset, preview_declaration, save_declaration, privacy_policy,
)

# Non-translatable URLs (admin, language switcher)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
]

# Translatable URLs with language prefix
urlpatterns += i18n_patterns(
    path('', home, name='home'),
    path('paso1/', step1_identification, name='step1'),
    path('paso2/', step2_usage_type, name='step2'),
    path('paso3/', step3_details, name='step3'),
    path('paso4/', step4_output, name='step4'),
    path('descargar/texto/', download_text, name='download_text'),
    path('descargar/json/', download_json, name='download_json'),
    path('cargar-plantilla/', load_preset, name='load_preset'),
    # Búsqueda y verificación de declaraciones
    path('buscar/', search_declaration, name='search'),
    path('declaracion/<str:declaration_id>/', view_declaration, name='view_declaration'),
    # Política de privacidad
    path('privacidad/', privacy_policy, name='privacy'),
    # Vista previa en tiempo real
    path('api/preview/', preview_declaration, name='preview_declaration'),
    # Guardar declaración (opcional)
    path('api/guardar/', save_declaration, name='save_declaration'),
    # Módulo de firmantes
    path('firmantes/', signers_list, name='signers_list'),
    path('firmar/', signer_register, name='signer_register'),
    path('api/firmar/', signer_create, name='signer_create'),
    path('v/<str:hash_short>/', signer_verify, name='signer_verify'),
)
