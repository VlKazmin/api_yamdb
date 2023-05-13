from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed


class IsSuperUserOrAdmin(permissions.BasePermission):
    """Доступ только для суперпользователи или администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    """Доступ только для администратора, модератора и автора объекта."""

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        ):
            return True
        raise AuthenticationFailed("Требуется авторизация")

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        ):
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role in ["admin", "moderator"]
                or request.user.is_superuser
                or obj.author == request.user
            )
        raise AuthenticationFailed("Требуется авторизация")


class ReadOnly(permissions.BasePermission):
    """Только чтение."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
