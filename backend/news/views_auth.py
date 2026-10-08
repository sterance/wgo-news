"""Session info for the React front end. Logging in happens on Django's admin login page."""

from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST


def user_context(user) -> dict:
    """The current user as the front end sees it."""
    return {
        "authenticated": user.is_authenticated,
        "username": user.get_username() if user.is_authenticated else None,
        "is_superuser": user.is_superuser,
    }


@require_GET
@ensure_csrf_cookie
def me(request):
    """GET /api/auth/me/ - who is logged in. Also sets the csrftoken cookie."""
    return JsonResponse(user_context(request.user))


@require_POST
def logout_view(request):
    """POST /api/auth/logout/ - end the session. CSRF-protected: send the X-CSRFToken header."""
    logout(request)
    return HttpResponse(status=204)
