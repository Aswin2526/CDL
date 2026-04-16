from django.contrib import admin

from customers.models import CustomerProfile, WishlistItem


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
