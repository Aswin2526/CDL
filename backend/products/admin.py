from django.contrib import admin

from products.models import Category, Product, ProductImage, StoreSettings


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")

    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "artist_name",
        "medium",
        "category",
        "price",
        "stock",
        "is_featured",
        "is_active",
    )
    list_filter = ("category", "medium", "is_framed", "is_featured", "is_active")
    search_fields = ("name", "artist_name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_primary", "sort_order")
