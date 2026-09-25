from django.contrib import admin
from django.db.models import Count

from .models import Category, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "article_count")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_article_count=Count("news"))

    @admin.display(description="Articles", ordering="_article_count")
    def article_count(self, obj):
        return obj._article_count


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "source", "date_and_time")
    list_filter = ("category", "date_and_time")
    list_select_related = ("category",)
    search_fields = ("title", "source", "content")
    date_hierarchy = "date_and_time"
    fields = ("title", "category", "source", "date_and_time", "content")
