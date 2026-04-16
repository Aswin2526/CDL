from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "full_name", "phone_number")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone_number", "profile_image")}),
        ("Role", {"fields": ("role", "is_customer", "is_admin")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions")
