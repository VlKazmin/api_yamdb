from rest_framework import serializers

from users.models import User
from reviews.models import Comment, Review
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "created")

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        title_id = self.context["view"].kwargs.get("title_id")
        author = self.context["request"].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "created")
        read_only_fields = ("id", "created")
