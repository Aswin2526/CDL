from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.models import Cart, CartItem
from customers.models import WishlistItem
from products.models import Category, Product
from reviews.models import Review
from users.models import Role
from users.permissions import IsAdminUser

User = get_user_model()


class AdminDashboardStatsView(APIView):
    """GET /api/analytics/admin/dashboard/ — store overview for admins."""

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        products = Product.objects.all()
        active = products.filter(is_active=True)
        cart_items = CartItem.objects.select_related("product", "cart__user")
        carts_with_items = Cart.objects.filter(items__isnull=False).distinct()

        category_rows = list(
            Category.objects.annotate(
                product_count=Count(
                    "products",
                    filter=models.Q(products__is_active=True),
                )
            )
            .order_by("name")
            .values("name", "slug", "product_count")
        )

        recent = list(
            active.select_related("category")
            .order_by("-updated_at")[:8]
            .values(
                "id",
                "name",
                "slug",
                "artist_name",
                "price",
                "stock",
                "is_featured",
                "category__name",
            )
        )

        low_stock = list(
            active.filter(stock__lte=2)
            .order_by("stock", "name")[:10]
            .values("id", "name", "slug", "stock", "price")
        )

        cart_subtotal = sum(item.line_total for item in cart_items)

        return Response(
            {
                "totals": {
                    "products_active": active.count(),
                    "products_inactive": products.filter(is_active=False).count(),
                    "categories": Category.objects.count(),
                    "customers": User.objects.filter(role=Role.CUSTOMER).count(),
                    "wishlist_items": WishlistItem.objects.count(),
                    "active_carts": carts_with_items.count(),
                    "cart_line_items": cart_items.count(),
                    "reviews": Review.objects.count(),
                    "featured_products": active.filter(is_featured=True).count(),
                    "sold_out": active.filter(stock=0).count(),
                },
                "cart_value": {
                    "subtotal": str(cart_subtotal),
                },
                "categories": category_rows,
                "recent_products": recent,
                "low_stock": low_stock,
            }
        )
