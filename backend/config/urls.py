"""URL configuration.

/admin/  -> Django's built-in admin (create / edit / delete categories and news)
/api/    -> read-only JSON API consumed by the React front end
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("news.urls")),
]
