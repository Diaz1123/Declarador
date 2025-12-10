#!/usr/bin/env python3
"""
Simple PO to MO compiler using polib
"""
import os
import sys

try:
    import polib
except ImportError:
    print("Installing polib...")
    os.system("pip install polib")
    import polib

def compile_po_file(po_path):
    """Compile a .po file to .mo"""
    mo_path = po_path.replace('.po', '.mo')
    print(f"Compiling {po_path} to {mo_path}")
    
    try:
        po = polib.pofile(po_path)
        po.save_as_mofile(mo_path)
        print(f"✓ Successfully compiled {mo_path}")
        return True
    except Exception as e:
        print(f"✗ Error compiling {po_path}: {e}")
        return False

def main():
    """Compile all .po files in locale directories"""
    locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
    
    if not os.path.exists(locale_dir):
        print(f"Error: locale directory not found: {locale_dir}")
        sys.exit(1)
    
    success_count = 0
    error_count = 0
    
    # Find all .po files
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.po'):
                po_path = os.path.join(root, file)
                if compile_po_file(po_path):
                    success_count += 1
                else:
                    error_count += 1
    
    print(f"\nCompilation complete: {success_count} successful, {error_count} errors")
    return 0 if error_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
