"""
Artwork image URLs and helpers for catalog seeding / API fallbacks.
Uses Picsum Photos (deterministic per product slug) for gallery thumbnails.
"""

import hashlib
import urllib.error
import urllib.request

from django.core.files.base import ContentFile

# Curated Picsum IDs — paintings, galleries, sketches (stable direct URLs)
COLOR_PICSUM_IDS = [
    29,  # art / paint
    37,  # abstract
    64,  # creative
    96,  # texture
    111,  # color
    119,  # structure
    146,  # nature color
    152,  # warm tones
    175,  # soft
    180,  # vivid
    213,  # landscape
    225,  # detail
    287,  # pattern
    338,  # gallery feel
    367,  # mood
]

PENCIL_PICSUM_IDS = [
    24,  # monochrome feel
    48,  # texture
    52,  # minimal
    60,  # contrast
    106,  # sketchy
    250,  # soft gray
    305,  # detail
    366,  # quiet
]


def _pool_index(slug: str, pool_size: int) -> int:
    digest = hashlib.md5(slug.encode(), usedforsecurity=False).hexdigest()
    return int(digest, 16) % pool_size


def external_image_url_for_product(product) -> str:
    """Public URL for a product when no uploaded file exists yet."""
    category_slug = getattr(product.category, "slug", "") or ""
    medium = getattr(product, "medium", "") or ""

    if category_slug == "pencil-paintings" or medium == "pencil":
        pool = PENCIL_PICSUM_IDS
    else:
        pool = COLOR_PICSUM_IDS

    photo_id = pool[_pool_index(product.slug, len(pool))]
    return f"https://picsum.photos/id/{photo_id}/400/500"


def download_image(url: str, timeout: int = 45) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ChitraBazarCatalogSeed/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def attach_catalog_image(product, stdout=None, style=None) -> bool:
    """Download and save primary ProductImage for one product."""
    from products.models import ProductImage

    url = external_image_url_for_product(product)
    try:
        data = download_image(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        if stdout and style:
            stdout.write(style.WARNING(f"  ! image failed for {product.slug}: {exc}"))
        return False

    ProductImage.objects.filter(product=product).delete()
    record = ProductImage(
        product=product,
        alt_text=product.name,
        is_primary=True,
        sort_order=0,
    )
    record.image.save(f"{product.slug}.jpg", ContentFile(data), save=True)
    if stdout:
        stdout.write(f"  img {product.name}")
    return True


def attach_images_for_all_products(stdout=None, style=None) -> tuple[int, int]:
    from products.models import Product

    ok = 0
    failed = 0
    for product in Product.objects.select_related("category").order_by("id"):
        if attach_catalog_image(product, stdout=stdout, style=style):
            ok += 1
        else:
            failed += 1
    return ok, failed
