from django.urls import path

from products.views import (
    CategoryListView,
    CategoryProductsView,
    FeaturedProductsView,
    LatestProductsView,
    ProductDetailView,
    ProductListView,
    StoreInfoView,
    TopRatedProductsView,
)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("store/", StoreInfoView.as_view(), name="store"),
    path("featured/", FeaturedProductsView.as_view(), name="featured"),
    path("latest/", LatestProductsView.as_view(), name="latest"),
    path("top-rated/", TopRatedProductsView.as_view(), name="top_rated"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path(
        "categories/<slug:slug>/products/",
        CategoryProductsView.as_view(),
        name="category_products",
    ),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]
