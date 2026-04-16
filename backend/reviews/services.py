from decimal import Decimal

from django.db.models import Avg, Count

from products.models import Product
from reviews.models import Review


def update_product_rating(product_id):
    """Recalculate average rating and review count for a product."""
    stats = Review.objects.filter(product_id=product_id).aggregate(
        avg=Avg("rating"),
        count=Count("id"),
    )
    Product.objects.filter(pk=product_id).update(
        average_rating=Decimal(str(round(stats["avg"] or 0, 2))),
        review_count=stats["count"] or 0,
    )
