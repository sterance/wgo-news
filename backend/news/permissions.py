from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperuserOrReadOnly(BasePermission):
    """Anyone can read; only a logged-in superuser can create, change or delete."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)
