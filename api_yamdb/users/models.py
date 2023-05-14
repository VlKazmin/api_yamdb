from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя с расширенным функционалом для Django приложения."""

    ROLE_CHOICES = [
        ("user", "User"),
        ("moderator", "Moderator"),
        ("admin", "Admin"),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^[\w]+[^@\.\+\-]*$",
                message="Неверное имя пользователя. "
                "Допускаются только буквы, цифры и знак подчеркивания."
                " Не может содержать символы «@», «.», «+» или «-».",
            )
        ],
        error_messages={
            "unique": "Пользователь с таким именем уже существует.",
        },
    )

    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=True
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    role = models.CharField(
        verbose_name="Роль",
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
    )
    confirmation_code = models.CharField(
        verbose_name="Код подтверждения",
        max_length=6,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        constraints = [
            models.UniqueConstraint(
                fields=("username", "email"), name="unique_username&email"
            )
        ]

    @property
    def is_admin(self):
        """Возвращает True, если пользователь является администратором."""
        return self.role == "admin"

    def __str__(self):
        return self.username
