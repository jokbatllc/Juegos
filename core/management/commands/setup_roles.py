from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from lexicon.models import Idioma, Categoria, Palabra, ListaPalabras
from puzzles.models import JuegoGenerado, Exportacion


class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **options):
        groups = {}
        for name in ["editor_contenidos", "generador", "visor"]:
            group, _ = Group.objects.get_or_create(name=name)
            groups[name] = group

        # editor_contenidos
        editor = groups["editor_contenidos"]
        models = [Idioma, Categoria, Palabra, ListaPalabras]
        for model in models:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            editor.permissions.add(*perms)

        # generador
        generador = groups["generador"]
        for model in [JuegoGenerado, Exportacion]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            generador.permissions.add(*perms)

        # visor
        visor = groups["visor"]
        for model in [JuegoGenerado, Exportacion]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct, codename__startswith="view")
            visor.permissions.add(*perms)

        for name, group in groups.items():
            self.stdout.write(self.style.SUCCESS(f"Grupo {name}: {group.permissions.count()} permisos"))
