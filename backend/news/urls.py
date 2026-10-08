from django.urls import path

from . import views, views_auth

app_name = "news"

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("news/", views.NewsListView.as_view(), name="news-list"),
    path("news/<int:pk>/", views.NewsDetailView.as_view(), name="news-detail"),
    path("auth/me/", views_auth.me, name="auth-me"),
    path("auth/logout/", views_auth.logout_view, name="auth-logout"),
]
