"""
Seed painting categories and artworks for ChitraBazar (single-vendor store).
Run:  python manage.py seed_catalog
Clear: python manage.py seed_catalog --clear
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.catalog_images import (
    RETIRED_ABSTRACT_SLUGS,
    RETIRED_COLOR_PAINTINGS_SLUGS,
    RETIRED_PENCIL_PAINTINGS_SLUGS,
    RETIRED_CONTEMPORARY_SLUGS,
    RETIRED_LANDSCAPE_SLUGS,
    RETIRED_PORTRAIT_SLUGS,
    RETIRED_STILL_LIFE_SLUGS,
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
                "Barkha ko Rang",
                "Abstract", "15500.00", 1, True, 4.8, 20,
                "Suman Thapa", O, "24 × 30 in", True, 2024,
                "Colourful umbrellas in the rain — thick impasto strokes and "
                "reflections on a wet street in bold red, green and gold.",
            ),
            (
                "Antardwanda",
                "Abstract", "18500.00", 1, True, 4.9, 16,
                "Kiran Chitrakar", O, "20 × 24 in", False, 2023,
                "Raw expressionist portrait — fractured features in black, white "
                "and crimson, conveying inner turmoil and psychological depth.",
            ),
            (
                "Kala Chakra",
                "Abstract", "9200.00", 1, False, 4.6, 10,
                "Siddhartha Tuladhar", AC, "22 × 28 in", True, 2024,
                "Geometric abstraction — interlocking circles, squares and triangles "
                "in primary red, yellow, blue and teal on a rhythmic grid.",
            ),
            (
                "Indreni Aankha",
                "Abstract", "18500.00", 1, False, 4.8, 14,
                "Samipya Rajbhandari", AC, "30 × 40 in", False, 2024,
                "A luminous rainbow iris — explosive colour, heavy texture and "
                "paint splatter around a single intense, contemporary eye.",
            ),
            (
                "Kiriko Jwalo",
                "Abstract", "28500.00", 1, True, 4.7, 12,
                "Suman Shrestha", O, "28 × 36 in", True, 2023,
                "Misty forest greens parted by a horizontal band of fiery orange "
                "and gold — atmospheric abstract landscape in bold brushwork.",
            ),

            # ── Still Life ────────────────────────────────────────────
            (
                "Pustak ra Suntala",
                "Still Life", "22500.00", 1, True, 4.8, 14,
                "Ramesh Poudel", O, "20 × 24 in", True, 2024,
                "Old books and peeled oranges in dramatic chiaroscuro — "
                "curling peel and worn spines in warm gold against deep shadow.",
            ),
            (
                "Falharu ko Jhund",
                "Still Life", "16800.00", 1, False, 4.6, 9,
                "Prakash Malla", O, "18 × 22 in", False, 2023,
                "Pineapple, ripe bananas and a glossy apple on a dark ground — "
                "classic fruit study with soft side light.",
            ),
            (
                "Jeevan ko Sandesh",
                "Still Life", "38500.00", 1, True, 4.9, 18,
                "Gopal Manandhar", O, "22 × 28 in", True, 2023,
                "Vanitas still life — skull, quill, inkwell and roemer glass "
                "on aged pages, reminding us of life's fleeting nature.",
            ),
            (
                "Phoolharu ko Guchchha",
                "Still Life", "28500.00", 1, True, 4.8, 16,
                "Januka Rizal", O, "24 × 30 in", True, 2024,
                "Lush roses, lilies and tulips overflowing a glass vase — "
                "Dutch-inspired floral abundance on a stone ledge.",
            ),
            (
                "Bhansa Kotha Still Life",
                "Still Life", "14200.00", 1, False, 4.5, 7,
                "Sarita Gurung", O, "16 × 20 in", False, 2022,
                "White enamel pot with red handle, onions and garlic on green "
                "cloth — humble kitchen objects in gentle realism.",
            ),

            # ── Contemporary ────────────────────────────────────────────
            (
                "Bada Khutta ra Surya",
                "Contemporary", "32000.00", 1, True, 4.8, 15,
                "Alok Bhattarai", AC, "28 × 36 in", False, 2024,
                "Bold modernist figure on a green mound — oversized foot, "
                "cactus and yellow sun against a brilliant blue sky.",
            ),
            (
                "Poolside Dui Roop",
                "Contemporary", "45000.00", 1, True, 4.9, 21,
                "Nirmal Bajracharya", AC, "36 × 48 in", True, 2023,
                "Two figures at a turquoise pool — one standing in pink, "
                "one swimming below rolling green hills in flat, vivid colour.",
            ),
            (
                "Sochko Dhara",
                "Contemporary", "24500.00", 1, False, 4.7, 12,
                "Meena Shakya", AC, "24 × 30 in", False, 2024,
                "Pop-art portrait in Ben-Day dots — anxious hands, red lips "
                "and bold outlines on a deep blue comic-book ground.",
            ),
            (
                "Rato Kursi ma Aram",
                "Contemporary", "19800.00", 1, False, 4.6, 10,
                "Puja Rana", AC, "22 × 28 in", False, 2023,
                "Woman reclining in a bright red deck chair — blocky brushwork, "
                "teal background and sunlit leisure in modern colour.",
            ),
            (
                "Jwan ko Chhaya",
                "Contemporary", "17500.00", 1, False, 4.7, 11,
                "Bikash Tamang", O, "20 × 24 in", True, 2024,
                "Contemporary portrait of a weary man in mustard shirt and vest — "
                "downcast gaze and rough brushwork on a textured ground.",
            ),

            # ── Color Paintings ───────────────────────────────────────
            (
                "Rangin Singhako Muhar",
                "Color Paintings", "26500.00", 1, True, 4.9, 23,
                "Manish Koirala", AC, "24 × 30 in", True, 2024,
                "Majestic lion in profile — explosive blues, magentas, oranges "
                "and gold in thick impasto against a glowing teal ground.",
            ),
            (
                "Mayur ra Rajkumari",
                "Color Paintings", "38500.00", 1, True, 4.8, 19,
                "Rekha Manandhar", O, "28 × 36 in", True, 2023,
                "Royal woman in blue and gold with peacocks — traditional "
                "jewellery, grapes and luminous feathers in a night garden.",
            ),
            (
                "Suryasta ra Rukh",
                "Color Paintings", "12500.00", 1, False, 4.5, 8,
                "Anita Sharma", AC, "18 × 22 in", False, 2022,
                "Sunset over water — black tree silhouettes, bright sun "
                "and horizontal bands of yellow, green and blue.",
            ),
            (
                "Rangin Barishma Paila",
                "Color Paintings", "22000.00", 1, True, 4.8, 16,
                "Prabhu KC", AC, "30 × 40 in", False, 2024,
                "Figures with colourful umbrellas in the rain — vertical paint "
                "drips and vivid reflections on a wet city street.",
            ),
            (
                "Rang ko Anga",
                "Color Paintings", "19500.00", 1, False, 4.7, 14,
                "Kamala Thapa", AC, "20 × 24 in", False, 2024,
                "Expressive colour portrait — warm and cool patches across "
                "the face, rainbow hair and bold palette-knife strokes.",
            ),

            # ── Pencil Paintings ──────────────────────────────────────
            (
                "Parekhuko Jhalak",
                "Pencil Paintings", "11800.00", 1, True, 4.7, 13,
                "Sabina Rai", PC, "12 × 16 in", False, 2024,
                "Delicate profile portrait in pencil — wispy hair across the face "
                "and a quiet, downward gaze in soft graphite lines.",
            ),
            (
                "Bagh ko Drishti",
                "Pencil Paintings", "19500.00", 1, True, 4.9, 21,
                "Rajesh Maharjan", PC, "18 × 22 in", True, 2024,
                "Hyper-real tiger head in graphite — piercing eyes, bold stripes "
                "and fine whiskers emerging from a deep black ground.",
            ),
            (
                "Aankha ra Haat",
                "Pencil Paintings", "16800.00", 1, False, 4.8, 15,
                "Deepak Shrestha", PC, "16 × 20 in", False, 2023,
                "Surreal drawing — many hands with pencils shaping a single "
                "detailed eye at the centre of the composition.",
            ),
            (
                "Shanti Taal ra Ghar",
                "Pencil Paintings", "14200.00", 1, False, 4.6, 10,
                "Nirmala Ghimire", PC, "20 × 26 in", True, 2023,
                "Lakeside village in pencil — villa, cypress trees, stone wall "
                "and calm water with layered hills beyond.",
            ),
            (
                "Hatti ko Muhar",
                "Pencil Paintings", "17500.00", 1, True, 4.8, 17,
                "Keshav Fuyal", PC, "18 × 24 in", True, 2024,
                "Elephant head in profile — wrinkled skin, curved trunk and tusk "
                "rendered in meticulous graphite shading.",
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
            slug__in=(
                *RETIRED_LANDSCAPE_SLUGS,
                *RETIRED_PORTRAIT_SLUGS,
                *RETIRED_ABSTRACT_SLUGS,
                *RETIRED_STILL_LIFE_SLUGS,
                *RETIRED_CONTEMPORARY_SLUGS,
                *RETIRED_COLOR_PAINTINGS_SLUGS,
                *RETIRED_PENCIL_PAINTINGS_SLUGS,
            )
        ).delete()
        if removed:
            self.stdout.write(self.style.WARNING(f"  - removed {removed} retired listing(s)"))

        if not options.get("skip_images"):
            self.stdout.write("Downloading painting images...")
            ok, failed = attach_images_for_all_products(self.stdout, self.style)
            self.stdout.write(self.style.SUCCESS(f"Images: {ok} ok, {failed} failed."))

        self.stdout.write(self.style.SUCCESS("ChitraBazar catalog seed complete."))
