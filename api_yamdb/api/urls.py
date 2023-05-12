from django.urls import include, path

from rest_framework import routers

from .views import (UserCreateViewSet, UserGetTokenViewSet, UserViewSet,
                    ReviewViewSet, CommentViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


auth_router_v1 = routers.SimpleRouter()
auth_router_v1.register(r"signup", UserCreateViewSet, basename="signup")
auth_router_v1.register(r"token", UserGetTokenViewSet, basename="token")


urlpatterns = [
    path("auth/", include(auth_router_v1.urls)),
    path("", include(router_v1.urls)),
]
