from django.urls import include, path

from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserCreateViewSet,
    UserGetTokenViewSet,
    UserViewSet,
)

app_name = "api"

# Роутер для API версии 1
router_v1 = routers.DefaultRouter()
router_v1.register("categories", CategoryViewSet, basename="category")
router_v1.register("genres", GenreViewSet, basename="genre")
router_v1.register("titles", TitleViewSet, basename="title")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(r"users", UserViewSet, basename="users")

# Роутер для авторизации
auth_router_v1 = routers.SimpleRouter()
auth_router_v1.register(r"signup", UserCreateViewSet, basename="signup")
auth_router_v1.register(r"token", UserGetTokenViewSet, basename="token")

# URL-шаблоны
urlpatterns = [
    path("auth/", include(auth_router_v1.urls)),
    path("", include(router_v1.urls)),
]
