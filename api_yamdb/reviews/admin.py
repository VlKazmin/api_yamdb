from django.contrib import admin

from .models import Title, Review, Comment, Genre, Category


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка произведений."""

    list_display = (
        "id",
        "name",
        "year",
        "description",
        "category",
    )
    list_editable = ("year", "category")
    search_fields = ("name", "year", "genre", "category")
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    list_per_page = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка отзывов."""

    list_display = ("pk", "author", "title", "text", "score", "pub_date")
    search_fields = ("author", "title", "text")
    list_filter = ("author",)
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка комментариев."""

    list_display = ("pk", "author", "review", "text", "pub_date")
    search_fields = ("author", "text", "pub_date")
    list_filter = ("author",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка жанров."""

    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ("slug",)
    list_filter = ("slug",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка категорий."""

    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ("slug",)
    list_filter = ("slug",)
