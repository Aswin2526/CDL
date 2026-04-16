from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from products.querysets import active_products_queryset
from reviews.models import Review
from reviews.serializers import ReviewCreateSerializer, ReviewSerializer
from reviews.services import update_product_rating


class ProductReviewListView(generics.ListAPIView):
    """GET /api/reviews/product/<product_id>/"""

    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(
            product_id=self.kwargs["product_id"]
        ).select_related("user")


class ProductReviewCreateView(generics.CreateAPIView):
    """POST /api/reviews/product/<product_id>/"""

    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        if not active_products_queryset().filter(pk=product_id).exists():
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if Review.objects.filter(product_id=product_id, user=request.user).exists():
            return Response(
                {"detail": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(
            product_id=product_id,
            user=request.user,
            **serializer.validated_data,
        )
        update_product_rating(product_id)
        return Response(
            ReviewSerializer(review, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
