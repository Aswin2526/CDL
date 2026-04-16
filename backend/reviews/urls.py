from django.urls import path

from reviews.views import ProductReviewCreateView, ProductReviewListView

app_name = "reviews"

urlpatterns = [
    path(
        "product/<int:product_id>/",
        ProductReviewListView.as_view(),
        name="product_reviews",
    ),
    path(
        "product/<int:product_id>/add/",
        ProductReviewCreateView.as_view(),
        name="add_review",
    ),
]
