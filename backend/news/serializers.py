from rest_framework import serializers

from .models import Category, News


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "article_count")


class CategoryBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class NewsItemSerializer(serializers.ModelSerializer):
    """The full article. Used for both the list and the detail endpoint -
    the front end's own CSS truncates it wherever a preview is needed."""

    category = CategoryBriefSerializer(read_only=True)

    class Meta:
        model = News
        fields = ("id", "title", "category", "source", "date_and_time", "content")
