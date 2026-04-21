"""
Seed painting categories and artworks for ChitraBazar (single-vendor store).
Run:  python manage.py seed_catalog
Clear: python manage.py seed_catalog --clear
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.catalog_images import attach_images_for_all_products
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
        store.tagline = "Online painting gallery & store"
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
                "Neta Ko Nayan — Blue Eye Portrait",
                "Portrait", "38000.00", 1, True, 4.9, 21,
                "Sunita Rai", O, "24 × 30 in", True, 2024,
                "A stunning oil portrait capturing piercing blue eyes framed by "
                "white daisies — inspired by the delicate beauty of Nepali hill women.",
            ),
            (
                "Bhadragol Sundar Akhi",
                "Portrait", "29500.00", 1, True, 4.8, 16,
                "Sunita Rai", O, "20 × 24 in", True, 2023,
                "Soft golden light falls on a young woman's gaze, evoking the "
                "timeless grace found in classical Newari portraiture.",
            ),
            (
                "Rato Oth Ko Roop",
                "Portrait", "34000.00", 1, False, 4.7, 12,
                "Maya Thapa", O, "24 × 24 in", False, 2023,
                "Bold contrast of a monochrome figure against stark white — "
                "a contemporary take on Nepali feminine elegance with crimson lips.",
            ),
            (
                "Pahadi Naari Portrait",
                "Portrait", "27000.00", 1, False, 4.6, 9,
                "Sunita Rai", WC, "18 × 22 in", False, 2022,
                "Delicate watercolor capturing a hill woman reading a letter "
                "by the window — quiet solitude in soft morning light.",
            ),
            (
                "Buwa Ko Muhar",
                "Portrait", "22500.00", 1, False, 4.5, 7,
                "Rajan Gurung", O, "16 × 20 in", True, 2021,
                "A moving self-portrait study in oil — textured brushwork "
                "reflecting the depth and dignity of an elder Nepali face.",
            ),

            # ── User reference portraits & scenes (local images) ───────
            (
                "Nilo Nayan — Phoolbhitra",
                "Portrait", "36000.00", 1, True, 4.9, 5,
                "Studio Artist", O, "24 × 30 in", True, 2024,
                "Hyper‑realistic blue eyes emerging from a ring of white flowers — "
                "inspired directly by the buyer’s custom reference painting.",
            ),
            (
                "Gaun Ko Ghar Bagaicha",
                "Landscape", "28000.00", 1, True, 4.8, 4,
                "Studio Artist", AC, "24 × 30 in", True, 2024,
                "Peaceful countryside house with bright green fields and wild "
                "daisies — perfect for living‑room wall decor.",
            ),
            (
                "Charcoal Gaun Ko Bato",
                "Pencil Paintings", "15000.00", 1, True, 4.7, 3,
                "Studio Artist", PC, "18 × 24 in", False, 2024,
                "Moody black‑and‑white charcoal landscape of a distant village "
                "road, echoing foggy winter evenings in the hills.",
            ),
            (
                "Kala Safed Fashion Portrait",
                "Portrait", "32000.00", 1, True, 4.8, 3,
                "Studio Artist", MX, "20 × 24 in", False, 2024,
                "Minimal black‑and‑white fashion illustration with bold red lips "
                "and sleek gloves — for modern apartment spaces.",
            ),

            # ── Landscape ─────────────────────────────────────────────
            (
                "Phewa Tal Bihani",
                "Landscape", "32000.00", 1, True, 4.9, 24,
                "Maya Thapa", O, "30 × 40 in", True, 2024,
                "Golden dawn light on Phewa Lake, Pokhara — misty reflections "
                "of the Annapurna range in still water.",
            ),
            (
                "Gaaun Ko Bato",
                "Landscape", "26500.00", 1, True, 4.7, 15,
                "Maya Thapa", AC, "24 × 36 in", False, 2023,
                "A winding dirt path through a Nepali village in full monsoon "
                "green — warm dusk light over thatched rooftops.",
            ),
            (
                "Himal Ko Bhor",
                "Landscape", "42000.00", 1, True, 5.0, 30,
                "Rajan Gurung", O, "36 × 48 in", True, 2024,
                "Sweeping Himalayan panorama at dawn — cobalt sky fading to "
                "rose gold above snow-capped Annapurna peaks.",
            ),
            (
                "Fulbari Sanjha",
                "Landscape", "19500.00", 1, False, 4.5, 8,
                "Maya Thapa", WC, "18 × 24 in", False, 2022,
                "A lush garden at twilight with blooming rhododendrons reflected "
                "in a still pond — impressionistic and serene.",
            ),
            (
                "Terai Khet Hari",
                "Landscape", "23000.00", 1, False, 4.6, 10,
                "Anil Karki", O, "24 × 32 in", True, 2022,
                "Vast golden paddy fields of the Terai plains under dramatic "
                "monsoon clouds — a celebration of Nepal's breadbasket.",
            ),
            (
                "Koshi Nadiko Kinara",
                "Landscape", "28000.00", 1, False, 4.4, 7,
                "Rajan Gurung", AC, "22 × 30 in", False, 2021,
                "Shimmering light on the Koshi River — fishermen on bamboo rafts "
                "against a backdrop of forest and distant hills.",
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

        if not options.get("skip_images"):
            self.stdout.write("Downloading painting images...")
            ok, failed = attach_images_for_all_products(self.stdout, self.style)
            self.stdout.write(self.style.SUCCESS(f"Images: {ok} ok, {failed} failed."))

        self.stdout.write(self.style.SUCCESS("ChitraBazar catalog seed complete."))
