from rest_framework import permissions


class SuperUserOrAdmin(permissions.BasePermission):
    """Доступ только для суперпользователи или администратора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )
