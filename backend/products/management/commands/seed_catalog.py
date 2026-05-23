"""
Seed painting categories and artworks for ChitraBazar (single-vendor store).
Run:  python manage.py seed_catalog
Clear: python manage.py seed_catalog --clear
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.catalog_images import (
    RETIRED_LANDSCAPE_SLUGS,
    RETIRED_PORTRAIT_SLUGS,
    attach_images_for_all_products,
)
from products.models import Category, PaintingMedium, Product, StoreSettings


class Command(BaseCommand):
    help = "Seed painting categories and artworks for ChitraBazar"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true",
                            help="Delete all products and categories first")
        parser.add_argument("--skip-images", action="store_true",
                            help="Do not download images after seeding")
        parser.add_argument("--images-only", action="store_true",
                            help="Only attach images (skip catalog seed)")

    def handle(self, *args, **options):
        if options["images_only"]:
            self.stdout.write("Attaching images to all products...")
            ok, failed = attach_images_for_all_products(self.stdout, self.style)
            self.stdout.write(self.style.SUCCESS(f"Images: {ok} ok, {failed} failed."))
            return

        # ── Store ────────────────────────────────────────────────────
        store = StoreSettings.load()
        store.name = "ChitraBazar"
        store.tagline = "Original hand-drawn paintings for sale"
        store.address = "Lakeside, Pokhara, Nepal"
        store.phone = "9801111111"
        store.email = "hello@chitrabazar.com"
        store.save()
        self.stdout.write(f"Store: {store.name}")

        if options["clear"]:
            dp, _ = Product.objects.all().delete()
            dc, _ = Category.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {dp} products, {dc} categories."))

        # ── Categories ───────────────────────────────────────────────
        cats_data = [
            ("Landscape",       "Mountains, valleys and open skies"),
            ("Portrait",        "Figurative and character studies"),
            ("Abstract",        "Modern and expressive compositions"),
            ("Still Life",      "Flowers, objects and interiors"),
            ("Contemporary",    "Bold current-era original works"),
            ("Color Paintings", "Original full-color oil, acrylic and watercolor works"),
            ("Pencil Paintings","Graphite, charcoal and pencil drawings"),
            (
                "Original Drawings",
                "One-of-a-kind hand-drawn originals — pencil, charcoal and ink. "
                "Each piece is a single original artwork ready to ship.",
            ),
        ]
        cats = {}
        for name, desc in cats_data:
            cat, _ = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name, "description": desc},
            )
            cats[name] = cat
            self.stdout.write(f"  cat: {cat.name}")

        # ── Paintings ────────────────────────────────────────────────
        # columns: name, category, price (Rs.), stock, featured,
        #          rating, review_count, artist, medium, dimensions, framed, year
        O = PaintingMedium.OIL
        AC = PaintingMedium.ACRYLIC
        WC = PaintingMedium.WATERCOLOR
        MX = PaintingMedium.MIXED
        PC = PaintingMedium.PENCIL

        paintings = [
            # ── Portrait ──────────────────────────────────────────────
            (
                "Antarman ko Jhalak",
                "Portrait", "18500.00", 1, True, 4.8, 19,
                "Roshan Pradhan", O, "20 × 24 in", True, 2024,
                "A soulful oil portrait — quiet reflection in soft light, "
                "delicate lace and a wistful gaze against a deep moody ground.",
            ),
            (
                "Suryodaya Sundari",
                "Portrait", "35000.00", 1, True, 4.9, 24,
                "Binod Shrestha", O, "24 × 30 in", True, 2024,
                "Bold contemporary portrait — radiant afro, peacock feathers "
                "and warm sunset light on confident, serene features.",
            ),
            (
                "Seto Lace ko Keti",
                "Portrait", "32000.00", 1, True, 4.8, 17,
                "Asha Dangol", O, "22 × 28 in", True, 2023,
                "Classical portrait of a young woman in an intricate white lace "
                "gown — fine detail and timeless elegance on a dark ground.",
            ),
            (
                "Nischal Herai",
                "Portrait", "16500.00", 1, False, 4.7, 12,
                "Suman Shrestha", O, "18 × 22 in", False, 2023,
                "Contemplative seated portrait — navy shawl over a vivid orange "
                "dress, crossed arms and a direct, soulful gaze.",
            ),
            (
                "Ujyalo Muskan",
                "Portrait", "22000.00", 1, False, 4.8, 15,
                "Sagar Thapa", AC, "20 × 26 in", False, 2024,
                "Luminous contemporary portrait — sun-kissed skin, flowing hair "
                "and sparkling light in a soft, natural setting.",
            ),

            # ── Original hand-drawn paintings for sale (local reference art) ──
            (
                "Nilo Nayan — Phoolbhitra",
                "Original Drawings", "36000.00", 1, True, 4.9, 5,
                "Sunita Rai", PC, "24 × 30 in", True, 2024,
                "ORIGINAL FOR SALE — Hand-drawn color portrait with blue eyes and "
                "white blossoms. Single piece on archival paper; certificate included.",
            ),
            (
                "Gaun Ko Ghar Bagaicha",
                "Original Drawings", "28000.00", 1, True, 4.8, 4,
                "Maya Thapa", AC, "24 × 30 in", True, 2024,
                "ORIGINAL FOR SALE — Acrylic landscape of a countryside home and "
                "meadow. Painted by hand; only one copy exists.",
            ),
            (
                "Charcoal Gaun Ko Bato",
                "Original Drawings", "15000.00", 1, True, 4.7, 3,
                "Rajan Gurung", PC, "18 × 24 in", False, 2024,
                "ORIGINAL FOR SALE — Charcoal drawing of a misty village path. "
                "Signed original; ships rolled or flat-packed.",
            ),
            (
                "Kala Safed Fashion Portrait",
                "Original Drawings", "32000.00", 1, True, 4.8, 3,
                "Sunita Rai", MX, "20 × 24 in", False, 2024,
                "ORIGINAL FOR SALE — Ink and wash fashion portrait with bold pink "
                "lips. Hand-painted original, not a print.",
            ),
            (
                "Hathle Baneko Gurans",
                "Original Drawings", "14500.00", 1, True, 4.8, 6,
                "Anil Karki", PC, "14 × 18 in", False, 2024,
                "ORIGINAL FOR SALE — Pencil study of rhododendron branches drawn "
                "from life in Ghorepani. One piece only.",
            ),
            (
                "Kathmandu Durbar Charcoal",
                "Original Drawings", "18500.00", 1, False, 4.7, 4,
                "Rajan Gurung", PC, "16 × 20 in", True, 2023,
                "ORIGINAL FOR SALE — Charcoal sketch of temple woodwork and "
                "courtyard shadows at Kathmandu Durbar Square.",
            ),
            (
                "Pokhara Lake Graphite Original",
                "Original Drawings", "16800.00", 1, False, 4.6, 5,
                "Maya Thapa", PC, "18 × 24 in", False, 2024,
                "ORIGINAL FOR SALE — Graphite lakeside drawing with Annapurna "
                "reflections. Hand-finished tonal work.",
            ),
            (
                "Baal Sain Charcoal Portrait",
                "Original Drawings", "22000.00", 1, True, 4.9, 7,
                "Sunita Rai", PC, "18 × 22 in", True, 2024,
                "ORIGINAL FOR SALE — Charcoal child portrait with soft highlights. "
                "Drawn from a live sitting in Pokhara.",
            ),
            (
                "Dhaka Topi Wala Sketch",
                "Original Drawings", "12500.00", 1, False, 4.5, 3,
                "Anil Karki", PC, "12 × 16 in", False, 2023,
                "ORIGINAL FOR SALE — Quick pencil sketch of an elder in traditional "
                "dhaka topi. Authentic hill-culture study.",
            ),
            (
                "Prayer Flag Ridge Drawing",
                "Original Drawings", "19500.00", 1, False, 4.7, 4,
                "Rajan Gurung", PC, "20 × 26 in", True, 2023,
                "ORIGINAL FOR SALE — Pencil and charcoal ridge line with fluttering "
                "prayer flags. Original Himalayan scene.",
            ),
            (
                "Sadak Ko Kukur — Pencil",
                "Original Drawings", "9800.00", 1, False, 4.4, 2,
                "Maya Thapa", PC, "11 × 14 in", False, 2022,
                "ORIGINAL FOR SALE — Street dog resting on a Kathmandu lane, drawn "
                "in graphite. Affordable original art.",
            ),
            (
                "Monsoon Khola Charcoal",
                "Original Drawings", "17200.00", 1, False, 4.6, 5,
                "Anil Karki", PC, "18 × 24 in", False, 2024,
                "ORIGINAL FOR SALE — Charcoal stream scene after monsoon rain. "
                "Textured paper, signed by artist.",
            ),

            # ── Landscape ─────────────────────────────────────────────
            (
                "Shishir Himal ra Pul",
                "Landscape", "28500.00", 1, True, 4.9, 22,
                "Dipak Rana", O, "24 × 36 in", True, 2024,
                "Snow peak above an autumn forest — golden larch and birch "
                "frame a stone bridge over a calm mountain river.",
            ),
            (
                "Himshanti Taal",
                "Landscape", "18500.00", 1, True, 4.8, 18,
                "Ramesh Shrestha", O, "30 × 40 in", True, 2024,
                "A stag on a rocky shore at dawn — still alpine lake and "
                "snow-capped peak reflected in cool morning light.",
            ),
            (
                "Sakura Sanjhama Himal",
                "Landscape", "12500.00", 1, False, 4.7, 14,
                "Arpan Rajbhandari", AC, "20 × 28 in", False, 2023,
                "Cherry blossoms along a lakeside at sunset — distant Himalayan "
                "silhouette and arched bridge mirrored in warm pink water.",
            ),
            (
                "Neelo Ghar ko Bato",
                "Landscape", "9800.00", 1, False, 4.6, 9,
                "Arjun Prajapati", AC, "18 × 24 in", False, 2022,
                "A blue cottage on rolling hills — folk-art colour and a winding "
                "path through terracotta rocks under a soft evening sky.",
            ),
            (
                "Suryodayako Bato",
                "Landscape", "15200.00", 1, False, 4.7, 11,
                "Saraswati Khatri", O, "24 × 30 in", True, 2024,
                "A winding village path at sunrise — bold brushwork, cypress "
                "trees and a cream cottage beneath a swirling golden sky.",
            ),
            (
                "Pataley Chhango",
                "Landscape", "35000.00", 1, True, 5.0, 26,
                "Bishnu Prasad Lamichhane", O, "36 × 48 in", True, 2023,
                "A tiered waterfall in a green valley — classical landscape "
                "with grazing cattle and distant hills in soft morning air.",
            ),

            # ── Abstract ──────────────────────────────────────────────
            (
                "Rangeen Sapana",
                "Abstract", "35000.00", 1, True, 4.8, 18,
                "Anil Karki", AC, "30 × 40 in", False, 2024,
                "Swirling arcs of colour inspired by festival lights of Tihar — "
                "joy and energy rendered in bold Kandinsky-esque form.",
            ),
            (
                "Naya Bihani Rang",
                "Abstract", "27500.00", 1, False, 4.6, 11,
                "Anil Karki", AC, "24 × 30 in", False, 2023,
                "Floral abstraction in warm ember tones — petals dissolving into "
                "pure colour, celebrating the new dawn of spring.",
            ),
            (
                "Rang Ko Khel",
                "Abstract", "31000.00", 1, False, 4.7, 13,
                "Maya Thapa", MX, "28 × 36 in", True, 2023,
                "Dynamic waves and spirals collide in deep indigo and gold — "
                "a visual poem inspired by Himalayan river currents.",
            ),

            # ── Still Life ────────────────────────────────────────────
            (
                "Phool Ko Ful",
                "Still Life", "18500.00", 1, False, 4.4, 8,
                "Sunita Rai", O, "16 × 20 in", True, 2022,
                "Sunflowers in a clay pot against warm ochre — "
                "vibrant and joyful, echoing Nepali harvest festivals.",
            ),
            (
                "Bagaincha Ko Mewa",
                "Still Life", "21000.00", 1, False, 4.3, 6,
                "Maya Thapa", WC, "18 × 24 in", False, 2021,
                "Ripe mangoes and pomegranates spilling from a hand-woven dhaka "
                "cloth — celebrating Nepal's seasonal abundance.",
            ),

            # ── Color Paintings ───────────────────────────────────────
            (
                "Lali Gurans Phuleko",
                "Color Paintings", "29000.00", 1, True, 4.9, 20,
                "Maya Thapa", WC, "22 × 28 in", True, 2024,
                "Vibrant rhododendron blooms cascading down a Himalayan hillside "
                "— Nepal's national flower in full color glory.",
            ),
            (
                "Indra Jatra Utsav",
                "Color Paintings", "36500.00", 1, True, 4.8, 17,
                "Anil Karki", AC, "30 × 40 in", False, 2023,
                "The living goddess Kumari chariot procession through Kathmandu "
                "Durbar Square — luminous crowds and marigold garlands.",
            ),
            (
                "Seto Machindranath Rath",
                "Color Paintings", "31000.00", 1, False, 4.6, 10,
                "Sunita Rai", O, "24 × 32 in", True, 2023,
                "The towering white chariot of Seto Machindranath rising above "
                "Kathmandu streets — bold color and devotional energy.",
            ),
            (
                "Taal Ko Rang",
                "Color Paintings", "24000.00", 1, False, 4.5, 8,
                "Rajan Gurung", AC, "20 × 26 in", False, 2022,
                "Abstract reflections in a mountain lake at sunset — "
                "fiery orange and violet rippling across still water.",
            ),
            (
                "Holi Ko Khushi",
                "Color Paintings", "27800.00", 1, False, 4.7, 12,
                "Maya Thapa", WC, "22 × 30 in", False, 2024,
                "Joyful splashes of festival color — Holi celebration in "
                "a Pokhara street, children laughing through clouds of gulal.",
            ),
            (
                "Parijat Phul",
                "Color Paintings", "19800.00", 1, False, 4.4, 7,
                "Sunita Rai", O, "16 × 20 in", True, 2021,
                "Night-blooming parijat flowers in soft candlelight — "
                "a delicate oil study of Nepal's beloved coral jasmine.",
            ),

            # ── Pencil Paintings ──────────────────────────────────────
            (
                "Charcoal Gaaun Saanjh",
                "Pencil Paintings", "13500.00", 1, True, 4.9, 22,
                "Rajan Gurung", PC, "16 × 20 in", True, 2024,
                "A Nepali village at dusk rendered in rich charcoal tones — "
                "thatched roofs, winding lanes and fading evening light.",
            ),
            (
                "Pencil Ko Pahaad",
                "Pencil Paintings", "11200.00", 1, True, 4.8, 14,
                "Anil Karki", PC, "14 × 18 in", False, 2023,
                "A precise graphite study of the Annapurna range from Sarangkot "
                "— every ridge and shadow captured with meticulous detail.",
            ),
            (
                "Graphite Portrait Budha",
                "Pencil Paintings", "16500.00", 1, False, 4.7, 11,
                "Sunita Rai", PC, "18 × 22 in", True, 2024,
                "A deeply expressive graphite portrait of a Nepali elder — "
                "weathered lines of a life well-lived in the hills.",
            ),
            (
                "Raat Ko Bato — Charcoal",
                "Pencil Paintings", "14000.00", 1, False, 4.6, 9,
                "Rajan Gurung", PC, "16 × 20 in", False, 2022,
                "A nocturnal charcoal scene — Kathmandu alley under a single "
                "street lamp, misty and atmospheric.",
            ),
            (
                "Aankhako Bhaav — Sketch",
                "Pencil Paintings", "12800.00", 1, False, 4.5, 8,
                "Sunita Rai", PC, "12 × 16 in", False, 2023,
                "Intimate pencil sketch of expressive eyes — raw emotion "
                "captured in minimal graphite strokes.",
            ),
            (
                "Mustang Dharahara — Pencil",
                "Pencil Paintings", "15500.00", 1, False, 4.6, 10,
                "Anil Karki", PC, "18 × 24 in", True, 2023,
                "The ancient walled city of Mustang Lo Manthang in tonal "
                "pencil — crumbling ochre walls and fluttering prayer flags.",
            ),
            (
                "Aakash Pencil Sketch",
                "Pencil Paintings", "10500.00", 1, False, 4.4, 6,
                "Maya Thapa", PC, "11 × 14 in", False, 2021,
                "A delicate sky study in pencil — layered cloud formations "
                "above the Kathmandu valley at first light.",
            ),
            (
                "Ghaam Pani — Charcoal",
                "Pencil Paintings", "17000.00", 1, True, 4.8, 16,
                "Rajan Gurung", PC, "20 × 26 in", True, 2024,
                "Monsoon rain and afternoon sun in dramatic charcoal contrast — "
                "the bittersweet play of Nepali weather on a mountain road.",
            ),
        ]

        for row in paintings:
            (name, cat_name, price, stock, featured,
             rating, reviews, artist, medium,
             dimensions, framed, year, description) = row

            product, created = Product.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "category": cats[cat_name],
                    "name": name,
                    "artist_name": artist,
                    "medium": medium,
                    "dimensions": dimensions,
                    "is_framed": framed,
                    "year_created": year,
                    "description": description,
                    "price": Decimal(price),
                    "stock": stock,
                    "is_featured": featured,
                    "is_active": True,
                    "average_rating": Decimal(str(rating)),
                    "review_count": reviews,
                },
            )
            status = "+" if created else "~"
            self.stdout.write(f"  {status} {product.name}")

        removed, _ = Product.objects.filter(
            slug__in=(*RETIRED_LANDSCAPE_SLUGS, *RETIRED_PORTRAIT_SLUGS)
        ).delete()
        if removed:
            self.stdout.write(self.style.WARNING(f"  - removed {removed} retired listing(s)"))

        if not options.get("skip_images"):
            self.stdout.write("Downloading painting images...")
            ok, failed = attach_images_for_all_products(self.stdout, self.style)
            self.stdout.write(self.style.SUCCESS(f"Images: {ok} ok, {failed} failed."))

        self.stdout.write(self.style.SUCCESS("ChitraBazar catalog seed complete."))
