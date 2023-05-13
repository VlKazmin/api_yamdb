from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from users.models import User
from django.db import models
from users.models import User

MAX_LENGHT: int = 20


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
        # это атрибут метакласса Meta в Django модели, который указывает,
        # что модель является абстрактной. Абстрактная модель не создает
        # отдельной таблицы в базе данных, она служит как базовый класс
        # для других моделей.
        abstract = True

    def __str__(self):
        return self.name[MAX_LENGHT]


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
    # вносим ограничение на уровне базы
    year = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[MAX_LENGHT]  # нужно вывести в переменную


class Review(models.Model):
    """
    Модель для отзыва на произведение.
    """

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            ),
        ]

    def __str__(self):
        return self.text[MAX_LENGHT]


class Comment(models.Model):
    """
    Модель для комментария к отзыву.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[MAX_LENGHT]
