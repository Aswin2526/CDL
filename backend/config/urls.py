"""
Root URL configuration for ChitraBazar API.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.views import root

admin.site.site_header = "ChitraBazar Administration"
admin.site.site_title = "ChitraBazar"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path("", root, name="root"),
    path("admin/", admin.site.urls),
    # API routes (Phase 2+)
    path("api/users/", include("users.urls")),
    path("api/customers/", include("customers.urls")),
    path("api/products/", include("products.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/carts/", include("carts.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/analytics/", include("analytics.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
