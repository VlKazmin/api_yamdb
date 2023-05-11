from django.urls import include, path

from rest_framework import routers

from .views import UserCreateViewSet, UserGetTokenViewSet, UserViewSet, ReviewViewSet, CommentViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
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
