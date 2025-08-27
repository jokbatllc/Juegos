#!/usr/bin/env python
import os
import sys

<<<<<<< ours
# 👇 Añade esto aquí, antes de cualquier import de Django
if os.name == "nt":
    os.add_dll_directory(r"C:\msys64\ucrt64\bin")

=======
>>>>>>> theirs
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juegos.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
<<<<<<< ours
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your "
            "PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
=======
        raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?") from exc
>>>>>>> theirs
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
