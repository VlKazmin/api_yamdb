from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import (
    unique_review_validator,
    validate_email,
    validate_me,
    validate_username,
)


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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    rating = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "rating",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления объектов модели Title.
    """

    name = serializers.CharField(max_length=256)
    rating = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "rating",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        unique_review_validator(self.context, data)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "pub_date")
