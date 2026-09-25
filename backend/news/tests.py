from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, News


def make_news(category, title="A headline", hours_ago=0, **kwargs):
    defaults = {
        "source": "Reuters",
        "content": "Body text " * 40,
        "date_and_time": timezone.now() - timedelta(hours=hours_ago),
    }
    defaults.update(kwargs)
    return News.objects.create(title=title, category=category, **defaults)


class CategoryModelTests(TestCase):
    def test_name_must_be_unique(self):
        Category.objects.create(name="war")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(name="war")

    def test_name_uniqueness_ignores_case(self):
        Category.objects.create(name="war")
        with self.assertRaises(ValidationError):
            Category(name="War").full_clean()

    def test_cannot_delete_category_with_articles(self):
        category = Category.objects.create(name="war")
        make_news(category)
        with self.assertRaises(ProtectedError):
            category.delete()


class NewsModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="nature")

    def test_title_cannot_be_empty(self):
        news = News(title="", category=self.category, source="BBC", content="x")
        with self.assertRaises(ValidationError) as ctx:
            news.full_clean()
        self.assertIn("title", ctx.exception.message_dict)

    def test_date_and_time_cannot_be_in_the_future(self):
        tomorrow = timezone.now() + timedelta(days=1)
        news = News(title="Future", category=self.category, source="BBC",
                    content="x", date_and_time=tomorrow)
        with self.assertRaises(ValidationError) as ctx:
            news.full_clean()
        self.assertIn("date_and_time", ctx.exception.message_dict)


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.war = Category.objects.create(name="war")
        cls.nature = Category.objects.create(name="nature")
        cls.empty = Category.objects.create(name="economy")
        cls.oldest = make_news(cls.war, "Oldest", hours_ago=240)
        cls.newest = make_news(cls.nature, "Newest", hours_ago=0)
        for i in range(1, 5):
            make_news(cls.war, f"War story {i}", hours_ago=i)

    def test_news_is_newest_first(self):
        data = self.client.get(reverse("news:news-list")).json()
        timestamps = [item["date_and_time"] for item in data]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))
        self.assertEqual(data[0]["title"], "Newest")
        self.assertEqual(data[-1]["title"], "Oldest")

    def test_limit_returns_most_recent(self):
        data = self.client.get(reverse("news:news-list"), {"limit": 4}).json()
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]["title"], "Newest")

    def test_filter_by_category_only_returns_that_category(self):
        data = self.client.get(reverse("news:news-list"), {"category": self.war.id}).json()
        self.assertEqual(len(data), 5)
        self.assertTrue(all(item["category"]["name"] == "war" for item in data))

    def test_bad_query_params_are_rejected(self):
        url = reverse("news:news-list")
        self.assertEqual(self.client.get(url, {"limit": "abc"}).status_code, 400)
        self.assertEqual(self.client.get(url, {"category": "0"}).status_code, 400)

    def test_list_and_detail_return_the_same_full_content(self):
        list_item = self.client.get(reverse("news:news-list")).json()[0]
        detail_item = self.client.get(reverse("news:news-detail", args=[self.newest.id])).json()
        self.assertEqual(list_item["content"], self.newest.content)
        self.assertEqual(list_item, detail_item)

    def test_detail_404(self):
        self.assertEqual(self.client.get(reverse("news:news-detail", args=[9999])).status_code, 404)

    def test_categories_include_empty_ones_with_counts(self):
        data = {c["name"]: c["article_count"] for c in self.client.get(reverse("news:category-list")).json()}
        self.assertEqual(data, {"economy": 0, "nature": 1, "war": 5})

    def test_api_is_read_only(self):
        self.assertEqual(self.client.post(reverse("news:news-list"), {}).status_code, 405)
        self.assertEqual(self.client.delete(reverse("news:news-detail", args=[self.newest.id])).status_code, 405)

    def test_cors_header_for_frontend_origin(self):
        response = self.client.get(reverse("news:news-list"), headers={"Origin": "http://localhost:5173"})
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "http://localhost:5173")


class AdminTests(TestCase):
    def test_models_are_registered_and_deletion_asks_for_confirmation(self):
        from django.contrib.auth import get_user_model

        admin_user = get_user_model().objects.create_superuser("admin", password="pw-for-tests-123")
        self.client.force_login(admin_user)
        category = Category.objects.create(name="war")
        news = make_news(category)

        self.assertEqual(self.client.get("/admin/news/category/").status_code, 200)
        self.assertEqual(self.client.get("/admin/news/news/add/").status_code, 200)
        confirm = self.client.get(f"/admin/news/news/{news.id}/delete/")
        self.assertContains(confirm, "Are you sure")
        self.assertTrue(News.objects.filter(id=news.id).exists())  # not deleted by a GET

    def test_admin_rejects_empty_title_and_accepts_valid_article(self):
        from django.contrib.auth import get_user_model

        self.client.force_login(get_user_model().objects.create_superuser("admin", password="pw-for-tests-123"))
        category = Category.objects.create(name="war")
        url = "/admin/news/news/add/"
        form = {
            "title": "", "category": category.id, "source": "BBC",
            "date_and_time_0": timezone.localdate().isoformat(), "date_and_time_1": "12:00:00",
            "content": "Some text",
        }

        bad = self.client.post(url, form)
        self.assertEqual(bad.status_code, 200)  # form re-rendered with an error
        self.assertContains(bad, "This field is required")
        self.assertEqual(News.objects.count(), 0)

        form["title"] = "A valid headline"
        self.assertEqual(self.client.post(url, form).status_code, 302)
        self.assertEqual(News.objects.count(), 1)
