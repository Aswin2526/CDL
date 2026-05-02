from rest_framework import serializers

from products.catalog_images import external_image_url_for_product
from products.models import Category, Product, ProductImage, StoreSettings


def build_absolute_media_url(request, file_field):
    """Return a URL the browser can load (relative /media/ works with Vite proxy)."""
    if not file_field:
        return None
    url = file_field.url
    if not request:
        return url
    # Prefer same-origin relative path so Vite dev proxy serves /media correctly
    if request.get_host().startswith("127.0.0.1") or request.get_host().startswith("localhost"):
        return url
    return request.build_absolute_uri(url)


class StoreSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = ("name", "tagline", "address", "phone", "email")


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "image", "product_count")

    product_count = serializers.IntegerField(read_only=True, required=False)

    def get_image(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt_text", "is_primary", "sort_order")

    def get_image(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    primary_image = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "artist_name",
            "medium",
            "dimensions",
            "is_framed",
            "price",
            "average_rating",
            "review_count",
            "category",
            "category_slug",
            "primary_image",
            "stock",
            "in_stock",
            "is_featured",
            "created_at",
        )

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image and image.image:
            return build_absolute_media_url(self.context.get("request"), image.image)
        return external_image_url_for_product(obj)


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    store = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    medium_display = serializers.CharField(source="get_medium_display", read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "artist_name",
            "medium",
            "medium_display",
            "dimensions",
            "is_framed",
            "year_created",
            "description",
            "price",
            "stock",
            "in_stock",
            "average_rating",
            "review_count",
            "is_featured",
            "category",
            "store",
            "images",
            "reviews",
            "created_at",
            "updated_at",
        )

    def get_store(self, obj):
        return StoreSettingsSerializer(StoreSettings.load()).data

    def get_reviews(self, obj):
        from reviews.serializers import ReviewSerializer

        reviews = obj.reviews.select_related("user")[:10]
        return ReviewSerializer(reviews, many=True, context=self.context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get("images"):
            data["images"] = [
                {
                    "id": None,
                    "image": external_image_url_for_product(instance),
                    "alt_text": instance.name,
                    "is_primary": True,
                    "sort_order": 0,
                }
            ]
        return data
