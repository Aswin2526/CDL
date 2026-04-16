from django.db.models import Q


def apply_product_filters(queryset, params):
    """Apply search and filter query params to product queryset."""
    search = params.get("q") or params.get("search")
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
            | Q(artist_name__icontains=search)
        )

    medium = params.get("medium")
    if medium:
        queryset = queryset.filter(medium=medium)

    category_slug = params.get("category")
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    category_id = params.get("category_id")
    if category_id:
        queryset = queryset.filter(category_id=category_id)

    min_price = params.get("min_price")
    if min_price not in (None, ""):
        queryset = queryset.filter(price__gte=min_price)

    max_price = params.get("max_price")
    if max_price not in (None, ""):
        queryset = queryset.filter(price__lte=max_price)

    min_rating = params.get("min_rating")
    if min_rating not in (None, ""):
        queryset = queryset.filter(average_rating__gte=min_rating)

    return queryset


SORT_OPTIONS = {
    "latest": "-created_at",
    "price_low": "price",
    "price_high": "-price",
    "top_rated": "-average_rating",
}


def apply_product_sorting(queryset, sort_param):
    ordering = SORT_OPTIONS.get(sort_param, "-created_at")
    return queryset.order_by(ordering)
