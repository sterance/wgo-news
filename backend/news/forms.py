"""Validation for categories and news, shared by the Django admin and the API.

The admin uses these forms directly (``ModelAdmin.form``); the API serializers
run them from ``validate()`` so both paths enforce the same rules with the same
messages. ModelForm ``CharField``s strip surrounding whitespace by default, so
a whitespace-only value counts as blank.
"""

from django import forms
from django.utils import timezone

from .models import Category, News


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        # The Lower("name") constraint catches this too, but reports it as a
        # non-field error. Checking here puts the message on the name field.
        # Exact duplicates are left to the field's own unique check, so its
        # message is unchanged.
        duplicates = Category.objects.filter(name__iexact=name).exclude(name=name)
        if self.instance.pk is not None:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "category", "source", "date_and_time", "content"]

    def clean_date_and_time(self):
        value = self.cleaned_data["date_and_time"]
        if value and value > timezone.now():
            raise forms.ValidationError("The date and time cannot be in the future.")
        return value
