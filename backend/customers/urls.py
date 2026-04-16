from django.urls import path

from customers.views import (
    WishlistListCreateView,
    WishlistRemoveView,
    WishlistToggleView,
)

app_name = "customers"

urlpatterns = [
    path("wishlist/", WishlistListCreateView.as_view(), name="wishlist"),
    path("wishlist/toggle/", WishlistToggleView.as_view(), name="wishlist_toggle"),
    path(
        "wishlist/<int:product_id>/",
        WishlistRemoveView.as_view(),
        name="wishlist_remove",
    ),
]
