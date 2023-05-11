from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed


class SuperUserOrAdmin(permissions.BasePermission):
    """Доступ только для суперпользователи или администратора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )
    

# class SuperUserOrAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS or (
#             request.user.is_authenticated and (
#                 request.user.is_admin or request.user.is_superuser
#             )
#         )


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """Доступ только для администратора, модератора и автора объекта."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or 	request.user.is_authenticated:
            return True
        raise AuthenticationFailed("Требуется авторизация")

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or 	request.user.is_authenticated:
            return (
                (obj.author == request.user)
                or request.user.is_admin
                or request.user.is_moderator
            )
        raise AuthenticationFailed("Требуется авторизация")
