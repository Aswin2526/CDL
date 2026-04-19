"""Attach artwork images to every product. Run: python manage.py attach_product_images"""

from django.core.management.base import BaseCommand

from products.catalog_images import attach_images_for_all_products


class Command(BaseCommand):
    help = "Download and attach primary images for all catalog products"

    def handle(self, *args, **options):
        self.stdout.write("Attaching images to all products...")
        ok, failed = attach_images_for_all_products(
            stdout=self.stdout,
            style=self.style,
        )
        self.stdout.write(self.style.SUCCESS(f"Done: {ok} ok, {failed} failed."))
