"""Serve the built React app through Django templates (`npm run build:django`)."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from .templatetags.vite import load_manifest
from .views_auth import user_context


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SpaView(TemplateView):
    """Any front-end route (/, /news, /news/<id>, ...); React Router takes it from there."""

    template_name = "spa.html"

    def get(self, request, *args, **kwargs):
        try:
            load_manifest()
        except FileNotFoundError:
            return self.response_class(request, "build_missing.html", status=503)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_context"] = user_context(self.request.user)
        return context


class AdminSpaView(LoginRequiredMixin, UserPassesTestMixin, SpaView):
    """/admin: superusers only.

    Anonymous users are redirected to LOGIN_URL?next=/admin; a logged-in user
    who isn't a superuser gets PermissionDenied, rendered by templates/403.html.
    """

    def test_func(self):
        return self.request.user.is_superuser
