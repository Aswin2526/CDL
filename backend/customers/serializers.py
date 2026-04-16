from rest_framework import serializers

from customers.models import WishlistItem
from products.serializers import ProductListSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WishlistItem
        fields = ("id", "product", "product_id", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        user = self.context["request"].user
        from products.models import Product

        product = Product.objects.get(pk=product_id, is_active=True)
        item, created = WishlistItem.objects.get_or_create(user=user, product=product)
        if not created:
            raise serializers.ValidationError(
                {"product_id": "Product is already in your wishlist."}
            )
        return item
