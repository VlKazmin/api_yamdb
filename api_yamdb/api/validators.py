from rest_framework import serializers

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
    Проверка, что username уникально.
    """
    username = data.get("username")
    email = data.get("email")

    if User.objects.exclude(username=username).filter(email=email).exists():
        raise serializers.ValidationError(
            f"Пользователь с именем '{username}' уже существует"
        )
    return data


def validate_email(data):
    """
    Проверка, что email уникален.
    """
    username = data.get("username")
    email = data.get("email")

    if User.objects.exclude(email=email).filter(username=username).exists():
        raise serializers.ValidationError(
            f"Пользователь с почтой '{email}' уже существует"
        )
    return data
