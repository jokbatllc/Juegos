#!/usr/bin/env python
import os
import sys

# (Opcional) Soporte DLLs en Windows para WeasyPrint/Cairo.
if os.name == "nt":
    try:
        os.add_dll_directory(r"C:\msys64\ucrt64\bin")
    except Exception:
        pass

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juegos.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Is it installed and on your PYTHONPATH? "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
