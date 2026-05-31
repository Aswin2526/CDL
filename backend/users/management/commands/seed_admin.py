"""
Create the default ChitraBazar admin account.
Run: python manage.py seed_admin
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from users.models import Role

DEFAULT_ADMIN_EMAIL = "admin@chitrabazar.com"
DEFAULT_ADMIN_PASSWORD = "ChitraAdmin@2024"
DEFAULT_ADMIN_NAME = "ChitraBazar Admin"


class Command(BaseCommand):
    help = "Create or update the default admin user for ChitraBazar"

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.update_or_create(
            email=DEFAULT_ADMIN_EMAIL,
            defaults={
                "full_name": DEFAULT_ADMIN_NAME,
                "role": Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        user.set_password(DEFAULT_ADMIN_PASSWORD)
        user.save()

        verb = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} admin account:"))
        self.stdout.write(f"  Email:    {DEFAULT_ADMIN_EMAIL}")
        self.stdout.write(f"  Password: {DEFAULT_ADMIN_PASSWORD}")
        self.stdout.write("  Login at /login then open Admin Dashboard.")
