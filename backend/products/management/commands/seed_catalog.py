"""
Seed painting categories and artworks for ChitraBazar (single-vendor store).
Run: python manage.py seed_catalog
Clear old catalog: python manage.py seed_catalog --clear
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.catalog_images import attach_images_for_all_products
from products.models import Category, PaintingMedium, Product, StoreSettings


class Command(BaseCommand):
    help = "Seed demo painting categories and artworks for ChitraBazar"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing products and categories before seeding",
        )
        parser.add_argument(
            "--skip-images",
            action="store_true",
            help="Do not download artwork images for products",
        )
        parser.add_argument(
            "--images-only",
            action="store_true",
            help="Only attach images to existing products (skip catalog seed)",
        )

    def handle(self, *args, **options):
        if options["images_only"]:
            self.stdout.write("Attaching images to all products...")
            ok, failed = attach_images_for_all_products(
                stdout=self.stdout,
                style=self.style,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Images attached: {ok} ok, {failed} failed.")
            )
            return

        store = StoreSettings.load()
        store.name = "ChitraBazar"
        store.tagline = "Online painting gallery & store"
        store.address = "Lakeside, Pokhara, Nepal"
        store.phone = "9801111111"
        store.email = "hello@chitrabazar.com"
        store.save()
        self.stdout.write(f"Store: {store.name}")

        if options["clear"]:
            deleted_products, _ = Product.objects.all().delete()
            deleted_categories, _ = Category.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Cleared {deleted_products} products and {deleted_categories} categories."
                )
            )

        categories_data = [
            ("Landscape", "Mountains, valleys, and open skies"),
            ("Portrait", "Figurative and character studies"),
            ("Abstract", "Modern and expressive compositions"),
            ("Still Life", "Objects, florals, and interiors"),
            ("Contemporary", "Bold current-era original works"),
            (
                "Color Paintings",
                "Original full-color works in oil, acrylic, and watercolor",
            ),
            (
                "Pencil Paintings",
                "Detailed graphite, charcoal, and pencil drawings on paper",
            ),
        ]
        categories = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name, "description": desc},
            )
            categories[name] = cat
            self.stdout.write(f"Category: {cat.name}")

        paintings_data = [
            (
                "Annapurna Dawn — Original Oil",
                "Landscape",
                "28500.00",
                1,
                True,
                4.9,
                18,
                "Maya Thapa",
                PaintingMedium.OIL,
                "30 × 40 in",
                True,
                2024,
            ),
            (
                "Phewa Lake Reflections",
                "Landscape",
                "19500.00",
                1,
                True,
                4.7,
                12,
                "Maya Thapa",
                PaintingMedium.WATERCOLOR,
                "22 × 30 in",
                False,
                2023,
            ),
            (
                "Monsoon Over the Valley",
                "Landscape",
                "22000.00",
                1,
                False,
                4.5,
                8,
                "Rajan Gurung",
                PaintingMedium.ACRYLIC,
                "24 × 36 in",
                True,
                2022,
            ),
            (
                "Portrait of a Weaver",
                "Portrait",
                "35000.00",
                1,
                True,
                4.8,
                15,
                "Sunita Rai",
                PaintingMedium.OIL,
                "28 × 36 in",
                True,
                2024,
            ),
            (
                "Street Musician — Charcoal Study",
                "Portrait",
                "12500.00",
                1,
                False,
                4.3,
                6,
                "Sunita Rai",
                PaintingMedium.OTHER,
                "18 × 24 in",
                False,
                2021,
            ),
            (
                "Crimson Geometry No. 7",
                "Abstract",
                "42000.00",
                1,
                True,
                4.9,
                22,
                "Anil Karki",
                PaintingMedium.ACRYLIC,
                "40 × 48 in",
                False,
                2024,
            ),
            (
                "Echoes in Indigo",
                "Abstract",
                "31000.00",
                1,
                False,
                4.6,
                9,
                "Anil Karki",
                PaintingMedium.MIXED,
                "30 × 40 in",
                True,
                2023,
            ),
            (
                "Copper Vessels & Marigolds",
                "Still Life",
                "16800.00",
                1,
                False,
                4.4,
                7,
                "Maya Thapa",
                PaintingMedium.OIL,
                "20 × 24 in",
                True,
                2022,
            ),
            (
                "Morning Tea Table",
                "Still Life",
                "14200.00",
                1,
                False,
                4.2,
                5,
                "Maya Thapa",
                PaintingMedium.WATERCOLOR,
                "16 × 20 in",
                False,
                2021,
            ),
            (
                "Urban Pulse — Limited Print",
                "Contemporary",
                "8900.00",
                3,
                False,
                4.1,
                4,
                "Rajan Gurung",
                PaintingMedium.DIGITAL,
                "12 × 18 in",
                False,
                2024,
            ),
            (
                "Neon Alley Dreams",
                "Contemporary",
                "27500.00",
                1,
                True,
                4.7,
                11,
                "Anil Karki",
                PaintingMedium.ACRYLIC,
                "36 × 48 in",
                False,
                2023,
            ),
            (
                "Silent Peaks at Dusk",
                "Landscape",
                "33200.00",
                1,
                True,
                5.0,
                25,
                "Maya Thapa",
                PaintingMedium.OIL,
                "36 × 48 in",
                True,
                2024,
            ),
            # —— Color Paintings ——
            (
                "Rhododendron Valley — Full Color",
                "Color Paintings",
                "24800.00",
                1,
                True,
                4.8,
                14,
                "Maya Thapa",
                PaintingMedium.WATERCOLOR,
                "22 × 30 in",
                True,
                2024,
            ),
            (
                "Festival of Lights — Acrylic",
                "Color Paintings",
                "31500.00",
                1,
                True,
                4.7,
                11,
                "Anil Karki",
                PaintingMedium.ACRYLIC,
                "30 × 40 in",
                False,
                2023,
            ),
            (
                "Lakeside Sunset in Color",
                "Color Paintings",
                "36200.00",
                1,
                True,
                4.9,
                19,
                "Maya Thapa",
                PaintingMedium.OIL,
                "36 × 48 in",
                True,
                2024,
            ),
            (
                "Terai Golden Fields",
                "Color Paintings",
                "18900.00",
                1,
                False,
                4.5,
                8,
                "Rajan Gurung",
                PaintingMedium.ACRYLIC,
                "24 × 32 in",
                True,
                2022,
            ),
            (
                "Monsoon Rainbow Over Pokhara",
                "Color Paintings",
                "27400.00",
                1,
                False,
                4.6,
                10,
                "Maya Thapa",
                PaintingMedium.WATERCOLOR,
                "20 × 28 in",
                False,
                2023,
            ),
            (
                "Village Courtyard — Oil on Canvas",
                "Color Paintings",
                "29800.00",
                1,
                False,
                4.4,
                7,
                "Sunita Rai",
                PaintingMedium.OIL,
                "28 × 36 in",
                True,
                2021,
            ),
            # —— Pencil Paintings ——
            (
                "Old Man of Pokhara — Graphite Portrait",
                "Pencil Paintings",
                "14500.00",
                1,
                True,
                4.8,
                16,
                "Sunita Rai",
                PaintingMedium.PENCIL,
                "16 × 20 in",
                True,
                2024,
            ),
            (
                "Temple Courtyard — Pencil Study",
                "Pencil Paintings",
                "11800.00",
                1,
                True,
                4.7,
                12,
                "Sunita Rai",
                PaintingMedium.PENCIL,
                "14 × 18 in",
                False,
                2023,
            ),
            (
                "Himalayan Macaque — Pencil Sketch",
                "Pencil Paintings",
                "9800.00",
                1,
                False,
                4.5,
                9,
                "Rajan Gurung",
                PaintingMedium.PENCIL,
                "12 × 16 in",
                False,
                2022,
            ),
            (
                "Mustang Alley — Charcoal & Pencil",
                "Pencil Paintings",
                "16200.00",
                1,
                False,
                4.6,
                11,
                "Anil Karki",
                PaintingMedium.PENCIL,
                "18 × 24 in",
                True,
                2023,
            ),
            (
                "Florals in Graphite",
                "Pencil Paintings",
                "11200.00",
                1,
                False,
                4.4,
                6,
                "Maya Thapa",
                PaintingMedium.PENCIL,
                "11 × 14 in",
                False,
                2021,
            ),
            (
                "Annapurna Ridge — Tonal Pencil",
                "Pencil Paintings",
                "17500.00",
                1,
                True,
                4.9,
                20,
                "Rajan Gurung",
                PaintingMedium.PENCIL,
                "20 × 26 in",
                True,
                2024,
            ),
        ]

        for row in paintings_data:
            (
                name,
                cat_name,
                price,
                stock,
                featured,
                rating,
                reviews,
                artist,
                medium,
                dimensions,
                framed,
                year,
            ) = row
            product, created = Product.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "category": categories[cat_name],
                    "name": name,
                    "artist_name": artist,
                    "medium": medium,
                    "dimensions": dimensions,
                    "is_framed": framed,
                    "year_created": year,
                    "description": (
                        f"{name} by {artist}. Original {medium} artwork, "
                        f"{dimensions}. Sold exclusively by {store.name}. "
                        "Certificate of authenticity included. Insured shipping worldwide."
                    ),
                    "price": Decimal(price),
                    "stock": stock,
                    "is_featured": featured,
                    "is_active": True,
                    "average_rating": Decimal(str(rating)),
                    "review_count": reviews,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  + {product.name}"))
            else:
                self.stdout.write(f"  ~ {product.name} (updated)")

        if not options["skip_images"]:
            self.stdout.write("Downloading artwork images for all products...")
            ok, failed = attach_images_for_all_products(
                stdout=self.stdout,
                style=self.style,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Images: {ok} attached, {failed} failed.")
            )

        self.stdout.write(self.style.SUCCESS("ChitraBazar catalog seed complete."))
