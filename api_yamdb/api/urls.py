from django.urls import include, path

from rest_framework import routers

from .views import UserCreateViewSet, UserGetTokenViewSet, UserViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="users")


auth_router_v1 = routers.SimpleRouter()
auth_router_v1.register(r"signup", UserCreateViewSet, basename="signup")
auth_router_v1.register(r"token", UserGetTokenViewSet, basename="token")


urlpatterns = [
    path("auth/", include(auth_router_v1.urls)),
    path("", include(router_v1.urls)),
]
