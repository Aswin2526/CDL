"""
Artwork images for catalog seeding — exactly one unique image per product slug.
Four user reference paintings use local files; every other slug has its own Picsum ID.
"""

import hashlib
import time
import urllib.error
import urllib.request
from pathlib import Path

from django.core.files.base import ContentFile

SEED_IMAGES_DIR = Path(__file__).resolve().parent.parent / "seed_images"

REFERENCE_LOCAL: dict[str, str] = {
    "nilo-nayan-phoolbhitra": "nayan-nilo-ankha.png",
    "gaun-ko-ghar-bagaicha": "ghar-bagaicha-landscape.png",
    "charcoal-gaun-ko-bato": "charcoal-gaon-bato.png",
    "kala-safed-fashion-portrait": "fashion-portrait-black-white.png",
    "shishir-himal-ra-pul": "shishir-himal-ra-pul.png",
    "himshanti-taal": "himshanti-taal.png",
    "sakura-sanjhama-himal": "sakura-sanjhama-himal.png",
    "neelo-ghar-ko-bato": "neelo-ghar-ko-bato.png",
    "suryodayako-bato": "suryodayako-bato.png",
    "pataley-chhango": "pataley-chhango.png",
    "antarman-ko-jhalak": "antarman-ko-jhalak.png",
    "suryodaya-sundari": "suryodaya-sundari.png",
    "seto-lace-ko-keti": "seto-lace-ko-keti.png",
    "nischal-herai": "nischal-herai.png",
    "ujyalo-muskan": "ujyalo-muskan.png",
    "barkha-ko-rang": "barkha-ko-rang.png",
    "antardwanda": "antardwanda.png",
    "kala-chakra": "kala-chakra.png",
    "indreni-aankha": "indreni-aankha.png",
    "kiriko-jwalo": "kiriko-jwalo.png",
    "pustak-ra-suntala": "pustak-ra-suntala.png",
    "falharu-ko-jhund": "falharu-ko-jhund.png",
    "jeevan-ko-sandesh": "jeevan-ko-sandesh.png",
    "phoolharu-ko-guchchha": "phoolharu-ko-guchchha.png",
    "bhansa-kotha-still-life": "bhansa-kotha-still-life.png",
    "bada-khutta-ra-surya": "bada-khutta-surya.png",
    "poolside-dui-roop": "poolside-dui-roop.png",
    "sochko-dhara": "sochko-dhara.png",
    "rato-kursi-ma-aram": "rato-kursi-aram.png",
    "jwan-ko-chhaya": "jwan-ko-chhaya.png",
    "rangin-singhako-muhar": "rangin-singhako-muhar.png",
    "mayur-ra-rajkumari": "mayur-ra-rajkumari.png",
    "suryasta-ra-rukh": "suryasta-ra-rukh.png",
    "rangin-barishma-paila": "rangin-barishma-paila.png",
    "rang-ko-anga": "rang-ko-anga.png",
    "parekhuko-jhalak": "parekhuko-jhalak.png",
    "bagh-ko-drishti": "bagh-ko-drishti.png",
    "aankha-ra-haat": "aankha-ra-haat.png",
    "shanti-taal-ra-ghar": "shanti-taal-ra-ghar.png",
    "hatti-ko-muhar": "hatti-ko-muhar.png",
}

# Replaced landscape listings (removed on seed)
RETIRED_LANDSCAPE_SLUGS = (
    "phewa-tal-bihani",
    "gaaun-ko-bato",
    "himal-ko-bhor",
    "fulbari-sanjha",
    "terai-khet-hari",
    "koshi-nadiko-kinara",
)

RETIRED_PORTRAIT_SLUGS = (
    "neta-ko-nayan-blue-eye-portrait",
    "bhadragol-sundar-akhi",
    "rato-oth-ko-roop",
    "pahadi-naari-portrait",
    "buwa-ko-muhar",
)

RETIRED_ABSTRACT_SLUGS = (
    "rangeen-sapana",
    "naya-bihani-rang",
    "rang-ko-khel",
)

RETIRED_STILL_LIFE_SLUGS = (
    "phool-ko-ful",
    "bagaincha-ko-mewa",
)

# Legacy contemporary slugs (category was empty in seed; safe cleanup)
RETIRED_CONTEMPORARY_SLUGS: tuple[str, ...] = ()

RETIRED_COLOR_PAINTINGS_SLUGS = (
    "lali-gurans-phuleko",
    "indra-jatra-utsav",
    "seto-machindranath-rath",
    "taal-ko-rang",
    "holi-ko-khushi",
    "parijat-phul",
)

RETIRED_PENCIL_PAINTINGS_SLUGS = (
    "charcoal-gaaun-saanjh",
    "pencil-ko-pahaad",
    "graphite-portrait-budha",
    "raat-ko-bato-charcoal",
    "aankhako-bhaav-sketch",
    "mustang-dharahara-pencil",
    "aakash-pencil-sketch",
    "ghaam-pani-charcoal",
)

# One unique Picsum photo ID per slug — no duplicates in the gallery
SLUG_TO_PICSUM_ID: dict[str, int] = {
    "ghaam-pani-charcoal": 366,
    "hathle-baneko-gurans": 433,
    "kathmandu-durbar-charcoal": 439,
    "pokhara-lake-graphite-original": 442,
    "baal-sain-charcoal-portrait": 449,
    "dhaka-topi-wala-sketch": 452,
    "prayer-flag-ridge-drawing": 454,
    "sadak-ko-kukur-pencil": 456,
    "monsoon-khola-charcoal": 457,
}


def _pool_index(slug: str, pool_size: int) -> int:
    digest = hashlib.md5(slug.encode(), usedforsecurity=False).hexdigest()
    return int(digest, 16) % pool_size


def picsum_url_for_slug(slug: str) -> str:
    photo_id = SLUG_TO_PICSUM_ID.get(slug)
    if photo_id is None:
        photo_id = 100 + _pool_index(slug, 900)
    return f"https://picsum.photos/id/{photo_id}/600/700"


def image_source_for_product(product) -> tuple[str, str]:
    slug = getattr(product, "slug", "") or ""
    if slug in REFERENCE_LOCAL:
        path = SEED_IMAGES_DIR / REFERENCE_LOCAL[slug]
        if path.is_file():
            return ("local", str(path))
    return ("url", picsum_url_for_slug(slug))


def external_image_url_for_product(product) -> str:
    kind, src = image_source_for_product(product)
    if kind == "url":
        return src
    return f"/media/seed-preview/{Path(src).name}"


def download_image(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ChitraBazarCatalogSeed/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def attach_catalog_image(product, stdout=None, style=None) -> bool:
    from products.models import ProductImage

    kind, src = image_source_for_product(product)

    try:
        if kind == "local":
            path = Path(src)
            data = path.read_bytes()
            ext = path.suffix.lower()
        else:
            data = download_image(src)
            ext = ".jpg"
    except (urllib.error.URLError, TimeoutError, OSError, FileNotFoundError) as exc:
        if stdout and style:
            stdout.write(style.WARNING(f"  ! {product.slug}: {exc}"))
        return False

    ProductImage.objects.filter(product=product).delete()
    record = ProductImage(
        product=product,
        alt_text=product.name,
        is_primary=True,
        sort_order=0,
    )
    record.image.save(f"{product.slug}{ext}", ContentFile(data), save=True)
    if stdout:
        stdout.write(f"  img {product.name}")
    return True


def attach_images_for_all_products(stdout=None, style=None) -> tuple[int, int]:
    from products.models import Product

    ok = 0
    failed = 0
    products = list(Product.objects.select_related("category").order_by("id"))
    for i, product in enumerate(products):
        if attach_catalog_image(product, stdout=stdout, style=style):
            ok += 1
        else:
            failed += 1
        # Gentle delay so Picsum does not throttle bulk downloads
        if i < len(products) - 1:
            time.sleep(0.35)
    return ok, failed
