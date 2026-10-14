from django.contrib import admin
from django.urls import include, path, re_path

from news.views_spa import AdminSpaView, SpaView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/", include("news.urls")),
    re_path(r"^admin/?$", AdminSpaView.as_view(), name="spa-admin"),
    re_path(r"^(?!api/|django-admin/|static/).*$", SpaView.as_view(), name="spa"),
]
