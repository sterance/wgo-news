import json
import shutil
import tempfile
from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .admin import CategoryAdmin, NewsAdmin
from .forms import CategoryForm, NewsForm
from .models import Category, News


def make_news(category, title="A headline", hours_ago=0, **kwargs):
    defaults = {
        "source": "Reuters",
        "content": "Body text " * 40,
        "date_and_time": timezone.now() - timedelta(hours=hours_ago),
    }
    defaults.update(kwargs)
    return News.objects.create(title=title, category=category, **defaults)


def make_superuser(username="admin"):
    return get_user_model().objects.create_superuser(username, password="pw-for-tests-123")


def make_staff_user(username="staff"):
    return get_user_model().objects.create_user(username, password="pw-for-tests-123", is_staff=True)


class CategoryModelTests(TestCase):
    databases = {"default", "news"}

    def test_name_must_be_unique(self):
        Category.objects.create(name="war")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(name="war")

    def test_name_uniqueness_ignores_case(self):
        Category.objects.create(name="war")
        with self.assertRaises(ValidationError):
            Category(name="War").full_clean()

    def test_deleting_category_deletes_its_articles(self):
        category = Category.objects.create(name="war")
        other = Category.objects.create(name="nature")
        make_news(category)
        kept = make_news(other)
        category.delete()
        self.assertEqual(list(News.objects.all()), [kept])


class NewsModelTests(TestCase):
    databases = {"default", "news"}

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


class CategoryFormTests(TestCase):
    databases = {"default", "news"}

    def test_name_is_stripped(self):
        form = CategoryForm(data={"name": "  Science  "})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Science")

    def test_blank_name_is_rejected(self):
        form = CategoryForm(data={"name": "   "})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_duplicate_in_different_case_is_rejected_on_the_name_field(self):
        Category.objects.create(name="war")
        form = CategoryForm(data={"name": "WAR"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"name": ["A category with this name already exists."]})

    def test_exact_duplicate_gives_one_error(self):
        Category.objects.create(name="war")
        form = CategoryForm(data={"name": " war "})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors["name"]), 1)
        self.assertNotIn("__all__", form.errors)

    def test_renaming_to_a_different_case_of_itself_is_allowed(self):
        category = Category.objects.create(name="war")
        self.assertTrue(CategoryForm(data={"name": "War"}, instance=category).is_valid())


class NewsFormTests(TestCase):
    databases = {"default", "news"}

    def setUp(self):
        self.category = Category.objects.create(name="nature")

    def data(self, **overrides):
        data = {
            "title": "A headline",
            "category": self.category.id,
            "source": "BBC",
            "date_and_time": timezone.now() - timedelta(hours=1),
            "content": "Body",
        }
        data.update(overrides)
        return data

    def test_valid_data_passes(self):
        self.assertTrue(NewsForm(data=self.data()).is_valid())

    def test_blank_title_is_rejected(self):
        form = NewsForm(data=self.data(title="   "))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["This field is required."])

    def test_short_title_is_rejected(self):
        form = NewsForm(data=self.data(title="ab"))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["Ensure this value has at least 3 characters (it has 2)."])

    def test_future_date_is_rejected(self):
        form = NewsForm(data=self.data(date_and_time=timezone.now() + timedelta(days=1)))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"date_and_time": ["The date and time cannot be in the future."]})

    def test_title_and_source_are_stripped(self):
        form = NewsForm(data=self.data(title="  A headline  ", source="  BBC  "))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "A headline")
        self.assertEqual(form.cleaned_data["source"], "BBC")


class AdminUsesFormsTests(TestCase):
    def test_admin_classes_use_the_shared_forms(self):
        self.assertIs(NewsAdmin.form, NewsForm)
        self.assertIs(CategoryAdmin.form, CategoryForm)


class ApiTests(TestCase):
    databases = {"default", "news"}

    @classmethod
    def setUpTestData(cls):
        cls.superuser = make_superuser()
        cls.war = Category.objects.create(name="war")
        cls.nature = Category.objects.create(name="nature")
        cls.empty = Category.objects.create(name="economy")
        cls.oldest = make_news(cls.war, "Oldest", hours_ago=240)
        cls.newest = make_news(cls.nature, "Newest", hours_ago=0)
        for i in range(1, 5):
            make_news(cls.war, f"War story {i}", hours_ago=i)

    def setUp(self):
        # Writes need a superuser; reads work either way (see PermissionTests).
        self.client.force_login(self.superuser)

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

    def test_category_can_be_created_and_renamed(self):
        create = self.client.post(
            reverse("news:category-list"),
            {"name": "Science"},
            content_type="application/json",
        )
        self.assertEqual(create.status_code, 201)
        category_id = create.json()["id"]

        rename = self.client.patch(
            reverse("news:category-detail", args=[category_id]),
            {"name": "science and tech"},
            content_type="application/json",
        )
        self.assertEqual(rename.status_code, 200)
        self.assertEqual(rename.json()["name"], "science and tech")

    def test_category_delete_cascades_to_its_articles(self):
        response = self.client.delete(reverse("news:category-detail", args=[self.war.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(id=self.war.id).exists())
        self.assertFalse(News.objects.filter(category_id=self.war.id).exists())

    def test_empty_category_can_be_deleted(self):
        response = self.client.delete(reverse("news:category-detail", args=[self.empty.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(id=self.empty.id).exists())

    def test_create_news_accepts_category_id_and_returns_nested_category(self):
        response = self.client.post(
            reverse("news:news-list"),
            {
                "title": "A new story",
                "category": self.war.id,
                "source": "BBC",
                "date_and_time": "2026-09-30T12:00:00Z",
                "content": "A body of news content.",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["category"], {"id": self.war.id, "name": "war"})

    def test_update_news_supports_partial_payload(self):
        response = self.client.patch(
            reverse("news:news-detail", args=[self.newest.id]),
            {"title": "Updated headline"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated headline")

    def test_delete_news_removes_article(self):
        response = self.client.delete(reverse("news:news-detail", args=[self.newest.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(News.objects.filter(id=self.newest.id).exists())

    def test_writes_reject_invalid_data(self):
        response = self.client.post(
            reverse("news:news-list"),
            {"title": "No", "category": self.war.id, "source": "BBC", "content": "Body"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json())

    def test_future_date_is_rejected(self):
        response = self.client.patch(
            reverse("news:news-detail", args=[self.newest.id]),
            {"date_and_time": "2099-01-01T12:00:00Z"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("date_and_time", response.json())

    def test_short_title_error_message_is_unchanged(self):
        response = self.client.post(
            reverse("news:news-list"),
            {"title": "No", "category": self.war.id, "source": "BBC", "content": "Body"},
            content_type="application/json",
        )
        self.assertEqual(response.json(), {"title": ["Ensure this field has at least 3 characters."]})

    def test_blank_fields_error_messages_are_unchanged(self):
        response = self.client.post(
            reverse("news:news-list"),
            {"title": "  ", "category": self.war.id, "source": "", "content": "Body"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "title": ["This field may not be blank."],
            "source": ["This field may not be blank."],
        })

    def test_future_date_error_message_is_unchanged(self):
        response = self.client.patch(
            reverse("news:news-detail", args=[self.newest.id]),
            {"date_and_time": "2099-01-01T12:00:00Z"},
            content_type="application/json",
        )
        self.assertEqual(response.json(), {"date_and_time": ["The date and time cannot be in the future."]})

    def test_create_news_without_date_uses_the_default(self):
        response = self.client.post(
            reverse("news:news-list"),
            {"title": "No date", "category": self.war.id, "source": "BBC", "content": "Body"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_exact_duplicate_category_gives_one_name_error(self):
        response = self.client.post(reverse("news:category-list"), {"name": "war"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"name": ["category with this name already exists."]})

    def test_duplicate_category_in_different_case_gives_one_name_error(self):
        response = self.client.post(reverse("news:category-list"), {"name": "WAR"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"name": ["A category with this name already exists."]})

    def test_renaming_category_to_another_in_different_case_is_rejected(self):
        response = self.client.patch(
            reverse("news:category-detail", args=[self.nature.id]),
            {"name": "War"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"name": ["A category with this name already exists."]})

    def test_cors_header_for_frontend_origin(self):
        response = self.client.get(reverse("news:news-list"), headers={"Origin": "http://localhost:5173"})
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "http://localhost:5173")


class PermissionTests(TestCase):
    databases = {"default", "news"}

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="war")
        cls.news = make_news(cls.category)

    def writes(self):
        """(method, url, payload) for every write endpoint."""
        news_payload = {
            "title": "A new story", "category": self.category.id, "source": "BBC",
            "date_and_time": "2026-01-01T12:00:00Z", "content": "Body",
        }
        return [
            ("post", reverse("news:news-list"), news_payload),
            ("patch", reverse("news:news-detail", args=[self.news.id]), {"title": "Changed"}),
            ("delete", reverse("news:news-detail", args=[self.news.id]), None),
            ("post", reverse("news:category-list"), {"name": "science"}),
            ("patch", reverse("news:category-detail", args=[self.category.id]), {"name": "conflict"}),
            ("delete", reverse("news:category-detail", args=[self.category.id]), None),
        ]

    def send(self, method, url, payload):
        if payload is None:
            return getattr(self.client, method)(url)
        return getattr(self.client, method)(url, payload, content_type="application/json")

    def assert_all_writes_forbidden(self):
        for method, url, payload in self.writes():
            with self.subTest(method=method, url=url):
                self.assertEqual(self.send(method, url, payload).status_code, 403)
        self.assertTrue(News.objects.filter(id=self.news.id, title="A headline").exists())
        self.assertTrue(Category.objects.filter(id=self.category.id, name="war").exists())

    def test_anonymous_writes_are_forbidden(self):
        self.assert_all_writes_forbidden()

    def test_staff_who_is_not_a_superuser_cannot_write(self):
        self.client.force_login(make_staff_user())
        self.assert_all_writes_forbidden()

    def test_superuser_can_write(self):
        self.client.force_login(make_superuser())
        expected = [201, 200, 204, 201, 200, 204]
        for (method, url, payload), status in zip(self.writes(), expected):
            with self.subTest(method=method, url=url):
                self.assertEqual(self.send(method, url, payload).status_code, status)

    def test_anonymous_reads_are_allowed(self):
        for url in [
            reverse("news:news-list"),
            reverse("news:news-detail", args=[self.news.id]),
            reverse("news:category-list"),
            reverse("news:category-detail", args=[self.category.id]),
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_superuser_write_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(make_superuser())
        response = client.post(reverse("news:category-list"), {"name": "science"}, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Category.objects.filter(name="science").exists())

    def test_superuser_write_with_csrf_token_succeeds(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(make_superuser())
        client.get(reverse("news:auth-me"))
        token = client.cookies["csrftoken"].value
        response = client.post(
            reverse("news:category-list"), {"name": "science"},
            content_type="application/json", headers={"X-CSRFToken": token},
        )
        self.assertEqual(response.status_code, 201)


class AuthEndpointTests(TestCase):
    databases = {"default", "news"}

    def test_me_when_anonymous(self):
        response = self.client.get(reverse("news:auth-me"))
        self.assertEqual(response.json(), {"authenticated": False, "username": None, "is_superuser": False})
        self.assertIn("csrftoken", response.cookies)

    def test_me_as_staff_user(self):
        self.client.force_login(make_staff_user())
        response = self.client.get(reverse("news:auth-me"))
        self.assertEqual(response.json(), {"authenticated": True, "username": "staff", "is_superuser": False})
        self.assertIn("csrftoken", response.cookies)

    def test_me_as_superuser(self):
        self.client.force_login(make_superuser())
        response = self.client.get(reverse("news:auth-me"))
        self.assertEqual(response.json(), {"authenticated": True, "username": "admin", "is_superuser": True})
        self.assertIn("csrftoken", response.cookies)

    def test_logout_with_csrf_token_ends_the_session(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(make_superuser())
        client.get(reverse("news:auth-me"))
        token = client.cookies["csrftoken"].value

        response = client.post(reverse("news:auth-logout"), headers={"X-CSRFToken": token})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(client.get(reverse("news:auth-me")).json()["authenticated"])

    def test_logout_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(make_superuser())

        response = client.post(reverse("news:auth-logout"))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(client.get(reverse("news:auth-me")).json()["authenticated"])

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get(reverse("news:auth-logout")).status_code, 405)


@override_settings(
    STORAGES={
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class AdminTests(TestCase):
    databases = {"default", "news"}

    def test_models_are_registered_and_deletion_asks_for_confirmation(self):
        self.client.force_login(make_superuser())
        category = Category.objects.create(name="war")
        news = make_news(category)

        self.assertEqual(self.client.get("/django-admin/news/category/").status_code, 200)
        self.assertEqual(self.client.get("/django-admin/news/news/add/").status_code, 200)
        confirm = self.client.get(f"/django-admin/news/news/{news.id}/delete/")
        self.assertContains(confirm, "Are you sure")
        self.assertTrue(News.objects.filter(id=news.id).exists())  # not deleted by a GET

    def test_admin_rejects_empty_title_and_accepts_valid_article(self):
        self.client.force_login(make_superuser())
        category = Category.objects.create(name="war")
        url = "/django-admin/news/news/add/"
        form = {
            "title": "", "category": category.id, "source": "BBC",
            "date_and_time_0": (timezone.localdate() - timedelta(days=1)).isoformat(), "date_and_time_1": "12:00:00",
            "content": "Some text",
        }

        bad = self.client.post(url, form)
        self.assertEqual(bad.status_code, 200)  # form re-rendered with an error
        self.assertContains(bad, "This field is required")
        self.assertEqual(News.objects.count(), 0)

        form["title"] = "A valid headline"
        self.assertEqual(self.client.post(url, form).status_code, 302)
        self.assertEqual(News.objects.count(), 1)

    def test_django_admin_lives_at_django_admin(self):
        response = self.client.get("/django-admin/")
        self.assertRedirects(response, "/django-admin/login/?next=/django-admin/")
        self.assertEqual(self.client.get("/django-admin/login/").status_code, 200)

    def test_old_admin_path_no_longer_reaches_django_admin(self):
        for path in ["/admin/", "/admin/login/", "/admin/news/news/"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertNotContains(response, "Django administration", status_code=response.status_code)


PLAIN_STATIC_STORAGE = {"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}


class SpaTests(TestCase):
    """Django serving the built React app (npm run build:django), against a fake build."""

    databases = {"default", "news"}

    @classmethod
    def setUpClass(cls):
        cls.build_dir = Path(tempfile.mkdtemp())
        (cls.build_dir / ".vite").mkdir()
        (cls.build_dir / "assets").mkdir()
        (cls.build_dir / "assets" / "index-abc123.js").write_text("console.log('app')")
        (cls.build_dir / "assets" / "index-def456.css").write_text("body {}")
        (cls.build_dir / ".vite" / "manifest.json").write_text(json.dumps({
            "index.html": {
                "file": "assets/index-abc123.js",
                "src": "index.html",
                "isEntry": True,
                "css": ["assets/index-def456.css"],
            },
        }))
        cls.settings_override = override_settings(
            FRONTEND_BUILD_DIR=cls.build_dir,
            STATICFILES_DIRS=[cls.build_dir],
            STORAGES=PLAIN_STATIC_STORAGE,
        )
        cls.settings_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.settings_override.disable()
        shutil.rmtree(cls.build_dir)

    def assert_is_spa(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="root"></div>', html=True)
        self.assertContains(response, '<script type="module" src="/static/assets/index-abc123.js"></script>', html=True)
        self.assertContains(response, '<link rel="stylesheet" href="/static/assets/index-def456.css">', html=True)
        self.assertContains(response, '<script src="/static/theme-init.js"></script>', html=True)

    def test_front_end_routes_render_the_app(self):
        for path in ["/", "/news", "/news/5", "/some/unknown/page"]:
            with self.subTest(path=path):
                self.assert_is_spa(self.client.get(path))

    def test_page_includes_the_current_user_and_a_csrf_cookie(self):
        response = self.client.get("/")
        self.assertContains(
            response,
            '<script id="django-context" type="application/json">'
            '{"authenticated": false, "username": null, "is_superuser": false}</script>',
            html=True,
        )
        self.assertIn("csrftoken", response.cookies)

    def test_admin_redirects_anonymous_users_to_the_login(self):
        for path in ["/admin", "/admin/"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertRedirects(response, f"/django-admin/login/?next={path}", fetch_redirect_response=False)

    def test_admin_login_brings_the_user_back_to_admin(self):
        make_superuser()
        response = self.client.post(
            "/django-admin/login/?next=/admin",
            {"username": "admin", "password": "pw-for-tests-123", "next": "/admin"},
        )
        self.assertRedirects(response, "/admin", fetch_redirect_response=False)
        self.assert_is_spa(self.client.get("/admin"))

    def test_admin_is_forbidden_for_a_user_who_is_not_a_superuser(self):
        self.client.force_login(make_staff_user())
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Superuser required", status_code=403)
        self.assertContains(response, "staff", status_code=403)
        self.assertNotContains(response, 'id="root"', status_code=403)

    def test_admin_renders_the_app_for_a_superuser(self):
        self.client.force_login(make_superuser())
        response = self.client.get("/admin")
        self.assert_is_spa(response)
        self.assertContains(response, '"username": "admin", "is_superuser": true')

    def test_403_page_logout_button_logs_out(self):
        self.client.force_login(make_staff_user())
        self.client.get("/admin")
        response = self.client.post("/django-admin/logout/", {"next": "/"})
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertFalse(self.client.get(reverse("news:auth-me")).json()["authenticated"])

    def test_missing_build_shows_instructions(self):
        with override_settings(FRONTEND_BUILD_DIR=self.build_dir / "missing"):
            response = self.client.get("/news")
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "npm run build:django", status_code=503)

    def test_api_and_django_admin_are_not_swallowed_by_the_app(self):
        self.assertEqual(self.client.get(reverse("news:news-list")).headers["Content-Type"], "application/json")
        self.assertEqual(self.client.get("/api/does-not-exist/").status_code, 404)
        self.assertNotContains(self.client.get("/api/does-not-exist/"), 'id="root"', status_code=404)
        self.assertContains(self.client.get("/django-admin/login/"), "Django administration")
