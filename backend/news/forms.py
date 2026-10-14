from django import forms
from django.utils import timezone

from .models import Category, News


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
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
