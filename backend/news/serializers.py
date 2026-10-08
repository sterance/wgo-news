from django.db import models
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.settings import api_settings

from .forms import CategoryForm, NewsForm
from .models import Category, News


class FormValidationMixin:
    """Run ``form_class`` over the incoming data so the API shares the admin's validation.

    DRF's own field checks (required, blank, max length, exact-duplicate name)
    run first, so ``validate()`` only sees data that passed them and those
    messages are unchanged. The form adds the rest (future dates,
    case-insensitive duplicate names).
    """

    form_class = None

    def validate(self, attrs):
        # Start from the saved instance (PATCH) or a fresh one (so model defaults
        # such as date_and_time apply), then overlay what was sent.
        base = self.instance if self.instance is not None else self.Meta.model()
        data = model_to_dict(base, fields=self.form_class._meta.fields)
        data.update(attrs)
        data = {key: value.pk if isinstance(value, models.Model) else value for key, value in data.items()}

        form = self.form_class(data=data, instance=self.instance)
        if not form.is_valid():
            errors = {
                api_settings.NON_FIELD_ERRORS_KEY if field == "__all__" else field: [error["message"] for error in field_errors]
                for field, field_errors in form.errors.get_json_data().items()
            }
            raise serializers.ValidationError(errors)
        return attrs


class CategorySerializer(FormValidationMixin, serializers.ModelSerializer):
    form_class = CategoryForm
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "article_count")


class CategoryBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class NewsItemSerializer(FormValidationMixin, serializers.ModelSerializer):
    """The full article, with a category ID accepted for writes."""

    form_class = NewsForm
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = News
        fields = ("id", "title", "category", "source", "date_and_time", "content")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = CategoryBriefSerializer(instance.category).data
        return data
