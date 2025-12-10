#!/usr/bin/env python
"""
Script para gestionar firmantes desde la línea de comandos
Uso: python scripts/manage_signers.py [comando]
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Signer


def list_signers():
    """Lista todos los firmantes"""
    signers = Signer.objects.all()

    if not signers:
        print("No hay firmantes registrados.")
        return

    print(f"\n{'='*80}")
    print(f"FIRMANTES REGISTRADOS ({signers.count()})")
    print(f"{'='*80}\n")

    for i, signer in enumerate(signers, 1):
        print(f"{i}. {signer.full_name}")
        print(f"   Email: {signer.email}")
        print(f"   ORCID: {signer.orcid}")
        print(f"   Afiliación: {signer.affiliation}")
        print(f"   Disciplina: {signer.discipline}")
        print(f"   Hash: {signer.hash_short}")
        print(f"   ID: {signer.signer_id}")
        print(f"   Fecha: {signer.created_at.strftime('%d/%m/%Y %H:%M')}")
        print(f"   Público: {'Sí' if signer.public_listing else 'No'}")
        print(f"   ORCID Verificado: {'Sí' if signer.orcid_verified else 'No'}")
        if signer.declaration:
            print(f"   Declaración: {signer.declaration[:60]}...")
        print()


def delete_all():
    """Elimina todos los firmantes"""
    count = Signer.objects.count()

    if count == 0:
        print("No hay firmantes para eliminar.")
        return

    confirm = input(f"¿Estás seguro de eliminar {count} firmante(s)? (sí/no): ")

    if confirm.lower() in ['sí', 'si', 's', 'yes', 'y']:
        deleted = Signer.objects.all().delete()
        print(f"✓ Eliminados {deleted[0]} firmante(s)")
    else:
        print("Operación cancelada.")


def delete_by_email():
    """Elimina firmantes por email"""
    email = input("Ingresa el email del firmante a eliminar: ")

    signers = Signer.objects.filter(email__iexact=email)

    if not signers.exists():
        print(f"No se encontró ningún firmante con el email: {email}")
        return

    signer = signers.first()
    print(f"\nFirmante encontrado:")
    print(f"  Nombre: {signer.full_name}")
    print(f"  Email: {signer.email}")
    print(f"  ORCID: {signer.orcid}")

    confirm = input("\n¿Eliminar este firmante? (sí/no): ")

    if confirm.lower() in ['sí', 'si', 's', 'yes', 'y']:
        signer.delete()
        print("✓ Firmante eliminado")
    else:
        print("Operación cancelada.")


def delete_test_signers():
    """Elimina firmantes de prueba (emails con @test, @example, etc.)"""
    test_emails = Signer.objects.filter(
        email__icontains='@test'
    ) | Signer.objects.filter(
        email__icontains='@example'
    ) | Signer.objects.filter(
        email__icontains='@prueba'
    )

    count = test_emails.count()

    if count == 0:
        print("No se encontraron firmantes de prueba.")
        return

    print(f"Firmantes de prueba encontrados: {count}")
    for signer in test_emails:
        print(f"  - {signer.full_name} ({signer.email})")

    confirm = input(f"\n¿Eliminar estos {count} firmante(s) de prueba? (sí/no): ")

    if confirm.lower() in ['sí', 'si', 's', 'yes', 'y']:
        deleted = test_emails.delete()
        print(f"✓ Eliminados {deleted[0]} firmante(s)")
    else:
        print("Operación cancelada.")


def stats():
    """Muestra estadísticas de firmantes"""
    total = Signer.objects.count()
    verified = Signer.objects.filter(orcid_verified=True).count()
    public = Signer.objects.filter(public_listing=True).count()

    print(f"\n{'='*60}")
    print("ESTADÍSTICAS DE FIRMANTES")
    print(f"{'='*60}")
    print(f"Total de firmantes:           {total}")
    print(f"ORCID verificados:            {verified} ({(verified/total*100) if total > 0 else 0:.1f}%)")
    print(f"Listado público:              {public} ({(public/total*100) if total > 0 else 0:.1f}%)")
    print()

    # Estadísticas por disciplina
    from django.db.models import Count
    disciplines = Signer.objects.values('discipline').annotate(count=Count('discipline')).order_by('-count')

    if disciplines:
        print("Por disciplina:")
        for d in disciplines:
            print(f"  - {d['discipline']}: {d['count']}")

    print()

    # Estadísticas por país
    countries = Signer.objects.exclude(country='').values('country').annotate(count=Count('country')).order_by('-count')

    if countries:
        print("Por país:")
        for c in countries[:10]:  # Top 10
            print(f"  - {c['country']}: {c['count']}")

    print(f"{'='*60}\n")


def export_csv():
    """Exporta firmantes a CSV"""
    import csv
    from datetime import datetime

    signers = Signer.objects.all()

    if not signers:
        print("No hay firmantes para exportar.")
        return

    filename = f"firmantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Nombre', 'Email', 'ORCID', 'Afiliación', 'Disciplina',
            'País', 'Hash', 'Verificado', 'Público', 'Fecha'
        ])

        for signer in signers:
            writer.writerow([
                signer.full_name,
                signer.email,
                signer.orcid,
                signer.affiliation,
                signer.discipline,
                signer.country or '',
                signer.hash_short,
                'Sí' if signer.orcid_verified else 'No',
                'Sí' if signer.public_listing else 'No',
                signer.created_at.strftime('%d/%m/%Y %H:%M')
            ])

    print(f"✓ Exportados {signers.count()} firmante(s) a: {filename}")


def show_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("GESTOR DE FIRMANTES - Declarador.io")
    print("="*60)
    print("\n1. Listar todos los firmantes")
    print("2. Ver estadísticas")
    print("3. Eliminar todos los firmantes")
    print("4. Eliminar firmante por email")
    print("5. Eliminar firmantes de prueba")
    print("6. Exportar a CSV")
    print("0. Salir")
    print()


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'list':
            list_signers()
        elif command == 'stats':
            stats()
        elif command == 'delete-all':
            delete_all()
        elif command == 'delete-test':
            delete_test_signers()
        elif command == 'export':
            export_csv()
        else:
            print(f"Comando desconocido: {command}")
            print("\nComandos disponibles:")
            print("  list         - Listar firmantes")
            print("  stats        - Ver estadísticas")
            print("  delete-all   - Eliminar todos")
            print("  delete-test  - Eliminar de prueba")
            print("  export       - Exportar a CSV")
    else:
        # Modo interactivo
        while True:
            show_menu()
            choice = input("Selecciona una opción: ")

            if choice == '1':
                list_signers()
            elif choice == '2':
                stats()
            elif choice == '3':
                delete_all()
            elif choice == '4':
                delete_by_email()
            elif choice == '5':
                delete_test_signers()
            elif choice == '6':
                export_csv()
            elif choice == '0':
                print("\n¡Hasta luego!")
                break
            else:
                print("\nOpción no válida. Intenta de nuevo.")

            if choice != '0':
                input("\nPresiona Enter para continuar...")


if __name__ == '__main__':
    main()
