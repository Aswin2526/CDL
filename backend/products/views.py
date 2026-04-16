from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from products.filters import apply_product_filters, apply_product_sorting
from products.models import Category, StoreSettings
from products.querysets import active_products_queryset, annotate_category_product_count
from products.serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    StoreSettingsSerializer,
)


class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    Query params: q, category, category_id, medium, min_price, max_price,
    min_rating, sort (latest|price_low|price_high|top_rated), page
    """

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = active_products_queryset()
        queryset = apply_product_filters(queryset, self.request.query_params)
        sort_param = self.request.query_params.get("sort", "latest")
        return apply_product_sorting(queryset, sort_param)


class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/products/<slug>/"""

    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return active_products_queryset().prefetch_related("reviews__user")


class StoreInfoView(APIView):
    """GET /api/products/store/ — single-vendor store details."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(StoreSettingsSerializer(StoreSettings.load()).data)


class CategoryListView(generics.ListAPIView):
    """GET /api/products/categories/"""

    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return annotate_category_product_count(
            Category.objects.filter(is_active=True)
        )


class CategoryProductsView(generics.ListAPIView):
    """GET /api/products/categories/<slug>/products/"""

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = active_products_queryset().filter(
            category__slug=self.kwargs["slug"]
        )
        queryset = apply_product_filters(queryset, self.request.query_params)
        sort_param = self.request.query_params.get("sort", "latest")
        return apply_product_sorting(queryset, sort_param)


class FeaturedProductsView(generics.ListAPIView):
    """GET /api/products/featured/"""

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return active_products_queryset().filter(is_featured=True)[:12]


class LatestProductsView(generics.ListAPIView):
    """GET /api/products/latest/"""

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return active_products_queryset()[:12]


class TopRatedProductsView(generics.ListAPIView):
    """GET /api/products/top-rated/"""

    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return (
            active_products_queryset()
            .filter(review_count__gt=0)
            .order_by("-average_rating")[:12]
        )
