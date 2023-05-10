from django.core.exceptions import ValidationError

from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


from .serializers import (
    UserCreateSerializer,
    JwtTokenSerializer,
)
from users.models import User
from .utils import send_confirmation_code, generate_confirm_code


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для создания пользователя."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
            confirmation_code = generate_confirm_code()
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_code(
                user.email,
                confirmation_code,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserGetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для создания JWT-токена и отправки кода для его получения."""

    queryset = User.objects.all()
    serializer_class = JwtTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = JwtTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")

        try:
            user = self.get_queryset().get(username=username)
        except User.DoesNotExist:
            message = {"Пользователь не найден."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        if User.objects.filter(confirmation_code=confirmation_code).exists():
            user.confirmation_code = None
            user.save()
            message = {"Ваш token -": str(AccessToken.for_user(user))}
            return Response(message, status=status.HTTP_200_OK)

        message = {"Неправильный код подтверждения."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления пользователями."""
    pass
