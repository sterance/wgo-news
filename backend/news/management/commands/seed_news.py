"""Fill the database with demo categories and articles.

    python manage.py seed_news

Safe to run repeatedly: existing categories and articles (matched by title) are left alone.
"""

import json
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Category, News

CATEGORIES = [
    "nature", "war", "government", "politics", "education",
    "health", "economy", "business", "entertainment",
]


class Command(BaseCommand):
    help = "Create demo categories and news articles (idempotent)."

    def handle(self, *args, **options):
        categories = {}
        for name in CATEGORIES:
            categories[name], _ = Category.objects.get_or_create(name=name)

        created = 0
        json_path = Path(__file__).resolve().parent.parent.parent.parent / "fake_news.json"
        with open(json_path) as f:
            articles_data = json.load(f)

        for article_data in articles_data:
            dt = datetime.fromisoformat(article_data["pub_date"])
            pub_date = dt if timezone.is_aware(dt) else timezone.make_aware(dt)
            category = article_data["category"]
            title = article_data["title"]
            source = article_data["source"]
            content = article_data["content"]

            _, was_created = News.objects.get_or_create(
                title=title,
                defaults={
                    "category": categories[category],
                    "source": source,
                    "content": content,
                    "date_and_time": pub_date,
                },
            )
            created += was_created

        self.stdout.write(self.style.SUCCESS(
            f"{len(CATEGORIES)} categories ready, {created} new article(s) added."
        ))