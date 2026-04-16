from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import WishlistItem
from customers.serializers import WishlistItemSerializer
from products.querysets import active_products_queryset


class WishlistListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/customers/wishlist/"""

    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        return (
            WishlistItem.objects.filter(user=self.request.user)
            .select_related("product__category", "product__vendor")
            .prefetch_related("product__images")
        )

    def perform_create(self, serializer):
        serializer.save()


class WishlistRemoveView(APIView):
    """DELETE /api/customers/wishlist/<product_id>/"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        deleted, _ = WishlistItem.objects.filter(
            user=request.user,
            product_id=product_id,
        ).delete()
        if not deleted:
            return Response(
                {"detail": "Item not in wishlist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistToggleView(APIView):
    """POST /api/customers/wishlist/toggle/ — body: { product_id }"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not active_products_queryset().filter(pk=product_id).exists():
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        item = WishlistItem.objects.filter(
            user=request.user,
            product_id=product_id,
        ).first()
        if item:
            item.delete()
            return Response({"in_wishlist": False, "message": "Removed from wishlist."})
        WishlistItem.objects.create(user=request.user, product_id=product_id)
        return Response({"in_wishlist": True, "message": "Added to wishlist."})
