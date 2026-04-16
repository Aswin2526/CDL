from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "product",
            "user",
            "user_name",
            "user_email",
            "rating",
            "comment",
            "created_at",
        )
        read_only_fields = ("id", "user", "product", "created_at")


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("rating", "comment")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
