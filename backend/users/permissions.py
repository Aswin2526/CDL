from rest_framework.permissions import BasePermission

from users.models import Role


class IsAdminUser(BasePermission):
    """Allow only admin role users."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.role == Role.ADMIN or user.is_superuser
        )


class IsCustomerUser(BasePermission):
    """Allow only customer role users."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == Role.CUSTOMER
