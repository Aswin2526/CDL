from django.urls import path

from analytics.views import AdminDashboardStatsView

app_name = "analytics"

urlpatterns = [
    path("admin/dashboard/", AdminDashboardStatsView.as_view(), name="admin_dashboard"),
]
