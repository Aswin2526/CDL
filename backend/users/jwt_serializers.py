from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept email + password for JWT login (custom user model)."""

    username_field = "email"
