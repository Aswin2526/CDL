"""
Custom user model for ChitraBazar — email-based authentication with roles.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from users.managers import UserManager


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    CUSTOMER = "customer", "Customer"


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(
        upload_to="profiles/users/",
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.is_admin = self.role == Role.ADMIN
        self.is_customer = self.role == Role.CUSTOMER
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)
