from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class Category(models.Model):
    """A news category such as "Sports", "Technology" or "World"."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"
        constraints = [
            # `unique=True` is case-sensitive, so "War" and "war" would both be
            # allowed. This closes that gap so there really are no duplicates.
            models.UniqueConstraint(
                Lower("name"),
                name="category_name_unique_ci",
                violation_error_message="A category with this name already exists.",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        self.name = (self.name or "").strip()


class News(models.Model):
    """A single news article."""

    title = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # can't delete a category that still has articles
        related_name="news",
    )
    source = models.CharField(
        max_length=100,
        help_text='Where the article came from, e.g. "Reuters".',
    )
    date_and_time = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ["-date_and_time", "-id"]  # newest first
        verbose_name_plural = "news"
        indexes = [models.Index(fields=["-date_and_time"], name="news_date_time_idx")]

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if self.date_and_time and self.date_and_time > timezone.now():
            raise ValidationError({"date_and_time": "The date and time cannot be in the future."})
