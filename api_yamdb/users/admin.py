from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка пользователей."""

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
    )
    list_editable = ("role",)
    search_fields = (
        "username",
        "role",
    )
    list_filter = ("username",)
    empty_value_display = "-пусто-"
    list_per_page = 15
