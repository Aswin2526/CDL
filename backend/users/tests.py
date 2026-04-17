import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")

    def _unique_email(self):
        return f"user_{uuid.uuid4().hex[:8]}@example.com"

    def test_register_returns_user_and_tokens(self):
        email = self._unique_email()
        payload = {
            "full_name": "Jane Collector",
            "email": email,
            "password": "securepass123",
            "phone_number": "9800000000",
            "address": "Pokhara",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])
        self.assertEqual(response.data["user"]["email"], email)
        self.assertEqual(response.data["user"]["role"], "customer")
        self.assertTrue(User.objects.filter(email=email).exists())

    def test_login_returns_jwt_and_user(self):
        email = self._unique_email()
        password = "securepass123"
        self.client.post(
            self.register_url,
            {
                "full_name": "Login Test",
                "email": email,
                "password": password,
            },
            format="json",
        )

        response = self.client.post(
            self.login_url,
            {"email": email, "password": password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], email)

    def test_register_rejects_duplicate_email(self):
        email = self._unique_email()
        payload = {
            "full_name": "First User",
            "email": email,
            "password": "securepass123",
        }
        self.client.post(self.register_url, payload, format="json")

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
