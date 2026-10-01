from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("news/", views.NewsListView.as_view(), name="news-list"),
    path("news/<int:pk>/", views.NewsDetailView.as_view(), name="news-detail"),
]
