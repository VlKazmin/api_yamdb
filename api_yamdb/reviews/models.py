from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from users.models import User
from django.db import models
from users.models import User


class BaseModel(models.Model):
    """
    Абстрактная базовая модель, содержащая общие поля и
    валидацию для подклассов.
    """

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$",
                message="Неверное имя пользователя. "
                "Допускаются только буквы, цифры и знак подчеркивания."
                " Не может содержать символы «@», «.», «+» или «-».",
            )
        ],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ReviewCommentBaseModel(models.Model):
    """Базовый абстрактный класс для отзывов и комментариев."""

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
    )

    class Meta:
        abstract = True
        ordering = ["-pub_date"]


class Category(BaseModel):
    """
    Модель для категории.
    """

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(BaseModel):
    """
    Модель для жанра.
    """

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    """
    Модель для произведения.
    """

    name = models.TextField()
    year = models.SmallIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True,)
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"

    def __str__(self):
        return self.name


class Review(ReviewCommentBaseModel):
    """
    Модель для отзыва на произведение.
    """

    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )

    class Meta(ReviewCommentBaseModel.Meta):
        default_related_name = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            ),
        ]

        def __str__(self):
            return self.text


class Comment(ReviewCommentBaseModel):
    """
    Модель для комментария к отзыву.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
    )

    class Meta(ReviewCommentBaseModel.Meta):
        default_related_name = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
