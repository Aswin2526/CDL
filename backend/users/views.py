from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.jwt_serializers import EmailTokenObtainPairSerializer
from users.serializers import (
    ProfileUpdateSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/users/register/ — create collector (customer) account."""

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Registration successful.",
                "user": UserSerializer(user, context={"request": request}).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """POST /api/users/login/ — obtain JWT access and refresh tokens."""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        email = (
            request.data.get("email") or request.data.get("username") or ""
        ).strip().lower()
        user = User.objects.filter(email__iexact=email).first()
        if user:
            response.data["user"] = UserSerializer(
                user, context={"request": request}
            ).data
            response.data["message"] = "Login successful."
        return response


class LogoutView(APIView):
    """
    POST /api/users/logout/ — client should discard stored JWT tokens.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/users/profile/ — view and update authenticated user profile."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProfileUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            UserSerializer(request.user, context={"request": request}).data
        )


class ProfileImageUploadView(APIView):
    """POST /api/users/profile/image/ — upload profile image."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image = request.FILES.get("profile_image")
        if not image:
            return Response(
                {"detail": "No image file provided (use field name 'profile_image')."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.profile_image = image
        request.user.save()
        return Response(
            UserSerializer(request.user, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )
