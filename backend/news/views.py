from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Category, News
from .serializers import CategorySerializer, NewsItemSerializer

MAX_LIMIT = 100


def positive_int_param(request, name: str) -> int | None:
    """Return a query-string parameter as a positive int, or None if absent."""
    raw = request.query_params.get(name)
    if raw in (None, ""):
        return None
    try:
        value = int(raw)
    except ValueError:
        value = 0
    if value < 1:
        raise ValidationError({name: "Must be a positive whole number."})
    return value


class CategoryListView(ListAPIView):
    """GET /api/categories/ - every category with its article count, A-Z."""

    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(article_count=Count("news")).order_by("name")


class NewsListView(ListAPIView):
    """GET /api/news/ - articles, newest first.

    Query parameters:
      category=<id>  only articles in that category
      limit=<n>      only the n most recent (max 100), e.g. limit=4 for the home page
    """

    serializer_class = NewsItemSerializer

    def get_queryset(self):
        queryset = News.objects.select_related("category")  # Meta.ordering = newest first

        category_id = positive_int_param(self.request, "category")
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        limit = positive_int_param(self.request, "limit")
        if limit is not None:
            queryset = queryset[: min(limit, MAX_LIMIT)]
        return queryset


class NewsDetailView(RetrieveAPIView):
    """GET /api/news/<id>/ - one full article."""

    serializer_class = NewsItemSerializer
    queryset = News.objects.select_related("category")
