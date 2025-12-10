"""
Vistas para búsqueda y verificación de declaraciones.
"""
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.utils.translation import get_language

from ..models import Declaration
from ..utils import (
    generate_declaration_text,
    generate_declaration_json,
)
from ..translations import get_translated_glossary


@require_http_methods(["GET", "POST"])
def search_declaration(request):
    """Página de búsqueda de declaraciones por hash o ID"""
    current_lang = get_language()

    context = {
        'glossary': get_translated_glossary(current_lang),
        'result': None,
        'not_found': False,
        'query': ''
    }

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        context['query'] = query

        if query:
            # Buscar por hash o ID
            try:
                # Intentar buscar por hash
                declaration = Declaration.objects.filter(validation_hash__iexact=query).first()

                # Si no se encuentra, intentar por ID
                if not declaration:
                    declaration = Declaration.objects.filter(declaration_id__iexact=query).first()

                if declaration:
                    context['result'] = declaration
                    context['text_output'] = generate_declaration_text(declaration, declaration.validation_hash, current_lang)
                    context['json_output'] = generate_declaration_json(declaration, declaration.validation_hash, current_lang)
                else:
                    context['not_found'] = True
            except Exception as e:
                context['not_found'] = True

    return render(request, 'core/search.html', context)


@require_http_methods(["GET"])
def view_declaration(request, declaration_id):
    """Ver una declaración específica por su ID"""
    current_lang = get_language()

    try:
        declaration = Declaration.objects.get(declaration_id=declaration_id)

        text_output = generate_declaration_text(declaration, declaration.validation_hash, current_lang)
        json_output = generate_declaration_json(declaration, declaration.validation_hash, current_lang)

        context = {
            'declaration': declaration,
            'text_output': text_output,
            'json_output': json_output,
            'hash': declaration.validation_hash,
            'glossary': get_translated_glossary(current_lang),
        }
        return render(request, 'core/view_declaration.html', context)
    except Declaration.DoesNotExist:
        return render(request, 'core/not_found.html', {'query': declaration_id})
