from rest_framework import serializers

from users.models import User
from .validators import validate_me, validate_email, validate_username


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

        validators = [
            validate_me,
            validate_username,
            validate_email,
        ]


class JwtTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    validators = [
        validate_me,
    ]
