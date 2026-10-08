"""URL configuration.

/django-admin/  -> Django's built-in admin, and the login page for the React admin
/api/           -> JSON API used by the React front end. Anyone can read; writes
                   need a logged-in superuser.
/admin          -> the React admin page, served by Django (superusers only)
everything else -> the React app, served by Django; React Router picks the page
"""

from django.contrib import admin
from django.urls import include, path, re_path

from news.views_spa import AdminSpaView, SpaView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/", include("news.urls")),
    re_path(r"^admin/?$", AdminSpaView.as_view(), name="spa-admin"),
    re_path(r"^(?!api/|django-admin/|static/).*$", SpaView.as_view(), name="spa"),
]
