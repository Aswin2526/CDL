"""
Artwork images for catalog seeding and API fallbacks.
Prefers bundled painting files in backend/seed_images/ (real artworks).
"""

import hashlib
from pathlib import Path

from django.core.files.base import ContentFile

# backend/seed_images/ — four reference paintings supplied for ChitraBazar
SEED_IMAGES_DIR = Path(__file__).resolve().parent.parent / "seed_images"

LOCAL_PAINTINGS = [
    "nayan-nilo-ankha.png",
    "ghar-bagaicha-landscape.png",
    "charcoal-gaon-bato.png",
    "fashion-portrait-black-white.png",
]

# Best match per slug for the four reference paintings
SLUG_TO_LOCAL_FILE: dict[str, str] = {
    # Four reference paintings (user-provided)
    "nilo-nayan-phoolbhitra": "nayan-nilo-ankha.png",
    "gaun-ko-ghar-bagaicha": "ghar-bagaicha-landscape.png",
    "charcoal-gaun-ko-bato": "charcoal-gaon-bato.png",
    "kala-safed-fashion-portrait": "fashion-portrait-black-white.png",
    "neta-ko-nayan-blue-eye-portrait": "nayan-nilo-ankha.png",
    "bhadragol-sundar-akhi": "nayan-nilo-ankha.png",
    "aankhako-bhaav-sketch": "nayan-nilo-ankha.png",
    "pahadi-naari-portrait": "nayan-nilo-ankha.png",
    "gaaun-ko-bato": "ghar-bagaicha-landscape.png",
    "phewa-tal-bihani": "ghar-bagaicha-landscape.png",
    "terai-khet-hari": "ghar-bagaicha-landscape.png",
    "fulbari-sanjha": "ghar-bagaicha-landscape.png",
    "himal-ko-bhor": "ghar-bagaicha-landscape.png",
    "koshi-nadiko-kinara": "ghar-bagaicha-landscape.png",
    "charcoal-gaaun-saanjh": "charcoal-gaon-bato.png",
    "raat-ko-bato-charcoal": "charcoal-gaon-bato.png",
    "pencil-ko-pahaad": "charcoal-gaon-bato.png",
    "mustang-dharahara-pencil": "charcoal-gaon-bato.png",
    "aakash-pencil-sketch": "charcoal-gaon-bato.png",
    "ghaam-pani-charcoal": "charcoal-gaon-bato.png",
    "graphite-portrait-budha": "charcoal-gaon-bato.png",
    "rato-oth-ko-roop": "fashion-portrait-black-white.png",
    "buwa-ko-muhar": "fashion-portrait-black-white.png",
}


def _pool_index(slug: str, pool_size: int) -> int:
    digest = hashlib.md5(slug.encode(), usedforsecurity=False).hexdigest()
    return int(digest, 16) % pool_size


def local_image_path_for_product(product) -> Path | None:
    slug = getattr(product, "slug", "") or ""
    filename = SLUG_TO_LOCAL_FILE.get(slug)
    if not filename:
        filename = LOCAL_PAINTINGS[_pool_index(slug, len(LOCAL_PAINTINGS))]
    path = SEED_IMAGES_DIR / filename
    return path if path.is_file() else None


def external_image_url_for_product(product) -> str | None:
    """Relative media path hint when no file is attached yet (dev fallback)."""
    path = local_image_path_for_product(product)
    if path:
        return f"/media/seed-preview/{path.name}"
    return None


def read_local_image(product) -> tuple[bytes, str] | None:
    path = local_image_path_for_product(product)
    if not path:
        return None
    ext = path.suffix.lower()
    return path.read_bytes(), ext


def attach_catalog_image(product, stdout=None, style=None) -> bool:
    from products.models import ProductImage

    local = read_local_image(product)
    if not local:
        if stdout and style:
            stdout.write(
                style.WARNING(f"  ! no local painting for {product.slug}")
            )
        return False

    data, ext = local
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
    for product in Product.objects.select_related("category").order_by("id"):
        if attach_catalog_image(product, stdout=stdout, style=style):
            ok += 1
        else:
            failed += 1
    return ok, failed
