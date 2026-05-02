from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.models import Cart, CartItem
from carts.serializers import CartSerializer
from products.querysets import active_products_queryset


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartDetailView(APIView):
    """GET /api/carts/ — current user's cart."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart, context={"request": request}).data)


class CartAddView(APIView):
    """POST /api/carts/add/ — body: { product_id, quantity? }."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response(
                {"detail": "quantity must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if quantity < 1:
            return Response(
                {"detail": "quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = active_products_queryset().filter(pk=product_id).first()
        if not product:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not product.in_stock:
            return Response(
                {"detail": "This painting is sold out."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if quantity > product.stock:
            return Response(
                {"detail": f"Only {product.stock} available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_or_create_cart(request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            new_qty = item.quantity + quantity
            if new_qty > product.stock:
                return Response(
                    {"detail": f"Only {product.stock} available."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.quantity = new_qty
            item.save(update_fields=["quantity", "updated_at"])

        return Response(
            {
                **_cart_response(cart, request, "Added to cart."),
                "in_cart": True,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


def _cart_response(cart, request, message):
    cart = Cart.objects.prefetch_related(
        "items__product__category",
        "items__product__images",
    ).get(pk=cart.pk)
    return {
        "message": message,
        "cart": CartSerializer(cart, context={"request": request}).data,
    }


class CartItemView(APIView):
    """PATCH /api/carts/items/<product_id>/ — set quantity.
    DELETE /api/carts/items/<product_id>/ — remove item."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id):
        try:
            quantity = int(request.data.get("quantity"))
        except (TypeError, ValueError):
            return Response(
                {"detail": "quantity is required and must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_or_create_cart(request.user)
        item = (
            CartItem.objects.filter(cart=cart, product_id=product_id)
            .select_related("product")
            .first()
        )
        if not item:
            return Response(
                {"detail": "Item not in cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

        product = item.product
        if quantity < 1:
            item.delete()
            return Response(
                {
                    **_cart_response(cart, request, "Removed from cart."),
                    "in_cart": False,
                }
            )

        if not product.is_active or not product.in_stock:
            return Response(
                {"detail": "This painting is no longer available."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if quantity > product.stock:
            return Response(
                {"detail": f"Only {product.stock} available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item.quantity = quantity
        item.save(update_fields=["quantity", "updated_at"])
        return Response(
            {
                **_cart_response(cart, request, "Quantity updated."),
                "in_cart": True,
            }
        )

    def delete(self, request, product_id):
        cart = get_or_create_cart(request.user)
        deleted, _ = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        if not deleted:
            return Response(
                {"detail": "Item not in cart."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {
                **_cart_response(cart, request, "Removed from cart."),
                "in_cart": False,
            }
        )


class CartClearView(APIView):
    """DELETE /api/carts/clear/."""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        CartItem.objects.filter(cart=cart).delete()
        return Response(
            {
                "message": "Cart cleared.",
                "cart": CartSerializer(cart, context={"request": request}).data,
            }
        )
