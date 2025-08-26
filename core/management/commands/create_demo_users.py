from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

USERS = [
    ("admin", "admin", {"is_staff": True, "is_superuser": True, "groups": []}),
    ("editor", "editor123", {"groups": ["editor_contenidos"]}),
    ("maker", "maker123", {"groups": ["generador"]}),
    ("viewer", "viewer123", {"groups": ["visor"]}),
]


class Command(BaseCommand):
    help = "Create demo users for development"

    def handle(self, *args, **options):
        User = get_user_model()
        for username, password, extra in USERS:
            user, created = User.objects.get_or_create(username=username, defaults=extra)
            if created:
                user.set_password(password)
            for gname in extra.get("groups", []):
                group = Group.objects.get(name=gname)
                user.groups.add(group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User {username}/{password}"))
