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
    """The full article, with a category ID accepted for writes."""

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = News
        fields = ("id", "title", "category", "source", "date_and_time", "content")

    def validate_date_and_time(self, value):
        from django.utils import timezone

        if value > timezone.now():
            raise serializers.ValidationError("The date and time cannot be in the future.")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = CategoryBriefSerializer(instance.category).data
        return data
