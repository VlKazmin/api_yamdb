from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (
    IsAdminOrModeratorOrAuthor,
    IsSuperUserOrAdmin,
    ReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    JwtTokenSerializer,
    ReviewSerializer,
    TitleCreateUpdateSerializer,
    TitleSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from .utils import send_confirmation_code


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Представление для создания пользователя."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
            send_confirmation_code(
                user.email,
                default_token_generator,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UserGetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Представление  для создания JWT-токена и
    отправки кода для его получения."""

    queryset = User.objects.all()
    serializer_class = JwtTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")

        try:
            user = self.get_queryset().get(username=username)
        except User.DoesNotExist:
            message = {"Пользователь не найден."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        if default_token_generator.check_token(user, ""):
            message = {"Ваш token -": str(AccessToken.for_user(user))}
            return Response(message, status=status.HTTP_200_OK)

        message = {"Неправильный код подтверждения."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Представление  для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsSuperUserOrAdmin,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["=username"]
    lookup_field = "username"

    @action(
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        methods=["get", "patch"],
    )
    def me(self, request):
        """
        Получение данных о пользователе или внесение изменений
        в данные о пользователе.
        """
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if request.method == "GET":
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            serializer.validated_data["role"] = request.user.role
            serializer.save()
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryGenreViewSet(CreateDestroyListViewSet):
    """Базовый класс для представлений категорий и жанров."""

    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    http_method_names = ["post", "get", "delete"]
    search_fields = ["name"]
    permission_classes = [
        IsSuperUserOrAdmin | ReadOnly,
    ]

    lookup_field = "slug"


class CategoryViewSet(CategoryGenreViewSet):
    """Представление для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Представление для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    pagination_class = PageNumberPagination
    permission_classes = (IsSuperUserOrAdmin | ReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    ordering_fields = ["name"]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return TitleCreateUpdateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для  для создания, просмотра, обновления и удаления отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для  для создания, просмотра,
    обновления и удаления комментария
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
