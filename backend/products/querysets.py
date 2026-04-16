from django.db.models import Count, Prefetch, Q

from products.models import Product, ProductImage


def active_products_queryset():
    """Base queryset: active products in the single-vendor catalog."""
    return Product.objects.filter(is_active=True).select_related("category").prefetch_related(
        Prefetch(
            "images",
            queryset=ProductImage.objects.order_by("-is_primary", "sort_order"),
        )
    )


def annotate_category_product_count(queryset):
    return queryset.annotate(
        product_count=Count(
            "products",
            filter=Q(products__is_active=True),
        )
    )
