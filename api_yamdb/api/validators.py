from rest_framework import serializers

from reviews.models import Review
from users.models import User


def validate_me(data):
    """
    Проверка, что username не равно 'me'.
    """
    if data.get("username") == "me":
        raise serializers.ValidationError("Использовать имя 'me' запрещено")
    return data


def validate_username(data):
    """
    Проверка уникальности username.
    """
    username = data["username"]
    email = data["email"]

    if User.objects.exclude(email=email).filter(username=username).exists():
        raise serializers.ValidationError(
            "Пользователь с таким именем уже существует."
        )
    return data


def validate_email(data):
    """
    Проверка уникальности email.
    """
    username = data["username"]
    email = data["email"]

    if User.objects.exclude(username=username).filter(email=email).exists():
        raise serializers.ValidationError(
            "Пользователь с таким email уже существует."
        )
    return data


def unique_review_validator(context, data):
    """Валидатор, который проверяет уникальность отзыва
    для заданного произведения."""

    if context["request"].method == "POST":
        title_id = context["view"].kwargs.get("title_id")
        author = context["request"].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError("Отзыв уже существует.")
