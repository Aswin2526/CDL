from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from customers.models import CustomerProfile
from users.models import Role

User = get_user_model()


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ("address", "profile_image", "created_at")
        read_only_fields = ("created_at",)


class UserSerializer(serializers.ModelSerializer):
    customer_profile = CustomerProfileSerializer(read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "profile_image",
            "role",
            "is_customer",
            "is_admin",
            "created_at",
            "customer_profile",
        )
        read_only_fields = (
            "profile_image",
            "id",
            "email",
            "role",
            "is_customer",
            "is_admin",
            "created_at",
            "customer_profile",
        )

    def get_profile_image(self, obj):
        if not obj.profile_image:
            return None
        request = self.context.get("request")
        url = obj.profile_image.url
        if request:
            return request.build_absolute_uri(url)
        return url


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        address = validated_data.pop("address", "")
        validated_data.pop("role", None)
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            role=Role.CUSTOMER,
            **validated_data,
        )
        CustomerProfile.objects.create(user=user, address=address)
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ("full_name", "phone_number", "profile_image", "address")

    def update(self, instance, validated_data):
        address = validated_data.pop("address", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address is not None:
            profile, _ = CustomerProfile.objects.get_or_create(user=instance)
            profile.address = address
            profile.save()

        return instance
