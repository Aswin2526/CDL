from django.urls import path

from carts.views import CartAddView, CartClearView, CartDetailView, CartRemoveView

app_name = "carts"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    path("add/", CartAddView.as_view(), name="cart_add"),
    path("clear/", CartClearView.as_view(), name="cart_clear"),
    path("items/<int:product_id>/", CartRemoveView.as_view(), name="cart_remove"),
]
